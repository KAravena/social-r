/**
 * Social R - Landing Page Controller v1.0
 * Coordinates hero animations (ColorBends + DotField), progress sync from localStorage,
 * dynamic CTA (Comenzar vs Continuar), and module status rendering.
 */
import { initHeroColorBends } from "./hero-color-bends.js";
import { initHeroDotField } from "./hero-dots.js";

(function () {
  "use strict";

  // Deep link safeguard: If visiting index.html with an exercise hash, redirect to course
  if (window.location.hash && /^#intro-r-/.test(window.location.hash)) {
    window.location.replace("curso.html" + window.location.hash);
    return;
  }

  const heroMotionState = {
    timeSec: 0,
    lastFrameTime: null,
    animationId: null,
    reduceMotion: false,
    isInViewport: true,
    isDocumentVisible: !document.hidden,
    initialized: false,
    drawBendsFunc: null,
    drawDotsFunc: null,
    requestFrame: requestHeroFrame
  };

  let colorBendsInstance = null;

  function shouldAnimateHero() {
    return (
      !heroMotionState.reduceMotion &&
      heroMotionState.isInViewport &&
      heroMotionState.isDocumentVisible
    );
  }

  function requestHeroFrame() {
    if (heroMotionState.animationId !== null || !shouldAnimateHero()) return;
    heroMotionState.animationId = requestAnimationFrame(animateMasterLoop);
  }

  function stopHeroLoop() {
    if (heroMotionState.animationId !== null) {
      cancelAnimationFrame(heroMotionState.animationId);
      heroMotionState.animationId = null;
    }
    heroMotionState.lastFrameTime = null;
  }

  function drawHeroStaticFrame() {
    const t = heroMotionState.timeSec || 0.5;
    if (heroMotionState.drawBendsFunc) heroMotionState.drawBendsFunc(t);
    if (heroMotionState.drawDotsFunc) heroMotionState.drawDotsFunc(t);
  }

  function animateMasterLoop(now) {
    heroMotionState.animationId = null;

    if (!shouldAnimateHero()) {
      heroMotionState.lastFrameTime = null;
      return;
    }

    if (heroMotionState.lastFrameTime === null) {
      heroMotionState.lastFrameTime = now;
    }

    const delta = Math.min((now - heroMotionState.lastFrameTime) * 0.001, 0.05);
    heroMotionState.lastFrameTime = now;
    heroMotionState.timeSec += delta;

    if (heroMotionState.drawBendsFunc) heroMotionState.drawBendsFunc(heroMotionState.timeSec);
    if (heroMotionState.drawDotsFunc) heroMotionState.drawDotsFunc(heroMotionState.timeSec);

    requestHeroFrame();
  }

  function initHeroVisuals() {
    const hero = document.querySelector(".sr-hero");
    if (!hero) return;

    heroMotionState.reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Visibility Observer to suspend animations off-screen
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          const entry = entries[0];
          heroMotionState.isInViewport = Boolean(entry && entry.isIntersecting);
          if (heroMotionState.isInViewport) {
            drawHeroStaticFrame();
            requestHeroFrame();
          } else {
            stopHeroLoop();
          }
        },
        { rootMargin: "100px 0px" }
      );
      observer.observe(hero);
    }

    // Document visibility listener
    document.addEventListener("visibilitychange", () => {
      heroMotionState.isDocumentVisible = !document.hidden;
      if (!heroMotionState.isDocumentVisible) {
        stopHeroLoop();
      } else {
        drawHeroStaticFrame();
        requestHeroFrame();
      }
    });

    // Initialize WebGL ColorBends
    try {
      colorBendsInstance = initHeroColorBends({ useExternalLoop: true });
      if (colorBendsInstance && typeof colorBendsInstance.render === "function") {
        heroMotionState.drawBendsFunc = colorBendsInstance.render;
      }
    } catch (e) {
      console.warn("[Social R] Could not initialize ColorBends WebGL:", e);
    }

    // Initialize 2D DotField
    try {
      initHeroDotField(colorBendsInstance, heroMotionState);
    } catch (e) {
      console.warn("[Social R] Could not initialize DotField Canvas:", e);
    }

    if (heroMotionState.reduceMotion) {
      drawHeroStaticFrame();
    } else {
      requestHeroFrame();
    }
  }

  /**
   * Sync landing page CTAs, Hero Progress, Accordion Badges, and Exercise Statuses
   */
  function syncProgress() {
    let storeState = null;
    try {
      const raw =
        localStorage.getItem("social-r:progress:intro-r") ||
        localStorage.getItem("social-r:progress:v2") ||
        localStorage.getItem("social-r:progress:intro-r:01-primeros-pasos") ||
        localStorage.getItem("social-r:progress");
      if (raw) {
        storeState = JSON.parse(raw);
      }
    } catch (e) {
      console.warn("[Social R] Failed to parse progress store:", e);
    }

    let hasProgress = false;
    let targetExId = "intro-r-01-001";
    let completedExCount = 0;
    let activeModuleId = "01-empezar-a-pensar-con-r";
    const completedSet = new Set();

    if (storeState) {
      if (storeState.modules && typeof storeState.modules === "object") {
        for (const [mId, m] of Object.entries(storeState.modules)) {
          if (Array.isArray(m.completedExercises)) {
            m.completedExercises.forEach((id) => {
              completedSet.add(id);
            });
          }
        }
      } else if (Array.isArray(storeState.completed)) {
        storeState.completed.forEach((id) => completedSet.add(id));
      }

      completedExCount = completedSet.size;

      if (storeState.currentExerciseId && storeState.currentExerciseId !== "intro-r-01-001") {
        hasProgress = true;
        targetExId = storeState.currentExerciseId;
      } else if (completedExCount > 0) {
        hasProgress = true;
        if (storeState.currentExerciseId) {
          targetExId = storeState.currentExerciseId;
        }
      }

      if (storeState.activeModuleId) {
        activeModuleId = storeState.activeModuleId;
      } else if (targetExId) {
        const match = targetExId.match(/intro-r-(\d{2})-/);
        if (match) {
          const modSlugs = [
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
          const num = parseInt(match[1], 10);
          if (num >= 1 && num <= 13) {
            activeModuleId = modSlugs[num - 1];
          }
        }
      }
    }

    const targetUrl = `curso.html#${targetExId}`;

    // Update Hero Primary CTA
    const heroBtn = document.getElementById("sr-hero-cta");
    const heroBtnText = document.getElementById("sr-hero-cta-text");
    const heroProgressLine = document.getElementById("sr-hero-progress-line");

    if (heroBtn) {
      heroBtn.setAttribute("href", targetUrl);
    }

    if (hasProgress) {
      if (heroBtnText) heroBtnText.textContent = "Continuar curso →";
      if (heroProgressLine) {
        heroProgressLine.style.display = "block";
        heroProgressLine.textContent = `${completedExCount}/88 ejercicios completados`;
      }
    } else {
      if (heroBtnText) heroBtnText.textContent = "Comenzar curso →";
      if (heroProgressLine) heroProgressLine.style.display = "none";
    }

    // Update Module Badges & Exercise items in Accordion
    const accordionItems = document.querySelectorAll(".sr-accordion-item");
    accordionItems.forEach((item) => {
      const modId = item.getAttribute("data-module-id");
      const badge = item.querySelector(".sr-module-badge");
      const modTotal = parseInt(item.getAttribute("data-module-total") || "8", 10);

      let modCompletedCount = 0;
      let isModDone = false;

      // Check exercises inside this module
      const exItems = item.querySelectorAll(".sr-exercise-item");
      let previousCompleted = true; // First exercise in module is unlocked by default

      exItems.forEach((exEl, exIdx) => {
        const exId = exEl.getAttribute("data-ex-id");
        const isDone = completedSet.has(exId);
        const isCur = exId === targetExId;
        const iconEl = exEl.querySelector(".sr-ex-status-icon");
        const linkEl = exEl.querySelector(".sr-ex-link");

        if (isDone) {
          modCompletedCount++;
          exEl.className = "sr-exercise-item is-completed";
          if (iconEl) iconEl.innerHTML = `<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg>`;
          if (linkEl) {
            linkEl.removeAttribute("tabindex");
            linkEl.removeAttribute("aria-disabled");
          }
          previousCompleted = true;
        } else if (isCur) {
          exEl.className = "sr-exercise-item is-current";
          if (iconEl) iconEl.textContent = "●";
          if (linkEl) {
            linkEl.removeAttribute("tabindex");
            linkEl.removeAttribute("aria-disabled");
          }
          previousCompleted = false;
        } else if (exIdx === 0 || previousCompleted) {
          exEl.className = "sr-exercise-item is-available";
          if (iconEl) iconEl.textContent = "○";
          if (linkEl) {
            linkEl.removeAttribute("tabindex");
            linkEl.removeAttribute("aria-disabled");
          }
          previousCompleted = false;
        } else {
          exEl.className = "sr-exercise-item is-locked";
          if (iconEl) iconEl.textContent = "";
          if (linkEl) {
            linkEl.setAttribute("tabindex", "-1");
            linkEl.setAttribute("aria-disabled", "true");
          }
          previousCompleted = false;
        }
      });

      if (storeState && storeState.modules && storeState.modules[modId]) {
        const mData = storeState.modules[modId];
        isModDone = Boolean(mData.completed || mData.isCompleted || modCompletedCount >= modTotal);
      } else {
        isModDone = modCompletedCount >= modTotal;
      }

      if (badge) {
        if (isModDone) {
          badge.className = "sr-module-badge is-completed";
          badge.innerHTML = `<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg> Completado`;
        } else if (modCompletedCount > 0) {
          badge.className = "sr-module-badge is-progress";
          badge.textContent = `${modCompletedCount}/${modTotal}`;
        } else {
          badge.className = "sr-module-badge";
          badge.textContent = "";
        }
      }
    });

    // Default accordion expansion
    let targetModuleEl = null;
    if (hasProgress && activeModuleId) {
      targetModuleEl = document.querySelector(`.sr-accordion-item[data-module-id="${activeModuleId}"]`);
    }
    if (!targetModuleEl) {
      targetModuleEl = document.querySelector(`.sr-accordion-item[data-module-order="1"]`);
    }
    if (targetModuleEl) {
      setAccordionExpanded(targetModuleEl, true);
    }
  }

  /**
   * Expand/collapse a single accordion item
   */
  function setAccordionExpanded(itemEl, expanded) {
    const header = itemEl.querySelector(".sr-accordion-header");
    if (expanded) {
      itemEl.classList.add("is-expanded");
      if (header) header.setAttribute("aria-expanded", "true");
    } else {
      itemEl.classList.remove("is-expanded");
      if (header) header.setAttribute("aria-expanded", "false");
    }
  }

  /**
   * Initialize interactive accordion functionality
   */
  function initAccordion() {
    const items = document.querySelectorAll(".sr-accordion-item");
    items.forEach((item) => {
      const header = item.querySelector(".sr-accordion-header");
      if (!header) return;

      header.addEventListener("click", (e) => {
        e.preventDefault();
        const isCurrentlyExpanded = item.classList.contains("is-expanded");

        // Close all other items (single expansion accordion)
        items.forEach((other) => {
          if (other !== item) {
            setAccordionExpanded(other, false);
          }
        });

        // Toggle clicked item
        setAccordionExpanded(item, !isCurrentlyExpanded);
      });
    });
  }

  // Smooth scroll for internal anchors
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href");
        if (targetId && targetId !== "#") {
          const targetEl = document.querySelector(targetId);
          if (targetEl) {
            e.preventDefault();
            targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });
    });
  }

  // Single clean initialization
  function boot() {
    initHeroVisuals();
    initAccordion();
    syncProgress();
    initSmoothScroll();
  }

  // Expose for external coordination (e.g., course reset)
  window.SocialR = window.SocialR || {};
  window.SocialR.syncProgress = syncProgress;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

