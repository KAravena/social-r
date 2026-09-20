# Social R — Módulo 10: Elegir y evaluar una correlación
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Puede generar un scatterplot y calcular correlación de Pearson descriptivamente (Módulo 9).

### Capacidad después
Distingue relaciones lineales de relaciones curvas monótonas, elige justificadamente entre Pearson y Spearman, aplica e interpreta pruebas inferenciales con `cor.test()`, distingue p-value de tamaño de efecto y toma decisiones metodológicas autónomas.

### Pregunta central
¿Cómo decidimos qué correlación usar y cómo sabemos si el patrón observado en la muestra entrega evidencia contra la hipótesis nula de no asociación?

### Modelo mental
`FORMA VISUAL (RECTA vs CURVA MONÓTONA) → MÉTODO (PEARSON vs SPEARMAN) → cor.test() → ESTIMACIÓN (r) + EVIDENCIA (p-value) → INTERPRETAR CON RIGOR`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Vectores Monótonos: `x_curva` e `y_curva` (E01, E02)
Relación exponencial monótona estricta:
- `x_curva <- 1:8`
- `y_curva <- c(2, 5, 11, 20, 36, 65, 118, 215)`

### 2. Base Central: `encuesta_social` (E04, E07)
12 estudiantes universitarios con `horas_estudio`, `puntaje_metodos`, `edad`.

### 3. Base de Transferencia: `encuesta_emprendimiento` (E08 Checkpoint D)
8 emprendimientos donde las ventas crecen de forma fuertemente acelerada según los años:

| id | antiguedad_anos | ventas_mensuales |
|:---|---:|---:|
| 1 | 1 | 100 |
| 2 | 2 | 110 |
| 3 | 3 | 120 |
| 4 | 4 | 140 |
| 5 | 5 | 180 |
| 6 | 6 | 300 |
| 7 | 7 | 800 |
| 8 | 8 | 3000 |

---

## Especificación Detallada de los 8 Ejercicios

### M10-E1 — No todas las relaciones son lineales
* **Rol**: Worked example y contraste conceptual.
* **Contexto**: Pearson mide qué tan bien los puntos se ajustan a una *línea recta*. Pero muchas relaciones en ciencias sociales son curvas monótonas: una variable siempre sube cuando la otra sube, pero a ritmo acelerado. En esos casos, el orden o jerarquía de los casos se preserva perfectamente.
  `cor(x, y, method = "spearman")` calcula la correlación por rangos.
* **Tarea**: Observa en el editor el cálculo de Pearson sobre los datos curvos ($r \approx 0.88$). Luego calcula la correlación de Spearman para comprobar que el orden de los casos se cumple al 100% ($r_s = 1.0$).
* **Starter code**:
  ```r
  # 1. Pearson mide ajuste a una recta:
  cor(x_curva, y_curva, method = "pearson")

  # 2. Ahora calcula Spearman para evaluar el orden de los casos:

  ```
* **Solución**:
  ```r
  cor(x_curva, y_curva, method = "pearson")
  cor(x_curva, y_curva, method = "spearman")
  ```
* **Checks**:
  - `ast_call`: `cor(x_curva, y_curva, method = "spearman")`.

---

### M10-E2 — Una relación basada en rangos
* **Rol**: Práctica activa de cálculo de Spearman.
* **Contexto**: Cuando sospechamos que la relación no es recta o hay valores extremos que distorsionarían una recta, usamos Spearman indicando el argumento explícito:
  `cor(x, y, method = "spearman")`
* **Tarea**: Calcula la correlación de Spearman entre `x_curva` e `y_curva` para verificar la asociación basada en jerarquías.
* **Starter code**:
  ```r
  # Calcula la correlación de Spearman entre x_curva e y_curva:

  ```
* **Solución**:
  ```r
  cor(x_curva, y_curva, method = "spearman")
  ```
* **Checks**:
  - `ast_call`: `cor(x_curva, y_curva, method = "spearman")`.

---

### M10-E3 — Elige antes de ejecutar
* **Rol**: Decisión metodológica a partir de gráficos.
* **Contexto**: Nunca elegimos el método a ciegas:
  - Nube en forma de recta $\rightarrow$ `"pearson"`.
  - Nube en curva ascendente/descendente $\rightarrow$ `"spearman"`.
  - Nube en forma de U o sin orden monótono $\rightarrow$ `"ninguno"`.
* **Tarea**: Observa los Gráficos A, B y C visibles en el panel. Asigna a `metodo_a`, `metodo_b` y `metodo_c` la opción correspondiente (`"pearson"`, `"spearman"` o `"ninguno"`).
* **Starter code**:
  ```r
  # Elige el método para cada gráfico ("pearson", "spearman" o "ninguno"):
  metodo_a <- "___"
  metodo_b <- "___"
  metodo_c <- "___"
  ```
* **Solución**:
  ```r
  metodo_a <- "pearson"
  metodo_b <- "spearman"
  metodo_c <- "ninguno"
  ```
* **Checks**:
  - `object_value`: `metodo_a == "pearson"`.
  - `object_value`: `metodo_b == "spearman"`.
  - `object_value`: `metodo_c == "ninguno"`.

---

### M10-E4 — De la muestra a la inferencia
* **Rol**: Práctica activa con `cor.test()`.
* **Contexto**: En una muestra podemos observar un coeficiente de correlación $r = 0.65$. ¿Es esa correlación evidencia creíble de una relación real en la población, o podría deberse al azar del muestreo?
  `cor.test(x, y)`
  calcula la estimación muestral y entrega el **p-value**, que mide la compatibilidad de los datos observados con la hipótesis nula de que en la población no existe relación ($H_0: \rho = 0$).
* **Tarea**: Realiza la prueba de correlación entre `horas_estudio` y `puntaje_metodos` en `encuesta_social`.
* **Starter code**:
  ```r
  # Realiza la prueba inferencial con cor.test:

  ```
* **Solución**:
  ```r
  cor.test(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)
  ```
* **Checks**:
  - `ast_call`: función `cor.test` entre `encuesta_social$horas_estudio` y `encuesta_social$puntaje_metodos`.

---

### M10-E5 — ¿Qué dice la hipótesis nula?
* **Rol**: Interpretación sustantiva conceptual.
* **Contexto**: Es crucial evitar malinterpretaciones habituales del p-value:
  - El p-value **NO** es la probabilidad de que la hipótesis nula sea verdadera.
  - El p-value mide qué tan incompatibles o extremos son los datos observados si la hipótesis nula fuese cierta.
* **Tarea**: Evalúa las dos afirmaciones asignando `TRUE` o `FALSE`:
  1. `afirmacion_probabilidad_h0`: "¿El p-value indica la probabilidad de que $H_0$ sea verdadera?"
  2. `afirmacion_incompatibilidad`: "¿Un p-value pequeño indica que los datos son poco compatibles con un modelo donde no hay relación?"
* **Starter code**:
  ```r
  # Responde con TRUE o FALSE a cada afirmación:
  afirmacion_probabilidad_h0 <- ___
  afirmacion_incompatibilidad <- ___
  ```
* **Solución**:
  ```r
  afirmacion_probabilidad_h0 <- FALSE
  afirmacion_incompatibilidad <- TRUE
  ```
* **Checks**:
  - `object_value`: `afirmacion_probabilidad_h0 == FALSE`.
  - `object_value`: `afirmacion_incompatibilidad == TRUE`.

---

### M10-E6 — Magnitud y evidencia son cosas distintas
* **Rol**: Interpretación y razonamiento crítico.
* **Contexto**: Considera dos investigaciones independientes que estudian la misma relación y obtienen exactamente la misma correlación muestral $r = 0.50$:
  - **Estudio A**: $n = 10$, $p = 0.14$ (muestra pequeña, alta incertidumbre).
  - **Estudio B**: $n = 500$, $p < 0.001$ (muestra grande, alta precisión).
* **Tarea**: Asigna a `estudio_menor_p` el estudio con mayor evidencia contra la hipótesis nula (`"Estudio A"` o `"Estudio B"`), y a `estudio_mayor_precision` el estudio con estimación más precisa.
* **Starter code**:
  ```r
  # Identifica cuál estudio tiene menor p-value y cuál tiene mayor precisión:
  estudio_menor_p <- "___"
  estudio_mayor_precision <- "___"
  ```
* **Solución**:
  ```r
  estudio_menor_p <- "Estudio B"
  estudio_mayor_precision <- "Estudio B"
  ```
* **Checks**:
  - `object_value`: `estudio_menor_p == "Estudio B"`.
  - `object_value`: `estudio_mayor_precision == "Estudio B"`.

---

### M10-E7 — Mira, elige y evalúa
* **Rol**: Pipeline combinado de visualización, decisión e inferencia.
* **Contexto**: Antes de extraer conclusiones sobre la relación entre `edad` y `horas_estudio` en `encuesta_social`:
  1. Miramos el gráfico de dispersión para confirmar su forma lineal.
  2. Ejecutamos la prueba de correlación inferencial.
* **Tarea**:
  1. Genera el gráfico de dispersión de `edad` en X y `horas_estudio` en Y.
  2. Ejecuta la prueba `cor.test()` entre ambas variables.
* **Starter code**:
  ```r
  # 1. Genera el gráfico de dispersión:

  # 2. Ejecuta la prueba cor.test:

  ```
* **Solución**:
  ```r
  plot(encuesta_social$edad, encuesta_social$horas_estudio)
  cor.test(encuesta_social$edad, encuesta_social$horas_estudio)
  ```
* **Checks**:
  - `ast_call`: llamada a `plot(encuesta_social$edad, encuesta_social$horas_estudio)`.
  - `ast_call`: llamada a `cor.test(encuesta_social$edad, encuesta_social$horas_estudio)`.

---

### M10-E8 — Checkpoint D: decide y justifica
* **Rol**: Checkpoint D / Transferencia autónoma.
* **Contexto**: Tienes a la vista la base `encuesta_emprendimiento`. Observa cómo las ventas aumentan muy lentamente al inicio (100, 110, 120...) y luego se disparan exponencialmente (800, 3000). Es una trayectoria monótona claramente curva.
* **Tarea**: Evalúa la relación entre `antiguedad_anos` y `ventas_mensuales` aplicando la prueba de correlación de Spearman (`method = "spearman"`).
* **Starter code**:
  ```r
  # Aplica la prueba de correlación de Spearman en encuesta_emprendimiento:

  ```
* **Solución**:
  ```r
  cor.test(encuesta_emprendimiento$antiguedad_anos, encuesta_emprendimiento$ventas_mensuales, method = "spearman")
  ```
* **Checks**:
  - `ast_call`: `cor.test(encuesta_emprendimiento$antiguedad_anos, encuesta_emprendimiento$ventas_mensuales, method = "spearman")`.
