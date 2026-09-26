/**
 * Social R Platform - Core Engine Orchestrator v0.4.0
 * Manages exercises, view routing, progress state, keyboard shortcuts, and native run delegation.
 */
(function () {
  "use strict";

  class SocialREngine {
    constructor() {
      this.buildId = "v0.4.0-20260819-modular";
      this.events = (window.SocialR && window.SocialR.events) ? window.SocialR.events : (window.EventBus ? new window.EventBus() : null);
      this.progress = (window.SocialR && window.SocialR.progress) ? window.SocialR.progress : (window.LocalProgressStore ? new window.LocalProgressStore() : null);
      this.navigation = (window.SocialR && window.SocialR.navigation) ? window.SocialR.navigation : null;
      this.adapter = (window.SocialR && window.SocialR.adapter) ? window.SocialR.adapter : (window.QuartoLiveAdapter ? new window.QuartoLiveAdapter() : null);
      this.graphics = (window.SocialR && window.SocialR.graphics) ? window.SocialR.graphics : (window.GraphicsManager ? new window.GraphicsManager() : null);
      this.devMode = false;
    }

    init() {
      console.log(`[Social R] Engine Initialized (${this.buildId})`);

      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.has("qa-clean")) {
        console.log("[Social R] QA Clean requested: clearing progress store.");
        this.resetProgress();
      }

      if (urlParams.has("dev") || urlParams.get("debug") === "1" || urlParams.get("debug") === "quarto-live") {
        this.devMode = true;
        document.body.classList.add("is-debug");
      }

      if (this.navigation && typeof this.navigation.init === "function") {
        this.navigation.init();
      }

      this.bindGlobalHandlers();
    }

    resetProgress() {
      if (this.progress && typeof this.progress.reset === "function") {
        this.progress.reset();
      } else if (this.progress && typeof this.progress.resetProgress === "function") {
        this.progress.resetProgress();
      }
      if (this.navigation && typeof this.navigation.setActiveIndex === "function") {
        this.navigation.setActiveIndex(0);
      }
    }

    getActiveExerciseElement() {
      return document.querySelector(".social-r-exercise.is-active-exercise") ||
             (this.navigation && typeof this.navigation.getCurrentExercise === "function" && this.navigation.getCurrentExercise() ? this.navigation.getCurrentExercise().node : null) ||
             null;
    }

    getActiveExerciseId() {
      const el = this.getActiveExerciseElement();
      return el ? el.getAttribute("data-exercise-id") : null;
    }

    runActiveExercise() {
      const activeEx = this.getActiveExerciseElement();
      if (!activeEx) return;

      const activeId = activeEx.getAttribute("data-exercise-id");

      // Visual button indicator
      const btn = activeEx.querySelector(".sr-btn-run");
      if (btn) {
        btn.classList.add("is-running");
        setTimeout(() => btn.classList.remove("is-running"), 400);
      }

      if (this.adapter && activeId) {
        this.adapter.runCode(activeId);
      }
    }

    async executeActiveExercise() {
      return this.runActiveExercise();
    }

    async submitActiveExercise() {
      const activeEx = this.getActiveExerciseElement();
      if (!activeEx) return;

      const activeId = activeEx.getAttribute("data-exercise-id");
      const btn = activeEx.querySelector(".sr-btn-submit");
      if (btn) {
        btn.classList.add("is-submitting");
        setTimeout(() => btn.classList.remove("is-submitting"), 400);
      }

      if (this.adapter && activeId) {
        await this.adapter.submitCode(activeId);
      }
    }

    bindGlobalHandlers() {
      // 1. Single Global Keyboard Shortcuts (Capture Phase)
      window.addEventListener(
        "keydown",
        (e) => {
          // Ctrl + Shift + Enter -> Submit
          if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "Enter") {
            e.preventDefault();
            e.stopPropagation();
            this.submitActiveExercise();
            return;
          }

          // Ctrl + Enter -> Run
          if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key === "Enter") {
            e.preventDefault();
            e.stopPropagation();
            this.runActiveExercise();
            return;
          }
        },
        true
      );

      // 2. Editor Input / Keyup listener for stale feedback invalidation & debounced code persistence
      const handleEditing = (e) => {
        const exContainer = (e.target && e.target.closest) ? e.target.closest(".social-r-exercise") : null;
        const targetEx = exContainer || this.getActiveExerciseElement();
        if (targetEx && this.adapter) {
          const exId = targetEx.getAttribute("data-exercise-id");
          if (exId) {
            this.adapter.invalidateFeedbackIfStale(exId);
            const currentCode = this.adapter.getCode(exId);
            if (currentCode && this.progress && this.progress.saveEditorCode) {
              this.progress.saveEditorCode(exId, currentCode);
            }
          }
        }
      };

      document.addEventListener("input", handleEditing, true);
      document.addEventListener(
        "keyup",
        (e) => {
          if (!e.ctrlKey && !e.metaKey && e.key !== "Shift" && e.key !== "Alt") {
            handleEditing(e);
          }
        },
        true
      );

      // 3. Button Click Delegations
      document.addEventListener("click", (e) => {
        // Run Button
        const runBtn = e.target.closest(".sr-btn-run");
        if (runBtn) {
          this.runActiveExercise();
          return;
        }

        // Submit Button
        const submitBtn = e.target.closest(".sr-btn-submit");
        if (submitBtn) {
          this.submitActiveExercise();
          return;
        }

        // Reset Button
        const resetBtn = e.target.closest(".sr-btn-reset");
        if (resetBtn && this.adapter) {
          const exId = resetBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.adapter.reset(exId);
          return;
        }

        // Hint Toggle Button
        const hintBtn = e.target.closest(".sr-hint-toggle-btn");
        if (hintBtn && this.adapter) {
          const exId = hintBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.adapter.toggleHint(exId);
          return;
        }

        // Challenge Retry Button
        const retryBtn = e.target.closest(".sr-btn-challenge-retry");
        if (retryBtn && this.adapter) {
          const exId = retryBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          const view = this.adapter.getCMView(exId);
          if (view) view.focus();
          return;
        }

        // Challenge Practice Button
        const practiceBtn = e.target.closest(".sr-btn-challenge-practice");
        if (practiceBtn && this.navigation) {
          const modId = practiceBtn.getAttribute("data-module-id");
          const modExs = this.navigation.exercises.filter((ex) => ex.moduleId === modId);
          const store = this.progress;
          const firstIncomplete = modExs.find((ex) => !store || !store.isCompleted(ex.id));
          const targetIdx = firstIncomplete ? firstIncomplete.globalIndex : (modExs[0] ? modExs[0].globalIndex : 0);
          this.navigation.setActiveIndex(targetIdx);
          return;
        }

        // Start Challenge from last exercise Button
        const startChBtn = e.target.closest(".sr-btn-start-challenge");
        if (startChBtn && this.navigation) {
          const modId = startChBtn.getAttribute("data-module-id");
          this.navigation.setActiveChallenge(modId);
          return;
        }

        // Continue to Next Module Button
        const nextModBtn = e.target.closest(".sr-btn-continue-next-module");
        if (nextModBtn && this.navigation) {
          const nextIdx = parseInt(nextModBtn.getAttribute("data-next-index"), 10);
          if (!isNaN(nextIdx)) {
            this.navigation.setActiveIndex(nextIdx);
          }
          return;
        }

        // Feedback Continue Button
        const feedbackContBtn = e.target.closest(".sr-btn-feedback-continue");
        if (feedbackContBtn && this.navigation) {
          if (feedbackContBtn.classList.contains("sr-btn-celebrate-module")) {
            const modId = feedbackContBtn.getAttribute("data-module-id") || (this.navigation.getCurrentExercise() ? this.navigation.getCurrentExercise().moduleId : null);
            this.navigation.showCelebration(modId);
          } else {
            this.navigation.next();
          }
          return;
        }

        // Clear Console Button
        const clearBtn = e.target.closest(".sr-btn-clear-console");
        if (clearBtn && this.adapter) {
          const exId = clearBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.adapter.clearConsole(exId);
          return;
        }
      });
    }
  }

  // Global Engine Instance Initialization
  window.SocialR = window.SocialR || {};
  const engine = new SocialREngine();
  window.SocialR.engine = engine;
  window.SocialR.adapter = engine.adapter;
  window.SocialR.events = engine.events;
  window.SocialR.progress = engine.progress;
  window.SocialR.graphics = engine.graphics;
  window.SocialR.resetProgress = () => engine.resetProgress();
  if (!window.SocialR.devMode) window.SocialR.devMode = false;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      engine.init();
    });
  } else {
    engine.init();
  }
})();
