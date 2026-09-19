# Social R — Módulo 6
## Trabajar cuando faltan datos

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede preparar subconjuntos de datos, recuperar variables y construir condiciones, pero todavía supone que todas las observaciones tienen un valor registrado.

### Capacidad después
Puede reconocer `NA`, distinguir una ausencia de un valor observado como 0, detectar y contar datos ausentes, comprender cómo afectan a un cálculo y decidir cuándo calcular usando únicamente los valores disponibles.

### Pregunta central
¿Qué significa que un dato no esté disponible y qué debemos revisar antes de calcular con los valores observados?

### Modelo mental
`DATO NO DISPONIBLE → NA → NA ≠ 0 → DETECTAR → is.na() → CONTAR → sum(is.na()) → EFECTO EN CÁLCULOS → DECIDIR → na.rm = TRUE → CALCULAR CON DISPONIBLES → RECORDAR CUÁNTOS CASOS ENTRARON`

### Habilidades nucleares
Al terminar M6, el estudiante debe poder:

- explicar que `NA` representa un valor no disponible;
- distinguir `NA` de `0`;
- distinguir `NA` de `"NA"`;
- reconocer que un dato ausente no implica necesariamente un error del archivo;
- detectar ausencias con `is.na()`;
- interpretar la salida lógica de `is.na()`;
- contar ausencias mediante `sum(is.na(x))`;
- comprender que un cálculo puede devolver `NA` cuando falta información;
- comprender qué significa calcular con los valores disponibles;
- distinguir casos totales, datos ausentes y datos disponibles;
- revisar missing antes de omitirlo;
- recuperar preparación de datos de M5 dentro de un problema con missing;
- interpretar un resultado calculado con valores disponibles sin presentarlo como si utilizara los casos ausentes.

### Habilidad funcional
`na.rm = TRUE` es una construcción funcional importante.

El estudiante debe comprender su significado, aunque después de una semana pueda requerir recordatorio de su escritura exacta.

No debe aprenderla como una respuesta automática a cualquier `NA`.

### Habilidades recuperadas
Se recuperan:

- `sum()`;
- `$`;
- `TRUE/FALSE`;
- `<-`;
- `==`;
- `filter()`;
- `select()`;
- `|>`;
- objeto → resultado;
- fila = caso;
- columna = variable.

### Habilidades pospuestas
No se introducen en M6:

- `mean()`;
- `complete.cases()`;
- `!`;
- `length()`;
- imputación;
- MCAR;
- MAR;
- MNAR;
- ponderación;
- estrategias avanzadas de eliminación de casos;
- teoría formal de mecanismos de missing.

### Sintaxis nueva
- `NA`;
- `is.na()`;
- `na.rm = TRUE`.

### Sintaxis que NO se introduce
M6 no introduce nuevas funciones estadísticas descriptivas ni nuevos operadores lógicos.

### Principio pedagógico central
M6 no enseña:

> “si aparece `NA`, agrega `na.rm = TRUE`”.

La secuencia obligatoria es:

```text
VEO NA
↓
NO LO CONFUNDO CON 0
↓
PREGUNTO DÓNDE FALTA
↓
CUENTO CUÁNTO FALTA
↓
OBSERVO CÓMO AFECTA AL CÁLCULO
↓
DECIDO SI TIENE SENTIDO USAR SOLO LOS DISPONIBLES
↓
RECUERDO CUÁNTOS DATOS ENTRARON
```

### Contrato de datos heredado
M4 y M5 dejaron fijadas las siguientes variables y valores de `encuesta_social_demo`:

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

M6 no modifica ninguna de esas celdas.

### Nueva variable revelada en M6
En este módulo aparece explícitamente una nueva variable de `encuesta_social_demo`:

`horas_cuidado`

Valores:

```text
id   horas_cuidado
1    6
2    NA
3    0
4    8
5    4
6    5
7    NA
8    7
```

Vista ampliada del objeto desde M6:

```text
id   edad   carrera          horas_estudio   trabaja   horas_cuidado
1    20     Sociología       3                No        6
2    22     Historia         5                Sí        NA
3    19     Antropología     2                No        0
4    21     Sociología       4                No        8
5    24     Trabajo Social   6                Sí        4
6    23     Antropología     3                Sí        5
7    20     Historia         5                No        NA
8    25     Sociología       2                Sí        7
```

Texto de continuidad obligatorio:

> En este módulo aparece una nueva variable de la encuesta: `horas_cuidado`.
>
> Las variables que ya conocíamos mantienen exactamente sus valores.

### Microvector pedagógico de E1–E4
Durante E1–E4 se usa una pequeña versión de ejemplo:

```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

Este vector no reemplaza la columna de ocho casos de `encuesta_social_demo`.

Su función es aislar el concepto de dato ausente y reducir carga cognitiva.

### Dataset de transferencia
E6 utiliza una base nueva:

```text
encuesta_barrio

id   minutos_viaje   transporte
1    35              Bus
2    NA              Metro
3    50              Bus
4    20              Bicicleta
5    NA              Metro
6    40              Bus
```

### Estrategia de scaffolding
1. Significado de `NA` con 0 visible al lado.
2. Pregunta worked con `is.na()`.
3. Completion para contar ausencias.
4. Error-driven learning con `sum()` y `na.rm = TRUE`.
5. Recuperación de `filter()`/`select()` y diagnóstico de missing dentro del subconjunto.
6. Transferencia a base nueva sin funciones nombradas.

### Estrategia de fading
`CONCEPTUAL GUIADO → WORKED EXAMPLE → COMPLETION → WORKED ERROR-DRIVEN → RECUPERACIÓN SEMIAUTÓNOMA → TRANSFERENCIA`

### Riesgos cognitivos
- confundir `NA` con 0;
- confundir `NA` con `"NA"`;
- intentar detectar missing mediante igualdad;
- pensar que `FALSE` en `is.na()` significa valor cero;
- memorizar posiciones de missing;
- escribir manualmente el conteo;
- creer que `na.rm = TRUE` convierte `NA` en 0;
- creer que `na.rm = TRUE` borra o modifica el objeto;
- usar `na.rm = TRUE` automáticamente sin diagnosticar missing;
- interpretar un total de valores registrados como total completo;
- creer que preparar un subconjunto elimina automáticamente sus datos ausentes;
- introducir inadvertidamente herramientas no enseñadas.

### Regla de decisión básica
Antes de calcular omitiendo valores ausentes:

1. detectar si existen;
2. contar cuántos son;
3. identificar cuántos valores quedan disponibles;
4. interpretar qué representa el cálculo resultante.

### Número de ejercicios
6

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M6-E1 | Aquí no sabemos el valor | NOVEDAD | significado de `NA` | vector, posición | baja |
| M6-E2 | ¿Dónde falta información? | NOVEDAD | `is.na()` | TRUE/FALSE | baja-media |
| M6-E3 | ¿Cuántos datos faltan? | PRÁCTICA | ninguna grande | `sum()`, `is.na()` | baja-media |
| M6-E4 | Por qué el cálculo no responde | NOVEDAD / ERROR-DRIVEN LEARNING | efecto del missing + `na.rm = TRUE` | `sum()` | media |
| M6-E5 | Prepara y revisa los casos pertinentes | RECUPERACIÓN | ninguna | `filter()`, `|>`, `select()`, `is.na()` | media |
| M6-E6 | Otra base con datos ausentes | TRANSFERENCIA | ninguna | diagnóstico + decisión | media |

---
## M6-E1 — Aquí no sabemos el valor

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Es la primera pantalla dedicada a datos ausentes. Su función no es enseñar una función, sino construir el significado de `NA` antes de que el estudiante tenga que operar con él.

La distinción crítica es:

```text
0 = valor conocido
NA = valor no disponible
```

Sin esta distinción, las operaciones posteriores pueden aprenderse mecánicamente.

### 3. Capacidad antes
Puede leer un vector, reconocer posiciones y trabajar con números y texto, pero todavía supone que cada posición contiene una respuesta conocida.

### 4. Capacidad después
Puede reconocer `NA` como ausencia de información y distinguirlo de un valor observado como 0.

### 5. Prerrequisitos
- vector;
- posición;
- número;
- texto;
- lectura de una salida.

No requiere `is.na()` ni herramientas de missing.

### 6. Gran novedad
- **Sintaxis nueva:** `NA`.
- **Concepto nuevo:** valor no disponible.
- **Decisión nueva:** distinguir ausencia de valor observado.

Existe una sola gran novedad.

### 7. Recuperaciones
Recupera:

- vector;
- correspondencia posición ↔ persona;
- lectura de valores.

### 8. Contexto sustantivo
Cinco personas responden una pregunta sobre horas de cuidado.

### 9. Dataset / objetos
Objeto de ejemplo ya disponible:

```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

Representación visible:

```text
Persona       1    2    3    4    5
Horas         6    0    NA   8    4
```

### 10. Texto para estudiante
Hasta ahora todos los valores que usamos estaban disponibles.

Pero en una encuesta puede ocurrir que una respuesta no esté registrada.

Observa:

```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

Para la persona 2 aparece:

```text
0
```

Eso es información: sabemos que reportó cero horas.

Para la persona 3 aparece:

```text
NA
```

Ahí no conocemos el valor.

En R, `NA` representa que el dato no está disponible.

Responde:

1. ¿Qué persona informó 0 horas?
2. ¿De qué persona no conocemos el valor?
3. ¿Significan lo mismo 0 y `NA`?

También recuerda:

> `NA` sin comillas representa ausencia.
>
> `"NA"` con comillas sería simplemente texto.

### 11. Modelo mental
```text
VALOR OBSERVADO
→ conozco la respuesta
→ puede ser 0

DATO AUSENTE
→ no conozco la respuesta
→ NA
```

### 12. Representación / código trabajado
Puede mostrarse y ejecutarse:

```r
horas_cuidado
```

No se requiere construir el vector.

### 13. Starter code
```r
horas_cuidado
```

Si la interfaz conceptual no necesita editor en esta pantalla, la misma representación puede mostrarse como output estático.

### 14. Acción esperada
Interpretar el vector y responder correctamente las tres preguntas conceptuales.

### 15. Solución canónica
- Persona 2 informó 0 horas.
- De la persona 3 no conocemos el valor.
- 0 y `NA` no significan lo mismo.

Resumen:

```text
Persona 2 → valor conocido = 0
Persona 3 → valor ausente = NA
```

### 16. Resultado esperado
Comprensión explícita:

```text
0 ≠ NA
NA ≠ "NA"
```

### 17. Criterio semántico de éxito
La futura comprobación debe verificar que el estudiante:

- identifica la persona 2 como caso con valor conocido 0;
- identifica la persona 3 como caso con valor ausente;
- rechaza la equivalencia `0 = NA`;
- distingue ausencia de texto literal `"NA"`.

No se evalúa producción de código complejo.

### 18. Estrategias alternativas válidas
Puede expresar “dato ausente” como:

- valor no disponible;
- respuesta no registrada;
- no conocemos el valor.

No es necesario exigir una definición literal.

### 19. Error esperado / misconception
- “NA significa cero”.
- “NA significa que la persona no hizo cuidado”.
- “NA es un error del programa”.
- “NA y `"NA"` son lo mismo”.

### 20. Feedback correcto
Bien. Cero es una respuesta conocida. `NA` indica que no tenemos un valor disponible para esa posición.

### 21. Feedback resultado correcto / estrategia incorrecta
No existe una estrategia de código que proteger en esta pantalla. Si la respuesta acierta por una explicación incorrecta, el feedback debe devolver al significado:

> La respuesta elegida coincide, pero la razón importante es que `0` es un valor registrado y `NA` representa que el valor no está disponible.

### 22. Hint 1
Pregunta primero: ¿conocemos el valor o no?

### 23. Hint 2
Para la persona 2 conocemos exactamente la respuesta: cero.

### 24. Hint 3
Persona 2 → valor conocido 0. Persona 3 → valor ausente `NA`.

### 25. Predicción
No se usa una fase formal de predicción. La pregunta conceptual “¿0 y NA significan lo mismo?” cumple la función diagnóstica necesaria.

### 26. Tipo de ejercicio
Interpretación conceptual guiada.

### 27. Andamiaje
Muy alto. El objeto, la representación y las preguntas son explícitas.

### 28. Carga cognitiva
Baja. Solo se añade una distinción conceptual a una estructura ya conocida.

### 29. Fading
E1 entrega el significado completamente. E2 utilizará ese significado para formular una pregunta computacional.

### 30. Recuperación futura
`NA` reaparece en E2–E6 y después en M8–M13 antes de descriptivos y asociaciones.

### 31. Riesgo de aprendizaje superficial
Recordar que “NA es algo vacío” sin comprender que no equivale a un valor numérico observado. La presencia simultánea de 0 y `NA` protege contra este riesgo.

### 32. Criterio de transferencia
Más adelante debe reconocer `NA` como ausencia aunque aparezca en otra variable, otra posición o una base distinta.

### 33. Notas de implementación futura
La comprobación debe ser conceptual. No exigir que el estudiante escriba `NA` ni reconstruya el vector. La interfaz puede usar opciones de respuesta, matching o selección visual.

---
## M6-E2 — ¿Dónde falta información?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Una vez construido el significado de `NA`, el estudiante necesita una forma reproducible de preguntar dónde aparecen las ausencias.

La pantalla recupera el modelo lógico de M3:

```text
PREGUNTA → TRUE/FALSE POR DATO
```

### 3. Capacidad antes
Reconoce `NA` y distingue ausencia de un valor conocido.

### 4. Capacidad después
Puede ejecutar e interpretar `is.na()` como una pregunta que devuelve `TRUE` justo donde falta información.

### 5. Prerrequisitos
- significado de `NA`;
- vector;
- TRUE/FALSE;
- correspondencia por posición.

### 6. Gran novedad
- **Sintaxis nueva:** `is.na()`.
- **Concepto nuevo:** pregunta específica por ausencia.
- **Decisión nueva:** ninguna importante; es un primer encuentro worked.

### 7. Recuperaciones
Recupera:

- TRUE/FALSE;
- pregunta aplicada a cada valor;
- posición.

### 8. Contexto sustantivo
El mismo microvector de horas de cuidado de E1.

### 9. Dataset / objetos
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 10. Texto para estudiante
Ya sabemos qué significa `NA`.

Ahora queremos preguntar automáticamente:

> ¿en qué posición falta información?

R tiene una función diseñada para esa pregunta:

```r
is.na(horas_cuidado)
```

Antes de ejecutar:

> ¿en qué posición esperas que aparezca `TRUE`?

Recuerda el significado:

```text
TRUE
→ en esa posición falta información

FALSE
→ en esa posición hay un valor disponible
```

Observa algo importante:

> la posición que contiene `0` produce `FALSE`,
> porque cero es un valor disponible.

### 11. Modelo mental
```text
DATO
↓
¿ESTÁ AUSENTE?
↓
is.na()
↓
TRUE / FALSE
```

Conexión con M3:

```text
M3: pregunta → TRUE/FALSE
M6: ¿falta información? → TRUE/FALSE
```

### 12. Representación / código trabajado
```r
is.na(horas_cuidado)
```

Representación alineada:

```text
dato        6      0      NA     8      4
is.na()    FALSE  FALSE   TRUE   FALSE  FALSE
```

### 13. Starter code
```r
is.na(horas_cuidado)
```

Es un worked example ejecutable.

### 14. Acción esperada
Predecir la posición de `TRUE`, ejecutar el código y explicar qué significa el resultado.

### 15. Solución canónica
```r
is.na(horas_cuidado)
```

### 16. Resultado esperado
```text
FALSE FALSE TRUE FALSE FALSE
```

### 17. Criterio semántico de éxito
Comprobar que:

- la pregunta se aplica a `horas_cuidado`;
- reconoce la posición 3 como ausente;
- interpreta `TRUE` como ausencia;
- interpreta `FALSE` como valor disponible;
- comprende que el 0 de la posición 2 no es missing;
- no escribe manualmente el vector lógico como estrategia.

Perturbation test recomendado: mover el `NA` y comprobar que el `TRUE` cambia de posición.

### 18. Estrategias alternativas válidas
En este primer encuentro, la construcción objetivo es `is.na()`. No se necesita enseñar otras formas de detectar ausencias.

### 19. Error esperado / misconception
- intentar igualdad con `NA`;
- creer que `FALSE` significa cero;
- hardcodear `c(FALSE, FALSE, TRUE, FALSE, FALSE)`;
- pensar que `is.na()` modifica el vector.

### 20. Feedback correcto
Bien. `TRUE` aparece justo donde falta información. `FALSE` indica que en esa posición sí hay un valor disponible.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe un vector lógico manual:

> Las respuestas coinciden, pero necesitamos que R detecte las ausencias desde el objeto. Si cambia la posición del `NA`, la respuesta debe actualizarse sola.

Si intenta comparar con `NA` mediante igualdad:

> Es razonable pensar en igualdad, pero `NA` representa un valor que no conocemos. Para preguntar específicamente si una posición está ausente usamos `is.na()`.

### 22. Hint 1
Necesitas una pregunta que sea `TRUE` justo donde falta información.

### 23. Hint 2
La función diseñada para preguntar por ausencia es `is.na()`.

### 24. Hint 3
```r
is.na(horas_cuidado)
```

### 25. Predicción
Sí. Preguntar únicamente:

> ¿en qué posición esperas `TRUE`?

Respuesta esperada: posición 3.

### 26. Tipo de ejercicio
Worked example con predicción.

### 27. Andamiaje
Alto. La función y el objeto están entregados.

### 28. Carga cognitiva
Baja-media. Aparece una función nueva, pero el formato de respuesta TRUE/FALSE ya es conocido.

### 29. Fading
E2 entrega `is.na()` completo. E3 exigirá producirlo dentro de otra función.

### 30. Recuperación futura
`is.na()` se practica en E3, se integra en E5 y alcanza transferencia en E6. Más tarde reaparece en M9/M11 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar `is.na()` como comando sin relacionar cada TRUE con una posición ausente. La representación alineada debe permanecer visible.

### 32. Criterio de transferencia
Debe poder detectar ausencias posteriormente en otra variable sin recibir el vector lógico correcto ni las posiciones de missing.

### 33. Notas de implementación futura
`horas_cuidado == NA` debe activar feedback diagnóstico específico, no una explicación extensa de lógica ternaria. No implementar operadores nuevos.

---
## M6-E3 — ¿Cuántos datos faltan?

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Detectar missing y cuantificar missing son habilidades distintas. Antes de enseñar a calcular omitiendo ausencias, el estudiante debe aprender a saber cuántas hay.

Además recupera `sum()` de M2 dentro de un problema real.

### 3. Capacidad antes
Puede identificar cada posición ausente mediante `is.na()`.

### 4. Capacidad después
Puede contar ausencias a partir del objeto mediante `sum(is.na(x))`.

### 5. Prerrequisitos
- `is.na()`;
- TRUE/FALSE;
- `sum()` como función ya conocida;
- composición simple de funciones.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** cuantificar ausencias.
- **Micro-novedad funcional:** para este uso, `sum()` cuenta los TRUE como 1.
- **Decisión nueva:** combinar dos herramientas conocidas.

No se enseña coerción formal.

### 7. Recuperaciones
Recupera:

- `sum()`;
- `is.na()`;
- TRUE/FALSE.

### 8. Contexto sustantivo
El mismo microvector:

```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

### 9. Dataset / objetos
Vector:

`horas_cuidado`

Resultado previo conocido:

```text
FALSE FALSE TRUE FALSE FALSE
```

### 10. Texto para estudiante
Ya podemos detectar dónde falta información.

Ahora queremos responder:

> ¿cuántos datos faltan?

`is.na()` produce TRUE/FALSE.

Para este uso dentro de `sum()`:

- cada `TRUE` aporta 1;
- cada `FALSE` aporta 0.

Por eso podemos combinar ambas ideas.

Completa el código para contar los valores ausentes de `horas_cuidado`.

### 11. Modelo mental
```text
is.na(x)
↓
TRUE/FALSE
↓
sum(...)
↓
NÚMERO DE AUSENCIAS
```

### 12. Representación / código trabajado
Puede mostrarse:

```text
FALSE FALSE TRUE FALSE FALSE
  0     0    1     0     0
              ↓
              1 ausencia
```

Esto es una explicación funcional, no una lección de tipos.

### 13. Starter code
```r
sum(____________________)
```

### 14. Acción esperada
Completar el interior de `sum()` con una expresión que detecte las ausencias del objeto.

### 15. Solución canónica
```r
sum(is.na(horas_cuidado))
```

### 16. Resultado esperado
```text
1
```

### 17. Criterio semántico de éxito
Comprobar que:

- el conteo depende de `horas_cuidado`;
- utiliza `is.na()` para identificar ausencias;
- utiliza `sum()` para contarlas;
- obtiene 1;
- no escribe manualmente el número como respuesta de código.

Perturbation test muy recomendado: agregar o mover un `NA` y comprobar que la misma expresión actualiza el conteo.

### 18. Estrategias alternativas válidas
La construcción curricular objetivo es `sum(is.na(horas_cuidado))`. Diferencias de espacios son válidas. No es necesario aceptar nuevas funciones de conteo no enseñadas.

### 19. Error esperado / misconception
- escribir `1` directamente;
- usar `sum(horas_cuidado)` pensando que cuenta missing;
- omitir `is.na()`;
- pensar que TRUE/FALSE deben escribirse a mano.

### 20. Feedback correcto
Bien. Primero identificaste qué posiciones están ausentes y después contaste cuántos `TRUE` produjo esa pregunta.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe solo `1`:

> El número coincide, pero no está calculado desde los datos. Necesitamos una expresión que siga funcionando si cambia la cantidad de ausencias.

### 22. Hint 1
Primero necesitas saber qué posiciones están ausentes.

### 23. Hint 2
`is.na()` produce TRUE/FALSE y `sum()` puede contar los TRUE.

### 24. Hint 3
```r
sum(is.na(horas_cuidado))
```

### 25. Predicción
No se añade una fase separada. La tarea de conteo ya obliga a interpretar la salida anterior.

### 26. Tipo de ejercicio
Completion problem.

### 27. Andamiaje
Medio. `sum()` está visible; el estudiante debe recuperar `is.na()` y el objeto.

### 28. Carga cognitiva
Baja-media. No hay gran sintaxis nueva; se combinan dos herramientas sencillas.

### 29. Fading
E2 entregó `is.na()` completo. E3 obliga a recuperarlo. E4 mantendrá diagnóstico visible pero añadirá el efecto sobre un cálculo.

### 30. Recuperación futura
El patrón detectar → contar reaparece en E5/E6 y conceptualmente antes de análisis posteriores con missing.

### 31. Riesgo de aprendizaje superficial
Memorizar `sum(is.na())` sin saber que está contando respuestas TRUE. La representación intermedia debe hacer visible la lógica.

### 32. Criterio de transferencia
Debe poder contar más adelante las ausencias de otro vector o columna aunque cambien las posiciones y el número de `NA`.

### 33. Notas de implementación futura
No comparar código literal si el estado semántico es equivalente, pero no introducir como alternativas funciones no enseñadas. El perturbation test debe cambiar el número de ausencias.

---
## M6-E4 — Por qué el cálculo no responde

### 1. Rol pedagógico
NOVEDAD / ERROR-DRIVEN LEARNING.

### 2. Por qué existe
Hasta E3 el estudiante sabe qué es missing, dónde aparece y cuánto falta. Ahora necesita comprender por qué la ausencia afecta un cálculo y qué significa calcular usando solo los valores disponibles.

Se utiliza una función ya conocida (`sum()`) para que la atención se concentre en missing.

### 3. Capacidad antes
Puede detectar y contar ausencias, y conoce `sum()`.

### 4. Capacidad después
Comprende por qué `sum(x)` puede devolver `NA`, interpreta `na.rm = TRUE` correctamente y distingue total de valores registrados de un total completo desconocido.

### 5. Prerrequisitos
- `NA`;
- `is.na()`;
- `sum(is.na())`;
- `sum()`;
- objeto/vector;
- lectura de output.

### 6. Gran novedad
- **Sintaxis nueva:** `na.rm = TRUE`.
- **Concepto nuevo:** una ausencia puede propagarse al resultado; una función puede calcular solo con valores disponibles.
- **Decisión nueva:** interpretar si ese cálculo responde realmente a la pregunta.

La unidad es coherente: “efecto del missing en el cálculo y opción para usar disponibles”.

### 7. Recuperaciones
Recupera:

- `sum()`;
- el diagnóstico de E3;
- diferencia `NA` vs 0.

### 8. Contexto sustantivo
El mismo microvector de cinco personas.

### 9. Dataset / objetos
```r
horas_cuidado <- c(6, 0, NA, 8, 4)
```

Estado ya conocido:

```text
casos totales:       5
datos ausentes:      1
datos disponibles:   4
```

### 10. Texto para estudiante
Ya sabemos que falta un dato.

Ahora intentemos calcular el total:

```r
sum(horas_cuidado)
```

Antes de ejecutar:

> ¿esperas obtener un número o `NA`?

Ejecuta.

R devuelve:

```text
NA
```

Eso no significa que R se haya roto.

Falta uno de los valores y R no inventa qué número debería ocupar esa posición.

Si la pregunta es:

> ¿cuál es el total de las horas **registradas**?

podemos pedir a `sum()` que utilice únicamente los valores disponibles:

```r
sum(horas_cuidado, na.rm = TRUE)
```

Aquí `na.rm = TRUE` configura una opción del cálculo.

No está preguntando igualdad y no cambia el objeto.

### 11. Modelo mental
```text
DATOS CON NA
↓
sum(x)
↓
NA

DIAGNÓSTICO YA HECHO
↓
PREGUNTA: TOTAL DE LOS VALORES DISPONIBLES
↓
sum(x, na.rm = TRUE)
↓
RESULTADO CON N DISPONIBLE
```

### 12. Representación / código trabajado
```r
sum(horas_cuidado)

sum(horas_cuidado, na.rm = TRUE)

horas_cuidado
```

Representación conceptual:

```text
6 + 0 + 8 + 4 = 18

casos totales:       5
datos ausentes:      1
datos disponibles:   4
```

### 13. Starter code
```r
sum(horas_cuidado)

sum(horas_cuidado, na.rm = TRUE)

horas_cuidado
```

Es un worked/error-driven example. No se exige todavía producir autónomamente la opción.

### 14. Acción esperada
1. predecir si `sum(horas_cuidado)` devolverá número o `NA`;
2. ejecutar;
3. ejecutar el cálculo con valores disponibles;
4. comprobar que `horas_cuidado` sigue conteniendo `NA`;
5. responder una pregunta contrafactual para distinguir omisión de reemplazo.

### 15. Solución canónica
```r
sum(horas_cuidado)

sum(horas_cuidado, na.rm = TRUE)

horas_cuidado
```

Respuestas conceptuales:

- primer resultado: `NA`;
- total de valores registrados: 18;
- el objeto sigue siendo `6 0 NA 8 4`;
- si el dato faltante fuese 10, el total completo sería 28.

### 16. Resultado esperado
```text
sum(horas_cuidado)
→ NA

sum(horas_cuidado, na.rm = TRUE)
→ 18

horas_cuidado
→ 6 0 NA 8 4
```

Interpretación:

> 18 es el total de los cuatro valores registrados.
>
> No conocemos el total completo de las cinco personas.

### 17. Criterio semántico de éxito
Comprobar que el estudiante:

- reconoce que el cálculo inicial devuelve `NA`;
- explica que falta información;
- entiende que 18 usa cuatro valores;
- no interpreta el `NA` como 0;
- comprende que `na.rm = TRUE` no rellena ni elimina el dato;
- reconoce que el objeto original sigue intacto;
- responde correctamente el contrafactual: si el valor faltante fuera 10, el total completo sería 28;
- distingue N total = 5 de N disponible = 4.

### 18. Estrategias alternativas válidas
Se aceptan explicaciones equivalentes como “omite la posición ausente para ese cálculo” o “usa solo los valores observados”. No aceptar explicaciones que impliquen reemplazo por cero.

### 19. Error esperado / misconception
- creer que `NA` apareció porque `sum()` falló;
- creer que `na.rm = TRUE` convierte NA a 0;
- creer que borra NA del vector;
- interpretar 18 como total real de las cinco personas;
- usar automáticamente `na.rm = TRUE` sin diagnóstico;
- confundir el `=` de la opción con `==` o con asignación canónica.

### 20. Feedback correcto
Bien. El primer cálculo no puede producir un total completo porque falta un valor. Con `na.rm = TRUE`, `sum()` utiliza únicamente los cuatro valores disponibles y obtiene 18.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice que el `NA` se convirtió en 0:

> El resultado numérico coincide, pero la interpretación no. El valor ausente sigue siendo desconocido y permanece como `NA`; simplemente no participó en ese cálculo.

Si presenta 18 como total completo:

> 18 corresponde a los cuatro valores registrados. Como falta una respuesta, no conocemos el total completo de las cinco personas.

### 22. Hint 1
¿Conocemos los cinco valores necesarios para calcular un total completo?

### 23. Hint 2
Algunas funciones pueden calcular usando únicamente los valores disponibles, pero primero debemos reconocer cuántos faltan.

### 24. Hint 3
```r
sum(horas_cuidado, na.rm = TRUE)
```

### 25. Predicción
Sí. Antes de `sum(horas_cuidado)`:

> ¿esperas un número o `NA`?

### 26. Tipo de ejercicio
Error-driven worked example.

### 27. Andamiaje
Alto. El código está entregado; la exigencia principal es interpretar.

### 28. Carga cognitiva
Media. La función principal ya es conocida. La atención se concentra en propagación del missing, la opción `na.rm` y la interpretación del N utilizado.

### 29. Fading
E4 entrega `na.rm = TRUE` completamente. E6 pedirá reconocer por sí mismo cuándo hace falta utilizarlo.

### 30. Recuperación futura
`na.rm` reaparece funcionalmente en M8–M11. La regla detectar → contar → decidir se recupera antes de asociaciones y descriptivos.

### 31. Riesgo de aprendizaje superficial
Convertir `na.rm = TRUE` en una receta para “arreglar” cualquier error. La secuencia del módulo y la pregunta contrafactual deben bloquear esa interpretación.

### 32. Criterio de transferencia
Debe poder más adelante reconocer una variable con missing, diagnosticarlo y utilizar una opción de cálculo con valores disponibles solo cuando la pregunta lo justifique.

### 33. Notas de implementación futura
No introducir `mean()`, `length()`, `complete.cases()` ni nuevos operadores. Debe existir feedback específico para las interpretaciones “NA = 0” y “na.rm borra datos”. La comprobación debe incluir la pregunta contrafactual.

---
## M6-E5 — Prepara y revisa los casos pertinentes

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
Recupera la preparación de datos de M5 dentro de un problema auténtico de missing.

La idea nueva del contexto, pero no una nueva herramienta, es:

> preparar un subconjunto no elimina automáticamente sus valores ausentes.

E5 evita enseñar todavía cómo excluir casos incompletos mediante nueva sintaxis.

### 3. Capacidad antes
Puede detectar, contar e interpretar missing en un vector y conoce `filter()`, `select()`, `|>` y asignación desde M5.

### 4. Capacidad después
Puede preparar los casos y variables pertinentes y luego diagnosticar las ausencias dentro del subconjunto obtenido.

### 5. Prerrequisitos
- `filter()`;
- `|>`;
- `select()`;
- `<-`;
- `==`;
- `$`;
- `is.na()`;
- `sum(is.na())`;
- caso/variable.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno grande; se consolida que preparación y completitud son problemas distintos.
- **Decisión nueva:** combinar herramientas conocidas en el orden necesario.

### 7. Recuperaciones
Recupera M5:

- filtrar casos;
- seleccionar variables;
- pipe;
- guardar resultado.

Recupera M6:

- detectar y contar missing.

### 8. Contexto sustantivo
Queremos revisar las horas de cuidado de las personas que trabajan.

### 9. Dataset / objetos
Desde M6, `encuesta_social_demo` contiene una nueva variable:

```text
id   trabaja   horas_cuidado
1    No        6
2    Sí        NA
3    No        0
4    No        8
5    Sí        4
6    Sí        5
7    No        NA
8    Sí        7
```

Las variables anteriores mantienen exactamente sus valores locked.

Casos que trabajan:

2, 5, 6, 8.

### 10. Texto para estudiante
Hasta ahora trabajamos el missing en un vector pequeño.

Volvamos a `encuesta_social_demo`.

En este módulo aparece una nueva variable:

`horas_cuidado`

Las variables que ya conocíamos mantienen sus valores.

Queremos estudiar las horas de cuidado de las personas que trabajan.

Primero prepara una base que:

- conserve solo quienes trabajan;
- conserve únicamente `id` y `horas_cuidado`.

Después responde:

> ¿cuántos datos de `horas_cuidado` faltan en ese subconjunto?

Observa si preparar los datos hizo desaparecer o no el missing.

### 11. Modelo mental
```text
PREGUNTA SUSTANTIVA
↓
FILTER: CASOS
↓
SELECT: VARIABLES
↓
SUBCONJUNTO
↓
DIAGNOSTICAR MISSING
↓
CONTAR AUSENCIAS
```

### 12. Representación / código trabajado
No se entrega una solución completa. Puede mostrarse solo el flujo:

```text
encuesta_social_demo
↓
personas que trabajan
↓
id + horas_cuidado
↓
revisar missing
```

### 13. Starter code
```r
datos_trabajan <- encuesta_social_demo |>
  filter(__________________) |>
  select(____, ____________)

# cuenta cuántos valores faltan en horas_cuidado
```

### 14. Acción esperada
1. completar la condición de filtrado;
2. completar las dos variables de `select()`;
3. crear `datos_trabajan`;
4. contar los missing de `datos_trabajan$horas_cuidado`.

### 15. Solución canónica
```r
datos_trabajan <- encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(id, horas_cuidado)

sum(is.na(datos_trabajan$horas_cuidado))
```

### 16. Resultado esperado
Objeto intermedio:

```text
id   horas_cuidado
2    NA
5    4
6    5
8    7
```

Conteo:

```text
1
```

Interpretación:

> preparar el grupo pertinente no eliminó automáticamente el dato ausente.

### 17. Criterio semántico de éxito
Comprobar:

- existe `datos_trabajan`;
- contiene casos originales 2,5,6,8;
- contiene exactamente `id` y `horas_cuidado`;
- el caso 2 mantiene `NA`;
- usa una estrategia dependiente de `trabaja == "Sí"`;
- el conteo de missing depende de `datos_trabajan$horas_cuidado`;
- obtiene 1;
- no hardcodea filas ni conteo.

Perturbation test muy recomendado: modificar quién trabaja y mover un `NA`. El pipeline y diagnóstico deben adaptarse.

### 18. Estrategias alternativas válidas
Se aceptan diferencias de formato y espacios. El objetivo requiere recuperar `filter()`, `select()` y `|>` porque son parte de la recuperación espaciada. No introducir sintaxis nueva para excluir missing.

### 19. Error esperado / misconception
- creer que `filter(trabaja == "Sí")` elimina los NA de otras variables;
- hardcodear casos 2,5,6,8;
- seleccionar columnas por posición;
- escribir `1` manualmente;
- intentar eliminar el `NA` en vez de diagnosticarlo;
- introducir una forma nueva no enseñada para quedarse con “no NA”.

### 20. Feedback correcto
Bien. Preparaste el grupo que necesitabas y después revisaste sus ausencias. El filtrado no eliminó automáticamente el `NA` de `horas_cuidado`.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea filas:

> El subconjunto coincide, pero depende de las posiciones actuales. Queremos que la condición decida quiénes trabajan.

Si escribe el conteo manual:

> El número coincide, pero debe calcularse desde el subconjunto preparado para seguir funcionando si cambian los datos.

Si intenta “limpiar” el NA:

> En esta pantalla no necesitamos eliminarlo. Primero queremos comprobar si el subconjunto pertinente contiene información ausente.

### 22. Hint 1
Primero decide qué casos necesitas y qué variables conservar.

### 23. Hint 2
Después de crear `datos_trabajan`, revisa su variable `horas_cuidado` con la herramienta de missing que ya conoces.

### 24. Hint 3
```r
datos_trabajan <- encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(id, horas_cuidado)

sum(is.na(datos_trabajan$horas_cuidado))
```

### 25. Predicción
No se agrega una fase formal. El resultado intermedio debe observarse antes de contar.

### 26. Tipo de ejercicio
Recuperación semi-autónoma.

### 27. Andamiaje
Medio. La estructura del pipeline está visible, pero faltan condición, variables y código de diagnóstico.

### 28. Carga cognitiva
Media. Interactúan varias herramientas conocidas, pero no aparece sintaxis nueva.

### 29. Fading
E5 recupera con apoyo parcial. E6 retirará nombres de funciones y estructura de código.

### 30. Recuperación futura
Preparación + missing reaparece en M8, M9, M11 y M13.

### 31. Riesgo de aprendizaje superficial
Creer que “preparar datos” equivale a “datos completos”. La presencia visible del `NA` después del pipeline debe combatir esa idea.

### 32. Criterio de transferencia
Debe poder más adelante preparar otro subconjunto y después diagnosticar missing sin que la consigna separe explícitamente ambas tareas.

### 33. Notas de implementación futura
No introducir herramientas para eliminar missing. El grader debe verificar estructura del objeto y diagnóstico por separado para ofrecer feedback específico.

---
## M6-E6 — Otra base con datos ausentes

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
Es la evidencia final de M6. Cambia base, variable, posiciones de missing y valores para comprobar que el estudiante no memorizó el ejemplo de `horas_cuidado`.

Debe transferir la secuencia completa:

```text
detectar → contar → calcular con disponibles cuando corresponde → interpretar N
```

### 3. Capacidad antes
Puede reconocer, detectar, contar e interpretar missing, y ha visto `na.rm = TRUE` en un worked example.

### 4. Capacidad después
Puede diagnosticar missing en una base nueva, elegir una estrategia de cálculo con valores disponibles y explicar exactamente cuántos casos aportaron información.

### 5. Prerrequisitos
- `$`;
- `is.na()`;
- `sum(is.na())`;
- `sum()`;
- `na.rm = TRUE`;
- interpretación N total/N disponible.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** elegir autónomamente las herramientas conocidas y justificar el resultado.

### 7. Recuperaciones
Recupera toda la ruta de M6.

No requiere `filter()`, `select()` ni nuevas funciones.

### 8. Contexto sustantivo
Encuesta de barrio sobre minutos de viaje.

### 9. Dataset / objetos
Objeto ya disponible:

`encuesta_barrio`

```text
id   minutos_viaje   transporte
1    35              Bus
2    NA              Metro
3    50              Bus
4    20              Bicicleta
5    NA              Metro
6    40              Bus
```

### 10. Texto para estudiante
Ahora cambia la base.

Queremos conocer el total de minutos de viaje **registrados** en esta pequeña encuesta.

Antes de calcular:

1. revisa dónde faltan datos en `minutos_viaje`;
2. cuenta cuántos datos faltan;
3. calcula el total usando los valores disponibles;
4. indica cuántos de los seis casos aportaron un valor al cálculo.

No se indican las funciones.

Decide qué herramientas conocidas necesitas.

### 11. Modelo mental
```text
BASE NUEVA
↓
VARIABLE
↓
DETECTAR
↓
CONTAR
↓
DECIDIR
↓
CALCULAR CON DISPONIBLES
↓
INTERPRETAR N USADO
```

### 12. Representación / código trabajado
No hay worked example nuevo.

Solo se muestra `encuesta_barrio`.

### 13. Starter code
```r
# revisa dónde falta minutos_viaje


# cuenta cuántos valores faltan


# calcula el total de los minutos registrados
```

### 14. Acción esperada
Producir por sí mismo:

- detección de missing;
- conteo;
- cálculo del total registrado;
- interpretación del número de casos utilizados.

### 15. Solución canónica
```r
is.na(encuesta_barrio$minutos_viaje)

sum(is.na(encuesta_barrio$minutos_viaje))

sum(encuesta_barrio$minutos_viaje, na.rm = TRUE)
```

Interpretación:

> faltan 2 valores;
>
> hay 4 valores disponibles;
>
> el total registrado es 145;
>
> no conocemos el total completo de los 6 casos.

### 16. Resultado esperado
Detección:

```text
FALSE TRUE FALSE FALSE TRUE FALSE
```

Conteo:

```text
2
```

Total de valores registrados:

```text
145
```

Resumen:

```text
casos totales:        6
datos ausentes:       2
datos disponibles:    4
total registrado:     145
```

### 17. Criterio semántico de éxito
Comprobar por componentes:

**Detección**
- usa `is.na()` sobre `encuesta_barrio$minutos_viaje`;
- resultado lógico correcto.

**Conteo**
- deriva el número desde los datos;
- resultado 2.

**Cálculo**
- usa `sum()` sobre la variable;
- utiliza la opción para trabajar con valores disponibles;
- resultado 145.

**Interpretación**
- identifica 6 casos totales;
- identifica 2 ausentes;
- identifica 4 disponibles;
- presenta 145 como total de los valores registrados;
- no afirma que 145 sea el total completo real de los seis casos.

Perturbation test muy recomendado: cambiar posiciones de missing, número de missing y valores observados.

### 18. Estrategias alternativas válidas
Diferencias de formato son válidas. La estrategia debe depender de la variable y de los datos. No se admiten resultados manuales como evidencia de dominio.

### 19. Error esperado / misconception
- memorizar posiciones 2 y 5;
- escribir `2` manualmente;
- escribir `145` manualmente;
- olvidar diagnosticar antes de calcular;
- interpretar 145 como total de los seis casos;
- asumir que los dos missing equivalen a 0;
- usar una herramienta no enseñada para eliminarlos.

### 20. Feedback correcto
Bien. Primero diagnosticaste las ausencias y después calculaste usando los valores disponibles. También identificaste cuántos casos realmente aportaron información.

### 21. Feedback resultado correcto / estrategia incorrecta
Si el total es 145 pero lo calculó manualmente:

> El total coincide, pero necesitamos una estrategia que se actualice si cambian los valores observados.

Si afirma que 145 es el total completo:

> 145 resume únicamente los cuatro valores registrados. Como dos valores siguen ausentes, no conocemos el total completo de los seis casos.

### 22. Hint 1
Antes de calcular, revisa si `minutos_viaje` contiene valores ausentes.

### 23. Hint 2
Primero detecta y cuenta las ausencias. Después piensa cómo pedir a `sum()` que use los valores disponibles.

### 24. Hint 3
```r
is.na(encuesta_barrio$minutos_viaje)

sum(is.na(encuesta_barrio$minutos_viaje))

sum(encuesta_barrio$minutos_viaje, na.rm = TRUE)
```

### 25. Predicción
No se usa una fase separada. La consigna integrada ya exige anticipar y decidir.

### 26. Tipo de ejercicio
Transferencia cercana.

### 27. Andamiaje
Bajo. Hay tres comentarios que estructuran el problema, pero ninguna función es nombrada en la consigna ni entregada en el starter.

### 28. Carga cognitiva
Media. No hay sintaxis nueva; la dificultad está en recuperar y coordinar una secuencia de decisiones.

### 29. Fading
Es el punto final de M6. Se retiran nombres de funciones, worked code y estructura parcial.

### 30. Recuperación futura
La estrategia de missing se recupera antes de descriptivos y asociaciones en M8–M13, especialmente M9/M11.

### 31. Riesgo de aprendizaje superficial
Aplicar `na.rm = TRUE` sin diagnosticar o interpretar N. Por eso la tarea exige explícitamente detectar, contar e informar cuántos casos aportaron datos.

### 32. Criterio de transferencia
Existe evidencia de transferencia si puede repetir la ruta en otra base/variable, con posiciones y cantidades de missing diferentes, sin que la consigna nombre las funciones.

### 33. Notas de implementación futura
El grader debe separar diagnóstico, conteo, cálculo e interpretación para ofrecer feedback localizado. No penalizar formato cosmético del código.

---

# Cierre conceptual de M6 y puente a M7

Después de E6 mostrar:

> Ya podemos revisar si una variable tiene datos ausentes,
> contar cuántos faltan y decidir cuándo tiene sentido trabajar
> con los valores disponibles.
>
> Una vez preparada la información todavía queda otra pregunta:
>
> **¿cómo deberíamos describir esta variable?**
>
> Eso dependerá de qué representan sus valores.

La transición termina ahí.

M6 NO introduce todavía:

- variable categórica;
- variable cuantitativa;
- `table()`;
- `prop.table()`;
- `barplot()`.

# Retención esperada después de una semana

## Reconocimiento
El estudiante debería reconocer:

```r
NA
```

como dato ausente.

Debería reconocer:

```r
is.na()
```

como una pregunta por ausencia.

Debería reconocer:

```r
na.rm = TRUE
```

como una opción que hace que una función calcule usando los valores disponibles.

## Producción
Con poca ayuda debería poder producir:

```r
is.na(x)
```

y:

```r
sum(is.na(x))
```

## Comprensión
Debe poder explicar que:

- `NA` no es 0;
- `na.rm = TRUE` no modifica el objeto;
- `na.rm = TRUE` no rellena ni convierte el missing;
- un cálculo puede utilizar menos casos que la base completa;
- el N utilizado debe interpretarse.

## Habilidad funcional
Puede requerir recordatorio de la escritura exacta:

```r
na.rm = TRUE
```

## Decisión
Antes de omitir missing debe preguntarse:

```text
¿cuántos valores faltan?
¿cuántos quedan disponibles?
¿qué representa el cálculo resultante?
```

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 2
- NOVEDAD / ERROR-DRIVEN LEARNING: 1
- PRÁCTICA: 1
- RECUPERACIÓN: 1
- TRANSFERENCIA: 1

## Porcentaje local de ejercicios con gran novedad
3 de 6: 50 %.

Este porcentaje no obliga a modificar la arquitectura porque:

- el criterio de ≤40 % pertenece al recorrido global de 88 ejercicios;
- la distribución maestra global permanece en 39,8 % de novedad;
- E1, E2 y E4 aíslan una sola gran novedad cada uno;
- E3 practica;
- E5 recupera;
- E6 transfiere.

## Habilidades nucleares relativamente consolidadas
- significado de `NA`;
- 0 ≠ NA;
- `is.na()`;
- `sum(is.na())`;
- diagnóstico antes de omisión;
- N total vs N disponible;
- interpretación de un cálculo con valores observados.

## Habilidad funcional
```r
na.rm = TRUE
```

## Habilidades pospuestas
- `mean()`;
- `complete.cases()`;
- `!`;
- `length()`;
- imputación;
- mecanismos avanzados de missing.

## Recuperaciones futuras
M8–M13 deben recuperar decisiones sobre missing antes de descriptivos y asociaciones.

Según la trayectoria del curso:

- `is.na()` vuelve a producirse/recuperarse en M9/M11;
- missing se integra en M13;
- `na.rm` permanece funcional en M8–M11.

## Riesgos de sobrecarga controlados
- E1 usa un vector pequeño;
- E2 introduce una sola función;
- E3 no introduce sintaxis grande;
- E4 usa `sum()` ya conocido en vez de introducir `mean()`;
- E5 no introduce formas nuevas de eliminar missing;
- E6 no contiene sintaxis nueva.

## Comprobación de una gran novedad por ejercicio
Cumplida:

```text
E1 → significado de NA
E2 → is.na()
E3 → práctica
E4 → efecto + na.rm como una unidad
E5 → recuperación
E6 → transferencia
```

## Checkpoint
No.

M6 no contiene checkpoint formal. E6 funciona como transferencia del módulo.

# Contrato de datos

## `encuesta_social_demo`
M6 preserva exactamente las variables y valores locked de M4–M5.

La única ampliación es la aparición explícita de:

`horas_cuidado`

con:

```text
6, NA, 0, 8, 4, 5, NA, 7
```

Esta variable pasa a formar parte del contrato pedagógico de `encuesta_social_demo` desde M6.

Cualquier dataset lock global futuro para M4–M8 debe preservar:

- las cinco variables ya locked;
- estos valores de `horas_cuidado`;

o requerirá una modificación deliberada de los Markdown locked antes de implementación.

## `encuesta_barrio`
La base de transferencia de E6 queda fijada pedagógicamente como:

```text
id   minutos_viaje   transporte
1    35              Bus
2    NA              Metro
3    50              Bus
4    20              Bicicleta
5    NA              Metro
6    40              Bus
```

# Declaración de lock

M6 queda pedagógicamente cerrado con 6 ejercicios.

- **Sintaxis introducida:** `NA`, `is.na()`, `na.rm = TRUE`.
- **Habilidad funcional:** `na.rm = TRUE`.
- **Conceptos nucleares:** ausencia vs cero, detectar, contar, efecto en cálculo, N total vs N disponible.
- **Habilidades pospuestas:** `mean()`, `complete.cases()`, `!`, `length()` y tratamiento avanzado de missing.
- **Recuperación:** `sum()`, `$`, `filter()`, `select()`, `|>`, `<-`, `==`.
- **Transferencia:** E6 diagnostica y calcula en `encuesta_barrio`.
- **Puente a M7:** datos preparados y revisados por missing → decidir cómo describir una variable según lo que representan sus valores.

# M6 PEDAGOGICALLY LOCKED
