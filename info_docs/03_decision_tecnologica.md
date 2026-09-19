# 03 · Decisión tecnológica

## Decisión

**MVP static-first: Quarto + Quarto Live + webR.**

JavaScript/TypeScript se reserva para funcionalidades de plataforma no resueltas por Quarto Live: progreso global, eventos, desbloqueo, navegación, analítica y adaptadores de persistencia.

## Evidencia que sustenta la decisión

Quarto Live documenta explícitamente:

- código R/Python interactivo en HTML;
- editor basado en CodeMirror;
- hints y solutions enlazados por identificador;
- grading personalizado;
- variables de grading con resultado, código del estudiante y ambientes antes/después;
- `persist: true` para conservar el código editado en localStorage;
- `timelimit` para limitar ejecución;
- recursos locales cargados al VFS;
- instalación de paquetes webR al inicio.

webR ejecuta R directamente en el navegador. GitHub Pages es compatible con el enfoque static-first, pero no permite configurar los headers COOP/COEP necesarios para SharedArrayBuffer; webR cae a PostMessage. Esa caída tiene una consecuencia importante: la interrupción de código R no está soportada en ese canal. Por ello, el `timelimit` de Quarto Live debe probarse específicamente bajo GitHub Pages antes de considerarlo una salvaguarda suficiente para bucles infinitos.

## Versión y pinning

No utilizar `latest` de forma ciega en producción. Cuando el prototipo sea validado, fijar:

- versión estable de Quarto;
- commit/tag de Quarto Live;
- versión del engine webR si Quarto Live lo permite mediante `engine-url`.

Registrar el conjunto en el ADR.
