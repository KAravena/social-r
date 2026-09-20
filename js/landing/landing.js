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
   * Sync landing page CTAs and Module Progress badges with localStorage
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

    if (storeState) {
      if (storeState.modules && typeof storeState.modules === "object") {
        for (const m of Object.values(storeState.modules)) {
          if (Array.isArray(m.completedExercises)) {
            completedExCount += m.completedExercises.length;
          }
        }
      } else if (Array.isArray(storeState.completed)) {
        completedExCount = storeState.completed.length;
      }

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
      }
    }

    const targetUrl = `curso.html#${targetExId}`;

    // Update Hero Primary CTA
    const heroBtn = document.getElementById("sr-hero-cta");
    const heroBtnText = document.getElementById("sr-hero-cta-text");
    const heroProgressPill = document.getElementById("sr-hero-progress-pill");

    if (heroBtn) {
      heroBtn.setAttribute("href", targetUrl);
    }

    if (hasProgress) {
      if (heroBtnText) heroBtnText.textContent = "Continuar curso →";
      if (heroProgressPill) {
        heroProgressPill.style.display = "inline-flex";
        heroProgressPill.textContent = `${completedExCount} de 88 ejercicios completados`;
      }
    } else {
      if (heroBtnText) heroBtnText.textContent = "Comenzar curso →";
      if (heroProgressPill) heroProgressPill.style.display = "none";
    }

    // Update Nav CTA
    const navBtn = document.getElementById("sr-nav-cta");
    if (navBtn) {
      navBtn.setAttribute("href", targetUrl);
      navBtn.textContent = hasProgress ? "Continuar curso" : "Comenzar curso";
    }

    // Update Final CTA
    const finalBtn = document.getElementById("sr-final-cta");
    if (finalBtn) {
      finalBtn.setAttribute("href", targetUrl);
      finalBtn.textContent = hasProgress ? "Continuar con tu progreso →" : "Comenzar curso gratis →";
    }

    // Update Module Badges in Curriculum Section
    const moduleRows = document.querySelectorAll(".sr-module-row");
    moduleRows.forEach((row) => {
      const modId = row.getAttribute("data-module-id");
      const badge = row.querySelector(".sr-module-badge");
      const modTotal = parseInt(row.getAttribute("data-module-total") || "8", 10);
      const firstExId = row.getAttribute("data-first-ex") || "intro-r-01-001";

      let modCompleted = 0;
      let isModDone = false;

      if (storeState) {
        if (storeState.modules && storeState.modules[modId]) {
          const mData = storeState.modules[modId];
          if (Array.isArray(mData.completedExercises)) {
            modCompleted = mData.completedExercises.length;
          }
          isModDone = Boolean(mData.completed || mData.isCompleted || modCompleted >= modTotal);
        } else if (storeState.moduleProgression && storeState.moduleProgression[modId]) {
          const mData = storeState.moduleProgression[modId];
          isModDone = Boolean(mData.completed);
          if (Array.isArray(storeState.completed)) {
            const modNumMatch = modId.match(/^(\d{2})-/);
            if (modNumMatch) {
              const modPrefix = `intro-r-${modNumMatch[1]}-`;
              modCompleted = storeState.completed.filter((id) => id.startsWith(modPrefix)).length;
            }
          }
        } else if (Array.isArray(storeState.completed)) {
          const modNumMatch = modId.match(/^(\d{2})-/);
          if (modNumMatch) {
            const modPrefix = `intro-r-${modNumMatch[1]}-`;
            modCompleted = storeState.completed.filter((id) => id.startsWith(modPrefix)).length;
            isModDone = modCompleted >= modTotal;
          }
        }
      }

      if (badge) {
        if (isModDone) {
          badge.className = "sr-module-badge is-completed";
          badge.innerHTML = `<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg> Completado`;
        } else if (modCompleted > 0) {
          badge.className = "sr-module-badge is-progress";
          badge.textContent = `${modCompleted}/${modTotal} en progreso`;
        } else if (modId === "01-empezar-a-pensar-con-r" || hasProgress) {
          badge.className = "sr-module-badge is-available";
          badge.textContent = "Disponible";
        } else {
          badge.className = "sr-module-badge is-ready";
          badge.textContent = "Por comenzar";
        }
      }

      // Make module clickable to enter directly
      row.style.cursor = "pointer";
      row.addEventListener("click", () => {
        let destEx = firstExId;
        if (storeState && storeState.modules && storeState.modules[modId] && storeState.modules[modId].currentExerciseId) {
          destEx = storeState.modules[modId].currentExerciseId;
        }
        window.location.href = `curso.html#${destEx}`;
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
    syncProgress();
    initSmoothScroll();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
