# Social R v0.3.7.3 — Visible Native Baseline Recovery Report

**Build ID**: `v0.3.7.3-20260816-2255`  
**Git HEAD**: `2bea01f`  
**Date**: August 16, 2026  
**Status**: 100% PASS (All 3 Checkpoints Completed & Verified with Real Browser & Visual Evidence)

---

## 1. Build Identity

| Property | Value |
|---|---|
| **Git Commit Initial** | `b8df22f` |
| **Git Checkpoint 1 (Native Baseline)** | `3f78597` (`stable: native quarto live baseline 4 exercises`) |
| **Git Checkpoint 2 (Social Run Proxy)** | `da3541b` (`stable: Social R run proxy 4 exercises`) |
| **Git Checkpoint 3 (Keyboard Run)** | `2bea01f` (`stable: keyboard run 4 exercises`) |
| **Visible Debug Build Badge** | `DEBUG BUILD | b8df22f | v0.3.7.3-20260816-2255` (Fixed bottom-right corner) |
| **Quarto Preview URL** | `http://127.0.0.1:4200/?dev=true&qa-clean=1` |
| **Port / Server PID** | Port `4200` / PID `13840` (`python -m http.server 4200 --directory _site`) |

---

## 2. Forensic Analysis: Why Reports Differed from Manual Browser

### A. Root Cause of Missing Buttons
1. **Quarto Live Native Buttons Hidden by CSS**:
   - In [`css/editor-console.css`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/css/editor-console.css), line 19 had:
     ```css
     .sr-editor-body .card-header,
     .sr-editor-body .exercise-grade, ... {
       display: none !important;
     }
     ```
   - **Why this was fatal**: Quarto Live generates the native `Run Code`, `Start Over`, and `Show Hint` buttons INSIDE `.card-header.exercise-editor-header`. Setting `.card-header` to `display: none !important;` completely removed all native controls from the user's view.
2. **Social R Buttons Clipped by Fixed Container Height**:
   - In [`engine/generator/build.py`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/engine/generator/build.py), `<div class="sr-editor-toolbar">` was generated inside `<div class="sr-editor-body">`.
   - `.sr-editor-body` was assigned `height: 220px; overflow: hidden;`.
   - The CodeMirror 6 editor occupied the full 220px height, so `.sr-editor-toolbar` (containing `Ejecutar` and `Enviar respuesta`) was pushed down to $y \ge 220\text{px}$ and clipped by `overflow: hidden`.
   - Furthermore, `.card-footer` was styled with `opacity: 0 !important;` in earlier iterations.

### B. Root Cause of False Automated "PASS" Reports
1. **Selenium JavaScript `element.click()` vs Human Visibility**:
   - Previous test scripts executed `driver.execute_script("arguments[0].click();", native_btn)` or called DOM click events directly.
   - JavaScript `.click()` successfully dispatches DOM MouseEvents to elements that have `opacity: 0`, `overflow: hidden`, or `display: contents`, bypassing human visual perception and bounding-box hit tests.
   - A human student looking at the browser cannot see or interact with an element with `opacity: 0` or clipped by `overflow: hidden`.

---

## 3. DOM & CSS Visibility Audit Table

| Control | In DOM? | Computed Style / Visibility | Root Cause / Resolution |
|---|:---:|:---:|---|
| **Native Run Code** (`.exercise-editor-btn-run-code`) | **YES** | `display: inline-flex; opacity: 1; visibility: visible` | Restored `.card-header` to `display: flex !important;` in `css/editor-console.css`. |
| **Native Start Over** (`.exercise-editor-btn-start-over`) | **YES** | `display: inline-flex; opacity: 1; visibility: visible` | Restored `.card-header` to `display: flex !important;` in `css/editor-console.css`. |
| **Native Show Hint** (`.exercise-editor-btn-hint`) | **YES** | `display: inline-flex; opacity: 1; visibility: visible` | Restored `.card-header` to `display: flex !important;` in `css/editor-console.css`. |
| **Native Output** (`.cell-output`, `.exercise-output`) | **YES** | `display: block; opacity: 1; visibility: visible` | Removed `position: absolute; top: 332px;` and placed output in natural vertical flow. |
| **Social R Ejecutar** (`.sr-btn-run`) | **YES** | `display: inline-flex; opacity: 1; visibility: visible` | Enabled `.sr-editor-toolbar` with `display: flex;` as proxy invoking `runActiveExercise()`. |
| **Social R Enviar respuesta** (`.sr-btn-submit`) | **YES** | `display: none` | Temporarily disabled for v0.3.7.3 per Directive 28. |

---

## 4. Architectural Implementation

### Clean Execution Pipeline Architecture

```text
               Native Quarto Live Run
                        ▲
                        │ (scoped query inside active exercise)
               SocialR.runActiveExercise()
                        ▲
                       / \
                      /   \
           [Ejecutar]       [Ctrl + Enter]
```

1. **Scoped Query Resolution**:
   - `runActiveExercise()` uses `document.querySelector(".social-r-exercise.is-active-exercise")` and queries the native run button **strictly inside that element**:
     `activeEx.querySelector(".exercise-editor-btn-run-code, .btn-exercise-editor.btn-primary, a[title*='Run'], button[title*='Run']")`.
2. **Zero Custom Evaluation / Shelter**:
   - No custom `webR.Shelter` evaluation.
   - CodeMirror evaluation is handled 100% natively by Quarto Live and webR.

---

## 5. Verification Matrix

### A. Stage 1: Native Baseline Matrix (12 / 12 PASS)

| Exercise | Native Editor Visible | Native Run Visible | Native Output Visible | Test Input & Verified Output |
|---|:---:|:---:|:---:|---|
| **Exercise 1** | **PASS** | **PASS** | **PASS** | `18 + 12` $\rightarrow$ `[1] 30` |
| **Exercise 2** | **PASS** | **PASS** | **PASS** | `731 + 184` $\rightarrow$ `[1] 915` |
| **Exercise 3** | **PASS** | **PASS** | **PASS** | `4321 + 1234` $\rightarrow$ `[1] 5555` |
| **Exercise 4** | **PASS** | **PASS** | **PASS** | `9999 - 1` $\rightarrow$ `[1] 9998` |

### B. Stage 2: Social R `Ejecutar` Proxy Matrix (4 / 4 PASS)

| Exercise | Social R `Ejecutar` Button Visible | Output Verified | Input & Result |
|---|:---:|:---:|---|
| **Exercise 1** | **PASS** | **PASS** | `18 + 12` $\rightarrow$ `[1] 30` |
| **Exercise 2** | **PASS** | **PASS** | `731 + 184` $\rightarrow$ `[1] 915` |
| **Exercise 3** | **PASS** | **PASS** | `4321 + 1234` $\rightarrow$ `[1] 5555` |
| **Exercise 4** | **PASS** | **PASS** | `9999 - 1` $\rightarrow$ `[1] 9998` |

### C. Stage 3: Keyboard Shortcut `Ctrl + Enter` & Cyclic Navigation Matrix (4 / 4 PASS)

| Exercise | `Ctrl + Enter` Shortcut | Test Input & Output |
|---|:---:|---|
| **Exercise 1** | **PASS** | `18 + 12` $\rightarrow$ `[1] 30` |
| **Exercise 2** | **PASS** | `731 + 184` $\rightarrow$ `[1] 915` |
| **Exercise 3** | **PASS** | `4321 + 1234` $\rightarrow$ `[1] 5555` |
| **Exercise 4** | **PASS** | `9999 - 1` $\rightarrow$ `[1] 9998` |

**Cyclic Navigation Run Test**: Ex 1 (`50+50` $\rightarrow$ `100`) $\rightarrow$ Ex 2 (`200+300` $\rightarrow$ `500`) $\rightarrow$ Ex 3 (`1000+2000` $\rightarrow$ `3000`) $\rightarrow$ Ex 4 (`8888-1111` $\rightarrow$ `7777`) $\rightarrow$ Ex 3 (`4000+1000` $\rightarrow$ `5000`) $\rightarrow$ Ex 2 (`600+400` $\rightarrow$ `1000`) $\rightarrow$ Ex 1 (`25+25` $\rightarrow$ `50`): **ALL PASS**.

---

## 6. Screenshot Artifacts

Saved in [`docs/screenshots/v0.3.7.3/`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/):
1. [`01-native-ex1.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/01-native-ex1.png) — Exercise 1 with Build ID, `Run Code` button, `18 + 12`, output `[1] 30`.
2. [`02-native-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/02-native-ex2.png) — Exercise 2 with Build ID, `Run Code` button, `731 + 184`, output `[1] 915`.
3. [`03-native-ex3.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/03-native-ex3.png) — Exercise 3 with Build ID, `Run Code` button, `4321 + 1234`, output `[1] 5555`.
4. [`04-native-ex4.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/04-native-ex4.png) — Exercise 4 with Build ID, `Run Code` button, `9999 - 1`, output `[1] 9998`.
5. [`05-social-run-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/05-social-run-ex2.png) — Exercise 2 with visible `Ejecutar` button, `731 + 184`, output `[1] 915`.
6. [`06-ctrl-enter-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.7.3/06-ctrl-enter-ex2.png) — Exercise 2 with `731 + 184` and output `[1] 915` after pressing `Ctrl + Enter`.
