# Social R — Módulo 4: Entender una base de datos
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Comprende vectores como secuencias ordenadas de valores y puede filtrarlos mediante comparaciones lógicas y corchetes (Módulos 1 a 3).

### Capacidad después
Comprende cómo varias características de los mismos casos se organizan en filas y columnas en un **data frame**, distingue **caso/fila** y **variable/columna**, inspecciona tablas con `head()` y `str()`, y recupera autónomamente columnas mediante el operador `$`, reconociendo que vuelven a comportarse como vectores.

### Pregunta central
¿Cómo organizamos varias características de los mismos casos en una tabla y cómo recuperamos una variable de esa base?

### Modelo mental
`UN VECTOR = UNA CARACTERÍSTICA → VARIOS VECTORES ALINEADOS POR CASO → TABLA (DATA FRAME) → FILA = CASO → COLUMNA = VARIABLE → BASE $ VARIABLE → VECTOR`

---

## Datasets Contractuales Canónicos (100% Coherencia R / Visual)

### 1. Microtabla Pedagógica (E01 y E02)
Utilizada en los ejercicios 1 y 2 para modelar y practicar la lectura de casos y variables:

```text
             edad   horas_estudio   carrera
Persona 1      20         3         Sociología
Persona 2      22         5         Historia
Persona 3      19         2         Antropología
Persona 4      21         4         Sociología
```

### 2. Base de Datos Central: `encuesta_social_demo` (E03, E04 y E05)
Data frame contractual en R de 8 casos y 5 variables:

```r
encuesta_social_demo <- data.frame(
  id = 1:8,
  edad = c(20, 22, 19, 21, 24, 23, 20, 25),
  carrera = c("Sociología", "Historia", "Antropología", "Sociología", "Trabajo Social", "Antropología", "Historia", "Sociología"),
  horas_estudio = c(3, 5, 2, 4, 6, 3, 5, 2),
  trabaja = c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
```

Vista tabular visual (panel pedagógico):
```text
id   edad   carrera          horas_estudio   trabaja
1    20     Sociología       3                No
2    22     Historia         5                Sí
3    19     Antropología     2                No
4    21     Sociología       4                No
5    24     Trabajo Social   6                Sí
6    23     Antropología     3                Sí
7    20     Historia         5                No
8    25     Sociología       2                Sí
```

### 3. Base de Datos de Transferencia: `encuesta_barrio` (E06)
Data frame contractual en R de 4 casos y 4 variables:

```r
encuesta_barrio <- data.frame(
  persona = 1:4,
  edad = c(34, 27, 41, 22),
  transporte = c("Bus", "Metro", "Bus", "Bicicleta"),
  minutos_viaje = c(45, 30, 50, 20),
  stringsAsFactors = FALSE
)
```

Vista tabular visual (panel pedagógico):
```text
persona   edad   transporte   minutos_viaje
1         34     Bus          45
2         27     Metro        30
3         41     Bus          50
4         22     Bicicleta    20
```

---

## Especificación Detallada de los 6 Ejercicios

### M4-E1 — Varias características de las mismas personas
* **Rol**: Novedad conceptual / Exploración guiada.
* **Autocontención**: Muestra la microtabla visualmente en el contexto del ejercicio.
* **Lenguaje**: Explica en lenguaje cotidiano:
  - Una fila reúne la información de una persona.
  - Una columna reúne los valores de una misma característica (por ejemplo, la edad).
  - En análisis de datos, llamamos **caso** a cada fila y **variable** a cada columna.
  - En R, una tabla que organiza casos y variables se llama **data frame**.
* **Starter code seguro (sin placeholders inválidos)**:
  ```r
  # La Persona 2 estudia 5 horas. ¿Cuántos años tiene?
  # Guarda su edad en edad_persona_2:

  ```
* **Solución**:
  ```r
  edad_persona_2 <- 22
  ```
* **Checks**:
  - `object_exists`: `edad_persona_2`
  - `object_value`: `edad_persona_2 == 22`

---

### M4-E2 — Lee una fila y una columna
* **Rol**: Práctica activa de lectura tabular (fila vs columna).
* **Autocontención**: Muestra la microtabla completa en el contexto. El estudiante no depende de la pantalla anterior.
* **Doble práctica activa**:
  1. Extraer los valores de la columna `edad` y guardarlos en `edades_encuesta`.
  2. Extraer los valores de la columna `horas_estudio` y guardarlos en `horas_encuesta`.
* **Starter code seguro**:
  ```r
  # 1. Guarda las cuatro edades de la tabla en edades_encuesta


  # 2. Guarda las cuatro horas de estudio de la tabla en horas_encuesta

  ```
* **Solución**:
  ```r
  edades_encuesta <- c(20, 22, 19, 21)
  horas_encuesta <- c(3, 5, 2, 4)
  ```
* **Checks**:
  - `object_exists`: `edades_encuesta`, `horas_encuesta`
  - `object_value`: `edades_encuesta == c(20, 22, 19, 21)`
  - `object_value`: `horas_encuesta == c(3, 5, 2, 4)`

---

### M4-E3 — Mira los primeros casos (`head()`)
* **Rol**: Inspección funcional guiada.
* **Autocontención**: Base `encuesta_social_demo` en R. Explicación de que las bases reales pueden tener miles de filas y `head()` permite un vistazo rápido.
* **Acción activa**: No es un simple Ctrl+Enter pasivo. El estudiante ejecuta la inspección y conecta la función con la lectura del resultado.
* **Starter code**:
  ```r
  # 1. Muestra las primeras filas de encuesta_social_demo con head()
  head(encuesta_social_demo)

  # 2. ¿Cuántas filas muestra head() por defecto? Guarda ese número en filas_visibles:

  ```
* **Solución**:
  ```r
  head(encuesta_social_demo)
  filas_visibles <- 6
  ```
* **Checks**:
  - Código utiliza `head(encuesta_social_demo)`.
  - `object_exists`: `filas_visibles`.
  - `object_value`: `filas_visibles == 6`.

---

### M4-E4 — Una variable dentro de la base (`$`)
* **Rol**: Novedad sintáctica nuclear del módulo.
* **Autocontención**: Muestra una vista previa de `encuesta_social_demo` en el panel izquierdo para que el estudiante conozca los nombres y contenidos de las columnas.
* **Modelado en texto**:
  - Muestra cómo opera `$`: `encuesta_social_demo$edad` extrae todas las edades como un vector.
* **Doble práctica activa**:
  - El starter code **NO contiene la solución preescrita**.
  - El estudiante escribe la extracción de `horas_estudio` y luego la extracción de `carrera`.
* **Starter code**:
  ```r
  # 1. Extrae la variable horas_estudio de encuesta_social_demo


  # 2. Ahora extrae la variable carrera de encuesta_social_demo

  ```
* **Solución**:
  ```r
  encuesta_social_demo$horas_estudio
  encuesta_social_demo$carrera
  ```
* **Checks**:
  - Verifica que el código incluya `encuesta_social_demo$horas_estudio` y `encuesta_social_demo$carrera`.
  - El último valor evaluado o resultado corresponde al vector de carreras (`c("Sociología", "Historia", ...)`).

---

### M4-E5 — ¿Qué contiene la base? (`str()`)
* **Rol**: Inspección estructural y conexión con extracción.
* **Autocontención**: Explicación de que `str()` muestra la radiografía técnica (filas, columnas, nombres y tipos de almacenamiento) sin que `chr`, `num` o `int` reemplacen la interpretación sustantiva de la variable.
* **Acción activa**:
  1. Ejecuta `str(encuesta_social_demo)` para ver las variables.
  2. Extrae la variable de empleo (`trabaja`) y la guarda en `situacion_laboral`.
* **Starter code**:
  ```r
  # 1. Inspecciona la estructura de encuesta_social_demo con str()


  # 2. Extrae con $ la variable de empleo (trabaja) y guárdala en situacion_laboral:

  ```
* **Solución**:
  ```r
  str(encuesta_social_demo)
  situacion_laboral <- encuesta_social_demo$trabaja
  ```
* **Checks**:
  - Verifica llamada a `str(encuesta_social_demo)`.
  - Verifica objeto `situacion_laboral` con valor `c("No", "Sí", "No", "No", "Sí", "Sí", "No", "Sí")`.

---

### M4-E6 — Otra encuesta (Transferencia)
* **Rol**: Mini-checkpoint / Transferencia autónoma.
* **Autocontención**: Muestra la tabla completa de `encuesta_barrio` en el panel izquierdo.
* **Tarea autónoma**:
  1. Extrae la variable `minutos_viaje` y guárdala en `tiempos`.
  2. Extrae la variable `transporte` y guárdala en `medios`.
* **Starter code**:
  ```r
  # 1. Guarda la columna minutos_viaje de encuesta_barrio en tiempos


  # 2. Guarda la columna transporte de encuesta_barrio en medios

  ```
* **Solución**:
  ```r
  tiempos <- encuesta_barrio$minutos_viaje
  medios <- encuesta_barrio$transporte
  ```
* **Checks**:
  - `object_exists`: `tiempos`, `medios`.
  - `object_value`: `tiempos == c(45, 30, 50, 20)`.
  - `object_value`: `medios == c("Bus", "Metro", "Bus", "Bicicleta")`.
