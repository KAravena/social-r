/**
 * Social R - Cloud Progress Adapter
 * Handles communication with Supabase Edge Functions, offline resilience queue,
 * monotonic progress merging, and sync status state.
 */
(function () {
  "use strict";

  class CloudProgressAdapter {
    constructor(options = {}) {
      this.courseId = options.courseId || "intro-r";
      this.config = (window.SocialR && window.SocialR.cloudConfig) || null;
      this.syncDebounceTimer = null;
      this.pendingSyncPayload = null;
      this.status = "idle"; // "idle" | "syncing" | "synced" | "offline" | "error"

      this._setupNetworkListeners();
    }

    _getQueueKey() {
      const studentId = this.config ? this.config.getStudentId() : null;
      return studentId ? `social-r:sync-queue:${this.courseId}:${studentId}` : `social-r:sync-queue:${this.courseId}`;
    }

    _setupNetworkListeners() {
      if (typeof window === "undefined") return;

      window.addEventListener("online", () => {
        console.info("[CloudAdapter] Network online detected. Processing offline queue...");
        this.setStatus("syncing");
        this.processOfflineQueue();
      });

      window.addEventListener("offline", () => {
        console.warn("[CloudAdapter] Network offline detected.");
        this.setStatus("offline");
      });
    }

    setStatus(status, message = "") {
      this.status = status;
      if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.emit === "function") {
        window.SocialR.events.emit("cloud_sync_status", { status, message });
      }
    }

    /**
     * Resolves public Supabase API key (modern publishable key preferred)
     */
    getApiKey() {
      return (this.config && (this.config.supabasePublishableKey || this.config.supabaseAnonKey)) || "";
    }

    /**
     * Authenticates student by RUT without password.
     */
    async login(rawRut) {
      if (!this.config || !this.config.isCloudEnabled()) {
        throw new Error("El servicio de sincronización en la nube no está configurado.");
      }

      const validator = window.SocialR && window.SocialR.RutValidator;
      if (validator && !validator.validate(rawRut)) {
        throw new Error("Revisa el RUT o IPE ingresado.");
      }

      const url = `${this.config.getFunctionsBaseUrl()}/student-login`;
      this.setStatus("syncing", "Iniciando sesión...");

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            apikey: this.getApiKey(),
          },
          body: JSON.stringify({
            rut: rawRut,
            courseId: this.courseId,
          }),
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
          this.setStatus("error", data.message || "Error al iniciar sesión.");
          throw new Error(data.message || "Error al iniciar sesión en el curso.");
        }

        // Save session locally
        this.config.setSession(data);
        this.setStatus("synced", "Sesión iniciada");
        return data;
      } catch (err) {
        this.setStatus("error", err.message);
        throw err;
      }
    }

    /**
     * Logs out active student and revokes session.
     */
    async logout() {
      const session = this.config ? this.config.getSession() : null;
      if (!session) return;

      const url = `${this.config.getFunctionsBaseUrl()}/student-logout`;

      try {
        await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.sessionToken}`,
            apikey: this.getApiKey(),
          },
        });
      } catch (err) {
        console.warn("[CloudAdapter] Logout request error (clearing local session regardless):", err);
      } finally {
        this.config.clearSession();
        this.setStatus("idle", "Sesión cerrada");
      }
    }

    /**
     * Fetches remote student progress from cloud.
     */
    async fetchCloudProgress() {
      const session = this.config ? this.config.getSession() : null;
      if (!session || !this.config.isCloudEnabled()) {
        return null;
      }

      const url = `${this.config.getFunctionsBaseUrl()}/student-progress-get?courseId=${this.courseId}`;

      try {
        this.setStatus("syncing", "Cargando progreso...");
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${session.sessionToken}`,
            apikey: this.getApiKey(),
          },
        });

        if (response.status === 401) {
          // Token expired or invalid
          console.warn("[CloudAdapter] Session token rejected. Clearing session.");
          this.config.clearSession();
          this.setStatus("offline", "Sesión expirada");
          return null;
        }

        if (!response.ok) {
          throw new Error("No se pudo obtener el progreso remoto.");
        }

        const data = await response.json();
        this.setStatus("synced", "Progreso actualizado");
        return data;
      } catch (err) {
        console.warn("[CloudAdapter] Error fetching cloud progress:", err);
        this.setStatus("offline", "Modo sin conexión");
        return null;
      }
    }

    /**
     * Merges remote cloud data into local state following monotonic rules:
     * - Exercises: Union of sets (completed = true always wins).
     * - Challenges: 'passed' is monotonic and is never downgraded.
     * - Drafts: Keep drafts, add remote drafts if not present locally.
     */
    mergeIntoLocalState(localState, cloudData) {
      if (!cloudData || typeof cloudData !== "object") return localState;

      // 1. Merge completed exercises
      if (Array.isArray(cloudData.completedExercises)) {
        cloudData.completedExercises.forEach((exId) => {
          // Find matching module
          const modSlugs = Object.keys(localState.modules || {});
          let targetMod = null;
          for (const slug of modSlugs) {
            const m = localState.modules[slug];
            if (m && m.completedExercises && m.completedExercises.includes(exId)) {
              targetMod = m;
              break;
            }
          }

          if (!targetMod) {
            // Infer module slug
            const match = exId.match(/intro-r-(\d{2})-\d{3}/);
            if (match) {
              const num = parseInt(match[1], 10);
              const slug = modSlugs[num - 1];
              if (slug && localState.modules[slug]) {
                targetMod = localState.modules[slug];
              }
            }
          }

          if (targetMod && !targetMod.completedExercises.includes(exId)) {
            targetMod.completedExercises.push(exId);
          }
        });
      }

      // 2. Merge challenges
      if (cloudData.challenges && typeof cloudData.challenges === "object") {
        localState.challenges = localState.challenges || {};
        for (const [modId, ch] of Object.entries(cloudData.challenges)) {
          if (!ch || typeof ch !== "object") continue;
          const currentStatus = localState.challenges[modId] ? localState.challenges[modId].status : "available";

          if (ch.status === "passed" || currentStatus === "passed") {
            localState.challenges[modId] = {
              status: "passed",
              passedAt: ch.passedAt || (localState.challenges[modId] && localState.challenges[modId].passedAt) || new Date().toISOString(),
            };
            if (localState.modules && localState.modules[modId]) {
              localState.modules[modId].accredited = true;
            }
          } else if (ch.status) {
            localState.challenges[modId] = {
              status: ch.status,
              passedAt: ch.passedAt || null,
            };
          }
        }
      }

      // 3. Merge drafts (editor state)
      if (cloudData.editorState && typeof cloudData.editorState === "object") {
        localState.editorState = localState.editorState || {};
        for (const [exId, code] of Object.entries(cloudData.editorState)) {
          if (!localState.editorState[exId] && typeof code === "string" && code.trim().length > 0) {
            localState.editorState[exId] = code;
          }
        }
      }

      return localState;
    }

    /**
     * Schedules a debounced sync of progress state to the cloud.
     */
    queueSync(progressState) {
      if (!this.config || !this.config.isCloudEnabled() || !this.config.isAuthenticated()) {
        return; // Pure local mode or unauthenticated
      }

      // Extract all completed exercises across modules
      const completedExercises = [];
      if (progressState.modules) {
        Object.values(progressState.modules).forEach((m) => {
          if (Array.isArray(m.completedExercises)) {
            m.completedExercises.forEach((id) => completedExercises.push(id));
          }
        });
      }

      const isDraftSync = this.config && typeof this.config.isDraftSyncEnabled === "function"
        ? this.config.isDraftSyncEnabled()
        : false;

      const payload = {
        courseId: this.courseId,
        completedExercises: [...new Set(completedExercises)],
        challenges: progressState.challenges || {},
        editorDrafts: isDraftSync ? (progressState.editorState || {}) : {},
        syncedAt: new Date().toISOString(),
      };

      this.pendingSyncPayload = payload;

      if (this.syncDebounceTimer) {
        clearTimeout(this.syncDebounceTimer);
      }

      this.setStatus("syncing", "Guardando...");
      this.syncDebounceTimer = setTimeout(() => {
        this.dispatchSync(this.pendingSyncPayload);
      }, 1000);
    }

    /**
     * Sends payload to server; if fails or offline, stores in offline queue.
     */
    async dispatchSync(payload) {
      if (!payload) return;
      const session = this.config.getSession();
      if (!session) return;

      if (typeof navigator !== "undefined" && !navigator.onLine) {
        console.warn("[CloudAdapter] Offline. Enqueuing sync mutation.");
        this._enqueueOffline(payload);
        this.setStatus("offline", "Sin conexión (guardado local)");
        return;
      }

      const url = `${this.config.getFunctionsBaseUrl()}/student-progress-sync`;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.sessionToken}`,
            apikey: this.getApiKey(),
          },
          body: JSON.stringify(payload),
        });

        if (response.status === 401) {
          console.warn("[CloudAdapter] Session expired during sync.");
          this.config.clearSession();
          this.setStatus("offline", "Sesión expirada");
          return;
        }

        if (!response.ok) {
          throw new Error("HTTP error during progress sync.");
        }

        this.setStatus("synced", "✓ Guardado en la nube");
      } catch (err) {
        console.warn("[CloudAdapter] Sync failed, caching to offline queue:", err);
        this._enqueueOffline(payload);
        this.setStatus("offline", "Sin conexión (guardado local)");
      }
    }

    _enqueueOffline(payload) {
      try {
        const queueKey = this._getQueueKey();
        window.localStorage.setItem(queueKey, JSON.stringify(payload));
      } catch (e) {
        console.warn("[CloudAdapter] Could not save to offline queue:", e);
      }
    }

    /**
     * Retries any pending mutations in the offline queue.
     */
    async processOfflineQueue() {
      try {
        const queueKey = this._getQueueKey();
        const raw = window.localStorage.getItem(queueKey);
        if (!raw) return;

        const payload = JSON.parse(raw);
        if (payload) {
          await this.dispatchSync(payload);
          window.localStorage.removeItem(queueKey);
        }
      } catch (e) {
        console.warn("[CloudAdapter] Error draining offline queue:", e);
      }
    }

    /**
     * Resets progress on server for active student.
     */
    async resetCloudProgress() {
      const session = this.config ? this.config.getSession() : null;
      if (!session || !this.config.isCloudEnabled()) return;

      const url = `${this.config.getFunctionsBaseUrl()}/student-reset`;

      try {
        await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session.sessionToken}`,
            apikey: this.getApiKey(),
          },
          body: JSON.stringify({ courseId: this.courseId }),
        });
        this.setStatus("synced", "Progreso reiniciado en la nube");
      } catch (err) {
        console.warn("[CloudAdapter] Error resetting cloud progress:", err);
      }
    }

    /**
     * Terminates active session on remote backend and locally resets sync status
     */
    async logout() {
      const session = this.config ? this.config.getSession() : null;
      if (session && session.sessionToken && this.config.isCloudEnabled()) {
        const url = `${this.config.getFunctionsBaseUrl()}/student-logout`;
        try {
          await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${session.sessionToken}`,
              apikey: this.getApiKey(),
            },
            body: JSON.stringify({ courseId: this.courseId }),
          });
        } catch (err) {
          console.warn("[CloudAdapter] Error notifying server of logout:", err);
        }
      }
      if (this.config && typeof this.config.clearSession === "function") {
        this.config.clearSession();
      }
      this.setStatus("offline", "Sesión cerrada");
    }
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.CloudProgressAdapter = CloudProgressAdapter;
  window.SocialR.cloudAdapter = new CloudProgressAdapter();

  if (typeof module !== "undefined" && module.exports) {
    module.exports = CloudProgressAdapter;
  }
})();
