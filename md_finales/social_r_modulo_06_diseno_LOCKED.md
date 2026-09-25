# Social R — Módulo 6
## Trabajar cuando faltan datos

### Estado
Diseño pedagógico canónico — **LOCKED** — Versión 2.0 (Rediseño pedagógico profundo con 7 ejercicios y Checkpoint B).

### Capacidad antes
Puede preparar subconjuntos de datos con `filter()` y `select()`, extraer variables y construir condiciones lógicas, pero todavía supone que todas las observaciones tienen un valor registrado y completo.

### Capacidad después
Puede reconocer `NA` y distinguirlo de un valor observado como 0, detectar y contar datos ausentes en columnas, evaluar el tamaño muestral efectivo ($N_{\text{disponible}}$), identificar casos completos a nivel de fila con `complete.cases()`, diagnosticar la completitud de subconjuntos analíticos multivariados y justificar decisiones transparentando cuántos casos participaron en el cálculo.

### Pregunta central
¿Qué significa que un dato no esté disponible y qué debemos revisar antes de calcular con los valores observados?

### Modelo mental nuclear
```text
DATO NO DISPONIBLE
↓
NA ≠ 0 (INFORMACIÓN AUSENTE)
↓
DETECTAR AUSENCIAS: is.na(x)
↓
CONTAR AUSENCIAS: sum(is.na(x))
↓
EVALUAR N DISPONIBLE: N_total - N_missing
↓
CALCULAR CON OBSERVADOS: na.rm = TRUE
↓
IDENTIFICAR CASOS COMPLETOS: complete.cases(datos)
↓
TRANSPARENTAR QUÉ CASOS Y CUÁNTOS VALORES ENTRARON AL ANÁLISIS
```

### Habilidades nucleares
Al terminar M6, el estudiante debe poder:

- explicar que `NA` representa un valor no disponible o desconocido;
- distinguir conceptualmente `NA` de `0` en contextos de investigación social;
- distinguir `NA` de la cadena de texto `"NA"`;
- reconocer que un dato ausente no implica un error de programación;
- detectar ausencias con `is.na()`;
- interpretar el vector lógico devuelto por `is.na()` (`TRUE` = falta información);
- contar ausencias mediante `sum(is.na(x))`;
- deducir cuántos datos válidos quedan disponibles ($N_{\text{disponible}}$);
- comprender por qué una función aritmética devuelve `NA` si no se le indica cómo proceder;
- usar `na.rm = TRUE` para calcular únicamente con los valores observados;
- explicar que `na.rm = TRUE` no altera la base de datos ni convierte `NA` en cero;
- reconocer que un caso puede tener datos en una variable pero faltar en otra;
- utilizar `complete.cases()` para identificar qué filas tienen información completa en todas sus variables;
- contar casos completos mediante `sum(complete.cases(datos))`;
- combinar preparación de datos (`filter()`, `select()`, `|>`) con diagnóstico de casos completos;
- diagnosticar datos ausentes y calcular con valores disponibles de manera autónoma en una base nueva.

### Habilidades funcionales
- Recordar la escritura exacta del argumento `na.rm = TRUE`.
- Interpretar el vector lógico devuelto por `complete.cases(df)`.

### Habilidades recuperadas
- `c()`;
- `<-`;
- `$`;
- `TRUE` y `FALSE`;
- `sum()`;
- `filter()`;
- `select()`;
- pipe `|>`;
- Fila = Caso, Columna = Variable.

### Habilidades pospuestas
- Imputación de datos ausentes;
- Teoría formal de mecanismos de pérdida (MCAR, MAR, MNAR);
- Subsetting avanzado con corchetes `datos[complete.cases(datos), ]`;
- `drop_na()`;
- `mean()`, `median()`, `sd()` (introducidos en M08);
- Operador `!` como contenido formal;
- Paquetes especializados de missing data.

### Sintaxis nueva
- `NA`;
- `is.na()`;
- `na.rm = TRUE`;
- `complete.cases()`.

### Sintaxis que NO se introduce
No se introducen corchetes para indexación `[ , ]`, operadores lógicos compuestos (`&`, `|`, `!`), ni funciones estadísticas como `mean()` o `sd()`.

### Principio pedagógico central
M6 no enseña:
> "Si R devuelve NA, agrega na.rm = TRUE para que funcione".

La secuencia obligatoria es:
```text
RECONOZCO NA COMO INFORMACIÓN AUSENTE
↓
DETECTO DÓNDE FALTA
↓
CUENTO CUÁNTOS FALTAN
↓
EVALÚO CUÁNTOS CASOS QUEDAN DISPONIBLES
↓
IDENTIFICO QUÉ CASOS ESTÁN COMPLETOS ENTRE VARIABLES
↓
CALCULO CON OBSERVADOS Y TRANSPARENTO EL N UTILIZADO
```

---

# Mapa del módulo (7 ejercicios)

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| **M6-E1** | El valor que no está | NOVEDAD | Significado de `NA` vs `0` | vector, posición | baja |
| **M6-E2** | ¿Dónde falta información? | NOVEDAD | `is.na()` | vector lógico, TRUE/FALSE | baja-media |
| **M6-E3** | ¿Cuántos faltan y cuántos quedan? | PRÁCTICA | `sum(is.na())` + $N_{\text{disponible}}$ | `sum()`, conteo | media |
| **M6-E4** | Calcular con los datos disponibles | NOVEDAD / TUNE | `na.rm = TRUE` + reporte de $N$ | `sum()` | media |
| **M6-E5** | Casos completos e incompletos | NOVEDAD / REDESIGN | `complete.cases()` a nivel de fila | data frame, fila=caso | media-alta |
| **M6-E6** | Diagnosticar antes de analizar | RECUPERACIÓN / REDESIGN | Preparación + casos completos | `filter()`, `select()`, `\|>` | media-alta |
| **M6-E7** | Checkpoint B: Decidir frente a datos ausentes | TRANSFERENCIA / CHECKPOINT | Ruta completa desasistida | Diagnóstico + decisión + $N$ | alta (autonomía) |

---

## M6-E1 — El valor que no está

### 1. Rol pedagógico
NOVEDAD (Significado de `NA` vs `0`).

### 2. Por qué existe
Construye el modelo mental de dato ausente antes de operar con él. La distinción entre 0 (valor medido) y NA (información desconocida) es el cimiento de la ética y el rigor en investigación cuantitativa.

### 3. Capacidad antes
Lee vectores y asume que toda celda contiene una respuesta conocida.

### 4. Capacidad después
Distingue conceptualmente un valor observado (como 0) de la ausencia de información (`NA`).

### 5. Prerrequisitos
Vector, posición, lectura de consola.

### 6. Gran novedad
- **Sintaxis:** `NA`.
- **Concepto:** Información no disponible / desconocida.

### 7. Contexto sustantivo
Horas semanales dedicadas al cuidado de personas dependientes (`horas_cuidado`).
La persona 2 reportó 0 horas (valor observado).
La persona 3 no respondió la pregunta (`NA`).

### 8. Dataset / objetos
Microvector de 5 observaciones:
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 9. Texto para estudiante
Hasta ahora todos los datos que usamos estaban disponibles. Pero en investigaciones sociales es muy común que algunas personas no respondan una pregunta.

En R, la falta de información se representa con `NA` (sin comillas):
- `0`: es un dato observado. Sabemos con certeza que la persona 2 reportó cero horas.
- `NA`: es un dato ausente. No sabemos cuántas horas dedicó la persona 3.

Reemplazar `NA` por 0 sería un error grave: asumiríamos que alguien no cuidó cuando en realidad simplemente no tenemos esa información.

Observa el vector disponible `horas_cuidado`:
`horas_cuidado <- c(6, 0, NA, 8, 4)`

### 10. Tarea
Ejecuta `horas_cuidado` para observar en la consola la diferencia entre el valor observado `0` y la ausencia de dato `NA`.

### 11. Starter code
```r
horas_cuidado
```

### 12. Solución canónica
```r
horas_cuidado
```

### 13. Checks
- `!is.null(.res_val)`

### 14. Pistas
- Pista 1 · Conceptual: Pregunta primero: ¿conocemos la respuesta de la persona 2? ¿Y la de la persona 3?
- Pista 2 · Procedimiento: La persona 2 dio una respuesta válida: 0 horas. Para la persona 3 la información no está disponible.
- Pista 3 · Sintaxis / Acción: Ejecuta `horas_cuidado` para ver cómo R muestra ambos valores.

### 15. Feedback
- **Correcto:** Bien. Cero es una respuesta observada (0 horas). `NA` indica que la información no está disponible.
- **Incorrecto:** Ejecuta `horas_cuidado` para inspeccionar el vector en la consola.

---

## M6-E2 — ¿Dónde falta información?

### 1. Rol pedagógico
NOVEDAD (`is.na()`).

### 2. Por qué existe
Enseña a formular la pregunta lógica de ausencia sobre un vector. El estudiante debe predecir y verificar dónde se ubican los valores ausentes.

### 3. Capacidad antes
Reconoce visualmente `NA`, pero no sabe cómo pedirle a R que lo detecte programáticamente.

### 4. Capacidad después
Aplica `is.na()` y comprende que devuelve `TRUE` únicamente donde falta información.

### 5. Prerrequisitos
M6-E1, vectores lógicos `TRUE`/`FALSE`.

### 6. Gran novedad
Función `is.na()`.

### 7. Dataset / objetos
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 8. Texto para estudiante
Para saber dónde faltan datos usamos la función `is.na()`.

Esta función revisa cada posición del vector y responde con valores lógicos:
- `TRUE`: falta información en esa posición.
- `FALSE`: hay un valor observado disponible.

Observa el vector: `horas_cuidado <- c(6, 0, NA, 8, 4)`.

¿En qué posición esperas que aparezca `TRUE`?

### 9. Tarea
Aplica `is.na()` sobre `horas_cuidado` para identificar qué posiciones contienen datos ausentes.

### 10. Starter code
```r
# Identifica qué posiciones contienen datos ausentes:
is.na(__________)
```

### 11. Solución canónica
```r
is.na(horas_cuidado)
```

### 12. Checks
- `is.logical(.res_val) && length(.res_val) == 5 && identical(.res_val, c(FALSE, FALSE, TRUE, FALSE, FALSE))`

### 13. Pistas
- Pista 1 · Conceptual: Necesitas una pregunta lógica que responda TRUE exactamente donde no hay dato registrado.
- Pista 2 · Procedimiento: Pasa el vector `horas_cuidado` como argumento dentro de `is.na()`.
- Pista 3 · Sintaxis / Acción: Completa los guiones con el nombre del vector: `is.na(horas_cuidado)`.

### 14. Feedback
- **Correcto:** Exacto. `TRUE` aparece en la tercera posición, donde está el `NA`. En las demás posiciones aparece `FALSE` porque sí hay un valor disponible (incluyendo el 0).
- **Incorrecto:** Aplica `is.na(horas_cuidado)` para obtener el vector lógico de ausencias.

---

## M6-E3 — ¿Cuántos faltan y cuántos quedan?

### 1. Rol pedagógico
PRÁCTICA / EXTENSIÓN (`sum(is.na())` + evaluación de $N$ disponible).

### 2. Por qué existe
Transforma el conteo de ausencias en una evaluación del tamaño muestral efectivo. El analista no solo cuenta cuántos faltan, sino cuántos casos válidos quedan para responder la pregunta.

### 3. Capacidad antes
Detecta `NA` con `is.na()`, pero no cuantifica ausencias ni calcula casos válidos disponibles.

### 4. Capacidad después
Combina `sum()` e `is.na()` para contar ausencias y calcula el número de casos disponibles restando del total de observaciones.

### 5. Prerrequisitos
M6-E2, `sum()`, tratar `TRUE` como 1 y `FALSE` como 0.

### 6. Gran novedad
Cálculo explícito del tamaño muestral disponible ($N_{\text{disponible}} = N_{\text{total}} - N_{\text{missing}}$).

### 7. Dataset / objetos
Vector con 5 casos:
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 8. Texto para estudiante
En operaciones aritméticas, R trata a `TRUE` como 1 y a `FALSE` como 0.

Por eso podemos contar cuántos datos ausentes hay sumando el resultado de `is.na()`:
`sum(is.na(horas_cuidado))`

Si tenemos 5 personas en total y sabemos cuántas faltan, podemos calcular cuántas personas quedan disponibles:
$$N_{\text{disponible}} = 5 - N_{\text{ausentes}}$$

Ese número representa el **tamaño muestral efectivo**: las personas con las que realmente podremos operar.

### 9. Tarea
1. Cuenta cuántos valores ausentes hay en `horas_cuidado` y guarda el resultado en `faltan`.
2. Calcula cuántos datos válidos quedan disponibles restando `faltan` al total de 5 personas, y guárdalo en `disponibles`.

### 10. Starter code
```r
# 1. Cuenta cuántos datos faltan en horas_cuidado:
faltan <- sum(is.na(horas_cuidado))
faltan

# 2. Calcula cuántos datos quedan disponibles (de un total de 5 personas):
disponibles <- 5 - ______
disponibles
```

### 11. Solución canónica
```r
faltan <- sum(is.na(horas_cuidado))
faltan

disponibles <- 5 - faltan
disponibles
```

### 12. Checks
- `object_exists`: `faltan`
- `object_exists`: `disponibles`
- `custom_r`: `.target_env$faltan == 1 && .target_env$disponibles == 4`

### 13. Pistas
- Pista 1 · Conceptual: Para saber cuántos quedan, resta las ausencias al total de 5 observaciones.
- Pista 2 · Procedimiento: Usa la variable `faltan` que creaste en el paso 1 para restarla de 5.
- Pista 3 · Sintaxis / Acción: Escribe `disponibles <- 5 - faltan`.

### 14. Feedback
- **Correcto:** Muy bien. Faltan 1 dato y quedan 4 disponibles. Conocer el $N$ disponible es fundamental antes de cualquier cálculo: nos dice con cuántas personas reales estamos trabajando.
- **Incorrecto:** Revisa el cálculo: `faltan` debe ser `sum(is.na(horas_cuidado))` y `disponibles` debe ser `5 - faltan`.

---

## M6-E4 — Calcular con los datos disponibles

### 1. Rol pedagógico
NOVEDAD / TUNE (`na.rm = TRUE` consciente + reporte de $N$).

### 2. Por qué existe
Desmitifica el resultado `NA` (no es un fallo de R, es prudencia epistémica) y enseña a usar `na.rm = TRUE` transparentando el número real de casos que entraron al cálculo.

### 3. Capacidad antes
Conoce los casos disponibles, pero no sabe cómo realizar operaciones cuando hay un dato ausente.

### 4. Capacidad después
Aplica `na.rm = TRUE` conscientemente y sabe que el resultado numérico resume únicamente los valores observados.

### 5. Prerrequisitos
M6-E3, función `sum()`.

### 6. Gran novedad
Argumento `na.rm = TRUE`.

### 7. Dataset / objetos
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 8. Texto para estudiante
Si intentamos sumar `horas_cuidado`, R responderá con `NA`:
`sum(horas_cuidado)` $\rightarrow$ `NA`

Esto **no es un error de programación**. R razona con prudencia: si no conoce el valor de la persona 3, no puede saber el total exacto de las cinco personas.

Para pedirle a R que calcule usando únicamente los valores observados, usamos el argumento `na.rm = TRUE` (abreviación de *NA remove*):
`sum(horas_cuidado, na.rm = TRUE)`

`na.rm = TRUE` no borra observaciones de tu base ni convierte el `NA` en 0. Solo le dice a la función: *"suma los 4 datos que sí tenemos"*.

### 9. Tarea
1. Observa el primer cálculo sin `na.rm` (devuelve `NA`).
2. En la segunda línea, calcula la suma de los valores disponibles agregando `na.rm = TRUE`.

### 10. Starter code
```r
# 1. Sin indicar qué hacer con NA, el total es desconocido:
sum(horas_cuidado)

# 2. Suma únicamente las horas observadas usando na.rm = TRUE:
sum(horas_cuidado, ______________)
```

### 11. Solución canónica
```r
sum(horas_cuidado)
sum(horas_cuidado, na.rm = TRUE)
```

### 12. Checks
- `custom_r`: `grepl('na\\.rm\\s*=\\s*TRUE', .user_code)`
- `custom_r`: `.res_val == 18`

### 13. Pistas
- Pista 1 · Conceptual: R devuelve NA porque le falta un número para completar la suma total.
- Pista 2 · Procedimiento: Agrega el argumento `na.rm = TRUE` dentro de `sum()` separado por coma.
- Pista 3 · Sintaxis / Acción: Completa los guiones con `na.rm = TRUE`.

### 14. Feedback
- **Correcto:** Excelente. Sin `na.rm = TRUE`, el total es desconocido (`NA`). Con `na.rm = TRUE`, R suma únicamente los 4 valores disponibles y obtiene 18 horas. Siempre debemos transparentar que este resultado representa a 4 de las 5 personas.
- **Incorrecto:** Asegúrate de agregar `, na.rm = TRUE` dentro de la llamada a `sum(horas_cuidado)`.

---

## M6-E5 — Casos completos e incompletos

### 1. Rol pedagógico
NOVEDAD / REDESIGN (`complete.cases()` a nivel de fila).

### 2. Por qué existe
Es el puente conceptual más importante del módulo. Pasa del diagnóstico de una sola columna al diagnóstico multivariado de observaciones. En ciencias sociales las personas pueden responder unas preguntas y omitir otras; un análisis conjunto exige saber qué casos tienen información completa.

### 3. Capacidad antes
Diagnostica missing en vectores columna, pero no comprende el estado de completitud de una fila en un data frame.

### 4. Capacidad después
Utiliza `complete.cases()` para identificar qué filas tienen información completa en todas sus variables y cuenta el total de casos completos con `sum()`.

### 5. Prerrequisitos
M04 (data frames, fila = caso), M6-E2 (`is.na()`).

### 6. Gran novedad
Función `complete.cases()` y el concepto de **caso completo**.

### 7. Dataset / objetos
Pequeño data frame visible `registro_cuidado`:
```r
registro_cuidado <- data.frame(
  id = 1:5,
  edad = c(20, 22, NA, 21, 24),
  horas_cuidado = c(6, NA, 0, 8, 4)
)
```
- Caso 1: edad 20, horas 6 $\rightarrow$ completo.
- Caso 2: horas NA $\rightarrow$ incompleto.
- Caso 3: edad NA $\rightarrow$ incompleto.
- Casos 4 y 5: ambos datos registrados $\rightarrow$ completos.

### 8. Texto para estudiante
Hasta ahora revisamos una variable a la vez. Pero cuando investigamos, casi siempre combinamos varias variables sobre las mismas personas.

Un **caso completo** es una persona que tiene información registrada en **todas** las variables que estamos analizando.

La función `complete.cases()` revisa las filas de una base y devuelve:
- `TRUE`: la fila tiene información completa (sin `NA`).
- `FALSE`: la fila tiene al menos un dato ausente en alguna columna.

Para saber cuántas personas tienen sus datos completos, sumamos esos `TRUE`:
`sum(complete.cases(registro_cuidado))`

### 9. Tarea
1. Aplica `complete.cases(registro_cuidado)` para ver qué filas tienen información completa.
2. Cuenta cuántos casos completos hay en total combinando `sum()` y `complete.cases()`.

### 10. Starter code
```r
# 1. Identifica qué filas están completas:
complete.cases(registro_cuidado)

# 2. Cuenta cuántos casos completos hay en total:
sum(______________________________)
```

### 11. Solución canónica
```r
complete.cases(registro_cuidado)
sum(complete.cases(registro_cuidado))
```

### 12. Checks
- `custom_r`: `grepl('complete\\.cases\\s*\\(', .user_code)`
- `custom_r`: `.res_val == 3`

### 13. Pistas
- Pista 1 · Conceptual: Un caso está completo solo si ninguna de sus variables contiene NA. En esta muestra, los casos 1, 4 y 5 están completos.
- Pista 2 · Procedimiento: Usa `complete.cases(registro_cuidado)` dentro de `sum()` para contar los TRUE.
- Pista 3 · Sintaxis / Acción: Completa con `sum(complete.cases(registro_cuidado))`.

### 14. Feedback
- **Correcto:** ¡Exacto! `complete.cases()` devuelve TRUE únicamente para los casos 1, 4 y 5. De las 5 personas de la muestra, solo 3 tienen información completa en ambas variables.
- **Incorrecto:** Ejecuta primero `complete.cases(registro_cuidado)` y luego cuenta los casos completos con `sum(complete.cases(registro_cuidado))`.

---

## M6-E6 — Diagnosticar antes de analizar

### 1. Rol pedagógico
RECUPERACIÓN / REDESIGN (Preparación M05 + diagnóstico multivariado de casos completos).

### 2. Por qué existe
Conecta la preparación de datos (`filter()`, `select()`, pipe `|>`) con el diagnóstico de completitud. El estudiante experimenta que filtrar un grupo no elimina automáticamente sus datos ausentes.

### 3. Capacidad antes
Sabe filtrar y seleccionar, y sabe aplicar `complete.cases()`, pero no los ha coordinado en una secuencia analítica real.

### 4. Capacidad después
Prepara un subconjunto analítico y determina cuántos casos pertenecen al grupo y cuántos de ellos tienen información completa para el estudio conjunto.

### 5. Prerrequisitos
M05 (`filter()`, `select()`, `|>`), M6-E5 (`complete.cases()`).

### 6. Gran novedad
Ninguna sintaxis nueva. Integración metodológica de preparación y diagnóstico.

### 7. Dataset / objetos
`encuesta_social_demo` (8 personas):
Variables focales: `edad`, `horas_cuidado`, filtro por `trabaja == "Sí"`.
Personas que trabajan: casos 2, 5, 6, 8 (4 personas).
De ellas, el caso 2 tiene `NA` en `horas_cuidado`.
Casos completos: 3 personas (5, 6, 8).

### 8. Texto para estudiante
Antes de analizar una relación, un investigador siempre realiza dos pasos:
1. Prepara las observaciones y variables pertinentes.
2. Revisa cuántos casos del grupo tienen la información completa.

Queremos estudiar `edad` y `horas_cuidado` entre quienes trabajan (`trabaja == "Sí"`).

Prepara ese grupo y averigua:
- ¿Cuántas personas trabajan?
- ¿Cuántas de ellas tienen datos completos en ambas variables?

### 9. Tarea
1. Filtra a quienes trabajan (`trabaja == "Sí"`) y selecciona las columnas `edad` y `horas_cuidado`, guardando el resultado en `datos_trabajan`.
2. Cuenta cuántos casos completos tiene `datos_trabajan` usando `sum()` y `complete.cases()`.

### 10. Starter code
```r
# 1. Prepara las personas que trabajan y conserva edad y horas_cuidado:
datos_trabajan <- encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(________, _____________)

# 2. Cuenta cuántos casos tienen información completa en ambas variables:
sum(______________________________)
```

### 11. Solución canónica
```r
datos_trabajan <- encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(edad, horas_cuidado)

sum(complete.cases(datos_trabajan))
```

### 12. Checks
- `object_exists`: `datos_trabajan`
- `custom_r`: `is.data.frame(.target_env$datos_trabajan) && nrow(.target_env$datos_trabajan) == 4 && all(c("edad", "horas_cuidado") %in% names(.target_env$datos_trabajan))`
- `custom_r`: `.res_val == 3`

### 13. Pistas
- Pista 1 · Conceptual: Primero filtra por `trabaja == "Sí"` y selecciona las dos variables analíticas (`edad`, `horas_cuidado`).
- Pista 2 · Procedimiento: Después aplica `complete.cases()` sobre el nuevo objeto `datos_trabajan` dentro de `sum()`.
- Pista 3 · Sintaxis / Acción: Completa `select(edad, horas_cuidado)` y en la segunda línea escribe `sum(complete.cases(datos_trabajan))`.

### 14. Feedback
- **Correcto:** Excelente trabajo. En `datos_trabajan` hay 4 personas que trabajan (casos 2, 5, 6 y 8). Sin embargo, la persona 2 no respondió sus horas de cuidado (`NA`). Por eso, solo 3 personas tienen información completa para analizar edad y horas de cuidado juntas.
- **Incorrecto:** Asegúrate de filtrar `trabaja == "Sí"`, seleccionar `edad` y `horas_cuidado`, y luego contar casos completos con `sum(complete.cases(datos_trabajan))`.

---

## M6-E7 — Checkpoint B: Decidir frente a datos ausentes

### 1. Rol pedagógico
TRANSFERENCIA AUTÓNOMA / CHECKPOINT FORMATIVO.

### 2. Por qué existe
Evalúa si el estudiante puede transferir la cadena completa (diagnosticar ausencias $\rightarrow$ cuantificar disponibles $\rightarrow$ calcular con observados) sobre una base completamente nueva y sin andamiaje en la consigna ni en el starter code.

### 3. Capacidad antes
Ha completado ejercicios guiados y de recuperación con apoyo parcial.

### 4. Capacidad después
Diagnostica datos ausentes y produce cálculos con valores observados de forma totalmente autónoma en una base no vista previamente.

### 5. Prerrequisitos
Todo el Módulo 06.

### 6. Gran novedad
Cero novedades sintácticas. Autonomía de transferencia.

### 7. Dataset / objetos
Base nueva `encuesta_vecinal` (6 residentes):
```r
encuesta_vecinal <- data.frame(
  vecino = 1:6,
  reuniones = c(4, 2, NA, 5, NA, 3),
  comite = c("Sí", "No", "Sí", "Sí", "No", "Sí"),
  stringsAsFactors = FALSE
)
```
- Total casos: 6
- Ausencias en `reuniones`: 2 (vecinos 3 y 5)
- Casos disponibles: 4
- Suma disponible: $4 + 2 + 5 + 3 = 14$ reuniones.

### 8. Texto para estudiante
Llegaste al desafío final del módulo. Ahora resolverás de forma autónoma, sin nombres de funciones en la consigna.

En `encuesta_vecinal` queremos estudiar la asistencia a reuniones comunitarias (`reuniones`).
Hay 6 vecinos en la muestra.

Realiza las siguientes acciones:
1. Averigua cuántos datos ausentes hay en `reuniones`.
2. Calcula el total de reuniones asistidas por los vecinos que sí aportaron información.

Observa cuántos casos entraron al cálculo final.

### 9. Tarea
1. Cuenta los datos ausentes de `encuesta_vecinal$reuniones`.
2. Calcula la suma de las reuniones disponibles usando `sum()` con `na.rm = TRUE`.

### 10. Starter code
```r
# 1. Cuenta cuántos datos faltan en reuniones:


# 2. Calcula el total de reuniones de los casos disponibles:

```

### 11. Solución canónica
```r
sum(is.na(encuesta_vecinal$reuniones))
sum(encuesta_vecinal$reuniones, na.rm = TRUE)
```

### 12. Checks
- `custom_r`: `grepl('is\\.na\\s*\\(', .user_code)`
- `custom_r`: `grepl('na\\.rm\\s*=\\s*TRUE', .user_code)`
- `custom_r`: `.res_val == 14`

### 13. Pistas
- Pista 1 · Conceptual: Primero debes saber cuántos datos faltan; luego debes pedirle a la suma que trabaje solo con los valores disponibles.
- Pista 2 · Procedimiento: Usa `sum(is.na(...))` sobre `encuesta_vecinal$reuniones` para contar faltantes. Luego usa `sum(..., na.rm = TRUE)` para sumar.
- Pista 3 · Sintaxis / Acción:
  ```r
  sum(is.na(encuesta_vecinal$reuniones))
  sum(encuesta_vecinal$reuniones, na.rm = TRUE)
  ```

### 14. Feedback
- **Correcto:** ¡Felicitaciones! Has completado el Checkpoint B. Faltan 2 datos de asistencia. La suma de los valores disponibles es 14 reuniones. Ahora sabes que este total representa a 4 de los 6 vecinos (N efectivo = 4). ¡Estás listo para describir variables categóricas en el Módulo 7!
- **Incorrecto:** Revisa tu código: primero cuenta las ausencias con `sum(is.na(encuesta_vecinal$reuniones))` y luego calcula el total disponible con `sum(encuesta_vecinal$reuniones, na.rm = TRUE)`.

---

# Cierre conceptual de M6 y puente a M7
> Ya puedes revisar si una variable tiene datos ausentes, contar cuántos faltan, evaluar qué casos están completos y decidir cuándo trabajar con los valores disponibles transparentando tu $N$ efectivo.
>
> Más adelante, cuando relacionemos variables en M9 y M11, esta misma noción de casos completos determinará qué personas pueden entrar en cada análisis.
>
> Ahora que sabemos preparar y diagnosticar nuestra información, queda la siguiente pregunta:
>
> **¿Cómo deberíamos describir una variable?**
>
> Eso dependerá de si sus valores representan categorías o cantidades. En el Módulo 7 comenzaremos aprendiendo a describir categorías.
