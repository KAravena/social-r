/**
 * Social R Platform - Native WebR Graphics Manager v1.0
 * Handles capture, display, pagination, responsive scaling, and modal expansion
 * for graphics produced by WebR (hist, plot, barplot, boxplot, etc.).
 */
(function () {
  "use strict";

  class GraphicsManager {
    constructor() {
      this.plotsByExercise = new Map(); // exerciseId -> { plots: [{ dataUrl, width, height, title }], activeIndex: number }
      this.activeExerciseId = null;
      this._boundKeyDown = this.handleKeyDown.bind(this);
    }

    init() {
      console.log("[Social R Graphics] Initializing Native WebR Graphics Manager...");
      this.bindDOMEvents();
      this.bindSystemEvents();
    }

    getExerciseContainer(exerciseId) {
      if (!exerciseId) {
        return document.querySelector(".social-r-exercise.is-active-exercise");
      }
      return document.querySelector(`.social-r-exercise[data-exercise-id="${exerciseId}"]`);
    }

    getActiveExerciseId() {
      const activeEl = document.querySelector(".social-r-exercise.is-active-exercise");
      return activeEl ? activeEl.getAttribute("data-exercise-id") : this.activeExerciseId;
    }

    bindDOMEvents() {
      // 1. Delegated click handler for output tabs, pagers, expand, and modal
      document.addEventListener("click", (e) => {
        // Output Tab Click
        const tabBtn = e.target.closest(".sr-output-tab");
        if (tabBtn) {
          const exContainer = tabBtn.closest(".social-r-exercise");
          const exId = exContainer ? exContainer.getAttribute("data-exercise-id") : this.getActiveExerciseId();
          const targetTab = tabBtn.getAttribute("data-tab");
          if (targetTab === "plot") {
            this.switchToPlotTab(exId);
          } else {
            this.switchToConsoleTab(exId);
          }
          return;
        }

        // Plot Pager: Previous
        const prevBtn = e.target.closest(".sr-plot-prev");
        if (prevBtn) {
          const exId = prevBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.prevPlot(exId);
          return;
        }

        // Plot Pager: Next
        const nextBtn = e.target.closest(".sr-plot-next");
        if (nextBtn) {
          const exId = nextBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.nextPlot(exId);
          return;
        }

        // Expand Plot Modal Button
        const expandBtn = e.target.closest(".sr-btn-expand-plot");
        if (expandBtn) {
          const exId = expandBtn.getAttribute("data-exercise-id") || this.getActiveExerciseId();
          this.expandPlot(exId);
          return;
        }

        // Close Modal Button
        const closeBtn = e.target.closest(".sr-plot-modal-close");
        if (closeBtn) {
          this.closeModal();
          return;
        }

        // Backdrop Click
        const backdrop = e.target.closest(".sr-plot-modal-backdrop");
        if (backdrop) {
          this.closeModal();
          return;
        }
      });

      // 2. Keyboard Navigation: Escape for Modal, Left/Right for Tabs
      window.addEventListener("keydown", this._boundKeyDown);
    }

    handleKeyDown(e) {
      // Escape closes expand modal
      if (e.key === "Escape") {
        const modal = document.getElementById("sr-plot-modal");
        if (modal && !modal.classList.contains("d-none")) {
          e.preventDefault();
          this.closeModal();
          return;
        }
      }

      // Arrow navigation between output tabs when focused on tablist
      const activeTab = document.activeElement ? document.activeElement.closest(".sr-output-tab") : null;
      if (activeTab && (e.key === "ArrowLeft" || e.key === "ArrowRight")) {
        e.preventDefault();
        const tablist = activeTab.closest(".sr-output-tabs");
        if (!tablist) return;
        const tabs = Array.from(tablist.querySelectorAll(".sr-output-tab:not(.d-none)"));
        const currentIndex = tabs.indexOf(activeTab);
        if (currentIndex === -1) return;

        let nextIndex = currentIndex;
        if (e.key === "ArrowRight") {
          nextIndex = (currentIndex + 1) % tabs.length;
        } else if (e.key === "ArrowLeft") {
          nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
        }

        const nextTab = tabs[nextIndex];
        if (nextTab) {
          nextTab.focus();
          nextTab.click();
        }
      }
    }

    bindSystemEvents() {
      if (!window.SocialR || !window.SocialR.events) return;

      // Exercise opened: update state for newly displayed exercise
      window.SocialR.events.on("exercise_opened", (detail) => {
        const exId = detail ? detail.exerciseId : null;
        this.activeExerciseId = exId;
        this.onExerciseOpened(exId);
      });

      // Exercise reset: clear graphics and return to console
      window.SocialR.events.on("exercise_reset", (detail) => {
        const exId = detail ? detail.exerciseId : null;
        if (exId) {
          this.clearExercise(exId);
        }
      });
    }

    onExerciseOpened(exerciseId) {
      if (!exerciseId) return;
      const container = this.getExerciseContainer(exerciseId);
      if (!container) return;

      const state = this.plotsByExercise.get(exerciseId);
      const tabPlot = container.querySelector(".sr-output-tab-plot");

      if (state && state.plots && state.plots.length > 0) {
        if (tabPlot) tabPlot.classList.remove("d-none");
        this.renderPlot(exerciseId);
      } else {
        if (tabPlot) tabPlot.classList.add("d-none");
        this.switchToConsoleTab(exerciseId);
      }
    }

    /**
     * Inspects HTML output node from WebR evaluator.asHtml(evalResult)
     * Extracts all rendered canvas/img graphics, stores them, and renders them.
     */
    captureFromHtmlNode(exerciseId, htmlNode) {
      if (!exerciseId || !htmlNode) return false;

      // Look for WebR rendered figure canvases or images
      const rawCanvases = Array.from(htmlNode.querySelectorAll("canvas"));
      const rawImages = Array.from(htmlNode.querySelectorAll(".cell-output-display img, img.figure-img"));

      const capturedPlots = [];

      // Process canvases
      rawCanvases.forEach((canvas, idx) => {
        if (canvas.width > 0 && canvas.height > 0) {
          try {
            const dataUrl = canvas.toDataURL("image/png");
            if (dataUrl && dataUrl.length > 100) {
              capturedPlots.push({
                dataUrl: dataUrl,
                width: canvas.width,
                height: canvas.height,
                title: `Gráfico ${idx + 1}`
              });
            }
          } catch (err) {
            console.warn("[Social R Graphics] Failed to extract dataUrl from canvas:", err);
          }
        }
      });

      // Process images (fallback if WebR used PNG output)
      rawImages.forEach((img, idx) => {
        const src = img.src || img.getAttribute("src");
        if (src && src.length > 100) {
          capturedPlots.push({
            dataUrl: src,
            width: img.naturalWidth || 600,
            height: img.naturalHeight || 400,
            title: `Gráfico ${capturedPlots.length + 1}`
          });
        }
      });

      if (capturedPlots.length === 0) {
        return false;
      }

      // Store in state
      this.plotsByExercise.set(exerciseId, {
        plots: capturedPlots,
        activeIndex: capturedPlots.length - 1 // Default to latest plot
      });

      // Reveal Gráfico Tab in UI
      const container = this.getExerciseContainer(exerciseId);
      if (container) {
        const tabPlot = container.querySelector(".sr-output-tab-plot");
        if (tabPlot) {
          tabPlot.classList.remove("d-none");
        }
      }

      // Render the active plot
      this.renderPlot(exerciseId);
      return true;
    }

    renderPlot(exerciseId) {
      const container = this.getExerciseContainer(exerciseId);
      if (!container) return;

      const stage = container.querySelector(`#sr-plot-stage-${exerciseId}`) || container.querySelector(".sr-plot-stage");
      if (!stage) return;

      const state = this.plotsByExercise.get(exerciseId);
      if (!state || !state.plots || state.plots.length === 0) {
        stage.innerHTML = '<div class="sr-plot-empty">Los gráficos que generes en R aparecerán aquí.</div>';
        return;
      }

      const activeIdx = Math.max(0, Math.min(state.activeIndex, state.plots.length - 1));
      const plot = state.plots[activeIdx];

      // Clean existing stage
      stage.innerHTML = "";

      // Create responsive crisp image element
      const img = document.createElement("img");
      img.className = "sr-plot-img";
      img.src = plot.dataUrl;
      img.alt = "Gráfico generado por R";
      img.setAttribute("role", "img");
      img.setAttribute("aria-label", "Gráfico generado por R");
      stage.appendChild(img);

      // Update Pager
      const pager = container.querySelector(`#sr-plot-pager-${exerciseId}`) || container.querySelector(".sr-plot-pager");
      const counter = container.querySelector(`#sr-plot-counter-${exerciseId}`) || container.querySelector(".sr-plot-counter");
      const prevBtn = container.querySelector(".sr-plot-prev");
      const nextBtn = container.querySelector(".sr-plot-next");

      if (pager) {
        if (state.plots.length > 1) {
          pager.classList.remove("d-none");
          if (counter) counter.textContent = `${activeIdx + 1} / ${state.plots.length}`;
          if (prevBtn) prevBtn.disabled = (activeIdx === 0);
          if (nextBtn) nextBtn.disabled = (activeIdx === state.plots.length - 1);
        } else {
          pager.classList.add("d-none");
        }
      }
    }

    switchToPlotTab(exerciseId) {
      const container = this.getExerciseContainer(exerciseId);
      if (!container) return;

      const tabConsole = container.querySelector(`#sr-tab-console-${exerciseId}`) || container.querySelector('[data-tab="console"]');
      const tabPlot = container.querySelector(`#sr-tab-plot-${exerciseId}`) || container.querySelector('[data-tab="plot"]');
      const paneConsole = container.querySelector(`#sr-pane-console-${exerciseId}`) || container.querySelector(".sr-console-transcript");
      const panePlot = container.querySelector(`#sr-pane-plot-${exerciseId}`) || container.querySelector(".sr-plot-pane");
      const actionsConsole = container.querySelector(`#sr-console-actions-${exerciseId}`) || container.querySelector(".sr-console-actions");
      const actionsPlot = container.querySelector(`#sr-plot-actions-${exerciseId}`) || container.querySelector(".sr-plot-actions");

      if (tabConsole) {
        tabConsole.classList.remove("is-active");
        tabConsole.setAttribute("aria-selected", "false");
        tabConsole.setAttribute("tabindex", "-1");
      }
      if (tabPlot) {
        tabPlot.classList.remove("d-none");
        tabPlot.classList.add("is-active");
        tabPlot.setAttribute("aria-selected", "true");
        tabPlot.setAttribute("tabindex", "0");
      }

      if (paneConsole) {
        paneConsole.classList.add("d-none");
        paneConsole.setAttribute("hidden", "true");
      }
      if (panePlot) {
        panePlot.classList.remove("d-none");
        panePlot.removeAttribute("hidden");
      }

      if (actionsConsole) {
        actionsConsole.classList.add("d-none");
      }
      if (actionsPlot) {
        actionsPlot.classList.remove("d-none");
      }

      // Ensure active plot is rendered in view
      this.renderPlot(exerciseId);
    }

    switchToConsoleTab(exerciseId) {
      const container = this.getExerciseContainer(exerciseId);
      if (!container) return;

      const tabConsole = container.querySelector(`#sr-tab-console-${exerciseId}`) || container.querySelector('[data-tab="console"]');
      const tabPlot = container.querySelector(`#sr-tab-plot-${exerciseId}`) || container.querySelector('[data-tab="plot"]');
      const paneConsole = container.querySelector(`#sr-pane-console-${exerciseId}`) || container.querySelector(".sr-console-transcript");
      const panePlot = container.querySelector(`#sr-pane-plot-${exerciseId}`) || container.querySelector(".sr-plot-pane");
      const actionsConsole = container.querySelector(`#sr-console-actions-${exerciseId}`) || container.querySelector(".sr-console-actions");
      const actionsPlot = container.querySelector(`#sr-plot-actions-${exerciseId}`) || container.querySelector(".sr-plot-actions");

      if (tabConsole) {
        tabConsole.classList.add("is-active");
        tabConsole.setAttribute("aria-selected", "true");
        tabConsole.setAttribute("tabindex", "0");
      }
      if (tabPlot) {
        tabPlot.classList.remove("is-active");
        tabPlot.setAttribute("aria-selected", "false");
        tabPlot.setAttribute("tabindex", "-1");
      }

      if (paneConsole) {
        paneConsole.classList.remove("d-none");
        paneConsole.removeAttribute("hidden");
      }
      if (panePlot) {
        panePlot.classList.add("d-none");
        panePlot.setAttribute("hidden", "true");
      }

      if (actionsConsole) {
        actionsConsole.classList.remove("d-none");
      }
      if (actionsPlot) {
        actionsPlot.classList.add("d-none");
      }
    }

    prevPlot(exerciseId) {
      const state = this.plotsByExercise.get(exerciseId);
      if (state && state.activeIndex > 0) {
        state.activeIndex--;
        this.renderPlot(exerciseId);
      }
    }

    nextPlot(exerciseId) {
      const state = this.plotsByExercise.get(exerciseId);
      if (state && state.activeIndex < state.plots.length - 1) {
        state.activeIndex++;
        this.renderPlot(exerciseId);
      }
    }

    /**
     * Clears graphics state prior to a new execution.
     * Prevents outdated plots from being mistaken for the result of a failed new run.
     */
    clearForExecution(exerciseId) {
      this.plotsByExercise.delete(exerciseId);
      const container = this.getExerciseContainer(exerciseId);
      if (container) {
        const stage = container.querySelector(`#sr-plot-stage-${exerciseId}`) || container.querySelector(".sr-plot-stage");
        if (stage) stage.innerHTML = "";

        const tabPlot = container.querySelector(`#sr-tab-plot-${exerciseId}`) || container.querySelector(".sr-output-tab-plot");
        if (tabPlot) tabPlot.classList.add("d-none");

        this.switchToConsoleTab(exerciseId);
      }
    }

    clearExercise(exerciseId) {
      this.clearForExecution(exerciseId);
    }

    expandPlot(exerciseId) {
      const state = this.plotsByExercise.get(exerciseId);
      if (!state || !state.plots || state.plots.length === 0) return;

      const activeIdx = Math.max(0, Math.min(state.activeIndex, state.plots.length - 1));
      const plot = state.plots[activeIdx];

      const modal = document.getElementById("sr-plot-modal");
      if (!modal) return;

      const modalStage = modal.querySelector(".sr-plot-modal-stage");
      if (modalStage) {
        modalStage.innerHTML = "";
        const img = document.createElement("img");
        img.src = plot.dataUrl;
        img.alt = "Gráfico generado por R (Vista ampliada)";
        img.setAttribute("role", "img");
        modalStage.appendChild(img);
      }

      modal.classList.remove("d-none");
      const closeBtn = modal.querySelector(".sr-plot-modal-close");
      if (closeBtn) closeBtn.focus();
    }

    closeModal() {
      const modal = document.getElementById("sr-plot-modal");
      if (modal) {
        modal.classList.add("d-none");
        const modalStage = modal.querySelector(".sr-plot-modal-stage");
        if (modalStage) modalStage.innerHTML = "";
      }
    }
  }

  // Register on window
  window.SocialR = window.SocialR || {};
  const graphicsManager = new GraphicsManager();
  window.SocialR.graphics = graphicsManager;
  window.GraphicsManager = GraphicsManager;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => graphicsManager.init());
  } else {
    graphicsManager.init();
  }
})();
