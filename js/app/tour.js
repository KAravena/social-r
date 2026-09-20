/**
 * Social R - Interactive Onboarding Tour Controller v1.0
 * Native, lightweight guided product tour over the real interface.
 * Auto-launches on first visit to M1E1 with 0 progress; replayable via ⓘ button.
 */
(function () {
  "use strict";

  const STORAGE_KEY = "social-r:onboarding";
  const TOUR_VERSION = 1;

  const TOUR_STEPS = [
    {
      id: "welcome",
      target: null,
      title: "Bienvenida a Social R",
      text: "Antes de empezar, veamos cómo funciona la interfaz. Te tomará menos de un minuto.",
      placement: "center",
      showSkip: true,
      nextLabel: "Comenzar →"
    },
    {
      id: "lesson",
      target: '[data-tour="lesson-panel"]',
      fallbackSelector: ".sr-lesson-panel",
      title: "Tu ejercicio",
      text: "Aquí encontrarás la explicación, el objetivo y la tarea que debes resolver.",
      placement: "right"
    },
    {
      id: "editor",
      target: '[data-tour="editor"]',
      fallbackSelector: ".sr-editor-panel",
      title: "Editor de R",
      text: "Escribe o modifica aquí el código que vas a ejecutar.",
      placement: "left"
    },
    {
      id: "run",
      target: '[data-tour="run"]',
      fallbackSelector: ".sr-shortcut-badge",
      title: "Ejecuta tu código",
      text: "Usa Ctrl + Enter para ejecutar el código del editor.",
      placement: "bottom"
    },
    {
      id: "console",
      target: '[data-tour="console"]',
      fallbackSelector: ".sr-console-panel",
      title: "Mira el resultado",
      text: "El resultado de R aparece aquí. También verás mensajes y errores.",
      placement: "top"
    },
    {
      id: "check",
      target: '[data-tour="check"]',
      fallbackSelector: ".sr-btn-submit",
      title: "Comprueba tu solución",
      text: "Cuando termines, comprueba tu respuesta. Social R te dirá si falta algo.",
      placement: "top"
    },
    {
      id: "hints",
      target: '[data-tour="hints"]',
      fallbackSelector: ".sr-help-actions",
      title: "¿Necesitas ayuda?",
      text: "Las pistas aparecen una a una. Úsalas solo cuando las necesites.",
      placement: "right"
    },
    {
      id: "progress",
      target: '[data-tour="progress"]',
      fallbackSelector: ".sr-bottombar",
      title: "Tu progreso",
      text: "Aquí puedes ver dónde estás dentro del módulo y cuánto has avanzado.",
      placement: "top"
    },
    {
      id: "course-map",
      target: '[data-tour="course-map"]',
      fallbackSelector: ".sr-drawer",
      title: "Todo el curso",
      text: "Desde aquí puedes ver los 13 módulos, tus avances y los ejercicios disponibles.",
      placement: "right",
      onEnter: async function (tour) {
        if (window.SocialR && window.SocialR.navigation && typeof window.SocialR.navigation.openDrawer === "function") {
          window.SocialR.navigation.openDrawer();

          // Prevent accidental exercise navigation while drawer is showcased
          const drawerList = document.getElementById("sr-drawer-list");
          if (drawerList) {
            tour._drawerBlocker = (e) => {
              if (e.target.closest(".sr-drawer-item")) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
              }
            };
            drawerList.addEventListener("click", tour._drawerBlocker, true);
            drawerList.addEventListener("keydown", tour._drawerBlocker, true);
          }

          // Wait for drawer slide-in transition (220ms) to complete
          await new Promise((resolve) => setTimeout(resolve, 250));
        }
      },
      onLeave: function (tour) {
        const drawerList = document.getElementById("sr-drawer-list");
        if (drawerList && tour._drawerBlocker) {
          drawerList.removeEventListener("click", tour._drawerBlocker, true);
          drawerList.removeEventListener("keydown", tour._drawerBlocker, true);
          tour._drawerBlocker = null;
        }

        if (window.SocialR && window.SocialR.navigation && typeof window.SocialR.navigation.closeDrawer === "function") {
          window.SocialR.navigation.closeDrawer();
        }
      }
    },
    {
      id: "ready",
      target: null,
      title: "Ya estás listo",
      text: "Lee la tarea, prueba tu código y usa las pistas si las necesitas.",
      placement: "center",
      isLast: true,
      nextLabel: "Empezar →"
    }
  ];

  class OnboardingTour {
    constructor() {
      this.steps = TOUR_STEPS;
      this.currentStepIndex = -1;
      this.active = false;
      this.triggerElement = null;

      this.overlayEl = null;
      this.maskCutoutEl = null;
      this.spotlightBorderEl = null;
      this.cardEl = null;

      this._resizeObserver = null;
      this._boundHandleKeyDown = this.handleKeyDown.bind(this);
      this._boundHandleResize = this.handleResize.bind(this);
    }

    init() {
      this.mountDOM();
      this.bindEvents();
      this.checkAutoLaunch();
    }

    mountDOM() {
      if (document.getElementById("sr-tour-overlay")) {
        this.overlayEl = document.getElementById("sr-tour-overlay");
        this.maskCutoutEl = document.getElementById("sr-tour-cutout");
        this.spotlightBorderEl = document.getElementById("sr-tour-spotlight-border");
        this.cardEl = document.getElementById("sr-tour-card");
        return;
      }

      // 1. Overlay container with SVG mask
      const overlay = document.createElement("div");
      overlay.id = "sr-tour-overlay";
      overlay.className = "sr-tour-overlay";
      overlay.setAttribute("aria-hidden", "true");

      overlay.innerHTML = `
        <svg class="sr-tour-svg-backdrop" width="100%" height="100%">
          <defs>
            <mask id="sr-tour-mask">
              <rect x="0" y="0" width="100%" height="100%" fill="white" />
              <rect id="sr-tour-cutout" x="0" y="0" width="0" height="0" rx="8" ry="8" fill="black" />
            </mask>
          </defs>
          <rect x="0" y="0" width="100%" height="100%" fill="rgba(7, 12, 28, 0.74)" mask="url(#sr-tour-mask)" />
        </svg>
        <div class="sr-tour-click-shield"></div>
      `;

      // 2. Spotlight Highlight Border
      const spotlightBorder = document.createElement("div");
      spotlightBorder.id = "sr-tour-spotlight-border";
      spotlightBorder.className = "sr-tour-spotlight-border";

      // 3. Tour Popover Card
      const card = document.createElement("div");
      card.id = "sr-tour-card";
      card.className = "sr-tour-card";
      card.setAttribute("role", "dialog");
      card.setAttribute("aria-modal", "true");
      card.setAttribute("aria-labelledby", "sr-tour-title");

      card.innerHTML = `
        <div class="sr-tour-card-header">
          <span id="sr-tour-step-badge" class="sr-tour-step-badge">Paso 1 de 10</span>
          <button id="sr-tour-close-btn" class="sr-tour-close-btn" aria-label="Cerrar tutorial">×</button>
        </div>
        <h3 id="sr-tour-title" class="sr-tour-card-title"></h3>
        <p id="sr-tour-text" class="sr-tour-card-text"></p>
        <div class="sr-tour-card-actions">
          <div class="sr-tour-actions-left">
            <button id="sr-tour-skip-btn" class="sr-tour-btn-skip">Saltar tutorial</button>
          </div>
          <div class="sr-tour-actions-right">
            <button id="sr-tour-prev-btn" class="sr-tour-btn-prev">← Anterior</button>
            <button id="sr-tour-next-btn" class="sr-tour-btn-next">Siguiente →</button>
          </div>
        </div>
      `;

      document.body.appendChild(overlay);
      document.body.appendChild(spotlightBorder);
      document.body.appendChild(card);

      this.overlayEl = overlay;
      this.maskCutoutEl = overlay.querySelector("#sr-tour-cutout");
      this.spotlightBorderEl = spotlightBorder;
      this.cardEl = card;
    }

    bindEvents() {
      // Replay button in topbar
      const replayBtn = document.getElementById("sr-tour-btn");
      if (replayBtn) {
        replayBtn.addEventListener("click", () => {
          this.triggerElement = replayBtn;
          this.start(0);
        });
      }

      // Card action buttons
      const nextBtn = document.getElementById("sr-tour-next-btn");
      const prevBtn = document.getElementById("sr-tour-prev-btn");
      const skipBtn = document.getElementById("sr-tour-skip-btn");
      const closeBtn = document.getElementById("sr-tour-close-btn");

      if (nextBtn) nextBtn.addEventListener("click", () => this.next());
      if (prevBtn) prevBtn.addEventListener("click", () => this.prev());
      if (skipBtn) skipBtn.addEventListener("click", () => this.skip());
      if (closeBtn) closeBtn.addEventListener("click", () => this.end(true));

      // Shield click: do nothing (prevents clicks from leaking to interface)
      const shield = this.overlayEl.querySelector(".sr-tour-click-shield");
      if (shield) {
        shield.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
        });
      }
    }

    checkAutoLaunch() {
      // Check stored onboarding state
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && parsed.completed && parsed.version >= TOUR_VERSION) {
            return; // Already completed
          }
        }
      } catch (e) {}

      // Check existing progress: do NOT auto-launch for users with prior progress
      const store = window.SocialR ? window.SocialR.progress : null;
      if (store && typeof store.getCourseProgress === "function") {
        const prog = store.getCourseProgress(88);
        if (prog.completedCount > 0) {
          return;
        }
      }

      // Check active exercise: must be Module 1 Exercise 1
      const nav = window.SocialR ? window.SocialR.navigation : null;
      const currentIdx = nav ? nav.currentIndex : 0;
      if (currentIdx !== 0) {
        return;
      }

      // Auto-launch with short delay for DOM and WebR layout stability
      setTimeout(() => {
        if (!this.active) {
          this.start(0);
        }
      }, 500);
    }

    start(stepIndex = 0) {
      this.active = true;
      document.body.classList.add("is-tour-active");
      this.overlayEl.classList.add("is-active");

      window.addEventListener("keydown", this._boundHandleKeyDown, true);
      window.addEventListener("resize", this._boundHandleResize, { passive: true });

      this.goToStep(stepIndex);
    }

    async goToStep(stepIndex) {
      if (stepIndex < 0 || stepIndex >= this.steps.length) {
        this.end(true);
        return;
      }

      // Call onLeave on previous step if present
      if (this.currentStepIndex >= 0 && this.steps[this.currentStepIndex].onLeave) {
        try {
          this.steps[this.currentStepIndex].onLeave(this);
        } catch (err) {
          console.warn("[OnboardingTour] Error in onLeave hook:", err);
        }
      }

      this.currentStepIndex = stepIndex;
      const step = this.steps[stepIndex];

      // Call onEnter on new step if present
      if (step.onEnter) {
        try {
          await step.onEnter(this);
        } catch (err) {
          console.warn("[OnboardingTour] Error in onEnter hook:", err);
        }
      }

      this.renderStep(step);
    }

    next() {
      if (this.currentStepIndex >= this.steps.length - 1) {
        this.end(true);
      } else {
        this.goToStep(this.currentStepIndex + 1);
      }
    }

    prev() {
      if (this.currentStepIndex > 0) {
        this.goToStep(this.currentStepIndex - 1);
      }
    }

    skip() {
      this.end(true);
    }

    end(saveState = true) {
      if (this.currentStepIndex >= 0 && this.steps[this.currentStepIndex].onLeave) {
        try {
          this.steps[this.currentStepIndex].onLeave(this);
        } catch (e) {}
      }

      this.active = false;
      this.currentStepIndex = -1;

      document.body.classList.remove("is-tour-active");
      this.overlayEl.classList.remove("is-active");
      this.spotlightBorderEl.classList.remove("is-visible");
      this.cardEl.classList.remove("is-visible");

      // Reset spotlight cutout
      this.maskCutoutEl.setAttribute("x", "0");
      this.maskCutoutEl.setAttribute("y", "0");
      this.maskCutoutEl.setAttribute("width", "0");
      this.maskCutoutEl.setAttribute("height", "0");

      window.removeEventListener("keydown", this._boundHandleKeyDown, true);
      window.removeEventListener("resize", this._boundHandleResize);

      if (saveState) {
        try {
          localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({
              completed: true,
              version: TOUR_VERSION,
              completedAt: new Date().toISOString()
            })
          );
        } catch (e) {}
      }

      // Restore focus
      if (this.triggerElement && typeof this.triggerElement.focus === "function") {
        this.triggerElement.focus();
      } else {
        const activeEx = document.querySelector(".social-r-exercise.is-active-exercise");
        if (activeEx) {
          const editor = activeEx.querySelector(".cm-content, textarea, .sr-exercise-title");
          if (editor) editor.focus();
        }
      }
    }

    renderStep(step) {
      // 1. Text & Badges
      const badge = document.getElementById("sr-tour-step-badge");
      const title = document.getElementById("sr-tour-title");
      const text = document.getElementById("sr-tour-text");
      const prevBtn = document.getElementById("sr-tour-prev-btn");
      const nextBtn = document.getElementById("sr-tour-next-btn");
      const skipBtn = document.getElementById("sr-tour-skip-btn");

      badge.textContent = `Paso ${this.currentStepIndex + 1} de ${this.steps.length}`;
      title.textContent = step.title;
      text.textContent = step.text;

      // Previous button visibility
      if (this.currentStepIndex === 0) {
        prevBtn.style.display = "none";
      } else {
        prevBtn.style.display = "inline-flex";
      }

      // Next / Finish button text
      if (step.nextLabel) {
        nextBtn.textContent = step.nextLabel;
      } else if (step.isLast) {
        nextBtn.textContent = "Empezar →";
      } else {
        nextBtn.textContent = "Siguiente →";
      }

      // Skip button
      if (step.isLast) {
        skipBtn.style.visibility = "hidden";
      } else {
        skipBtn.style.visibility = "visible";
      }

      // 2. Target Spotlight & Card Placement
      const targetEl = this.resolveTarget(step);

      if (targetEl) {
        // Ensure visible in scrollable container if needed
        this.ensureVisible(targetEl);

        const rect = targetEl.getBoundingClientRect();
        this.updateSpotlight(rect);
        this.positionCard(rect, step.placement || "bottom");
      } else {
        // Centered step (e.g. Welcome & Conclusion)
        this.clearSpotlight();
        this.positionCardCenter();
      }

      // 3. Make card visible and focus next action
      this.cardEl.classList.add("is-visible");
      setTimeout(() => {
        nextBtn.focus();
      }, 50);
    }

    resolveTarget(step) {
      if (!step.target) return null;

      // First check within active exercise
      const activeEx = document.querySelector(".social-r-exercise.is-active-exercise");
      let el = null;

      if (activeEx) {
        el = activeEx.querySelector(step.target);
        if (!el && step.fallbackSelector) {
          el = activeEx.querySelector(step.fallbackSelector);
        }
      }

      // Global check if not inside exercise (e.g. drawer, bottombar)
      if (!el) {
        el = document.querySelector(step.target);
      }
      if (!el && step.fallbackSelector) {
        el = document.querySelector(step.fallbackSelector);
      }

      return el;
    }

    ensureVisible(targetEl) {
      // Check if target is inside the lesson panel scroll container
      const lessonPanel = targetEl.closest(".sr-lesson-panel");
      if (lessonPanel) {
        const lRect = lessonPanel.getBoundingClientRect();
        const tRect = targetEl.getBoundingClientRect();
        if (tRect.top < lRect.top || tRect.bottom > lRect.bottom) {
          targetEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      }
    }

    updateSpotlight(rect) {
      const pad = 6;
      const x = Math.max(0, rect.left - pad);
      const y = Math.max(0, rect.top - pad);
      const width = rect.width + pad * 2;
      const height = rect.height + pad * 2;
      const radius = 8;

      // Update SVG Cutout
      this.maskCutoutEl.setAttribute("x", String(x));
      this.maskCutoutEl.setAttribute("y", String(y));
      this.maskCutoutEl.setAttribute("width", String(width));
      this.maskCutoutEl.setAttribute("height", String(height));
      this.maskCutoutEl.setAttribute("rx", String(radius));
      this.maskCutoutEl.setAttribute("ry", String(radius));

      // Update Highlight Frame
      this.spotlightBorderEl.style.top = `${y}px`;
      this.spotlightBorderEl.style.left = `${x}px`;
      this.spotlightBorderEl.style.width = `${width}px`;
      this.spotlightBorderEl.style.height = `${height}px`;
      this.spotlightBorderEl.style.borderRadius = `${radius}px`;
      this.spotlightBorderEl.classList.add("is-visible");
    }

    clearSpotlight() {
      this.maskCutoutEl.setAttribute("x", "0");
      this.maskCutoutEl.setAttribute("y", "0");
      this.maskCutoutEl.setAttribute("width", "0");
      this.maskCutoutEl.setAttribute("height", "0");
      this.spotlightBorderEl.classList.remove("is-visible");
    }

    positionCard(targetRect, preferredPlacement) {
      // In mobile viewports (<= 640px), layout is handled via bottom-sheet CSS
      if (window.innerWidth <= 640) {
        this.cardEl.style.top = "auto";
        this.cardEl.style.left = "0.75rem";
        return;
      }

      const cardRect = this.cardEl.getBoundingClientRect();
      const cardWidth = cardRect.width || 360;
      const cardHeight = cardRect.height || 180;
      const gap = 16;
      const viewportPad = 14;

      let top = 0;
      let left = 0;

      switch (preferredPlacement) {
        case "right":
          left = targetRect.right + gap;
          top = targetRect.top + (targetRect.height - cardHeight) / 2;
          // Fallback if overflowing right
          if (left + cardWidth > window.innerWidth - viewportPad) {
            left = targetRect.left - cardWidth - gap;
          }
          break;

        case "left":
          left = targetRect.left - cardWidth - gap;
          top = targetRect.top + (targetRect.height - cardHeight) / 2;
          // Fallback if overflowing left
          if (left < viewportPad) {
            left = targetRect.right + gap;
          }
          break;

        case "top":
          left = targetRect.left + (targetRect.width - cardWidth) / 2;
          top = targetRect.top - cardHeight - gap;
          // Fallback if overflowing top
          if (top < viewportPad) {
            top = targetRect.bottom + gap;
          }
          break;

        case "bottom":
        default:
          left = targetRect.left + (targetRect.width - cardWidth) / 2;
          top = targetRect.bottom + gap;
          // Fallback if overflowing bottom
          if (top + cardHeight > window.innerHeight - viewportPad) {
            top = targetRect.top - cardHeight - gap;
          }
          break;
      }

      // Clamp to viewport
      left = Math.max(viewportPad, Math.min(left, window.innerWidth - cardWidth - viewportPad));
      top = Math.max(viewportPad, Math.min(top, window.innerHeight - cardHeight - viewportPad));

      this.cardEl.style.left = `${left}px`;
      this.cardEl.style.top = `${top}px`;
    }

    positionCardCenter() {
      if (window.innerWidth <= 640) {
        this.cardEl.style.top = "auto";
        this.cardEl.style.left = "0.75rem";
        return;
      }

      const cardRect = this.cardEl.getBoundingClientRect();
      const cardWidth = cardRect.width || 380;
      const cardHeight = cardRect.height || 200;

      const left = (window.innerWidth - cardWidth) / 2;
      const top = (window.innerHeight - cardHeight) / 2;

      this.cardEl.style.left = `${left}px`;
      this.cardEl.style.top = `${top}px`;
    }

    handleKeyDown(e) {
      if (!this.active) return;

      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        this.end(true);
        return;
      }

      if (e.key === "ArrowRight" && e.altKey) {
        e.preventDefault();
        this.next();
        return;
      }

      if (e.key === "ArrowLeft" && e.altKey) {
        e.preventDefault();
        this.prev();
        return;
      }

      // Focus trap within card
      if (e.key === "Tab") {
        const focusables = Array.from(
          this.cardEl.querySelectorAll('button:not([style*="display: none"]), [tabindex="0"]')
        ).filter((el) => el.offsetParent !== null);

        if (focusables.length === 0) return;

        const first = focusables[0];
        const last = focusables[focusables.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    }

    handleResize() {
      if (!this.active || this.currentStepIndex < 0) return;
      const step = this.steps[this.currentStepIndex];
      const targetEl = this.resolveTarget(step);

      if (targetEl) {
        const rect = targetEl.getBoundingClientRect();
        this.updateSpotlight(rect);
        this.positionCard(rect, step.placement || "bottom");
      } else {
        this.positionCardCenter();
      }
    }
  }

  // Global Tour Instance Initialization
  window.SocialR = window.SocialR || {};
  const tour = new OnboardingTour();
  window.SocialR.tour = tour;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => tour.init());
  } else {
    tour.init();
  }
})();
