# SOCIAL R v0.3.7.4 — STABLE EXERCISE LOOP DOCUMENTATION

## Resumen Ejecutivo

En la versión **Social R v0.3.7.4** se ha completado la estabilización integral del ciclo de aprendizaje en Social R:

```
CodeMirror Editor
  ↓ (Ctrl + Enter / Ejecutar)
webR Runtime (WASM)
  ↓
R Console (Dark Theme #0f172a, font-mono, order-based layout)
  ↓ (Ctrl + Shift + Enter / Enviar respuesta)
WebREvaluator & WebRGrader (Quarto Live Native Engine)
  ↓
Feedback Pedagógico (Correcto / Revisa tu respuesta / Diagnósticos en panel izquierdo)
  ↓
Ciclo de Progreso & Navegación (0% -> 25% -> 50% -> 75% -> 100%, Siguiente / Continuar habilitados)
```

---

## 1. Arquitectura y Soluciones Implementadas

### A. R Console Styling sin Alteración del DOM Reactivo
- **Problema Anterior**: Intentos previos de mover nodos reactivos de Quarto Live o crear adapters de espejo (`RConsoleAdapter` / `MutationObserver`) producían desincronizaciones y fallos a partir del segundo ejercicio.
- **Solución v0.3.7.4**:
  - Se configuró `display: contents !important;` en `.sr-editor-body > div` y `.sr-editor-body .exercise-cell`.
  - Mediante CSS Flexbox `order`, se estructuró visualmente el panel de código:
    1. `order: 1` $\rightarrow$ Editor CodeMirror 6 (`.card.exercise-editor`)
    2. `order: 2` $\rightarrow$ Barra de herramientas Social R (`.sr-editor-toolbar`: `Ejecutar`, `Enviar respuesta`)
    3. `order: 3` $\rightarrow$ Cabecera de consola (`.sr-console-header`: `R Console`, `Limpiar`, `Colapsar`)
    4. `order: 4` $\rightarrow$ Salida nativa de R (`.cell-output-container` estilizado como consola oscura `#0f172a`, `#38bdf8` stdout, `#f87171` stderr).
  - Los controles nativos de Quarto Live (`Start Over`, `Show Hint`, `Run Code`) se ocultan en modo normal y quedan disponibles con `?debug=1` o `?debug=quarto-live`.

### B. Separación Estricta: RUN vs SUBMIT
- **RUN (`Ctrl + Enter` / Botón `Ejecutar`)**:
  - Sincroniza el código del editor con la celda activa.
  - Ejecuta el código en webR y muestra la salida en R Console (ej. `18 + 11` $\rightarrow$ `[1] 29`).
  - **NUNCA** evalúa criterios pedagógicos, **NUNCA** muestra feedback y **NUNCA** completa el ejercicio.
- **SUBMIT (`Ctrl + Shift + Enter` / Botón `Enviar respuesta`)**:
  - Evalúa el código del estudiante contra las condiciones y diagnósticos definidos en YAML mediante `WebREvaluator` y `WebRGrader`.
  - Renderiza la tarjeta de feedback pedagógico en `#sr-feedback-card-${exerciseId}` en el panel izquierdo (`is-success`, `is-warning`, `is-info`, `is-error`).
  - Si es correcto: guarda estado `status: "completed"`, actualiza el progreso (25%, 50%, 75%, 100%), habilita el botón `Siguiente` en TopBar y hace visible el botón `Continuar` en BottomBar.
  - Si es incorrecto: incrementa intentos (`attempts`), mantiene bloqueada la navegación al siguiente ejercicio.

### C. Invalidación Inmediata de Feedback Obsoleto (Stale Feedback)
- Al escribir o modificar cualquier carácter en CodeMirror, un listener en fase de captura detecta la edición y limpia inmediatamente la tarjeta de feedback previo.

---

## 2. Matriz de Aceptación (14 Puntos)

| # | Criterio de Verificación | Estado | Evidencia / Test |
|---|--------------------------|:------:|------------------|
| 1 | R inicializa correctamente y muestra "R listo" | PASS | `test_checkpoint_a_v0374.py` |
| 2 | Ejecutar 18+11 muestra [1] 29 en consola sin feedback ni progreso | PASS | `01-run-wrong-no-feedback.png` |
| 3 | Enviar 18+11 muestra feedback de advertencia ("El resultado debería ser 30") | PASS | `02-submit-wrong.png` |
| 4 | Enviar 18+12 muestra feedback de éxito ("¡Muy bien! R calculó...") | PASS | `03-submit-correct.png` |
| 5 | Progreso avanza a 25% tras completar Ejercicio 1 | PASS | `03-submit-correct.png` |
| 6 | Botón "Siguiente" se habilita tras completar Ejercicio 1 | PASS | `04-next-enabled.png` |
| 7 | Navegación a Ejercicio 2 funciona sin recarga de página | PASS | `test_navigation_v0374.py` |
| 8 | Ejecutar 25+17 en Ejercicio 2 muestra [1] 42 en consola | PASS | `05-ex2-run-console.png` |
| 9 | Enviar 25+17 en Ejercicio 2 completa y avanza a 50% | PASS | `test_submit_v0374.py` |
| 10 | Enviar 120 en Ejercicio 3 completa y avanza a 75% | PASS | `test_submit_v0374.py` |
| 11 | Ejercicio 4: `edad_promedio <- "21.4"` activa diagnóstico de tipo (texto/comillas) | PASS | `06-ex4-type-feedback.png` |
| 12 | Ejercicio 4: `edad_promedio <- 21.4` completa y avanza a 100% | PASS | `test_submit_v0374.py` |
| 13 | Shortcuts `Ctrl + Enter` (Run) y `Ctrl + Shift + Enter` (Submit) en todos los ejercicios | PASS | `test_shortcuts_v0374.py` |
| 14 | Modificar código en el editor limpia feedback obsoleto | PASS | `test_shortcuts_v0374.py` |

---

## 3. Capturas de Pantalla Generadas

- `docs/screenshots/v0.3.7.4/01-run-wrong-no-feedback.png`
- `docs/screenshots/v0.3.7.4/02-submit-wrong.png`
- `docs/screenshots/v0.3.7.4/03-submit-correct.png`
- `docs/screenshots/v0.3.7.4/04-next-enabled.png`
- `docs/screenshots/v0.3.7.4/05-ex2-run-console.png`
- `docs/screenshots/v0.3.7.4/06-ex4-type-feedback.png`
