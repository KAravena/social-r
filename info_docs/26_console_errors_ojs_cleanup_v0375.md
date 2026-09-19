# Social R v0.3.7.5 — Console Error Semantics & OJS Cleanup

**Fecha:** 17 de Agosto, 2026  
**Versión:** `v0.3.7.5`  
**Estado:** Stable Baseline Passed (E2E 8/8 PASS)

---

## 1. Bug Observado

En versiones anteriores (`v0.3.7.4`), la ejecución de código válido como `18 + 25` o `18 + 12` se renderizaba correctamente en la zona visual de la **R Console** (`[1] 43` / `[1] 30`). Sin embargo, se presentaron dos anomalías severas:
1. **Errores y Warnings Invisibles:** Al ejecutar código con errores de sintaxis (`18 +`) o referencias a objetos inexistentes (`social_r_objeto_que_no_existe_92831`), la región de R Console permanecía en blanco y parecía no responder.
2. **Fuga de Variables Internas de OJS/Quarto Live:** En la interfaz normal del estudiante aparecían objetos reactivos internos de Quarto Live / Observable JS tales como `_webr_editor_1 = Object {code: ...}` y `_webr_value_1 = Object {result: ...}`, contaminando la interfaz de usuario.

---

## 2. Error DOM Diagnosis & Native Quarto Live Error Test

### Diagnóstico en el DOM Nativo
Al ejecutar `social_r_objeto_que_no_existe_92831` con `?debug=quarto-live`, se constató que:
- El motor de Quarto Live WebAssembly **SÍ** ejecutó el código y produjo la evaluación nativa en R.
- El contenedor `.cell-output-container` contenía el elemento `.callout-important` con el texto:
  ```html
  <div class="callout-important callout callout-style-default callout-captioned">
    <div class="callout-header d-flex align-content-center">
      <div class="callout-icon-container"><i class="callout-icon"></i></div>
      <div class="callout-caption-container flex-fill">R Error: </div>
    </div>
    <div class="callout-body-container callout-body">
      <pre>Error: object 'social_r_objeto_que_no_existe_92831' not found</pre>
    </div>
  </div>
  ```
- Para warnings (`sqrt(-1)`), Quarto Live produjo un `.callout-warning` con `Warning: NaNs produced`.

---

## 3. Causa Raíz en CSS y Análisis de `display: contents`

### Causa 1: Ocultamiento Global de Callouts
En `css/editor-console.css`, una regla preventiva diseñada para ocultar callouts de documentación externa dentro de la celda de ejercicio estaba ocultando todos los callouts:
```css
/* REGRESIÓN ANTERIOR */
.sr-editor-body .callout {
  display: none !important;
}
```
Esto provocaba que `.callout-important` (errores de R) y `.callout-warning` (advertencias de R) fueran silenciados del DOM visible.

### Causa 2: Ruptura de Encapsulación de OJS (`display: contents`)
En `v0.3.7.4`, para empujar el output nativo al grid inferior de la consola, se aplicó:
```css
/* REGRESIÓN ANTERIOR */
.sr-editor-body .ojs-in-a-box-waiting-for-module-import {
  display: contents !important;
}
```
Quarto Live coloca los inspectores reactivos de OJS dentro de un contenedor con clase `<div class="quarto-ojs-hide ojs-in-a-box-waiting-for-module-import">`. La regla nativa de Quarto es `.quarto-ojs-hide { display: none; }`. Al forzar `display: contents !important` sin excluir `.quarto-ojs-hide`, se anulaba el `display: none` nativo, forzando a que las celdas reactivas `_webr_editor_1` y `_webr_value_1` se renderizaran en la pantalla.

---

## 4. Solución Implementada (Fix)

### A. Restauración y Estilización Limpia de Errores y Warnings
Se eliminó la regla que ocultaba `.callout` y se definieron selectores específicos en estilo Positron/RStudio claro:
```css
/* Errores nativos de R */
.sr-editor-body .callout-important.callout {
  display: block !important;
  margin: 0.35rem 0.5rem;
  padding: 0.4rem 0.6rem;
  background-color: #fef2f2 !important;
  border: 1px solid #fecaca !important;
  border-left: 4px solid #ef4444 !important;
  border-radius: 4px;
  color: #b91c1c !important;
  font-family: var(--sr-font-mono);
  font-size: 0.82rem;
}

/* Warnings nativos de R */
.sr-editor-body .callout-warning.callout {
  display: block !important;
  margin: 0.35rem 0.5rem;
  padding: 0.4rem 0.6rem;
  background-color: #fffbeb !important;
  border: 1px solid #fef3c7 !important;
  border-left: 4px solid #f59e0b !important;
  border-radius: 4px;
  color: #b45309 !important;
  font-family: var(--sr-font-mono);
  font-size: 0.82rem;
}
```

### B. Encapsulación Estricta de Internals de OJS
Se restringió el uso de `display: contents` para excluir explícitamente `.quarto-ojs-hide`:
```css
.sr-editor-body > div:not(.quarto-ojs-hide),
.sr-editor-body .ojs-in-a-box-waiting-for-module-import:not(.quarto-ojs-hide),
.sr-editor-body .exercise-cell {
  display: contents !important;
}

.sr-editor-body .quarto-ojs-hide,
.sr-editor-body .observablehq--inspect,
.sr-editor-body .observablehq--cellname,
.sr-editor-body .observablehq--field {
  display: none !important;
  visibility: hidden !important;
}
```

---

## 5. Matriz de Validación E2E

Todas las pruebas automatizadas y capturas de pantalla fueron generadas en `docs/screenshots/v0.3.7.5/`:

| Test | Input Código | Comportamiento Esperado | Resultado | Screenshot |
|---|---|---|---|---|
| **1. Normal Result** | `18 + 25` | Output `[1] 43` en R Console | **PASS** | `01-normal-result.png` |
| **2. Object Error** | `social_r_objeto_que_no_existe_92831` | `R Error: Error: object 'social_r_...' not found` | **PASS** | `02-object-error.png` |
| **3. Syntax Error** | `18 +` | `R Error in parse(text = input): unexpected end of input` | **PASS** | `03-syntax-error.png` |
| **4. Warning** | `sqrt(-1)` | `R Warning in sqrt(-1): NaNs produced` + `[1] NaN` | **PASS** | `04-warning.png` |
| **5. Recovery** | `18 + 12` | Output `[1] 30` en R Console tras errores | **PASS** | `05-recovery-after-error.png` |
| **6. Message/Cat** | `message()`, `cat()` | Mensajes capturados en stderr y stdout | **PASS** | Verificado en log |
| **7. Clean UI** | N/A | `_webr_editor_` y `_webr_value_` ausentes de la UI | **PASS** | `06-clean-ui-no-ojs.png` |
| **8. Run vs Submit** | `18 + 11` vs `18 + 12` | Run no califica; Submit valida en panel izq. | **PASS** | Verificado en suite |

---

## 6. Verificación de Regresiones

Se ejecutó la suite completa de checkpoints anteriores (`tests/run_v0374_master_suite.py`):
- **Checkpoint A (Native Run & Console Positioning):** PASS
- **Checkpoint B (Grading & Stale Feedback Invalidation):** PASS (4/4)
- **Checkpoint C (Navigation Stepper & Linear Gating):** PASS (4/4)
- **Checkpoint D (Shortcuts Ctrl+Enter / Ctrl+Shift+Enter):** PASS (4/4)
