/**
 * Social R Platform - Modular Navigation Manager v3.0
 * Unified CourseModel architecture, independent module unlocking,
 * single-module horizontal stepper, 3-tier TopBar, and robust Course Outline.
 */
(function () {
  "use strict";

  class NavigationManager {
    constructor() {
      this.exercises = [];
      this.modules = {};
      this.courseModel = { modules: [] };
      this.currentIndex = 0;
      this.drawerMounted = false;
      this.drawerDirty = true;
      this.drawerItemMap = new Map();
      this.drawerModuleMap = new Map();
    }

    init() {
      // 1. Load module metadata from embedded JSON script
      const metaScript = document.getElementById("sr-modules-metadata");
      if (metaScript && metaScript.textContent) {
        try {
          this.modules = JSON.parse(metaScript.textContent);
        } catch (e) {
          console.warn("[Navigation] Failed to parse sr-modules-metadata:", e);
        }
      }

      // 2. Index all exercise DOM elements and normalize CourseModel
      const nodes = Array.from(document.querySelectorAll(".social-r-exercise"));
      this.exercises = nodes.map((node, index) => {
        const modId = node.getAttribute("data-module-id") || "01-empezar-a-pensar-con-r";
        const modMeta = this.modules[modId] || {};

        return {
          index,
          id: node.getAttribute("data-exercise-id"),
          order: parseInt(node.getAttribute("data-exercise-order") || "0", 10),
          globalIndex: index,
          title: node.getAttribute("data-exercise-title") || `Ejercicio ${index + 1}`,
          moduleId: modId,
          moduleTitle: node.getAttribute("data-module-title") || modMeta.title || "Módulo 1",
          moduleShortTitle: node.getAttribute("data-module-short-title") || modMeta.short_title || "Módulo 1",
          moduleOrder: parseInt(node.getAttribute("data-module-order") || modMeta.order || "1", 10),
          moduleTotal: parseInt(node.getAttribute("data-module-total") || "8", 10),
          node,
        };
      });

      this.buildCourseModel();
      this.mountDrawer();
      this.renderDrawer();
      this.drawerDirty = false;

      if (this.exercises.length === 0) return;

      // 3. Determine initial exercise from URL hash or ProgressStore v2
      let initialIndex = 0;
      const store = (window.SocialR && window.SocialR.progress) ? window.SocialR.progress : null;

      const hash = window.location.hash.replace("#", "");
      if (hash) {
        const found = this.exercises.findIndex((ex) => ex.id === hash);
        if (found !== -1 && this.isUnlocked(found)) {
          initialIndex = found;
        }
      } else if (store && store.state) {
        const activeModId = (store.state.activeModuleId === "primeros-pasos" ? "01-empezar-a-pensar-con-r" : (store.state.activeModuleId || "01-empezar-a-pensar-con-r"));
        const savedExId = (store.state.modules && store.state.modules[activeModId])
          ? store.state.modules[activeModId].currentExerciseId
          : store.state.currentExerciseId;

        if (savedExId) {
          const found = this.exercises.findIndex((ex) => ex.id === savedExId);
          if (found !== -1 && this.isUnlocked(found)) {
            initialIndex = found;
          }
        }
      }

      this.setActiveIndex(initialIndex);
      this.bindEvents();
      this.restoreEditorStates();
    }

    buildCourseModel() {
      const modMap = new Map();

      // Collect modules from metadata first
      Object.keys(this.modules).forEach((modId) => {
        const meta = this.modules[modId];
        modMap.set(modId, {
          id: modId,
          title: meta.title || `Módulo ${meta.order || ""}`,
          shortTitle: meta.short_title || meta.title || `Módulo ${meta.order || ""}`,
          order: meta.order || 1,
          learningOutcomes: meta.learning_outcomes || [],
          exercises: [],
        });
      });

      // Populate exercises into each module group
      this.exercises.forEach((ex) => {
        if (!modMap.has(ex.moduleId)) {
          modMap.set(ex.moduleId, {
            id: ex.moduleId,
            title: ex.moduleTitle,
            shortTitle: ex.moduleShortTitle,
            order: ex.moduleOrder,
            learningOutcomes: [],
            exercises: [],
          });
        }
        modMap.get(ex.moduleId).exercises.push(ex);
      });

      this.courseModel.modules = Array.from(modMap.values()).sort((a, b) => a.order - b.order);
    }

    restoreEditorStates() {
      if (!window.SocialR || !window.SocialR.progress || !window.SocialR.adapter) return;
      this.exercises.forEach((ex) => {
        if (!ex.id) return;
        const savedCode = window.SocialR.progress.getEditorCode(ex.id);
        if (savedCode) {
          setTimeout(() => {
            const view = window.SocialR.adapter.getCMView(ex.id);
            if (view && view.state && view.state.doc) {
              view.dispatch({
                changes: { from: 0, to: view.state.doc.length, insert: savedCode }
              });
            }
          }, 300);
        }
      });
    }

    /**
     * Autonomous Module Unlocking Rule:
     * 1. The first exercise of ANY module (order === 0) is ALWAYS unlocked from the start.
     * 2. Exercise [n] (where order > 0) is unlocked IF AND ONLY IF exercise [n - 1] in the SAME module is completed.
     * 3. No cross-module locking or dependency.
     */
    isUnlocked(index) {
      if (window.SocialR && window.SocialR.devMode) return true;
      if (index < 0 || index >= this.exercises.length) return false;

      const currentEx = this.exercises[index];
      if (!currentEx) return false;

      // First exercise in this module is ALWAYS unlocked
      if (currentEx.order === 0) {
        return true;
      }

      // Check immediately previous exercise in the SAME module
      const prevEx = this.exercises[index - 1];
      if (!prevEx || prevEx.moduleId !== currentEx.moduleId) {
        return true;
      }

      if (window.SocialR && window.SocialR.progress && typeof window.SocialR.progress.isCompleted === "function") {
        return window.SocialR.progress.isCompleted(prevEx.id);
      }
      return false;
    }

    getCurrentExercise() {
      return this.exercises[this.currentIndex];
    }

    getCurrentModule() {
      const current = this.getCurrentExercise();
      if (!current) return this.courseModel.modules[0] || null;
      return this.courseModel.modules.find((m) => m.id === current.moduleId) || {
        id: current.moduleId,
        title: current.moduleTitle,
        shortTitle: current.moduleShortTitle,
        order: current.moduleOrder,
        exercises: this.exercises.filter((e) => e.moduleId === current.moduleId),
      };
    }

    getExerciseInfo(exerciseId) {
      const idx = this.exercises.findIndex((ex) => ex.id === exerciseId);
      if (idx === -1) {
        const cur = this.getCurrentExercise();
        return {
          index: this.currentIndex,
          order: cur ? cur.order : 0,
          title: cur ? cur.title : "",
          moduleId: cur ? cur.moduleId : "01-empezar-a-pensar-con-r",
          moduleTitle: cur ? cur.moduleTitle : "",
          moduleShortTitle: cur ? cur.moduleShortTitle : "",
          moduleOrder: cur ? cur.moduleOrder : 1,
          moduleTotal: cur ? cur.moduleTotal : 8,
          total: this.exercises.length,
          isLastInModule: cur ? cur.order >= cur.moduleTotal - 1 : false,
          isLastInCourse: this.currentIndex >= this.exercises.length - 1,
        };
      }

      const ex = this.exercises[idx];
      const isLastInModule = ex.order >= ex.moduleTotal - 1;
      const nextEx = !isLastInModule ? this.exercises[idx + 1] : null;

      return {
        index: idx,
        order: ex.order,
        globalIndex: idx,
        title: ex.title,
        moduleId: ex.moduleId,
        moduleTitle: ex.moduleTitle,
        moduleShortTitle: ex.moduleShortTitle,
        moduleOrder: ex.moduleOrder,
        moduleTotal: ex.moduleTotal,
        total: this.exercises.length,
        nextTitle: nextEx ? nextEx.title : "",
        isLastInModule,
        isLastInCourse: idx >= this.exercises.length - 1,
      };
    }

    setActiveIndex(index) {
      if (index < 0 || index >= this.exercises.length) return;
      if (!this.isUnlocked(index) && !(window.SocialR && window.SocialR.devMode)) {
        console.warn(`[Navigation] Exercise ${index} is locked.`);
        return;
      }

      this.currentIndex = index;
      const current = this.exercises[this.currentIndex];

      // Save current exercise and module to ProgressStore v2
      if (window.SocialR && window.SocialR.progress && current && current.id) {
        window.SocialR.progress.setCurrentExercise(current.id, current.moduleId);
      }

      // Update DOM visibility
      this.exercises.forEach((ex, idx) => {
        if (idx === index) {
          ex.node.classList.add("is-active-exercise");
          ex.node.classList.remove("d-none");
          ex.node.style.display = "flex";
        } else {
          ex.node.classList.remove("is-active-exercise");
          ex.node.classList.add("d-none");
          ex.node.style.display = "none";
          const fb = ex.node.querySelector(".sr-feedback-card");
          if (fb) {
            fb.className = "sr-feedback-card";
            fb.innerHTML = "";
          }
          if (window.SocialR && window.SocialR.adapter && window.SocialR.adapter.resetHints) {
            window.SocialR.adapter.resetHints(ex.id);
          }
        }
      });

      // Update URL hash
      try {
        window.history.replaceState(null, "", `#${current.id}`);
      } catch (e) {}

      // Refresh TopBar, BottomBar, and Course Outline Drawer
      this.refreshUI();

      // Emit event
      if (window.SocialR && window.SocialR.events) {
        window.SocialR.events.emit("exercise_opened", {
          exerciseId: current.id,
          index: this.currentIndex,
          order: current.order,
          moduleId: current.moduleId,
          total: this.exercises.length,
        });
      }
    }

    next() {
      const current = this.getCurrentExercise();
      if (!current) return;

      // If last in module and completed, show celebration
      if (current.order >= current.moduleTotal - 1) {
        if (window.SocialR && window.SocialR.progress && window.SocialR.progress.isCompleted(current.id)) {
          this.showCelebration(current.moduleId);
          return;
        }
      }

      if (this.currentIndex < this.exercises.length - 1) {
        const nextEx = this.exercises[this.currentIndex + 1];
        if (nextEx && (this.isUnlocked(this.currentIndex + 1) || (window.SocialR && window.SocialR.devMode))) {
          this.setActiveIndex(this.currentIndex + 1);
        }
      }
    }

    previous() {
      const current = this.getCurrentExercise();
      // Rule 29: within a module, Previous is disabled on the first exercise (order === 0)
      if (current && current.order > 0 && this.currentIndex > 0) {
        this.setActiveIndex(this.currentIndex - 1);
      }
    }

    showCelebration(moduleId) {
      const backdrop = document.getElementById("sr-celebration-backdrop");
      if (!backdrop) return;

      const modMeta = this.modules[moduleId] || {};
      const currentEx = this.getCurrentExercise();
      const modTitle = modMeta.title || (currentEx ? currentEx.moduleTitle : `Módulo ${moduleId}`);
      const modTotal = currentEx ? currentEx.moduleTotal : 8;
      const modOrder = modMeta.order || (currentEx ? currentEx.moduleOrder : 1);

      // Populate Title and Subtitle
      const titleEl = document.getElementById("sr-cel-title");
      if (titleEl) titleEl.textContent = modTitle.includes(":") ? modTitle.split(":")[1].trim() : modTitle;

      const subtitleEl = document.getElementById("sr-cel-subtitle");
      if (subtitleEl) subtitleEl.textContent = `Has terminado los ${modTotal} ejercicios del Módulo ${modOrder}.`;

      // Populate Outcomes
      const outcomesList = document.getElementById("sr-cel-outcomes-list");
      if (outcomesList) {
        outcomesList.innerHTML = "";
        const outcomes = modMeta.learning_outcomes || [
          "Ejecutar instrucciones en R y leer la consola",
          "Guardar información y crear objetos con <-",
          "Reutilizar objetos en nuevos cálculos",
          "Reconocer y operar con tipos de datos",
        ];
        outcomes.forEach((out) => {
          const li = document.createElement("li");
          li.className = "sr-outcome-item";
          const formattedOut = (window.SocialR && typeof window.SocialR.renderInlineMarkdown === "function")
            ? window.SocialR.renderInlineMarkdown(out)
            : out;
          li.innerHTML = `
            <svg class="sr-outcome-check" aria-hidden="true" focusable="false" role="img" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg>
            <span>${formattedOut}</span>
          `;
          outcomesList.appendChild(li);
        });
      }

      // Next step section
      const nextSection = document.getElementById("sr-cel-next-section");
      const nextTitleEl = document.getElementById("sr-cel-next-title");
      const continueBtn = document.getElementById("sr-cel-continue-btn");
      const btnText = document.getElementById("sr-cel-btn-text");

      // Find next module
      const allModIds = Object.keys(this.modules).sort((a, b) => (this.modules[a].order || 0) - (this.modules[b].order || 0));
      const curModIdx = allModIds.indexOf(moduleId);
      const nextModId = curModIdx !== -1 && curModIdx < allModIds.length - 1 ? allModIds[curModIdx + 1] : null;

      if (nextModId && this.modules[nextModId]) {
        const nextMeta = this.modules[nextModId];
        if (nextTitleEl) nextTitleEl.textContent = `Módulo ${nextMeta.order} · ${nextMeta.title.replace(/^Módulo \d+:\s*/, "")}`;

        // Check if next module already has progress
        const store = window.SocialR ? window.SocialR.progress : null;
        const nextModState = store ? store.getModuleState(nextModId) : null;
        const hasStarted = nextModState && nextModState.completedExercises.length > 0;

        if (btnText) {
          btnText.textContent = hasStarted ? `Continuar en Módulo ${nextMeta.order}` : `Comenzar Módulo ${nextMeta.order}`;
        }

        if (continueBtn) {
          continueBtn.onclick = () => {
            this.hideCelebration();
            // Find target exercise in next module (saved or first)
            const targetExId = (nextModState && nextModState.currentExerciseId) ? nextModState.currentExerciseId : null;
            let targetIdx = targetExId ? this.exercises.findIndex((e) => e.id === targetExId) : -1;
            if (targetIdx === -1) {
              targetIdx = this.exercises.findIndex((e) => e.moduleId === nextModId);
            }
            if (targetIdx !== -1) {
              this.setActiveIndex(targetIdx);
            }
          };
        }
      } else {
        // Course Completed!
        if (nextTitleEl) nextTitleEl.textContent = "🎓 ¡Has completado todos los módulos del curso!";
        if (btnText) btnText.textContent = "Revisar esquema del curso";
        if (continueBtn) {
          continueBtn.onclick = () => {
            this.hideCelebration();
            this.openDrawer();
          };
        }
      }

      backdrop.style.display = "flex";
      backdrop.classList.add("is-open");
      backdrop.setAttribute("aria-hidden", "false");
    }

    hideCelebration() {
      const backdrop = document.getElementById("sr-celebration-backdrop");
      if (backdrop) {
        backdrop.classList.remove("is-open");
        backdrop.style.display = "none";
        backdrop.setAttribute("aria-hidden", "true");
      }
    }

    openDrawer() {
      if (this.drawerDirty) {
        this.renderDrawer();
        this.drawerDirty = false;
      }
      const backdrop = document.getElementById("sr-drawer-backdrop");
      if (backdrop) {
        backdrop.setAttribute("aria-hidden", "false");
        backdrop.classList.add("is-open");
        const closeBtn = document.getElementById("sr-drawer-close");
        if (closeBtn) {
          setTimeout(() => {
            try {
              closeBtn.focus({ preventScroll: true });
            } catch (e) {
              closeBtn.focus();
            }
          }, 0);
        }
      }
    }

    closeDrawer() {
      const backdrop = document.getElementById("sr-drawer-backdrop");
      if (backdrop) {
        backdrop.classList.remove("is-open");
        backdrop.setAttribute("aria-hidden", "true");
        const trigger = document.getElementById("sr-outline-trigger");
        if (trigger) {
          try {
            trigger.focus({ preventScroll: true });
          } catch (e) {
            trigger.focus();
          }
        }
      }
    }

    refreshUI() {
      const current = this.getCurrentExercise();
      if (!current) return;
      const currentMod = this.getCurrentModule();

      // 0. Update Navigation Buttons
      const prevBtn = document.getElementById("sr-btn-prev");
      const nextBtn = document.getElementById("sr-btn-next");

      if (prevBtn) {
        prevBtn.disabled = current.order === 0;
      }

      if (nextBtn) {
        if (current.order < current.moduleTotal - 1) {
          const nextUnlocked = this.isUnlocked(this.currentIndex + 1) || (window.SocialR && window.SocialR.devMode);
          nextBtn.disabled = !nextUnlocked;
        } else {
          // Last in module: enabled if completed (to open celebration)
          const isCompleted = window.SocialR && window.SocialR.progress && window.SocialR.progress.isCompleted(current.id);
          nextBtn.disabled = !isCompleted && !(window.SocialR && window.SocialR.devMode);
        }
      }

      // 1. Update 3-Tier Central TopBar Control
      const modPill = document.getElementById("sr-topbar-mod-pill");
      if (modPill) {
        modPill.textContent = `Módulo ${current.moduleOrder}`;
      }

      const counterSpan = document.getElementById("sr-topbar-counter");
      if (counterSpan) {
        counterSpan.textContent = `${current.order + 1}/${current.moduleTotal} ·`;
      }

      const titleSpan = document.getElementById("sr-topbar-title");
      if (titleSpan) {
        titleSpan.textContent = current.title;
      }

      // Fallback for combined single span if present
      const combinedTitle = document.getElementById("sr-topbar-exercise-title");
      if (combinedTitle) {
        combinedTitle.textContent = `${current.order + 1}/${current.moduleTotal} · ${current.title}`;
      }

      const breadcrumbMod = document.querySelector(".sr-breadcrumb-module");
      if (breadcrumbMod && current.moduleTitle) {
        breadcrumbMod.textContent = current.moduleTitle;
      }

      // 2. Render Single-Module Horizontal BottomBar Stepper
      this.renderBottomBar(current, currentMod);

      // 3. Render Course Outline Drawer
      this.renderDrawer();
      this.drawerDirty = false;
    }

    renderBottomBar(current, currentMod) {
      const store = window.SocialR ? window.SocialR.progress : null;

      // BottomBar Counter (Left: compact single-line)
      const counterEl = document.getElementById("sr-bottombar-counter");
      if (counterEl) {
        const modName = current.moduleTitle.includes(":") ? current.moduleTitle.split(":")[0] : `Módulo ${current.moduleOrder}`;
        counterEl.textContent = `${modName} · ${current.order + 1} de ${current.moduleTotal}`;
      }

      // Horizontal Connected Circles Track for Current Module
      const trackContainer = document.getElementById("sr-bottom-module-track") || document.getElementById("sr-stepper");
      if (trackContainer && currentMod && currentMod.exercises) {
        trackContainer.innerHTML = "";

        currentMod.exercises.forEach((exItem, itemIdx) => {
          const isCompleted = store ? store.isCompleted(exItem.id) : false;
          const isCurrent = exItem.globalIndex === this.currentIndex;
          const isLocked = !this.isUnlocked(exItem.globalIndex) && !(window.SocialR && window.SocialR.devMode);

          const node = document.createElement("button");
          node.type = "button";
          node.className = `sr-bottom-module-step ${isCurrent ? "is-active" : ""} ${isCompleted ? "is-completed" : ""} ${isLocked ? "is-locked" : "is-available"}`;
          
          const statusText = isCompleted ? "completado" : isCurrent ? "actual" : isLocked ? "bloqueado" : "pendiente";
          node.setAttribute("aria-label", `Ejercicio ${exItem.order + 1}: ${exItem.title} (${statusText})`);
          if (isCurrent) node.setAttribute("aria-current", "step");
          
          if (isCompleted) {
            node.textContent = "✓";
          } else if (isCurrent) {
            node.textContent = (exItem.order + 1).toString();
          } else {
            node.textContent = "";
          }

          node.title = `Ejercicio ${exItem.order + 1} de ${currentMod.exercises.length}: ${exItem.title} (${statusText})`;
          node.disabled = isLocked;

          if (!isLocked) {
            node.addEventListener("click", () => this.setActiveIndex(exItem.globalIndex));
          }
          trackContainer.appendChild(node);

          if (itemIdx < currentMod.exercises.length - 1) {
            const nextEx = currentMod.exercises[itemIdx + 1];
            const nextCompleted = store ? store.isCompleted(nextEx.id) : false;
            const line = document.createElement("span");
            let connState = "";
            if (isCompleted && nextCompleted) {
              connState = "is-completed";
            } else if (isCompleted) {
              connState = "is-active-edge";
            }
            line.className = `sr-bottom-module-connector ${connState}`;
            trackContainer.appendChild(line);
          }
        });
      }

      // Percentage text (Right: subtle global progress)
      const pctEl = document.getElementById("sr-progress-pct");
      if (pctEl && store) {
        const courseProgress = store.getCourseProgress(this.exercises.length);
        pctEl.textContent = `${courseProgress.percentage}% del curso`;
      }
    }

    mountDrawer() {
      const drawerList = document.getElementById("sr-drawer-list");
      if (!drawerList) return;

      drawerList.innerHTML = "";
      this.drawerItemMap.clear();
      this.drawerModuleMap.clear();

      if (this.courseModel.modules.length === 0) {
        this.buildCourseModel();
      }

      const frag = document.createDocumentFragment();

      this.courseModel.modules.forEach((modGroup) => {
        // Module Section Header
        const modHeader = document.createElement("div");
        modHeader.className = "sr-drawer-module-header";
        modHeader.setAttribute("data-module-id", modGroup.id);

        const titleSpan = document.createElement("span");
        titleSpan.className = "sr-drawer-module-title";
        titleSpan.textContent = modGroup.title;

        const summarySpan = document.createElement("span");
        summarySpan.className = "sr-drawer-module-summary";
        summarySpan.textContent = `0/${modGroup.exercises.length}`;

        modHeader.appendChild(titleSpan);
        modHeader.appendChild(summarySpan);
        frag.appendChild(modHeader);

        this.drawerModuleMap.set(modGroup.id, {
          header: modHeader,
          summary: summarySpan,
          total: modGroup.exercises.length,
        });

        // Exercises List
        modGroup.exercises.forEach((ex) => {
          const item = document.createElement("div");
          item.className = "sr-drawer-item is-available";
          item.setAttribute("role", "button");
          item.setAttribute("tabindex", "0");
          item.setAttribute("data-global-index", String(ex.globalIndex));
          item.setAttribute("data-exercise-id", ex.id);

          const titleEl = document.createElement("span");
          titleEl.className = "sr-drawer-item-title";
          titleEl.textContent = `${ex.order + 1}. ${ex.title}`;

          const badgeEl = document.createElement("span");
          badgeEl.className = "sr-drawer-badge is-available";
          badgeEl.textContent = "○";

          item.appendChild(titleEl);
          item.appendChild(badgeEl);
          frag.appendChild(item);

          const prevExId = (ex.order > 0 && modGroup.exercises[ex.order - 1]) ? modGroup.exercises[ex.order - 1].id : null;

          this.drawerItemMap.set(ex.globalIndex, {
            item,
            badge: badgeEl,
            title: ex.title,
            id: ex.id,
            order: ex.order,
            prevExId,
          });
        });
      });

      drawerList.appendChild(frag);

      // Single Delegated Click Listener (Zero duplicate event listeners)
      drawerList.addEventListener("click", (e) => {
        const item = e.target.closest(".sr-drawer-item");
        if (!item || item.classList.contains("is-locked")) return;
        const gIdx = parseInt(item.getAttribute("data-global-index"), 10);
        if (!isNaN(gIdx)) {
          this.setActiveIndex(gIdx);
          this.closeDrawer();
        }
      });

      // Keyboard accessibility (Enter / Space)
      drawerList.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          const item = e.target.closest(".sr-drawer-item");
          if (!item || item.classList.contains("is-locked")) return;
          e.preventDefault();
          const gIdx = parseInt(item.getAttribute("data-global-index"), 10);
          if (!isNaN(gIdx)) {
            this.setActiveIndex(gIdx);
            this.closeDrawer();
          }
        }
      });

      this.drawerMounted = true;
    }

    renderDrawer() {
      const drawerList = document.getElementById("sr-drawer-list");
      if (!drawerList) return;

      if (!this.drawerMounted) {
        this.mountDrawer();
      }

      const store = window.SocialR ? window.SocialR.progress : null;
      const current = this.getCurrentExercise();

      // Collect completed exercise IDs into a Set in one pass (O(1) lookups)
      const completedSet = new Set();
      if (store && store.state && store.state.modules) {
        for (const m of Object.values(store.state.modules)) {
          if (Array.isArray(m.completedExercises)) {
            for (const id of m.completedExercises) completedSet.add(id);
          }
        }
      }

      // 1. Update Module Headers
      this.courseModel.modules.forEach((modGroup) => {
        const modEntry = this.drawerModuleMap.get(modGroup.id);
        if (!modEntry) return;

        let completedCount = 0;
        for (const ex of modGroup.exercises) {
          if (completedSet.has(ex.id)) completedCount++;
        }
        const isModuleCompleted = completedCount === modGroup.exercises.length && modGroup.exercises.length > 0;
        const isCurrentModule = current && modGroup.id === current.moduleId;

        modEntry.header.classList.toggle("is-current-module", Boolean(isCurrentModule));

        const summaryText = `${completedCount}/${modGroup.exercises.length} ${isModuleCompleted ? "✓" : ""}`;
        if (modEntry.summary.textContent !== summaryText) {
          modEntry.summary.textContent = summaryText;
        }
        modEntry.summary.classList.toggle("is-done", Boolean(isModuleCompleted));
      });

      // 2. Update Exercise Items
      const isDevMode = Boolean(window.SocialR && window.SocialR.devMode);

      this.drawerItemMap.forEach((entry, globalIdx) => {
        const isCompleted = completedSet.has(entry.id);
        const isCurrent = globalIdx === this.currentIndex;
        const isUnlocked = entry.order === 0 || (entry.prevExId && completedSet.has(entry.prevExId)) || isDevMode;
        const isLocked = !isUnlocked;

        const itemClass = `sr-drawer-item ${isCurrent ? "is-active" : ""} ${isCompleted ? "is-completed" : ""} ${isLocked ? "is-locked" : "is-available"}`;
        if (entry.item.className !== itemClass) {
          entry.item.className = itemClass;
        }

        const tabIndex = isLocked ? "-1" : "0";
        if (entry.item.getAttribute("tabindex") !== tabIndex) {
          entry.item.setAttribute("tabindex", tabIndex);
        }

        const ariaLabel = `${entry.title} - ${isCompleted ? "Completado" : isLocked ? "Bloqueado" : "Disponible"}`;
        if (entry.item.getAttribute("aria-label") !== ariaLabel) {
          entry.item.setAttribute("aria-label", ariaLabel);
        }

        const badgeSymbol = isCompleted ? "✓" : (isCurrent ? "●" : (isLocked ? "🔒" : "○"));
        const badgeClass = `sr-drawer-badge ${isCompleted ? "is-completed" : (isCurrent ? "is-current" : (isLocked ? "is-locked" : "is-available"))}`;

        if (entry.badge.className !== badgeClass) {
          entry.badge.className = badgeClass;
        }
        if (entry.badge.textContent !== badgeSymbol) {
          entry.badge.textContent = badgeSymbol;
        }
      });
    }

    bindEvents() {
      const prevBtn = document.getElementById("sr-btn-prev");
      const nextBtn = document.getElementById("sr-btn-next");
      const trigger = document.getElementById("sr-outline-trigger");
      const closeBtn = document.getElementById("sr-drawer-close");
      const backdrop = document.getElementById("sr-drawer-backdrop");

      if (prevBtn) prevBtn.addEventListener("click", () => this.previous());
      if (nextBtn) nextBtn.addEventListener("click", () => this.next());

      if (trigger) {
        const prewarm = () => {
          if (this.drawerDirty) {
            this.renderDrawer();
            this.drawerDirty = false;
          }
          const drawer = document.querySelector(".sr-drawer");
          if (drawer) drawer.style.willChange = "transform";
        };
        trigger.addEventListener("pointerenter", prewarm, { passive: true });
        trigger.addEventListener("pointerdown", prewarm, { passive: true });
        trigger.addEventListener("click", () => this.openDrawer());
      }

      if (closeBtn) {
        closeBtn.addEventListener("click", () => this.closeDrawer());
      }

      if (backdrop) {
        backdrop.addEventListener("click", (e) => {
          if (e.target === backdrop) this.closeDrawer();
        });
        const drawer = backdrop.querySelector(".sr-drawer");
        if (drawer) {
          drawer.addEventListener("transitionend", (e) => {
            if (e.propertyName === "transform" && !backdrop.classList.contains("is-open")) {
              drawer.style.willChange = "auto";
            }
          });
        }
      }

      // Close drawer on Escape key
      window.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
          const bd = document.getElementById("sr-drawer-backdrop");
          if (bd && bd.classList.contains("is-open")) {
            this.closeDrawer();
          }
        }
      });

      // Celebration Close Button
      const celClose = document.getElementById("sr-celebration-close");
      if (celClose) celClose.addEventListener("click", () => this.hideCelebration());

      // Event listeners for exercise completion & module completion
      if (window.SocialR && window.SocialR.events) {
        window.SocialR.events.on("exercise_completed", (data) => {
          if (data && data.exerciseId && window.SocialR.progress) {
            const exInfo = this.getExerciseInfo(data.exerciseId);
            window.SocialR.progress.markCompleted(data.exerciseId, exInfo.moduleId);

            // Check if all exercises in module are completed
            const modProgress = window.SocialR.progress.getModuleProgress(exInfo.moduleId, exInfo.moduleTotal);
            if (modProgress.isCompleted) {
              window.SocialR.progress.setModuleCompleted(exInfo.moduleId, true);
              window.SocialR.events.emit("module_completed", {
                moduleId: exInfo.moduleId,
                moduleTitle: exInfo.moduleTitle,
                moduleOrder: exInfo.moduleOrder,
              });
            }
          }
          this.drawerDirty = true;
          this.refreshUI();
        });

        window.SocialR.events.on("module_completed", (data) => {
          if (data && data.moduleId) {
            this.showCelebration(data.moduleId);
          }
        });
      }
    }
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.navigation = new NavigationManager();
})();
