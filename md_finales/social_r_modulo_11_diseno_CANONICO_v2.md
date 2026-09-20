# Social R — Módulo 11: Trabajar con varias correlaciones
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Puede elegir y calcular una correlación e inferencia para un par de variables cuantitativas (Módulos 9 y 10).

### Capacidad después
Prepara subconjuntos de variables cuantitativas con `select()`, calcula e interpreta matrices de correlación completas con `cor()`, identifica pares únicos sin redundancia de espejo, gestiona datos faltantes en pares con `use = "pairwise.complete.obs"`, aplica correlación punto-biserial con variables binarias 0/1 y responde preguntas sustantivas leyendo matrices complejas.

### Pregunta central
¿Cómo exploramos simultáneamente múltiples asociaciones entre variables cuantitativas sin perdernos en redundancias ni errores de missing?

### Modelo mental
`SELECT VARIABLES → MATRIZ DE CORRELACIONES → DIAGONAL (1.0) Y ESPEJO (PARES ÚNICOS) → TRATAMIENTO DE MISSING (pairwise) → VARIABLE BINARIA (0/1) → INTERPRETAR PREGUNTAS SUSTANTIVAS`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_social` (E01, E02, E03, E05, E06)
12 estudiantes universitarios con variables:
- `edad`, `horas_estudio`, `horas_ocio`, `trabaja_01`, `ingreso_miles`.

| id | edad | horas_estudio | horas_ocio | trabaja_01 | ingreso_miles |
|:---|---:|---:|---:|---:|---:|
| 1 | 20 | 2 | 6.0 | 1 | 420 |
| 2 | 22 | 4 | 5.2 | 1 | 650 |
| 3 | 19 | 3 | 6.1 | 0 | 300 |
| 4 | 21 | 6 | 5.0 | 1 | 380 |
| 5 | 24 | 5 | 5.8 | 1 | 720 |
| 6 | 23 | 8 | 5.4 | 0 | 450 |
| 7 | 20 | 7 | 5.6 | 1 | 500 |
| 8 | 25 | 10 | 5.2 | 1 | 800 |
| 9 | 27 | 9 | 5.0 | 0 | 520 |
| 10 | 26 | 11 | 4.8 | 1 | 620 |
| 11 | 22 | 4 | 5.5 | 0 | 350 |
| 12 | 24 | 6 | 5.1 | 1 | 550 |

### 2. Base de Seguimiento con Missing: `seguimiento` (E04)
10 casos donde algunas personas faltaron a mediciones:

| id | horas_estudio | horas_sueno | estres |
|:---|---:|---:|---:|
| 1 | 2 | 8.1 | 3 |
| 2 | 4 | 7.4 | 5 |
| 3 | 3 | NA | 4 |
| 4 | 6 | 7.8 | 6 |
| 5 | 5 | 6.9 | NA |
| 6 | 8 | 7.2 | 8 |
| 7 | 7 | 6.5 | 5 |
| 8 | 10 | NA | 7 |
| 9 | 9 | 7.0 | NA |
| 10 | 6 | 7.6 | 4 |

---

## Especificación Detallada de los 6 Ejercicios

### M11-E1 — Elige las variables relevantes
* **Rol**: Práctica activa de preparación con `select()`.
* **Contexto**: Antes de calcular una matriz de correlaciones, debemos quedarnos únicamente con las variables numéricas que nos interesa correlacionar. Pasar variables de texto provocaría un error en R.
* **Tarea**: Selecciona las variables `edad`, `horas_estudio` y `horas_ocio` desde `encuesta_social` y guarda la base resultante en `analisis`.
* **Starter code**:
  ```r
  # Selecciona las 3 variables numéricas relevantes:
  analisis <- encuesta_social |>
    select(
      ___,
      ___,
      ___
    )
  ```
* **Solución**:
  ```r
  analisis <- encuesta_social |>
    select(
      edad,
      horas_estudio,
      horas_ocio
    )
  ```
* **Checks**:
  - `object_exists`: `analisis`.
  - `object_columns`: columnas `edad`, `horas_estudio`, `horas_ocio`.

---

### M11-E2 — Varias relaciones a la vez
* **Rol**: Práctica activa con matriz de correlaciones.
* **Contexto**: Si le pasamos a `cor()` una tabla con varias columnas numéricas, R calcula todas las combinaciones posibles de correlación y las organiza en una **matriz de correlaciones**:
  `cor(tabla, method = "pearson")`
* **Tarea**: Calcula la matriz de correlaciones de la base `analisis` que preparaste en el ejercicio anterior.
* **Starter code**:
  ```r
  # Calcula la matriz de correlaciones de analisis:

  ```
* **Solución**:
  ```r
  cor(analisis, method = "pearson")
  ```
* **Checks**:
  - `ast_call`: función `cor` aplicada a `analisis`.

---

### M11-E3 — No leas dos veces la misma relación
* **Rol**: Interpretación guiada de matrices de correlación.
* **Contexto**: En una matriz de correlaciones:
  - La diagonal principal siempre vale $1.0$ (cada variable consigo misma).
  - La mitad inferior es un espejo exacto de la mitad superior (la correlación entre X e Y es idéntica a la correlación entre Y y X).
* **Tarea**: En una matriz de $3 \times 3$ variables, ¿cuántos pares de correlación *únicos* e informativos existen (sin contar la diagonal ni los duplicados reflejados)? Asigna el número a `pares_unicos`.
* **Starter code**:
  ```r
  # Escribe cuántos pares únicos contiene una matriz de 3 variables:
  pares_unicos <- ___
  ```
* **Solución**:
  ```r
  pares_unicos <- 3
  ```
* **Checks**:
  - `object_value`: `pares_unicos == 3`.

---

### M11-E4 — No todos los pares usan los mismos casos
* **Rol**: Práctica activa con missing en matrices.
* **Contexto**: Cuando faltan datos en algunas variables, la opción por defecto `use = "everything"` produce `NA` en cualquier par afectado. Para aprovechar la mayor cantidad posible de información caso por caso, usamos:
  `use = "pairwise.complete.obs"`
  que calcula cada par de correlación usando todos los casos que tengan ambos datos disponibles.
* **Tarea**: Calcula la matriz de correlaciones de `seguimiento` usando `use = "pairwise.complete.obs"`.
* **Starter code**:
  ```r
  # Calcula la matriz usando pares completos caso por caso:

  ```
* **Solución**:
  ```r
  cor(seguimiento, use = "pairwise.complete.obs", method = "pearson")
  ```
* **Checks**:
  - `ast_call`: función `cor` con argumento `use = "pairwise.complete.obs"`.

---

### M11-E5 — Cuando una variable tiene dos categorías
* **Rol**: Práctica activa de correlación punto-biserial.
* **Contexto**: Si una variable categórica se codifica numéricamente como $0$ y $1$ (por ejemplo, `trabaja_01`: 0 = No trabaja, 1 = Sí trabaja), podemos correlacionarla directamente con una variable cuantitativa. Esto se conoce como **correlación punto-biserial** y su signo nos indica qué grupo tiene promedios más altos.
* **Tarea**: Calcula la correlación entre `trabaja_01` e `ingreso_miles` en `encuesta_social`.
* **Starter code**:
  ```r
  # Calcula la correlación entre la variable binaria e ingreso_miles:

  ```
* **Solución**:
  ```r
  cor(encuesta_social$trabaja_01, encuesta_social$ingreso_miles, method = "pearson")
  ```
* **Checks**:
  - `ast_call`: función `cor` entre `encuesta_social$trabaja_01` y `encuesta_social$ingreso_miles`.

---

### M11-E6 — Lee una matriz para responder una pregunta
* **Rol**: Transferencia y síntesis analítica.
* **Contexto**: Tienes a la vista `encuesta_social`. Queremos analizar conjuntamente tres variables: `trabaja_01`, `ingreso_miles` y `horas_ocio`.
* **Tarea**:
  1. Prepara `analisis_final` seleccionando `trabaja_01`, `ingreso_miles` y `horas_ocio`.
  2. Calcula la matriz de correlaciones de `analisis_final`.
  3. Ejecuta la prueba de correlación `cor.test()` para el par entre `trabaja_01` y `horas_ocio`.
* **Starter code**:
  ```r
  # 1. Selecciona las 3 variables:
  analisis_final <- encuesta_social |>
    select(
      ___,
      ___,
      ___
    )

  # 2. Calcula la matriz de correlaciones:

  # 3. Evalúa la inferencia entre trabaja_01 y horas_ocio:

  ```
* **Solución**:
  ```r
  analisis_final <- encuesta_social |>
    select(
      trabaja_01,
      ingreso_miles,
      horas_ocio
    )

  cor(analisis_final, method = "pearson")
  cor.test(encuesta_social$trabaja_01, encuesta_social$horas_ocio, method = "pearson")
  ```
* **Checks**:
  - `object_exists`: `analisis_final`.
  - `ast_call`: llamada a `cor(analisis_final)`.
  - `ast_call`: llamada a `cor.test` entre `trabaja_01` y `horas_ocio`.
