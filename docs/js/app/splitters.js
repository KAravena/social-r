/**
 * Social R Platform - Splitters
 * Fluid horizontal and vertical workspace resizing using Pointer Events and CSS custom properties.
 */
(function () {
  "use strict";

  function initSplitters() {
    const workspace = document.querySelector(".sr-workspace");
    const codingPanel = document.querySelector(".sr-coding-panel");
    const splitterH = document.querySelector(".sr-splitter-h");
    const splitterV = document.querySelector(".sr-splitter-v");
    const dragOverlay = document.querySelector(".sr-drag-overlay");

    if (!workspace || !splitterH) return;

    // Load saved dimensions if any
    const savedLeftWidth = localStorage.getItem("social-r:left-width");
    const savedEditorHeight = localStorage.getItem("social-r:editor-height");
    if (savedLeftWidth) document.documentElement.style.setProperty("--sr-left-width", savedLeftWidth);
    if (savedEditorHeight) document.documentElement.style.setProperty("--sr-editor-height", savedEditorHeight);

    // --- Horizontal Splitter (Left vs Right) ---
    splitterH.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      splitterH.classList.add("is-dragging");
      if (dragOverlay) dragOverlay.className = "sr-drag-overlay is-active-h";

      const onPointerMove = (moveEvent) => {
        const workspaceRect = workspace.getBoundingClientRect();
        let newLeftWidthPx = moveEvent.clientX - workspaceRect.left;
        const minPx = 300;
        const maxPx = workspaceRect.width - 360;

        if (newLeftWidthPx < minPx) newLeftWidthPx = minPx;
        if (newLeftWidthPx > maxPx) newLeftWidthPx = maxPx;

        const leftPct = (newLeftWidthPx / workspaceRect.width) * 100;
        const value = `${leftPct.toFixed(1)}%`;
        document.documentElement.style.setProperty("--sr-left-width", value);
        localStorage.setItem("social-r:left-width", value);
      };

      const onPointerUp = () => {
        splitterH.classList.remove("is-dragging");
        if (dragOverlay) dragOverlay.className = "sr-drag-overlay";
        window.removeEventListener("pointermove", onPointerMove);
        window.removeEventListener("pointerup", onPointerUp);
      };

      window.addEventListener("pointermove", onPointerMove);
      window.addEventListener("pointerup", onPointerUp);
    });

    // --- Vertical Splitter (Editor vs Console) ---
    if (splitterV && codingPanel) {
      splitterV.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        splitterV.classList.add("is-dragging");
        if (dragOverlay) dragOverlay.className = "sr-drag-overlay is-active-v";

        const onPointerMove = (moveEvent) => {
          const panelRect = codingPanel.getBoundingClientRect();
          let newEditorHeightPx = moveEvent.clientY - panelRect.top;
          const minHeight = 160;
          const maxHeight = panelRect.height - 120;

          if (newEditorHeightPx < minHeight) newEditorHeightPx = minHeight;
          if (newEditorHeightPx > maxHeight) newEditorHeightPx = maxHeight;

          const topPct = (newEditorHeightPx / panelRect.height) * 100;
          const value = `${topPct.toFixed(1)}%`;
          document.documentElement.style.setProperty("--sr-editor-height", value);
          localStorage.setItem("social-r:editor-height", value);
        };

        const onPointerUp = () => {
          splitterV.classList.remove("is-dragging");
          if (dragOverlay) dragOverlay.className = "sr-drag-overlay";
          window.removeEventListener("pointermove", onPointerMove);
          window.removeEventListener("pointerup", onPointerUp);
        };

        window.addEventListener("pointermove", onPointerMove);
        window.addEventListener("pointerup", onPointerUp);
      });
    }
  }

  // Auto-boot splitters on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSplitters);
  } else {
    initSplitters();
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.initSplitters = initSplitters;
})();
