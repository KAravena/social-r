/**
 * Social R - Central Course Publication Configuration
 * Defines publication state, published exercise boundaries, and module access control.
 * M06–M13 están temporalmente en revisión pedagógica / standby. No eliminar.
 * Generated automatically from content/courses/intro-r/course.yml
 */
(function () {
  "use strict";

  const courseConfig = {
    courseId: "intro-r",
    totalModules: 13,
    totalExercises: 88,
    publishedThrough: 5,
    publishedModuleCount: 5,
    publishedExerciseCount: 36,
    lastPublishedExerciseId: "intro-r-05-008",
    publishedModuleSlugs: [
      "01-empezar-a-pensar-con-r",
      "02-trabajar-con-varios-valores",
      "03-hacer-preguntas-a-los-datos",
      "04-entender-una-base-de-datos",
      "05-seleccionar-y-filtrar-datos"
],
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
