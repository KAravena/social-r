# Social R v0.3.7.1 — Technical Report & Regression Analysis

**Build ID**: `v0.3.7.1-runtime-recovery-20260816-2150`  
**Date**: August 16, 2026  
**Status**: 100% PASS (All 6 Gates Verified in Real Automated Edge Browser)

---

## 1. Executive Summary & Root Cause Findings

In version **v0.3.7**, a critical visual indicator regression occurred where the header status badge remained stuck indefinitely on `"Iniciando R..."`, leading to the initial impression that webR had failed to boot.

### Step-by-Step Regression Analysis (Answers to User Questions):

1. **Did removing `#sr-console-body` cause or contribute to the startup failure?**  
   * **NO.** `#sr-console-body` was an artificial mirror panel used in legacy custom console attempts. Removing it was correct as part of adopting Quarto Live's native output architecture.

2. **Did stale-feedback listeners cause or contribute to startup failure?**  
   * **NO.** The input event listener in `SocialREngine` was lightweight and did not block the promise resolution of webR.

3. **Did `QuartoLiveAdapter` changes cause or contribute to startup failure?**  
   * **INDIRECTLY (Missing Script Inclusion).** `js/app/shell.js` contained `initWebRStatus()`, the function responsible for polling webR/OJS runtime readiness and updating `<span id="sr-webr-status-text">Iniciando R...</span>` to `"R listo"`. When `build.py` was refactored in v0.3.7, `<script src="js/app/shell.js"></script>` was omitted from `include-after-body`. As a result, `initWebRStatus()` was never invoked, leaving the DOM element stuck on `"Iniciando R..."` forever even though webR was running. Furthermore, `js/app/shell.js` did not self-invoke on DOM ready.

4. **Runtime Boot Classification**:
   * **webR Runtime Ready**: **YES**
   * **Status Indicator Accurate**: **YES** (after restoring `js/app/shell.js` inclusion and auto-booting `initShell()`)

---

## 2. Minimal Fix Applied

1. **`engine/generator/build.py`**: Added `<script src="js/app/shell.js"></script>` to `include-after-body` YAML section.
2. **`js/app/shell.js`**:
   - Updated `initWebRStatus()` to inspect `window._ojs` main module scope, `window.webR`, and `.cm-editor` elements.
   - Added auto-execution of `initShell()` on `DOMContentLoaded`.
3. **`js/platform/quarto-live-adapter.js`**:
   - Preserved `.last_value` and `.result` in webR evaluation before calling `WebRGrader` to ensure exercise submissions reliably produce success cards (`¡Excelente! R calculó el total de 42 estudiantes.`).

---

## 3. Real Browser Verification Gates (6 / 6 PASS)

| Gate # | Description | Input / Trigger | Expected Output | Actual Empirical Result | Status |
|---|---|---|---|---|---|
| **Gate 1** | R Ready Status Transition | Page load (127.0.0.1:4200) | `Iniciando R...` -> `R listo` | `R listo` (0s) | **PASS** |
| **Gate 2** | Ex 1 Native Run | Ex 1 (`18 + 12`) -> Native Run button | `[1] 30` in R Console | `[1] 30` | **PASS** |
| **Gate 3** | Ex 2 Native Run | Ex 2 (`25 + 17`) -> Native Run button | `[1] 42` in R Console | `[1] 42` | **PASS** |
| **Gate 4** | Ex 2 Social R Run | Ex 2 (`999 + 1`) -> `Ejecutar` button | `[1] 1000` in R Console | `[1] 1000` | **PASS** |
| **Gate 5** | Ex 2 Keyboard Shortcut | Ex 2 (`731 + 184`) -> `Ctrl + Enter` | `[1] 915` in R Console | `[1] 915` | **PASS** |
| **Gate 6** | Ex 2 Submit Basic | Ex 2 (`25 + 17`) -> `Enviar respuesta` | Feedback: `Correcto` | Feedback: `Correcto` | **PASS** |

---

## 4. Screenshot Evidence Artifacts

All screenshots have been generated and stored in `docs/screenshots/v0.3.7.1/`:

1. [`01-runtime-initializing.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/01-runtime-initializing.png) — Initial page load state
2. [`02-runtime-ready.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/02-runtime-ready.png) — Header badge displaying `R listo`
3. [`03-native-run-ex1.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/03-native-run-ex1.png) — Ex 1 producing `[1] 30`
4. [`04-native-run-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/04-native-run-ex2.png) — Ex 2 producing `[1] 42` via Native Run
5. [`05-social-run-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/05-social-run-ex2.png) — Ex 2 producing `[1] 1000` via Social R `Ejecutar`
6. [`06-submit-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.1/06-submit-ex2.png) — Ex 2 displaying green `Correcto` feedback card

---

## 5. Next Steps & Hard Stop

As required by user directives:
- All execution, layout changes, feature additions, or further refactoring are **HALTED**.
- Awaiting user manual testing and review on `http://127.0.0.1:4200/`.
