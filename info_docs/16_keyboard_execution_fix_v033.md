# Social R v0.3.3 — Informe de Resolución Crítica de Atajos de Teclado (Run / Submit)

**Fecha:** 16 de Agosto de 2026  
**Versión:** Social R v0.3.3  
**Evaluación Global:**
- **ACTIVE EDITOR RESOLUTION: PASS**
- **KEYBOARD RUN QA: PASS** (Ctrl+Enter funcional en el 100% de los ejercicios)
- **KEYBOARD SUBMIT QA: PASS** (Ctrl+Shift+Enter funcional en el 100% de los ejercicios)
- **BUTTON QA: PASS** (Botones Ejecutar y Enviar respuesta enrutados al mismo pipeline centralizado)

---

## 1. Bug Observado Inicialmente

Al comenzar la sesión, el atajo `Ctrl + Enter` funcionaba únicamente en el primer ejercicio (Ejercicio 1: `intro-r-01-000`). Al navegar al Ejercicio 2 (`intro-r-01-001`), Ejercicio 3 (`intro-r-01-002`) o Ejercicio 4 (`intro-r-01-003`), al presionar `Ctrl + Enter` dentro del editor CodeMirror no ocurría nada y la consola de R permanecía vacía o ejecutaba la celda del primer ejercicio.

---

## 2. Causa Raíz Exacta

1. **Intercepción de Eventos en CodeMirror 6**:  
   Quarto Live registra una extensión interna en CodeMirror 6 con un keymap para la combinación `Mod-Enter` (`Ctrl+Enter`). Cuando el foco reside dentro de `.cm-content` en los ejercicios 2, 3 y 4, el listener de CodeMirror intercepta el evento de teclado y ejecuta `e.stopPropagation()`, impidiendo que el evento escuche en la fase de burbuja (bubble phase) en `window.addEventListener("keydown")`.

2. **Falta de Descodificación Dinámica del Ejercicio Activo**:  
   El resolver anterior leía `window.SocialR.navigation.getCurrentExercise()` que dependía únicamente del índice de navegación guardado, sin inspeccionar cuál era el contenedor `.social-r-exercise` o el editor `.cm-content` que tenía el foco activo (`document.activeElement`).

3. **Inconsistencia en los Botones**:  
   Los botones de la interfaz invocaban selectores directos sin pasar por un pipeline unificado con los atajos de teclado.

---

## 3. Solución Arquitectónica Implementada

### A. Intercepción en Fase de Captura (Capture-Phase Listener)
Se registró el listener global de teclado utilizando `useCapture = true`:
```javascript
window.addEventListener("keydown", (e) => {
  const isMac = navigator.platform.toUpperCase().indexOf("MAC") >= 0;
  const ctrlOrCmd = isMac ? e.metaKey : e.ctrlKey;
  const isEnterKey = e.key === "Enter" || e.key === "NumpadEnter" || e.keyCode === 13;

  if (ctrlOrCmd && e.shiftKey && isEnterKey) {
    e.preventDefault();
    e.stopPropagation();
    submitActiveExercise();
    return;
  }

  if (ctrlOrCmd && !e.shiftKey && isEnterKey) {
    e.preventDefault();
    e.stopPropagation();
    executeActiveExercise();
    return;
  }
}, true); // useCapture = true intercepta el evento ANTES que CodeMirror lo consuma
```

### B. Servicio Único de Resolución Dinámica (`getActiveExerciseId`)
El sistema resuelve el ejercicio activo mediante la siguiente jerarquía de prioridad:
1. `document.activeElement.closest('.social-r-exercise')` (Si el estudiante tiene el cursor dentro de un editor o panel de un ejercicio).
2. `.social-r-exercise.is-active-exercise` (El contenedor actualmente visible en la SPA).
3. `window.SocialR.navigation.getCurrentExercise().id` (Fallback al gestor de navegación).

### C. Unificación de Pipelines (Run / Submit)
Tanto los botones como los atajos de teclado consumen **exactamente el mismo servicio**:
```text
Botón "Ejecutar"        ──────┐
                              ├─► executeActiveExercise() ──► adapter.runCode(activeId)
Atajo "Ctrl + Enter"    ──────┘

Botón "Enviar respuesta"─────┐
                              ├─► submitActiveExercise()  ──► adapter.submitCode(activeId)
Atajo "Ctrl+Shift+Enter"─────┘
```

---

## 4. Matriz Final de Resultados E2E (4 × 4)

Se ejecutó la suite E2E automatizada [`tests/test_v033_shortcuts_all.py`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/tests/test_v033_shortcuts_all.py) probando los 4 canales de interacción en los 4 ejercicios:

| Ejercicio | Botón Ejecutar | Atajo Ctrl+Enter | Botón Enviar Respuesta | Atajo Ctrl+Shift+Enter | Estado Global |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ejercicio 1** (`intro-r-01-000`) | **PASS** | **PASS** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 2** (`intro-r-01-001`) | **PASS** | **PASS** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 3** (`intro-r-01-002`) | **PASS** | **PASS** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 4** (`intro-r-01-003`) | **PASS** | **PASS** | **PASS** | **PASS** | **PASS (4/4)** |

**Navegación Ida y Vuelta (Re-Test):** **PASS**  
**Total de Aserciones E2E:** **16 / 16 PASSED**

---

## 5. Capturas de Pantalla Guardadas (`docs/screenshots/v0.3.3/`)

- [`exercise-1-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3/exercise-1-console.png): Ejecución de `18 + 12` vía teclado en Ejercicio 1.
- [`exercise-2-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3/exercise-2-console.png): Ejecución de `25 + 17` vía teclado en Ejercicio 2.
- [`exercise-3-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3/exercise-3-console.png): Ejecución de `numero_estudiantes <- 120` silenciosa vía teclado en Ejercicio 3.
- [`exercise-4-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3/exercise-4-console.png): Ejecución de `edad_promedio <- 21.4` vía teclado en Ejercicio 4.

---

## 6. Veredicto Final

```text
Social R v0.3.3

ACTIVE EDITOR RESOLUTION: PASS
KEYBOARD RUN QA: PASS
KEYBOARD SUBMIT QA: PASS
BUTTON QA: PASS
```
