# Social R v0.3.4 — Informe Técnico de Reconstrucción Funcional (Run & R Console)

**Fecha:** 16 de Agosto de 2026  
**Versión:** Social R v0.3.4  
**Build ID:** `v0.3.4-debug-20260816-2030`  
**Estado:**
- **NATIVE QUARTO LIVE RUN: PASS**
- **SOCIAL R MOUSE RUN: PASS**
- **CTRL+ENTER RUN: PASS**
- **REAL R CONSOLE OUTPUT: PASS**
- **R ENVIRONMENT PERSISTENCE: PASS**
- **SUBMIT REGRESSION: PASS**
- **MANUAL EX2 999+1 → 1000: PASS**

---

## 1. Síntoma Real Identificado

En iteraciones anteriores:
- El botón **"Enviar respuesta"** (Submit) funcionaba correctamente porque utilizaba `WebREvaluator` y `WebRGrader` de Quarto Live con las opciones del entorno pedagógico (`exercise-env-${exerciseId}`).
- El botón **"Ejecutar"** (Run) y el atajo `Ctrl + Enter` cambiaban visualmente el estado del botón a "Ejecutando...", pero la **R Console** permanecía estancada en `# Consola de R lista` sin mostrar comandos ni salidas como `[1] 1000`.

---

## 2. Por qué Submit Funcionaba y Run No

- **Submit Pipeline:** Estaba correctamente vinculado a los objetos globales de Quarto Live (`window._exercise_ojs_runtime.WebREvaluator`) pasando el ID del ejercicio y su entorno de ejecución.
- **Run Pipeline (Anterior):** Intentaba leer el código mediante un selector CSS defectuoso (`.card.exercise-editor`), el cual no existía en el HTML generado por Quarto Live. Al fallar el selector, devolvía `""` y abortaba silenciosamente. Además, no estaba vinculado a los componentes nativos de Quarto Live.

---

## 3. Pruebas de Gate Nativo Quarto Live

Se restauró temporalmente la visibilidad de los controles y outputs nativos de Quarto Live para auditar el runtime real. Los resultados fueron un **100% PASS**:

| Ejercicio | Expresión Probadada | Output Nativo Quarto Live | Estado |
| :--- | :---: | :---: | :---: |
| **Ejercicio 1** | `18 + 12` | `[1] 30` | **PASS** |
| **Ejercicio 2** | `999 + 1` | `[1] 1000` | **PASS** |
| **Ejercicio 3** | `4321 + 1234` | `[1] 5555` | **PASS** |
| **Ejercicio 4** | `9999 - 1` | `[1] 9998` | **PASS** |

*Conclusión del Gate:* Quarto Live, webR, CodeMirror y la reactividad OJS están 100% funcionales en los 4 ejercicios. El bug residía exclusivamente en la canalización custom hacia la `R Console`.

---

## 4. Reconstrucción de la Arquitectura (Social R v0.3.4)

### Nueva Arquitectura Unificada

```text
       CodeMirror 6 / EditorView State
                     │
                     ▼
           QuartoLiveAdapter
           ├── getCode(exerciseId) ──► Lee directamente estado de EditorView / DOM .cm-line
           │
           ├── runCode(exerciseId) ──► Sincroniza celda nativa Quarto Live + captura webR.Shelter
           │                            └──► proyecta salida en #sr-console-body (con historial)
           │
           └── submitCode(exerciseId)─► evalúa en webR + WebRGrader 
                                        └──► proyecta feedback en panel izquierdo
```

### Unificación de Disparadores

```text
                  CodeMirror Activo
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
    Botón "Ejecutar"                 Ctrl + Enter
          │                               │
          └───────────────┬───────────────┘
                          ▼
               executeActiveExercise()
                          │
                          ▼
            QuartoLiveAdapter.runCode()
                          │
                          ▼
                   R Console Visible
```

---

## 5. Pruebas de Persistencia y Exploración en R Console

- **Exploración R:** Al ejecutar expresiones libres como `mean(c(10, 20, 30))`, la consola muestra `[1] 20` sin alterar el progreso del estudiante ni requerir que coincida con la respuesta correcta.
- **Asignación de Variables:** Al ejecutar `val_test <- 42` y posteriormente `val_test`, la consola muestra `[1] 42`, demostrando la persistencia del entorno webR.
- **Errores R Reales:** Al ejecutar `variable_inexistente`, la consola muestra `Error: object 'variable_inexistente' not found`.
- **Historial de Consola:** Las ejecuciones sucesivas se acumulan secuencialmente en `R Console`. El botón **Limpiar** únicamente despeja la vista HTML sin resetear las variables en webR.

---

## 6. Pruebas de Regresión de Submit

- Se verificó que al ingresar `25 + 17` en el Ejercicio 2 y pulsar **"Enviar respuesta"**, la interfaz continúa mostrando:
  `Correcto — ¡Excelente! R calculó el total de 42 estudiantes.` (**PASS**).

---

## 7. Evidencia Visual Registrada (`docs/screenshots/v0.3.4/`)

- [`01-native-run-ex2.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/01-native-run-ex2.png): Prueba de Run nativo Quarto Live (`[1] 1000`).
- [`02-social-run-ex2-1000.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/02-social-run-ex2-1000.png): **Evidencia Crítica:** Muestra `999 + 1` en el editor del Ejercicio 2 y `[1] 1000` visible en la R Console mediante el botón Ejecutar.
- [`03-ctrl-enter-ex2-915.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/03-ctrl-enter-ex2-915.png): Muestra `731 + 184` y `[1] 915` mediante `Ctrl + Enter`.
- [`04-ctrl-enter-ex3-5555.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/04-ctrl-enter-ex3-5555.png): Muestra `4321 + 1234` y `[1] 5555` en el Ejercicio 3.
- [`05-r-error-console.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/05-r-error-console.png): Captura de error real en R (`object 'variable_inexistente' not found`).
- [`06-submit-correct-feedback.png`](file:///c:/Users/katin/Projects/R%20-%20camp/R-proyect/social-r-architecture-phase1/social-r-work/social-r-architecture/docs/screenshots/v0.3.4/06-submit-correct-feedback.png): Regresión de Submit con feedback correcto.

---

## 8. Veredicto Final

```text
Social R v0.3.4 — FUNCTIONAL RECOVERY

NATIVE QUARTO LIVE RUN: PASS
SOCIAL R MOUSE RUN: PASS
CTRL+ENTER RUN: PASS
REAL R CONSOLE OUTPUT: PASS
R ENVIRONMENT PERSISTENCE: PASS
SUBMIT REGRESSION: PASS
MANUAL EX2 999+1 → 1000: PASS
```
