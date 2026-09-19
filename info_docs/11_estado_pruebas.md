# 11 · Estado de pruebas

## Pruebas ejecutadas en este entorno

- [x] ZIP inspeccionado: 62 PNG de ejercicios + archivos de registro.
- [x] Schema JSON cargado y validación de 3 YAML.
- [x] Generador Python ejecutado.
- [x] Tests unitarios del generador.
- [x] Compilación sintáctica de Python.
- [ ] `quarto check`.
- [ ] `quarto render`.
- [ ] `quarto preview`.
- [ ] ejecución real de webR en navegador.
- [ ] mediciones de rendimiento en navegador.

## Bloqueo del entorno de ejecución

El contenedor disponible para esta fase no tiene `quarto` ni `R` instalados y no tiene resolución DNS de salida para descargar el instalador o ejecutar `quarto add`. Por esa razón no es metodológicamente correcto marcar A–L como comprobados.

El proyecto incluye `engine/verify.py` para continuar exactamente desde este punto en una máquina con Quarto y conexión a Internet.

## Criterios A–L

| Criterio | Estado aquí | Evidencia/acción pendiente |
|---|---|---|
| A Renderiza con Quarto | PENDIENTE | `quarto render` |
| B Editor R navegador | PENDIENTE | abrir preview |
| C 18+12 sin R local | PENDIENTE | ejecutar exercise calc-01 |
| D Resultado visible | PENDIENTE | inspección browser |
| E Correcto/incorrecto | FUENTE VALIDADA / RUNTIME PENDIENTE | grader generado |
| F Inspecciona objetos | FUENTE VALIDADA / RUNTIME PENDIENTE | `.envir_result` |
| G Distingue errores | FUENTE VALIDADA / RUNTIME PENDIENTE | tipo vs valor/ausencia |
| H Feedback distinto | FUENTE VALIDADA / RUNTIME PENDIENTE | diagnostics/checks |
| I Pistas progresivas | FUENTE VALIDADA / RUNTIME PENDIENTE | 3 `.hint` enlazadas |
| J Solución | FUENTE VALIDADA / RUNTIME PENDIENTE | `.solution` |
| K Contenido sin modificar motor | PASS | 3 YAML → generador común |
| L HTML estático | DISEÑO VALIDADO / RENDER PENDIENTE | `live-html`; sin Shiny server |

## Intento adicional de instalación en este entorno

Se identificó la distribución oficial estable `quarto-1.10.18-linux-amd64.tar.gz` (24-07-2026), pero el runtime de herramientas de esta sesión impide incorporar archivos `application/gzip` y el contenedor no tiene salida DNS directa. Por ello no fue posible instalar una copia portátil de Quarto aquí. Esto es una limitación del entorno de ejecución de esta auditoría, no una validación negativa del prototipo.
