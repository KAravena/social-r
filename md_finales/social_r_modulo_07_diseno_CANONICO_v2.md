# Social R — Módulo 7: Describir categorías
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Trata valores ausentes con `is.na()` y `na.rm = TRUE` (Módulo 6).

### Capacidad después
Distingue variables cuantitativas de categóricas, construye tablas de conteo con `table()`, calcula proporciones y porcentajes con `prop.table()`, grafica frecuencias con `barplot()`, e interpreta la distribución de una variable categórica nueva de forma autónoma.

### Pregunta central
¿Cómo resumimos variables cualitativas o de grupo para saber cuántas personas pertenecen a cada categoría?

### Modelo mental
`CATEGORÍAS = GRUPOS / NOMBRES | CANTIDADES = NÚMEROS MEDIBLES`
`table(BASE$VARIABLE) → CONTEO DE FRECUENCIAS ABSOLUTAS`
`prop.table(TABLA) → PROPORCIONES (SUMAN 1.0) | * 100 → PORCENTAJES (%)`
`barplot(TABLA) → REPRESENTACIÓN VISUAL DE LAS BARRAS`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_social_demo` (E01 a E05)
8 casos con variables categóricas (`carrera`, `trabaja`):

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

### 2. Base de Transferencia: `encuesta_campus` (E06)
8 estudiantes con variable `satisfaccion`:

| id | carrera | transporte | satisfaccion |
|:---|:---|:---|:---|
| 1 | Sociología | Metro | Alta |
| 2 | Historia | Bus | Media |
| 3 | Antropología | Bicicleta | Alta |
| 4 | Sociología | Metro | Baja |
| 5 | Trabajo Social | A pie | Media |
| 6 | Antropología | Bus | Alta |
| 7 | Historia | Metro | Media |
| 8 | Sociología | Bicicleta | Alta |

---

## Especificación Detallada de los 6 Ejercicios

### M7-E1 — ¿Cantidad o categoría?
* **Rol**: Práctica activa de clasificación conceptual.
* **Contexto**: Para elegir el análisis correcto debemos distinguir dos tipos de información:
  - **Categoría**: nombres, grupos o etiquetas (ej. carrera, zona).
  - **Cantidad**: mediciones numéricas donde tiene sentido sumar o promediar (ej. horas, edad).
* **Tarea**: Clasifica cada variable asignando `"categoria"` o `"cantidad"` a `tipo_carrera`, `tipo_horas` y `tipo_zona_codigo`.
* **Starter code**:
  ```r
  # Clasifica cada variable con "categoria" o "cantidad":
  tipo_carrera <- "___"
  tipo_horas <- "___"
  tipo_zona_codigo <- "___"
  ```
* **Solución**:
  ```r
  tipo_carrera <- "categoria"
  tipo_horas <- "cantidad"
  tipo_zona_codigo <- "categoria"
  ```
* **Checks**:
  - `object_value`: `tipo_carrera == "categoria"`.
  - `object_value`: `tipo_horas == "cantidad"`.
  - `object_value`: `tipo_zona_codigo == "categoria"`.

---

### M7-E2 — ¿Cuántas personas respondieron cada cosa?
* **Rol**: Práctica activa con `table()`.
* **Contexto**: Para resumir una variable categórica contamos cuántos casos hay en cada grupo mediante una tabla de frecuencias:
  `table(base$variable)`
* **Tarea**: Construye la tabla de frecuencias de la variable `carrera` en `encuesta_social_demo` y guárdala en `tabla_carrera`.
* **Starter code**:
  ```r
  # Construye la tabla de frecuencias de carrera:

  ```
* **Solución**:
  ```r
  tabla_carrera <- table(encuesta_social_demo$carrera)
  ```
* **Checks**:
  - `object_exists`: `tabla_carrera`.
  - `custom_r`: `sum(tabla_carrera) == 8`.

---

### M7-E3 — Del conteo a la proporción
* **Rol**: Práctica activa con `prop.table()`.
* **Contexto**: Las frecuencias absolutas dependen del tamaño de la muestra. Para comparar grupos usamos proporciones relativas que suman 1.0:
  `prop.table(tabla)`
* **Tarea**: Calcula las proporciones de `tabla_carrera` usando `prop.table()` y guárdalas en `prop_carrera`.
* **Starter code**:
  ```r
  # Calcula proporciones de tabla_carrera:

  ```
* **Solución**:
  ```r
  prop_carrera <- prop.table(tabla_carrera)
  ```
* **Checks**:
  - `object_exists`: `prop_carrera`.
  - `custom_r`: `isTRUE(all.equal(sum(prop_carrera), 1))`.

---

### M7-E4 — Cuenta no es lo mismo que porcentaje
* **Rol**: Práctica guiada (conversión a porcentajes).
* **Contexto**: Para expresar las proporciones como porcentajes multiplicamos por 100:
  `prop.table(tabla) * 100`
* **Tarea**: Calcula los porcentajes de `tabla_carrera` multiplicando sus proporciones por 100 y guárdalos en `porc_carrera`.
* **Starter code**:
  ```r
  # Calcula los porcentajes de tabla_carrera:

  ```
* **Solución**:
  ```r
  porc_carrera <- prop.table(tabla_carrera) * 100
  ```
* **Checks**:
  - `object_exists`: `porc_carrera`.
  - `custom_r`: `isTRUE(all.equal(sum(porc_carrera), 100))`.

---

### M7-E5 — Ver la distribución
* **Rol**: Práctica activa con `barplot()`.
* **Contexto**: El gráfico de barras representa la altura de cada categoría proporcional a su frecuencia:
  `barplot(tabla)`
* **Tarea**: Genera el gráfico de barras de `tabla_carrera` usando `barplot()`.
* **Starter code**:
  ```r
  # Grafica las frecuencias de tabla_carrera:

  ```
* **Solución**:
  ```r
  barplot(tabla_carrera)
  ```
* **Checks**:
  - `custom_r`: `grepl('barplot\\s*\\(', .user_code)`.

---

### M7-E6 — Describe otra variable categórica
* **Rol**: Transferencia autónoma sobre nueva base.
* **Contexto**: La base `encuesta_campus` (visible en la tabla) contiene el nivel de satisfacción de 8 estudiantes (`satisfaccion`).
* **Tarea**:
  1. Construye la tabla de frecuencias de `satisfaccion` en `encuesta_campus` y guárdala en `tabla_satisfaccion`.
  2. Calcula los porcentajes de esa tabla multiplicando por 100 y guárdalos en `porc_satisfaccion`.
* **Starter code**:
  ```r
  # 1. Construye la tabla de frecuencias de satisfaccion:


  # 2. Calcula sus porcentajes (prop.table * 100) en porc_satisfaccion:

  ```
* **Solución**:
  ```r
  tabla_satisfaccion <- table(encuesta_campus$satisfaccion)
  porc_satisfaccion <- prop.table(tabla_satisfaccion) * 100
  ```
* **Checks**:
  - `object_exists`: `tabla_satisfaccion`, `porc_satisfaccion`.
  - `custom_r`: `sum(tabla_satisfaccion) == 8`.
  - `custom_r`: `isTRUE(all.equal(sum(porc_satisfaccion), 100))`.
