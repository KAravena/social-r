# Social R v0.3.3 HOTFIX — Informe Técnico de Causa Raíz y Solución Definitiva de Atajos de Teclado (Ctrl+Enter)

**Fecha:** 16 de Agosto de 2026  
**Versión:** Social R v0.3.3-HOTFIX  
**Estado:**
- **ROOT CAUSE IDENTIFIED: YES**
- **CTRL+ENTER ALL EXERCISES: PASS**
- **CTRL+SHIFT+ENTER ALL EXERCISES: PASS**
- **ACTIVE EDITOR RESOLUTION: PASS**
- **E2E KEYBOARD TESTS: PASS**

---

## 1. Síntoma Registrado Manualmente

En versiones anteriores, al interactuar manualmente con el workspace:
- En el **Ejercicio 1** (`intro-r-01-000`), hacer clic en el editor, escribir `18 + 12` y presionar `Ctrl + Enter` ejecutaba el código correctamente produciendo `[1] 30` en la consola de R.
- En el **Ejercicio 2** (`intro-r-01-001`), la interfaz permitía hacer clic y editar normalmente dentro de CodeMirror (por ejemplo escribiendo `25 + 17` o `999 + 1`). Sin embargo, al presionar `Ctrl + Enter`, **no ocurría nada**: no se enviaba ejecución a webR, no cambiaba la consola de R y la salida permanecía vacía.
- El mismo fallo se replicaba en los Ejercicios 3 y 4.

---

## 2. Pasos Exactos de Reproducción

1. Abrir la plataforma en el navegador (`http://localhost:4200/`).
2. Navegar al Ejercicio 2 ("Modificar una operación") utilizando la barra superior de navegación.
3. Hacer clic dentro del editor CodeMirror del Ejercicio 2.
4. Reemplazar el código por `999 + 1`.
5. Presionar la combinación física `Ctrl + Enter`.
6. Observar que la consola de R no responde ni muestra `[1] 1000`.

---

## 3. Causa Raíz Técnica Exacta

### A. Selector DOM Erróneo en la Extracción de Código (`getCode`)
En `QuartoLiveAdapter.getCode(exerciseId)`, la función buscaba el elemento del editor utilizando el selector:
```javascript
// CÓDIGO ANTERIOR CON BUG
const editorCard = container.querySelector(".card.exercise-editor");
```
Sin embargo, **Quarto Live NO añade la clase `.exercise-editor` a la tarjeta del editor** en la estructura HTML renderizada (solo genera contenedores con clases `.sr-editor-body`, `.exercise-cell`, `.cm-editor` o `.card`).  
Debido a esta discrepancia:
- `editorCard` evaluaba a `null` para los ejercicios 2, 3 y 4.
- `getCode(exerciseId)` devolvía una cadena vacía `""`.
- `runCode(exerciseId)` ejecutaba la guarda de seguridad `if (!code || !code.trim()) return;` **abortando silenciosamente la ejecución** antes de llegar a webR.

### B. Intercepción en la Fase de Burbuja por CodeMirror 6
CodeMirror 6 registra keymaps internos para `Mod-Enter`. Cuando el escuchador global de teclado está configurado en la fase normal de burbuja (bubble phase), el handler interno de CodeMirror intercepta la pulsación dentro del elemento editable e invoca `e.stopPropagation()`, impidiendo que el evento llegue a los escuchadores del `document`.

---

## 4. Por qué los Tests Anteriores No Detectaron el Problema

1. **Simulación Superficial mediante DOM HTML Directo (`cm.innerHTML`)**:  
   Los tests E2E previos inyectaban HTML directamente en `.cm-content` e invocaban programáticamente métodos simulados. Al no realizar la simulación mediante eventos reales de teclado (`ActionChains` de Selenium o `keyboard.press` de Playwright), no replicaban el flujo de foco y propagación de eventos real que ocurre cuando un usuario físico presiona las teclas.
2. **Evaluación de Variables Internas de OJS**:  
   Los scripts de test leían `card.parentElement.value.code`, el cual contenía el valor inicial inyectado por Quarto Live al cargar el primer ejercicio, generando un falso positivo en la suite de pruebas.

---

## 5. Comparativa Arquitectónica (Diagramas)

### Arquitectura Anterior (Con Bug)
```text
Usuario presiona Ctrl+Enter en Ejercicio 2
                   │
                   ▼
  CodeMirror 6 (e.stopPropagation) ──► Evento bloqueado
                   │ (Si continuaba)
                   ▼
   QuartoLiveAdapter.getCode("intro-r-01-001")
                   │
                   ▼
container.querySelector(".card.exercise-editor") ──► null
                   │
                   ▼
            devuelve "" ──► ABORTA SILENCIOSAMENTE
```

### Nueva Arquitectura Unificada (Social R v0.3.3 HOTFIX)
```text
Usuario presiona Ctrl+Enter en cualquier ejercicio
                           │
                           ▼
     [window.addEventListener("keydown", handler, true)]  ◄── CAPTURE PHASE!
                           │
                           ▼
                 getActiveExerciseId()
                 ├── 1. document.activeElement.closest('.social-r-exercise')
                 ├── 2. .social-r-exercise.is-active-exercise
                 └── 3. Navigation fallback index
                           │
                           ▼
               executeActiveExercise()
                           │
                           ▼
      QuartoLiveAdapter.getCode(exerciseId)
      (container.querySelector(".sr-editor-body") || container)
                           │
                           ▼
              Lee líneas .cm-line reales
                           │
                           ▼
          webR Evaluator ──► Consola de R: [1] 1000
```

---

## 6. Matriz Final de Resultados E2E (16 / 16 PASS)

Se ejecutó la suite E2E completa [`tests/test_v033_hotfix_full.py`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/tests/test_v033_hotfix_full.py) simulan pulsaciones físicas reales de teclado (`ActionChains`):

| Ejercicio | Botón Ejecutar | Atajo Ctrl+Enter | Botón Enviar Respuesta | Atajo Ctrl+Shift+Enter | Estado Global |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ejercicio 1** (`intro-r-01-000`) | **PASS** | **PASS** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 2** (`intro-r-01-001`) | **PASS** | **PASS (999+1 → 1000)** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 3** (`intro-r-01-002`) | **PASS** | **PASS (Objeto creado)** | **PASS** | **PASS** | **PASS (4/4)** |
| **Ejercicio 4** (`intro-r-01-003`) | **PASS** | **PASS (Objeto creado)** | **PASS** | **PASS** | **PASS (4/4)** |

**Prueba de Navegación Cíclica (1 → 2 → 3 → 4 → 3 → 2 → 1):** **PASS**  
**Resultado Global:** **16 / 16 PASSED**

---

## 7. Evidencia Visual Registrada (`docs/screenshots/v0.3.3-hotfix/`)

- [`01-ex1-keyboard-run.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3-hotfix/01-ex1-keyboard-run.png): Ejecución de `18 + 12` vía teclado en Ejercicio 1.
- [`02-ex2-keyboard-run-1000.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3-hotfix/02-ex2-keyboard-run-1000.png): **Evidencia Crítica:** Muestra explícitamente `999 + 1` en el editor 2 y `[1] 1000` impreso en la consola de R.
- [`03-ex3-keyboard-run.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3-hotfix/03-ex3-keyboard-run.png): Asignación y evaluación del objeto `numero_estudiantes <- 120`.
- [`04-ex4-keyboard-run.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.3-hotfix/04-ex4-keyboard-run.png): Asignación y evaluación del objeto `edad_promedio <- 21.4`.

---

## 8. Veredicto Final

```text
Social R v0.3.3 HOTFIX

ROOT CAUSE IDENTIFIED: YES
CTRL+ENTER ALL EXERCISES: PASS
CTRL+SHIFT+ENTER ALL EXERCISES: PASS
ACTIVE EDITOR RESOLUTION: PASS
E2E KEYBOARD TESTS: PASS
```
