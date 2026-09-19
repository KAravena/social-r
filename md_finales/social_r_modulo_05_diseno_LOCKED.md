# Social R — Módulo 5
## Seleccionar y filtrar datos

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede recuperar una variable de una base mediante `$`, comprenderla como vector y construir condiciones sobre vectores.

### Capacidad después
Puede conservar casos mediante condiciones, seleccionar variables por nombre y encadenar ambas operaciones con `|>` para preparar un subconjunto reproducible.

### Pregunta central
¿Cómo preparo solo los casos y variables que necesito para una pregunta?

### Modelo mental
`VARIABLE → PREGUNTA / CONDICIÓN → TRUE / FALSE POR CASO → TRUE CONSERVA EL CASO COMPLETO → FILTER = QUÉ CASOS NECESITO → SELECT = QUÉ VARIABLES NECESITO → PIPE = PASAR EL RESULTADO A LA SIGUIENTE ACCIÓN → DATOS PREPARADOS`

### Habilidades nucleares
Al terminar M5, el estudiante debe poder:

- aplicar una condición a una variable de una base;
- comprender que una condición sobre una columna produce una respuesta por caso;
- comprender que `TRUE` puede conservar una fila/caso completo;
- distinguir casos de variables al preparar datos;
- usar `filter()` para conservar casos que cumplen una condición;
- practicar `==` con texto dentro de una tarea de filtrado;
- usar el pipe nativo `|>`;
- comprender que cada etapa de un pipeline recibe el resultado de la anterior;
- comprender que ejecutar un pipeline no modifica automáticamente la base original;
- usar `select()` para conservar variables por nombre;
- distinguir semánticamente `filter()` de `select()`;
- encadenar `filter()` y `select()` mediante `|>`;
- preparar un subconjunto reproducible;
- guardar un resultado preparado en un nuevo objeto cuando la tarea lo requiere.

### Habilidad solo puente
La expresión:

```r
datos[condicion, ]
```

se utiliza únicamente para hacer visible el mecanismo por el cual un vector lógico puede conservar filas completas de una base.

No se considera habilidad terminal de M5. No se exige producción autónoma, retención después de una semana ni uso en Checkpoint B.

### Habilidades recuperadas
M5 recupera:

- `$` desde M4;
- `>` desde M3;
- `==` desde M3;
- `TRUE/FALSE`;
- vectores lógicos;
- selección por condición;
- fila = caso;
- columna = variable;
- `<-` en el checkpoint;
- nombres de variables y texto entre comillas.

### Sintaxis nueva
- `filter()`;
- `|>`;
- `select()`.

### Sintaxis funcional de puente
- `datos[condicion, ]`, solo como worked example conceptual.

### Sintaxis que NO se introduce
No se introducen:

- `%>%`;
- `library(dplyr)` como contenido del estudiante;
- `dplyr::filter()`;
- `dplyr::select()`;
- `mutate()`;
- `group_by()`;
- `summarise()`;
- `arrange()`;
- `rename()`;
- pipelines largos;
- tidy evaluation;
- NSE;
- data masking;
- quosures;
- missing data.

### Política dplyr
Desde M5 la plataforma deja disponibles `filter()` y `select()`.

Puede mostrarse una nota breve:

> Desde este módulo están disponibles dos funciones de un paquete de R llamado `dplyr`: `filter()` y `select()`.

No se pide ejecutar `library(dplyr)` y no se evalúa conocimiento sobre paquetes.

### Dataset principal
M5 conserva exactamente la vista pedagógica locked de M4:

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

Objeto:

`encuesta_social_demo`

Condiciones canónicas:

- E1–E3: `edad > 21` → casos 2, 5, 6 y 8.
- E4–E5: `carrera == "Sociología"` → casos 1, 4 y 8.
- E7: `trabaja == "Sí"` → casos 2, 5, 6 y 8.

### Dataset de transferencia
M5-E8 utiliza:

```text
encuesta_jovenes

id   edad   estudia   comuna    transporte
1    18     Sí        Norte     Bus
2    20     No        Centro    Metro
3    19     Sí        Sur       Bicicleta
4    22     Sí        Centro    Bus
5    21     No        Norte     Metro
6    23     Sí        Sur       Metro
```

### Estrategia de scaffolding
1. Recuperar `base$variable > valor`.
2. Hacer visible que cada respuesta lógica corresponde a un caso.
3. Mostrar worked example donde ese vector lógico conserva filas completas.
4. Reexpresar la misma selección con `filter()`.
5. Pedir producción de otro filtro.
6. Introducir `|>` con una sola operación conocida.
7. Introducir `select()` sin pipe.
8. Integrar `filter() |> select()`.
9. Transferir a una base nueva sin nombrar las funciones.

### Estrategia de fading
`RECUPERACIÓN SEMIAUTÓNOMA → WORKED BRIDGE → WORKED FILTER → PRODUCCIÓN FILTER → WORKED PIPE → COMPLETION SELECT → INTEGRACIÓN GUIADA → CHECKPOINT AUTÓNOMO`

### Riesgos cognitivos
- creer que una condición selecciona valores pero no casos completos;
- convertir `[condicion, ]` en una sintaxis nueva que debe memorizarse;
- interpretar mal la coma en indexación bidimensional;
- confundir `filter()` con “buscar valores” en vez de conservar casos;
- no comprender por qué dentro de `filter()` se nombra `edad` sin `$`;
- usar `=` en lugar de `==`;
- olvidar comillas en texto;
- filtrar por posiciones memorizadas;
- usar `%>%`;
- tratar `|>` como decoración;
- creer que un pipeline modifica permanentemente la base original;
- confundir `filter()` y `select()`;
- seleccionar columnas por posiciones cuando la habilidad objetivo es nombre;
- resolver el checkpoint por hardcoding;
- producir un resultado correcto sin demostrar la estrategia curricular pedida.

### Número de ejercicios
8

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M5-E1 | Vuelve a hacer una pregunta | RECUPERACIÓN | ninguna | `$`, `>`, TRUE/FALSE | baja-media |
| M5-E2 | De TRUE/FALSE a personas completas | NOVEDAD / PUENTE CONCEPTUAL | TRUE/FALSE puede conservar casos completos | `[]`, condición, fila/caso | media |
| M5-E3 | Una forma más legible de filtrar | NOVEDAD | `filter()` | mecanismo de E2 | media |
| M5-E4 | Filtra otro grupo | PRÁCTICA | ninguna | `$`, `==`, texto, `filter()` | media |
| M5-E5 | Los datos pasan a la siguiente acción | NOVEDAD | `|>` | `filter()` | media |
| M5-E6 | Qué variables necesito | NOVEDAD | `select()` | columna/variable | media |
| M5-E7 | Filtra y después selecciona | INTEGRACIÓN | ninguna | `filter()`, `|>`, `select()`, `==` | media |
| M5-E8 | Checkpoint B: prepara los datos | TRANSFERENCIA / CHECKPOINT | ninguna | preparación completa | media |

---

## M5-E1 — Vuelve a hacer una pregunta

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
Une explícitamente dos aprendizajes previos: M3 enseñó a formular condiciones sobre vectores y M4 enseñó a recuperar una variable de una base como vector. M5 necesita recombinar ambas capacidades antes de introducir filtrado de casos.

### 3. Capacidad antes
Puede usar `>` sobre un vector y puede recuperar una variable con `$`.

### 4. Capacidad después
Puede formular una condición sobre una variable de una base y comprender que obtiene una respuesta `TRUE/FALSE` para cada caso.

### 5. Prerrequisitos
- `$`;
- vector;
- `>`;
- `TRUE/FALSE`;
- caso/fila;
- variable/columna.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno grande; se conectan capacidades previas.
- **Decisión nueva:** traducir una pregunta sobre una variable de la base a `base$variable > valor`.

### 7. Recuperaciones
Recupera:

- `>` de M3;
- `$` de M4;
- correspondencia posición ↔ respuesta lógica;
- fila/caso.

### 8. Contexto sustantivo
Encuesta social de ocho estudiantes.

### 9. Dataset / objetos
Objeto:

`encuesta_social_demo`

Variable objetivo:

`edad`

Valores:

```text
20 22 19 21 24 23 20 25
```

Pregunta:

> ¿Qué edades son mayores que 21?

### 10. Texto para estudiante
En M3 hicimos preguntas a vectores.

En M4 aprendimos que una variable de una base puede recuperarse como vector.

Ahora juntaremos ambas ideas.

Queremos preguntar:

> ¿qué edades son mayores que 21?

La variable `edad` está dentro de `encuesta_social_demo`.

Escribe la expresión que haga esa pregunta a toda la columna.

Antes de ejecutar, piensa:

> Para 22, ¿esperas `TRUE` o `FALSE`?
>
> ¿Y para 21?

Después ejecuta y observa cómo cada respuesta corresponde a un caso.

### 11. Modelo mental
`BASE $ VARIABLE → VECTOR → PREGUNTA → TRUE/FALSE POR CASO`

### 12. Representación / código trabajado
Después de la ejecución debe mostrarse:

```text
id        1      2      3      4      5      6      7      8
edad     20     22     19     21     24     23     20     25
> 21    FALSE   TRUE   FALSE  FALSE  TRUE   TRUE   FALSE  TRUE
```

### 13. Starter code
```r
# pregunta qué edades son mayores que 21
```

### 14. Acción esperada
Producir una comparación sobre `encuesta_social_demo$edad`.

### 15. Solución canónica
```r
encuesta_social_demo$edad > 21
```

### 16. Resultado esperado
```text
FALSE TRUE FALSE FALSE TRUE TRUE FALSE TRUE
```

### 17. Criterio semántico de éxito
Comprobar que:

- usa `encuesta_social_demo`;
- accede a `edad` con `$`;
- usa `>`;
- compara con 21;
- produce ocho valores lógicos en el orden de los casos;
- no escribe manualmente el vector lógico.

Perturbación opcional: si cambia una edad, la misma expresión debe actualizar la respuesta correspondiente.

### 18. Estrategias alternativas válidas
Se toleran diferencias de espacios y saltos de línea. La construcción objetivo requiere `$` porque este ejercicio también recupera esa habilidad. Un vector lógico literal no cuenta como estrategia válida.

### 19. Error esperado / misconception
- comparación invertida `21 > encuesta_social_demo$edad`;
- usar una variable inexistente;
- escribir manualmente TRUE/FALSE;
- creer que 21 produce TRUE en una comparación estricta `> 21`;
- olvidar que la salida corresponde a casos de la base.

### 20. Feedback correcto
**Bien.** Recuperaste `edad` como vector y le hiciste una pregunta. Ahora hay una respuesta `TRUE/FALSE` para cada caso de la base.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea el vector lógico:

> Las respuestas coinciden, pero las escribiste manualmente. Necesitamos que la condición las produzca desde `encuesta_social_demo$edad` para que cambien si cambian los datos.

Si invierte la comparación:

> `21 > encuesta_social_demo$edad` pregunta si 21 es mayor que cada edad. Queremos preguntar si cada edad es mayor que 21.

### 22. Hint 1
Primero piensa qué variable contiene la información que quieres preguntar.

### 23. Hint 2
En M4 recuperabas una variable con `$`; después puedes hacerle la pregunta con `>`.

### 24. Hint 3
```r
encuesta_social_demo$edad > 21
```

### 25. Predicción
Sí, breve. Predecir 22 y 21 antes de ejecutar.

### 26. Tipo de ejercicio
Recuperación semiautónoma.

### 27. Andamiaje
Medio: contexto y objetivo explícitos, sin sintaxis resuelta.

### 28. Carga cognitiva
**Baja-media.** No aparece contenido nuevo, pero se coordinan dos habilidades previamente separadas.

### 29. Fading
E1 exige producir la condición. E2 reutiliza esa misma condición en un worked example donde cambia la unidad seleccionada.

### 30. Recuperación futura
`>` reaparecerá en módulos posteriores; `$` continúa como infraestructura de M6–M13. La lógica condición → caso reaparece en todo filtrado futuro.

### 31. Riesgo de aprendizaje superficial
Memorizar una secuencia de símbolos sin comprender que cada respuesta lógica pertenece al mismo caso que el valor de `edad` correspondiente.

### 32. Criterio de transferencia
Debe poder aplicar más adelante otra condición a otra variable de una base sin que se le escriba la expresión completa.

### 33. Notas de implementación futura
El grader debe inspeccionar la expresión/resultado semánticamente y rechazar un vector lógico literal. No comparar texto exacto de consola.

---

## M5-E2 — De TRUE/FALSE a personas completas

### 1. Rol pedagógico
NOVEDAD / PUENTE CONCEPTUAL.

### 2. Por qué existe
Hace visible el cambio conceptual central entre M3 y M5: en M3 `TRUE` conservaba un valor de un vector; ahora una respuesta lógica puede decidir si permanece una fila/caso completo de una base. Este puente hace que `filter()` tenga significado antes de aprender la función.

### 3. Capacidad antes
Puede producir una condición que genera una respuesta `TRUE/FALSE` por caso.

### 4. Capacidad después
Comprende que un vector lógico alineado con las filas puede conservar casos completos y todas sus variables.

### 5. Prerrequisitos
- condición;
- TRUE/FALSE;
- `[]` en vectores;
- fila/caso;
- columna/variable;
- `$`.

### 6. Gran novedad
- **Sintaxis nueva:** `[,]` aparece solo como micro-novedad de lectura.
- **Concepto nuevo:** `TRUE` puede conservar una fila/caso completo.
- **Decisión nueva:** ninguna; el código es worked.

La gran novedad no es aprender indexación bidimensional general.

### 7. Recuperaciones
Recupera la condición de E1 y la idea de M3: `TRUE` conserva, `FALSE` deja fuera.

### 8. Contexto sustantivo
La misma pregunta de E1: edades mayores que 21.

### 9. Dataset / objetos
```r
mayores_21 <- encuesta_social_demo$edad > 21
```

Vector lógico esperado:

```text
FALSE TRUE FALSE FALSE TRUE TRUE FALSE TRUE
```

### 10. Texto para estudiante
En M3 usamos un vector lógico para conservar valores de otro vector.

Ahora la pregunta cambia:

> ¿podemos usar esas mismas respuestas para conservar **personas completas** de la base?

Primero guardamos la condición:

```r
mayores_21 <- encuesta_social_demo$edad > 21
```

Eso produce una respuesta para cada caso.

Mira la correspondencia:

```text
caso      cumple?
1         FALSE   → sale toda la fila
2         TRUE    → queda toda la fila
3         FALSE   → sale toda la fila
4         FALSE   → sale toda la fila
5         TRUE    → queda toda la fila
6         TRUE    → queda toda la fila
7         FALSE   → sale toda la fila
8         TRUE    → queda toda la fila
```

En una base, una forma de mostrar este mecanismo es:

```r
encuesta_social_demo[mayores_21, ]
```

Puedes leer la estructura mínima así:

```text
datos [ filas , columnas ]
```

y en nuestro ejemplo:

```text
encuesta_social_demo [ mayores_21 , ]
                       │            │
                       │            └─ no elegimos columnas: quedan todas
                       └────────────── TRUE/FALSE decide qué filas quedan
```

No necesitas memorizar esta forma.

Antes de ejecutar:

> ¿qué casos completos esperas que permanezcan?

### 11. Modelo mental
`TRUE/FALSE POR CASO → TRUE CONSERVA FILA COMPLETA → FALSE DEJA FUERA FILA COMPLETA`

### 12. Representación / código trabajado
```r
mayores_21 <- encuesta_social_demo$edad > 21
encuesta_social_demo[mayores_21, ]
```

### 13. Starter code
```r
mayores_21 <- encuesta_social_demo$edad > 21
encuesta_social_demo[mayores_21, ]
```

Es un worked example completo.

### 14. Acción esperada
Predecir los casos que quedarán, ejecutar el código y explicar la relación entre cada `TRUE` y una fila completa.

### 15. Solución canónica
```r
mayores_21 <- encuesta_social_demo$edad > 21
encuesta_social_demo[mayores_21, ]
```

### 16. Resultado esperado
Casos originales:

```text
2, 5, 6, 8
```

Todas las variables permanecen:

```text
id   edad   carrera          horas_estudio   trabaja
2    22     Historia         5                Sí
5    24     Trabajo Social   6                Sí
6    23     Antropología     3                Sí
8    25     Sociología       2                Sí
```

### 17. Criterio semántico de éxito
La evidencia principal es conceptual:

- identifica 2, 5, 6 y 8;
- explica que corresponden a posiciones `TRUE`;
- comprende que permanece la fila completa;
- comprende que el espacio después de la coma conserva todas las columnas;
- no necesita producir `[,]` autónomamente.

Perturbation test recomendado para implementación: cambiar valores de `edad` y comprobar que la selección de filas cambia con la condición.

### 18. Estrategias alternativas válidas
La explicación puede formularse de diferentes maneras. No se evalúan como habilidad otras formas de indexar data frames. El código de puente se entrega completo.

### 19. Error esperado / misconception
- creer que solo se conserva el valor de `edad`;
- creer que `TRUE` corresponde a una columna;
- pensar que el espacio después de la coma es un error;
- memorizar las filas 2,5,6,8 como estrategia;
- tratar `[condicion, ]` como nueva habilidad terminal.

### 20. Feedback correcto
**Bien.** La condición sigue produciendo una respuesta por caso, pero ahora cada `TRUE` conserva la fila completa de esa persona.

### 21. Feedback resultado correcto / estrategia incorrecta
Si explica la selección por números de fila:

> Esas son las filas que hoy permanecen, pero la idea importante no es memorizar 2, 5, 6 y 8. Permanecen porque sus posiciones tienen `TRUE` en `mayores_21`.

Si intenta producir manualmente otra indexación:

> En esta pantalla no necesitas aprender otra forma de indexar data frames. Concéntrate en el mecanismo: `TRUE` conserva casos completos.

### 22. Hint 1
Mira las posiciones donde `mayores_21` contiene `TRUE`.

### 23. Hint 2
Cada posición del vector lógico corresponde a la fila del mismo caso.

### 24. Hint 3
Los casos 2, 5, 6 y 8 tienen `TRUE`; por eso permanecen sus filas completas.

### 25. Predicción
Sí. Predecir filas antes de ejecutar.

### 26. Tipo de ejercicio
Worked example conceptual.

### 27. Andamiaje
Muy alto: condición, código y representación visual entregados.

### 28. Carga cognitiva
**Media.** El cambio de valor individual a caso completo es importante. La carga sintáctica se controla al no pedir producción de `[,]`.

### 29. Fading
E2 explica el mecanismo. E3 introduce una función más legible para expresar exactamente la misma selección.

### 30. Recuperación futura
La idea condición → casos se convierte en fundamento de `filter()` y reaparece desde M5-E3 hasta M13.

### 31. Riesgo de aprendizaje superficial
Recordar la forma `[condicion, ]` sin comprender la correspondencia lógica. Por eso la pantalla no la evalúa productivamente.

### 32. Criterio de transferencia
Debe poder comprender después que `filter()` conserva casos porque la condición se cumple, aunque ya no vuelva a usar la forma base R del puente.

### 33. Notas de implementación futura
No convertir esta pantalla en tutorial de indexación bidimensional. El grader debe priorizar explicación/selección conceptual y no exigir que el estudiante edite el código worked.

---

## M5-E3 — Una forma más legible de filtrar

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce `filter()` sobre un significado ya construido. El estudiante ya comprende que una condición conserva casos completos; ahora aprende una forma más legible y reusable de expresarlo.

### 3. Capacidad antes
Comprende que `TRUE/FALSE` puede determinar qué filas completas permanecen.

### 4. Capacidad después
Comprende y ejecuta `filter(base, condicion)` como operación que conserva casos que cumplen una condición.

### 5. Prerrequisitos
- condición;
- fila/caso;
- variable;
- E2;
- función con argumentos.

### 6. Gran novedad
- **Sintaxis nueva:** `filter()`.
- **Concepto nuevo:** ninguno grande; expresa el mecanismo ya construido.
- **Decisión nueva:** ninguna en el worked example.

### 7. Recuperaciones
Recupera exactamente la pregunta `edad > 21` y el subconjunto de E2.

### 8. Contexto sustantivo
Misma encuesta y misma pregunta que E1–E2.

### 9. Dataset / objetos
`encuesta_social_demo`

Condición:

```r
edad > 21
```

Casos esperados:

2, 5, 6, 8.

### 10. Texto para estudiante
En la pantalla anterior vimos el mecanismo:

> una condición produce `TRUE/FALSE` por caso y los `TRUE` conservan filas completas.

Ahora R dispone de una función más legible para expresar esa misma idea:

```r
filter(encuesta_social_demo, edad > 21)
```

Puedes leerla así:

```text
filter( BASE , CONDICIÓN )
        │          │
        │          └─ qué casos cumplen
        └──────────── dónde están los datos
```

`filter()` conserva los **casos** donde la condición se cumple.

Antes de ejecutar:

> ¿esperas que cambien las personas que quedaban en E2?

No deberían cambiar: estamos expresando la misma selección de otra manera.

Una diferencia de escritura importante:

Antes escribimos:

```r
encuesta_social_demo$edad > 21
```

porque necesitábamos recuperar la columna.

Dentro de `filter()` ya indicamos la base como primer argumento. Por eso podemos nombrar directamente una variable de esa base:

```r
edad > 21
```

No necesitas aprender cómo funciona internamente; por ahora basta con esta regla de lectura.

### 11. Modelo mental
`BASE + CONDICIÓN → filter() → SOLO CASOS QUE CUMPLEN + MISMAS VARIABLES`

### 12. Representación / código trabajado
```r
filter(encuesta_social_demo, edad > 21)
```

Comparación conceptual:

```text
E2: mecanismo visible con TRUE/FALSE
E3: misma idea expresada con filter()
```

### 13. Starter code
```r
filter(encuesta_social_demo, edad > 21)
```

### 14. Acción esperada
Predecir que quedarán los mismos casos de E2, ejecutar y comprobarlo.

### 15. Solución canónica
```r
filter(encuesta_social_demo, edad > 21)
```

### 16. Resultado esperado
```text
id   edad   carrera          horas_estudio   trabaja
2    22     Historia         5                Sí
5    24     Trabajo Social   6                Sí
6    23     Antropología     3                Sí
8    25     Sociología       2                Sí
```

### 17. Criterio semántico de éxito
Comprobar que:

- usa `filter()`;
- base correcta;
- condición `edad > 21`;
- conserva casos 2,5,6,8;
- mantiene todas las variables;
- comprende que el resultado coincide con E2;
- no interpreta el resultado como modificación permanente de la base.

Perturbation test recomendado: cambiar una edad y verificar que `filter()` conserva los casos que cumplan la nueva condición.

### 18. Estrategias alternativas válidas
Durante el primer encuentro, la construcción objetivo es `filter()`. Puede funcionar técnicamente `filter(encuesta_social_demo, encuesta_social_demo$edad > 21)`, pero no es la forma canónica; debe enseñarse a nombrar `edad` directamente dentro de `filter()`.

### 19. Error esperado / misconception
- usar posiciones de filas;
- pensar que `filter()` conserva variables;
- creer que `filter()` busca un valor puntual;
- repetir `$` por creerlo obligatorio;
- creer que la base original desaparece;
- usar un umbral incorrecto.

### 20. Feedback correcto
**Bien.** `filter()` conservó los mismos casos que el mecanismo de E2. La función no cambia la idea: expresa de forma más legible qué filas deben permanecer.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa `$` dentro de `filter()`:

> El resultado puede funcionar, pero dentro de `filter()` ya indicaste la base. Puedes escribir directamente `edad > 21`.

Si usa posiciones:

> Esas posiciones coinciden hoy, pero `filter()` debe decidir los casos mediante una condición para seguir funcionando si cambia el orden.

### 22. Hint 1
La operación busca conservar casos que cumplen una condición.

### 23. Hint 2
La forma general es `filter(base, condicion)`.

### 24. Hint 3
```r
filter(encuesta_social_demo, edad > 21)
```

### 25. Predicción
Sí. Preguntar si quedarán las mismas personas de E2.

### 26. Tipo de ejercicio
Worked example con comparación conceptual.

### 27. Andamiaje
Muy alto: código completo y resultado conceptualmente anticipado.

### 28. Carga cognitiva
**Media.** Se introduce una función nueva, pero el significado ya fue construido.

### 29. Fading
E3 entrega la función completa. E4 pedirá producir un nuevo filtro desde una pregunta sustantiva.

### 30. Recuperación futura
`filter()` se practica en E4, se integra en E7, se produce en E8 y reaparece en M6/M8/M9 y M13.

### 31. Riesgo de aprendizaje superficial
Aprender `filter()` como receta sin relacionarlo con caso/condición. El contraste explícito E2–E3 protege contra este riesgo.

### 32. Criterio de transferencia
Debe poder aplicar `filter()` a otra variable y otra condición sin posiciones manuales.

### 33. Notas de implementación futura
dplyr debe estar pre-cargado. No insertar `library(dplyr)` en el editor del estudiante. El grader debe verificar filas y condición, no código literal.

---

## M5-E4 — Filtra otro grupo

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Es la primera producción real de un filtro simple y, al mismo tiempo, recupera `==` y texto entre comillas. Además consolida `$` antes de retirar más apoyo.

### 3. Capacidad antes
Comprende `filter()` mediante un worked example y puede construir condiciones con `>`.

### 4. Capacidad después
Puede traducir una pregunta textual a una condición de igualdad y utilizarla para filtrar casos.

### 5. Prerrequisitos
- `$`;
- `==`;
- texto entre comillas;
- `filter()`;
- caso/fila.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** elegir la variable y formular una condición de igualdad para resolver la tarea.

### 7. Recuperaciones
Recupera:

- `==` de M3;
- `$` de M4;
- `filter()` de E3;
- texto entre comillas.

### 8. Contexto sustantivo
Identificar y conservar estudiantes de Sociología.

### 9. Dataset / objetos
Variable:

`carrera`

Valores:

```text
Sociología, Historia, Antropología, Sociología, Trabajo Social, Antropología, Historia, Sociología
```

Casos esperados:

1, 4, 8.

### 10. Texto para estudiante
Ahora cambia la pregunta.

Queremos conservar solo las personas cuya carrera es:

```text
Sociología
```

Hazlo en dos pasos.

**Paso 1.** Construye la condición que identifica qué casos tienen carrera `"Sociología"`.

**Paso 2.** Usa esa misma idea para conservar las filas completas de esos casos con `filter()`.

Recuerda:

> fuera de `filter()` recuperamos una variable desde la base con `$`;
>
> dentro de `filter()` ya indicamos la base y podemos nombrar directamente la variable.

### 11. Modelo mental
`BASE$VARIABLE == TEXTO → TRUE/FALSE → filter(BASE, VARIABLE == TEXTO) → CASOS QUE CUMPLEN`

### 12. Representación / código trabajado
No se entrega código resuelto. Puede mostrarse solo la estructura conceptual:

```text
pregunta lógica
↓
mismos casos
↓
filter()
```

### 13. Starter code
```r
# 1. pregunta qué casos tienen carrera "Sociología"


# 2. conserva solo esos casos
```

### 14. Acción esperada
Producir una condición con `$` y `==`, después un `filter()` equivalente.

### 15. Solución canónica
```r
encuesta_social_demo$carrera == "Sociología"

filter(encuesta_social_demo, carrera == "Sociología")
```

### 16. Resultado esperado
Vector lógico:

```text
TRUE FALSE FALSE TRUE FALSE FALSE FALSE TRUE
```

Base filtrada:

```text
id   edad   carrera      horas_estudio   trabaja
1    20     Sociología   3                No
4    21     Sociología   4                No
8    25     Sociología   2                Sí
```

### 17. Criterio semántico de éxito
**Condición**
- usa `encuesta_social_demo$carrera`;
- usa `==`;
- compara con `"Sociología"` entre comillas;
- produce vector lógico correcto.

**Filtro**
- usa `filter()`;
- base correcta;
- condición correcta;
- conserva casos 1,4,8;
- mantiene todas las variables;
- no hardcodea posiciones.

Perturbation test muy recomendado: cambiar `carrera` de uno o más casos y verificar que la misma estrategia se adapta.

### 18. Estrategias alternativas válidas
Se aceptan espacios y formato diferentes. En la segunda parte, la forma canónica usa `filter()` y `carrera` directamente. Una selección por números de fila no demuestra la habilidad objetivo.

### 19. Error esperado / misconception
- usar `=` en lugar de `==`;
- escribir `Sociología` sin comillas;
- seleccionar filas 1,4,8 por posición;
- usar variable incorrecta;
- construir bien la condición pero no trasladarla a `filter()`;
- pensar que `filter()` cambia columnas.

### 20. Feedback correcto
**Bien.** Primero construiste la pregunta lógica y después usaste esa misma condición para conservar casos completos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa posiciones:

> El subconjunto coincide, pero seleccionaste filas por posición. Queremos una condición que siga funcionando si las carreras o el orden de los casos cambian.

Si usa `=`:

> Para preguntar si dos valores son iguales usamos `==`. Aquí no estamos guardando un valor.

Si omite comillas:

> `"Sociología"` es texto; necesita comillas.

### 22. Hint 1
¿Qué variable contiene la carrera de cada caso?

### 23. Hint 2
La condición debe preguntar si `carrera` es igual a `"Sociología"`.

### 24. Hint 3
```r
encuesta_social_demo$carrera == "Sociología"

filter(encuesta_social_demo, carrera == "Sociología")
```

### 25. Predicción
No se añade una fase separada; construir la condición ya exige anticipar el grupo.

### 26. Tipo de ejercicio
Producción guiada en dos pasos.

### 27. Andamiaje
Medio: estructura de dos pasos, sin sintaxis resuelta.

### 28. Carga cognitiva
**Media.** Coordina varias habilidades conocidas (`$`, `==`, texto y `filter()`), pero no introduce contenido nuevo.

### 29. Fading
Se retira el worked code de E3. E5 volverá a ofrecer un worked example porque introducirá una sintaxis nueva distinta: el pipe.

### 30. Recuperación futura
`==` alcanza producción en Checkpoint B y reaparece en M7/M12. `$` continúa en M6–M12. `filter()` se integra en E7 y E8.

### 31. Riesgo de aprendizaje superficial
Memorizar los casos de Sociología por posición. El grader y perturbation test deben exigir dependencia de `carrera`.

### 32. Criterio de transferencia
Debe poder formular después otra igualdad textual y usarla dentro de `filter()` sin que se le entregue la condición.

### 33. Notas de implementación futura
El editor puede contener dos zonas o un único bloque con dos líneas. La comprobación debe distinguir condición y filtro para ofrecer feedback diagnóstico separado.

---

## M5-E5 — Los datos pasan a la siguiente acción

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce el pipe nativo `|>` después de que `filter()` ya tenga significado y práctica. Utiliza una sola operación conocida para aislar la nueva idea de flujo.

### 3. Capacidad antes
Puede producir un `filter()` simple.

### 4. Capacidad después
Puede leer y ejecutar un pipeline de una operación, comprendiendo que los datos pasan a la acción siguiente y que la base original no se modifica automáticamente.

### 5. Prerrequisitos
- `filter()`;
- base de datos;
- condición;
- resultado de E4.

### 6. Gran novedad
- **Sintaxis nueva:** `|>`.
- **Concepto nuevo:** flujo de datos entre etapas.
- **Decisión nueva:** ninguna; se reutiliza exactamente el filtro anterior.

### 7. Recuperaciones
Recupera el filtro:

```r
filter(encuesta_social_demo, carrera == "Sociología")
```

### 8. Contexto sustantivo
Mismo grupo de Sociología de E4.

### 9. Dataset / objetos
`encuesta_social_demo`

Condición:

```r
carrera == "Sociología"
```

### 10. Texto para estudiante
En E4 escribiste una función donde la base aparecía dentro de los paréntesis:

```r
filter(encuesta_social_demo, carrera == "Sociología")
```

R también permite escribir el flujo desde los datos hacia la acción:

```r
encuesta_social_demo |>
  filter(carrera == "Sociología")
```

Puedes leer `|>` como:

> toma estos datos y pásalos a la siguiente acción.

Visualmente:

```text
encuesta_social_demo
↓
filter(carrera == "Sociología")
↓
casos de Sociología
```

Antes de ejecutar:

> ¿esperas que cambien los casos respecto de E4?

No deberían cambiar. La operación es la misma; cambia la forma de escribir el flujo.

Después de ejecutar el pipeline, consulta otra vez:

```r
encuesta_social_demo
```

y observa que la base original sigue completa.

### 11. Modelo mental
`DATOS → |> → ACCIÓN → RESULTADO`

### 12. Representación / código trabajado
```r
encuesta_social_demo |>
  filter(carrera == "Sociología")
```

### 13. Starter code
```r
encuesta_social_demo |>
  filter(carrera == "Sociología")
```

Después:

```r
encuesta_social_demo
```

### 14. Acción esperada
Ejecutar el pipeline, comparar su resultado con E4 y volver a consultar la base original.

### 15. Solución canónica
```r
encuesta_social_demo |>
  filter(carrera == "Sociología")
```

### 16. Resultado esperado
Mismas filas de E4:

```text
id   edad   carrera      horas_estudio   trabaja
1    20     Sociología   3                No
4    21     Sociología   4                No
8    25     Sociología   2                Sí
```

Al volver a consultar `encuesta_social_demo`, siguen existiendo los 8 casos.

### 17. Criterio semántico de éxito
Comprobar que:

- usa pipe nativo `|>`;
- parte desde `encuesta_social_demo`;
- pasa la base a `filter(carrera == "Sociología")`;
- obtiene las mismas filas de E4;
- comprende que la base original sigue completa;
- no usa `%>%`.

### 18. Estrategias alternativas válidas
Para esta pantalla el objetivo es específicamente `|>`, por lo que `filter(encuesta_social_demo, ...)` produce el resultado correcto pero no demuestra la nueva habilidad. Debe recibir feedback de estrategia incompleta, no considerarse dominio completo.

### 19. Error esperado / misconception
- usar `%>%`;
- creer que el pipe modifica la base original;
- pensar que `|>` significa asignación;
- perder de vista qué objeto entra a `filter()`;
- añadir más operaciones antes de comprender una sola etapa.

### 20. Feedback correcto
**Bien.** Los datos pasaron a `filter()` mediante `|>` y obtuviste el mismo subconjunto. La base original sigue disponible sin cambios.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa `filter(encuesta_social_demo, ...)`:

> El resultado es correcto. En esta pantalla también queremos practicar cómo pasar la base a la acción siguiente mediante `|>`.

Si usa `%>%`:

> En Social R usamos únicamente el pipe nativo `|>`.

Si cree que modificó la base:

> El pipeline produjo un resultado temporal. Consulta `encuesta_social_demo`: la fuente sigue completa.

### 22. Hint 1
Parte desde la base que quieres enviar a una acción.

### 23. Hint 2
`|>` puede leerse como “pasa este resultado a la siguiente acción”.

### 24. Hint 3
```r
encuesta_social_demo |>
  filter(carrera == "Sociología")
```

### 25. Predicción
Sí. Preguntar si cambiarán los casos respecto de E4.

### 26. Tipo de ejercicio
Worked example + comprobación de permanencia de la fuente.

### 27. Andamiaje
Muy alto: una sola operación y código completo.

### 28. Carga cognitiva
**Media.** La notación es nueva, pero la operación y el resultado ya son conocidos.

### 29. Fading
E5 introduce el pipe con una sola etapa. E7 lo recuperará con dos operaciones y argumentos incompletos.

### 30. Recuperación futura
El pipe se practica en E7, se produce autónomamente en E8 y reaparece M6–M13.

### 31. Riesgo de aprendizaje superficial
Memorizar `|>` como una flecha decorativa. La lectura verbal y la comprobación de la base original deben mantener el significado de flujo.

### 32. Criterio de transferencia
Debe poder interpretar un pipeline nuevo explicando qué resultado recibe cada etapa.

### 33. Notas de implementación futura
No mostrar `%>%`. No guardar todavía el resultado en un objeto. La consulta posterior de `encuesta_social_demo` debe ocurrir en la misma pantalla para comprobar no-mutación.

---

## M5-E6 — Qué variables necesito

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce `select()` como respuesta a una necesidad diferente de `filter()`: conservar variables, no casos. Se presenta sin pipe para aislar la función y reducir interacción entre elementos nuevos.

### 3. Capacidad antes
Puede filtrar casos y comprende el pipe con una sola operación.

### 4. Capacidad después
Puede usar `select()` para conservar variables por nombre y distinguir con claridad la pregunta “qué casos” de “qué variables”.

### 5. Prerrequisitos
- variable/columna;
- caso/fila;
- nombres de variables;
- función con argumentos;
- significado de `filter()`.

### 6. Gran novedad
- **Sintaxis nueva:** `select()`.
- **Concepto nuevo:** conservar variables por nombre.
- **Decisión nueva:** distinguir si una tarea requiere cambiar casos o variables.

### 7. Recuperaciones
Recupera M4:

- columna = variable;
- fila = caso.

También contrasta con `filter()`.

### 8. Contexto sustantivo
Preparar una vista con solo `edad` y `carrera`.

### 9. Dataset / objetos
`encuesta_social_demo`

Variables originales:

```text
id, edad, carrera, horas_estudio, trabaja
```

Variables objetivo:

```text
edad, carrera
```

### 10. Texto para estudiante
Hasta ahora aprendimos a responder:

> ¿qué **casos** necesito?

Eso lo hacemos con:

```r
filter()
```

Ahora aparece otra pregunta:

> ¿qué **variables** necesito?

Para conservar variables por nombre podemos usar:

```r
select()
```

Queremos mantener únicamente:

- `edad`;
- `carrera`.

Observa la diferencia:

| Pregunta | Herramienta |
|---|---|
| ¿Qué casos necesito? | `filter()` |
| ¿Qué variables necesito? | `select()` |

Antes:

```text
id | edad | carrera | horas_estudio | trabaja
```

Después esperamos:

```text
edad | carrera
```

Antes de ejecutar:

> ¿cambiará la cantidad de casos o la cantidad de variables?

Completa el código.

### 11. Modelo mental
`BASE → select() → MISMOS CASOS + SOLO VARIABLES ELEGIDAS`

### 12. Representación / código trabajado
Estructura:

```r
select(base, variable1, variable2)
```

No se muestra todavía con pipe.

### 13. Starter code
```r
select(encuesta_social_demo, ______, ______)
```

### 14. Acción esperada
Completar los nombres `edad` y `carrera`.

### 15. Solución canónica
```r
select(encuesta_social_demo, edad, carrera)
```

### 16. Resultado esperado
Ocho casos y dos variables:

```text
edad   carrera
20     Sociología
22     Historia
19     Antropología
21     Sociología
24     Trabajo Social
23     Antropología
20     Historia
25     Sociología
```

### 17. Criterio semántico de éxito
Comprobar que:

- usa `select()`;
- base correcta;
- conserva exactamente `edad` y `carrera`;
- mantiene los ocho casos y su orden;
- selecciona variables por nombre;
- no usa posiciones numéricas como estrategia objetivo.

### 18. Estrategias alternativas válidas
Diferencias de espacios son válidas. El orden `carrera, edad` solo es válido si la tarea no exige explícitamente el orden mostrado; en esta especificación la consigna presenta `edad` y luego `carrera`, por lo que el resultado canónico conserva ese orden. Otras sintaxis de selección de columnas no demuestran la habilidad objetivo.

### 19. Error esperado / misconception
- usar `filter()`;
- seleccionar filas en lugar de columnas;
- usar posiciones numéricas `[, c(2,3)]`;
- creer que `select()` elimina casos;
- incluir variables extra;
- usar pipe aunque aún no sea necesario.

### 20. Feedback correcto
**Bien.** Conservaste todos los casos y cambiaste únicamente qué variables aparecen. Eso es lo que distingue `select()` de `filter()`.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa posiciones:

> El resultado coincide, pero seleccionaste columnas por posición. Queremos elegir variables por nombre para que el código siga siendo legible y resistente a cambios de orden.

Si usa `filter()`:

> `filter()` responde qué casos quedan. Aquí la pregunta es qué variables conservar.

### 22. Hint 1
La tarea no pide quitar personas; pide conservar ciertas variables.

### 23. Hint 2
`select()` recibe primero la base y después los nombres de las variables.

### 24. Hint 3
```r
select(encuesta_social_demo, edad, carrera)
```

### 25. Predicción
Sí. Preguntar si cambiarán casos o variables.

### 26. Tipo de ejercicio
Worked/completion.

### 27. Andamiaje
Alto: función y base visibles; solo faltan nombres de variables.

### 28. Carga cognitiva
**Media.** Aparece una función nueva, pero se apoya directamente en la distinción caso/variable de M4 y no se combina todavía con pipe.

### 29. Fading
E6 aísla `select()`. E7 lo combinará con `filter()` y `|>`.

### 30. Recuperación futura
`select()` se practica E7, se produce E8 y reaparece M9/M11/M13.

### 31. Riesgo de aprendizaje superficial
Confundir `select()` con `filter()` o memorizar posiciones de columnas. La representación casos vs variables es central.

### 32. Criterio de transferencia
Debe poder seleccionar por nombre otras variables de otra base sin usar posiciones.

### 33. Notas de implementación futura
No introducir pipe en el primer encuentro. El grader debe validar nombres/columnas y número de casos, no literal de impresión.

---

## M5-E7 — Filtra y después selecciona

### 1. Rol pedagógico
INTEGRACIÓN.

### 2. Por qué existe
Combina por primera vez las tres construcciones nucleares de M5: `filter()`, `|>` y `select()`. La tarea obliga a distinguir qué casos necesita y qué variables necesita.

### 3. Capacidad antes
Conoce `filter()`, comprende `|>` y ha usado `select()` de forma aislada.

### 4. Capacidad después
Puede seguir y completar un pipeline de dos operaciones donde cada etapa recibe el resultado de la anterior.

### 5. Prerrequisitos
- `filter()`;
- `|>`;
- `select()`;
- `==`;
- texto entre comillas;
- caso vs variable.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno; integración.
- **Decisión nueva:** coordinar una condición de casos y una elección de variables dentro del mismo flujo.

### 7. Recuperaciones
Recupera:

- `trabaja == "Sí"`;
- `filter()`;
- pipe;
- `select()`;
- distinción caso/variable.

### 8. Contexto sustantivo
Preparar una base de personas que trabajan conservando solo edad y carrera.

### 9. Dataset / objetos
`encuesta_social_demo`

Casos donde `trabaja == "Sí"`:

2, 5, 6, 8.

Variables finales:

`edad`, `carrera`.

### 10. Texto para estudiante
Ahora combinaremos dos decisiones distintas.

Necesitamos:

1. quedarnos solo con las personas que trabajan;
2. conservar únicamente `edad` y `carrera`.

Piensa en dos preguntas:

> ¿qué **casos** necesito?

y después:

> ¿qué **variables** necesito?

En esta tarea primero filtramos casos y después seleccionamos variables.

Eso no significa que siempre exista una única regla universal de orden. Aquí este orden responde a la pregunta.

Completa el pipeline.

### 11. Modelo mental
`BASE → FILTER: CASOS → RESULTADO INTERMEDIO → SELECT: VARIABLES → RESULTADO FINAL`

### 12. Representación / código trabajado
Representación conceptual:

```text
encuesta_social_demo
↓
filter(trabaja == "Sí")
↓
casos 2, 5, 6, 8
↓
select(edad, carrera)
↓
2 variables
```

### 13. Starter code
```r
encuesta_social_demo |>
  filter(__________________) |>
  select(________, ________)
```

### 14. Acción esperada
Completar la condición y los nombres de variables.

### 15. Solución canónica
```r
encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(edad, carrera)
```

### 16. Resultado esperado
```text
edad   carrera
22     Historia
24     Trabajo Social
23     Antropología
25     Sociología
```

### 17. Criterio semántico de éxito
Comprobar:

- parte desde `encuesta_social_demo`;
- usa pipe nativo `|>`;
- `filter()` recibe condición `trabaja == "Sí"`;
- usa otro `|>`;
- `select()` conserva `edad` y `carrera`;
- resultado tiene cuatro casos y dos variables;
- conserva el orden de los casos;
- no hardcodea filas ni columnas;
- no usa `%>%`.

Perturbation test muy recomendado: cambiar orden de filas, valores de `trabaja` y orden de columnas; la estrategia debe seguir funcionando.

### 18. Estrategias alternativas válidas
Variaciones de espacios y saltos de línea son válidas. El orden lógico de esta tarea debe mantener primero la selección de casos y luego las dos variables porque el starter y la progresión trabajan ese flujo. Un resultado equivalente sin pipe se considera resultado correcto pero estrategia incompleta para esta actividad.

### 19. Error esperado / misconception
- intercambiar `filter()` y `select()` sin adaptar la tarea;
- usar `=` en vez de `==`;
- omitir comillas en `"Sí"`;
- usar `%>%`;
- seleccionar posiciones;
- hardcodear casos;
- pensar que `select()` decide qué personas quedan;
- creer que cada etapa opera otra vez sobre la base original en vez del resultado anterior.

### 20. Feedback correcto
**Bien.** Primero decidiste qué casos necesitabas y después qué variables. Cada etapa recibió el resultado de la anterior.

### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene el mismo resultado sin pipe:

> El resultado es correcto, pero esta actividad también practica pasar el resultado de una operación a la siguiente con `|>`.

Si usa posiciones:

> El subconjunto coincide, pero depende de posiciones. La estrategia debe seguir funcionando si cambian el orden de filas o columnas.

Si confunde operaciones:

> Pregunta primero “¿qué casos necesito?” y después “¿qué variables necesito?”.

### 22. Hint 1
Primero decide qué casos necesitas; después qué variables.

### 23. Hint 2
El resultado de `filter()` puede pasar a `select()` mediante `|>`.

### 24. Hint 3
```r
encuesta_social_demo |>
  filter(trabaja == "Sí") |>
  select(edad, carrera)
```

### 25. Predicción
No se añade una fase separada. La propia integración exige razonar el resultado intermedio.

### 26. Tipo de ejercicio
Completion / integración.

### 27. Andamiaje
Medio: estructura del pipeline y funciones visibles, argumentos incompletos.

### 28. Carga cognitiva
**Media.** Interactúan tres herramientas ya conocidas. La carga es mayor que E5/E6, pero no hay sintaxis nueva.

### 29. Fading
E7 mantiene nombres de funciones y pipe. E8 retirará también esas señales.

### 30. Recuperación futura
La preparación mediante pipeline reaparece desde M6 hasta M13.

### 31. Riesgo de aprendizaje superficial
Completar huecos por imitación sin entender casos vs variables. El feedback y las preguntas conceptuales deben sostener el significado de cada etapa.

### 32. Criterio de transferencia
Debe poder producir en E8 un pipeline equivalente en una base nueva sin que la consigna nombre `filter()`, `select()` ni pipe.

### 33. Notas de implementación futura
El grader debe inspeccionar estructura del pipeline y resultado. No penalizar formato cosmético. Registrar por separado errores de condición, filter, pipe y select.

---

## M5-E8 — Checkpoint B: prepara los datos

### 1. Rol pedagógico
TRANSFERENCIA / CHECKPOINT.

### 2. Por qué existe
Diagnostica si el estudiante puede recibir una necesidad de preparación de datos, decidir qué casos conservar, qué variables conservar y construir un pipeline reproducible sin que la consigna nombre las funciones.

### 3. Capacidad antes
Ha practicado `filter()`, `|>`, `select()`, igualdad textual y asignación en módulos previos.

### 4. Capacidad después
Puede preparar de forma autónoma un subconjunto simple en una base nueva y guardarlo en un objeto.

### 5. Prerrequisitos
- `<-`;
- `==`;
- texto entre comillas;
- `filter()`;
- `|>`;
- `select()`;
- caso vs variable.

No se exige `$`, `head()`, `str()` ni `[condicion, ]`.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** decidir autónomamente la ruta completa.

### 7. Recuperaciones
Recupera:

- asignación;
- igualdad textual;
- selección de casos;
- selección de variables;
- pipe;
- distinción caso/variable.

### 8. Contexto sustantivo
Nueva encuesta juvenil para una pregunta posterior.

### 9. Dataset / objetos
Objeto ya disponible:

`encuesta_jovenes`

```text
id   edad   estudia   comuna    transporte
1    18     Sí        Norte     Bus
2    20     No        Centro    Metro
3    19     Sí        Sur       Bicicleta
4    22     Sí        Centro    Bus
5    21     No        Norte     Metro
6    23     Sí        Sur       Metro
```

Objeto final requerido:

`datos_preparados`

### 10. Texto para estudiante
**Checkpoint B — Bases y preparación**

Para una pregunta posterior necesitamos trabajar solo con las personas que estudian.

De ellas necesitamos únicamente:

- `edad`;
- `comuna`.

Prepara esos datos y guárdalos en un objeto llamado:

```text
datos_preparados
```

No se indican las funciones. Decide qué operaciones necesita la tarea.

Las pistas están disponibles si las necesitas.

### 11. Modelo mental
`BASE NUEVA → DECIDIR CASOS → DECIDIR VARIABLES → ENCADENAR → GUARDAR RESULTADO`

### 12. Representación / código trabajado
No hay worked example nuevo. Solo se muestra la tabla de `encuesta_jovenes`.

### 13. Starter code
```r
# guarda aquí los datos preparados
```

### 14. Acción esperada
Construir y guardar un pipeline que:

1. conserve casos con `estudia == "Sí"`;
2. conserve `edad` y `comuna`;
3. use `|>`;
4. guarde el resultado en `datos_preparados`.

### 15. Solución canónica
```r
datos_preparados <- encuesta_jovenes |>
  filter(estudia == "Sí") |>
  select(edad, comuna)
```

### 16. Resultado esperado
```text
edad   comuna
18     Norte
19     Sur
22     Centro
23     Sur
```

### 17. Criterio semántico de éxito
Comprobar por componentes:

**Objeto**
- `datos_preparados` existe.

**Condición**
- identifica `estudia == "Sí"` semánticamente;
- no usa posiciones de filas.

**Filter**
- conserva los casos originales 1,3,4,6.

**Pipe**
- utiliza `|>`;
- el resultado de `filter()` alimenta a `select()`.

**Select**
- conserva exactamente `edad` y `comuna`;
- no usa posiciones numéricas de columnas.

**Resultado**
- cuatro filas;
- dos variables;
- valores correctos;
- orden de casos conservado.

**Fuente**
- `encuesta_jovenes` permanece disponible como base original.

Perturbation test obligatoriamente recomendado para implementación: cambiar orden de casos, respuestas de `estudia` y orden de columnas. La solución semántica debe seguir funcionando.

### 18. Estrategias alternativas válidas
Se aceptan diferencias de espacios, indentación y saltos de línea.

Una solución anidada como:

```r
datos_preparados <- select(
  filter(encuesta_jovenes, estudia == "Sí"),
  edad,
  comuna
)
```

puede producir el resultado correcto, pero no demuestra producción del pipe, que es una habilidad terminal de M5. Debe clasificarse como **resultado correcto / estrategia curricular incompleta**.

No se exige `$`.

### 19. Error esperado / misconception
- hardcodear filas 1,3,4,6;
- hardcodear valores del resultado;
- seleccionar columnas por posiciones;
- usar `=` en vez de `==`;
- olvidar comillas en `"Sí"`;
- usar `%>%`;
- no usar pipe;
- no guardar el resultado;
- conservar variables extra;
- filtrar correctamente pero no seleccionar;
- seleccionar correctamente pero no filtrar;
- modificar/sobrescribir la base original.

### 20. Feedback correcto
**Checkpoint B completado.** Decidiste qué casos necesitabas, qué variables necesitabas, encadenaste ambas operaciones y guardaste un nuevo objeto sin depender de posiciones manuales.

### 21. Feedback resultado correcto / estrategia incorrecta
**Condición incorrecta**

> ¿Qué característica distingue a las personas que deben permanecer? La condición debe salir de `estudia`.

**Filter ausente**

> Ya identificaste el grupo, pero todavía necesitas conservar únicamente esos casos.

**Select ausente**

> Los casos son correctos, pero todavía conservas variables que la pregunta no necesita.

**Pipe ausente**

> El resultado puede ser correcto, pero el checkpoint también comprueba que puedes pasar el resultado de una etapa a la siguiente con `|>`.

**Hardcoding**

> El resultado coincide, pero elegiste filas, columnas o valores manualmente. La estrategia debe seguir funcionando si cambia el orden.

**Objeto no guardado**

> El subconjunto es correcto. Ahora guárdalo en `datos_preparados`.

### 22. Hint 1
Primero decide qué casos deben quedar y después qué variables necesitas.

### 23. Hint 2
Una operación conserva casos y otra conserva variables. Puedes pasar el resultado de la primera a la segunda con `|>`.

### 24. Hint 3
```r
datos_preparados <- encuesta_jovenes |>
  filter(estudia == "Sí") |>
  select(edad, comuna)
```

### 25. Predicción
No se añade una predicción ritual. La tarea integrada ya exige decidir el estado final.

### 26. Tipo de ejercicio
Checkpoint de transferencia cercana.

### 27. Andamiaje
Bajo: solo comentario inicial. Las pistas comienzan cerradas y escalan concepto → estructura → casi solución.

### 28. Carga cognitiva
**Media.** Integra varias habilidades conocidas, pero no introduce sintaxis ni conceptos nuevos y la pregunta sustantiva es simple.

### 29. Fading
Punto final de M5. Se retiran nombres de funciones, pipe y estructura del starter.

### 30. Recuperación futura
M6, M8, M9, M10, M11 y M13 recuperan preparación de datos. El pipe y filtrado se convierten en infraestructura recurrente.

### 31. Riesgo de aprendizaje superficial
Reproducir el resultado mediante posiciones conocidas o memorizar la secuencia sin decidir casos/variables. El semantic grader y perturbation test deben proteger contra ambas estrategias.

### 32. Criterio de transferencia
Existe evidencia de dominio si puede preparar otra base con otra condición y otras variables sin que la consigna nombre las funciones y sin hardcoding.

### 33. Notas de implementación futura
Registrar el nivel de ayuda puede ser útil para diagnóstico, pero no penalizar el uso de pistas. El criterio de dominio debe distinguir resultado, estrategia y dependencia de los datos. No implementar nuevas herramientas en el checkpoint.

---

# Cierre conceptual de M5 y puente a M6

Después del Checkpoint B mostrar:

> Ya podemos preparar los casos y variables que necesitamos para una pregunta.
>
> Hasta ahora, sin embargo, todas las celdas que usamos tenían una respuesta.
>
> ¿Qué ocurre cuando una persona no respondió o un valor no está registrado?

La transición termina ahí.

M5 NO debe introducir todavía:

```r
NA
is.na()
na.rm = TRUE
complete.cases()
```

# Retención esperada después de una semana

## Reconocimiento
El estudiante debería reconocer:

```r
filter()
```

como una operación para conservar casos que cumplen una condición.

Debería reconocer:

```r
select()
```

como una operación para conservar variables.

Debería reconocer:

```r
|>
```

como una forma de pasar el resultado de una etapa a la siguiente.

## Producción
Con poca ayuda debería poder producir:

```r
filter(base, condicion)
```

y:

```r
select(base, variable1, variable2)
```

## Integración
Con poca ayuda debería poder producir:

```r
base |>
  filter(condicion) |>
  select(variable1, variable2)
```

## Puente base R
No se exige producir:

```r
datos[condicion, ]
```

Solo debe reconocer, si vuelve a verlo, que una condición puede seleccionar filas completas.

# Checkpoint B — habilidades diagnosticadas

| Habilidad | Nivel esperado |
|---|---|
| `<-` | producir |
| `==` | producir |
| condición | producir |
| `filter()` | producir |
| `|>` | producir |
| `select()` | producir |
| casos vs variables | decidir |
| hardcoding | evitar |
| `$` | no se exige como núcleo |
| `[condicion, ]` | no se exige |

# Auditoría del módulo

## Conteo por rol
- RECUPERACIÓN: 1
- NOVEDAD / PUENTE CONCEPTUAL: 1
- NOVEDAD: 3
- PRÁCTICA: 1
- INTEGRACIÓN: 1
- TRANSFERENCIA / CHECKPOINT: 1

## Porcentaje local de pantallas con gran novedad
4 de 8 ejercicios: 50 %.

Este valor no obliga a modificar la arquitectura porque:

- el criterio de ≤40 % se aplica al conjunto de 88 ejercicios;
- E2 contiene una gran novedad conceptual pero no una habilidad sintáctica terminal;
- E3, E5 y E6 aíslan una sola construcción nueva cada uno;
- existen pantallas de práctica e integración entre las nuevas construcciones;
- la distribución global del plan maestro permanece en 39,8 % de novedad.

## Habilidades nucleares relativamente consolidadas
- condición sobre una variable de una base;
- `filter()` para conservar casos;
- `==` en una condición textual;
- `|>` como flujo;
- `select()` por nombres;
- distinción filter/casos vs select/variables;
- pipeline simple de dos operaciones;
- guardado de resultado preparado.

## Habilidad solo puente
```r
datos[condicion, ]
```

## Recuperación futura
- `filter()`: M6/M8/M9 y M13;
- `|>`: M6–M13;
- `select()`: M9/M11/M13;
- `$`: M6–M12;
- `==`: M7/M12/M13.

## Riesgos de sobrecarga controlados
- E2 es fully worked;
- E3 expresa el mismo resultado que E2;
- `library(dplyr)` no se enseña;
- E5 usa una sola acción;
- E6 introduce `select()` sin pipe;
- E7 integra herramientas ya conocidas;
- E8 no introduce contenido nuevo.

## Checkpoint
Sí: M5-E8.

No contiene sintaxis nueva y diagnostica la cadena:

```text
necesidad
→ casos
→ variables
→ filter
→ pipe
→ select
→ guardar
```

# Contrato de datos

M5 conserva exactamente la vista pedagógica locked de M4 para `encuesta_social_demo`.

No amplía ni redefine:

- edades;
- carreras;
- horas de estudio;
- codificación de `trabaja`.

`trabaja` continúa representada como texto `"Sí"` / `"No"`.

El dataset lock global M4–M8 sigue siendo una tarea técnica/pedagógica transversal pendiente del plan maestro. Cualquier futuro dataset lock debe preservar este contrato o actualizar deliberadamente los Markdown locked antes de implementación.

# Declaración de lock

M5 queda pedagógicamente cerrado con 8 ejercicios.

- **Sintaxis introducida:** `filter()`, `|>`, `select()`.
- **Habilidad solo puente:** `datos[condicion, ]`.
- **Habilidades nucleares:** condición por caso, filtrado de casos, selección de variables, flujo mediante pipe, preparación reproducible.
- **dplyr:** pre-cargado; `library(dplyr)` no es contenido del estudiante.
- **Checkpoint:** M5-E8 diagnostica preparación autónoma en `encuesta_jovenes`.
- **Recuperación futura:** M6–M13.
- **Puente a M6:** seleccionar datos → reconocer cuándo falta información.

# M5 PEDAGOGICALLY LOCKED
