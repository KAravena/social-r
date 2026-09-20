# Social R — Módulo 6: Trabajar cuando faltan datos
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Filtra casos y selecciona columnas mediante pipelines con `|>` (Módulo 5).

### Capacidad después
Comprende el significado de `NA` como dato no disponible, detecta valores ausentes con `is.na()`, cuantifica faltantes con `sum(is.na())`, calcula resúmenes sobre datos disponibles con `na.rm = TRUE`, y diagnostica la integridad de variables tras preparar subconjuntos de datos.

### Pregunta central
¿Cómo identificamos, contamos y tratamos la información ausente (`NA`) en encuestas sociales sin alterar los datos observados?

### Modelo mental
`VALOR 0 = DATO OBSERVADO | NA = DATO AUSENTE / NO DISPONIBLE`
`is.na(VECTOR) → TRUE DONDE FALTA EL DATO, FALSE DONDE ESTÁ PRESENTE`
`sum(is.na(VECTOR)) → CANTIDAD DE CASOS SIN RESPUESTA`
`sum(VECTOR, na.rm = TRUE) → SUMA DE VALORES EFECTIVAMENTE DISPONIBLES`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Vector y Base Central: `encuesta_social_demo$horas_cuidado` (E01 a E05)
8 casos con datos observados y ausencias reales:

| id | edad | trabaja | horas_cuidado |
|:---|---:|:---|---:|
| 1 | 20 | No | 6 |
| 2 | 22 | Sí | NA |
| 3 | 19 | No | 0 |
| 4 | 21 | No | 8 |
| 5 | 24 | Sí | 4 |
| 6 | 23 | Sí | 5 |
| 7 | 20 | No | NA |
| 8 | 25 | Sí | 7 |

*Nota sustantiva*: El caso 3 dedicó 0 horas (valor observado). Los casos 2 y 7 no respondieron (`NA`).

### 2. Base de Transferencia: `encuesta_barrio_m6` (E06)
6 casos de movilidad con datos ausentes:

| id | transporte | minutos_viaje |
|:---|:---|---:|
| 1 | Bus | 35 |
| 2 | Metro | NA |
| 3 | Bus | 50 |
| 4 | Bicicleta | 20 |
| 5 | Metro | NA |
| 6 | Bus | 40 |

---

## Especificación Detallada de los 6 Ejercicios

### M6-E1 — Aquí no sabemos el valor
* **Rol**: Worked example + distinción conceptual activa.
* **Contexto**: En encuestas sociales es común que algunas personas no respondan. En R, la ausencia de información se representa con `NA` (sin comillas):
  - `0`: es un valor observado (la persona reportó cero horas).
  - `NA`: no disponible (la persona no respondió o no se tiene el dato).
* **Tarea**: Consulta el vector `horas_cuidado` en la consola para observar sus valores y distinguir las posiciones con `0` de las que tienen `NA`.
* **Starter code**:
  ```r
  # Consulta horas_cuidado para ver dónde hay 0 y dónde hay NA:
  horas_cuidado
  ```
* **Solución**:
  ```r
  horas_cuidado
  ```
* **Checks**:
  - `result_equals`: `c(6, NA, 0, 8, 4, 5, NA, 7)`.

---

### M6-E2 — ¿Dónde falta información?
* **Rol**: Práctica activa con `is.na()`.
* **Contexto**: Para saber qué posiciones tienen datos ausentes usamos `is.na()`. Devuelve `TRUE` donde falta información y `FALSE` donde hay un dato disponible:
  `is.na(c(6, 0, NA))` → `FALSE, FALSE, TRUE`
* **Tarea**: Aplica `is.na()` sobre `horas_cuidado` y guarda el vector lógico resultante en `faltan_datos`.
* **Starter code**:
  ```r
  # Detecta valores ausentes con is.na() y guárdalo en faltan_datos:

  ```
* **Solución**:
  ```r
  faltan_datos <- is.na(horas_cuidado)
  ```
* **Checks**:
  - `object_exists`: `faltan_datos`.
  - `object_value`: `faltan_datos == c(FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE)`.

---

### M6-E3 — ¿Cuántos datos faltan?
* **Rol**: Práctica guiada (conteo de valores lógicos).
* **Contexto**: En R, `TRUE` vale 1 y `FALSE` vale 0 en operaciones aritméticas. Por eso podemos contar cuántos datos faltan sumando las respuestas lógicas:
  `sum(is.na(vector))`
* **Tarea**: Cuenta la cantidad total de ausencias en `horas_cuidado` combinando `sum()` e `is.na()`.
* **Starter code**:
  ```r
  # Cuenta cuántos NA hay en horas_cuidado:

  ```
* **Solución**:
  ```r
  sum(is.na(horas_cuidado))
  ```
* **Checks**:
  - `result_equals`: `2`.

---

### M6-E4 — Por qué el cálculo no responde
* **Rol**: Práctica activa con `na.rm = TRUE`.
* **Contexto**: Si intentas sumar un vector con `NA`, el resultado es `NA` porque R no puede inventar el total de datos desconocidos. Para calcular la suma o el promedio ignorando las ausencias agregamos el argumento `na.rm = TRUE`:
  `sum(vector, na.rm = TRUE)`
* **Tarea**: Calcula el promedio de las horas de cuidado disponibles usando `mean()` con `na.rm = TRUE`.
* **Starter code**:
  ```r
  # Calcula la media de horas_cuidado ignorando los NA:

  ```
* **Solución**:
  ```r
  mean(horas_cuidado, na.rm = TRUE)
  ```
* **Checks**:
  - `result_equals`: `5`.

---

### M6-E5 — Prepara y revisa los casos pertinentes
* **Rol**: Práctica combinada (pipeline + diagnóstico de missing).
* **Contexto**: Queremos estudiar las horas de cuidado de quienes trabajan en `encuesta_social_demo`.
* **Tarea**:
  1. Prepara `datos_trabajan` filtrando a quienes trabajan (`trabaja == "Sí"`) y seleccionando `id` y `horas_cuidado`.
  2. Cuenta cuántos `NA` hay en `horas_cuidado` dentro de ese grupo usando `sum(is.na())`.
* **Starter code**:
  ```r
  # 1. Prepara datos_trabajan con filter() y select():


  # 2. Cuenta cuántos NA hay en horas_cuidado del subgrupo:

  ```
* **Solución**:
  ```r
  datos_trabajan <- encuesta_social_demo |>
    filter(trabaja == "Sí") |>
    select(id, horas_cuidado)

  sum(is.na(datos_trabajan$horas_cuidado))
  ```
* **Checks**:
  - `object_exists`: `datos_trabajan`.
  - `custom_r`: `nrow(datos_trabajan) == 4`.
  - `result_equals`: `1`.

---

### M6-E6 — Otra base con datos ausentes
* **Rol**: Transferencia autónoma sobre nueva base.
* **Contexto**: La base `encuesta_barrio_m6` (visible en la tabla) registra minutos de viaje de 6 personas, con algunas ausencias.
* **Tarea**:
  1. Cuenta cuántos datos faltan en `minutos_viaje` usando `sum(is.na())`.
  2. Calcula el total de minutos de viaje sumando los valores disponibles con `sum()` y `na.rm = TRUE`.
* **Starter code**:
  ```r
  # 1. Cuenta las ausencias en encuesta_barrio_m6$minutos_viaje:


  # 2. Suma los minutos disponibles con na.rm = TRUE:

  ```
* **Solución**:
  ```r
  sum(is.na(encuesta_barrio_m6$minutos_viaje))
  sum(encuesta_barrio_m6$minutos_viaje, na.rm = TRUE)
  ```
* **Checks**:
  - `custom_r`: `grepl('sum\\s*\\(\\s*is\\.na', .user_code)`.
  - `result_equals`: `185`.
