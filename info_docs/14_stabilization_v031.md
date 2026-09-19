# Social R v0.3.1 — Informe de Estabilización Funcional y Refinamiento Visual Profesional

**Fecha de ejecución:** 16 de Agosto de 2026  
**Versión de la plataforma:** Social R v0.3.1 (Stabilization & Professional Visual Refinement)  
**Entorno de ejecución:** Quarto Live + webR (WebAssembly) + CodeMirror 6 + Headless Edge Automated QA Engine  
**Resultado Global:**
- **FUNCTIONAL QA: PASS** (19/19 verificaciones interactivas en navegador real superadas con 0 fallos)
- **VISUAL QA: PASS** (Iconografía sobria sin emojis, tipografía del sistema, paleta neutra, 0 scroll global)

---

## 1. Problemas Encontrados y Diagnóstico de Causa Raíz

En la auditoría profunda de la interacción real del navegador, se identificaron cuatro desconexiones críticas entre la interfaz visual y el runtime WebAssembly:

| ID | Síntoma / Problema Observado | Causa Técnica Raíz | Corrección Implementada |
| :--- | :--- | :--- | :--- |
| **BUG-01** | `Ejecutar código` no enviaba salida a la consola ni evaluaba en webR. | `QuartoLiveAdapter` despachaba eventos DOM simulados (`CustomEvent('input')`) a contenedores sin listeners vinculados a la API de evaluación. | Integración directa con el objeto `webR` WebAssembly expuesto en el scope de Observable (`window._ojs.ojsConnector.mainModule._scope.get('webROjs')._value.webRPromise`), ejecutando código exploratorio con `shelter.captureR(code, { withAutoprint: true })` y formateando `stdout`/`stderr` en `#sr-console-body`. |
| **BUG-02** | `Enviar respuesta` no capturaba el contenido actual de CodeMirror ni ejecutaba el árbol diagnóstico estructurado. | No existía extracción real de texto desde los nodos `.cm-content` / `.cm-line` de CodeMirror 6 hacia la instancia de `WebRGrader`. | Implementación de `getCode(exerciseId)` que extrae las líneas exactas del editor activo y las pasa directamente a `WebREvaluator` y `WebRGrader`, parseando las clases de feedback (`alert-success`, `alert-warning`, `alert-info`, `alert-danger`) de manera no bloqueante. |
| **BUG-03** | El estado `R listo` se mostraba mediante un timeout artificial de 3.2s sin confirmar la inicialización del kernel. | `initShell()` usaba un contador de intervalos fijo (`checks > 8`). | Detección asíncrona real vinculada a la resolución de `window.SocialR.adapter.getWebR()`, cambiando el indicador a `R listo` únicamente cuando el worker de WebAssembly está 100% operativo. |
| **BUG-04** | Estética sobrecargada, con emojis decorativos (`📊`, `💡`, `🔓`, `✓`, `▶`), cajas anidadas innecesarias y control `Dev` visible para estudiantes. | Residuos de prototipado rápido en las plantillas del generador y en el bundle CSS. | Eliminación total de emojis, simplificación de la TopBar (46px), ocultación de `Dev Mode` salvo activación intencional (`?dev=true` o localStorage), tipografía del sistema (`Inter` / `ui-monospace`) y rediseño de botones a estilos sobrios y legibles. |

---

## 2. Archivos Modificados

1. **`js/platform/quarto-live-adapter.js`**:
   - `getWebR()`: Conexión asíncrona directa con la promesa `webROjs.webRPromise`.
   - `getCode(exerciseId)`: Extracción fidedigna de código desde `.cm-content` / `.cm-line`.
   - `run(exerciseId)`: Ejecución exploratoria en WebAssembly con captura de stdout/stderr y proyección en consola R sin calificar.
   - `submit(exerciseId)`: Evaluación diagnóstica con `WebREvaluator` y `WebRGrader`, renderizado de tarjeta de feedback sobria (`is-success`, `is-warning`, `is-info`, `is-error`), actualización de `LocalProgressStore` y desbloqueo de navegación.
   - `reset(exerciseId)`: Restauración de starter code, limpieza de feedback y reset de consola.
   - `revealNextHint(exerciseId)` & `revealSolution(exerciseId)`: Revelación progresiva estructurada (`Pista 1 de N` -> `Pista 2 de N` -> `Ver solución`).
2. **`js/social-r.js`**:
   - Integración unificada del master engine sin dependencias rotas ni stubs duplicados.
   - Enlace reactivo del estado de webR en la TopBar (`R listo` / `Iniciando R...` / `Error al iniciar R`).
   - Sincronización de progreso (`LocalProgressStore`) con persistencia en localStorage y renderizado de la barra de avance inferior (`25%`, `50%`, `75%`, `100%`).
   - Atajos de teclado: `Ctrl+Enter` (Ejecutar), `Ctrl+Shift+Enter` (Enviar), `Alt+P` (Pistas), `Alt+←/→` (Navegación).
3. **`engine/generator/build.py`**:
   - Eliminación total de iconografía basada en emojis.
   - Limpieza de microcopy a un tono académico y sobrio.
   - Generación de markup estructurado para layout full-screen sin scroll global.
4. **`css/app-shell.css`**, **`css/workspace.css`**, **`css/lesson-panel.css`**, **`css/editor-console.css`**:
   - Centralización de tokens de diseño sobrios (paleta slate/azul neutro).
   - Eliminación de mitades rígidas 50/50: panel pedagógico flexible (explicación auto-ajustable con `max-height: 55%` e instrucciones fluidas).
   - Botones con jerarquía visual sobria (`Reiniciar` = tertiary, `Ejecutar` = secondary, `Enviar respuesta` = primary).
   - Consola R con prompt `>`, colores de texto suaves (`#86efac` stdout, `#f87171` stderr, `#94a3b8` prompt).
5. **`_quarto.yml`**:
   - Inclusión de recursos estáticos `resources: [css, js]` para distribución limpia en `_site/`.
6. **`tests/test_generator.py`**:
   - Actualización de aserciones unitarias a la sintaxis actual de Quarto Live (`jupyter: false`).

---

## 3. Matriz de Pruebas Funcionales E2E en Navegador Real

Ejecutadas mediante `tests/run_stabilization_tests.py` contra el servidor Quarto en `http://127.0.0.1:4200/`:

| Paso / Flujo | Entrada Evaluada | Comportamiento Esperado | Resultado Real Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **01. Estado webR** | Carga inicial | Detección real del runtime en WebAssembly | Badge TopBar: `R listo` con punto verde | **PASS** |
| **02. Run Exploratorio** | `18 + 11` (Ejecutar) | Salida en consola sin evaluar ni calificar | Consola: `> 18 + 11` seguido de `[1] 29`. Progreso permanece `not_started` | **PASS** |
| **03. No-Grading en Run** | Verificación Store | Progreso no debe mutar a `completed` | `status: not_started`, progreso `0% Completado` | **PASS** |
| **04. Función R en Run** | `mean(c(10, 20, 30))` | Ejecución de funciones estadísticas R | Consola: `[1] 20` | **PASS** |
| **05. Error de Objeto en Run**| `objeto_inexistente` | Captura fidedigna de error de R en consola | Consola: `Error in eval(ei, envir): object 'objeto_inexistente' not found` | **PASS** |
| **06. Error de Sintaxis en Run**| `x <-` | Captura de parse error sin colapsar UI | Consola: `Error in parse(text = expr): <text>:2:0: unexpected end of input` | **PASS** |
| **07. Submit Incorrecto** | `18 + 11` (Enviar) | Calificación evaluativa con diagnóstico | Tarjeta ámbar: `Revisa tu respuesta. El resultado de la operación debería ser 30.` | **PASS** |
| **08. Submit Correcto** | `18 + 12` (Enviar) | Calificación aprobatoria y registro | Tarjeta verde: `Correcto. ¡Muy bien! R calculó la operación y obtuvo 30.` | **PASS** |
| **09. Progreso Módulo** | Post Ex0 Submit | Incremento a 25% | BottomBar: `25% Completado`, Stepper nodo 1 verde | **PASS** |
| **10. Botón Continuar** | Post Ex0 Submit | Botón activado para avance fluido | `#sr-btn-continue-bottom` visible y operativo | **PASS** |
| **11. Navegación Ex1** | Clic en Siguiente | Transición 0 ms a `intro-r-01-001` | Ejercicio 1 activo, URL hash `#intro-r-01-001` | **PASS** |
| **12. Pistas Secuenciales** | Clic en `Ver pista` | Revelación escalonada de ayudas | Pista 1 revelada, texto de botón cambia a `Pista 2 de 2` | **PASS** |
| **13. Finalización Ex1** | `25 + 17` (Enviar) | Calificación exitosa de suma | Tarjeta verde, progreso avanza a `50% Completado` | **PASS** |
| **14. Diagnóstico Ex2** | `numero_estudiantes <- 100` | Detección de objeto con valor incorrecto | Tarjeta ámbar: `R encontró el objeto numero_estudiantes, pero su valor todavía no es 120.` | **PASS** |
| **15. Finalización Ex2** | `numero_estudiantes <- 120` | Creación correcta de variable en entorno | Tarjeta verde, progreso avanza a `75% Completado` | **PASS** |
| **16. Diagnóstico Ex3 (Tipo)**| `edad_promedio <- "21.4"` | Detección de `character` vs `numeric` | Tarjeta informativa: `El valor parece correcto, pero está guardado como texto (comillas)...` | **PASS** |
| **17. Finalización Ex3** | `edad_promedio <- 21.4` | Asignación numérica con decimal | Tarjeta verde, progreso alcanza `100% Completado` | **PASS** |
| **18. Persistencia (F5)** | Recarga completa de página | Retención de progreso en `localStorage` | Los 4 ejercicios mantienen estado `completed` | **PASS** |
| **19. Contador Post-Reload**| Comprobación post-F5 | Progreso global del curso | BottomBar muestra `100% Completado` y los 4 nodos completados | **PASS** |

---

## 4. Auditoría Visual y de Resoluciones (Screenshots en `docs/screenshots/v0.3.1/`)

### Resoluciones de Pantalla
- **1366 × 768 (Laptop estándar):** `docs/screenshots/v0.3.1/social-r-1366x768.png`  
  *Evaluación:* Ajuste perfecto al 100% del viewport. Altura útil de 684px distribuida de forma equilibrada entre editor (380px), consola (190px), explicación e instrucciones sin ningún scroll exterior de ventana.
- **1440 × 900 (MacBook / Pantalla media):** `docs/screenshots/v0.3.1/social-r-1440x900.png`  
  *Evaluación:* Visualización sumamente holgada y legible. El panel pedagógico respeta el límite ergonómico de lectura (`max-width: 75ch`).
- **1920 × 1080 (Monitor Full HD):** `docs/screenshots/v0.3.1/social-r-1920x1080.png`  
  *Evaluación:* Proporciones sólidas con panel de código de más de 1150px de ancho y consola espaciosa.

### Capturas de Estados de Progresión
1. **`01-inicial.png`:** Estado inicial limpio con estado `● R listo`, breadcrumbs sobrios y botones directos.
2. **`02-run-output.png`:** Ejecución de `18 + 12` en consola R con prompt `>` y resultado `[1] 30` manteniendo progreso en 0%.
3. **`03-feedback-incorrecto.png`:** Envío de `18 + 11` mostrando tarjeta ámbar de diagnóstico `El resultado de la operación debería ser 30.` sin habilitar el botón de continuar.
4. **`04-feedback-correcto.png`:** Envío de `18 + 12` mostrando tarjeta verde de éxito, progreso al 25% y botón `Continuar →`.
5. **`05-course-outline.png`:** Drawer de esquema de curso abierto mostrando estados `Completado` y `Pendiente` sin emojis ni candados.

---

## 5. Elementos Eliminados y Limpieza Visual

- **Eliminación total de emojis:** Removidos `📊`, `💡`, `🔓`, `✓`, `▶`, `⏳`, `🔒`, `⚠️`.
- **Eliminación de modo desarrollador en UI:** El selector `Dev` fue retirado de la TopBar visible de estudiante.
- **Eliminación de gradientes y animaciones llamativas:** Se eliminaron los pulsos de botón y gradientes de color estridentes en favor de fondos sólidos sobrios (`#16a34a`, `#2563eb`, `#334155`).
- **Eliminación de jerarquía rígida 50/50:** Se flexibilizó el contenedor de explicaciones e instrucciones para evitar huecos en blanco innecesarios.

---

## 6. Problemas Pendientes

- Ninguno para la fase v0.3.1. Todos los criterios de estabilización funcional y refinamiento visual han sido cumplidos y verificados.

---

## 7. Dictamen Final de Entrega

```text
======================================================================
SOCIAL R v0.3.1 — STABILIZATION & PROFESSIONAL VISUAL REFINEMENT
FUNCTIONAL QA: PASS
VISUAL QA: PASS
======================================================================
```
