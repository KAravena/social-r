/**
 * Social R - Cloud Sync & Authentication Configuration
 * Central configuration and session manager for cloud progress persistence.
 */
(function () {
  "use strict";

  // Production base public configuration (Strictly public endpoints; secrets are NEVER in client)
  const PRODUCTION_PUBLIC_CONFIG = {
    supabaseUrl: "https://ecxxebchsuxkmhhnpvub.supabase.co",
    supabasePublishableKey: "sb_publishable_Vz6kVXQoddw_RJmb74lR8Q_6LvHpFgL",
    courseId: "intro-r",
    cloudProgressEnabled: true,
    syncDraftsToCloud: false,
  };

  // Host protection: overrides enabling cloud are strictly restricted to localhost / 127.0.0.1
  const isLocalhost = typeof window !== "undefined" && Boolean(
    window.location && (
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      window.location.hostname === "::1" ||
      window.location.hostname === "[::1]"
    )
  );

  // Global override from window (e.g. from environment or meta tag)
  const userConfig = (window.SocialR && window.SocialR.cloudConfig) || window.SocialRCloudConfig || {};

  // Resolve cloud progress feature flag:
  // In production (non-localhost), value is strictly determined by PRODUCTION_PUBLIC_CONFIG.cloudProgressEnabled.
  // Developer overrides (window / localStorage) are strictly restricted to localhost / 127.0.0.1.
  let resolvedCloudProgressEnabled = PRODUCTION_PUBLIC_CONFIG.cloudProgressEnabled;
  if (isLocalhost) {
    const localDevConfig =
      (window.SocialR && window.SocialR.localDevConfig) ||
      window.SocialRLocalDevConfig ||
      null;

    if (localDevConfig && typeof localDevConfig === "object") {
      if (typeof localDevConfig.cloudProgressEnabled === "boolean") {
        resolvedCloudProgressEnabled = localDevConfig.cloudProgressEnabled;
      }
    } else if (typeof userConfig.cloudProgressEnabled === "boolean") {
      resolvedCloudProgressEnabled = userConfig.cloudProgressEnabled;
    } else if (typeof userConfig.cloudSyncEnabled === "boolean") {
      resolvedCloudProgressEnabled = userConfig.cloudSyncEnabled;
    } else if (typeof userConfig.CLOUD_SYNC_ENABLED === "boolean") {
      resolvedCloudProgressEnabled = userConfig.CLOUD_SYNC_ENABLED;
    } else {
      // Local storage developer switch (only active on localhost)
      try {
        const storedOverride = window.localStorage && window.localStorage.getItem("social-r:dev:cloud-enabled");
        if (storedOverride === "true") {
          resolvedCloudProgressEnabled = true;
        } else if (storedOverride === "false") {
          resolvedCloudProgressEnabled = false;
        }
      } catch (_) {}
    }
  } else {
    // In production environments (such as karavena.github.io), strictly follow PRODUCTION_PUBLIC_CONFIG
    resolvedCloudProgressEnabled = PRODUCTION_PUBLIC_CONFIG.cloudProgressEnabled;
  }

  const CloudConfig = {
    courseId: userConfig.courseId || PRODUCTION_PUBLIC_CONFIG.courseId,
    // Supabase project endpoints (Only modern public publishable key is safe in client; secret key is NEVER here)
    supabaseUrl: userConfig.supabaseUrl || userConfig.SUPABASE_URL || PRODUCTION_PUBLIC_CONFIG.supabaseUrl,
    supabasePublishableKey: userConfig.supabasePublishableKey || userConfig.SUPABASE_PUBLISHABLE_KEY || userConfig.supabaseAnonKey || userConfig.SUPABASE_ANON_KEY || PRODUCTION_PUBLIC_CONFIG.supabasePublishableKey,

    // Legacy compatibility getter (isolated fallback)
    get supabaseAnonKey() {
      return this.supabasePublishableKey;
    },

    // Feature Flag: If false, Social R operates in pure local-only mode (identical to legacy behavior)
    // If true and supabaseUrl is configured, RUT authentication & cloud sync are activated.
    get cloudProgressEnabled() {
      return this.cloudSyncEnabled;
    },

    cloudSyncEnabled: resolvedCloudProgressEnabled,

    // Draft Sync Policy (MVP Free-Tier: strictly false = local-only in localStorage, 0 cloud requests)
    syncDraftsToCloud: false,

    // Storage keys
    sessionStorageKey: "social-r:auth:session",
    guestModeStorageKey: "social-r:auth:guest-mode",
    legacyProgressKey: "social-r:progress:intro-r",

    /**
     * Checks if user has explicitly chosen Guest Mode ("Continuar sin iniciar sesión")
     */
    isGuestMode() {
      try {
        return Boolean(window.localStorage && window.localStorage.getItem(this.guestModeStorageKey) === "true");
      } catch (_) {
        return false;
      }
    },

    /**
     * Sets or unsets guest mode
     */
    setGuestMode(enabled = true) {
      try {
        if (enabled) {
          window.localStorage.setItem(this.guestModeStorageKey, "true");
        } else {
          window.localStorage.removeItem(this.guestModeStorageKey);
        }
        if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.emit === "function") {
          window.SocialR.events.emit("guest_mode_changed", { guest: Boolean(enabled) });
        }
        if (typeof window !== "undefined" && typeof window.dispatchEvent === "function") {
          window.dispatchEvent(new CustomEvent("social-r:guest_mode_changed", { detail: { guest: Boolean(enabled) } }));
        }
      } catch (err) {
        console.warn("[CloudConfig] Error setting guest mode:", err);
      }
    },

    clearGuestMode() {
      this.setGuestMode(false);
    },

    /**
     * Checks if cloud progress sync is active and configured
     */
    isCloudEnabled() {
      return Boolean(this.cloudSyncEnabled && this.supabaseUrl);
    },

    /**
     * Checks if code drafts should sync to cloud (MVP Free-Tier: false)
     */
    isDraftSyncEnabled() {
      return Boolean(this.isCloudEnabled() && this.syncDraftsToCloud);
    },

    /**
     * Returns the base URL for Edge Functions
     */
    getFunctionsBaseUrl() {
      if (!this.supabaseUrl) return "";
      const base = this.supabaseUrl.replace(/\/+$/, "");
      return `${base}/functions/v1`;
    },

    /**
     * Retrieves current active session if valid and not expired
     */
    getSession() {
      try {
        const raw = window.localStorage.getItem(this.sessionStorageKey);
        if (!raw) return null;
        const session = JSON.parse(raw);
        if (!session || !session.sessionToken || !session.student) {
          return null;
        }

        // Expiration check
        if (session.expiresAt) {
          const expTime = new Date(session.expiresAt).getTime();
          if (Date.now() > expTime) {
            console.info("[CloudConfig] Session has expired. Clearing.");
            this.clearSession();
            return null;
          }
        }
        return session;
      } catch (err) {
        console.warn("[CloudConfig] Error reading session:", err);
        return null;
      }
    },

    /**
     * Saves session payload to localStorage
     */
    setSession(sessionData) {
      if (!sessionData) return;
      try {
        this.clearGuestMode();
        window.localStorage.setItem(this.sessionStorageKey, JSON.stringify(sessionData));
        if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.emit === "function") {
          window.SocialR.events.emit("auth_state_changed", { authenticated: true, session: sessionData });
        }
        if (typeof window !== "undefined" && typeof window.dispatchEvent === "function") {
          window.dispatchEvent(new CustomEvent("social-r:auth_state_changed", { detail: { authenticated: true, session: sessionData } }));
        }
      } catch (err) {
        console.warn("[CloudConfig] Error saving session:", err);
      }
    },

    /**
     * Clears session from localStorage
     */
    clearSession() {
      try {
        window.localStorage.removeItem(this.sessionStorageKey);
        if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.emit === "function") {
          window.SocialR.events.emit("auth_state_changed", { authenticated: false, session: null });
        }
        if (typeof window !== "undefined" && typeof window.dispatchEvent === "function") {
          window.dispatchEvent(new CustomEvent("social-r:auth_state_changed", { detail: { authenticated: false, session: null } }));
        }
      } catch (err) {
        console.warn("[CloudConfig] Error clearing session:", err);
      }
    },

    /**
     * Returns true if a valid student session is active
     */
    isAuthenticated() {
      return this.getSession() !== null;
    },

    /**
     * Returns active student UUID, or null
     */
    getStudentId() {
      const session = this.getSession();
      return (session && session.student && (session.student.studentId || session.student.id)) || null;
    },

    /**
     * Returns active student display name, or null
     */
    getDisplayName() {
      const session = this.getSession();
      return (session && session.student && session.student.displayName) || null;
    },

    /**
     * Extracts a friendly short first name from a full display name.
     * Rules:
     * - Case A (institutional format with comma): "Apellidos, Nombre SegundoNombre" -> first token after comma ("Nombre")
     * - Case B (conventional format without comma): "Nombre SegundoNombre Apellidos" -> first token ("Nombre")
     * - Case C (extra whitespace): cleanly trimmed and tokenized
     * - Case D (empty/null/undefined/non-string): returns fallback ("Estudiante") without throwing
     *
     * @param {string} [displayName] - Optional. If omitted/undefined, resolves from active session.
     * @param {string} [fallback="Estudiante"] - Fallback if no valid first name found.
     * @returns {string} First name or fallback.
     */
    getFirstName(displayName, fallback = "Estudiante") {
      let raw = displayName;
      if (raw === undefined && typeof this === "object" && this !== null && typeof this.getDisplayName === "function") {
        raw = this.getDisplayName();
      }
      if (!raw || typeof raw !== "string") {
        return fallback;
      }
      const trimmed = raw.trim();
      if (!trimmed) {
        return fallback;
      }
      if (trimmed.includes(",")) {
        const commaIndex = trimmed.indexOf(",");
        const afterComma = trimmed.slice(commaIndex + 1).trim();
        if (afterComma) {
          const tokens = afterComma.split(/\s+/).filter(Boolean);
          if (tokens.length > 0) {
            return tokens[0];
          }
        }
        // Fallback if nothing after comma (e.g. "Rojas, ")
        const beforeTokens = trimmed.slice(0, commaIndex).trim().split(/\s+/).filter(Boolean);
        return beforeTokens.length > 0 ? beforeTokens[0] : fallback;
      }
      const tokens = trimmed.split(/\s+/).filter(Boolean);
      return tokens.length > 0 ? tokens[0] : fallback;
    },

    /**
     * Returns active student masked RUT (e.g. ••.•••.678-9), or null
     */
    getRutMasked() {
      const session = this.getSession();
      return (session && session.student && session.student.rutMasked) || null;
    },

    /**
     * Resolves the namespaced localStorage key for the given course.
     * When authenticated: 'social-r:progress:<courseId>:<studentId>'
     * When unauthenticated: 'social-r:progress:<courseId>'
     */
    getProgressNamespace(courseId = "intro-r") {
      const studentId = this.getStudentId();
      if (studentId) {
        return `social-r:progress:${courseId}:${studentId}`;
      }
      return `social-r:progress:${courseId}`;
    },

    /**
     * Checks if unauthenticated legacy progress exists with completed exercises or passed challenges
     */
    hasLegacyProgress(courseId = "intro-r") {
      try {
        const raw = window.localStorage.getItem(`social-r:progress:${courseId}`);
        if (!raw) return false;
        const parsed = JSON.parse(raw);
        if (!parsed) return false;

        let hasCompletedExercises = false;
        if (parsed.modules && typeof parsed.modules === "object") {
          hasCompletedExercises = Object.values(parsed.modules).some(
            (m) => Array.isArray(m.completedExercises) && m.completedExercises.length > 0
          );
        } else if (Array.isArray(parsed.completed) && parsed.completed.length > 0) {
          hasCompletedExercises = true;
        }

        let hasPassedChallenges = false;
        if (parsed.challenges && typeof parsed.challenges === "object") {
          hasPassedChallenges = Object.values(parsed.challenges).some(
            (c) => c && c.status === "passed"
          );
        }

        return hasCompletedExercises || hasPassedChallenges;
      } catch (err) {
        return false;
      }
    },

    /**
     * Checks if current runtime is localhost / 127.0.0.1
     */
    isLocalEnvironment() {
      return isLocalhost;
    },

    /**
     * Reads unauthenticated legacy progress
     */
    getLegacyProgress(courseId = "intro-r") {
      try {
        const raw = window.localStorage.getItem(`social-r:progress:${courseId}`);
        return raw ? JSON.parse(raw) : null;
      } catch (err) {
        return null;
      }
    },

    /**
     * Cleans unauthenticated legacy progress from browser storage (e.g. after migration or shared computer decision)
     */
    clearLegacyProgress(courseId = "intro-r") {
      try {
        window.localStorage.removeItem(`social-r:progress:${courseId}`);
        window.localStorage.removeItem(`social-r:progress:${courseId}:01-primeros-pasos`);
      } catch (err) {
        console.warn("[CloudConfig] Error clearing legacy progress:", err);
      }
    }
  };

  window.SocialR = window.SocialR || {};
  window.SocialR.cloudConfig = CloudConfig;
  window.SocialR.getFirstName = function (displayName, fallback) {
    return CloudConfig.getFirstName(displayName, fallback);
  };

  // Local development helpers (strictly guarded by isLocalhost)
  window.SocialR.enableLocalCloud = function () {
    if (!isLocalhost) {
      console.warn("[SocialR] Local cloud activation is strictly forbidden on non-localhost hosts.");
      return false;
    }
    try {
      window.localStorage.setItem("social-r:dev:cloud-enabled", "true");
      console.info("[SocialR] Local cloud override ENABLED for localhost. Reloading...");
      window.location.reload();
      return true;
    } catch (e) {
      console.error("[SocialR] Failed to set local cloud override:", e);
      return false;
    }
  };

  window.SocialR.disableLocalCloud = function () {
    try {
      window.localStorage.removeItem("social-r:dev:cloud-enabled");
      console.info("[SocialR] Local cloud override DISABLED. Reloading...");
      window.location.reload();
      return true;
    } catch (e) {
      console.error("[SocialR] Failed to remove local cloud override:", e);
      return false;
    }
  };

  window.SocialR.isLocalCloudOverridden = function () {
    if (!isLocalhost) return false;
    try {
      return window.localStorage.getItem("social-r:dev:cloud-enabled") === "true";
    } catch (_) {
      return false;
    }
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = CloudConfig;
  }
})();
