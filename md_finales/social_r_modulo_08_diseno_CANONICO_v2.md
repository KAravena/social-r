# Social R — Módulo 8: Describir cantidades
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
Puede reconocer y describir variables categóricas, preparar datos y revisar missing (Módulos 5 a 7).

### Capacidad después
Puede reconocer una variable cuantitativa por el significado de sus valores, observar su distribución, describir su centro mediante media y mediana, interpretar su dispersión mediante desviación estándar y elegir un resumen razonable según la distribución y la pregunta.

### Pregunta central
¿Cómo describo una variable cuyos valores representan cantidades sin reducirla automáticamente a un solo número?

### Modelo mental
`CANTIDADES → MIRAR DISTRIBUCIÓN (hist) → CENTRO (mean vs median) → DISPERSIÓN (sd) → INTERPRETAR`

---

## Datasets Contractuales (100% Coherencia R / Visual)

### 1. Base Central: `encuesta_social_demo` (E01, E02, E05, E06)
8 estudiantes universitarios:

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

### 2. Base de Transferencia: `encuesta_movilidad` (E07 Checkpoint C)
10 personas y sus tiempos de traslado:

| id | transporte | minutos_viaje |
|:---|:---|---:|
| 1 | Metro | 25 |
| 2 | Bus | 30 |
| 3 | Metro | 32 |
| 4 | Bus | 28 |
| 5 | Bicicleta | 35 |
| 6 | Metro | 27 |
| 7 | Bus | 31 |
| 8 | A pie | 29 |
| 9 | Metro | 34 |
| 10 | Bus | 90 |

---

## Especificación Detallada de los 7 Ejercicios

### M8-E1 — Mira la distribución
* **Rol**: Práctica activa con `hist()`.
* **Contexto**: Antes de calcular cualquier promedio o resumen, debemos mirar cómo se reparten los valores. Un histograma agrupa los valores en intervalos y dibuja barras cuya altura indica cuántos casos hay en cada intervalo:
  `hist(base$variable)`
* **Tarea**: Genera un histograma de la variable `horas_estudio` en `encuesta_social_demo` para observar cómo se distribuyen las horas de estudio.
* **Starter code**:
  ```r
  # Genera el histograma de horas_estudio:

  ```
* **Solución**:
  ```r
  hist(encuesta_social_demo$horas_estudio)
  ```
* **Checks**:
  - `ast_call`: función `hist` llamada sobre `encuesta_social_demo$horas_estudio`.

---

### M8-E2 — ¿Dónde está el centro?
* **Rol**: Práctica activa con `mean()`.
* **Contexto**: El promedio o media aritmética suma todos los valores y los divide por la cantidad de casos:
  `mean(base$variable)`
  La media representa el punto de equilibrio de los datos en las mismas unidades de la variable.
* **Tarea**: Calcula la media de `horas_estudio` en `encuesta_social_demo` para saber cuántas horas de estudio promedian en el grupo.
* **Starter code**:
  ```r
  # Calcula la media de horas_estudio:

  ```
* **Solución**:
  ```r
  mean(encuesta_social_demo$horas_estudio)
  ```
* **Checks**:
  - `ast_call`: función `mean` con argumento `encuesta_social_demo$horas_estudio`.

---

### M8-E3 — Otro centro posible
* **Rol**: Práctica activa con `median()`.
* **Contexto**: La mediana es el valor que queda exactamente al medio cuando ordenamos todos los datos de menor a mayor. Deja al 50% de los casos por debajo y al 50% por encima:
  `median(vector)`
  Tenemos el vector `minutos_lectura <- c(15, 20, 25, 30, 45, 60, 120)`.
* **Tarea**: Calcula la mediana de `minutos_lectura` para encontrar el tiempo de lectura que divide al grupo en dos mitades iguales.
* **Starter code**:
  ```r
  minutos_lectura <- c(15, 20, 25, 30, 45, 60, 120)

  # Calcula la mediana de minutos_lectura:

  ```
* **Solución**:
  ```r
  minutos_lectura <- c(15, 20, 25, 30, 45, 60, 120)
  median(minutos_lectura)
  ```
* **Checks**:
  - `ast_call`: función `median` sobre `minutos_lectura`.

---

### M8-E4 — ¿Cuál centro describe mejor?
* **Rol**: Comparación y razonamiento sustantivo.
* **Contexto**: Observa qué ocurre cuando un valor es atípico o muy extremo:
  - `viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)` (tiempos habituales).
  - `viaje_con_accidente <- c(20, 22, 24, 25, 26, 28, 120)` (un día con taco masivo).
* **Tarea**: Calcula la media y la mediana de `viaje_regular`, y luego la media y la mediana de `viaje_con_accidente`. Observa cómo la media salta a casi el doble mientras la mediana se mantiene en 25 minutos.
* **Starter code**:
  ```r
  viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)
  viaje_con_accidente <- c(20, 22, 24, 25, 26, 28, 120)

  # 1. Media y mediana del viaje regular:
  mean(viaje_regular)
  median(viaje_regular)

  # 2. Ahora calcula la media y mediana del viaje con accidente:

  ```
* **Solución**:
  ```r
  viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)
  viaje_con_accidente <- c(20, 22, 24, 25, 26, 28, 120)

  mean(viaje_regular)
  median(viaje_regular)

  mean(viaje_con_accidente)
  median(viaje_con_accidente)
  ```
* **Checks**:
  - `ast_call`: llamada a `mean(viaje_con_accidente)` y `median(viaje_con_accidente)`.

---

### M8-E5 — ¿Qué tan distintos son los valores?
* **Rol**: Práctica activa con `sd()`.
* **Contexto**: Dos grupos pueden tener el mismo promedio pero una realidad muy distinta si los valores están muy agrupados o muy dispersos. La **desviación estándar** (`sd()`) mide cuánto se alejan típicamente los valores respecto a la media.
* **Tarea**: Observa la dispersión en `grupo_a` y `grupo_b`. Luego calcula la desviación estándar de `horas_estudio` en `encuesta_social_demo`.
* **Starter code**:
  ```r
  grupo_a <- c(24, 25, 25, 26)
  grupo_b <- c(10, 20, 30, 40)

  sd(grupo_a)
  sd(grupo_b)

  # Ahora calcula la desviación estándar de horas_estudio:

  ```
* **Solución**:
  ```r
  grupo_a <- c(24, 25, 25, 26)
  grupo_b <- c(10, 20, 30, 40)

  sd(grupo_a)
  sd(grupo_b)

  sd(encuesta_social_demo$horas_estudio)
  ```
* **Checks**:
  - `ast_call`: función `sd` aplicada a `encuesta_social_demo$horas_estudio`.

---

### M8-E6 — Primero prepara, después describe
* **Rol**: Pipeline combinado de preparación y resumen.
* **Contexto**: En investigación casi nunca describimos la base entera sin antes seleccionar el subgrupo relevante. Queremos analizar únicamente a las personas que no trabajan.
* **Tarea**:
  1. Filtra a quienes tienen `trabaja == "No"` y guarda el subgrupo en `datos_no_trabajan`.
  2. Luego calcula la media y la desviación estándar de `horas_estudio` en ese subgrupo.
* **Starter code**:
  ```r
  # 1. Filtra las personas que no trabajan:
  datos_no_trabajan <- encuesta_social_demo |>
    filter(trabaja == "No")

  # 2. Calcula la media y desviación estándar de horas_estudio en ese subgrupo:

  ```
* **Solución**:
  ```r
  datos_no_trabajan <- encuesta_social_demo |>
    filter(trabaja == "No")

  mean(datos_no_trabajan$horas_estudio)
  sd(datos_no_trabajan$horas_estudio)
  ```
* **Checks**:
  - `object_exists`: `datos_no_trabajan`.
  - `ast_call`: llamada a `mean(datos_no_trabajan$horas_estudio)`.
  - `ast_call`: llamada a `sd(datos_no_trabajan$horas_estudio)`.

---

### M8-E7 — Checkpoint C: describe una variable nueva
* **Rol**: Checkpoint C / Transferencia autónoma.
* **Contexto**: Tienes a la vista la base `encuesta_movilidad` con los tiempos de traslado de 10 personas. Observa que el caso 10 demoró 90 minutos debido a una contingencia vial.
* **Tarea**: Realiza una descripción estadística completa de `minutos_viaje` en `encuesta_movilidad`:
  1. Calcula la media.
  2. Calcula la mediana.
  3. Calcula la desviación estándar.
* **Starter code**:
  ```r
  # Describe minutos_viaje en encuesta_movilidad:
  # 1. Calcula la media:

  # 2. Calcula la mediana:

  # 3. Calcula la desviación estándar:

  ```
* **Solución**:
  ```r
  mean(encuesta_movilidad$minutos_viaje)
  median(encuesta_movilidad$minutos_viaje)
  sd(encuesta_movilidad$minutos_viaje)
  ```
* **Checks**:
  - `ast_call`: llamada a `mean(encuesta_movilidad$minutos_viaje)`.
  - `ast_call`: llamada a `median(encuesta_movilidad$minutos_viaje)`.
  - `ast_call`: llamada a `sd(encuesta_movilidad$minutos_viaje)`.
