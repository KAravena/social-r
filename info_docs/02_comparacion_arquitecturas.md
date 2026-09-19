# 02 · Comparación de arquitecturas

Escala: 1 = desfavorable, 5 = favorable para este proyecto.

| Criterio | A Quarto Live + webR | B webR + motor JS/TS | C Shinylive | D Shiny servidor |
|---|---:|---:|---:|---:|
| Complejidad inicial | 5 | 2 | 3 | 2 |
| Mantenimiento | 5 | 2 | 3 | 2 |
| Microejercicios con grading | 5 | 5 potencial / 1 inicial | 3 | 5 |
| Feedback específico | 5 | 5 | 5 | 5 |
| Pistas/soluciones listas | 5 | 1 | 2 | 2 |
| Static hosting | 5 | 5 | 5 | 1 |
| GitHub Pages | 5 | 5 | 5 | 1 |
| Sin servidor R | 5 | 5 | 5 | 1 |
| Control absoluto del runtime | 3 | 5 | 3 | 5 |
| Afinidad con R + Quarto | 5 | 3 | 4 | 5 |
| Coste operativo | 5 | 5 | 5 | 2 |

## A · Quarto + Quarto Live + webR

**Fortalezas:** es la solución más alineada con el problema. Quarto Live ofrece exactamente primitivas educativas: exercise, setup, hint, solution, check, CodeMirror y persistencia. El grader recibe `.user_code`, `.result`, `.envir_prep`, `.envir_result`, `.evaluate_result` y solución, permitiendo evaluación semántica.

**Debilidades:** no es una plataforma completa. No ofrece un modelo de usuario, progreso de curso, sincronización remota ni un contrato público documentado de eventos de finalización. La API de webR y Quarto Live sigue evolucionando.

**Uso recomendado:** motor base del MVP.

## B · Quarto + webR + motor propio JS/TS

**Fortalezas:** control total sobre editor, eventos, estados, telemetría y navegación.

**Debilidades:** habría que reconstruir editor, ejecución, captura de output/errores, grader, hints, soluciones, entornos, timeouts, accesibilidad y compatibilidad de versiones. Es el coste técnico más alto y hoy no está justificado.

**Condición para migrar:** si Quarto Live impide requisitos centrales o su DOM/API resulta demasiado inestable para la plataforma.

## C · Quarto + Shinylive

Shinylive ejecuta aplicaciones Shiny enteramente en navegador sobre webR y exporta a hosting estático. Es excelente para simuladores, miniaplicaciones y exploradores interactivos. Sin embargo, un ejercicio DataCamp-like es un problema más pequeño que una app Shiny; usar una app por ejercicio introduce una abstracción más pesada y no trae de serie el modelo específico de hints/check/solution de Quarto Live.

**Uso recomendado:** componente especial futuro para laboratorios/simulaciones, no motor principal de microejercicios.

## D · Quarto + Shiny tradicional

Es la alternativa con más libertad para autenticación, datos sensibles, persistencia central y cálculo en servidor. Sin embargo, exige un servidor activo y despliegue específico; no funciona en GitHub Pages como una aplicación interactiva Shiny tradicional.

**Uso recomendado:** reconsiderar cuando exista necesidad real de usuarios, datos centralizados, evaluación de alto impacto o tareas que no puedan ejecutarse razonablemente en WebAssembly.

## Recomendación

Adoptar A. Mantener una frontera explícita para sustituir el runtime en el futuro y no acoplar el contenido pedagógico a la sintaxis interna de Quarto Live.
