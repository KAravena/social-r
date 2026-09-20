# Social R — Módulo 13: De la pregunta al análisis
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Domina herramientas aisladas: filtrar, seleccionar, missing, categorías, cantidades, correlaciones bivariadas y matrices, tablas cruzadas y pruebas inferenciales (Módulos 1 a 12).

### Capacidad después
Integra de forma autónoma el ciclo analítico completo: clasifica la naturaleza de la pregunta sociológica, prepara los datos pertinentes con pipe (`|>`), selecciona las variables de interés, evalúa missing, ejecuta el análisis adecuado (cuantitativo o categórico) e interpreta resultados y evidencia estadística con mínima guía externa.

### Pregunta central
¿Cómo pasamos de una pregunta de investigación sustantiva a la secuencia completa de decisiones y código en R?

### Modelo mental
`PREGUNTA SUSTANTIVA → TIPO DE PROBLEMA (CANTIDADES O CATEGORÍAS) → PREPARACIÓN (filter + select) → REVISIÓN DE MISSING → ANÁLISIS BIVARIADO (plot/cor.test O table/chisq.test) → INTERPRETACIÓN SOCIOLÓGICA`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_vida_universitaria` (E01 a E04)
48 estudiantes universitarios con variables:
- `jornada` (Diurna, Vespertina)
- `horas_estudio`
- `autoeficacia_academica`
- `transporte_campus`
- `participa_organizacion`

Muestra de las primeras filas:

| id | jornada | horas_estudio | autoeficacia_academica | transporte_campus | participa_organizacion |
|:---|:---|---:|---:|:---|:---|
| 1 | Diurna | 2 | 59 | Metro | Sí |
| 2 | Diurna | 4 | 68 | Bus | No |
| 3 | Diurna | 3 | 58 | Bicicleta | Sí |
| 4 | Diurna | 6 | 64 | Bus | No |
| 5 | Diurna | 5 | 62 | Metro | No |
| 6 | Diurna | 8 | 75 | Bus | Sí |

### 2. Base del Checkpoint Final: `encuesta_vinculos_barriales` (E05)
40 personas residentes en un barrio con variables:
- `ocupado` ("Sí", "No")
- `participa_vecinal_01` (1 = Participa, 0 = No participa)
- `confianza_comunitaria` (escala 1 a 10)

Muestra de las primeras filas:

| id | ocupado | participa_vecinal_01 | confianza_comunitaria |
|:---|:---|---:|---:|
| 1 | Sí | 1 | 7 |
| 2 | Sí | 0 | 8 |
| 3 | Sí | 1 | 6 |
| 4 | Sí | 1 | 9 |
| 5 | Sí | 0 | 5 |
| 6 | No | 1 | 8 |

---

## Especificación Detallada de los 5 Ejercicios

### M13-E1 — ¿Qué tipo de problema es?
* **Rol**: Clasificación y decisión metodológica inicial.
* **Contexto**: Antes de escribir una sola línea de código en un proyecto real, debemos definir si cada variable representa cantidades o categorías:
  - **Problema 1**: "¿Las personas que dedican más horas de estudio semanal tienen mayor nivel de autoeficacia académica?"
  - **Problema 2**: "¿El medio de transporte que usa un estudiante se asocia con si participa o no en organizaciones universitarias?"
* **Tarea**: Clasifica cada problema asignando `"cuantitativo"` o `"categorico"` a `problema_1` y `problema_2`.
* **Starter code**:
  ```r
  # Clasifica cada problema como "cuantitativo" o "categorico":
  problema_1 <- "___"
  problema_2 <- "___"
  ```
* **Solución**:
  ```r
  problema_1 <- "cuantitativo"
  problema_2 <- "categorico"
  ```
* **Checks**:
  - `object_value`: `problema_1 == "cuantitativo"`.
  - `object_value`: `problema_2 == "categorico"`.

---

### M13-E2 — Prepara antes de analizar
* **Rol**: Práctica de preparación e higiene de datos.
* **Contexto**: Queremos analizar a los estudiantes de jornada `"Diurna"`, enfocándonos en `horas_estudio` y `autoeficacia_academica`. Debemos filtrar los casos pertinentes, seleccionar las variables y verificar si existen datos ausentes.
* **Tarea**:
  1. Filtra a quienes tienen `jornada == "Diurna"` y selecciona `horas_estudio` y `autoeficacia_academica`, guardando la base en `datos_estudio_diurno`.
  2. Cuenta los valores ausentes en ambas variables usando `sum(is.na())`.
* **Starter code**:
  ```r
  # 1. Filtra por jornada Diurna y selecciona las variables:
  datos_estudio_diurno <- encuesta_vida_universitaria |>
    filter(jornada == "Diurna") |>
    select(
      horas_estudio,
      autoeficacia_academica
    )

  # 2. Cuenta los valores ausentes en cada variable:

  ```
* **Solución**:
  ```r
  datos_estudio_diurno <- encuesta_vida_universitaria |>
    filter(jornada == "Diurna") |>
    select(
      horas_estudio,
      autoeficacia_academica
    )

  sum(is.na(datos_estudio_diurno$horas_estudio))
  sum(is.na(datos_estudio_diurno$autoeficacia_academica))
  ```
* **Checks**:
  - `object_exists`: `datos_estudio_diurno`.
  - `ast_call`: llamada a `sum(is.na(datos_estudio_diurno$horas_estudio))`.
  - `ast_call`: llamada a `sum(is.na(datos_estudio_diurno$autoeficacia_academica))`.

---

### M13-E3 — Responde una pregunta cuantitativa
* **Rol**: Integración cuantitativa completa (gráfico + inferencia).
* **Contexto**: Con los datos preparados en `datos_estudio_diurno`, respondemos la pregunta sobre horas de estudio y autoeficacia.
* **Tarea**:
  1. Genera el gráfico de dispersión con `horas_estudio` en X y `autoeficacia_academica` en Y.
  2. Ejecuta la prueba de correlación inferencial con `cor.test()`.
* **Starter code**:
  ```r
  # 1. Genera el gráfico de dispersión:

  # 2. Ejecuta la prueba de correlación inferencial:

  ```
* **Solución**:
  ```r
  plot(
    datos_estudio_diurno$horas_estudio,
    datos_estudio_diurno$autoeficacia_academica
  )

  cor.test(
    datos_estudio_diurno$horas_estudio,
    datos_estudio_diurno$autoeficacia_academica,
    method = "pearson"
  )
  ```
* **Checks**:
  - `ast_call`: llamada a `plot(...)`.
  - `ast_call`: llamada a `cor.test(...)`.

---

### M13-E4 — Responde una pregunta categórica
* **Rol**: Integración categórica completa (tabla + porcentajes + inferencia).
* **Contexto**: Ahora abordamos el Problema 2 sobre `transporte_campus` y `participa_organizacion` en `encuesta_vida_universitaria`.
* **Tarea**:
  1. Construye la tabla cruzada y guárdala en `tabla_participacion`.
  2. Calcula los porcentajes por fila con `prop.table()`.
  3. Ejecuta la prueba de Chi-cuadrado, guárdala en `prueba_participacion` y consulta sus frecuencias esperadas `$expected`.
* **Starter code**:
  ```r
  # 1. Tabla cruzada:
  tabla_participacion <- table(
    encuesta_vida_universitaria$transporte_campus,
    encuesta_vida_universitaria$participa_organizacion
  )

  # 2. Proporciones por fila:

  # 3. Prueba Chi-cuadrado y frecuencias esperadas:

  ```
* **Solución**:
  ```r
  tabla_participacion <- table(
    encuesta_vida_universitaria$transporte_campus,
    encuesta_vida_universitaria$participa_organizacion
  )

  prop.table(tabla_participacion, 1)

  prueba_participacion <- chisq.test(tabla_participacion)
  prueba_participacion
  prueba_participacion$expected
  ```
* **Checks**:
  - `object_exists`: `tabla_participacion`.
  - `object_exists`: `prueba_participacion`.
  - `ast_call`: `prop.table(tabla_participacion, 1)`.
  - `ast_call`: acceso a `prueba_participacion$expected`.

---

### M13-E5 — Checkpoint E: nueva base, nueva pregunta
* **Rol**: Checkpoint Final / Máxima Autonomía y Transferencia.
* **Contexto**: Tienes a la vista `encuesta_vinculos_barriales` con 40 residentes. Queremos responder una pregunta sociológica nueva: *Entre las personas ocupadas, ¿participar en organizaciones vecinales se asocia con una mayor confianza comunitaria?*
* **Tarea**:
  1. Prepara los datos en `datos_checkpoint`: filtra a quienes tienen `ocupado == "Sí"` y selecciona las variables `participa_vecinal_01` y `confianza_comunitaria`.
  2. Ejecuta la prueba de correlación `cor.test()` entre ambas variables en ese subgrupo.
* **Starter code**:
  ```r
  # Checkpoint Final: Nueva base, nueva pregunta
  # 1. Prepara los datos en datos_checkpoint (filtra ocupados y selecciona variables):

  # 2. Evalúa la correlación entre participa_vecinal_01 y confianza_comunitaria:

  ```
* **Solución**:
  ```r
  datos_checkpoint <- encuesta_vinculos_barriales |>
    filter(ocupado == "Sí") |>
    select(participa_vecinal_01, confianza_comunitaria)

  cor.test(datos_checkpoint$participa_vecinal_01, datos_checkpoint$confianza_comunitaria)
  ```
* **Checks**:
  - `object_exists`: `datos_checkpoint`.
  - `ast_call`: `cor.test(datos_checkpoint$participa_vecinal_01, datos_checkpoint$confianza_comunitaria)`.
