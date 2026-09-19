# 08 · Riesgos y limitaciones

## 1. Evolución de webR/Quarto Live

webR declara que está en desarrollo activo; Quarto Live también evoluciona. Mitigación: pinning, ADR y pruebas de regresión.

## 2. GitHub Pages y SharedArrayBuffer

webR recomienda COOP/COEP para usar SharedArrayBuffer. GitHub Pages no permite configurar esos headers de forma normal, por lo que webR utiliza PostMessage. En PostMessage, la documentación de webR indica que la interrupción de código R no está soportada.

**Impacto:** un bucle infinito es un riesgo real que debe probarse. Si Quarto Live `timelimit` no puede detenerlo bajo GitHub Pages, considerar un host estático con headers configurables (por ejemplo Netlify/Cloudflare Pages) o una estrategia de worker reset.

## 3. Memoria y CPU del dispositivo

R corre en el equipo del estudiante. Datasets y operaciones pesadas pueden congelar equipos modestos. Limitar tamaño de datos y complejidad.

## 4. Networking

WebAssembly no tiene sockets directos. Descargas simples dependen de CORS; networking avanzado requiere proxy. Para un curso, preferir recursos empaquetados con el sitio.

## 5. Paquetes

No se compilan paquetes desde source en el navegador. Depender de binarios Wasm disponibles.

## 6. Seguridad

webR corre en un sandbox de WebAssembly y no tiene acceso arbitrario al filesystem del sistema del usuario. Sin embargo, `webr::eval_js()` puede ejecutar JavaScript y debe considerarse una API poderosa; no debe exponerse como mecanismo pedagógico a código no confiable sin evaluar consecuencias.

El código de estudiantes puede consumir CPU/memoria. Debe existir límite temporal y mecanismo de recuperación/reset verificable.

## 7. Progreso local

localStorage no sincroniza entre equipos, puede borrarse y no sirve como registro oficial de evaluación. Adecuado solo para MVP/autoprendizaje.

## 8. Accesibilidad

Quarto Live usa un editor CodeMirror y botones con `role`, `tabindex` y `aria-label` en su implementación actual. Esto es una buena base, no una certificación. Deben probarse navegación por teclado, foco, lectura de feedback y lector de pantalla en la interfaz final.
