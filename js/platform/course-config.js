/**
 * Social R - Central Course Publication Configuration
 * Defines publication state, published exercise boundaries, and module access control.
 * M01–M05: published (production baseline).
 * M06–M13: standby (editorial state kept intact, enabled exclusively in local preview mode).
 * Generated automatically from content/courses/intro-r/course.yml
 */
(function () {
  "use strict";

  const courseConfig = {
    courseId: "intro-r",
    totalModules: 13,
    totalExercises: 89,
    publishedThrough: 5,
    publishedModuleCount: 5,
    publishedExerciseCount: 36,
    lastPublishedExerciseId: "intro-r-05-008",
    lastCourseExerciseId: "intro-r-13-005",
    publishedModuleSlugs: [
      "01-empezar-a-pensar-con-r",
      "02-trabajar-con-varios-valores",
      "03-hacer-preguntas-a-los-datos",
      "04-entender-una-base-de-datos",
      "05-seleccionar-y-filtrar-datos"
],
    allModuleSlugs: [
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
],

    // Editorial status checks (Strictly reflect course.yml metadata)
    isModulePublished(moduleIdOrOrder) {
      if (typeof moduleIdOrOrder === "number") {
        return moduleIdOrOrder >= 1 && moduleIdOrOrder <= this.publishedThrough;
      }
      if (typeof moduleIdOrOrder === "string") {
        const m = moduleIdOrOrder.match(/^intro-r-(\d+)-/);
        if (m) {
          const modNum = parseInt(m[1], 10);
          return modNum >= 1 && modNum <= this.publishedThrough;
        }
        return this.publishedModuleSlugs.includes(moduleIdOrOrder);
      }
      return false;
    },

    isExercisePublished(exerciseId) {
      if (!exerciseId || typeof exerciseId !== "string") return false;
      const m = exerciseId.match(/^intro-r-(\d+)-/);
      if (!m) return false;
      const modNum = parseInt(m[1], 10);
      return modNum >= 1 && modNum <= this.publishedThrough;
    },

    isStandbyExercise(exerciseId) {
      if (!exerciseId || typeof exerciseId !== "string") return false;
      const m = exerciseId.match(/^intro-r-(\d+)-/);
      if (!m) return false;
      const modNum = parseInt(m[1], 10);
      return modNum > this.publishedThrough && modNum <= this.totalModules;
    },

    isStandbyModule(moduleIdOrOrder) {
      if (typeof moduleIdOrOrder === "number") {
        return moduleIdOrOrder > this.publishedThrough && moduleIdOrOrder <= this.totalModules;
      }
      if (typeof moduleIdOrOrder === "string") {
        const m = moduleIdOrOrder.match(/^intro-r-(\d+)-/);
        if (m) {
          const modNum = parseInt(m[1], 10);
          return modNum > this.publishedThrough && modNum <= this.totalModules;
        }
        const idx = this.allModuleSlugs.indexOf(moduleIdOrOrder);
        return idx >= this.publishedThrough && idx < this.totalModules;
      }
      return false;
    },

    // Central local preview detection (localhost / 127.0.0.1)
    isLocalPreview() {
      if (typeof window !== "undefined" && window.__FORCE_PRODUCTION_MODE__) {
        return false;
      }
      if (typeof window === "undefined" || !window.location) return false;
      const hostname = window.location.hostname;
      return hostname === "localhost" || hostname === "127.0.0.1";
    },

    // Availability layer for QA / local preview overrides
    // In production: availability == publication (M01-M05, 36 exercises)
    // In local preview: availability == published + standby (M01-M13, 88 exercises)
    isModuleAvailable(moduleIdOrOrder) {
      if (this.isModulePublished(moduleIdOrOrder)) return true;
      if (this.isLocalPreview()) {
        return this.isStandbyModule(moduleIdOrOrder);
      }
      return false;
    },

    isExerciseAvailable(exerciseId) {
      if (this.isExercisePublished(exerciseId)) return true;
      if (this.isLocalPreview()) {
        return this.isStandbyExercise(exerciseId);
      }
      return false;
    },

    getAvailableModuleIds() {
      return this.isLocalPreview() ? [...this.allModuleSlugs] : [...this.publishedModuleSlugs];
    },

    getAvailableExerciseCount() {
      return this.isLocalPreview() ? this.totalExercises : this.publishedExerciseCount;
    },

    getAvailableModuleCount() {
      return this.isLocalPreview() ? this.totalModules : this.publishedModuleCount;
    },

    getLastAvailableExerciseId() {
      return this.isLocalPreview() ? this.lastCourseExerciseId : this.lastPublishedExerciseId;
    },

    getPublishedModuleIds() {
      return [...this.publishedModuleSlugs];
    },

    getLastPublishedExerciseId() {
      return this.lastPublishedExerciseId;
    },

    // =========================================================================
    // Centralized Progression & Mastery Gating Architecture
    // =========================================================================

    _resolveStoreState(storeOrState) {
      if (!storeOrState) {
        if (typeof window !== "undefined" && window.SocialR) {
          if (window.SocialR.progress && window.SocialR.progress.state) return window.SocialR.progress.state;
          if (window.SocialR.progressStore && window.SocialR.progressStore.state) return window.SocialR.progressStore.state;
        }
        if (typeof localStorage !== "undefined") {
          try {
            const raw = localStorage.getItem("social-r:progress:intro-r") || localStorage.getItem("social-r:progress:v2");
            if (raw) return JSON.parse(raw);
          } catch (_) {}
        }
        return null;
      }
      return storeOrState.state ? storeOrState.state : storeOrState;
    },

    isModuleSatisfied(moduleId, storeOrState) {
      if (!moduleId) return false;
      const state = this._resolveStoreState(storeOrState);
      if (!state) return false;

      if (state.challenges && state.challenges[moduleId]) {
        const ch = state.challenges[moduleId];
        if (ch.status === "passed" || Boolean(ch.passed)) return true;
      }

      if (state.modules && state.modules[moduleId] && state.modules[moduleId].accredited) {
        return true;
      }

      return false;
    },

    isModuleUnlocked(moduleIdOrOrder, storeOrState) {
      if (typeof window !== "undefined" && window.SocialR && window.SocialR.devMode) return true;

      let modSlug = "";
      let modOrder = 1;

      if (typeof moduleIdOrOrder === "number") {
        modOrder = moduleIdOrOrder;
        modSlug = this.allModuleSlugs[modOrder - 1] || "";
      } else if (typeof moduleIdOrOrder === "string") {
        modSlug = moduleIdOrOrder;
        const idx = this.allModuleSlugs.indexOf(modSlug);
        if (idx !== -1) {
          modOrder = idx + 1;
        } else {
          const m = modSlug.match(/^intro-r-(\d+)-/);
          if (m) {
            modOrder = parseInt(m[1], 10);
            modSlug = this.allModuleSlugs[modOrder - 1] || modSlug;
          }
        }
      }

      if (!modSlug) return false;

      if (!this.isModuleAvailable(modSlug)) {
        return false;
      }

      if (modOrder <= 1) return true;

      const prevModSlug = this.allModuleSlugs[modOrder - 2];
      if (this.isModuleSatisfied(prevModSlug, storeOrState)) {
        return true;
      }

      const state = this._resolveStoreState(storeOrState);
      if (state && state.modules && state.modules[modSlug]) {
        const m = state.modules[modSlug];
        if (Array.isArray(m.completedExercises) && m.completedExercises.length > 0) {
          return true;
        }
      }

      return false;
    },

    isChallengeUnlocked(moduleId, storeOrState) {
      return this.isModuleUnlocked(moduleId, storeOrState);
    },

    canNavigateToModule(moduleId, storeOrState) {
      return this.isModuleAvailable(moduleId) && this.isModuleUnlocked(moduleId, storeOrState);
    },

    isExerciseUnlocked(exercise, storeOrState, exercisesList) {
      if (typeof window !== "undefined" && window.SocialR && window.SocialR.devMode) return true;
      if (!exercise) return false;

      const modId = exercise.moduleId || exercise.module;
      if (!this.isModuleUnlocked(modId, storeOrState)) {
        return false;
      }

      if (this.isModuleSatisfied(modId, storeOrState)) {
        return true;
      }

      if (exercise.order === 0) {
        return true;
      }

      const state = this._resolveStoreState(storeOrState);
      if (!state) return false;

      const completedSet = new Set();
      if (state.modules) {
        for (const m of Object.values(state.modules)) {
          if (Array.isArray(m.completedExercises)) {
            m.completedExercises.forEach((id) => completedSet.add(id));
          }
        }
      }
      if (Array.isArray(state.completed)) {
        state.completed.forEach((id) => completedSet.add(id));
      }

      if (exercise.prevExId) {
        return completedSet.has(exercise.prevExId);
      }

      if (Array.isArray(exercisesList)) {
        const curIdx = exercisesList.findIndex((e) => e.id === exercise.id);
        if (curIdx > 0) {
          const prev = exercisesList[curIdx - 1];
          if (prev && (prev.moduleId === modId || prev.module === modId)) {
            return completedSet.has(prev.id);
          }
        }
      }

      return false;
    }
  };

  window.SocialR = window.SocialR || {};
  window.SocialR.courseConfig = courseConfig;
})();
