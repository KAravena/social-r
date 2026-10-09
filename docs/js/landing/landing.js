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
    const cloud = (window.SocialR && window.SocialR.cloudConfig) || null;
    let storeState = null;
    try {
      if (cloud && cloud.isAuthenticated()) {
        const studentNs = cloud.getProgressNamespace("intro-r");
        const raw = localStorage.getItem(studentNs);
        if (raw) {
          storeState = JSON.parse(raw);
        }
      } else {
        const raw =
          localStorage.getItem("social-r:progress:intro-r") ||
          localStorage.getItem("social-r:progress:v2") ||
          localStorage.getItem("social-r:progress:intro-r:01-primeros-pasos") ||
          localStorage.getItem("social-r:progress");
        if (raw) {
          storeState = JSON.parse(raw);
        }
      }
    } catch (e) {
      console.warn("[Social R] Failed to parse progress store:", e);
    }

    const config = (window.SocialR && window.SocialR.courseConfig) || null;
    const totalPublishedCount = config ? config.publishedExerciseCount : 89;
    let hasProgress = false;
    let targetExId = "intro-r-01-001";
    let completedExCount = 0;
    let activeModuleId = "01-empezar-a-pensar-con-r";
    const completedSet = new Set();

    if (storeState) {
      if (storeState.modules && typeof storeState.modules === "object") {
        for (const [mId, m] of Object.entries(storeState.modules)) {
          if (config && !config.isModulePublished(mId)) {
            continue; // Standby module: preserve progress in state, do not count in public total
          }
          if (Array.isArray(m.completedExercises)) {
            m.completedExercises.forEach((id) => {
              if (!config || config.isExercisePublished(id)) {
                completedSet.add(id);
              }
            });
          }
        }
      } else if (Array.isArray(storeState.completed)) {
        storeState.completed.forEach((id) => {
          if (!config || config.isExercisePublished(id)) {
            completedSet.add(id);
          }
        });
      }

      completedExCount = completedSet.size;

      let hasChallengeProgress = false;
      if (storeState.challenges && typeof storeState.challenges === "object") {
        for (const [mId, ch] of Object.entries(storeState.challenges)) {
          if (ch && (ch.status === "passed" || ch.passedAt || (ch.attempts && ch.attempts > 0))) {
            hasChallengeProgress = true;
            break;
          }
        }
      }
      if (!hasChallengeProgress && storeState.modules && typeof storeState.modules === "object") {
        for (const [mId, m] of Object.entries(storeState.modules)) {
          if (m && (m.challengePassed || m.accredited || (m.challengeAttempts && m.challengeAttempts > 0))) {
            hasChallengeProgress = true;
            break;
          }
        }
      }

      if (completedExCount > 0 || hasChallengeProgress || (storeState.currentExerciseId && storeState.currentExerciseId !== "intro-r-01-001")) {
        hasProgress = true;
        if (config && typeof config.getResumeExerciseId === "function") {
          targetExId = config.getResumeExerciseId(storeState);
        } else if (storeState.currentExerciseId) {
          targetExId = storeState.currentExerciseId;
        }
      }

      // If targetExId is in a standby module, clamp to published range
      if (config && config.isStandbyExercise(targetExId)) {
        targetExId = config.getLastPublishedExerciseId();
      }

      if (storeState.activeModuleId) {
        activeModuleId = storeState.activeModuleId;
        if (config && !config.isModulePublished(activeModuleId)) {
          activeModuleId = (config.publishedModuleSlugs && config.publishedModuleSlugs.length > 0)
            ? config.publishedModuleSlugs[config.publishedModuleSlugs.length - 1]
            : "13-de-la-pregunta-al-analisis";
        }
      } else if (targetExId) {
        const match = targetExId.match(/intro-r-(\d{2})-/);
        if (match) {
          const modSlugs = (config && config.publishedModuleSlugs) ? config.publishedModuleSlugs : [
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
          if (num >= 1 && num <= modSlugs.length) {
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

    // Identity belongs exclusively in topbar / header profile; remove any hero identity pill
    const identityEl = document.getElementById("sr-hero-student-pill");
    if (identityEl) {
      identityEl.remove();
    }

    if (hasProgress) {
      if (heroBtnText) heroBtnText.textContent = "Continuar curso →";
      if (heroProgressLine) {
        heroProgressLine.style.display = "block";
        heroProgressLine.textContent = `${completedExCount}/${totalPublishedCount} ejercicios completados`;
      }
    } else {
      if (heroBtnText) heroBtnText.textContent = "Comenzar curso →";
      if (heroProgressLine) heroProgressLine.style.display = "none";
    }

    // Update Module Badges & Exercise items in Accordion
    const accordionItems = document.querySelectorAll(".sr-accordion-item");
    accordionItems.forEach((item) => {
      const modId = item.getAttribute("data-module-id");
      const isPublished = !config || config.isModulePublished(modId);
      const isModAvailable = config ? config.isModuleAvailable(modId) : isPublished;
      const badge = item.querySelector(".sr-module-badge");
      const modTotal = parseInt(item.getAttribute("data-module-total") || "8", 10);
      const modOrder = parseInt(item.getAttribute("data-module-order") || "1", 10);

      if (!isModAvailable) {
        item.classList.add("sr-accordion-item--standby");
        if (badge) {
          badge.className = "sr-module-badge sr-module-badge--standby";
          badge.textContent = "En preparación";
        }
        const challengeCard = item.querySelector(".sr-challenge-card");
        if (challengeCard) {
          challengeCard.className = "sr-challenge-card is-standby";
          const rightEl = challengeCard.querySelector(".sr-challenge-card__right");
          if (rightEl) {
            rightEl.innerHTML = `<span class="sr-challenge-badge is-standby">En preparación</span>`;
          }
        }
        return;
      }

      const cloud = window.SocialR && window.SocialR.cloudConfig;
      const isAdmin = Boolean(
        (cloud && typeof cloud.isAdmin === "function" && cloud.isAdmin()) ||
        (config && typeof config.isAdmin === "function" && config.isAdmin(storeState))
      );
      const isModUnlocked = (config ? config.isModuleUnlocked(modId, storeState) : (modOrder === 1)) || isAdmin;
      const isChallengePassed = config ? config.isModuleSatisfied(modId, storeState) : false;

      let modCompletedCount = 0;

      // Check exercises inside this module
      const exItems = item.querySelectorAll(".sr-exercise-item");
      let previousCompleted = true;

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
        } else if (!isModUnlocked) {
          exEl.className = "sr-exercise-item is-locked";
          if (iconEl) iconEl.textContent = "";
          if (linkEl) {
            linkEl.setAttribute("tabindex", "-1");
            linkEl.setAttribute("aria-disabled", "true");
          }
          previousCompleted = false;
        } else if (isChallengePassed) {
          exEl.className = "sr-exercise-item is-available";
          if (iconEl) iconEl.textContent = "○";
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
        } else if (isAdmin) {
          // ADMIN FREE NAVIGATION: All exercises in module are available and clickable
          exEl.className = "sr-exercise-item is-available";
          if (iconEl) iconEl.textContent = "○";
          if (linkEl) {
            linkEl.removeAttribute("tabindex");
            linkEl.removeAttribute("aria-disabled");
          }
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

      // Check Challenge Status for this module
      const challengeCard = item.querySelector(".sr-challenge-card");

      if (challengeCard) {
        const challengeId = challengeCard.getAttribute("data-challenge-id") || `intro-r-${String(modOrder).padStart(2, '0')}-challenge`;
        const rightEl = challengeCard.querySelector(".sr-challenge-card__right");
        const descEl = challengeCard.querySelector(".sr-challenge-card__desc");

        if (isChallengePassed) {
          challengeCard.className = "sr-challenge-card is-accredited";
          if (descEl) descEl.textContent = "Módulo acreditado";
          if (rightEl) {
            rightEl.innerHTML = `
              <div class="sr-challenge-accredited-group">
                <span class="sr-challenge-badge is-accredited">✓ Acreditado</span>
                <a href="curso.html#${challengeId}" class="sr-challenge-link-secondary">Ver desafío →</a>
              </div>
            `;
          }
        } else if (!isModUnlocked) {
          challengeCard.className = "sr-challenge-card is-module-locked";
          if (descEl) descEl.textContent = "Demuestra lo que sabes y acredita el módulo.";
          if (rightEl) {
            rightEl.innerHTML = `
              <span class="sr-challenge-badge is-module-locked">Disponible cuando acredites el módulo anterior</span>
            `;
          }
        } else {
          challengeCard.className = "sr-challenge-card is-available";
          if (descEl) descEl.textContent = "Demuestra lo que sabes y acredita el módulo.";
          if (rightEl) {
            rightEl.innerHTML = `
              <a href="curso.html#${challengeId}" class="sr-challenge-btn sr-challenge-btn--available">Comenzar desafío →</a>
            `;
          }
        }
      }

      if (badge) {
        if (isChallengePassed) {
          badge.className = "sr-module-badge is-completed is-accredited";
          badge.innerHTML = `<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/></svg> ${modCompletedCount}/${modTotal} · Acreditado`;
        } else if (!isModUnlocked) {
          badge.className = "sr-module-badge is-locked";
          badge.textContent = "Bloqueado";
        } else if (modCompletedCount >= modTotal) {
          badge.className = "sr-module-badge is-practice-completed";
          badge.textContent = "Práctica completada";
        } else if (modCompletedCount > 0) {
          badge.className = "sr-module-badge is-progress";
          badge.textContent = `${modCompletedCount}/${modTotal}`;
        } else {
          badge.className = "sr-module-badge is-available";
          badge.textContent = "Disponible";
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

  /**
   * Optional authentication prompt for curso.html links when not authenticated and not in guest mode.
   * In Guest Mode or Authenticated Mode: allows direct navigation without blocking.
   */
  function initCourseLinksGate() {
    document.addEventListener("click", (e) => {
      const link = e.target.closest("a[href*='curso.html']");
      if (!link) return;

      const cloud = window.SocialR && window.SocialR.cloudConfig;
      if (!cloud || !cloud.isCloudEnabled()) return;

      // Guest Mode: strictly direct navigation to local course without blocking
      if (typeof cloud.isGuestMode === "function" && cloud.isGuestMode()) {
        return;
      }

      // Authenticated: strictly direct navigation to student session course
      if (cloud.isAuthenticated()) {
        return;
      }

      // Unauthenticated first-time visitor: prompt login modal offering login or guest mode
      e.preventDefault();
      const targetHref = link.getAttribute("href") || "curso.html";
      if (window.SocialR && window.SocialR.loginModal) {
        window.SocialR.loginModal.open({
          dismissible: true,
          targetUrl: targetHref,
          onSuccess: () => {
            syncProgress();
            const config = window.SocialR && window.SocialR.courseConfig;
            const progress = window.SocialR && window.SocialR.progress;
            const isAdmin = Boolean((cloud && typeof cloud.isAdmin === "function" && cloud.isAdmin()) || (config && typeof config.isAdmin === "function" && config.isAdmin()));
            const hasExplicitHash = Boolean(targetHref && /#intro-r-/.test(targetHref));
            if (hasExplicitHash || isAdmin) {
              window.location.href = targetHref;
              return;
            }
            const resumeExId = (progress && typeof progress.getResumeExerciseId === "function")
              ? progress.getResumeExerciseId()
              : (config && typeof config.getResumeExerciseId === "function" ? config.getResumeExerciseId() : null);
            if (resumeExId) {
              window.location.href = `curso.html#${resumeExId}`;
            } else {
              window.location.href = targetHref;
            }
          }
        });
      } else {
        window.location.href = targetHref;
      }
    });
  }

  /**
   * Home Profile Icon controller (supports unauthenticated, guest mode, and authenticated states)
   */
  function updateProfileControl() {
    const container = document.getElementById("sr-home-profile-container");
    if (!container) return;

    const cloud = window.SocialR && window.SocialR.cloudConfig;
    const isAuth = cloud ? cloud.isAuthenticated() : false;
    const isGuest = cloud && typeof cloud.isGuestMode === "function" ? cloud.isGuestMode() : false;

    if (isAuth) {
      const displayName = cloud.getDisplayName() || "Estudiante";
      const firstName = (window.SocialR && typeof window.SocialR.getFirstName === "function")
        ? window.SocialR.getFirstName(displayName, "Estudiante")
        : (cloud && typeof cloud.getFirstName === "function"
          ? cloud.getFirstName(displayName, "Estudiante")
          : displayName.split(" ")[0]);
      const initial = (firstName[0] || "E").toUpperCase();
      const safeName = firstName.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]);
      const safeFullName = displayName.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]);

      container.innerHTML = `
        <div class="sr-home-profile-pill" role="region" aria-label="Sesión de estudiante">
          <div class="sr-home-profile-info" title="Sesión activa como ${safeFullName}">
            <span class="sr-home-profile-avatar" aria-hidden="true">${initial}</span>
            <span class="sr-home-profile-name">${safeName}</span>
          </div>
          <button type="button" class="sr-home-profile-logout" id="sr-home-logout-btn" aria-label="Cerrar sesión" title="Cerrar sesión">Salir</button>
        </div>
      `;

      const logoutBtn = container.querySelector("#sr-home-logout-btn");
      if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
          if (window.SocialR && window.SocialR.loginModal) {
            window.SocialR.loginModal.handleLogout();
          } else if (cloud) {
            cloud.clearSession();
            updateProfileControl();
            syncProgress();
          }
        });
      }
    } else {
      // Guest mode or unauthenticated visitor
      const labelText = isGuest ? "Sin sesión" : "Iniciar sesión";
      const tooltip = isGuest
        ? "Modo invitado — Iniciar sesión con RUT o IPE"
        : "Iniciar sesión con RUT o IPE";

      container.innerHTML = `
        <button type="button" class="sr-home-profile-btn ${isGuest ? "is-guest" : ""}" id="sr-home-profile-btn" aria-label="${tooltip}" title="${tooltip}">
          <svg class="sr-home-profile-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span class="sr-home-profile-label">${labelText}</span>
        </button>
      `;

      const profileBtn = container.querySelector("#sr-home-profile-btn");
      if (profileBtn) {
        profileBtn.addEventListener("click", () => {
          if (window.SocialR && window.SocialR.loginModal) {
            window.SocialR.loginModal.open({
              dismissible: true,
              onSuccess: () => {
                updateProfileControl();
                syncProgress();
              }
            });
          }
        });
      }
    }
  }

  function initProfileControl() {
    updateProfileControl();

    // Listen for auth state changes or guest mode changes via window CustomEvents or EventBus
    if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.on === "function") {
      window.SocialR.events.on("auth_state_changed", () => {
        updateProfileControl();
        syncProgress();
      });
      window.SocialR.events.on("progress_reloaded", () => {
        updateProfileControl();
        syncProgress();
      });
      window.SocialR.events.on("guest_mode_changed", () => {
        updateProfileControl();
        syncProgress();
      });
    }

    window.addEventListener("social-r:auth_state_changed", () => {
      updateProfileControl();
      syncProgress();
    });
    window.addEventListener("social-r:guest_mode_changed", () => {
      updateProfileControl();
      syncProgress();
    });

    window.addEventListener("storage", (e) => {
      if (e.key === "social-r:auth:session" || e.key === "social-r:auth:guest-mode") {
        updateProfileControl();
        syncProgress();
      }
    });
  }

  function checkFirstVisitModal() {
    const cloud = window.SocialR && window.SocialR.cloudConfig;
    if (cloud && cloud.isCloudEnabled() && !cloud.isAuthenticated() && !cloud.isGuestMode()) {
      if (window.SocialR && window.SocialR.loginModal) {
        window.SocialR.loginModal.open({
          dismissible: true
        });
      }
    }
  }

  // Single clean initialization
  function boot() {
    initHeroVisuals();
    initAccordion();
    syncProgress();
    initSmoothScroll();
    initCourseLinksGate();
    initProfileControl();

    // Rebind session on startup if authenticated student/admin is active
    const cloud = window.SocialR && window.SocialR.cloudConfig;
    if (cloud && cloud.isAuthenticated() && window.SocialR && window.SocialR.progress && typeof window.SocialR.progress.rebindSession === "function") {
      window.SocialR.progress.rebindSession(cloud.getStudentId()).then(() => {
        syncProgress();
        updateProfileControl();
      }).catch((e) => {
        console.warn("[Social R] Error rebinding session on landing:", e);
      });
    }

    setTimeout(() => {
      checkFirstVisitModal();
    }, 350);
  }

  // Expose for external coordination (e.g., course reset, login modal)
  window.SocialR = window.SocialR || {};
  window.SocialR.syncProgress = syncProgress;
  window.SocialR.updateProfileControl = updateProfileControl;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

