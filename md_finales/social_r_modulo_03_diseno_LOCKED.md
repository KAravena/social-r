# Social R — Módulo 3
## Hacer preguntas a los datos

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede crear vectores numéricos, comprender su orden y seleccionar uno o varios valores cuando conoce sus posiciones.

### Capacidad después
Puede formular comparaciones simples, interpretar las respuestas `TRUE/FALSE` y utilizar una condición para seleccionar valores de un vector según lo que cumplen, en vez de según posiciones memorizadas.

### Pregunta central
¿Cómo puedo encontrar valores por lo que cumplen en vez de saber previamente dónde están?

### Modelo mental
`PREGUNTA → COMPARACIÓN → TRUE/FALSE → UNA RESPUESTA POR DATO → VECTOR LÓGICO → TRUE CONSERVA → SELECCIÓN`

### Habilidades nucleares
Al terminar M3, el estudiante debe poder:

- leer `>` como una pregunta de comparación;
- interpretar `TRUE` y `FALSE` como respuestas producidas por R;
- aplicar una comparación a un vector;
- comprender que existe una respuesta lógica por cada valor y que ambas secuencias mantienen correspondencia posicional;
- guardar el resultado de una comparación dentro de un objeto;
- comprender qué es un vector lógico en el nivel necesario para este curso;
- utilizar un vector lógico dentro de `[]`;
- seleccionar valores por una condición y no por posiciones memorizadas;
- reconocer y producir una selección lógica simple;
- distinguir `<-` de `==`.

### Habilidades en consolidación
Quedan en consolidación:

- la forma compacta `x[x > valor]`;
- `==`;
- selección lógica con texto.

Estas habilidades reaparecerán posteriormente y no deben tratarse como dominio completamente autónomo después de una sola aparición.

### Habilidades recuperadas
M3 recupera desde M1 y M2:

- `<-`;
- consulta de objetos;
- reutilización;
- números y texto;
- `c()`;
- vectores;
- orden;
- posición;
- `[]`.

La recuperación ocurre dentro de problemas reales; no se reenseñan los módulos anteriores.

### Sintaxis nueva
- `>` para preguntar si un valor es mayor que otro;
- `==` para preguntar si dos valores son iguales;
- `x[condicion]` como selección lógica;
- forma compacta `x[x > valor]` únicamente después de comprender la forma descompuesta.

### Sintaxis que NO se introduce
No se introducen:

- `<`;
- `>=`;
- `<=`;
- `!=`;
- `&`;
- `|`;
- `%in%`;
- condiciones múltiples;
- data frames;
- `$`;
- `filter()`;
- `select()`;
- pipes;
- missing.

### Dataset
Microdatos visibles en vectores pequeños de tiempos de viaje, horas de estudio, respuestas de carrera y horas de cuidado.

M3 trabaja con una característica por vez. No introduce todavía filas, columnas, casos, variables ni data frames.

### Estrategia de scaffolding
1. Pregunta escalar y primer significado de `TRUE/FALSE`.
2. Misma pregunta aplicada a todos los valores de un vector.
3. Guardar las respuestas para hacer visible el vector lógico.
4. Worked example de selección mediante ese vector lógico.
5. Integración de condición + selección y presentación de la forma compacta.
6. Generalización a texto mediante `==`.
7. Checkpoint con datos nuevos y sin sintaxis nueva.

### Estrategia de fading
`PREGUNTAR → OBSERVAR RESPUESTAS → GUARDAR RESPUESTAS → USAR RESPUESTAS → COMPONER → GENERALIZAR → DECIDIR`

### Riesgos cognitivos
- tratar `TRUE/FALSE` como palabras que debe escribir manualmente;
- no comprender que cada respuesta corresponde al dato en la misma posición;
- pensar que `>` ya selecciona valores;
- memorizar “TRUE conserva” como regla arbitraria sin entender la correspondencia;
- usar posiciones conocidas en lugar de una condición;
- hardcodear resultados;
- confundir `<-` con `==`;
- invertir una comparación;
- perderse ante la doble aparición del mismo objeto en `x[x > valor]`;
- interpretar la forma compacta como receta opaca;
- olvidar las comillas al comparar texto.

### Número de ejercicios
7

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M3-E1 | De posiciones a preguntas | NOVEDAD | `>` + significado de `TRUE/FALSE` | ejecución y lectura de resultados | baja-media |
| M3-E2 | Pregunta a todos los valores | PRÁCTICA | comparación aplicada a un vector | `c()`, vector, orden, `>` | baja-media |
| M3-E3 | Guarda las respuestas | PRÁCTICA | vector lógico como resultado guardado | `<-`, comparación vectorizada | baja-media |
| M3-E4 | TRUE conserva | NOVEDAD | selección lógica con `x[condicion]` | `[]`, vector lógico | media |
| M3-E5 | Selecciona tú | PRÁCTICA / INTEGRACIÓN | forma compacta como composición | `>`, `[]`, condición | media |
| M3-E6 | También podemos preguntar por texto | NOVEDAD | `==` | texto, vector lógico, selección | baja-media |
| M3-E7 | Checkpoint A: encuentra lo que buscas | TRANSFERENCIA / CHECKPOINT | ninguna | fundamentos M1–M3 relevantes | media |

---

## M3-E1 — De posiciones a preguntas

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Abre M3 exactamente desde la necesidad creada al final de M2. Hasta ahora el estudiante seleccionaba cuando conocía la posición. E1 introduce una nueva posibilidad: formular una pregunta sobre un valor y dejar que R responda si la afirmación se cumple.

### 3. Capacidad antes
Puede seleccionar un valor si sabe dónde está dentro de un vector.

### 4. Capacidad después
Puede leer una comparación con `>` como una pregunta y comprender qué significan `TRUE` y `FALSE`.

### 5. Prerrequisitos
- ejecutar código;
- leer resultados;
- números;
- comprender la pregunta cotidiana “¿es mayor que...?”.

No requiere conocimiento previo de lógica computacional.

### 6. Gran novedad
- **Sintaxis nueva:** `>`.
- **Concepto nuevo:** R puede evaluar una afirmación y responder `TRUE/FALSE`.
- **Decisión nueva:** mínima; el código está trabajado.

`>` y `TRUE/FALSE` se enseñan como una sola unidad conceptual: **hacer una pregunta de comparación a R**.

### 7. Recuperaciones
Recupera ejecución, lectura de outputs y la necesidad conceptual dejada por M2: buscar por lo que un valor cumple en lugar de por su posición.

### 8. Contexto sustantivo
Tiempos de viaje.

Pregunta inicial:

> ¿35 minutos es más que 30 minutos?

### 9. Dataset / objetos
No se necesita un objeto todavía.

Comparaciones:

```r
35 > 30
25 > 30
```

### 10. Texto para estudiante
**Situación.** Hasta ahora, para recuperar un valor necesitabas saber su posición.

Pero ahora queremos responder una pregunta distinta:

> ¿35 minutos es más que 30 minutos?

En R podemos escribir esa pregunta así:

```r
35 > 30
```

Lee `>` como **“es mayor que”**.

Antes de ejecutar, piensa:

> ¿La afirmación se cumple?

Ejecuta.

R responde:

```text
TRUE
```

`TRUE` significa:

> la afirmación se cumple.

Ahora prueba:

```r
25 > 30
```

R responde:

```text
FALSE
```

`FALSE` significa:

> la afirmación no se cumple.

De manera informal puedes pensar:

- `TRUE` → sí, se cumple;
- `FALSE` → no, no se cumple.

Pero recuerda: `TRUE` y `FALSE` son valores que **R produce** al evaluar la pregunta.

En R se llaman **valores lógicos**.

### 11. Modelo mental
`PREGUNTA COTIDIANA → COMPARACIÓN EN R → TRUE/FALSE`

### 12. Código trabajado / ejemplo
```r
35 > 30
25 > 30
```

### 13. Starter code
```r
35 > 30

25 > 30
```

### 14. Acción esperada
Predecir si cada afirmación se cumple, ejecutar ambas comparaciones y conectar cada resultado con el significado de `TRUE` y `FALSE`.

### 15. Solución canónica
```r
35 > 30
25 > 30
```

### 16. Resultado esperado
Primera comparación:

```text
TRUE
```

Segunda comparación:

```text
FALSE
```

### 17. Criterio semántico de éxito
Comprobar que:

- se ejecutan comparaciones reales con `>`;
- `35 > 30` produce `TRUE`;
- `25 > 30` produce `FALSE`;
- no se sustituyen las comparaciones por los literales `TRUE` y `FALSE`.

No hace falta exigir todavía producción autónoma de una comparación nueva.

### 18. Estrategias alternativas válidas
Se toleran espacios diferentes alrededor de `>`. El objetivo exige que R evalúe las comparaciones; escribir manualmente las respuestas no constituye una estrategia equivalente.

### 19. Error esperado / misconception
- escribir `TRUE` y `FALSE` directamente;
- creer que `>` selecciona datos;
- interpretar `TRUE/FALSE` como texto;
- leer la dirección del símbolo al revés.

### 20. Feedback correcto
**Bien.** Usaste `>` para formular una pregunta y R respondió si la afirmación se cumplía. `TRUE` y `FALSE` son resultados producidos por la comparación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `TRUE` y `FALSE`:

> Esas son las respuestas correctas, pero aquí queremos que R las produzca evaluando las comparaciones.

Si interpreta `>` como selección:

> `>` todavía no selecciona valores. Primero construye una pregunta que R responde con `TRUE` o `FALSE`.

### 22. Hint 1
Lee `35 > 30` como una pregunta: “¿35 es mayor que 30?”.

### 23. Hint 2
R responderá `TRUE` si la afirmación se cumple y `FALSE` si no se cumple.

### 24. Hint 3
Ejecuta:

```r
35 > 30
25 > 30
```

y compara las dos respuestas.

### 25. Predicción
Sí.

Antes de ejecutar cada comparación, pedir:

> ¿Esperas `TRUE` o `FALSE`?

### 26. Tipo de ejercicio
Worked example con predicción.

### 27. Andamiaje
Muy alto: pregunta cotidiana, traducción a código, interpretación y código completo.

### 28. Carga cognitiva
**Baja-media.** La matemática es deliberadamente simple. La carga está en aprender que una comparación funciona como pregunta y que R produce un tipo de respuesta nuevo.

### 29. Fading
E1 entrega comparaciones escalares completas. E2 aplicará la misma idea a un vector completo.

### 30. Recuperación futura
- E2: aplicar `>` a un vector;
- E3: guardar el resultado;
- E5/E7: producir condiciones;
- M5: recuperar la lógica antes de `filter()`.

### 31. Riesgo de aprendizaje superficial
Memorizar que `>` “da TRUE o FALSE” sin comprender que está evaluando una afirmación. La lectura verbal de la comparación debe permanecer visible en esta primera pantalla.

### 32. Criterio de transferencia
Más adelante debe poder leer otra comparación simple como pregunta aunque cambien los valores y el contexto.

### 33. Notas de implementación futura
No presentar `TRUE/FALSE` antes de ejecutar las comparaciones. No introducir `vector lógico`, otros operadores ni selección lógica todavía.

---

## M3-E2 — Pregunta a todos los valores

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Extiende la comparación escalar de E1 a un vector completo. Su función es construir explícitamente la idea de que R hace la misma pregunta a cada valor y produce una respuesta correspondiente para cada uno.

### 3. Capacidad antes
Puede leer `35 > 30` como “¿35 es mayor que 30?” e interpretar `TRUE/FALSE`.

### 4. Capacidad después
Puede aplicar una comparación a un vector y comprender que existe una respuesta `TRUE/FALSE` por cada valor, en el mismo orden.

### 5. Prerrequisitos
- `c()`;
- vector;
- orden;
- `>`;
- significado de `TRUE/FALSE`.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** la misma comparación puede aplicarse a todos los valores de un vector.
- **Decisión nueva:** ninguna grande.

No usar todavía el término técnico “vectorización” como lenguaje para estudiante.

### 7. Recuperaciones
Recupera `c()`, vector, orden y `>`.

### 8. Contexto sustantivo
Cinco tiempos de viaje.

### 9. Dataset / objetos
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

Comparación:

```r
tiempos_viaje > 30
```

### 10. Texto para estudiante
**Situación.** `tiempos_viaje` contiene:

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

En E1 hicimos una pregunta a un solo valor.

Ahora podemos hacer **la misma pregunta a todos los valores**:

```r
tiempos_viaje > 30
```

Antes de ejecutar, piensa solo en dos casos:

- ¿25 es mayor que 30?
- ¿40 es mayor que 30?

Después ejecuta la comparación completa.

R responde una vez por cada valor:

```text
tiempo      pregunta        respuesta
25          25 > 30         FALSE
40          40 > 30         TRUE
35          35 > 30         TRUE
50          50 > 30         TRUE
30          30 > 30         FALSE
```

La misma idea puede verse alineada así:

```text
datos:       25     40     35     50     30
respuesta:   FALSE  TRUE   TRUE   TRUE   FALSE
```

La primera respuesta corresponde al primer dato, la segunda al segundo dato, y así sucesivamente.

### 11. Modelo mental
`VECTOR → MISMA PREGUNTA A CADA VALOR → UNA RESPUESTA POR DATO`

### 12. Código trabajado / ejemplo
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje > 30
```

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje > 30
```

### 14. Acción esperada
Predecir algunas respuestas, ejecutar la comparación del vector completo y relacionar cada `TRUE/FALSE` con el dato en la misma posición.

### 15. Solución canónica
```r
tiempos_viaje > 30
```

### 16. Resultado esperado
```text
FALSE TRUE TRUE TRUE FALSE
```

### 17. Criterio semántico de éxito
Comprobar que:

- existe `tiempos_viaje` con el orden correcto;
- la comparación se aplica al vector completo;
- se utiliza `> 30`;
- el resultado lógico es `FALSE TRUE TRUE TRUE FALSE`.

No aceptar como estrategia objetivo un vector lógico escrito manualmente.

### 18. Estrategias alternativas válidas
Se toleran diferencias de espacios. Para demostrar la capacidad, la comparación debe depender de `tiempos_viaje`.

### 19. Error esperado / misconception
- escribir manualmente `c(FALSE, TRUE, TRUE, TRUE, FALSE)`;
- comparar un solo elemento;
- no reconocer que hay cinco respuestas porque hay cinco datos;
- creer que las respuestas no conservan correspondencia posicional.

### 20. Feedback correcto
**Bien.** Hiciste la misma pregunta a los cinco valores. R produjo cinco respuestas en el mismo orden que los datos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe el vector lógico manualmente:

> Las respuestas coinciden, pero deben ser producidas por `tiempos_viaje > 30`. Así cambiarán automáticamente si cambian los tiempos.

### 22. Hint 1
No necesitas escribir cinco preguntas. Piensa si puedes hacer la misma comparación al objeto completo.

### 23. Hint 2
Coloca `> 30` después del nombre del vector.

### 24. Hint 3
```r
tiempos_viaje > 30
```

### 25. Predicción
Sí, parcialmente.

Primero preguntar por 25 y 40. Después, si resulta útil, anticipar las cinco respuestas.

### 26. Tipo de ejercicio
Worked/práctica guiada.

### 27. Andamiaje
Alto: comparación completa y representación alineada.

### 28. Carga cognitiva
**Baja-media.** No aparece sintaxis nueva; el desafío es comprender que una operación sobre un vector produce una respuesta correspondiente para cada elemento.

### 29. Fading
E2 todavía muestra el mecanismo. E3 retirará la comparación completa y pedirá reconstruirla dentro de una asignación.

### 30. Recuperación futura
E3–E7 y posteriormente M5.

### 31. Riesgo de aprendizaje superficial
Mirar solo la secuencia final de `TRUE/FALSE` sin comprender qué respuesta corresponde a qué dato. La tabla de correspondencia es obligatoria.

### 32. Criterio de transferencia
Debe poder aplicar posteriormente una comparación simple a otro vector y anticipar que habrá una respuesta por dato.

### 33. Notas de implementación futura
Mantener visibles los cinco datos y sus cinco respuestas. No introducir todavía selección lógica ni el término `vector lógico`.

---

## M3-E3 — Guarda las respuestas

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Reduce la carga cognitiva antes de la selección lógica. Convierte el resultado de la comparación en un objeto visible e inspeccionable que podrá utilizarse después dentro de `[]`.

### 3. Capacidad antes
Puede aplicar una comparación a un vector y comprender la correspondencia entre datos y respuestas.

### 4. Capacidad después
Puede guardar las respuestas de una comparación y reconocer ese conjunto de `TRUE/FALSE` como un vector lógico.

### 5. Prerrequisitos
- `<-`;
- objeto;
- comparación vectorizada;
- `TRUE/FALSE`;
- correspondencia posicional.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** el resultado lógico puede guardarse como un objeto y utilizarse después.
- **Vocabulario nuevo:** vector lógico.
- **Decisión nueva:** reconstruir la comparación dentro de una asignación.

### 7. Recuperaciones
Recupera `<-`, consulta de objetos y `tiempos_viaje > 30`.

### 8. Contexto sustantivo
Los mismos tiempos de viaje para mantener el foco en el nuevo paso conceptual.

### 9. Dataset / objetos
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

Objeto nuevo:

`supera_30`

### 10. Texto para estudiante
**Situación.** Ya sabemos que:

```r
tiempos_viaje > 30
```

produce una respuesta para cada tiempo.

Ahora queremos **guardar esas respuestas** para usarlas después.

Completa:

```r
supera_30 <- 
```

Después consulta `supera_30`.

El objeto debe contener:

```text
FALSE TRUE TRUE TRUE FALSE
```

`supera_30` contiene una respuesta `TRUE/FALSE` para cada valor de `tiempos_viaje`.

Como contiene varios valores lógicos, podemos llamarlo un **vector lógico**.

### 11. Modelo mental
`DATOS → PREGUNTA → RESPUESTAS → GUARDAR RESPUESTAS`

### 12. Código trabajado / ejemplo
Recordatorio mínimo:

```r
tiempos_viaje > 30
```

No mostrar la asignación completa antes de la tarea.

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- 

supera_30
```

### 14. Acción esperada
Completar la asignación con la comparación correcta y consultar el nuevo objeto.

### 15. Solución canónica
```r
supera_30 <- tiempos_viaje > 30
supera_30
```

### 16. Resultado esperado
```text
FALSE TRUE TRUE TRUE FALSE
```

### 17. Criterio semántico de éxito
Comprobar que:

- existe `supera_30`;
- contiene cinco valores lógicos;
- contiene exactamente `FALSE TRUE TRUE TRUE FALSE`;
- deriva de la comparación entre `tiempos_viaje` y 30;
- no fue construido escribiendo los valores lógicos manualmente.

### 18. Estrategias alternativas válidas
Se aceptan diferencias de espacios. El nombre `supera_30` forma parte de la tarea para mantener estable el puente hacia E4.

### 19. Error esperado / misconception
- `supera_30 <- c(FALSE, TRUE, TRUE, TRUE, FALSE)`;
- guardar un número o texto en lugar de la comparación;
- olvidar que el objeto debe tener una respuesta por dato.

### 20. Feedback correcto
**Bien.** Guardaste las respuestas de la pregunta. `supera_30` contiene un `TRUE/FALSE` por cada valor de `tiempos_viaje`. Ese conjunto es un vector lógico.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe los valores lógicos manualmente:

> Las respuestas son correctas, pero quedaron hardcodeadas. Queremos que `supera_30` se construya a partir de `tiempos_viaje > 30` para que cambie si cambian los datos.

### 22. Hint 1
Piensa qué expresión produjo las cinco respuestas en E2.

### 23. Hint 2
A la derecha de `<-` debe ir la comparación completa aplicada al vector.

### 24. Hint 3
```r
supera_30 <- tiempos_viaje > 30
```

### 25. Predicción
No necesaria como paso separado.

### 26. Tipo de ejercicio
Completion problem.

### 27. Andamiaje
Alto: nombre del objeto, datos y estructura de asignación ya están presentes.

### 28. Carga cognitiva
**Baja-media.** La asignación es conocida; el esfuerzo está en comprender que el resultado lógico puede guardarse y convertirse en un objeto reutilizable.

### 29. Fading
Retira el código completo de E2 y exige reconstruir la comparación dentro de una asignación.

### 30. Recuperación futura
E4 utilizará `supera_30` dentro de `[]`; E7 volverá a exigir construir una condición.

### 31. Riesgo de aprendizaje superficial
Creer que “vector lógico” es una etiqueta para memorizar sin comprender que existe una respuesta por cada dato. Mantener la correspondencia conceptual visible.

### 32. Criterio de transferencia
Debe poder guardar más adelante el resultado de otra comparación en un objeto con otro nombre.

### 33. Notas de implementación futura
No introducir clases, `typeof()`, “Boolean” ni selección lógica en el texto previo a la tarea. El término “vector lógico” aparece después de observar el objeto.

---

## M3-E4 — TRUE conserva

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce el mecanismo central de selección lógica: usar las respuestas `TRUE/FALSE` dentro de `[]` para decidir qué valores conservar.

### 3. Capacidad antes
Puede construir y guardar un vector lógico correspondiente a los datos.

### 4. Capacidad después
Puede interpretar y ejecutar una selección `x[condicion]`, comprendiendo por qué permanecen los valores correspondientes a `TRUE`.

### 5. Prerrequisitos
- vector;
- orden;
- `[]`;
- `TRUE/FALSE`;
- vector lógico;
- correspondencia posicional.

### 6. Gran novedad
- **Sintaxis nueva:** utilizar una condición lógica dentro de `[]`.
- **Concepto nuevo:** `TRUE` conserva el dato de la misma posición y `FALSE` lo deja fuera.
- **Decisión nueva:** ninguna importante; es un worked example.

### 7. Recuperaciones
Recupera `[]` desde M2 y `supera_30` desde E3.

### 8. Contexto sustantivo
Tiempos de viaje mayores que 30.

### 9. Dataset / objetos
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
supera_30 <- tiempos_viaje > 30
```

Representación central:

```text
dato          25      40      35      50      30
supera_30     FALSE   TRUE    TRUE    TRUE    FALSE
                       ↓       ↓       ↓
resultado             40      35      50
```

### 10. Texto para estudiante
**Situación.** Tenemos los datos:

```text
dato          25      40      35      50      30
supera_30     FALSE   TRUE    TRUE    TRUE    FALSE
```

Cada respuesta corresponde al dato en la misma posición.

Ahora observa:

```r
tiempos_viaje[supera_30]
```

Cuando usamos un vector de `TRUE/FALSE` dentro de los corchetes:

- `TRUE` conserva el valor de esa posición;
- `FALSE` lo deja fuera.

Antes de ejecutar, predice:

> ¿qué valores deberían quedar?

La idea puede verse así:

```text
dato          25      40      35      50      30
supera_30     FALSE   TRUE    TRUE    TRUE    FALSE
                       ↓       ↓       ↓
resultado             40      35      50
```

### 11. Modelo mental
`DATOS + VECTOR LÓGICO → TRUE CONSERVA / FALSE DEJA FUERA → SELECCIÓN`

### 12. Código trabajado / ejemplo
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

tiempos_viaje[supera_30]
```

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

tiempos_viaje[supera_30]
```

### 14. Acción esperada
Predecir los valores que permanecerán, ejecutar la selección y explicar por qué esos valores corresponden a posiciones con `TRUE`.

### 15. Solución canónica
```r
tiempos_viaje[supera_30]
```

### 16. Resultado esperado
```text
40 35 50
```

### 17. Criterio semántico de éxito
Comprobar que:

- `supera_30` deriva de `tiempos_viaje > 30`;
- la selección se realiza desde `tiempos_viaje`;
- la selección utiliza el vector lógico;
- el resultado es `40 35 50`;
- no se seleccionan posiciones numéricas memorizadas;
- no se reconstruyen los valores manualmente.

**Perturbation test recomendado:** modificar los valores de `tiempos_viaje` y verificar que la condición y la selección se actualizan al reejecutar.

### 18. Estrategias alternativas válidas
En esta pantalla el objetivo es hacer visible la forma descompuesta. Se considera válida una estrategia lógicamente equivalente que dependa de una condición, pero la implementación didáctica debe priorizar `tiempos_viaje[supera_30]`.

### 19. Error esperado / misconception
- `c(40, 35, 50)`;
- `tiempos_viaje[c(2, 3, 4)]`;
- usar `TRUE/FALSE` sin mantener correspondencia con los datos;
- creer que `TRUE` significa “valor verdadero” sustantivamente y no “la condición se cumple”.

### 20. Feedback correcto
**Bien.** `supera_30` marca con `TRUE` las posiciones que cumplen la pregunta. Al usarlo dentro de `[]`, permanecen los valores correspondientes.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa posiciones:

> Obtienes los mismos valores, pero elegiste posiciones conocidas. En M3 queremos seleccionar porque los valores cumplen una pregunta, aunque cambien de lugar.

Si escribe `c(40, 35, 50)`:

> El resultado coincide, pero los valores fueron reconstruidos manualmente. La selección debe depender de la condición.

### 22. Hint 1
Observa qué posiciones de `supera_30` contienen `TRUE`.

### 23. Hint 2
El vector lógico puede colocarse dentro de los corchetes del vector de datos.

### 24. Hint 3
```r
tiempos_viaje[supera_30]
```

### 25. Predicción
Sí.

Preguntar:

> Si solo permanecen las posiciones con `TRUE`, ¿qué valores deberían quedar?

### 26. Tipo de ejercicio
Worked example conceptual.

### 27. Andamiaje
Muy alto para la selección lógica: condición ya construida, representación alineada y código completo.

### 28. Carga cognitiva
**Media.** Están activos vector, correspondencia, `TRUE/FALSE`, condición y `[]`. E1–E3 reducen la carga al haber construido cada componente previamente.

### 29. Fading
E4 muestra la forma descompuesta completa. E5 exigirá construir una nueva selección y permitirá integrar condición y corchetes en una sola expresión.

### 30. Recuperación futura
E5, E7 y M5.

### 31. Riesgo de aprendizaje superficial
Memorizar “TRUE conserva” sin comprender la alineación posicional. La representación dato/respuesta/resultado es obligatoria.

### 32. Criterio de transferencia
Debe poder seleccionar posteriormente desde otro vector utilizando otro vector lógico, sin depender de posiciones numéricas conocidas.

### 33. Notas de implementación futura
No usar la palabra “máscara” en lenguaje visible. El grader debe diferenciar selección lógica de selección por posiciones aunque ambas produzcan el mismo output en los datos originales.

---

## M3-E5 — Selecciona tú

### 1. Rol pedagógico
PRÁCTICA / INTEGRACIÓN.

### 2. Por qué existe
Retira el worked example de E4 y exige construir una selección lógica en un contexto numérico nuevo. Introduce la forma directa únicamente como compactación de una estrategia ya comprendida.

### 3. Capacidad antes
Puede usar una condición guardada dentro de `[]`.

### 4. Capacidad después
Puede construir una condición simple y utilizarla para seleccionar valores, ya sea en dos pasos o mediante la forma compacta.

### 5. Prerrequisitos
- vector;
- `>`;
- `TRUE/FALSE`;
- condición;
- `[]`;
- selección lógica.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna esencial.
- **Forma nueva:** `x[x > valor]`, presentada como compactación.
- **Decisión nueva:** formular la condición correcta y seleccionar por ella.

### 7. Recuperaciones
Recupera `>`, `[]`, correspondencia y selección lógica.

### 8. Contexto sustantivo
Horas de estudio de cinco estudiantes.

### 9. Dataset / objetos
```r
horas_estudio <- c(2, 5, 3, 6, 4)
```

Pregunta:

> encuentra las horas de estudio que superan 4.

### 10. Texto para estudiante
**Situación.** Cinco estudiantes informaron estas horas de estudio:

```r
horas_estudio <- c(2, 5, 3, 6, 4)
```

**Tarea.** Encuentra los valores que **superan 4**.

Puedes resolverlo en dos pasos, como en E4:

```r
supera_4 <- horas_estudio > 4
horas_estudio[supera_4]
```

También podemos escribir la misma idea directamente:

```r
horas_estudio[horas_estudio > 4]
```

La expresión puede leerse así:

```text
horas_estudio [ horas_estudio > 4 ]
      │                 │
      │                 └─ pregunta hecha a los valores
      └─────────────────── objeto del que selecciono
```

La segunda forma no es una regla nueva: es la versión compacta de los dos pasos anteriores.

Ahora resuelve la tarea.

### 11. Modelo mental
`PREGUNTA → CONDICIÓN → SELECCIÓN`

Forma descompuesta:

`condicion <- x > valor → x[condicion]`

Forma compacta:

`x[x > valor]`

### 12. Código trabajado / ejemplo
Recordatorio de E4:

```r
supera_4 <- horas_estudio > 4
horas_estudio[supera_4]
```

Y equivalencia compacta:

```r
horas_estudio[horas_estudio > 4]
```

### 13. Starter code
```r
horas_estudio <- c(2, 5, 3, 6, 4)

# selecciona los valores que superan 4
```

### 14. Acción esperada
Construir una selección basada en la condición “mayor que 4”.

### 15. Solución canónica
Forma compacta:

```r
horas_estudio[horas_estudio > 4]
```

Forma descompuesta también válida:

```r
supera_4 <- horas_estudio > 4
horas_estudio[supera_4]
```

### 16. Resultado esperado
```text
5 6
```

### 17. Criterio semántico de éxito
Comprobar que:

- existe `horas_estudio` con valores y orden correctos;
- la estrategia utiliza la condición `> 4`;
- la selección depende de esa condición;
- el resultado es `5 6`;
- no utiliza posiciones manuales;
- no reconstruye `c(5, 6)`.

**Perturbation test muy recomendado:** cambiar los valores fuente, manteniendo la pregunta “> 4”, y verificar que la selección siga respondiendo correctamente.

### 18. Estrategias alternativas válidas
Son válidas:

```r
horas_estudio[horas_estudio > 4]
```

y:

```r
supera_4 <- horas_estudio > 4
horas_estudio[supera_4]
```

No exigir una única cadena literal.

### 19. Error esperado / misconception
- `horas_estudio[c(2, 4)]`;
- `c(5, 6)`;
- `4 > horas_estudio`;
- utilizar la condición correcta pero no usarla para seleccionar;
- no comprender por qué `horas_estudio` aparece dos veces en la forma compacta.

### 20. Feedback correcto
**Bien.** Ya no necesitaste saber dónde estaban los valores: formulaste una condición y seleccionaste los que la cumplían.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa posiciones:

> El resultado coincide con estos datos, pero elegiste posiciones. Si los valores cambian de lugar, tu código dejaría de responder “¿cuáles superan 4?”.

Si escribe `c(5, 6)`:

> Los valores son correctos, pero están hardcodeados. La selección debe depender de `horas_estudio` y de la condición.

Si escribe `4 > horas_estudio`:

> Esa expresión pregunta si 4 es mayor que cada hora. La pregunta necesaria es si cada hora es mayor que 4.

### 22. Hint 1
¿Qué pregunta necesitas hacerle a cada valor de `horas_estudio`?

### 23. Hint 2
La comparación “mayor que 4” puede utilizarse dentro de los corchetes.

### 24. Hint 3
```r
horas_estudio[horas_estudio > 4]
```

### 25. Predicción
No se añade como fase separada. La propia construcción de la condición exige anticipar qué debería conservarse.

### 26. Tipo de ejercicio
Producción / integración.

### 27. Andamiaje
Medio: datos y pregunta están dados; se muestra la equivalencia conceptual, pero el starter no contiene la solución.

### 28. Carga cognitiva
**Media.** No hay sintaxis nuclear nueva, pero debe coordinar comparación y selección. La forma descompuesta permanece disponible para reducir carga si la forma compacta resulta difícil.

### 29. Fading
E5 retira la condición ya construida de E4 y exige producir una solución. El apoyo se concentra en explicar la equivalencia entre dos pasos y forma compacta.

### 30. Recuperación futura
E7 y posteriormente M5.

### 31. Riesgo de aprendizaje superficial
Copiar `x[x > valor]` como plantilla sin comprender las dos funciones de `x`. La representación anotada de la expresión es obligatoria.

### 32. Criterio de transferencia
Ante una pregunta cuantitativa nueva debe decidir utilizar una condición y no posiciones memorizadas.

### 33. Notas de implementación futura
El grader debe aceptar forma directa y descompuesta. No premiar compacidad sobre comprensión. Usar perturbation test para discriminar condición genuina de selección por posiciones.

---

## M3-E6 — También podemos preguntar por texto

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Generaliza el modelo “pregunta → TRUE/FALSE” desde cantidades hacia texto. Introduce `==` sin cambiar la lógica conceptual construida en E1–E5.

### 3. Capacidad antes
Puede construir condiciones numéricas simples y utilizarlas para seleccionar valores.

### 4. Capacidad después
Puede preguntar si cada texto es igual a un valor determinado, guardar las respuestas y reutilizarlas en una selección.

### 5. Prerrequisitos
- texto entre comillas;
- vector;
- `TRUE/FALSE`;
- condición;
- selección lógica;
- `<-`.

### 6. Gran novedad
- **Sintaxis nueva:** `==`.
- **Concepto nuevo:** igualdad como otra clase de pregunta.
- **Decisión nueva:** mínima; se reutiliza el mismo modelo lógico.

### 7. Recuperaciones
Recupera texto de M1, `c()` de M2 y vector lógico/selección de M3.

### 8. Contexto sustantivo
Cuatro respuestas sobre carrera.

No introducir todavía el término formal “variable categórica”.

### 9. Dataset / objetos
```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)
```

Objeto de condición:

`es_sociologia`

### 10. Texto para estudiante
**Situación.** Tenemos cuatro respuestas sobre carrera:

```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)
```

Hasta ahora preguntamos cosas como:

> ¿cada valor es mayor que 4?

También podemos preguntar:

> ¿cada respuesta es exactamente `"Sociología"`?

En R usamos:

```r
carreras == "Sociología"
```

`==` significa:

> pregunta si es igual.

Antes de continuar, observa la diferencia:

```text
<-   guardar
==   preguntar si es igual
```

Por ejemplo:

```r
carrera <- "Sociología"
```

guarda un texto.

Mientras:

```r
carrera == "Sociología"
```

pregunta si ese texto es igual a `"Sociología"`.

Ahora crea `es_sociologia` con la pregunta aplicada al vector `carreras`, consulta el objeto y después usa esas respuestas para recuperar las coincidencias.

### 11. Modelo mental
`PREGUNTA DE IGUALDAD → TRUE/FALSE → CONDICIÓN → SELECCIÓN`

### 12. Código trabajado / ejemplo
```r
carreras == "Sociología"
```

Contraste:

```r
carrera <- "Sociología"
carrera == "Sociología"
```

### 13. Starter code
```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)

es_sociologia <- 

es_sociologia

# usa es_sociologia para seleccionar desde carreras
```

### 14. Acción esperada
Construir la comparación de igualdad, guardarla y reutilizarla dentro de `[]`.

### 15. Solución canónica
```r
es_sociologia <- carreras == "Sociología"
es_sociologia

carreras[es_sociologia]
```

### 16. Resultado esperado
Para `es_sociologia`:

```text
TRUE FALSE TRUE FALSE
```

Para la selección:

```text
"Sociología" "Sociología"
```

### 17. Criterio semántico de éxito
Comprobar que:

- existe `carreras` con cuatro textos en el orden correcto;
- existe `es_sociologia`;
- `es_sociologia` depende de `carreras == "Sociología"`;
- contiene `TRUE FALSE TRUE FALSE`;
- la selección depende del vector lógico;
- no utiliza posiciones manuales `c(1, 3)`;
- no hardcodea los textos seleccionados.

### 18. Estrategias alternativas válidas
Se toleran comillas simples como equivalentes semánticos si la política general del curso lo permite internamente, aunque el material visible mantenga comillas dobles. La comparación debe utilizar `==`.

### 19. Error esperado / misconception
- usar `<-` cuando quiere comparar;
- escribir un solo `=`;
- olvidar comillas;
- hardcodear `TRUE/FALSE`;
- seleccionar por posiciones `c(1, 3)`.

### 20. Feedback correcto
**Bien.** La lógica es la misma que con `>`: `==` hace una pregunta y R produce una respuesta `TRUE/FALSE` para cada texto. Después reutilizaste esas respuestas para seleccionar.

### 21. Feedback resultado correcto / estrategia incorrecta
Si confunde `<-` con `==`:

> `<-` guarda información. `==` pregunta si dos valores son iguales. Aquí necesitamos hacer una pregunta.

Si omite comillas:

> `"Sociología"` es texto. Para compararlo debes escribirlo entre comillas.

Si usa posiciones:

> Esas posiciones coinciden en estos datos, pero la tarea es seleccionar por igualdad, no porque ya sabes dónde están las respuestas.

### 22. Hint 1
La pregunta es: “¿cada respuesta es igual a Sociología?”.

### 23. Hint 2
Para preguntar si dos valores son iguales usamos `==`; el texto debe ir entre comillas.

### 24. Hint 3
```r
es_sociologia <- carreras == "Sociología"
carreras[es_sociologia]
```

### 25. Predicción
Sí, breve.

Antes de ejecutar la comparación:

> ¿qué posiciones esperas que produzcan `TRUE`?

Primera y tercera.

### 26. Tipo de ejercicio
Worked/completion.

### 27. Andamiaje
Alto: se presenta el nuevo operador y el contraste con `<-`; el estudiante completa la condición y recupera una selección ya conocida.

### 28. Carga cognitiva
**Baja-media.** `==` es nuevo, pero texto, vectores, `TRUE/FALSE` y selección lógica ya están disponibles.

### 29. Fading
Se introduce un operador nuevo sobre una estructura mental ya consolidada. El checkpoint siguiente no exigirá dominio autónomo de `==`.

### 30. Recuperación futura
`==` se practicará en M5 y volverá posteriormente en tareas categóricas.

### 31. Riesgo de aprendizaje superficial
Memorizar que `==` “va con texto” sin comprender que pregunta por igualdad. El contraste con `<-` y la lectura verbal deben prevenirlo.

### 32. Criterio de transferencia
Más adelante debe poder reconocer y utilizar `==` en nuevas preguntas de igualdad sin confundirlo con asignación.

### 33. Notas de implementación futura
No introducir `=`, `!=`, `%in%` ni “variable categórica”. El grader debe verificar estrategia y no solo el vector lógico final.

---

## M3-E7 — Checkpoint A: encuentra lo que buscas

### 1. Rol pedagógico
TRANSFERENCIA / CHECKPOINT.

### 2. Por qué existe
Es el primer diagnóstico integrado de los fundamentos necesarios para seguir avanzando. Comprueba si el estudiante puede crear datos, formular una pregunta, producir respuestas lógicas y utilizar esas respuestas para seleccionar sin recibir sintaxis nueva.

### 3. Capacidad antes
Ha completado M1–M3 y puede crear vectores, construir condiciones y realizar selección lógica con apoyo decreciente.

### 4. Capacidad después
Demuestra que puede reconstruir de forma integrada la cadena `datos → vector → condición → selección` en un contexto nuevo.

### 5. Prerrequisitos
- `<-`;
- `c()`;
- vector y orden;
- `>`;
- `TRUE/FALSE`;
- vector lógico;
- `[]`;
- selección lógica.

`==` no es requisito central del checkpoint.

### 6. Gran novedad
Ninguna.

- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** integrar capacidades conocidas sin que la consigna nombre las herramientas.

### 7. Recuperaciones
Recupera fundamentos seleccionados de M1–M3:

- asignación;
- creación de vector;
- comparación;
- condición;
- selección lógica.

### 8. Contexto sustantivo
Horas semanales dedicadas a tareas de cuidado.

### 9. Dataset / objetos
Valores, en este orden:

`6, 12, 8, 15, 10`

Objetos requeridos:

- `horas_cuidado`;
- `supera_10`;
- `horas_seleccionadas`.

### 10. Texto para estudiante
# Checkpoint A — Fundamentos

Cinco personas informaron dedicar:

**6, 12, 8, 15 y 10 horas semanales** a tareas de cuidado, en ese orden.

Construye un pequeño script que:

1. guarde los cinco valores juntos en `horas_cuidado`;
2. guarde en `supera_10` una pregunta que identifique qué valores son mayores que 10;
3. use esa condición para guardar en `horas_seleccionadas` únicamente las horas que cumplen la pregunta.

Intenta resolver primero sin abrir las pistas.

### 11. Modelo mental
`DATOS → VECTOR → PREGUNTA → VECTOR LÓGICO → SELECCIÓN`

### 12. Código trabajado / ejemplo
No se entrega código trabajado. El checkpoint no introduce contenido nuevo.

### 13. Starter code
```r
# guarda las horas en horas_cuidado


# guarda una condición que identifique valores mayores que 10


# selecciona las horas que cumplen esa condición
```

### 14. Acción esperada
Crear los tres objetos requeridos mediante una cadena reproducible.

### 15. Solución canónica
```r
horas_cuidado <- c(6, 12, 8, 15, 10)
supera_10 <- horas_cuidado > 10
horas_seleccionadas <- horas_cuidado[supera_10]
```

### 16. Resultado esperado
`horas_cuidado`:

```text
6 12 8 15 10
```

`supera_10`:

```text
FALSE TRUE FALSE TRUE FALSE
```

`horas_seleccionadas`:

```text
12 15
```

### 17. Criterio semántico de éxito
Comprobar por componentes:

**Construcción**
- `horas_cuidado` existe;
- contiene cinco números;
- conserva el orden;
- fue construido como vector.

**Condición**
- `supera_10` existe;
- deriva de `horas_cuidado > 10`;
- contiene `FALSE TRUE FALSE TRUE FALSE`.

**Selección**
- `horas_seleccionadas` existe;
- depende de una condición lógica;
- contiene `12 15`;
- no usa posiciones manuales;
- no hardcodea los resultados.

**Perturbation test altamente recomendado:** modificar los valores fuente y comprobar que condición y selección se actualizan al reejecutar.

### 18. Estrategias alternativas válidas
El checkpoint exige explícitamente crear `supera_10` porque necesita diagnosticar si el estudiante puede producir e interpretar un vector lógico. Dentro de esa restricción se toleran diferencias de espacios y orden de líneas que no rompan las dependencias.

### 19. Error esperado / misconception
- no poder construir el vector;
- comparación invertida;
- hardcodear el vector lógico;
- hardcodear `12, 15`;
- seleccionar `c(2, 4)` en vez de por condición;
- construir correctamente `supera_10` pero no saber usarlo dentro de `[]`.

### 20. Feedback correcto
**Checkpoint completado.** Creaste los datos, formulaste una pregunta, guardaste sus respuestas y utilizaste esas respuestas para seleccionar. Ya puedes encontrar valores por lo que cumplen sin conocer previamente sus posiciones.

### 21. Feedback resultado correcto / estrategia incorrecta
**Si falla la construcción del vector**

> Primero necesitas guardar las cinco observaciones juntas. Recupera cómo construías vectores con `c()`.

**Si la comparación está invertida**

> `10 > horas_cuidado` pregunta si 10 es mayor que cada valor. Necesitamos preguntar si cada hora es mayor que 10.

**Si el vector lógico está hardcodeado**

> Las respuestas pueden coincidir, pero `supera_10` debe ser producido por una comparación para que cambie si cambian los datos.

**Si usa posiciones**

> `c(2, 4)` funciona con estos valores, pero depende de saber dónde están. El checkpoint busca comprobar selección por condición.

**Si hardcodea `12, 15`**

> El resultado coincide, pero debe salir de `horas_cuidado` mediante la condición.

**Si construye la condición pero no selecciona**

> La pregunta ya está correcta. Ahora usa `supera_10` dentro de los corchetes de `horas_cuidado`.

### 22. Hint 1
Divide el problema en tres etapas: guardar los datos, hacer la pregunta y usar las respuestas.

### 23. Hint 2
La condición central pregunta si cada valor de `horas_cuidado` es mayor que 10. Guarda esa comparación antes de seleccionar.

### 24. Hint 3
```r
horas_cuidado <- c(6, 12, 8, 15, 10)
supera_10 <- horas_cuidado > 10
horas_seleccionadas <- horas_cuidado[supera_10]
```

### 25. Predicción
No se añade una predicción separada. La tarea ya exige construir e interpretar la condición.

### 26. Tipo de ejercicio
Checkpoint de transferencia cercana.

### 27. Andamiaje
Bajo-medio: comentarios estructurales y nombres de objetos, sin sintaxis resuelta. Las pistas comienzan cerradas.

### 28. Carga cognitiva
**Media.** Integra varias habilidades conocidas, pero no añade sintaxis ni conceptos nuevos.

### 29. Fading
Es el punto final del fading de M3. El estudiante recibe contexto y productos esperados, pero debe reconstruir la ruta.

### 30. Recuperación futura
M5 recuperará condiciones y selección como fundamento conceptual del filtrado. `>` continuará reapareciendo; `==` se practicará después.

### 31. Riesgo de aprendizaje superficial
La mayor amenaza es sustituir la lógica por posiciones conocidas o resultados literales. El grader y el perturbation test deben proteger contra ambas estrategias.

### 32. Criterio de transferencia
La evidencia de dominio es poder resolver una tarea nueva de selección por condición sin que la consigna indique la sintaxis y sin depender de posiciones memorizadas.

### 33. Notas de implementación futura
El checkpoint no debe penalizar pedir pistas ni introducir contenido nuevo. Registrar el nivel de ayuda puede ser útil para diagnóstico, pero el criterio de aprobación depende del estado y estrategia finales. No exigir `==` como habilidad central del checkpoint.

---

# Cierre conceptual de M3 y puente a M4

Después de completar el checkpoint, mostrar:

> Hasta ahora trabajamos con **una característica a la vez**:
> tiempos de viaje, horas de estudio o respuestas de carrera.
>
> Podemos guardar sus valores y hacer preguntas para encontrar los que nos interesan.
>
> Pero una encuesta no suele tener una sola característica.
>
> ¿Cómo organizamos varias características de las mismas personas?

La transición termina ahí.

M3 NO debe introducir todavía:

- fila;
- columna;
- caso;
- variable;
- data frame;
- `$`.

# Retención esperada después de una semana

## Reconocimiento
El estudiante debería reconocer:

```r
>
```

como una comparación de “mayor que”,

```text
TRUE / FALSE
```

como respuestas producidas por una condición y:

```r
x[condicion]
```

como selección lógica.

## Producción
Con poca ayuda debería poder producir:

```r
x > valor
```

y, preferentemente:

```r
condicion <- x > valor
x[condicion]
```

## Elección
Ante una consigna como:

> encuentra los valores mayores que 30

debería decidir usar una condición y no posiciones manuales.

## Habilidades todavía en consolidación
Pueden requerir recuperación posterior:

```r
x[x > valor]
```

y:

```r
==
```

# Checkpoint A — habilidades diagnosticadas

| Habilidad | Nivel esperado en M3-E7 |
|---|---|
| `<-` | producir |
| `c()` | producir |
| vector y orden | aplicar |
| `>` | producir |
| `TRUE/FALSE` | interpretar |
| vector lógico | construir |
| `[]` con condición | producir |
| selección por condición | decidir |
| `==` | no se exige como núcleo del checkpoint |

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 3
- PRÁCTICA: 2
- PRÁCTICA / INTEGRACIÓN: 1
- TRANSFERENCIA / CHECKPOINT: 1

## Porcentaje local de pantallas con novedad
3 de 7 ejercicios: aproximadamente 42,9 %.

Este valor no obliga a cambiar la arquitectura: el criterio de balance de novedad se evalúa en la progresión global del curso, y las tres pantallas de novedad de M3 introducen unidades conceptuales diferentes y necesarias (`>` + significado lógico, selección lógica, `==`).

## Habilidades relativamente consolidadas
- `>` como pregunta;
- significado de `TRUE/FALSE`;
- comparación aplicada a un vector;
- correspondencia dato ↔ respuesta;
- construcción de una condición;
- uso de `x[condicion]`;
- selección por condición en vez de posiciones.

## Habilidades todavía en consolidación
- forma compacta `x[x > valor]`;
- `==`;
- selección por igualdad textual.

## Recuperación futura
M5 debe recuperar la lógica de condición y selección como fundamento del filtrado. La trayectoria maestra mantiene `>` y `[]` en producción y recuperación posteriores; `==` se practica más adelante.

## Riesgos de sobrecarga controlados
- `TRUE/FALSE` se introduce antes de pedir vector lógico;
- vector lógico se construye antes de selección;
- forma descompuesta antecede a la compacta;
- `==` aparece después de consolidar el modelo de pregunta;
- el checkpoint no introduce sintaxis nueva.

## Checkpoint
Sí: M3-E7.

No incluye novedad sintáctica y diagnostica la cadena `datos → vector → condición → selección`.

# Declaración de lock

M3 queda pedagógicamente cerrado con 7 ejercicios.

- **Sintaxis introducida:** `>`, `==`, selección lógica `x[condicion]`.
- **Forma en consolidación:** `x[x > valor]`.
- **Habilidades nucleares:** comparación como pregunta, `TRUE/FALSE`, correspondencia dato-respuesta, vector lógico y selección por condición.
- **Habilidad en consolidación:** `==`.
- **Checkpoint:** M3-E7 diagnostica construcción de vector, condición y selección lógica sin hardcoding.
- **Recuperación futura:** M5 y módulos posteriores.
- **Puente a M4:** una característica a la vez → necesidad de organizar varias características de las mismas personas.

# M3 PEDAGOGICALLY LOCKED
