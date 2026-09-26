/**
 * Social R Platform - ProgressStore Architecture v2.0
 * Manages modular progress persistence, independent module progression,
 * per-module exercise tracking, editor state persistence, and v1 -> v2 automatic schema migration.
 */
(function () {
  "use strict";

  class ProgressStore {
    load() {
      throw new Error("[ProgressStore] load() must be implemented by subclass.");
    }
    save() {
      throw new Error("[ProgressStore] save() must be implemented by subclass.");
    }
    setCurrentExercise(exerciseId, moduleId) {
      throw new Error("[ProgressStore] setCurrentExercise() must be implemented by subclass.");
    }
    markCompleted(exerciseId, moduleId) {
      throw new Error("[ProgressStore] markCompleted() must be implemented by subclass.");
    }
    saveEditorCode(exerciseId, code) {
      throw new Error("[ProgressStore] saveEditorCode() must be implemented by subclass.");
    }
    resetProgress() {
      throw new Error("[ProgressStore] resetProgress() must be implemented by subclass.");
    }
  }

  class LocalProgressStore extends ProgressStore {
    constructor(options = {}) {
      super();
      this.courseId = options.courseId || "intro-r";
      this.version = 2;
      this.contentVersion = "3.0-global-pedagogical-standard";
      this.namespace = `social-r:progress:${this.courseId}`;
      this.legacyNamespace = `social-r:progress:${this.courseId}:01-primeros-pasos`;

      this._debounceTimer = null;
      this._pendingEditorState = {};
      this.state = this.load();
    }

    getDefaultModules() {
      const moduleSlugs = [
        "01-empezar-a-pensar-con-r",
        "02-trabajar-con-varios-valores",
        "03-hacer-preguntas-a-los-datos",
        "04-entender-una-base-de-datos",
        "05-seleccionar-y-filtrar-datos",
        "06-trabajar-cuando-faltan-datos",
        "07-describir-categorias",
        "08-describir-cantidades",
        "09-ver-relaciones-entre-dos-cantidades",
        "10-elegir-y-evaluar-una-correlacion",
        "11-trabajar-con-varias-correlaciones",
        "12-relacionar-categorias",
        "13-de-la-pregunta-al-analisis"
      ];
      const mods = {};
      moduleSlugs.forEach((slug, idx) => {
        const modNumStr = String(idx + 1).padStart(2, "0");
        mods[slug] = {
          id: slug,
          currentExerciseId: `intro-r-${modNumStr}-001`,
          completedExercises: [],
          completed: false,
        };
      });
      return mods;
    }

    getDefaultState() {
      return {
        version: this.version,
        courseId: this.courseId,
        activeModuleId: "01-empezar-a-pensar-con-r",
        currentExerciseId: "intro-r-01-001",
        modules: this.getDefaultModules(),
        challenges: {},
        editorState: {},
        lastActivity: new Date().toISOString(),
      };
    }

    inferModuleId(exerciseId) {
      if (!exerciseId || typeof exerciseId !== "string") return "01-empezar-a-pensar-con-r";
      const moduleSlugs = [
        "01-empezar-a-pensar-con-r",
        "02-trabajar-con-varios-valores",
        "03-hacer-preguntas-a-los-datos",
        "04-entender-una-base-de-datos",
        "05-seleccionar-y-filtrar-datos",
        "06-trabajar-cuando-faltan-datos",
        "07-describir-categorias",
        "08-describir-cantidades",
        "09-ver-relaciones-entre-dos-cantidades",
        "10-elegir-y-evaluar-una-correlacion",
        "11-trabajar-con-varias-correlaciones",
        "12-relacionar-categorias",
        "13-de-la-pregunta-al-analisis"
      ];
      const match = exerciseId.match(/intro-r-(\d{2})-\d{3}/);
      if (match) {
        const num = parseInt(match[1], 10);
        if (num >= 1 && num <= moduleSlugs.length) {
          return moduleSlugs[num - 1];
        }
      }
      if (exerciseId.includes("-01-") || exerciseId === "primeros-pasos") return "01-empezar-a-pensar-con-r";
      if (exerciseId.includes("-02-")) return "02-trabajar-con-varios-valores";
      if (exerciseId.includes("-03-")) return "03-hacer-preguntas-a-los-datos";
      return "01-empezar-a-pensar-con-r";
    }

    migrateV1toV2(rawV1) {
      console.log("[ProgressStore] Migrating progress from Schema v1 to v2...");
      const v2 = this.getDefaultState();

      if (rawV1.editorState && typeof rawV1.editorState === "object") {
        v2.editorState = { ...rawV1.editorState };
      }

      if (Array.isArray(rawV1.completedExercises)) {
        rawV1.completedExercises.forEach((exId) => {
          const modId = this.inferModuleId(exId);
          if (v2.modules[modId] && !v2.modules[modId].completedExercises.includes(exId)) {
            v2.modules[modId].completedExercises.push(exId);
          }
        });
      }

      if (rawV1.currentExerciseId) {
        v2.currentExerciseId = rawV1.currentExerciseId;
        v2.activeModuleId = this.inferModuleId(rawV1.currentExerciseId);
        if (v2.modules[v2.activeModuleId]) {
          v2.modules[v2.activeModuleId].currentExerciseId = rawV1.currentExerciseId;
        }
      }

      if (rawV1.moduleCompleted && (v2.modules["01-empezar-a-pensar-con-r"] || v2.modules["primeros-pasos"])) {
        const target = v2.modules["01-empezar-a-pensar-con-r"] || v2.modules["primeros-pasos"];
        target.completed = true;
      }

      v2.lastActivity = rawV1.lastActivity || new Date().toISOString();
      return v2;
    }

    load() {
      try {
        let raw = window.localStorage.getItem(this.namespace);

        // Check if data is stored in legacy namespace
        if (!raw) {
          const legacyRaw = window.localStorage.getItem(this.legacyNamespace);
          if (legacyRaw) {
            try {
              const legacyParsed = JSON.parse(legacyRaw);
              const migrated = this.migrateV1toV2(legacyParsed);
              this.state = migrated;
              this.save();
              return migrated;
            } catch (err) {
              console.warn("[ProgressStore] Error migrating legacy state:", err);
            }
          }
          return this.getDefaultState();
        }

        const parsed = JSON.parse(raw);
        if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
          console.warn("[ProgressStore] Invalid format. Resetting to default state.");
          return this.getDefaultState();
        }

        // Schema v1 detected in current namespace
        if (parsed.version === 1 || !parsed.modules) {
          const migrated = this.migrateV1toV2(parsed);
          this.state = migrated;
          this.save();
          return migrated;
        }

        // Ensure all default modules exist in state
        const defaultMods = this.getDefaultModules();
        const mergedModules = {};

        Object.keys(defaultMods).forEach((mId) => {
          if (parsed.modules && parsed.modules[mId]) {
            mergedModules[mId] = {
              id: mId,
              currentExerciseId: parsed.modules[mId].currentExerciseId || defaultMods[mId].currentExerciseId,
              completedExercises: Array.isArray(parsed.modules[mId].completedExercises)
                ? [...new Set(parsed.modules[mId].completedExercises)]
                : [],
              completed: Boolean(parsed.modules[mId].completed),
            };
          } else {
            mergedModules[mId] = defaultMods[mId];
          }
        });

        // Invalidate stale persisted editor code for audited/modified exercises
        const staleExercises = [
          "intro-r-02-006", "intro-r-02-007",
          "intro-r-03-005", "intro-r-03-007",
          "intro-r-04-001", "intro-r-04-002", "intro-r-04-003", "intro-r-04-004", "intro-r-04-005", "intro-r-04-006",
          "intro-r-05-008", "intro-r-09-001", "intro-r-10-005", "intro-r-10-008", "intro-r-11-003", "intro-r-12-003", "intro-r-13-005"
        ];
        if (parsed.contentVersion !== this.contentVersion) {
          parsed.editorState = {};
          parsed.contentVersion = this.contentVersion;
        }

        return {
          version: this.version,
          contentVersion: this.contentVersion,
          courseId: parsed.courseId || this.courseId,
          activeModuleId: (parsed.activeModuleId === "primeros-pasos" ? "01-empezar-a-pensar-con-r" : (parsed.activeModuleId || "01-empezar-a-pensar-con-r")),
          currentExerciseId: parsed.currentExerciseId || "intro-r-01-001",
          modules: mergedModules,
          challenges: (parsed.challenges && typeof parsed.challenges === "object") ? parsed.challenges : {},
          editorState: (parsed.editorState && typeof parsed.editorState === "object") ? parsed.editorState : {},
          lastActivity: parsed.lastActivity || new Date().toISOString(),
        };
      } catch (e) {
        console.warn("[ProgressStore] LocalStorage read/parse error:", e);
        return this.getDefaultState();
      }
    }

    getChallengeStatus(moduleId) {
      if (!moduleId) return "pending";
      if (this.state.challenges && this.state.challenges[moduleId]) {
        return this.state.challenges[moduleId].status || "pending";
      }
      return "pending";
    }

    setChallengeStatus(moduleId, status) {
      if (!moduleId) return;
      if (!this.state.challenges) this.state.challenges = {};
      if (!this.state.challenges[moduleId]) {
        this.state.challenges[moduleId] = { status: "pending", passedAt: null };
      }
      this.state.challenges[moduleId].status = status;
      if (status === "passed" && !this.state.challenges[moduleId].passedAt) {
        this.state.challenges[moduleId].passedAt = new Date().toISOString();
      }
      this.save();
    }

    markChallengePassed(moduleId) {
      this.setChallengeStatus(moduleId, "passed");
      if (this.state.modules && this.state.modules[moduleId]) {
        this.state.modules[moduleId].accredited = true;
      }
      this.save();
    }

    isChallengePassed(moduleId) {
      return this.getChallengeStatus(moduleId) === "passed";
    }

    isModuleAccredited(moduleId) {
      if (!moduleId) return false;
      return this.isChallengePassed(moduleId);
    }

    save(exerciseId, patch) {
      if (typeof exerciseId === "string" && patch && typeof patch === "object") {
        if (patch.status === "completed") {
          this.markCompleted(exerciseId);
        }
        return this.get(exerciseId);
      }

      try {
        this.state.lastActivity = new Date().toISOString();
        window.localStorage.setItem(this.namespace, JSON.stringify(this.state));
      } catch (e) {
        console.warn("[ProgressStore] LocalStorage write error:", e);
      }
      return this.state;
    }

    getModuleState(moduleId) {
      if (!moduleId) moduleId = this.state.activeModuleId;
      if (!this.state.modules[moduleId]) {
        this.state.modules[moduleId] = {
          id: moduleId,
          currentExerciseId: null,
          completedExercises: [],
          completed: false,
        };
      }
      return this.state.modules[moduleId];
    }

    setCurrentExercise(exerciseId, moduleId) {
      if (!exerciseId || typeof exerciseId !== "string") return;
      if (!moduleId) {
        moduleId = this.inferModuleId(exerciseId);
      }

      this.state.currentExerciseId = exerciseId;
      this.state.activeModuleId = moduleId;

      const modState = this.getModuleState(moduleId);
      modState.currentExerciseId = exerciseId;

      this.save();
    }

    getModuleCurrentExercise(moduleId) {
      if (!moduleId) return null;
      const modState = this.state.modules[moduleId];
      return modState ? modState.currentExerciseId : null;
    }

    markCompleted(exerciseId, moduleId) {
      if (!exerciseId || typeof exerciseId !== "string") return;
      if (!moduleId) {
        moduleId = this.inferModuleId(exerciseId);
      }

      const modState = this.getModuleState(moduleId);
      if (!modState.completedExercises.includes(exerciseId)) {
        modState.completedExercises.push(exerciseId);
      }

      this.save();
    }

    setModuleCompleted(moduleId, isCompleted = true) {
      if (!moduleId) moduleId = this.state.activeModuleId;
      const modState = this.getModuleState(moduleId);
      modState.completed = Boolean(isCompleted);
      this.save();
    }

    isModuleCompleted(moduleId) {
      if (!moduleId) return false;
      const modState = this.state.modules[moduleId];
      return Boolean(modState && modState.completed);
    }

    isCompleted(exerciseId) {
      if (!exerciseId) return false;
      const modId = this.inferModuleId(exerciseId);
      const modState = this.state.modules[modId];
      if (modState && modState.completedExercises.includes(exerciseId)) {
        return true;
      }
      // Check across all modules in case of unknown ID mapping
      for (const m of Object.values(this.state.modules)) {
        if (m.completedExercises && m.completedExercises.includes(exerciseId)) {
          return true;
        }
      }
      return false;
    }

    get(exerciseId) {
      const completed = this.isCompleted(exerciseId);
      return {
        exerciseId,
        status: completed ? "completed" : "not_started",
        completedAt: completed ? this.state.lastActivity : null,
      };
    }

    saveEditorCode(exerciseId, code) {
      if (!exerciseId || typeof code !== "string") return;

      this.state.editorState[exerciseId] = code;
      this._pendingEditorState[exerciseId] = code;

      if (this._debounceTimer) {
        clearTimeout(this._debounceTimer);
      }

      this._debounceTimer = setTimeout(() => {
        this.save();
        this._pendingEditorState = {};
      }, 500);
    }

    getEditorCode(exerciseId) {
      if (!exerciseId) return null;
      return this.state.editorState[exerciseId] || null;
    }

    getModuleProgress(moduleId, totalModuleCount) {
      const modState = this.getModuleState(moduleId);
      const completedCount = modState.completedExercises.length;
      const total = totalModuleCount || completedCount || 1;
      const percentage = Math.round((completedCount / total) * 100);
      return {
        completedCount,
        totalCount: total,
        percentage,
        isCompleted: modState.completed || completedCount >= total,
      };
    }

    getCourseProgress(totalCourseCount) {
      const config = (window.SocialR && window.SocialR.courseConfig) || null;
      const defaultTotal = (config && typeof config.getAvailableExerciseCount === "function")
        ? config.getAvailableExerciseCount()
        : (config ? config.publishedExerciseCount : 36);
      const effectiveTotal = (typeof totalCourseCount === "number" && totalCourseCount > 0)
        ? totalCourseCount
        : defaultTotal;

      let totalCompleted = 0;
      Object.entries(this.state.modules).forEach(([modSlug, mod]) => {
        // If config exists, only count completed exercises in currently available modules
        if (config && typeof config.isModuleAvailable === "function") {
          if (!config.isModuleAvailable(modSlug)) {
            return; // Preserved in localStorage, but not counted when module is unavailable
          }
        } else if (config && typeof config.isModulePublished === "function") {
          if (!config.isModulePublished(modSlug)) {
            return; // Preserved in localStorage, but not counted in current public progress
          }
        }
        totalCompleted += (mod.completedExercises || []).length;
      });
      const percentage = Math.round((totalCompleted / effectiveTotal) * 100);
      return {
        completedCount: totalCompleted,
        totalCount: effectiveTotal,
        percentage: Math.min(100, percentage),
      };
    }

    resetProgress() {
      try {
        if (this._debounceTimer) clearTimeout(this._debounceTimer);
        window.localStorage.removeItem(this.namespace);
        window.localStorage.removeItem(this.legacyNamespace);
        this.state = this.getDefaultState();
        this.save();
      } catch (e) {
        console.warn("[ProgressStore] Error resetting progress:", e);
      }
      return this.state;
    }

    clearAll() {
      return this.resetProgress();
    }
  }

  window.ProgressStore = ProgressStore;
  window.LocalProgressStore = LocalProgressStore;
  window.SocialR = window.SocialR || {};
  window.SocialR.progress = new LocalProgressStore();
})();
