# Social R v0.3.6 — Informe Técnico de Arquitectura de Consola Nativa

**Fecha:** 16 de Agosto de 2026  
**Versión:** Social R v0.3.6  
**Build ID:** `v0.3.6-debug-20260816-2030`  
**Estado:**
- **CUSTOM CONSOLE MIRROR REMOVED: YES**
- **NATIVE OUTPUT AS CONSOLE: PASS**
- **EX1 RUN: PASS**
- **EX2 RUN: PASS**
- **EX3 RUN: PASS**
- **EX4 RUN: PASS**
- **CTRL+ENTER ALL: PASS**
- **R ERROR OUTPUT: PASS**
- **SUBMIT REGRESSION: PASS**

---

## 1. Por qué `RConsoleAdapter` Fue Abandonado

Las versiones anteriores intentaron construir una consola propia interceptando eventos, duplicando ejecuciones o usando `MutationObserver` para copiar texto hacia un elemento custom `#sr-console-body`. Esta estrategia introdujo fragilidad y falló al cambiar entre ejercicios.

En **Social R v0.3.6**, se eliminó la capa intermedia `RConsoleAdapter` y se adoptó el principio:
**El output nativo generado por Quarto Live es la única fuente de verdad y la representación visual de la consola.**

---

## 2. Nodo Native Output Real y Posicionamiento Layout

El nodo nativo generado por Quarto Live posee la clase `.cell-output-container` / `.cell-output-container-webr` (o `.cell-output`).

Mediante reglas CSS Grid / Flexbox en [`css/editor-console.css`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/css/editor-console.css):
- El editor CodeMirror 6 ocupa la región superior.
- La barra de herramientas ("Ejecutar", "Enviar respuesta") ocupa la región intermedia.
- La cabecera "R Console" junto con el nodo nativo `.cell-output-container` ocupa físicamente la región inferior.

No existe duplicación ni reparenting de nodos en tiempo de ejecución.

---

## 3. Delegación de Ejecución (Botón "Ejecutar" y `Ctrl + Enter`)

1. **Botón "Ejecutar":** Al presionar el botón de Social R, [`js/social-r.js`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/js/social-r.js) resuelve el contenedor del ejercicio activo (`.social-r-exercise.is-active-exercise`) e invoca `QuartoLiveAdapter.runCode(exerciseId)`.
2. **`QuartoLiveAdapter.runCode()`**: Sincroniza el código del editor con la celda nativa de Quarto Live (`.exercise-cell`) y delega directamente la ejecución al control nativo `a.exercise-editor-btn-run-code`.
3. **`Ctrl + Enter`:** El listener global en fase de captura detecta el atajo y delega directamente a `executeActiveExercise()`, asegurando que `Ctrl + Enter` funcione idénticamente en **TODOS** los ejercicios.

---

## 4. Inspección DOM Real en DevTools

Tras ejecutar `999 + 1` en el Ejercicio 2:
- **Elemento visual:** `<div class="cell-output-container cell-output-container-webr"><div class="cell-output-stdout"><pre><code>[1] 1000</code></pre></div></div>`
- **Contenedor ancestro:** `.social-r-exercise[data-exercise-id="intro-r-01-001"]`
- **Pertenece a output nativo:** **SÍ (100% Nativo Quarto Live)**.

---

## 5. Entorno de Ejecución Real (Runtime Environment)

`Quarto Live isolated R environment per exercise`. Cada celda de ejercicio posee su propio entorno R aislado (`exercise-env-${exerciseId}`) nativo de Quarto Live.

---

## 6. Capturas de Evidencia Registradas (`docs/screenshots/v0.3.6/`)

1. [`02-ex2-native-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.6/02-ex2-native-console.png): **Evidencia Crítica:** Ejercicio 2 con editor (`999 + 1`) y región R Console mostrando nativamente `[1] 1000` sin duplicados.
2. [`03-ex3-native-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.6/03-ex3-native-console.png): Ejercicio 3 con editor (`4321 + 1234`) y región R Console mostrando nativamente `[1] 5555`.
3. [`04-r-error-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.6/04-r-error-console.png): Captura de error nativo de R (`variable_no_existe`) proyectado en la región R Console.

---

## 7. Pendientes para v0.3.7

- Historial acumulativo tipo terminal (posterga a v0.3.7).
- Command prompt custom `>`.
