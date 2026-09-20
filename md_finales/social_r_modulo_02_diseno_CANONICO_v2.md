# Social R — Módulo 2: Trabajar con varios valores
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Guarda y reutiliza valores individuales en objetos con `<-` (Módulo 1).

### Capacidad después
Comprende que un **vector** reúne una secuencia ordenada de valores del mismo tipo usando `c()`, calcula resúmenes sobre el conjunto con `sum()` y `length()`, y recupera posiciones específicas mediante corchetes `[]` de forma individual o combinada (`c(1, 3)`).

### Pregunta central
¿Cómo reunimos varios valores de la misma característica en un solo objeto y cómo extraemos posiciones específicas?

### Modelo mental
`VARIOS VALORES → c(v1, v2, v3) → VECTOR (SECUENCIA CON POSICIONES 1, 2, 3...)`
`VECTOR[1] → PRIMER VALOR | VECTOR[c(1, 3)] → SUBCONJUNTO DE POSICIONES`

---

## Datasets Contractuales y Objetos del Módulo

* **E01–E05**: Tiempos de viaje (`tiempos_viaje <- c(25, 40, 35, 50, 30)`).
* **E01–E02**: Edades de estudiantes (`edades <- c(20, 22, 19, 21)`).
* **E06–E07**: Horas de estudio (`horas_estudio <- c(3, 5, 2, 4)`).

---

## Especificación Detallada de los 7 Ejercicios

### M2-E1 — De uno a varios
* **Rol**: Worked example + práctica inmediata.
* **Contexto**: En ciencias sociales rara vez analizamos un solo valor. Para reunir varias respuestas en un solo objeto usamos la función `c()` (de *combinar*):
  `tiempos_viaje <- c(25, 40, 35, 50, 30)`
  Esta secuencia ordenada de valores se llama **vector**.
* **Tarea**: Siguiendo el ejemplo, crea un vector con las edades de cuatro personas (`20, 22, 19, 21`) y guárdalo en `edades`.
* **Starter code**:
  ```r
  # Crea el vector con las cuatro edades y guárdalo en edades:

  ```
* **Solución**:
  ```r
  edades <- c(20, 22, 19, 21)
  ```
* **Checks**:
  - `object_exists`: `edades`.
  - `object_value`: `edades == c(20, 22, 19, 21)`.

---

### M2-E2 — Tu primer vector
* **Rol**: Práctica guiada.
* **Contexto**: Cada número dentro de `c()` se separa con una coma. El orden en que los escribes se conserva exactamente.
* **Tarea**: Cinco participantes asistieron a 3, 5, 2, 4 y 6 sesiones de un taller. Guarda esos cinco valores en un vector llamado `sesiones`.
* **Starter code**:
  ```r
  # Guarda las sesiones (3, 5, 2, 4, 6) en el objeto sesiones:

  ```
* **Solución**:
  ```r
  sesiones <- c(3, 5, 2, 4, 6)
  ```
* **Checks**:
  - `object_exists`: `sesiones`.
  - `object_value`: `sesiones == c(3, 5, 2, 4, 6)`.

---

### M2-E3 — Usa todos los valores juntos
* **Rol**: Práctica guiada (operaciones agregadas).
* **Contexto**: Al aplicar una función como `sum()` sobre un vector, R suma automáticamente todos sus elementos:
  `sum(tiempos_viaje)`
* **Tarea**: Dispones del vector `tiempos_viaje`. Calcula la suma total de minutos y guárdala en el objeto `total_minutos`.
* **Starter code**:
  ```r
  # Calcula la suma de tiempos_viaje y guárdala en total_minutos:

  ```
* **Solución**:
  ```r
  total_minutos <- sum(tiempos_viaje)
  ```
* **Checks**:
  - `object_exists`: `total_minutos`.
  - `object_value`: `total_minutos == 180`.

---

### M2-E4 — ¿Qué hay en esta posición?
* **Rol**: Práctica guiada (indexación por posición simple).
* **Contexto**: Para extraer un valor específico según su orden en el vector usamos corchetes `[]` con el número de posición:
  `vector[1]` recupera el primer elemento.
* **Tarea**: Extrae el primer valor del vector `tiempos_viaje` y guárdalo en `primer_tiempo`.
* **Starter code**:
  ```r
  # Extrae la primera posición de tiempos_viaje:

  ```
* **Solución**:
  ```r
  primer_tiempo <- tiempos_viaje[1]
  ```
* **Checks**:
  - `object_exists`: `primer_tiempo`.
  - `object_value`: `primer_tiempo == 25`.

---

### M2-E5 — Más de una posición
* **Rol**: Práctica guiada (indexación múltiple).
* **Contexto**: Para pedir más de una posición a la vez, combinamos las posiciones deseadas dentro de los corchetes usando `c()`:
  `vector[c(1, 3)]` recupera los elementos 1 y 3.
* **Tarea**: Extrae la primera y la tercera posición de `tiempos_viaje` y guárdalas en `tiempos_extremos`.
* **Starter code**:
  ```r
  # Extrae las posiciones 1 y 3 de tiempos_viaje:

  ```
* **Solución**:
  ```r
  tiempos_extremos <- tiempos_viaje[c(1, 3)]
  ```
* **Checks**:
  - `object_exists`: `tiempos_extremos`.
  - `object_value`: `tiempos_extremos == c(25, 35)`.

---

### M2-E6 — Vuelve a usar lo aprendido
* **Rol**: Práctica autónoma / Repetición.
* **Contexto**: Dispones del vector `edades <- c(20, 22, 19, 21)`.
* **Tarea**:
  1. Consulta la cantidad de elementos de `edades` usando `length(edades)`.
  2. Extrae la segunda y cuarta edad y guárdalas en `edades_pares`.
* **Starter code**:
  ```r
  # 1. Consulta la cantidad de elementos de edades con length():


  # 2. Extrae las posiciones 2 y 4 de edades en edades_pares:

  ```
* **Solución**:
  ```r
  length(edades)
  edades_pares <- edades[c(2, 4)]
  ```
* **Checks**:
  - `object_exists`: `edades_pares`.
  - `object_value`: `edades_pares == c(22, 21)`.

---

### M2-E7 — Encuentra la información que piden (Checkpoint)
* **Rol**: Checkpoint / Integración autónoma.
* **Contexto**: Cuatro estudiantes registraron las siguientes horas de estudio semanal:

| Persona | Horas de estudio |
|:---|---:|
| Estudiante 1 | 3 |
| Estudiante 2 | 5 |
| Estudiante 3 | 2 |
| Estudiante 4 | 4 |

Dispones del vector `horas_estudio <- c(3, 5, 2, 4)`.
* **Tarea**:
  1. Extrae las horas del Estudiante 2 y guárdalas en `horas_estudiante_2`.
  2. Extrae las horas del Estudiante 1 y Estudiante 4 y guárdalas en `horas_seleccionadas`.
* **Starter code**:
  ```r
  # 1. Extrae la posición 2 de horas_estudio en horas_estudiante_2:


  # 2. Extrae las posiciones 1 y 4 de horas_estudio en horas_seleccionadas:

  ```
* **Solución**:
  ```r
  horas_estudiante_2 <- horas_estudio[2]
  horas_seleccionadas <- horas_estudio[c(1, 4)]
  ```
* **Checks**:
  - `object_exists`: `horas_estudiante_2`, `horas_seleccionadas`.
  - `object_value`: `horas_estudiante_2 == 5`.
  - `object_value`: `horas_seleccionadas == c(3, 4)`.
