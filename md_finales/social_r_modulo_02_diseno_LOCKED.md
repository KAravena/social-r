# Social R — Módulo 2
## Trabajar con varios valores

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede trabajar con objetos que contienen un único valor: crearlos con `<-`, consultarlos y reutilizarlos.

### Capacidad después
Puede crear un vector numérico, reconocer que conserva varios valores en un orden, utilizarlo como un conjunto de valores y seleccionar uno o varios elementos por posición.

### Pregunta central
¿Cómo guardo varios valores relacionados en un mismo objeto y cómo recupero los que necesito?

### Modelo mental
`UN VALOR → VARIOS VALORES RELACIONADOS → VECTOR → ORDEN → POSICIÓN → SELECCIÓN`

### Habilidades nucleares
Al terminar el módulo, el estudiante debe poder:

- crear un vector numérico con `c()`;
- comprender que un objeto puede contener varios valores;
- reconocer que el orden de esos valores importa;
- interpretar una posición como la ubicación de un valor dentro del vector;
- seleccionar un valor mediante `[]`;
- seleccionar varias posiciones mediante una combinación de `c()` y `[]`;
- recuperar `<-`, consulta y reutilización sin que vuelvan a enseñarse desde cero.

Las habilidades nucleares del módulo son `c()`, la idea de orden/posición y `[]`.

### Habilidades funcionales
`sum()` se introduce como herramienta funcional secundaria para mostrar que un vector completo puede utilizarse dentro de una operación. No se considera una habilidad nuclear equivalente a `c()` o `[]`, ni se exige el mismo nivel de autonomía después de una semana sin práctica.

### Habilidades recuperadas
M2 recupera desde M1:

- `<-`;
- objetos;
- consulta;
- reutilización;
- ejecución con Ctrl + Enter.

Estas habilidades se utilizan dentro de problemas nuevos; no se reenseñan desde cero.

Dentro de M2 hay recuperación intramódulo. La recuperación espaciada principal de `c()` y `[]` ocurrirá en módulos posteriores.

### Sintaxis nueva
- `c()` para combinar varios valores dentro de un vector;
- `sum()` como función funcional para sumar todos los valores de un vector;
- `[]` para seleccionar una o varias posiciones.

### Sintaxis que NO se introduce
No se introducen:

- `TRUE`;
- `FALSE`;
- condiciones lógicas;
- `>`;
- `==`;
- `$`;
- data frames;
- pipes;
- `filter()`;
- `select()`.

### Dataset
Microdatos visibles de 3–5 valores. Los contextos son tiempos de viaje, respuestas diarias, horas de estudio y participación semanal. M2 todavía no trabaja con data frames ni introduce formalmente casos, filas, columnas o variables estadísticas.

### Estrategia de scaffolding
1. Worked example completo de `c()` y vector.
2. Producción guiada de un vector nuevo.
3. Worked example + completion con `sum()`.
4. Representación explícita de posiciones antes de introducir `[]`.
5. Integración de `c()` dentro de `[]` para seleccionar varias posiciones.
6. Recuperación integrada con menos apoyo.
7. Transferencia en contexto nuevo sin nombrar las herramientas.

### Estrategia de fading
`OBSERVAR → PRODUCIR → USAR EL VECTOR COMPLETO → COMPRENDER POSICIÓN → SELECCIONAR → RECUPERAR → DECIDIR`

### Riesgos cognitivos
- creer que `c()` suma o resume valores en vez de reunirlos;
- memorizar la palabra “vector” sin comprender que un objeto contiene varios valores;
- ignorar que el orden importa;
- confundir valor con posición;
- creer que R comienza las posiciones en 0;
- confundir `()` con `[]`;
- reconstruir manualmente un resultado en vez de seleccionarlo desde el objeto;
- confundir el `[1]` que R puede mostrar al imprimir resultados con la indexación escrita por el estudiante;
- interpretar `c(2, 5)` dentro de `x[c(2, 5)]` como datos en vez de posiciones.

### Número de ejercicios
7

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M2-E1 | De uno a varios | NOVEDAD | `c()` + objeto con varios valores | `<-`, objeto, consulta | baja-media |
| M2-E2 | Tu primer vector | PRÁCTICA | ninguna | `c()`, `<-`, consulta | baja-media |
| M2-E3 | Usa todos los valores juntos | NOVEDAD FUNCIONAL | `sum()` + modelo mínimo de función | vector, reutilización | baja-media |
| M2-E4 | ¿Qué hay en esta posición? | NOVEDAD | posición + `[]` | vector, orden | media |
| M2-E5 | Más de una posición | PRÁCTICA | ninguna | `c()`, `[]`, orden | media |
| M2-E6 | Vuelve a usar lo aprendido | RECUPERACIÓN / INTEGRACIÓN | ninguna | `<-`, `c()`, `sum()`, `[]` | media |
| M2-E7 | Encuentra la información que piden | TRANSFERENCIA | ninguna | capacidades centrales de M2 | media |

---

## M2-E1 — De uno a varios

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Abre M2 exactamente donde termina M1: hasta ahora cada objeto guardaba un valor, pero una misma característica puede observarse en varias personas. El ejercicio introduce una forma de conservar varios valores relacionados dentro de un solo objeto sin obligar a crear un objeto distinto para cada observación.

### 3. Capacidad antes
Puede crear, consultar y reutilizar objetos que contienen un único valor.

### 4. Capacidad después
Comprende que un objeto puede contener varios valores relacionados y reconoce `c()` como la forma inicial de construir ese conjunto en R.

### 5. Prerrequisitos
- crear un objeto con `<-`;
- consultar un objeto;
- ejecutar código;
- reconocer números.

### 6. Gran novedad
- **Sintaxis nueva:** `c()`.
- **Modelo mental nuevo:** un objeto puede guardar varios valores relacionados y conservar su orden.
- **Decisión nueva:** ninguna importante; el código está trabajado.

La palabra **vector** aparece solo después de que el estudiante haya observado el resultado.

### 7. Recuperaciones
Recupera `<-`, objeto, ejecución y consulta desde M1.

### 8. Contexto sustantivo
Cinco personas informaron cuánto tardaron en viajar a la universidad.

Tiempos, en minutos:

`25, 40, 35, 50, 30`

### 9. Dataset / objetos
Objeto:

`tiempos_viaje`

Valores:

`25, 40, 35, 50, 30`

### 10. Texto para el estudiante
**Situación.** Cinco personas informaron tiempos de viaje de 25, 40, 35, 50 y 30 minutos.

En M1 aprendiste a guardar un valor dentro de un objeto. Aquí queremos guardar **los cinco tiempos juntos**.

Antes de ejecutar, piensa:

> ¿`tiempos_viaje` guardará un solo valor o los cinco?

Observa el código:

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

`c()` combina varios valores para que puedan quedar juntos dentro de un mismo objeto.

Ejecuta esa línea y después consulta:

```r
tiempos_viaje
```

Ahora `tiempos_viaje` contiene cinco valores. En R llamamos **vector** a una estructura como esta.

El orden también queda guardado: 25 está primero, 40 segundo, 35 tercero, y así sucesivamente.

### 11. Modelo mental
`VARIOS VALORES RELACIONADOS → c(...) → UN OBJETO → VECTOR`

### 12. Código trabajado / ejemplo
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
tiempos_viaje
```

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje
```

### 14. Acción esperada
Ejecutar la asignación, consultar el objeto y reconocer que un único objeto contiene los cinco valores en el orden indicado.

### 15. Solución canónica
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
tiempos_viaje
```

### 16. Resultado esperado
`tiempos_viaje` contiene, en este orden:

`25, 40, 35, 50, 30`.

La consola puede mostrar algo como:

```text
[1] 25 40 35 50 30
```

### 17. Criterio semántico de éxito
Comprobar que:

- existe `tiempos_viaje`;
- contiene cinco valores numéricos;
- los valores son 25, 40, 35, 50 y 30;
- el orden coincide exactamente con la situación;
- el estudiante ejecutó y consultó el objeto.

No es necesario exigir producción autónoma de `c()` todavía.

### 18. Estrategias alternativas válidas
Se toleran diferencias de espacios. El nombre `tiempos_viaje`, los cinco valores y su orden forman parte de la tarea. No se exige una cadena textual exacta.

### 19. Error esperado / misconception
- creer que `c()` calcula algo como una suma;
- pensar que el objeto guarda solamente el primer o el último valor;
- tratar el orden como irrelevante;
- confundir el `[1]` impreso por R con uno de los datos.

### 20. Feedback correcto
**Bien.** Antes cada objeto contenía un valor. Ahora `tiempos_viaje` contiene cinco valores relacionados y conserva su orden. A este conjunto ordenado de valores dentro de un objeto lo llamaremos **vector**.

### 21. Feedback resultado correcto / estrategia incorrecta
Si el estudiante reemplaza el ejemplo por varios objetos separados:

> Los valores son correctos, pero siguen separados. La idea nueva de este ejercicio es que los cinco queden juntos dentro de un solo objeto.

Si interpreta `c()` como suma:

> `c()` no suma los valores. Los reúne dentro del mismo objeto.

### 22. Hint 1
No queremos calcular todavía. Queremos conservar los cinco tiempos juntos.

### 23. Hint 2
`c()` permite reunir varios valores dentro del objeto que está a la izquierda de `<-`.

### 24. Hint 3
Usa:

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

y después consulta `tiempos_viaje`.

### 25. Predicción
Sí. Antes de ejecutar:

> ¿`tiempos_viaje` guardará un valor o los cinco?

No pedir predicción del formato exacto de la consola.

### 26. Tipo de ejercicio
Worked example con predicción conceptual.

### 27. Andamiaje
Muy alto: código completo, contexto explícito y explicación inmediata.

### 28. Carga cognitiva
**Baja-media.** El estudiante coordina una sintaxis nueva (`c()`), la idea de varios valores en un solo objeto y el término vector. La tarea no agrega decisiones analíticas.

### 29. Fading
E1 muestra la estructura completa. E2 retirará el código resuelto y exigirá producir el vector.

### 30. Recuperación futura
- E2: producción inmediata de `c()`;
- E5: `c()` reaparece para expresar varias posiciones;
- E6–E7: producción con menos apoyo;
- M3/M5/M11: recuperación posterior según necesidad.

### 31. Riesgo de aprendizaje superficial
Memorizar “vector = algo con `c()`” sin comprender que el objeto contiene varios valores en un orden. El feedback y la explicitación del orden deben priorizar el modelo mental.

### 32. Criterio de transferencia
Más adelante debe reconocer que varios valores relacionados pueden almacenarse en un solo objeto y producir un vector nuevo sin volver a recibir el ejemplo completo.

### 33. Notas de implementación futura
Si la consola muestra `[1]`, incluir un callout discreto:

> `[1]` forma parte de cómo R muestra la salida. No es otro dato y no tienes que escribirlo.

No introducir todavía selección por posición.

---

## M2-E2 — Tu primer vector

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Convierte el reconocimiento de E1 en producción. El estudiante debe recuperar `c()` y `<-` para construir un objeto con varios valores sin recibir la línea completa.

### 3. Capacidad antes
Reconoce que `c()` permite reunir varios valores dentro de un objeto y que el orden se conserva.

### 4. Capacidad después
Puede producir un vector numérico pequeño con un nombre y un orden determinados.

### 5. Prerrequisitos
- `<-`;
- objeto;
- `c()`;
- consulta;
- orden de valores.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** transformar una lista visible de cinco valores en un solo objeto.

### 7. Recuperaciones
Recupera `<-`, consulta y `c()`.

### 8. Contexto sustantivo
Otro grupo de cinco personas informa sus tiempos de viaje.

### 9. Dataset / objetos
Valores, en este orden:

`20, 35, 45, 25, 30`

Objeto requerido:

`tiempos_viaje`

### 10. Texto para el estudiante
**Situación.** Otro grupo informó estos tiempos de viaje, en minutos:

**20, 35, 45, 25 y 30**, en ese orden.

**Tarea.** Crea un objeto llamado `tiempos_viaje` que guarde los cinco valores juntos. Después consulta el objeto para comprobar qué quedó guardado.

### 11. Modelo mental
`VALORES RELACIONADOS + ORDEN → c(...) → VECTOR`

### 12. Código trabajado / ejemplo
El worked example completo ya apareció en E1. No se agrega otro.

### 13. Starter code
```r
# guarda aquí los cinco tiempos en tiempos_viaje
```

### 14. Acción esperada
Producir una asignación con `c()` y consultar el objeto.

### 15. Solución canónica
```r
tiempos_viaje <- c(20, 35, 45, 25, 30)
tiempos_viaje
```

### 16. Resultado esperado
`tiempos_viaje` contiene:

`20, 35, 45, 25, 30`

en ese orden.

### 17. Criterio semántico de éxito
Comprobar que:

- existe `tiempos_viaje`;
- contiene cinco valores numéricos;
- los valores son correctos;
- el orden es exactamente `20, 35, 45, 25, 30`;
- la construcción utiliza `c()`.

No basta con crear cinco objetos separados.

### 18. Estrategias alternativas válidas
Se toleran espacios y saltos de línea diferentes. No se acepta un orden distinto aunque el conjunto de números sea el mismo, porque el orden será relevante para la selección posterior.

### 19. Error esperado / misconception
- crear `tiempo_1`, `tiempo_2`, etc.;
- alterar el orden;
- olvidar `c()`;
- escribir únicamente los cinco números sin asignarlos a `tiempos_viaje`.

### 20. Feedback correcto
**Bien.** Creaste un solo objeto que contiene los cinco tiempos y mantuviste su orden. Ya no necesitas un objeto diferente para cada observación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si crea varios objetos:

> Los cinco valores están presentes, pero siguen separados. La habilidad de este ejercicio es guardarlos juntos dentro de `tiempos_viaje`.

Si usa el orden incorrecto:

> Están los mismos números, pero cambiaste su orden. En un vector la posición depende del orden en que guardas los valores.

### 22. Hint 1
Piensa en la estructura que permitió guardar cinco valores juntos en E1.

### 23. Hint 2
El objeto debe llamarse `tiempos_viaje` y a la derecha de `<-` necesitas `c(...)`.

### 24. Hint 3
```r
tiempos_viaje <- c(20, 35, 45, 25, 30)
```

Después consulta `tiempos_viaje`.

### 25. Predicción
No necesaria.

### 26. Tipo de ejercicio
Completion / producción guiada.

### 27. Andamiaje
Alto: se entregan nombre, datos y orden, pero no la asignación.

### 28. Carga cognitiva
**Baja-media.** No aparece sintaxis nueva. El esfuerzo está en recuperar `c()` y producir la estructura correcta respetando el orden.

### 29. Fading
Retira el código completo de E1. E3 volverá a entregar un vector ya construido para introducir una herramienta funcional sin añadir una segunda exigencia de producción.

### 30. Recuperación futura
`c()` reaparece en E5, E6 y E7.

### 31. Riesgo de aprendizaje superficial
Copiar mentalmente la forma de E1 sin comprender por qué un solo objeto es preferible. El feedback sobre varios objetos separados ataca este riesgo.

### 32. Criterio de transferencia
Debe poder crear posteriormente otro vector con nombre, valores y contexto diferentes.

### 33. Notas de implementación futura
El grader debe inspeccionar la estructura semántica y el estado del objeto, no comparar texto literal. El orden forma parte del éxito.

---

## M2-E3 — Usa todos los valores juntos

### 1. Rol pedagógico
NOVEDAD FUNCIONAL.

### 2. Por qué existe
Demuestra que un vector no solo almacena varios valores: el objeto completo puede reutilizarse dentro de una operación. Recupera la idea de reutilización de M1 sin desviar el núcleo del módulo hacia funciones estadísticas.

### 3. Capacidad antes
Puede crear y consultar un vector numérico.

### 4. Capacidad después
Puede usar un vector completo como entrada de una función sencilla y guardar el resultado.

### 5. Prerrequisitos
- objeto;
- reutilización;
- vector;
- `c()`;
- `<-`.

### 6. Gran novedad
- **Sintaxis nueva:** `sum()`.
- **Modelo funcional nuevo:** una función puede recibir un objeto completo entre paréntesis.
- **Decisión nueva:** mínima; la función se muestra antes de pedir producción.

`sum()` es una habilidad funcional secundaria.

### 7. Recuperaciones
Recupera vector, objeto, `<-` y reutilización de objetos.

### 8. Contexto sustantivo
Cantidad de respuestas recibidas durante cinco días.

### 9. Dataset / objetos
```r
respuestas_diarias <- c(18, 22, 15, 25, 20)
```

Objeto nuevo:

`total_respuestas`

### 10. Texto para el estudiante
**Situación.** `respuestas_diarias` guarda la cantidad de respuestas recibidas durante cinco días:

```r
respuestas_diarias <- c(18, 22, 15, 25, 20)
```

Ahora queremos sumar **todos los valores del vector**.

Observa:

```r
sum(respuestas_diarias)
```

`sum()` suma todos los valores contenidos en el objeto.

`c()` y `sum()` son funciones de R. Por ahora basta con reconocer este patrón: una función se escribe con su nombre seguido de paréntesis, y dentro colocamos la información que necesita.

**Tarea.** Guarda el resultado de `sum(respuestas_diarias)` en un objeto llamado `total_respuestas`. Después consúltalo.

### 11. Modelo mental
`VECTOR COMPLETO → FUNCIÓN → RESULTADO`

### 12. Código trabajado / ejemplo
```r
respuestas_diarias <- c(18, 22, 15, 25, 20)
sum(respuestas_diarias)
```

### 13. Starter code
```r
respuestas_diarias <- c(18, 22, 15, 25, 20)

# guarda la suma completa en total_respuestas
```

### 14. Acción esperada
Crear `total_respuestas` mediante `sum(respuestas_diarias)` y consultarlo.

### 15. Solución canónica
```r
respuestas_diarias <- c(18, 22, 15, 25, 20)

total_respuestas <- sum(respuestas_diarias)
total_respuestas
```

### 16. Resultado esperado
`100`.

### 17. Criterio semántico de éxito
Comprobar que:

- existe `respuestas_diarias` con los cinco valores correctos;
- existe `total_respuestas`;
- `total_respuestas == 100`;
- el resultado depende de `respuestas_diarias`;
- la operación utiliza `sum()` sobre el objeto.

No aceptar como dominio:

```r
total_respuestas <- 100
```

ni:

```r
total_respuestas <- 18 + 22 + 15 + 25 + 20
```

### 18. Estrategias alternativas válidas
Se aceptan diferencias de espacios y orden de ejecución siempre que `total_respuestas` sea producido mediante `sum(respuestas_diarias)`. Para esta actividad, otras formas de sumar no demuestran la construcción objetivo.

### 19. Error esperado / misconception
- hardcodear `100`;
- volver a escribir los cinco valores;
- creer que `sum()` crea un vector nuevo;
- olvidar que puede pasar el nombre del objeto dentro de la función.

### 20. Feedback correcto
**Bien.** Reutilizaste el vector completo dentro de una función. No tuviste que volver a escribir los cinco valores: `sum()` trabajó directamente con `respuestas_diarias`.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `100`:

> El total es correcto, pero lo escribiste directamente. Queremos que el resultado dependa del objeto `respuestas_diarias`.

Si vuelve a escribir los cinco números:

> La suma da lo mismo, pero estás repitiendo datos que ya están guardados. Usa el objeto completo dentro de `sum()`.

### 22. Hint 1
Los cinco valores ya están guardados en `respuestas_diarias`. No necesitas escribirlos otra vez.

### 23. Hint 2
La función que acabas de ver se usa como `sum(objeto)`.

### 24. Hint 3
```r
total_respuestas <- sum(respuestas_diarias)
total_respuestas
```

### 25. Predicción
No es necesaria como paso separado. El foco está en reutilizar el vector completo.

### 26. Tipo de ejercicio
Worked example + completion.

### 27. Andamiaje
Alto: se muestra `sum()` y después se pide incorporarlo a una asignación.

### 28. Carga cognitiva
**Baja-media.** Se introduce una función nueva y un modelo mínimo de `funcion(objeto)`, pero el vector ya está creado y la decisión sustantiva es simple.

### 29. Fading
La función se muestra antes de pedir producción. E4 cambia de eje y concentra el esfuerzo en posición/selección, evitando acumular dos novedades grandes.

### 30. Recuperación futura
E6 y E7 recuperan `sum()` con menos apoyo. Puede requerir una pista breve después de varios días.

### 31. Riesgo de aprendizaje superficial
Memorizar `sum()` como receta aislada. El texto debe enfatizar que la idea importante es reutilizar el objeto completo.

### 32. Criterio de transferencia
Más adelante debe reconocer que un vector puede entregarse completo a una función conocida, aunque pueda necesitar recordar el nombre exacto de la función.

### 33. Notas de implementación futura
El grader debe distinguir valor y estrategia. Un perturbation test puede cambiar los valores de `respuestas_diarias` y comprobar que `total_respuestas` se actualiza al reejecutar.

---

## M2-E4 — ¿Qué hay en esta posición?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce la idea de posición y la selección con corchetes. Es el núcleo conceptual que permitirá posteriormente pasar de seleccionar “porque sé dónde está” a seleccionar “porque cumple una condición”.

### 3. Capacidad antes
Puede crear un vector, reconocer su orden y usar el vector completo.

### 4. Capacidad después
Comprende qué significa una posición y puede recuperar un valor concreto desde un vector mediante `[]`.

### 5. Prerrequisitos
- vector;
- orden;
- consulta de objetos;
- ejecución.

### 6. Gran novedad
- **Sintaxis nueva:** `[]`.
- **Concepto nuevo:** posición.
- **Decisión nueva:** identificar qué posición corresponde al valor solicitado.

El concepto de posición debe construirse visualmente antes de mostrar `[]`.

### 7. Recuperaciones
Recupera `c()`, vector y orden.

### 8. Contexto sustantivo
Tiempos de viaje:

`25, 40, 35, 50, 30`

### 9. Dataset / objetos
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

Representación conceptual:

```text
posición        1    2    3    4    5
tiempo         25   40   35   50   30
```

### 10. Texto para el estudiante
**Situación.** `tiempos_viaje` contiene cinco valores:

```text
posición        1    2    3    4    5
tiempo         25   40   35   50   30
```

Antes de escribir código:

> ¿Qué valor está en la posición 3?

La respuesta es `35`.

En R, la primera posición es **1**.

Ahora observa:

```r
tiempos_viaje[3]
```

Los corchetes permiten seleccionar desde un objeto. El número dentro de los corchetes indica la **posición** que queremos recuperar.

`tiempos_viaje[3]` no significa “busca el número 3”. Significa:

> dame el valor que está en la posición 3.

Antes de ejecutar, predice qué valor aparecerá.

### 11. Modelo mental
`OBJETO + POSICIÓN → VALOR SELECCIONADO`

### 12. Código trabajado / ejemplo
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
tiempos_viaje[3]
```

Contraste mínimo:

```text
c(...)
sum(...)
```

usan paréntesis porque son funciones.

```r
tiempos_viaje[3]
```

usa corchetes para seleccionar una parte del objeto.

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje[3]
```

### 14. Acción esperada
Identificar conceptualmente la tercera posición, predecir `35`, ejecutar `tiempos_viaje[3]` y observar el resultado.

### 15. Solución canónica
```r
tiempos_viaje[3]
```

### 16. Resultado esperado
`35`.

R puede imprimir:

```text
[1] 35
```

Ese `[1]` pertenece al formato de salida de R y no significa que se haya seleccionado la posición 1.

### 17. Criterio semántico de éxito
Comprobar que:

- `tiempos_viaje` existe;
- la selección depende del objeto;
- se utiliza la posición 3;
- el resultado es `35`;
- no se hardcodea `35`.

Un perturbation test puede cambiar el tercer valor y verificar que la misma estrategia recupera el nuevo tercer elemento.

### 18. Estrategias alternativas válidas
La forma pedagógicamente válida debe seleccionar desde `tiempos_viaje`. No se exige formato textual exacto, pero el índice debe representar la tercera posición.

### 19. Error esperado / misconception
- `tiempos_viaje(3)`;
- `tiempos_viaje[0]`;
- `tiempos_viaje[35]`;
- escribir `35`;
- interpretar `[1] 35` como si R hubiese seleccionado la posición 1.

### 20. Feedback correcto
**Bien.** Usaste una posición para recuperar un valor desde el vector. El `3` dentro de los corchetes significa “tercera posición”, no “valor 3”.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `35`:

> Encontraste el dato correcto, pero lo escribiste directamente. Queremos recuperarlo desde `tiempos_viaje`.

Si usa `tiempos_viaje(3)`:

> Usaste paréntesis. Los paréntesis aparecen en funciones como `c()` y `sum()`. Para seleccionar una posición desde un objeto usamos corchetes.

Si usa `[0]`:

> En R, la primera posición es 1.

Si usa `[35]`:

> Dentro de los corchetes debes indicar **dónde está** el valor, no escribir el valor que esperas encontrar.

### 22. Hint 1
Primero identifica dónde está el dato: ¿qué valor ocupa la tercera posición?

### 23. Hint 2
Para seleccionar una posición, escribe el nombre del objeto seguido de corchetes.

### 24. Hint 3
```r
tiempos_viaje[3]
```

### 25. Predicción
Sí. Antes de ejecutar `tiempos_viaje[3]`:

> ¿Qué valor esperas obtener?

### 26. Tipo de ejercicio
Representación conceptual + worked example.

### 27. Andamiaje
Alto: la posición se hace visible antes de introducir la sintaxis y se entrega el primer ejemplo completo.

### 28. Carga cognitiva
**Media.** Están activos vector, orden, posición, `[]`, distinción `()`/`[]` y la interpretación del output. La carga se controla separando primero la posición conceptual y después la sintaxis.

### 29. Fading
E4 muestra la selección completa. E5 retirará parte del apoyo y exigirá construir una selección múltiple.

### 30. Recuperación futura
- E5: selección de varias posiciones;
- E6–E7: uso sin explicación completa;
- M3: `[]` se reutiliza con condiciones;
- M5: subsetting como antecedente conceptual del filtrado.

### 31. Riesgo de aprendizaje superficial
Memorizar `x[3]` como patrón sin comprender posición. La representación visual y los errores `[35]`/`35` deben hacer explícita la diferencia entre valor y ubicación.

### 32. Criterio de transferencia
Debe poder seleccionar posteriormente otra posición de otro vector sin que la consigna vuelva a explicar qué significan los corchetes.

### 33. Notas de implementación futura
Incluir un callout breve:

> Si R muestra `[1] 35`, ese `[1]` pertenece a la forma en que R imprime la respuesta. No tienes que escribirlo y no cambia la posición que pediste.

No anticipar condiciones lógicas.

---

## M2-E5 — Más de una posición

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Extiende la selección de una posición a varias y obliga a reutilizar `c()` dentro de `[]`. Es una oportunidad de interleaving: una construcción conocida (`c()`) adquiere una nueva función contextual.

### 3. Capacidad antes
Puede crear vectores y seleccionar un único valor por posición.

### 4. Capacidad después
Puede seleccionar varias posiciones desde un vector y comprender que `c(2, 5)` representa posiciones cuando aparece dentro de los corchetes.

### 5. Prerrequisitos
- `c()`;
- orden;
- posición;
- `[]`.

### 6. Gran novedad
No hay sintaxis completamente nueva. La dificultad proviene de combinar dos construcciones ya conocidas:

```r
tiempos_viaje[c(2, 5)]
```

### 7. Recuperaciones
Recupera `c()` y `[]`.

### 8. Contexto sustantivo
Del mismo vector de tiempos, queremos recuperar los valores registrados en las posiciones 2 y 5.

### 9. Dataset / objetos
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
```

### 10. Texto para el estudiante
**Situación.** Queremos recuperar dos valores de `tiempos_viaje`: los que están en las posiciones **2 y 5**.

Antes de ejecutar, usa el orden para responder:

> ¿Qué dos valores deberían aparecer?

Respuesta esperada: `40` y `30`.

Observa que `c()` puede reunir números con distintos significados según el contexto.

En:

```r
c(25, 40, 35)
```

los números son datos.

En:

```r
tiempos_viaje[c(2, 5)]
```

`c(2, 5)` indica las posiciones que queremos seleccionar.

Puede leerse así:

```text
tiempos_viaje [ c(2, 5) ]
       │          │
       │          └─ posiciones que quiero
       └──────────── objeto del que selecciono
```

### 11. Modelo mental
`OBJETO + VARIAS POSICIONES → VARIOS VALORES SELECCIONADOS`

### 12. Código trabajado / ejemplo
El ejemplo conceptual de E4 proporciona `objeto[posicion]`. E5 transforma la posición única en un pequeño vector de posiciones.

### 13. Starter code
```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# selecciona las posiciones 2 y 5
```

### 14. Acción esperada
Construir y ejecutar una selección múltiple desde `tiempos_viaje`.

### 15. Solución canónica
```r
tiempos_viaje[c(2, 5)]
```

### 16. Resultado esperado
`40, 30`, en ese orden.

### 17. Criterio semántico de éxito
Comprobar que:

- la selección parte de `tiempos_viaje`;
- las posiciones solicitadas son 2 y 5;
- el resultado contiene `40` y `30` en ese orden;
- se usa una estructura equivalente a selección múltiple desde el vector;
- no se reconstruyen manualmente los valores.

Un perturbation test puede cambiar los valores en posiciones 2 y 5 y comprobar que la selección sigue funcionando.

### 18. Estrategias alternativas válidas
Se toleran diferencias de espacios. Para la capacidad objetivo, `c(2, 5)` y la selección desde el objeto son obligatorias conceptualmente. No se acepta `c(40, 30)` como estrategia equivalente.

### 19. Error esperado / misconception
- `tiempos_viaje[2, 5]`;
- `tiempos_viaje[c(40, 30)]`;
- `c(40, 30)`;
- confundir valores con posiciones;
- invertir las posiciones y alterar el orden solicitado.

### 20. Feedback correcto
**Bien.** Reuniste las posiciones 2 y 5 con `c()` y después las usaste para seleccionar desde `tiempos_viaje`. Aquí `c(2, 5)` representa posiciones, no tiempos de viaje.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa `c(40, 30)`:

> Los valores son correctos, pero los reconstruiste manualmente. Queremos recuperarlos desde `tiempos_viaje`.

Si usa `tiempos_viaje[2, 5]`:

> Para seleccionar varias posiciones dentro de este vector, reúne primero las posiciones con `c()`.

Si usa `tiempos_viaje[c(40, 30)]`:

> Dentro de `c()` deben ir las posiciones que quieres recuperar, no los valores esperados.

### 22. Hint 1
Piensa primero en **dónde** están los dos valores, no en cuáles son.

### 23. Hint 2
Necesitas reunir las posiciones 2 y 5 y colocar ese conjunto dentro de los corchetes.

### 24. Hint 3
```r
tiempos_viaje[c(2, 5)]
```

### 25. Predicción
Sí. Antes de ejecutar:

> Si seleccionamos las posiciones 2 y 5, ¿qué valores deberían aparecer?

### 26. Tipo de ejercicio
Completion / integración de construcciones.

### 27. Andamiaje
Medio: el vector y las posiciones están dados, pero la expresión debe producirse.

### 28. Carga cognitiva
**Media.** La principal dificultad es interpretar una expresión anidada y distinguir datos de posiciones. No aparece sintaxis nueva.

### 29. Fading
Se retira el worked example completo de E4. E6 quitará además las funciones nombradas explícitamente.

### 30. Recuperación futura
E6–E7 recuperan selección; M3 reutilizará `[]` para una lógica distinta.

### 31. Riesgo de aprendizaje superficial
Aprender de memoria `x[c(...)]` sin comprender qué representan los números interiores. La explicación datos vs posiciones debe ser obligatoria.

### 32. Criterio de transferencia
Debe poder seleccionar más adelante otra combinación de posiciones en un vector distinto.

### 33. Notas de implementación futura
El feedback debe identificar específicamente si el estudiante entregó los valores en vez de las posiciones. No comparar únicamente el resultado final.

---

## M2-E6 — Vuelve a usar lo aprendido

### 1. Rol pedagógico
RECUPERACIÓN / INTEGRACIÓN.

### 2. Por qué existe
Comprueba si el estudiante puede recuperar la secuencia construida en M2 dentro de un nuevo contexto sin que el starter le entregue el vector ya resuelto.

### 3. Capacidad antes
Puede crear vectores, usar un vector completo con `sum()` y seleccionar posiciones con `[]`.

### 4. Capacidad después
Puede recuperar e integrar `<-`, `c()`, `sum()` y `[]` con apoyo reducido.

### 5. Prerrequisitos
Todo M2-E1 a M2-E5 y las capacidades de objetos provenientes de M1.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** recordar qué herramienta conocida corresponde a cada subtarea.

### 7. Recuperaciones
Recuperación intramódulo de:

- `<-`;
- `c()`;
- `sum()`;
- posición;
- `[]`.

No se clasifica como práctica espaciada.

### 8. Contexto sustantivo
Cinco estudiantes informaron cuántas horas estudiaron el día anterior.

### 9. Dataset / objetos
Valores:

`2, 4, 3, 5, 1`

Objeto:

`horas_estudio`

Resultados requeridos:

- `total = 15`;
- `cuarta = 5`.

### 10. Texto para el estudiante
**Situación.** Cinco estudiantes informaron que estudiaron:

**2, 4, 3, 5 y 1 horas**, en ese orden.

Sin volver a los ejemplos anteriores si no es necesario:

1. guarda los cinco valores juntos en un objeto llamado `horas_estudio`;
2. crea `total` con la suma de todos los valores guardados;
3. crea `cuarta` recuperando la cuarta observación desde `horas_estudio`.

Intenta resolver primero sin abrir pistas.

### 11. Modelo mental
`DATOS → VECTOR → USAR TODO / SELECCIONAR UNA PARTE`

### 12. Código trabajado / ejemplo
No se añade código trabajado. La función del ejercicio es recuperar.

### 13. Starter code
```r
# guarda los cinco valores en horas_estudio


# calcula el total


# recupera la cuarta observación
```

### 14. Acción esperada
Construir el vector, sumar sus valores y seleccionar la cuarta posición.

### 15. Solución canónica
```r
horas_estudio <- c(2, 4, 3, 5, 1)
total <- sum(horas_estudio)
cuarta <- horas_estudio[4]
```

### 16. Resultado esperado
- `horas_estudio`: `2, 4, 3, 5, 1`;
- `total`: `15`;
- `cuarta`: `5`.

### 17. Criterio semántico de éxito
Comprobar que:

- `horas_estudio` existe, es numérico y mantiene el orden;
- se construye como vector mediante `c()`;
- `total == 15` y depende de `sum(horas_estudio)`;
- `cuarta == 5` y depende de la selección de la posición 4;
- no se hardcodean `15` ni `5`.

Un perturbation test puede modificar los datos y verificar que las relaciones se mantienen.

### 18. Estrategias alternativas válidas
Se toleran espacios y orden de líneas cuando no altera dependencias. Los nombres `horas_estudio`, `total` y `cuarta` son requeridos para simplificar el contrato del grader.

### 19. Error esperado / misconception
- crear el vector incorrectamente;
- `total <- 15`;
- `cuarta <- 5`;
- reconstruir la suma con literales;
- seleccionar por valor en vez de por posición;
- olvidar que la cuarta posición es 5.

### 20. Feedback correcto
**Bien.** Recuperaste varias ideas sin que la consigna nombrara directamente cada herramienta: construiste un vector, usaste todos sus valores y recuperaste una posición concreta.

### 21. Feedback resultado correcto / estrategia incorrecta
Si `total` está hardcodeado:

> El total coincide, pero debe depender de `horas_estudio`, no de un número escrito manualmente.

Si `cuarta` está hardcodeada:

> El valor es correcto, pero queremos recuperarlo desde la cuarta posición de `horas_estudio`.

Si el vector está mal ordenado:

> Los valores están, pero el orden cambió. La cuarta posición solo tiene sentido si conservas el orden original.

### 22. Hint 1
Divide el problema en tres decisiones: primero guardar juntos, después usar todos, después recuperar una posición.

### 23. Hint 2
Para el primer paso necesitas la construcción de vectores; para el total, la función vista en E3; para la cuarta observación, los corchetes.

### 24. Hint 3
```r
horas_estudio <- c(2, 4, 3, 5, 1)
total <- sum(horas_estudio)
cuarta <- horas_estudio[4]
```

### 25. Predicción
No como paso separado. La carga ya está en recuperar tres construcciones conocidas.

### 26. Tipo de ejercicio
Recuperación integrada.

### 27. Andamiaje
Medio-bajo: solo hay comentarios estructurales; no se nombran `c()`, `sum()` ni `[]` en el starter.

### 28. Carga cognitiva
**Media.** Coordina cuatro construcciones conocidas y tres productos relacionados. No añade sintaxis nueva.

### 29. Fading
E6 elimina los ejemplos y exige recuperar las herramientas. E7 retirará además la división tan explícita entre operaciones y cambiará de contexto.

### 30. Recuperación futura
La recuperación espaciada real deberá ocurrir en M3, M5 y módulos posteriores.

### 31. Riesgo de aprendizaje superficial
Resolver a partir de memoria inmediata de E5. El cambio de contexto y la ausencia de sintaxis en el starter reducen ese riesgo, pero no lo convierten en spaced retrieval.

### 32. Criterio de transferencia
Debe poder reconstruir el mismo tipo de flujo con otros datos y nombres sin consultar instrucciones completas.

### 33. Notas de implementación futura
Las pistas deben estar cerradas al inicio. Registrar si el estudiante llega a la solución sin pistas puede ser útil para analítica formativa, pero no debe alterar el criterio de aprobación.

---

## M2-E7 — Encuentra la información que piden

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
Cierra M2 con un contexto nuevo en el que el estudiante debe decidir cuándo guardar varios valores, cuándo trabajar con el vector completo y cuándo seleccionar posiciones, sin que la consigna nombre las herramientas.

### 3. Capacidad antes
Puede recuperar las construcciones centrales de M2 con apoyo estructural.

### 4. Capacidad después
Puede decidir de forma relativamente autónoma cómo construir y usar un vector para responder preguntas simples sobre todos sus valores o sobre posiciones específicas.

### 5. Prerrequisitos
Todo M2.

### 6. Gran novedad
No hay sintaxis nueva. La novedad está en la decisión: la consigna formula preguntas sustantivas y el estudiante selecciona la estrategia.

### 7. Recuperaciones
Recupera:

- `<-`;
- `c()`;
- vector;
- orden;
- `sum()`;
- posición;
- selección múltiple.

### 8. Contexto sustantivo
Durante cinco semanas se registró la cantidad de participaciones de un grupo.

### 9. Dataset / objetos
Valores semanales:

`3, 1, 4, 2, 5`

Objeto requerido:

`participacion`

Objetos derivados:

- `total`;
- `seleccion`.

### 10. Texto para el estudiante
**Situación.** Durante cinco semanas se registraron estas cantidades de participaciones:

**3, 1, 4, 2 y 5**, en ese orden.

**Tarea.** Escribe código para:

1. guardar los cinco valores juntos en un objeto llamado `participacion`;
2. responder cuántas participaciones hubo en total;
3. recuperar cuántas participaciones se registraron en las semanas 2 y 5.

Guarda el total en `total` y los dos valores seleccionados en `seleccion`.

No se indica qué herramientas debes usar. Decide a partir de lo que ya sabes.

### 11. Modelo mental
`PREGUNTA → ¿NECESITO TODO EL VECTOR O SOLO ALGUNAS POSICIONES? → ELEGIR ESTRATEGIA`

### 12. Código trabajado / ejemplo
No hay worked example. Es una actividad de transferencia cercana.

### 13. Starter code
```r
# guarda los datos


# responde las dos preguntas
```

### 14. Acción esperada
Crear el vector, calcular el total y seleccionar las posiciones 2 y 5.

### 15. Solución canónica
```r
participacion <- c(3, 1, 4, 2, 5)
total <- sum(participacion)
seleccion <- participacion[c(2, 5)]
```

### 16. Resultado esperado
- `participacion`: `3, 1, 4, 2, 5`;
- `total`: `15`;
- `seleccion`: `1, 5`.

### 17. Criterio semántico de éxito
Comprobar por separado:

**Construcción**
- existe `participacion`;
- contiene cinco números;
- conserva el orden;
- fue construido como vector.

**Total**
- `total == 15`;
- depende del objeto `participacion`;
- utiliza una estrategia equivalente a `sum(participacion)` para esta tarea.

**Selección**
- `seleccion` contiene `1, 5`;
- depende de `participacion`;
- selecciona las posiciones 2 y 5;
- no reconstruye manualmente `c(1, 5)`.

Un perturbation test puede cambiar los valores del vector manteniendo las posiciones y verificar que `total` y `seleccion` se actualicen al reejecutar.

### 18. Estrategias alternativas válidas
Pueden variar espacios y orden de algunas líneas siempre que se respeten las dependencias. No se exige coincidencia textual exacta.

### 19. Error esperado / misconception
- crear varios objetos en vez de un vector;
- alterar el orden;
- hardcodear `15`;
- hardcodear `c(1, 5)`;
- seleccionar valores en vez de posiciones;
- necesitar que la consigna nombre explícitamente `c()`, `sum()` o `[]`.

### 20. Feedback correcto
**Bien.** Decidiste cuándo trabajar con todos los valores y cuándo recuperar posiciones específicas. Construiste y usaste un vector sin que la consigna nombrara las herramientas.

Cierre conceptual:

> Hasta ahora pudiste encontrar valores cuando sabías **en qué posición estaban**.
>
> Pero ¿qué pasa si no conoces la posición y solo sabes qué característica buscas?
>
> Por ejemplo: “los tiempos mayores que 30”.

### 21. Feedback resultado correcto / estrategia incorrecta
Si `total` está hardcodeado:

> El total coincide, pero debe calcularse a partir de `participacion`.

Si `seleccion` es `c(1, 5)`:

> Esos son los valores correctos, pero los escribiste directamente. Queremos recuperarlos desde las posiciones 2 y 5 del objeto.

Si crea cinco objetos separados:

> Los datos están, pero perdiste la idea central de M2: varios valores relacionados deben quedar juntos dentro de un mismo objeto.

### 22. Hint 1
Para cada pregunta, decide primero si necesitas trabajar con **todos los valores** o con **posiciones concretas**.

### 23. Hint 2
Primero necesitas crear `participacion`. Después una pregunta usa el vector completo y la otra pide las posiciones 2 y 5.

### 24. Hint 3
```r
participacion <- c(3, 1, 4, 2, 5)
total <- sum(participacion)
seleccion <- participacion[c(2, 5)]
```

### 25. Predicción
No necesaria como paso independiente.

### 26. Tipo de ejercicio
Transferencia cercana.

### 27. Andamiaje
Bajo para el nivel del módulo: contexto, nombres de objetos y preguntas; sin sintaxis indicada.

### 28. Carga cognitiva
**Media.** Integra construcción, orden, uso completo y selección múltiple, pero todo el contenido sintáctico ya apareció.

### 29. Fading
Es el punto final del fading de M2. La consigna deja de nombrar herramientas y exige elegirlas.

### 30. Recuperación futura
M3 debe recuperar `c()`, vector, posición y `[]` como prerrequisitos. M5 y M11 vuelven a utilizar construcciones de selección y combinación.

### 31. Riesgo de aprendizaje superficial
La principal amenaza es resolver por memoria de la secuencia inmediatamente anterior. El contexto y los valores cambian, y el grader debe proteger contra hardcoding.

### 32. Criterio de transferencia
El estudiante demuestra transferencia si puede construir un vector nuevo, decidir trabajar con todo el objeto o seleccionar posiciones y producir resultados dependientes de los datos.

### 33. Notas de implementación futura
No mostrar `>`, `TRUE`, `FALSE` ni selección lógica. El cierre conceptual debe generar la necesidad de M3 sin resolverla.

---

# Cierre conceptual de M2 y puente a M3

Mostrar después de completar E7:

> Hasta ahora pudiste encontrar valores cuando sabías **en qué posición estaban**.
>
> Pero ¿qué pasa si no conoces la posición y solo sabes qué característica buscas?
>
> Por ejemplo:
>
> “los tiempos mayores que 30”.

La transición termina ahí.

M2 NO debe mostrar todavía:

```r
>
```

ni:

```r
TRUE
FALSE
```

ni:

```r
x[x > 30]
```

Esas construcciones pertenecen a M3.

# Retención esperada después de una semana

## Reconocimiento
El estudiante debería reconocer:

```r
c(...)
```

como construcción de varios valores dentro de un objeto y:

```r
x[3]
```

como selección de la tercera posición.

## Producción
Con poca o ninguna ayuda debería poder producir:

```r
x <- c(...)
x[2]
```

## Elección
Ante una consigna como:

> recupera la cuarta observación

debería decidir seleccionar desde el objeto en vez de hardcodear el valor.

## Habilidad funcional
`sum()` puede requerir una pista breve sobre el nombre de la función. No se exige el mismo nivel de autonomía que para `c()` y `[]`.

# Declaración de lock

M2 queda pedagógicamente cerrado con 7 ejercicios.

- **Sintaxis introducida:** `c()`, `sum()`, `[]`.
- **Habilidades nucleares:** vector, varios valores en un objeto, orden, posición, selección simple y múltiple.
- **Habilidad funcional secundaria:** `sum()`.
- **Habilidades recuperadas:** `<-`, objetos, consulta, reutilización y ejecución.
- **Recuperación futura:** M3, M5, M11 y posteriormente M13.
- **Puente a M3:** selección por posición → necesidad de seleccionar por una pregunta o condición.

# M2 PEDAGOGICALLY LOCKED
