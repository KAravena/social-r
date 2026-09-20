/**
 * Social R Platform - App Shell v0.4.0
 * Coordinates topbar, webR status indicator, drawer, dev mode, and global navigation.
 */
(function () {
  "use strict";

  function initShell() {
    console.log("[Social R Shell] Initializing App Shell & WebR Status Monitor...");
    initWebRStatus();
    initDevMode();
    initDrawer();
    initKeyboardShortcuts();
    initTour();
  }

  function initTour() {
    const replayBtn = document.getElementById("sr-tour-btn");
    if (replayBtn) {
      replayBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (window.SocialR && window.SocialR.tour && typeof window.SocialR.tour.start === "function") {
          window.SocialR.tour.triggerElement = replayBtn;
          window.SocialR.tour.start(0);
        }
      });
    }
  }

  function initWebRStatus() {
    const statusContainer = document.getElementById("sr-webr-status");
    const statusText = document.getElementById("sr-webr-status-text");

    let checks = 0;
    const interval = setInterval(() => {
      checks++;
      let isReady = false;

      try {
        const runBtn = document.querySelector(".exercise-editor-btn-run-code, .btn-exercise-editor.btn-primary");
        if (runBtn && !runBtn.classList.contains("disabled")) {
          isReady = true;
        } else if (window.webR && window.webR.ready) {
          isReady = true;
        }
      } catch (e) {}

      if (isReady) {
        clearInterval(interval);
        if (statusContainer) {
          statusContainer.classList.add("is-ready");
          statusContainer.classList.remove("is-error");
        }
        if (statusText) statusText.textContent = "R listo";
        if (window.SocialR && window.SocialR.events) {
          window.SocialR.events.emit("webr_ready");
        }
        console.log("[Social R Shell] WebR Status transitioned to 'R listo'.");
      } else if (checks > 120) {
        clearInterval(interval);
        if (statusContainer) statusContainer.classList.add("is-error");
        if (statusText) statusText.textContent = "Error al iniciar R";
      }
    }, 400);
  }

  function initDevMode() {
    const toggle = document.getElementById("sr-dev-mode-checkbox");
    if (!toggle) return;

    const saved = localStorage.getItem("social-r:dev_mode") === "true";
    if (window.SocialR) window.SocialR.devMode = saved;
    toggle.checked = saved;

    toggle.addEventListener("change", (e) => {
      if (window.SocialR) window.SocialR.devMode = e.target.checked;
      localStorage.setItem("social-r:dev_mode", e.target.checked);
      if (window.SocialR && window.SocialR.navigation) {
        window.SocialR.navigation.refreshUI();
      }
    });
  }

  function initDrawer() {
    // Course Outline drawer events and lifecycle are managed by NavigationManager in navigation.js
  }

  function initKeyboardShortcuts() {
    document.addEventListener("keydown", (e) => {
      const activeId = window.SocialR && window.SocialR.getActiveExerciseId ? window.SocialR.getActiveExerciseId() : null;
      if (!activeId) return;

      // 1. Alt + P -> Next Hint
      if (e.altKey && (e.key === "p" || e.key === "P")) {
        e.preventDefault();
        if (window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.revealNextHint(activeId);
        }
        return;
      }

      // 2. Alt + Left / Alt + Right -> Navigation
      if (e.altKey && e.key === "ArrowLeft") {
        e.preventDefault();
        if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.previous();
        return;
      }

      if (e.altKey && e.key === "ArrowRight") {
        e.preventDefault();
        if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.next();
        return;
      }

      // 3. Escape -> Close drawer
      if (e.key === "Escape") {
        const backdrop = document.getElementById("sr-drawer-backdrop");
        if (backdrop && backdrop.classList.contains("is-open")) {
          if (window.SocialR && window.SocialR.navigation && typeof window.SocialR.navigation.closeDrawer === "function") {
            window.SocialR.navigation.closeDrawer();
          } else {
            backdrop.classList.remove("is-open");
          }
        }
      }
    });
  }

  // Auto-boot shell on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initShell);
  } else {
    initShell();
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.initShell = initShell;
})();
