/**
 * Social R Platform - Global Course Reset Manager
 * Safely resets pedagogical progress, restored starter codes, updates drawers/landing,
 * and preserves onboarding completion status and visual preferences.
 * NEVER uses localStorage.clear().
 */
(function () {
  "use strict";

  window.SocialR = window.SocialR || {};

  const PRESERVED_KEYS = new Set([
    "social-r:onboarding",
    "social-r:left-width",
    "social-r:editor-height",
    "social-r:dev_mode"
  ]);

  let triggerElement = null;
  let keydownListener = null;

  /**
   * Safely purge course pedagogical storage while keeping preferences & onboarding
   */
  function purgeCourseStorage() {
    try {
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (!key) continue;

        // Never touch preserved keys
        if (PRESERVED_KEYS.has(key)) continue;

        // Target course progress namespaces and Quarto Live editor caches
        if (
          key.startsWith("social-r:progress") ||
          key.startsWith("editor-")
        ) {
          keysToRemove.push(key);
        }
      }

      keysToRemove.forEach((k) => {
        try {
          localStorage.removeItem(k);
        } catch (err) {
          console.warn("[CourseReset] Error removing key:", k, err);
        }
      });

      // Synchronize runtime store if present
      if (window.SocialR && window.SocialR.progress && typeof window.SocialR.progress.resetProgress === "function") {
        window.SocialR.progress.resetProgress();
      }
    } catch (e) {
      console.warn("[CourseReset] Storage purge error:", e);
    }
  }

  /**
   * Performs full pedagogical reset and updates UI
   */
  function performReset() {
    // 1. Purge storage
    purgeCourseStorage();

    // 2. If in application (curso.html)
    if (window.SocialR && window.SocialR.navigation) {
      const nav = window.SocialR.navigation;

      // Reset each exercise DOM & adapter state
      if (Array.isArray(nav.exercises)) {
        nav.exercises.forEach((ex) => {
          // Reset hints
          if (window.SocialR.adapter && typeof window.SocialR.adapter.resetHints === "function") {
            window.SocialR.adapter.resetHints(ex.id);
          }
          // Reset feedback card
          if (ex.node) {
            const fb = ex.node.querySelector(".sr-feedback-card");
            if (fb) {
              fb.className = "sr-feedback-card";
              fb.innerHTML = "";
            }
          }
          // Reset editor code to initial starter code
          if (window.SocialR.adapter && typeof window.SocialR.adapter.reset === "function") {
            try {
              window.SocialR.adapter.reset(ex.id);
            } catch (err) {}
          }
        });
      }

      // Close drawer if open
      if (typeof nav.closeDrawer === "function") {
        nav.closeDrawer();
      }

      // Mark drawer dirty and navigate to M1E1
      nav.drawerDirty = true;
      if (typeof nav.goToIndex === "function") {
        nav.goToIndex(0);
      }
      if (typeof nav.refreshUI === "function") {
        nav.refreshUI();
      }
    }

    // 3. If on Landing page (index.html)
    if (window.SocialR && typeof window.SocialR.syncProgress === "function") {
      window.SocialR.syncProgress();
    }

    // 4. Emit event for custom listeners
    if (window.SocialR && window.SocialR.events) {
      window.SocialR.events.emit("course_reset_completed");
    }

    // 5. Show brief toast notification
    showToast("Progreso del curso reiniciado.");
  }

  /**
   * Builds or retrieves modal DOM elements
   */
  function ensureModalElements() {
    let backdrop = document.getElementById("sr-reset-modal-backdrop");
    if (backdrop) return backdrop;

    backdrop = document.createElement("div");
    backdrop.id = "sr-reset-modal-backdrop";
    backdrop.className = "sr-reset-modal-backdrop";
    backdrop.setAttribute("aria-hidden", "true");

    backdrop.innerHTML = `
      <div id="sr-reset-modal" class="sr-reset-modal-card" role="dialog" aria-modal="true" aria-labelledby="sr-reset-modal-title" aria-describedby="sr-reset-modal-desc">
        <div class="sr-reset-modal-header">
          <div class="sr-reset-modal-icon-box" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <h3 id="sr-reset-modal-title" class="sr-reset-modal-title">Reiniciar todo el curso</h3>
        </div>
        <div class="sr-reset-modal-body">
          <p id="sr-reset-modal-desc" class="sr-reset-modal-desc">
            Se borrará tu progreso y volverás al primer ejercicio. Esta acción no se puede deshacer.<br><br>
            También se restablecerán tus ejercicios, pistas y respuestas guardadas.
          </p>
        </div>
        <div class="sr-reset-modal-footer">
          <button id="sr-reset-modal-cancel" class="sr-reset-modal-btn-cancel" type="button">Cancelar</button>
          <button id="sr-reset-modal-confirm" class="sr-reset-modal-btn-danger" type="button">Reiniciar curso</button>
        </div>
      </div>
    `;

    document.body.appendChild(backdrop);

    // Click outside modal card to cancel
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) {
        closeModal();
      }
    });

    const cancelBtn = backdrop.querySelector("#sr-reset-modal-cancel");
    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => closeModal());
    }

    const confirmBtn = backdrop.querySelector("#sr-reset-modal-confirm");
    if (confirmBtn) {
      confirmBtn.addEventListener("click", () => {
        closeModal();
        performReset();
      });
    }

    return backdrop;
  }

  function openModal(trigger) {
    triggerElement = trigger || document.activeElement;
    const backdrop = ensureModalElements();
    backdrop.removeAttribute("aria-hidden");
    backdrop.classList.add("is-visible");

    const cancelBtn = backdrop.querySelector("#sr-reset-modal-cancel");
    const confirmBtn = backdrop.querySelector("#sr-reset-modal-confirm");

    if (cancelBtn) {
      setTimeout(() => cancelBtn.focus(), 50);
    }

    // Focus trap & Escape key
    if (keydownListener) {
      document.removeEventListener("keydown", keydownListener);
    }

    keydownListener = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        closeModal();
        return;
      }

      if (e.key === "Tab") {
        const focusables = [cancelBtn, confirmBtn].filter(Boolean);
        if (focusables.length === 0) return;

        const first = focusables[0];
        const last = focusables[focusables.length - 1];

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };

    document.addEventListener("keydown", keydownListener);
  }

  function closeModal() {
    const backdrop = document.getElementById("sr-reset-modal-backdrop");
    if (backdrop) {
      backdrop.setAttribute("aria-hidden", "true");
      backdrop.classList.remove("is-visible");
    }

    if (keydownListener) {
      document.removeEventListener("keydown", keydownListener);
      keydownListener = null;
    }

    if (triggerElement && typeof triggerElement.focus === "function") {
      try {
        triggerElement.focus();
      } catch (err) {}
      triggerElement = null;
    }
  }

  function showToast(message) {
    let toast = document.getElementById("sr-reset-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "sr-reset-toast";
      toast.className = "sr-reset-toast";
      document.body.appendChild(toast);
    }

    toast.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 16 16" fill="#10b981" aria-hidden="true">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
      </svg>
      <span>${message}</span>
    `;

    toast.classList.add("is-visible");
    setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 2800);
  }

  function initResetTriggers() {
    // Drawer reset button in curso.html
    const drawerResetBtn = document.getElementById("sr-drawer-reset-btn");
    if (drawerResetBtn) {
      drawerResetBtn.addEventListener("click", (e) => {
        e.preventDefault();
        openModal(drawerResetBtn);
      });
    }

    // Landing footer reset button in index.html
    const landingResetBtn = document.getElementById("sr-landing-reset-btn");
    if (landingResetBtn) {
      landingResetBtn.addEventListener("click", (e) => {
        e.preventDefault();
        openModal(landingResetBtn);
      });
    }
  }

  // Auto-init on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResetTriggers);
  } else {
    initResetTriggers();
  }

  // Public API
  window.SocialR.courseReset = {
    openModal,
    closeModal,
    performReset,
    initResetTriggers
  };
  window.SocialR.resetCourse = performReset;
})();
