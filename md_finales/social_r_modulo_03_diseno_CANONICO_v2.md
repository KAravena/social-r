# Social R — Módulo 3: Hacer preguntas a los datos
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Reúne valores en un vector con `c()` y extrae elementos por posición con `[]` (Módulo 2).

### Capacidad después
Formula comparaciones con operadores relacionales (`>`, `==`), comprende la evaluación vectorizada de respuestas lógicas (`TRUE`/`FALSE`), almacena vectores lógicos, y selecciona elementos mediante condiciones en un solo paso (`vector[condicion]`).

### Pregunta central
¿Cómo le preguntamos a R cuáles valores cumplen un criterio de interés y cómo usamos esas respuestas para filtrar la información?

### Modelo mental
`VALOR > UMBRAL → TRUE / FALSE`
`VECTOR > UMBRAL → VECTOR LÓGICO (TRUE, FALSE, TRUE...)`
`VECTOR[VECTOR LÓGICO] → CONSERVA POSICIONES CON TRUE, DEJA FUERA FALSE`

---

## Datasets Contractuales y Objetos del Módulo

* **E01–E04**: Tiempos de viaje (`tiempos_viaje <- c(25, 40, 35, 50, 30)`).
* **E05**: Horas de estudio (`horas_estudio <- c(3, 5, 2, 4, 6)`).
* **E06**: Carreras de estudiantes (`carreras <- c("Sociología", "Historia", "Antropología", "Sociología")`).
* **E07 (Checkpoint A)**: Sesiones comunitarias (`sesiones <- c(6, 12, 8, 15, 10)`).

---

## Especificación Detallada de los 7 Ejercicios

### M3-E1 — De posiciones a preguntas
* **Rol**: Worked example + práctica inmediata.
* **Contexto**: En lugar de saber de antemano la posición de cada dato, podemos hacerle preguntas a R usando comparaciones:
  `35 > 30` responde `TRUE` (verdadero).
  `25 > 30` responde `FALSE` (falso).
* **Tarea**:
  1. Pregunta si `45` es mayor que `40`.
  2. Pregunta si `15` es mayor que `40`.
* **Starter code**:
  ```r
  # 1. Compara si 45 es mayor que 40:


  # 2. Compara si 15 es mayor que 40:

  ```
* **Solución**:
  ```r
  45 > 40
  15 > 40
  ```
* **Checks**:
  - `result_equals`: `FALSE`.

---

### M3-E2 — Pregunta a todos los valores
* **Rol**: Práctica guiada (evaluación vectorizada).
* **Contexto**: Si comparamos un vector completo contra un número, R le hace la pregunta a cada elemento por separado:
  `tiempos_viaje > 30`
  El resultado es una secuencia de respuestas `TRUE` y `FALSE`.
* **Tarea**: Ejecuta la comparación `tiempos_viaje > 30` y comprueba cómo R responde con un `TRUE` o `FALSE` para cada posición.
* **Starter code**:
  ```r
  # Pregunta qué tiempos superan 30 minutos:
  tiempos_viaje > 30
  ```
* **Solución**:
  ```r
  tiempos_viaje > 30
  ```
* **Checks**:
  - `result_equals`: `c(FALSE, TRUE, TRUE, TRUE, FALSE)`.

---

### M3-E3 — Guarda las respuestas
* **Rol**: Práctica guiada (vector lógico).
* **Contexto**: El resultado de una comparación puede guardarse en un objeto:
  `supera_30 <- tiempos_viaje > 30`
  Este objeto contiene valores lógicos (`TRUE` y `FALSE`).
* **Tarea**: Guarda la comparación `tiempos_viaje > 30` en el objeto `supera_30` y consúltalo.
* **Starter code**:
  ```r
  # Guarda la condición lógica en supera_30:


  # Consulta el nuevo objeto:

  ```
* **Solución**:
  ```r
  supera_30 <- tiempos_viaje > 30
  supera_30
  ```
* **Checks**:
  - `object_exists`: `supera_30`.
  - `object_value`: `supera_30 == c(FALSE, TRUE, TRUE, TRUE, FALSE)`.

---

### M3-E4 — TRUE conserva
* **Rol**: Práctica guiada (selección lógica).
* **Contexto**: Al poner un vector lógico dentro de los corchetes:
  `tiempos_viaje[supera_30]`
  R conserva las posiciones marcadas con `TRUE` y deja fuera las que tienen `FALSE`.
* **Tarea**: Selecciona los elementos de `tiempos_viaje` usando `supera_30` y guarda el resultado en `viajes_largos`.
* **Starter code**:
  ```r
  # Usa supera_30 dentro de corchetes para guardar los viajes largos:

  ```
* **Solución**:
  ```r
  viajes_largos <- tiempos_viaje[supera_30]
  ```
* **Checks**:
  - `object_exists`: `viajes_largos`.
  - `object_value`: `viajes_largos == c(40, 35, 50)`.

---

### M3-E5 — Selecciona tú
* **Rol**: Práctica autónoma (selección en un solo paso / fading).
* **Contexto**: Podemos seleccionar directamente escribiendo la condición dentro de los corchetes, sin crear un objeto intermedio:
  `vector[vector > umbral]`
* **Tarea**: Dispones del vector `horas_estudio <- c(3, 5, 2, 4, 6)`. Selecciona en un solo paso las horas mayores que 4 y guárdalas en `estudio_alto`.
* **Starter code**:
  ```r
  # Selecciona las horas mayores que 4 en estudio_alto:

  ```
* **Solución**:
  ```r
  estudio_alto <- horas_estudio[horas_estudio > 4]
  ```
* **Checks**:
  - `object_exists`: `estudio_alto`.
  - `object_value`: `estudio_alto == c(5, 6)`.

---

### M3-E6 — También podemos preguntar por texto
* **Rol**: Práctica guiada (comparación de categorías con `==`).
* **Contexto**: Para comparar texto usamos el operador de igualdad `==` con comillas:
  `carreras == "Sociología"`
  Devuelve `TRUE` donde coincide exactamente el texto.
* **Tarea**:
  1. Compara qué elementos de `carreras` coinciden con `"Sociología"` y guárdalo en `es_sociologia`.
  2. Usa esa condición para filtrar las carreras correspondientes en `solo_sociologia`.
* **Starter code**:
  ```r
  # 1. Guarda la comparación con "Sociología" en es_sociologia:


  # 2. Filtra carreras usando es_sociologia en solo_sociologia:

  ```
* **Solución**:
  ```r
  es_sociologia <- carreras == "Sociología"
  solo_sociologia <- carreras[es_sociologia]
  ```
* **Checks**:
  - `object_exists`: `es_sociologia`, `solo_sociologia`.
  - `object_value`: `es_sociologia == c(TRUE, FALSE, FALSE, TRUE)`.
  - `object_value`: `solo_sociologia == c("Sociología", "Sociología")`.

---

### M3-E7 — Checkpoint A: encuentra lo que buscas
* **Rol**: Checkpoint / Integración autónoma del Módulo 3.
* **Contexto**: Cinco personas registraron **6, 12, 8, 15 y 10** sesiones de participación comunitaria.
* **Tarea**:
  Usando lo aprendido:
  1. Guarda esos valores en un objeto llamado `sesiones`.
  2. Identifica cuáles son mayores que 8 y guarda esa respuesta en `mas_de_ocho`.
  3. Usa esa respuesta para guardar las sesiones seleccionadas en `seleccionadas`.
* **Starter code**:
  ```r
  # 1. Guarda los cinco valores en sesiones:


  # 2. Identifica cuáles superan 8 en mas_de_ocho:


  # 3. Guarda las sesiones seleccionadas en seleccionadas:

  ```
* **Solución**:
  ```r
  sesiones <- c(6, 12, 8, 15, 10)
  mas_de_ocho <- sesiones > 8
  seleccionadas <- sesiones[mas_de_ocho]
  ```
* **Checks**:
  - `object_exists`: `sesiones`, `mas_de_ocho`, `seleccionadas`.
  - `object_value`: `sesiones == c(6, 12, 8, 15, 10)`.
  - `object_value`: `mas_de_ocho == c(FALSE, TRUE, FALSE, TRUE, TRUE)`.
  - `object_value`: `seleccionadas == c(12, 15, 10)`.
