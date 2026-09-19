# Social R v0.3.5 — Informe Técnico de Enrutamiento y Presentación de R Console

**Fecha:** 16 de Agosto de 2026  
**Versión:** Social R v0.3.5  
**Build ID:** `v0.3.5-debug-20260816-2030`  
**Estado:**
- **REAL R OUTPUT → CONSOLE: PASS**
- **TOP NATIVE OUTPUT HIDDEN: PASS**
- **CONSOLE HISTORY: PASS**
- **R ERRORS: PASS**
- **R WARNINGS: PASS**
- **R ENVIRONMENT: PASS**
- **RUN VS SUBMIT SEPARATION: PASS**

---

## 1. Problema Anterior Identificado

En la versión v0.3.4, la evaluación real de R funcionaba, pero el resultado (como `[1] 42`) se desplegaba en el área superior nativa de Quarto Live inmediatamente debajo del editor CodeMirror. La `R Console` inferior se mantenía inactiva o duplicaba información.

---

## 2. Solución y Enrutamiento (3 Canales Separados)

Se formalizaron tres canales estrictamente desacoplados:

1. **Editor Panel (Superior):** Contiene únicamente código R (CodeMirror 6), números de línea, resaltado de sintaxis y cursor. Salidas nativas y controles de debugging de Quarto Live quedan ocultos en modo normal.
2. **R Console Panel (Inferior):** Recibe comandos (`> code`), stdout (`[1] 42`, outputs de `cat()` y `print()`), stderr (`Error: ...`), warnings (`Warning message:`), y mensajes (`message()`). Acumula historial continuo.
3. **Pedagogical Feedback Panel (Izquierdo):** Recibe exclusivamente las evaluaciones formales del Submit/Grader (`Correcto`, `Revisa tu respuesta`, diagnósticos prioritarios y pistas).

---

## 3. Arquitectura del `RConsoleAdapter`

Se implementó el componente `RConsoleAdapter` ([`js/platform/r-console-adapter.js`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/js/platform/r-console-adapter.js)):

```text
       CodeMirror 6
            │
            ▼
   QuartoLiveAdapter.runCode() / submitCode()
            │
            ▼
       webR.Shelter (captureR)
            │
            ├── stdout / stderr / output stream
            │
            ▼
      RConsoleAdapter
      ├── processResult(code, stdout, stderr)
      ├── appendCommand(code) ──► `> 25 + 17` (Grafito oscuro)
      ├── appendOutput(text)  ──► `[1] 42` (Grafito sobrio)
      ├── appendError(text)   ──► `Error: object 'x' not found` (Rojo sobrio)
      ├── appendWarning(text) ──► `Warning: NaNs produced` (Ámbar sobrio)
      └── appendMessage(text) ──► `test-message` (Gris en cursiva)
```

---

## 4. Comportamiento R Nativo Formalizado

- **Asignaciones de Variables:** Ejecutar `x <- 10` produce en la consola únicamente `> x <- 10` (sin imprimir `[1] 10` espurio). Consultar `x` a continuación produce `[1] 10`.
- **Exploración Libre:** Expresiones como `mean(c(10, 20, 30))` producen `[1] 20` en la consola sin activar la calificación pedagógica ni alterar el progreso del módulo.
- **Limpiar Consola:** El botón **Limpiar** vacía el historial de la pantalla HTML pero **NO borra las variables ni reinicia el motor R**.
- **Colapsar Consola:** El botón **Colapsar** oculta visualmente el panel inferior ampliando el editor; al expandir nuevamente, el historial permanece intacto.

---

## 5. Capturas de Evidencia Registradas (`docs/screenshots/v0.3.5/`)

1. [`01-console-empty.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/01-console-empty.png): Consola inicial limpia (sin texto desactualizado).
2. [`02-run-25-17-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/02-run-25-17-console.png): **Evidencia Crítica:** Editor con `25 + 17` SIN output `[1] 42` debajo; `R Console` muestra `> 25 + 17` y `[1] 42`.
3. [`03-history-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/03-history-console.png): Historial continuo en R Console (`483 + 217` -> `[1] 700`).
4. [`04-assignment-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/04-assignment-console.png): Asignación de variables (`social_r_test <- 12345`) y consulta posterior (`[1] 12345`).
5. [`05-r-error-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/05-r-error-console.png): Error nativo de R (`Error: object 'social_r_variable_that_does_not_exist' not found`).
6. [`06-warning-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/06-warning-console.png): Warning nativo de R (`sqrt(-1)` -> `Warning message: NaNs produced`).
7. [`07-submit-incorrect.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/07-submit-incorrect.png): Submit incorrecto (`25 + 16`) con output en consola y feedback de advertencia en panel izquierdo.
8. [`08-submit-correct.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.5/08-submit-correct.png): Submit correcto (`25 + 17`) con output en consola y feedback de éxito en panel izquierdo.

---

## 6. Veredicto Final

```text
Social R v0.3.5 — REAL R CONSOLE

REAL R OUTPUT → CONSOLE: PASS
TOP NATIVE OUTPUT HIDDEN: PASS
CONSOLE HISTORY: PASS
R ERRORS: PASS
R WARNINGS: PASS
R ENVIRONMENT: PASS
RUN VS SUBMIT SEPARATION: PASS
```
