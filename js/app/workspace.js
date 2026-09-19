/**
 * Social R Platform - Workspace Manager
 * Coordinates action toolbars, hints, and feedback cards.
 */
(function () {
  "use strict";

  function initWorkspace() {
    bindActionButtons();
    initFeedbackObserver();
  }

  function bindActionButtons() {
    // 1. Run Buttons
    document.querySelectorAll(".sr-btn-run").forEach((btn) => {
      btn.addEventListener("click", () => {
        const exId = btn.getAttribute("data-exercise-id");
        if (exId && window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.run(exId);
        }
      });
    });

    // 2. Submit Buttons
    document.querySelectorAll(".sr-btn-submit").forEach((btn) => {
      btn.addEventListener("click", () => {
        const exId = btn.getAttribute("data-exercise-id");
        if (exId && window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.submit(exId);
        }
      });
    });

    // 3. Reset Buttons
    document.querySelectorAll(".sr-btn-reset").forEach((btn) => {
      btn.addEventListener("click", () => {
        const exId = btn.getAttribute("data-exercise-id");
        if (exId && window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.reset(exId);
        }
      });
    });

    // 4. Progressive Hint Buttons
    document.querySelectorAll(".sr-hint-toggle-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const exId = btn.getAttribute("data-exercise-id");
        if (exId && window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.toggleHint(exId);
        }
      });
    });

    // 5. Clear Console Buttons
    document.querySelectorAll(".sr-btn-clear-console").forEach((btn) => {
      btn.addEventListener("click", () => {
        const exId = btn.getAttribute("data-exercise-id") || (window.SocialR && window.SocialR.getActiveExerciseId ? window.SocialR.getActiveExerciseId() : null);
        if (exId && window.SocialR && window.SocialR.adapter) {
          window.SocialR.adapter.clearConsole(exId);
        }
      });
    });
  }

  function initFeedbackObserver() {
    // Observe when Quarto Live generates grading alert
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const grades = node.classList && node.classList.contains("exercise-grade")
              ? [node]
              : Array.from(node.querySelectorAll ? node.querySelectorAll(".exercise-grade") : []);

            grades.forEach((gradeEl) => {
              processGradeFeedback(gradeEl);
            });
          }
        });
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  function processGradeFeedback(gradeEl) {
    const exContainer = gradeEl.closest(".social-r-exercise");
    if (!exContainer) return;

    const exId = exContainer.getAttribute("data-exercise-id");
    if (!exId) return;

    const feedbackCard = exContainer.querySelector(".sr-feedback-card");
    if (!feedbackCard) return;

    const text = gradeEl.textContent || "";
    const isCorrect = gradeEl.classList.contains("alert-success") || text.includes("¡Muy bien!") || text.includes("¡Excelente!") || text.includes("¡Bien!");
    const isWarning = gradeEl.classList.contains("alert-warning");
    const isInfo = gradeEl.classList.contains("alert-info");

    feedbackCard.className = "sr-feedback-card is-visible";
    if (isCorrect) {
      feedbackCard.classList.add("is-success");
      feedbackCard.innerHTML = `<strong>✓ ¡Excelente trabajo!</strong><p>${text.replace(/^Feedback:?/i, "").trim()}</p>`;

      // Save completion
      window.SocialR.progress.save(exId, { status: "completed" });
      window.SocialR.events.emit("answer_correct", { exerciseId: exId });
      window.SocialR.events.emit("exercise_completed", { exerciseId: exId });
    } else if (isWarning || isInfo) {
      feedbackCard.classList.add(isWarning ? "is-warning" : "is-info");
      feedbackCard.innerHTML = `<strong>💡 Pista diagnóstica:</strong><p>${text.replace(/^Feedback:?/i, "").trim()}</p>`;

      const current = window.SocialR.progress.get(exId);
      window.SocialR.progress.save(exId, {
        status: current.status === "completed" ? "completed" : "in_progress",
        attempts: (current.attempts || 0) + 1,
      });
      window.SocialR.events.emit("answer_incorrect", { exerciseId: exId, message: text });
    } else {
      feedbackCard.classList.add("is-error");
      feedbackCard.innerHTML = `<strong>⚠️ Revisa tu código:</strong><p>${text}</p>`;
      window.SocialR.events.emit("answer_incorrect", { exerciseId: exId, message: text });
    }

    feedbackCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.initWorkspace = initWorkspace;
})();
