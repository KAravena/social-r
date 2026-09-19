# ADR-001 · Runtime de ejercicios

- **Estado:** Accepted
- **Fecha:** 2026-08-16

## Problema

Necesitamos ejecutar y corregir ejercicios de R en una plataforma Quarto, con feedback pedagógico, pistas y solución, sin requerir un servidor R en el MVP y sin programar cada página manualmente.

## Alternativas evaluadas

1. Quarto + Quarto Live + webR.
2. Quarto + webR + motor JS/TS propio.
3. Quarto + Shinylive.
4. Quarto + Shiny tradicional.

## Decisión

Adoptar **Quarto + Quarto Live + webR** como runtime inicial. Usar un schema YAML propio y generación build-time de QMD. Mantener una capa JS/TS independiente para funcionalidades de plataforma.

## Motivos

- Quarto Live ya resuelve editor, ejecución, grading, hints y solution.
- webR elimina el servidor R en el MVP.
- el sitio puede servirse de forma estática.
- Quarto sigue siendo el sistema de autoría.
- el grader dispone del ambiente posterior a la ejecución, permitiendo validación semántica.
- reduce mucho el código propio crítico.

## Consecuencias positivas

- menor tiempo de desarrollo;
- menor superficie de bugs;
- contenido auditable y versionable;
- posibilidad de GitHub Pages;
- fácil experimentación pedagógica.

## Consecuencias negativas

- dependencia de un proyecto en evolución;
- progreso global no viene resuelto;
- integración avanzada puede depender de APIs/DOM no documentados;
- paquetes restringidos a binarios WebAssembly;
- GitHub Pages obliga normalmente al canal PostMessage, con limitaciones de interrupción.

## Condiciones para reconsiderarla

Reabrir ADR si ocurre cualquiera de estas condiciones:

- no podemos detener de forma segura código problemático en el hosting elegido;
- no existe forma mantenible de observar éxito/intentos/hints;
- el frontend requerido no puede desacoplarse del DOM de Quarto Live;
- paquetes esenciales para el currículo no funcionan en webR;
- necesitamos evaluación formal con identidad y persistencia central;
- rendimiento real en dispositivos estudiantiles resulta inaceptable.
