# 07 · Datasets y paquetes

## Datasets

Quarto Live permite declarar `resources` para descargar archivos al Virtual Filesystem de WebAssembly. Para ejercicios educativos pequeños, estrategia recomendada:

1. datasets mínimos y anonimizados incluidos en el sitio;
2. CSV para transparencia y depuración inicial;
3. `setup_code` para crear objetos muy pequeños sin archivo;
4. no descargar una encuesta nacional completa para enseñar una operación de cinco filas;
5. mantener datasets grandes para proyectos finales o preparar extractos pedagógicos.

## RDS

webR dispone de un filesystem virtual y R base, por lo que archivos binarios R pueden ser técnicamente posibles si son accesibles en VFS; sin embargo, para el MVP se prefiere CSV por portabilidad, inspección y menor acoplamiento a versiones. RDS debe probarse antes de declararlo formato estándar.

## Paquetes

Quarto Live permite declarar paquetes en YAML para instalarlos al iniciar el motor. La documentación oficial usa explícitamente `dplyr` y `ggplot2` como ejemplo, por lo que ambos son candidatos demostrados por la propia documentación.

Para `tidyr`, `forcats`, `stringr` y `readr`, no se declara compatibilidad sin un smoke test contra la versión de webR fijada. El repositorio webR distribuye paquetes precompilados para WebAssembly y no permite compilar paquetes desde source dentro del navegador.

## Política

- Base R primero en los primeros ejercicios, para reducir descarga y carga cognitiva.
- Cargar tidyverse por módulos, no globalmente desde la portada.
- Preferir paquetes concretos (`dplyr`, `ggplot2`) en vez de `tidyverse` completo.
- Fijar versiones/runtime antes de producción.
- Si un paquete no existe en el repo por defecto, evaluar R-universe o una repo CRAN-like compilada con `{rwasm}`.

## Prueba futura obligatoria

Crear un documento diagnóstico que intente instalar/cargar:

```r
c("dplyr", "ggplot2", "tidyr", "forcats", "stringr", "readr")
```

y registrar éxito, versión, tamaño transferido y tiempo.
