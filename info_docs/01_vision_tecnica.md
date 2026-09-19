# 01 · Visión técnica

## Objetivo

Construir un motor de microejercicios de R que permita mantener Quarto como sistema de autoría y publicación, y ejecutar R en el navegador sin servidor de R durante el MVP.

## Hallazgo principal

Quarto Live ya cubre una parte muy grande del núcleo requerido: editor CodeMirror, ejecución mediante webR, ejercicios, setup, pistas, soluciones, grading personalizado, entornos separados, límite de tiempo y persistencia del código editado en localStorage. Por ello, reconstruir desde cero editor + runtime + grader en JavaScript sería duplicar infraestructura antes de demostrar una necesidad real.

## Arquitectura propuesta

```text
Contenido YAML
     │
     ▼
Generador build-time (Python ahora; reemplazable)
     │
     ▼
Quarto/QMD generado
     │
     ▼
Quarto Live
 ┌───────────────┬────────────────┐
 │ CodeMirror    │ Exercise grader│
 └──────┬────────┴───────┬────────┘
        │                │
        └─────── webR ───┘
                 │
                 ▼
         R/WebAssembly navegador

Capa Social R (JS/TS pequeña)
 ├─ ProgressStore
 ├─ EventBus
 ├─ navegación/desbloqueo futuro
 └─ adaptador remoto futuro
```

## Por qué JavaScript y no Java

El runtime adicional requerido vive en el navegador: almacenamiento local, eventos, navegación, integración con DOM y eventualmente telemetría. El lenguaje nativo de ese entorno es JavaScript; TypeScript aporta tipado para una base mayor. Java implicaría añadir otra plataforma/runtime sin resolver una necesidad que no esté cubierta mejor por JS/TS.

## Regla de diseño

- **Contenido**: declara qué aprende el estudiante, qué código inicial ve, qué se considera correcto, pistas y feedback.
- **Motor**: ejecuta, comprueba, registra estado y presenta ayuda.
- **Adaptadores**: conectan Quarto Live con progreso/analítica sin contaminar los YAML pedagógicos.

## Fuentes oficiales consultadas

- https://r-wasm.github.io/quarto-live/
- https://r-wasm.github.io/quarto-live/exercises/exercises.html
- https://r-wasm.github.io/quarto-live/exercises/grading.html
- https://docs.r-wasm.org/
- https://quarto.org/docs/publishing/github-pages.html
