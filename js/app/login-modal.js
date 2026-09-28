/**
 * Social R - RUT Login Modal & User Identity Controller
 * Simple, passwordless student identification via Chilean RUT.
 */
(function () {
  "use strict";

  class LoginModal {
    constructor() {
      this.backdropEl = null;
      this.cardEl = null;
      this.options = {
        dismissible: true,
        onSuccess: null,
      };
      this.pendingStudentData = null;

      this._initDom();
      this._bindGlobalEvents();
    }

    _initDom() {
      if (typeof document === "undefined") return;
      if (document.getElementById("sr-login-modal")) return;

      const backdrop = document.createElement("div");
      backdrop.id = "sr-login-modal";
      backdrop.className = "sr-login-backdrop";
      backdrop.setAttribute("role", "dialog");
      backdrop.setAttribute("aria-modal", "true");
      backdrop.setAttribute("aria-labelledby", "sr-login-title");

      backdrop.innerHTML = `
        <div class="sr-login-card" id="sr-login-card">
          <button type="button" class="sr-login-close-btn" id="sr-login-close-btn" aria-label="Cerrar ventana">×</button>

          <div class="sr-login-header">
            <div class="sr-login-icon" aria-hidden="true">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <h2 class="sr-login-title" id="sr-login-title">Ingresa a Social R</h2>
            <p class="sr-login-subtitle" id="sr-login-subtitle">Usa tu RUT o IPE para guardar tu progreso y continuar desde cualquier dispositivo.</p>
          </div>

          <div class="sr-login-body" id="sr-login-body">
            <!-- STEP 1: RUT INPUT FORM -->
            <form id="sr-login-form" autocomplete="off">
              <div class="sr-login-form-group">
                <label for="sr-login-rut-input" class="sr-login-label">RUT o IPE</label>
                <div class="sr-login-input-wrapper">
                  <input
                    type="text"
                    id="sr-login-rut-input"
                    class="sr-login-input"
                    placeholder="12.345.678-9"
                    maxlength="14"
                    inputmode="text"
                    autocomplete="username"
                    autocapitalize="characters"
                    spellcheck="false"
                    required
                  />
                </div>
                <div class="sr-login-error-msg" id="sr-login-error"></div>
              </div>

              <button type="submit" class="sr-login-btn-primary" id="sr-login-submit-btn">
                <span>Ingresar</span>
                <span aria-hidden="true">→</span>
              </button>
            </form>
          </div>
        </div>
      `;

      document.body.appendChild(backdrop);
      this.backdropEl = backdrop;
      this.cardEl = backdrop.querySelector(".sr-login-card");

      // Bind close button
      const closeBtn = backdrop.querySelector("#sr-login-close-btn");
      closeBtn.addEventListener("click", () => this.close());

      // Close on backdrop click (if dismissible)
      backdrop.addEventListener("click", (e) => {
        if (e.target === backdrop && this.options.dismissible) {
          this.close();
        }
      });

      // Bind form
      const form = backdrop.querySelector("#sr-login-form");
      const input = backdrop.querySelector("#sr-login-rut-input");
      const errorMsg = backdrop.querySelector("#sr-login-error");

      // Live RUT formatting on input
      input.addEventListener("input", (e) => {
        const validator = window.SocialR && window.SocialR.RutValidator;
        if (!validator) return;
        const cursorPos = input.selectionStart;
        const prevLen = input.value.length;
        const formatted = validator.format(input.value);
        input.value = formatted;
        input.classList.remove("has-error");
        errorMsg.classList.remove("is-visible");
        errorMsg.textContent = "";
      });

      // Form submit
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await this._handleSubmit(input.value);
      });
    }

    _bindGlobalEvents() {
      if (typeof window === "undefined") return;

      // Close on ESC
      window.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && this.isOpen() && this.options.dismissible) {
          this.close();
        }
      });

      // Listen to auth changes to update topbar/drawer
      if (window.SocialR && window.SocialR.events && typeof window.SocialR.events.on === "function") {
        window.SocialR.events.on("auth_state_changed", () => {
          this.updateUiElements();
        });
        window.SocialR.events.on("cloud_sync_status", (e) => {
          this.updateSyncIndicator(e);
        });
      }
    }

    isOpen() {
      return Boolean(this.backdropEl && this.backdropEl.classList.contains("is-open"));
    }

    open(options = {}) {
      this._initDom();
      this.options = {
        dismissible: typeof options.dismissible === "boolean" ? options.dismissible : true,
        onSuccess: options.onSuccess || null,
        targetUrl: options.targetUrl || null,
      };

      // Pause/end tour if active so it does not collide with login modal
      if (window.SocialR && window.SocialR.tour && typeof window.SocialR.tour.end === "function" && window.SocialR.tour.active) {
        window.SocialR.tour.end(false);
      }

      const closeBtn = this.backdropEl.querySelector("#sr-login-close-btn");
      if (closeBtn) {
        closeBtn.style.display = this.options.dismissible ? "block" : "none";
      }

      this._renderStep1();
      this.backdropEl.classList.add("is-open");

      setTimeout(() => {
        const input = this.backdropEl.querySelector("#sr-login-rut-input");
        if (input) input.focus();
      }, 100);
    }

    close() {
      if (!this.backdropEl) return;
      this.backdropEl.classList.remove("is-open");
      this.pendingStudentData = null;

      // Update home profile control if on landing
      if (window.SocialR && typeof window.SocialR.updateProfileControl === "function") {
        window.SocialR.updateProfileControl();
      }

      // When login modal closes, trigger tour auto-launch check if eligible
      if (window.SocialR && window.SocialR.tour && typeof window.SocialR.tour.checkAutoLaunch === "function") {
        setTimeout(() => {
          window.SocialR.tour.checkAutoLaunch();
        }, 300);
      }
    }

    _renderStep1() {
      const title = this.backdropEl.querySelector("#sr-login-title");
      const subtitle = this.backdropEl.querySelector("#sr-login-subtitle");
      const body = this.backdropEl.querySelector("#sr-login-body");

      title.textContent = "Ingresa a Social R";
      subtitle.textContent = "Identifícate con tu RUT o IPE para sincronizar tu progreso, o continúa como invitado.";

      body.innerHTML = `
        <form id="sr-login-form" autocomplete="off">
          <div class="sr-login-form-group">
            <label for="sr-login-rut-input" class="sr-login-label">RUT o IPE</label>
            <div class="sr-login-input-wrapper">
              <input
                type="text"
                id="sr-login-rut-input"
                class="sr-login-input"
                placeholder="12.345.678-9"
                maxlength="14"
                inputmode="text"
                autocomplete="username"
                autocapitalize="characters"
                spellcheck="false"
                required
              />
            </div>
            <div class="sr-login-error-msg" id="sr-login-error"></div>
          </div>

          <button type="submit" class="sr-login-btn-primary" id="sr-login-submit-btn">
            <span>Ingresar con RUT o IPE</span>
            <span aria-hidden="true">→</span>
          </button>
        </form>

        <div class="sr-login-divider"><span>o</span></div>

        <button type="button" class="sr-login-btn-guest" id="sr-login-guest-btn">
          <span>Continuar sin iniciar sesión</span>
        </button>

        <div class="sr-login-info-box">
          <p class="sr-login-info-item">
            <strong>Estudiantes de los cursos:</strong> Inicia sesión para guardar tu progreso y continuar desde cualquier dispositivo.
          </p>
          <p class="sr-login-info-item">
            <strong>Invitados:</strong> Puedes usar Social R libremente sin iniciar sesión. Tu progreso quedará guardado solo en este navegador.
          </p>
        </div>
      `;

      const input = body.querySelector("#sr-login-rut-input");
      const errorMsg = body.querySelector("#sr-login-error");
      const form = body.querySelector("#sr-login-form");
      const guestBtn = body.querySelector("#sr-login-guest-btn");

      input.addEventListener("input", () => {
        const validator = window.SocialR && window.SocialR.RutValidator;
        if (validator) {
          input.value = validator.format(input.value);
        }
        input.classList.remove("has-error");
        errorMsg.classList.remove("is-visible");
      });

      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await this._handleSubmit(input.value);
      });

      if (guestBtn) {
        guestBtn.addEventListener("click", () => {
          const cloudConfig = window.SocialR && window.SocialR.cloudConfig;
          if (cloudConfig && typeof cloudConfig.setGuestMode === "function") {
            cloudConfig.setGuestMode(true);
          }
          this.close();
        });
      }
    }

    _showError(message) {
      const input = this.backdropEl.querySelector("#sr-login-rut-input");
      const errorMsg = this.backdropEl.querySelector("#sr-login-error");
      if (input) input.classList.add("has-error");
      if (errorMsg) {
        errorMsg.textContent = message;
        errorMsg.classList.add("is-visible");
      }
    }

    async _handleSubmit(rawRut) {
      const validator = window.SocialR && window.SocialR.RutValidator;
      if (validator && !validator.validate(rawRut)) {
        this._showError("Revisa el RUT o IPE ingresado.");
        return;
      }

      const submitBtn = this.backdropEl.querySelector("#sr-login-submit-btn");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span>Verificando...</span>`;
      }

      const adapter = window.SocialR && window.SocialR.cloudAdapter;
      if (!adapter) {
        this._showError("Servicio de conexión no disponible.");
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>Ingresar</span> →`;
        }
        return;
      }

      try {
        const data = await adapter.login(rawRut);
        this.pendingStudentData = data;
        this._renderStep2(data);
      } catch (err) {
        this._showError(err.message || "Error al verificar el RUT o IPE.");
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>Ingresar</span> →`;
        }
      }
    }

    _renderStep2(data) {
      const student = data.student || {};
      const title = this.backdropEl.querySelector("#sr-login-title");
      const subtitle = this.backdropEl.querySelector("#sr-login-subtitle");
      const body = this.backdropEl.querySelector("#sr-login-body");

      const cloudConfig = window.SocialR && window.SocialR.cloudConfig;
      const firstName = (window.SocialR && typeof window.SocialR.getFirstName === "function")
        ? window.SocialR.getFirstName(student.displayName)
        : (cloudConfig && typeof cloudConfig.getFirstName === "function"
          ? cloudConfig.getFirstName(student.displayName)
          : (student.displayName || "Estudiante").split(" ")[0]);
      title.textContent = `¡Hola, ${firstName}!`;
      subtitle.textContent = "Confirmemos tu identidad para ingresar a tu sesión.";

      const hasLegacy = cloudConfig ? cloudConfig.hasLegacyProgress() : false;

      let legacyHtml = "";
      if (hasLegacy) {
        legacyHtml = `
          <div class="sr-login-legacy-choice-card">
            <div class="sr-login-legacy-header">
              <span class="sr-login-legacy-icon" aria-hidden="true">💡</span>
              <span>Progreso previo en este navegador</span>
            </div>
            <p class="sr-login-legacy-desc">
              Detectamos ejercicios resueltos antes de iniciar sesión. ¿Deseas asociarlos a tu cuenta?
            </p>
            <div class="sr-login-legacy-options">
              <label class="sr-login-legacy-option">
                <input type="radio" name="sr-legacy-decision" value="merge" checked />
                <span class="sr-login-option-label">
                  <strong>Sí, asociar a mi cuenta</strong>
                  <small>Conservar el trabajo previo y sincronizarlo a mi perfil.</small>
                </span>
              </label>
              <label class="sr-login-legacy-option">
                <input type="radio" name="sr-legacy-decision" value="discard" />
                <span class="sr-login-option-label">
                  <strong>No, usar solo mi progreso en la nube</strong>
                  <small>Recomendado si este computador es compartido o de uso público.</small>
                </span>
              </label>
            </div>
          </div>
        `;
      }

      body.innerHTML = `
        <div class="sr-login-confirm-box">
          <div class="sr-login-confirm-name">${student.displayName || "Estudiante"}</div>
          <div class="sr-login-confirm-rut">Identificador: ${student.rutMasked || "••.•••.•••-•"}</div>
        </div>

        ${legacyHtml}

        <button type="button" class="sr-login-btn-primary" id="sr-login-confirm-btn">
          <span>Continuar al curso</span>
          <span aria-hidden="true">→</span>
        </button>

        <button type="button" class="sr-login-btn-secondary" id="sr-login-back-btn">
          <span>No soy yo (cambiar identificación)</span>
        </button>
      `;

      const confirmBtn = body.querySelector("#sr-login-confirm-btn");
      const backBtn = body.querySelector("#sr-login-back-btn");

      confirmBtn.addEventListener("click", async () => {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = `<span>Cargando tu progreso...</span>`;

        let shouldMergeLegacy = false;
        if (hasLegacy) {
          const selectedOption = body.querySelector('input[name="sr-legacy-decision"]:checked');
          shouldMergeLegacy = selectedOption ? (selectedOption.value === "merge") : false;
        }

        // If user explicitly chose to merge legacy progress
        if (shouldMergeLegacy && window.SocialR && window.SocialR.progress) {
          window.SocialR.progress.mergeLegacyProgress();
        }

        // Always clean unauthenticated legacy progress so it cannot leak to subsequent users
        if (hasLegacy && cloudConfig && typeof cloudConfig.clearLegacyProgress === "function") {
          cloudConfig.clearLegacyProgress(cloudConfig.courseId);
        }

        // Rebind progress store to student namespace and pull cloud progress
        if (window.SocialR && window.SocialR.progress) {
          await window.SocialR.progress.rebindSession(student.id);
        }

        this.close();

        if (typeof this.options.onSuccess === "function") {
          this.options.onSuccess(data);
        } else if (this.options.targetUrl) {
          window.location.href = this.options.targetUrl;
        } else if (!window.location.pathname.includes("curso.html")) {
          window.location.href = "curso.html";
        }
      });

      backBtn.addEventListener("click", () => {
        if (cloudConfig) cloudConfig.clearSession();
        this._renderStep1();
      });
    }

    /**
     * Updates topbar user pill and sync indicator
     */
    updateUiElements() {
      const cloud = window.SocialR && window.SocialR.cloudConfig;
      const isAuth = cloud ? cloud.isAuthenticated() : false;
      const displayName = cloud ? cloud.getDisplayName() : null;
      const firstName = (window.SocialR && typeof window.SocialR.getFirstName === "function")
        ? window.SocialR.getFirstName(displayName)
        : (cloud && typeof cloud.getFirstName === "function"
          ? cloud.getFirstName(displayName)
          : (displayName ? displayName.split(" ")[0] : "Estudiante"));

      // 1. Topbar user pill
      const userContainer = document.getElementById("sr-topbar-user-area");
      if (userContainer) {
        if (isAuth) {
          userContainer.innerHTML = `
            <div class="sr-user-pill" title="Sesión activa como ${displayName}">
              <span class="sr-user-pill__name">👤 ${firstName}</span>
              <button class="sr-user-pill__logout" id="sr-topbar-logout-btn" title="Cerrar sesión">Salir</button>
            </div>
          `;
          const logoutBtn = userContainer.querySelector("#sr-topbar-logout-btn");
          if (logoutBtn) {
            logoutBtn.addEventListener("click", () => this.handleLogout());
          }
        } else if (cloud && cloud.isCloudEnabled()) {
          userContainer.innerHTML = `
            <button class="sr-btn-login-trigger" id="sr-topbar-login-btn" style="background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #cbd5e1; border-radius: 6px; padding: 0.25rem 0.6rem; font-size: 0.775rem; cursor: pointer;">
              Ingresar con RUT o IPE
            </button>
          `;
          const loginBtn = userContainer.querySelector("#sr-topbar-login-btn");
          if (loginBtn) {
            loginBtn.addEventListener("click", () => this.open());
          }
        } else {
          userContainer.innerHTML = "";
        }
      }

      // 2. Drawer user box
      const drawerList = document.getElementById("sr-drawer-list");
      let drawerUserBox = document.getElementById("sr-drawer-user-box");
      if (drawerList) {
        if (isAuth) {
          if (!drawerUserBox) {
            drawerUserBox = document.createElement("div");
            drawerUserBox.id = "sr-drawer-user-box";
            drawerUserBox.className = "sr-drawer-user-box";
            const drawerFooter = document.querySelector(".sr-drawer-footer");
            if (drawerFooter) {
              drawerFooter.parentElement.insertBefore(drawerUserBox, drawerFooter);
            }
          }
          drawerUserBox.innerHTML = `
            <div>
              <div class="sr-drawer-user-name">${displayName}</div>
              <div class="sr-drawer-user-rut">${cloud.getRutMasked() || ""}</div>
            </div>
            <button class="sr-drawer-user-btn" id="sr-drawer-logout-btn">Cambiar estudiante</button>
          `;
          const logoutBtn = drawerUserBox.querySelector("#sr-drawer-logout-btn");
          if (logoutBtn) {
            logoutBtn.addEventListener("click", () => this.handleLogout());
          }
        } else if (drawerUserBox) {
          drawerUserBox.remove();
        }
      }
    }

    updateSyncIndicator(e) {
      const container = document.getElementById("sr-sync-indicator");
      if (!container) return;

      const status = (e && e.status) || "synced";
      const message = (e && e.message) || "";

      container.className = `sr-sync-indicator is-${status}`;

      let label = "Guardado";
      if (status === "syncing") label = "Guardando...";
      if (status === "offline") label = "Sin conexión";
      if (status === "error") label = "Error de sync";

      container.innerHTML = `
        <span class="sr-sync-dot"></span>
        <span class="sr-sync-text">${label}</span>
      `;
      if (message) {
        container.setAttribute("title", message);
      }
    }

    async handleLogout() {
      const adapter = window.SocialR && window.SocialR.cloudAdapter;
      if (adapter && typeof adapter.logout === "function") {
        await adapter.logout();
      }
      const cloud = window.SocialR && window.SocialR.cloudConfig;
      if (cloud && typeof cloud.clearSession === "function") {
        cloud.clearSession();
      }
      if (window.SocialR && window.SocialR.progress) {
        window.SocialR.progress.rebindSession(null);
      }
      this.updateUiElements();
      if (window.SocialR && typeof window.SocialR.updateProfileControl === "function") {
        window.SocialR.updateProfileControl();
      }
      // Redirect or reload
      if (window.location.pathname.includes("curso.html")) {
        window.location.href = "index.html";
      } else {
        window.location.reload();
      }
    }
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.LoginModal = LoginModal;

  document.addEventListener("DOMContentLoaded", () => {
    window.SocialR.loginModal = new LoginModal();
    window.SocialR.loginModal.updateUiElements();
  });
})();
