# Social R — Módulo 5: Seleccionar y filtrar datos
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Reconoce la estructura tabular de un **data frame** y extrae columnas individuales con el operador `$` (Módulo 4).

### Capacidad después
Formula condiciones lógicas sobre columnas de una base, conserva casos completos (filas) con `filter()`, selecciona variables de interés (columnas) con `select()`, encadena operaciones en flujos legibles con el pipe `|>`, y prepara autónomamente subconjuntos de datos en el checkpoint.

### Pregunta central
¿Cómo filtramos casos específicos y seleccionamos únicamente las variables que necesitamos para una investigación social?

### Modelo mental
`BASE $ VARIABLE > UMBRAL → VECTOR LÓGICO SOBRE FILAS`
`filter(BASE, CONDICIÓN) → CONSERVA FILAS QUE CUMPLEN (CASOS)`
`select(BASE, VAR1, VAR2) → CONSERVA COLUMNAS (VARIABLES)`
`BASE |> filter(...) |> select(...) → FLUJO SECUENCIAL SIN GUARDAR PASOS INTERMEDIOS`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_social_demo` (E01 a E07)
8 casos reales y 5 variables:

| id | edad | carrera | horas_estudio | trabaja |
|:---|---:|:---|---:|:---|
| 1 | 20 | Sociología | 3 | No |
| 2 | 22 | Historia | 5 | Sí |
| 3 | 19 | Antropología | 2 | No |
| 4 | 21 | Sociología | 4 | No |
| 5 | 24 | Trabajo Social | 6 | Sí |
| 6 | 23 | Antropología | 3 | Sí |
| 7 | 20 | Historia | 5 | No |
| 8 | 25 | Sociología | 2 | Sí |

### 2. Base de Transferencia: `encuesta_jovenes` (E08 - Checkpoint)
8 casos reales de jóvenes y 4 variables:

| id | edad | estudia | comuna | transporte |
|:---|---:|:---|:---|:---|
| 1 | 18 | Sí | Norte | Bus |
| 2 | 20 | No | Centro | Metro |
| 3 | 19 | Sí | Sur | Bicicleta |
| 4 | 22 | Sí | Centro | Bus |
| 5 | 21 | No | Norte | Metro |
| 6 | 23 | Sí | Sur | Metro |
| 7 | 19 | No | Norte | Bus |
| 8 | 24 | Sí | Centro | Bicicleta |

---

## Especificación Detallada de los 8 Ejercicios

### M5-E1 — Vuelve a hacer una pregunta
* **Rol**: Práctica guiada (conectar `$` con operadores lógicos).
* **Contexto**: En el Módulo 3 hicimos preguntas a vectores simples. En el Módulo 4 aprendimos que una columna de una base se extrae con `$`. Ahora juntamos ambas ideas para formular preguntas sobre una variable de la base:
  `encuesta_social_demo$edad > 21`
* **Tarea**: Pregunta qué edades en `encuesta_social_demo` son mayores que 21 combinando `$` y `> 21`.
* **Starter code**:
  ```r
  # Pregunta qué edades son mayores a 21:

  ```
* **Solución**:
  ```r
  encuesta_social_demo$edad > 21
  ```
* **Checks**:
  - `result_equals`: `c(FALSE, TRUE, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE)`.

---

### M5-E2 — De TRUE/FALSE a personas completas
* **Rol**: Worked example en panel + práctica activa en editor.
* **Contexto**: Cuando usamos una condición lógica para indexar las filas de una base:
  `mayores_21 <- encuesta_social_demo$edad > 21`
  `encuesta_social_demo[mayores_21, ]`
  R conserva a la persona completa con todas sus columnas para cada fila donde la respuesta fue `TRUE`.
* **Tarea**: Siguiendo el modelo, identifica a las personas que trabajan (`trabaja == "Sí"`) y úsalo para conservar las filas correspondientes en `personas_trabajan`.
* **Starter code**:
  ```r
  # 1. Identifica qué personas trabajan:
  trabajan <- encuesta_social_demo$trabaja == "Sí"

  # 2. Conserva sus filas completas en personas_trabajan:

  ```
* **Solución**:
  ```r
  trabajan <- encuesta_social_demo$trabaja == "Sí"
  personas_trabajan <- encuesta_social_demo[trabajan, ]
  ```
* **Checks**:
  - `object_exists`: `personas_trabajan`.
  - `custom_r`: `nrow(personas_trabajan) == 4`.

---

### M5-E3 — Una forma más legible de filtrar
* **Rol**: Práctica activa con `filter()`.
* **Contexto**: La función `filter()` simplifica el filtrado de filas. En lugar de usar corchetes y `$`, escribimos directamente la condición:
  `filter(base, condicion)`
* **Tarea**: Usa `filter()` para conservar a los estudiantes con más de 3 horas de estudio (`horas_estudio > 3`) en `encuesta_social_demo`.
* **Starter code**:
  ```r
  # Filtra las personas con más de 3 horas de estudio:

  ```
* **Solución**:
  ```r
  filter(encuesta_social_demo, horas_estudio > 3)
  ```
* **Checks**:
  - `result_equals`: `filter(encuesta_social_demo, horas_estudio > 3)`.

---

### M5-E4 — Filtra otro grupo
* **Rol**: Práctica guiada (filtrar por categoría con `==`).
* **Contexto**: Para filtrar por una categoría de texto usamos `==` con el texto entre comillas:
  `filter(base, variable == "Categoría")`
* **Tarea**: Filtra `encuesta_social_demo` para conservar únicamente a los estudiantes de Sociología (`carrera == "Sociología"`).
* **Starter code**:
  ```r
  # Filtra a las personas cuya carrera es "Sociología":

  ```
* **Solución**:
  ```r
  filter(encuesta_social_demo, carrera == "Sociología")
  ```
* **Checks**:
  - `result_equals`: `filter(encuesta_social_demo, carrera == "Sociología")`.

---

### M5-E5 — Los datos pasan a la siguiente acción
* **Rol**: Práctica activa con pipe `|>`.
* **Contexto**: El operador pipe `|>` pasa el resultado de la izquierda como primer argumento a la función de la derecha:
  `base |> filter(condicion)`
  Esto permite leer el código como una secuencia ordenada de pasos sin alterar la base original.
* **Tarea**: Filtra a los estudiantes de Sociología pasando la base con el pipe `|>`.
* **Starter code**:
  ```r
  # Pasa la base con |> hacia filter():

  ```
* **Solución**:
  ```r
  encuesta_social_demo |> filter(carrera == "Sociología")
  ```
* **Checks**:
  - `custom_r`: `grepl('\\|>', .user_code)`.
  - `result_equals`: `filter(encuesta_social_demo, carrera == "Sociología")`.

---

### M5-E6 — Qué variables necesito
* **Rol**: Práctica activa con `select()`.
* **Contexto**: Mientras `filter()` elige **casos (filas)**, `select()` elige **variables (columnas)** por su nombre:
  - `filter(base, condicion)` → elige filas.
  - `select(base, var1, var2)` → elige columnas.
* **Tarea**: Selecciona únicamente las columnas `edad` y `carrera` de `encuesta_social_demo`.
* **Starter code**:
  ```r
  # Selecciona las columnas edad y carrera:

  ```
* **Solución**:
  ```r
  select(encuesta_social_demo, edad, carrera)
  ```
* **Checks**:
  - `result_equals`: `select(encuesta_social_demo, edad, carrera)`.

---

### M5-E7 — Filtra y después selecciona
* **Rol**: Práctica combinada (pipeline encadenado).
* **Contexto**: El pipe permite encadenar múltiples decisiones en un flujo de lectura limpio:
  ```r
  base |>
    filter(condicion) |>
    select(var1, var2)
  ```
* **Tarea**: Construye un pipeline con `|>` que primero filtre a las personas que trabajan (`trabaja == "Sí"`) y luego seleccione `edad` y `carrera`.
* **Starter code**:
  ```r
  # Encadena filter() y select() usando el pipe |>:
  encuesta_social_demo |>


  ```
* **Solución**:
  ```r
  encuesta_social_demo |>
    filter(trabaja == "Sí") |>
    select(edad, carrera)
  ```
* **Checks**:
  - `custom_r`: `grepl('\\|>', .user_code)`.
  - `result_equals`: `encuesta_social_demo |> filter(trabaja == "Sí") |> select(edad, carrera)`.

---

### M5-E8 — Checkpoint B: prepara los datos
* **Rol**: Checkpoint / Integración autónoma sobre nueva base.
* **Contexto**: En `encuesta_jovenes` (visible en la tabla) necesitamos trabajar solo con quienes estudian (`estudia == "Sí"`). De ellos necesitamos únicamente su `edad` y `comuna`.
* **Tarea**: Construye un flujo con `|>` que conserve a quienes estudian, seleccione `edad` y `comuna`, y guarde el resultado en `datos_preparados`.
* **Starter code**:
  ```r
  # Prepara los datos en datos_preparados usando |>, filter() y select():

  ```
* **Solución**:
  ```r
  datos_preparados <- encuesta_jovenes |>
    filter(estudia == "Sí") |>
    select(edad, comuna)
  ```
* **Checks**:
  - `object_exists`: `datos_preparados`.
  - `custom_r`: `nrow(datos_preparados) == 5 && ncol(datos_preparados) == 2`.
  - `custom_r`: `all(c("edad", "comuna") %in% names(datos_preparados))`.
