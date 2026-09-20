# Social R — Módulo 9: Ver relaciones entre dos cantidades
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Describe una sola variable cuantitativa usando distribución, centro y dispersión (Módulo 8).

### Capacidad después
Comprende la noción de par bivariado, genera e interpreta gráficos de dispersión (`plot`), evalúa dirección y fuerza, calcula e interpreta el coeficiente de correlación de Pearson (`cor`), prepara pares pertinentes y transfiere el flujo a una nueva base de datos.

### Pregunta central
¿Cómo exploramos si dos cantidades varían conjuntamente en un grupo de personas?

### Modelo mental
`MISMA PERSONA → PAR BIVARIADO (X, Y) → PUNTO EN EL PLANO (plot) → FORMA Y DIRECCIÓN → RESUMEN NUMÉRICO (cor) → INTERPRETAR`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_social` (E01, E02, E05, E06)
12 estudiantes universitarios:

| id | horas_estudio | puntaje_metodos | horas_trabajo | trabaja |
|:---|---:|---:|---:|:---|
| 1 | 2 | 59 | 20 | Sí |
| 2 | 4 | 68 | 35 | Sí |
| 3 | 3 | 58 | 0 | No |
| 4 | 6 | 64 | 25 | Sí |
| 5 | 5 | 62 | 40 | Sí |
| 6 | 8 | 75 | 0 | No |
| 7 | 7 | 65 | 30 | Sí |
| 8 | 10 | 64 | 45 | Sí |
| 9 | 9 | 74 | 0 | No |
| 10 | 11 | 84 | 38 | Sí |
| 11 | 4 | 59 | 0 | No |
| 12 | 6 | 73 | 32 | Sí |

### 2. Base de Transferencia: `encuesta_lectura` (E07)
10 participantes en un taller:

| id | minutos_lectura | puntaje_comprension |
|:---|---:|---:|
| 1 | 15 | 50 |
| 2 | 35 | 57 |
| 3 | 25 | 66 |
| 4 | 55 | 84 |
| 5 | 20 | 59 |
| 6 | 50 | 69 |
| 7 | 30 | 68 |
| 8 | 60 | 83 |
| 9 | 40 | 55 |
| 10 | 45 | 62 |

---

## Especificación Detallada de los 7 Ejercicios

### M9-E1 — Dos valores de la misma persona
* **Rol**: Práctica activa de construcción de pares bivariados.
* **Contexto**: Para estudiar si dos cantidades se relacionan, debemos observar ambos valores en la *misma* persona. Observa la fila 3 de `encuesta_social`: estudió 3 horas y obtuvo 58 puntos.
* **Tarea**: Guarda en `par_persona_3` un vector con las horas de estudio y el puntaje de la persona 3 (en ese orden).
* **Starter code**:
  ```r
  # Guarda las horas de estudio y puntaje de la persona 3:
  par_persona_3 <- c(___, ___)
  ```
* **Solución**:
  ```r
  par_persona_3 <- c(3, 58)
  ```
* **Checks**:
  - `object_value`: `par_persona_3 == c(3, 58)`.

---

### M9-E2 — Cada persona se vuelve un punto
* **Rol**: Práctica activa con `plot()`.
* **Contexto**: En un gráfico de dispersión o *scatterplot*, cada fila de la base se representa como un punto:
  - El eje horizontal (X) muestra la primera variable.
  - El eje vertical (Y) muestra la segunda variable.
  `plot(base$variable_x, base$variable_y)`
* **Tarea**: Genera un gráfico de dispersión que ubique las `horas_estudio` en el eje horizontal y el `puntaje_metodos` en el eje vertical usando `encuesta_social`.
* **Starter code**:
  ```r
  # Genera el gráfico de dispersión entre horas de estudio y puntaje:

  ```
* **Solución**:
  ```r
  plot(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)
  ```
* **Checks**:
  - `ast_call`: función `plot` con `encuesta_social$horas_estudio` y `encuesta_social$puntaje_metodos`.

---

### M9-E3 — ¿Hacia dónde va la relación?
* **Rol**: Práctica guiada de interpretación visual.
* **Contexto**: Observa la dirección de los puntos:
  - **Positiva**: a mayores valores en X, mayores valores en Y (la nube sube hacia la derecha).
  - **Negativa**: a mayores valores en X, menores valores en Y (la nube baja hacia la derecha).
* **Tarea**: Clasifica la relación observada en el Gráfico A y en el Gráfico B asignando `"positiva"` o `"negativa"` a `direccion_a` y `direccion_b`.
* **Starter code**:
  ```r
  # Clasifica la dirección de cada gráfico ("positiva" o "negativa"):
  direccion_a <- "___"
  direccion_b <- "___"
  ```
* **Solución**:
  ```r
  direccion_a <- "positiva"
  direccion_b <- "negativa"
  ```
* **Checks**:
  - `object_value`: `direccion_a == "positiva"`.
  - `object_value`: `direccion_b == "negativa"`.

---

### M9-E4 — No basta con la dirección
* **Rol**: Práctica guiada de evaluación de fuerza/dispersión.
* **Contexto**: Dos relaciones pueden ser ambas positivas, pero una puede tener sus puntos muy alineados y concentrados, mientras que en la otra los puntos están dispersos y difusos.
* **Tarea**: Observa los dos gráficos comparativos. Asigna a `grafico_mas_concentrado` la letra `"A"` o `"B"` según cuál exhibe los puntos más cercanos a una trayectoria definida.
* **Starter code**:
  ```r
  # Indica cuál gráfico tiene los puntos más concentrados ("A" o "B"):
  grafico_mas_concentrado <- "___"
  ```
* **Solución**:
  ```r
  grafico_mas_concentrado <- "A"
  ```
* **Checks**:
  - `object_value`: `grafico_mas_concentrado == "A"`.

---

### M9-E5 — Resume el patrón con un número
* **Rol**: Práctica activa con `cor()`.
* **Contexto**: El coeficiente de correlación lineal de Pearson ($r$) resume en un solo número entre $-1$ y $+1$ la dirección y la fuerza de la relación:
  `cor(base$x, base$y)`
  - Valores cercanos a $+1$ indican fuerte relación positiva.
  - Valores cercanos a $0$ indican ausencia de relación lineal.
  - Valores cercanos a $-1$ indican fuerte relación negativa.
* **Tarea**: Calcula la correlación entre `horas_estudio` y `puntaje_metodos` en `encuesta_social`.
* **Starter code**:
  ```r
  # Calcula la correlación entre horas_estudio y puntaje_metodos:

  ```
* **Solución**:
  ```r
  cor(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)
  ```
* **Checks**:
  - `ast_call`: función `cor` entre `encuesta_social$horas_estudio` y `encuesta_social$puntaje_metodos`.

---

### M9-E6 — Prepara los pares antes de correlacionar
* **Rol**: Pipeline combinado de preparación y correlación.
* **Contexto**: Antes de calcular la correlación, a menudo debemos aislar el grupo pertinente. Queremos estudiar la relación entre horas de trabajo e ingreso únicamente entre quienes efectivamente trabajan (`trabaja == "Sí"`).
* **Tarea**:
  1. Filtra las personas que trabajan y guarda el subgrupo en `datos_trabajan`.
  2. Calcula la correlación entre `horas_trabajo` e `ingreso_miles` en ese subgrupo.
* **Starter code**:
  ```r
  # 1. Filtra las personas que trabajan:
  datos_trabajan <- encuesta_social |>
    filter(trabaja == "Sí")

  # 2. Calcula la correlación entre horas_trabajo e ingreso_miles:

  ```
* **Solución**:
  ```r
  datos_trabajan <- encuesta_social |>
    filter(trabaja == "Sí")

  cor(datos_trabajan$horas_trabajo, datos_trabajan$ingreso_miles)
  ```
* **Checks**:
  - `object_exists`: `datos_trabajan`.
  - `ast_call`: llamada a `cor(datos_trabajan$horas_trabajo, datos_trabajan$ingreso_miles)`.

---

### M9-E7 — Otra pregunta, otra base
* **Rol**: Transferencia a un nuevo contexto.
* **Contexto**: Tienes a la vista `encuesta_lectura` con 10 personas participantes de un taller de lectura. Queremos saber si dedicar más minutos a leer se asocia con un mayor puntaje de comprensión.
* **Tarea**:
  1. Genera el gráfico de dispersión con `minutos_lectura` en X y `puntaje_comprension` en Y.
  2. Calcula el coeficiente de correlación entre ambas variables.
* **Starter code**:
  ```r
  # 1. Genera el gráfico de dispersión:

  # 2. Calcula la correlación entre ambas variables:

  ```
* **Solución**:
  ```r
  plot(encuesta_lectura$minutos_lectura, encuesta_lectura$puntaje_comprension)
  cor(encuesta_lectura$minutos_lectura, encuesta_lectura$puntaje_comprension)
  ```
* **Checks**:
  - `ast_call`: `plot(encuesta_lectura$minutos_lectura, encuesta_lectura$puntaje_comprension)`.
  - `ast_call`: `cor(encuesta_lectura$minutos_lectura, encuesta_lectura$puntaje_comprension)`.
