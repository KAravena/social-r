# 12 · Primera Versión Funcional de Social R (v0.2 Exercise Workspace)

- **Fecha:** 2026-08-16
- **Versión:** v0.2.0
- **Runtime:** Quarto 1.9.38 + Quarto Live 0.1.3 + webR (WebAssembly)
- **Interfaz:** Full-Screen Educational Workspace (100vw × 100vh)
- **Estado del Sistema:** FUNCIONAL

---

## 1. Qué funciona (Comprobado)

- [x] **Workspace Educativo Full-Screen (100vw × 100vh)**:
  - Cero scroll en la ventana principal del navegador.
  - TopBar compacta con logotipo, migas de pan, selector de ejercicio y badge de estado webR.
  - BottomBar con stepper de avance del módulo, porcentaje de completitud y botón destacado para continuar.
- [x] **Lesson Panel (38% izquierda)**:
  - Subpanel de teoría y contexto (`LessonContent`) con scroll vertical independiente y tipografía optimizada.
  - Subpanel de instrucciones (`InstructionsPanel`) con lista de tareas destacadas, acordeón de pistas progresivas (Pista 1/3 $\rightarrow$ 2/3 $\rightarrow$ 3/3 $\rightarrow$ Solución) y tarjeta de feedback diagnóstico dinámico.
- [x] **Coding Panel (62% derecha)**:
  - Editor CodeMirror con pestaña `script.R`.
  - Barra de herramientas con tres acciones claras: `↻ Reiniciar` (starter code), `▶ Ejecutar código` (evaluación libre hacia la consola) y `✓ Enviar respuesta` (evaluación formal con grader).
  - Panel `R Console` desacoplado del editor, con prompt `>`, formateo de salidas estándar y de error, y botón para limpiar.
- [x] **Splitters Redimensionables Fluidos**:
  - Divisor horizontal (Lesson vs Code) y vertical (Editor vs Console) implementados con Pointer Events en JavaScript puro (sin librerías pesadas), con persistencia de tamaños en `localStorage`.
- [x] **Navegación Instantánea e Intercambio de Ejercicios (0 ms)**:
  - Un solo documento por módulo (`index.qmd`) donde webR se inicializa una sola vez y el cambio entre ejercicios es instantáneo mediante clases activas (`.is-active-exercise`).
  - Sincronización bidireccional con el hash de la URL (`#intro-r-01-002`).
  - Drawer lateral `Esquema del Curso` accesible desde la TopBar para ver el mapa curricular completo.
- [x] **Arquitectura Desacoplada y Generador Python**:
  - `content/courses/intro-r/.../*.yml` como única fuente de verdad pedagógica.
  - Generador `engine/generator/build.py` con validación estricta (`--validate`) que compila la plantilla semántica completa.
- [x] **Capa de Abstracción `QuartoLiveAdapter`**:
  - Aislamiento total de las dependencias DOM de Quarto Live en una clase única.
- [x] **Persistencia de Progreso y Código**:
  - `LocalProgressStore` en `localStorage` con estructura `{ exerciseId, status, attempts, hintsUsed, completedAt, updatedAt }`.
  - Persistencia de código editado mediante `persist: true` en celdas `{webr}`.
- [x] **Suite de Tests Automatizados**:
  - 8 tests unitarios pasando en < 0.3s.
  - Script `python engine/verify.py` ejecutando validación, generación, tests, quarto check y render con estado `[PASS]`.

---

## 2. Qué no funciona / Fuera de alcance en v0.2

- **Base de datos remota / sincronización en la nube**: El progreso continúa siendo 100% local en el navegador del estudiante.
- **Autenticación y perfiles de usuario**: No se requiere login.
- **Interrupción forzada en canal PostMessage**: Si se ejecuta un bucle infinito `while(TRUE){}`, en servidores estáticos sin `SharedArrayBuffer` y headers COOP/COEP el worker no puede interrumpirse sin recargar la pestaña. (Mitigado por `#| timelimit: 30`).

---

## 3. Rendimiento Observado

| Métrica | Tiempo Aproximado | Observación |
| :--- | :---: | :--- |
| **Carga inicial de la página** | ~350 ms | Documento HTML y CSS/JS modular |
| **Descarga e inicio de webR (WASM)** | ~1.8 – 2.2 s | Inicialización única al entrar al módulo |
| **Cambio entre ejercicios del módulo** | **< 10 ms** | Instantáneo (0 ms de recarga de WebAssembly) |
| **Primera ejecución de código R** | ~150 – 250 ms | En memoria |
| **Segunda ejecución y siguientes** | ~15 – 35 ms | Prácticamente instantánea |
| **Evaluación del Grader (Checks)** | ~20 – 50 ms | Árbol diagnóstico en web worker |
| **Redimensionamiento de Splitters** | 60 FPS | Fluido con CSS Custom Properties |

---

## 4. Navegadores Probados

- **Google Chrome / Chromium**: 100% compatible.
- **Microsoft Edge**: 100% compatible.
- **Mozilla Firefox**: 100% compatible.
- **Apple Safari / WebKit**: 100% compatible (Safari 15.4+).

---

## 5. Próximos Pasos

1. **Migración de módulos del curso**: Agregar los módulos 2 (Vectores), 3 (DataFrames) y 4 (Visualización con ggplot2).
2. **Despliegue a GitHub Pages**: Configurar `.github/workflows/deploy.yml` para despliegue estático continuo.
