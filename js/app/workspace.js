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

    // If adapter is active and already managing feedback, avoid duplicate/unparsed overwrite
    if (window.SocialR && window.SocialR.adapter && typeof window.SocialR.adapter.renderFeedbackCard === "function") {
      return;
    }

    const feedbackCard = exContainer.querySelector(".sr-feedback-card");
    if (!feedbackCard) return;

    const text = gradeEl.textContent || "";
    const isCorrect = gradeEl.classList.contains("alert-success") || text.includes("¡Muy bien!") || text.includes("¡Excelente!") || text.includes("¡Bien!");
    const isWarning = gradeEl.classList.contains("alert-warning");
    const isInfo = gradeEl.classList.contains("alert-info");
    const type = isCorrect ? "success" : (isWarning ? "warning" : (isInfo ? "info" : "error"));
    const title = isCorrect ? "✓ ¡Excelente trabajo!" : (isWarning || isInfo ? "💡 Pista diagnóstica:" : "⚠️ Revisa tu código:");

    const rawContent = text.replace(/^Feedback:?/i, "").trim();
    let formattedBody;
    if (window.SocialR && typeof window.SocialR.renderMarkdown === "function") {
      formattedBody = window.SocialR.renderMarkdown(rawContent);
    } else {
      let s = rawContent
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      s = s.replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>");
      s = s.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");
      s = s.replace(/`([^`]+)`/g, '<code class="sr-inline-code">$1</code>');
      formattedBody = `<p class="sr-feedback-p">${s}</p>`;
    }

    feedbackCard.className = `sr-feedback-card is-visible is-${type}`;
    feedbackCard.innerHTML = `
      <div class="sr-feedback-header">
        <span class="sr-feedback-title">${title}</span>
      </div>
      <div class="sr-feedback-body">${formattedBody}</div>
    `;

    feedbackCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.initWorkspace = initWorkspace;
})();
