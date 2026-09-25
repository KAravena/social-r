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
    }
  };

  window.SocialR = window.SocialR || {};
  window.SocialR.courseConfig = courseConfig;
})();
