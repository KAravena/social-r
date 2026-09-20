# Social R — Módulo 12: Relacionar categorías
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Puede describir una variable categórica mediante tablas de frecuencias y porcentajes (Módulo 7).

### Capacidad después
Cruza dos variables categóricas en tablas de contingencia (`table`), calcula e interpreta porcentajes condicionales por fila (`prop.table`), comprende la noción intuitiva de independencia (lo observado vs lo esperado), aplica la prueba de Chi-cuadrado (`chisq.test`), inspecciona frecuencias observadas y esperadas, distingue significancia estadística de fuerza de asociación y transfiere el análisis a una nueva encuesta.

### Pregunta central
¿Cómo exploramos si pertenecer a un grupo se asocia con responder de forma distinta en otra variable cualitativa?

### Modelo mental
`TABLA CRUZADA (OBSERVADO) → PORCENTAJES POR FILA → COMPARAR CON LO ESPERADO SIN ASOCIACIÓN → PRUEBA CHI-CUADRADO (chisq.test) → OBSERVADO VS ESPERADO → INTERPRETAR CON RIGOR`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_participacion` (E01 a E05)
60 personas consultadas sobre participación en organizaciones y medio de transporte al campus.

Distribución observada conjunta:

| Participación | Metro | Bus | Bicicleta | Total |
|:---|---:|---:|---:|---:|
| **Participa** | 12 | 20 | 8 | 40 |
| **No participa** | 3 | 10 | 7 | 20 |
| **Total** | 15 | 30 | 15 | 60 |

### 2. Base de Transferencia: `encuesta_comunidad` (E07)
80 personas consultadas sobre su `zona_residencia` (Norte, Centro, Sur) y su nivel de `actividad_comunitaria` (Alta, Media, Baja).

---

## Especificación Detallada de los 7 Ejercicios

### M12-E1 — Dos variables categóricas
* **Rol**: Práctica activa con tablas cruzadas (`table`).
* **Contexto**: Para saber si dos variables cualitativas están asociadas, cruzamos sus categorías en una **tabla de contingencia** o tabla cruzada:
  `table(base$variable_fila, base$variable_columna)`
* **Tarea**: Construye la tabla cruzada entre `participacion_organizacion` y `transporte_campus` en `encuesta_participacion`, guárdala en `tabla` y muéstrala en consola.
* **Starter code**:
  ```r
  # Construye la tabla cruzada entre ambas variables:
  tabla <- table(
    ___,
    ___
  )

  tabla
  ```
* **Solución**:
  ```r
  tabla <- table(
    encuesta_participacion$participacion_organizacion,
    encuesta_participacion$transporte_campus
  )

  tabla
  ```
* **Checks**:
  - `object_exists`: `tabla`.
  - `ast_call`: función `table` con ambas variables.

---

### M12-E2 — Comparar porcentajes
* **Rol**: Práctica activa con porcentajes por fila.
* **Contexto**: Como los grupos suelen tener tamaños distintos (en nuestra base hay 40 personas que participan y solo 20 que no), comparar números absolutos confunde. Debemos calcular **porcentajes condicionales por fila**:
  `prop.table(tabla, margin = 1)`
  donde cada fila suma $1.0$ ($100\%$).
* **Tarea**: Calcula las proporciones por fila de `tabla` usando el argumento `margin = 1`.
* **Starter code**:
  ```r
  # Calcula las proporciones por fila:

  ```
* **Solución**:
  ```r
  prop.table(tabla, margin = 1)
  ```
* **Checks**:
  - `ast_call`: función `prop.table` con `tabla` y margen por fila (`1` o `margin = 1`).

---

### M12-E3 — ¿Qué esperaríamos sin asociación?
* **Rol**: Razonamiento sustantivo sobre independencia.
* **Contexto**: En el total de la muestra, 15 de 60 personas usan Metro ($25\%$). Si participar en una organización no tuviera *ninguna relación* con el medio de transporte (independencia completa), esperaríamos que en ambos grupos el uso del Metro fuera exactamente el mismo $25\%$.
* **Tarea**: Asigna a `porcentaje_esperado_metro` el porcentaje global esperado ($25$).
* **Starter code**:
  ```r
  # ¿Qué porcentaje usaría Metro si no hubiera relación?
  porcentaje_esperado_metro <- ___
  ```
* **Solución**:
  ```r
  porcentaje_esperado_metro <- 25
  ```
* **Checks**:
  - `object_value`: `porcentaje_esperado_metro == 25`.

---

### M12-E4 — Medir observado vs esperado
* **Rol**: Práctica activa con Chi-cuadrado (`chisq.test`).
* **Contexto**: La prueba de Chi-cuadrado ($\chi^2$) compara sistemáticamente las frecuencias observadas en cada celda contra las que esperaríamos si las variables fueran independientes. Si las diferencias son grandes, el p-value será pequeño, aportando evidencia contra la hipótesis nula de independencia:
  `prueba <- chisq.test(tabla)`
* **Tarea**: Ejecuta la prueba de Chi-cuadrado sobre `tabla`, guárdala en `prueba` y muéstrala en consola.
* **Starter code**:
  ```r
  # Ejecuta la prueba de Chi-cuadrado y guárdala en prueba:

  ```
* **Solución**:
  ```r
  prueba <- chisq.test(tabla)
  prueba
  ```
* **Checks**:
  - `object_exists`: `prueba`.
  - `ast_call`: función `chisq.test` aplicada a `tabla`.

---

### M12-E5 — Mira lo que esperaba la prueba
* **Rol**: Práctica activa de inspección de objetos inferenciales.
* **Contexto**: El objeto retornado por `chisq.test()` contiene tanto las frecuencias reales que ocurrieron (`prueba$observed`) como las frecuencias teóricas calculadas bajo independencia (`prueba$expected`).
* **Tarea**: Consulta las frecuencias observadas y luego las frecuencias esperadas del objeto `prueba`.
* **Starter code**:
  ```r
  # 1. Consulta las frecuencias observadas:
  prueba$observed

  # 2. Ahora consulta las frecuencias esperadas:

  ```
* **Solución**:
  ```r
  prueba$observed
  prueba$expected
  ```
* **Checks**:
  - `ast_call`: acceso a `prueba$expected`.

---

### M12-E6 — ¿Significativo significa grande?
* **Rol**: Interpretación crítica entre p-value y fuerza de asociación.
* **Contexto**: Al igual que en correlaciones cuantitativas, una prueba $\chi^2$ con $p < 0.05$ solo nos dice que el patrón difícilmente se debe al azar, pero no garantiza que la diferencia entre porcentajes sea sociológicamente grande:
  - **Tabla 1**: Diferencias mínimas de $2\%$ entre grupos, pero muestra masiva de $n = 5000$ ($p = 0.03$).
  - **Tabla 2**: Diferencias sustantivas de $25\%$ entre grupos con muestra moderada ($p = 0.01$).
* **Tarea**: Asigna a `tabla_asociacion_mas_fuerte` la tabla que presenta una asociación sustantiva real más intensa (`"Tabla 1"` o `"Tabla 2"`).
* **Starter code**:
  ```r
  # Identifica cuál tabla muestra la asociación más fuerte:
  tabla_asociacion_mas_fuerte <- "___"
  ```
* **Solución**:
  ```r
  tabla_asociacion_mas_fuerte <- "Tabla 2"
  ```
* **Checks**:
  - `object_value`: `tabla_asociacion_mas_fuerte == "Tabla 2"`.

---

### M12-E7 — Otra asociación categórica
* **Rol**: Transferencia a una nueva base de datos.
* **Contexto**: Tienes a la vista `encuesta_comunidad` con 80 residentes. Queremos analizar si la `zona_residencia` se asocia con el nivel de `actividad_comunitaria`.
* **Tarea**:
  1. Construye la tabla cruzada entre `zona_residencia` y `actividad_comunitaria` y guárdala en `tabla_comunidad`.
  2. Calcula las proporciones por fila con `prop.table()`.
  3. Ejecuta la prueba `chisq.test()` sobre la tabla y guárdala en `prueba_comunidad`.
  4. Muestra `prueba_comunidad` y sus frecuencias esperadas `prueba_comunidad$expected`.
* **Starter code**:
  ```r
  # 1. Construye la tabla cruzada:

  # 2. Proporciones por fila:

  # 3. Prueba de Chi-cuadrado y frecuencias esperadas:

  ```
* **Solución**:
  ```r
  tabla_comunidad <- table(
    encuesta_comunidad$zona_residencia,
    encuesta_comunidad$actividad_comunitaria
  )

  prop.table(tabla_comunidad, margin = 1)

  prueba_comunidad <- chisq.test(tabla_comunidad)
  prueba_comunidad
  prueba_comunidad$expected
  ```
* **Checks**:
  - `object_exists`: `tabla_comunidad`.
  - `object_exists`: `prueba_comunidad`.
  - `ast_call`: `prop.table(tabla_comunidad, ...)`.
  - `ast_call`: acceso a `prueba_comunidad$expected`.
