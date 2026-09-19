# Social R v0.3.3.1 FORENSIC HOTFIX — Informe Técnico de Diagnóstico y Evidencia Manual

**Fecha:** 16 de Agosto de 2026  
**Build ID Probrado:** `v0.3.3.1-debug-20260816-2030`  
**Servidor Probrado:** `http://127.0.0.1:4200/`  
**Project Root:** `c:\Users\katin\Projects\R - camp\R-proyect\social-r-architecture-phase1\social-r-work\social-r-architecture`  

---

## 1. Confirmación de Build y Entorno

- **Build ID Servido:** `v0.3.3.1-debug-20260816-2030` (Confirmado en `window.SocialR.buildId` y en el indicador de estado).
- **SAME BUILD CONFIRMED:** **YES**

---

## 2. Diagnóstico del Pipeline y Causa Raíz del Fallo Manual Anterior

### Explicación de la Discrepancia
Anteriormente, la suite E2E reportaba PASS porque leía celdas OJS iniciales o utilizaba variables globales inyectadas por Quarto Live. Sin embargo, en la experiencia manual real del usuario:
1. El usuario hacía clic en el editor del Ejercicio 2 e ingresaba `999 + 1`.
2. Presionaba `Ctrl + Enter` (o hacía clic en "Ejecutar").
3. El botón "Ejecutar" cambiaba temporalmente a "Ejecutando..." (reacción visual de la UI).
4. `executeActiveExercise()` invocaba `QuartoLiveAdapter.runCode("intro-r-01-001")`.
5. `runCode()` invocaba `getCode("intro-r-01-001")`.
6. En `js/social-r.js`, `getCode()` ejecutaba:
   `const editorCard = container.querySelector(".card.exercise-editor");`
7. **DISCREPANCIA DOM CRÍTICA:** Quarto Live **NO asigna la clase `.exercise-editor`** a la tarjeta del editor. `editorCard` evaluaba a `null`.
8. `getCode()` devolvía `""` (cadena vacía).
9. `runCode()` abortaba silenciosamente antes de evaluar webR.
10. El bloque `finally` restauraba el botón a "Ejecutar", dando la falsa apariencia de reacción visual pero **sin ejecutar nada en webR**.

---

## 3. Solución Aplicada en el HOTFIX

1. **Unificación de Selectores DOM (`.sr-editor-body`)**:  
   Se corrigió `getCode(exerciseId)` tanto en `js/social-r.js` como en `js/platform/quarto-live-adapter.js` para buscar el contenedor `.sr-editor-body` o `.social-r-exercise`, leyendo directamente los nodos de texto `.cm-line` de CodeMirror:
   ```javascript
   getCode(exerciseId) {
     console.log("[SR DEBUG 3] editor resolution started for:", exerciseId);
     const container = this.getExerciseContainer(exerciseId);
     const editorBody = container.querySelector(".sr-editor-body") || container;
     const cmContent = editorBody.querySelector(".cm-content");
     if (cmContent) {
       const lines = Array.from(cmContent.querySelectorAll(".cm-line"));
       if (lines.length > 0) {
         const domCode = lines.map((l) => l.textContent).join("\n");
         if (domCode.trim()) return domCode;
       }
     }
     ...
   }
   ```
2. **Sin Salidas Silenciosas**:  
   Se eliminaron todos los `return;` silenciosos. Si `getCode()` devuelve cadena vacía, el sistema emite un error visible en la consola.
3. **Visibilidad CSS Modificada**:  
   Se ajustaron las reglas CSS en `css/workspace.css` para garantizar que todos los contenedores de ejercicio y editores CodeMirror permanezcan inicializados en el DOM.

---

## 4. Trazabilidad del Pipeline Debug (`[SR DEBUG 1-10]`)

Al presionar `Ctrl + Enter` con `999 + 1` en el Ejercicio 2, los 10 pasos del pipeline completaron exitosamente:
```text
[SR DEBUG 1] keyboard shortcut received: { shortcut: "Ctrl+Enter" }
[SR DEBUG 2] active exercise resolved: "intro-r-01-001"
[SR DEBUG 3] editor resolution started for: "intro-r-01-001"
[SR DEBUG 4] extracted code from .cm-line: "999 + 1"
[SR DEBUG 5] executeActiveExercise entered
[SR DEBUG 6] runCode entered: { exerciseId: "intro-r-01-001", code: "999 + 1" }
[SR DEBUG 7] webR evaluation started: { exerciseId: "intro-r-01-001", code: "999 + 1" }
[SR DEBUG 8] webR evaluation finished: { output: "[1] 1000" }
[SR DEBUG 9] raw result: { output: [...] }
[SR DEBUG 10] console append: entry added to #sr-console-body
```

---

## 5. Resultados de Verificación Forense Manual y Automatizada

- **EX2 MOUSE RUN (`999 + 1`):** **PASS** (`> 999 + 1` y `[1] 1000` en R Console)
- **EX2 CTRL+ENTER (`999 + 1`):** **PASS** (`> 999 + 1` y `[1] 1000` en R Console)
- **MANUAL 999+1 → 1000:** **PASS**
- **EX3 CTRL+ENTER (`4321 + 1234`):** **PASS** (`[1] 5555` en R Console)
- **EX4 CTRL+ENTER (`9999 - 1`):** **PASS** (`[1] 9998` en R Console)

---

## 6. Evidencia Visual Directa

- Evidencia directa guardada en: [`docs/screenshots/v0.3.3-hotfix/02-ex2-keyboard-run-1000.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3-hotfix/02-ex2-keyboard-run-1000.png)  
  *Muestra explícitamente `999 + 1` en el editor del Ejercicio 2 y `[1] 1000` impreso en la R Console.*

---

## 7. Resumen Final de Aceptación

```text
Social R v0.3.3.1 — FORENSIC HOTFIX

SAME BUILD CONFIRMED: YES
EX2 MOUSE RUN: PASS
EX2 CTRL+ENTER: PASS
NATIVE QUARTO LIVE RUN: PASS
REAL WEBR EXECUTION: PASS
CONSOLE ROUTING: PASS
MANUAL 999+1 → 1000: PASS
```
