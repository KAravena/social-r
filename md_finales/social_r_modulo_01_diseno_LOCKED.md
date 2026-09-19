# Social R — Módulo 1
## Empezar a pensar con R

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
No ha usado R ni distingue todavía entre escribir código, ejecutarlo y observar un resultado.

### Capacidad después
Puede ejecutar instrucciones sencillas, guardar valores en objetos, consultarlos y reutilizarlos en un cálculo nuevo.

### Pregunta central
¿Cómo puedo darle instrucciones a R y guardar información para volver a usarla?

### Modelo mental
`INSTRUCCIÓN → EJECUCIÓN → RESULTADO → OBJETO → CONSULTA → REUTILIZACIÓN`

### Habilidades nucleares
Al terminar el módulo, el estudiante debe poder producir y no solo reconocer las siguientes acciones:

- ejecutar una instrucción sencilla y localizar su resultado;
- modificar código existente y volver a ejecutarlo;
- crear un objeto con `<-`;
- consultar un objeto escribiendo su nombre;
- reutilizar objetos dentro de una operación nueva;
- distinguir, en situaciones simples, un número de un texto escrito entre comillas;
- usar un error sencillo como pista para corregir una representación incorrecta.

La asignación con `<-`, la consulta y la reutilización no se consideran consolidadas por aparecer una vez: deben recuperarse desde M2 en adelante.

### Habilidades recuperadas
M1 no presupone conocimientos previos de R. La recuperación comienza dentro del propio módulo a partir de M1-E2. M1-E7 constituye recuperación **inmediata/intramódulo**, no práctica espaciada. La recuperación espaciada principal de objetos, asignación, consulta y reutilización ocurre en módulos posteriores.

### Sintaxis nueva
- `+` como operación deliberadamente familiar para aprender a ejecutar código;
- `<-` para asignar un valor a un objeto;
- comillas dobles para representar texto.

### Sintaxis que NO se introduce
No se introducen `c()`, `[]`, `$`, pipes, data frames, funciones estadísticas, `class()`, `typeof()` ni condiciones lógicas como contenido formal. `TRUE` y `FALSE` se posponen para M3, donde aparecerán con significado al responder comparaciones.

### Dataset
No se utiliza todavía una base tabular. Se trabaja con microdatos visibles y estables: conteos pequeños de respuestas de encuestas, un nombre de estudio y una edad. Los valores exactos están fijados dentro de cada ejercicio para que la implementación y el grading sean deterministas.

### Estrategia de scaffolding
El apoyo comienza al máximo y disminuye de forma identificable:

1. código completo para ejecutar;
2. código completo para modificar;
3. worked example de asignación y consulta;
4. completion problem;
5. producción guiada con objetos ya creados;
6. producción con una nueva representación;
7. debugging guiado;
8. integración con comentarios estructurales pero sin asignaciones resueltas.

### Estrategia de fading
`EJECUTAR → MODIFICAR → OBSERVAR ASIGNACIÓN → COMPLETAR → PRODUCIR → DISTINGUIR REPRESENTACIONES → DEPURAR → INTEGRAR`

### Riesgos cognitivos
- confundir escribir código con ejecutarlo;
- creer que asignar un valor debe mostrarlo automáticamente;
- confundir el nombre de un objeto con su contenido;
- hardcodear un resultado correcto sin reutilizar los objetos requeridos;
- tratar un número escrito entre comillas como si siguiera siendo una cantidad numérica;
- interpretar un mensaje de error como fracaso en vez de como información utilizable.

### Número de ejercicios
8

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M1-E1 | Tu primera instrucción | NOVEDAD | ejecutar código y localizar un resultado | ninguna | baja |
| M1-E2 | Cambia la respuesta | PRÁCTICA | ninguna | ejecución inmediata | baja |
| M1-E3 | Guardar para después | NOVEDAD | `<-` + modelo guardar ≠ mostrar | ejecución | baja-media |
| M1-E4 | Crea un objeto tú | PRÁCTICA | ninguna | asignación y consulta | baja-media |
| M1-E5 | Reutiliza lo guardado | PRÁCTICA | ninguna | objetos, asignación y `+` | media |
| M1-E6 | Número o texto | NOVEDAD | comillas para representar texto | asignación y consulta | baja-media |
| M1-E7 | Lee el error antes de corregir | RECUPERACIÓN | ninguna | número/texto + reutilización | media |
| M1-E8 | Encuesta piloto | INTEGRACIÓN | ninguna | habilidades centrales de M1 | media |

---

## M1-E1 — Tu primera instrucción

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Es la primera interacción con R. Debe enseñar una sola idea operacional: el código escrito no hace nada hasta que se ejecuta, y al ejecutarlo R produce un resultado que puede observarse. La suma se usa porque es familiar y no debe competir por atención con la nueva acción de ejecutar.

### 3. Capacidad antes
No ha usado R ni distingue todavía entre escribir código, ejecutarlo y observar un resultado.

### 4. Capacidad después
Puede ejecutar una instrucción sencilla con Ctrl + Enter y localizar el resultado producido por R.

### 5. Prerrequisitos
Ninguno de R. Solo reconocer una suma elemental.

### 6. Gran novedad
- **Sintaxis nueva:** aparece `+`, pero no es el foco conceptual.
- **Modelo mental nuevo:** escribir código y ejecutarlo son acciones distintas; la ejecución produce un resultado.
- **Decisión nueva:** ninguna. El código ya está escrito.

### 7. Recuperaciones
Ninguna. Es el punto de entrada al curso.

### 8. Contexto sustantivo
Dos grupos de una encuesta aportaron 18 y 12 respuestas. Queremos que R calcule cuántas respuestas hay en total.

### 9. Dataset / objetos
No hay objetos todavía. Valores visibles: `18` y `12`.

### 10. Texto para el estudiante
**Situación.** Dos grupos respondieron una encuesta: uno aportó 18 respuestas y otro 12.

**Tarea.** La instrucción ya está escrita. Coloca el cursor en esa línea, usa **Ctrl + Enter** y observa dónde aparece el resultado.

No necesitas cambiar el código todavía.

### 11. Modelo mental que queremos construir
`INSTRUCCIÓN ESCRITA → EJECUTAR → RESULTADO`

El estudiante debe comprender que ver `18 + 12` en el editor no equivale a haberlo ejecutado.

### 12. Código trabajado / ejemplo
```r
18 + 12
```

### 13. Starter code propuesto
```r
18 + 12
```

### 14. Acción esperada
Ejecutar la línea con Ctrl + Enter y localizar el resultado.

### 15. Solución canónica
```r
18 + 12
```

### 16. Resultado esperado
`30`.

### 17. Criterio semántico de éxito
La evaluación futura debe comprobar que se ejecutó una suma que produce `30`. El valor `30` escrito como literal no demuestra la habilidad. Si se inspecciona la expresión ejecutada, debe contener una operación aritmética equivalente con `18` y `12`; no debe exigirse coincidencia textual exacta.

### 18. Estrategias alternativas válidas
Puede aceptarse una forma aritméticamente equivalente como `12 + 18` si el objetivo técnico permite editar el starter. La acción central es ejecutar una operación y observar su resultado.

### 19. Error esperado / misconception
- mirar el código sin ejecutarlo y esperar que aparezca un resultado;
- reemplazar la instrucción por `30` porque ya conoce la respuesta.

### 20. Feedback si está correcto
**Bien.** Ejecutaste una instrucción y R produjo `30`. Escribir código y ejecutarlo son dos acciones diferentes.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si el estudiante escribe `30`:

> `30` es el resultado correcto, pero aquí queremos que R haga el cálculo. Vuelve a usar la suma y ejecútala.

### 22. Hint 1
La instrucción ya está escrita. No necesitas calcular ni modificar nada todavía.

### 23. Hint 2
Coloca el cursor en la línea `18 + 12`.

### 24. Hint 3
Usa **Ctrl + Enter** sobre `18 + 12` y busca el resultado que aparece después de ejecutar.

### 25. Predicción antes de ejecutar
No necesaria. La novedad está en ejecutar y localizar el resultado, no en anticipar una suma elemental.

### 26. Tipo de ejercicio
Ejecución/observación.

### 27. Andamiaje
Muy alto: código completo y una sola acción nueva.

### 28. Carga cognitiva
**Baja.** Están activos únicamente la línea de código, el comando de ejecución y la localización del resultado. La operación matemática es deliberadamente familiar.

### 29. Fading
Es el nivel máximo de apoyo. E2 mantiene el código completo, pero obliga a modificar una parte antes de ejecutarlo.

### 30. Recuperación futura
La ejecución reaparece en todos los ejercicios posteriores. Desde E3 se añade la distinción entre ejecutar una asignación y consultar un objeto.

### 31. Riesgo de aprendizaje superficial
Bajo en esta pantalla. El principal riesgo es creer que el objetivo era obtener `30`, en vez de aprender el ciclo escribir/ejecutar/observar. El feedback debe enfatizar la acción, no el número.

### 32. Criterio de transferencia
La habilidad se considerará disponible cuando pueda ejecutar posteriormente una instrucción nueva sin que la consigna vuelva a explicar qué significa ejecutar.

### 33. Notas para implementación futura
Mantener visualmente separados **Ctrl + Enter = ejecutar/observar** y **Comprobar respuesta = evaluar la tarea**. No introducir todavía lenguaje sobre objetos, variables o tipos. El grader no debe aceptar un literal `30` como equivalente pedagógico a ejecutar la suma.

---

## M1-E2 — Cambia la respuesta

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Permite repetir el ciclo de ejecución con una pequeña reducción del apoyo: ahora el estudiante debe identificar qué parte del código representa un dato que cambió, editarla y volver a ejecutar.

### 3. Capacidad antes
Puede ejecutar una instrucción ya escrita y localizar su resultado.

### 4. Capacidad después
Puede modificar un dato dentro de una instrucción existente, volver a ejecutarla y comprobar que el resultado cambia.

### 5. Prerrequisitos
M1-E1: ejecutar código y observar un resultado.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Modelo mental nuevo:** se consolida que el código puede editarse y ejecutarse nuevamente.
- **Decisión nueva:** identificar cuál de los dos valores cambió.

### 7. Recuperaciones
Recuperación inmediata de ejecutar y observar.

### 8. Contexto sustantivo
El segundo grupo de la encuesta ya no tiene 12 respuestas: el conteo actualizado es 15.

### 9. Dataset / objetos
No hay objetos todavía. Valores: primer grupo `18`; segundo grupo actualizado `15`.

### 10. Texto para el estudiante
**Situación.** Antes calculamos 18 respuestas de un grupo y 12 del otro. El segundo conteo fue actualizado: ahora son **15** respuestas.

**Tarea.** Cambia solo lo necesario en el código y vuelve a ejecutarlo con Ctrl + Enter.

### 11. Modelo mental que queremos construir
`CÓDIGO EXISTENTE → CAMBIA UN DATO → EDITAR → VOLVER A EJECUTAR → NUEVO RESULTADO`

### 12. Código trabajado / ejemplo
El ejemplo previo ya fue M1-E1; no se agrega otro ejemplo para no resolver la modificación.

### 13. Starter code propuesto
```r
18 + 12
```

### 14. Acción esperada
Cambiar `12` por `15` y ejecutar la nueva instrucción.

### 15. Solución canónica
```r
18 + 15
```

### 16. Resultado esperado
`33`.

### 17. Criterio semántico de éxito
Debe producir `33` mediante una suma que represente los dos conteos actuales. Un literal `33` no demuestra la capacidad objetivo. Deben aceptarse operandos equivalentes como `15 + 18` si producen el mismo cálculo.

### 18. Estrategias alternativas válidas
`15 + 18` es válido. No es necesario exigir espacios específicos. No se aceptan `33` ni otras formas que omitan la operación.

### 19. Error esperado / misconception
- ejecutar nuevamente `18 + 12` sin editarlo;
- cambiar el número equivocado;
- reemplazar todo por `33`.

### 20. Feedback si está correcto
**Bien.** Modificaste un dato del código y R volvió a calcular el resultado. Cuando cambia la información, puedes cambiar la instrucción y ejecutarla otra vez.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si escribe `33`:

> Llegaste al total correcto, pero evitaste la tarea. Queremos que el código represente los dos conteos y que R haga la suma.

### 22. Hint 1
Solo cambió la cantidad del segundo grupo.

### 23. Hint 2
El primer valor sigue siendo `18`; el segundo debe pasar de `12` a `15`.

### 24. Hint 3
Deja la línea como `18 + 15` y ejecútala.

### 25. Predicción antes de ejecutar
No necesaria.

### 26. Tipo de ejercicio
Modificación.

### 27. Andamiaje
Alto: la estructura completa ya existe y solo se modifica un dato.

### 28. Carga cognitiva
**Baja.** Se recupera la ejecución y se añade una única decisión de edición.

### 29. Fading
Respecto de E1, se retira la indicación de que el código ya está listo: ahora el estudiante debe localizar y cambiar un valor.

### 30. Recuperación futura
Editar y volver a ejecutar reaparece de manera implícita durante todo el curso. En E3 se introduce guardar resultados para no depender solo de instrucciones aisladas.

### 31. Riesgo de aprendizaje superficial
Puede limitarse a imitar el cambio `12 → 15`. Ese riesgo es aceptable aquí porque E3–E5 cambian el problema y exigen un nuevo modelo mental.

### 32. Criterio de transferencia
Más adelante debe poder ajustar datos o nombres dentro de código conocido sin recibir instrucciones sobre cada tecla o cada posición.

### 33. Notas para implementación futura
El grader debe distinguir `18 + 15` de `33`. No exigir orden de operandos ni formato textual exacto.

---

## M1-E3 — Guardar para después

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce la idea central de objeto y la asignación con `<-`. La pantalla debe resolver explícitamente una misconception frecuente: **guardar un valor no es lo mismo que mostrarlo**.

### 3. Capacidad antes
Puede ejecutar y modificar instrucciones que producen un resultado inmediato.

### 4. Capacidad después
Puede guardar un valor con un nombre y consultar posteriormente el contenido de ese objeto.

### 5. Prerrequisitos
Ejecución con Ctrl + Enter y lectura de resultados de E1–E2.

### 6. Gran novedad
- **Sintaxis nueva:** `<-`.
- **Modelo mental nuevo:** un objeto conserva información bajo un nombre; asignar y consultar son acciones distintas.
- **Decisión nueva:** ninguna en la primera parte; el ejemplo está trabajado.

### 7. Recuperaciones
Recupera ejecutar código. Todavía no es recuperación espaciada.

### 8. Contexto sustantivo
El conteo actualizado de la encuesta es `33`. Queremos conservarlo para usarlo después sin volver a escribir el número cada vez.

### 9. Dataset / objetos
Objeto nuevo: `respuestas`, con valor numérico `33`.

### 10. Texto para el estudiante
**Situación.** Ya sabemos que la encuesta tiene 33 respuestas. Ahora queremos guardar ese valor para volver a usarlo después.

**Antes de ejecutar**, responde mentalmente:

> ¿Crees que `respuestas <- 33` mostrará `33` inmediatamente como resultado?

Ejecuta solo la primera línea.

```r
respuestas <- 33
```

Si no apareció `33`, no significa que haya fallado: R guardó el valor.

Un **objeto** permite guardar información usando un nombre para poder consultarla y reutilizarla después.

Ahora ejecuta la segunda línea:

```r
respuestas
```

### 11. Modelo mental que queremos construir
`VALOR → ASIGNAR A UN NOMBRE → OBJETO` y luego `NOMBRE → CONSULTAR → VALOR`.

Idea crítica: **asignar ≠ mostrar**.

### 12. Código trabajado / ejemplo
```r
respuestas <- 33
respuestas
```

La experiencia debe guiar al estudiante a ejecutar primero la asignación y después la consulta, no ambas como un bloque indistinguible.

### 13. Starter code propuesto
```r
respuestas <- 33

respuestas
```

### 14. Acción esperada
Ejecutar primero `respuestas <- 33`; observar que la asignación no imprime el valor; luego ejecutar `respuestas` y observar `33`.

### 15. Solución canónica
```r
respuestas <- 33
respuestas
```

### 16. Resultado esperado
Existe el objeto `respuestas` con valor `33`, y al consultarlo se observa `33`.

### 17. Criterio semántico de éxito
Debe comprobarse que el objeto `respuestas` existe y contiene numéricamente `33`. Cuando la infraestructura permita inspeccionar las expresiones ejecutadas, también debe registrarse una consulta posterior de `respuestas`; no basta con ejecutar solamente el literal `33`.

### 18. Estrategias alternativas válidas
No es necesario exigir espacios alrededor de `<-`. La consulta puede ocurrir inmediatamente después de la asignación. El nombre `respuestas` sí forma parte de la tarea porque se reutilizará conceptualmente en el ejercicio.

### 19. Error esperado / misconception
- creer que la ausencia de output al asignar significa que R no hizo nada;
- escribir `33` para “consultar” en vez del nombre del objeto;
- modificar el nombre entre asignación y consulta.

### 20. Feedback si está correcto
**Bien.** Guardaste `33` con el nombre `respuestas` y después consultaste ese objeto. Crear un objeto y mostrar su contenido son acciones diferentes.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si obtiene `33` ejecutando solo `33`:

> Puedes ver `33`, pero todavía no lo has guardado. La tarea es crear `respuestas` con `<-` y después consultar ese nombre.

### 22. Hint 1
Piensa en dos acciones distintas: primero **guardar**, después **consultar**.

### 23. Hint 2
Para guardar un valor con un nombre usamos la forma `nombre <- valor`.

### 24. Hint 3
Ejecuta `respuestas <- 33` y después ejecuta solamente `respuestas`.

### 25. Predicción antes de ejecutar
Sí. Pregunta central: “¿Crees que `respuestas <- 33` mostrará 33 inmediatamente?”. La predicción debe ocurrir antes de ejecutar la asignación.

### 26. Tipo de ejercicio
Worked example con predicción conceptual.

### 27. Andamiaje
Muy alto: se entrega el código y se secuencia explícitamente qué línea ejecutar primero.

### 28. Carga cognitiva
**Baja-media.** Aparecen `<-`, el término objeto y la distinción guardar/consultar. Son elementos relacionados de una sola nueva unidad funcional.

### 29. Fading
E3 muestra la estructura completa. E4 conservará una asignación resuelta, pero obligará a producir una segunda sin verla escrita.

### 30. Recuperación futura
E4–E8 recuperan asignación y consulta de inmediato. M2 y módulos posteriores constituyen la recuperación espaciada real de `<-` y los objetos.

### 31. Riesgo de aprendizaje superficial
Memorizar el patrón visual `nombre <- número` sin comprender por qué consultar el nombre produce el valor. La ejecución separada y la predicción atacan directamente este riesgo.

### 32. Criterio de transferencia
La capacidad estará disponible cuando pueda crear y consultar un objeto nuevo con otro nombre y otro valor sin volver a recibir el ejemplo completo.

### 33. Notas para implementación futura
La UI debe permitir ejecutar las líneas por separado. No presentar la ausencia de output de una asignación como fallo. No introducir `=` como alternativa de asignación en este módulo. `==` todavía no aparece.

---

## M1-E4 — Crea un objeto tú

### 1. Rol pedagógico
PRÁCTICA / completion problem.

### 2. Por qué existe
Es el primer paso desde observar una asignación completa hacia producirla. Mantiene una asignación resuelta como apoyo y deja la segunda para completar.

### 3. Capacidad antes
Puede guardar un valor con `<-` y consultar un objeto cuando el ejemplo está completamente escrito.

### 4. Capacidad después
Puede producir una asignación sencilla y consultar objetos con menor apoyo.

### 5. Prerrequisitos
M1-E3: objeto, `<-`, guardar y consultar.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Modelo mental nuevo:** se consolida la asignación como estructura productiva.
- **Decisión nueva:** completar correctamente nombre y valor del segundo objeto.

### 7. Recuperaciones
Recuperación inmediata de `<-` y consulta.

### 8. Contexto sustantivo
En la encuesta, Sociología aportó 18 respuestas y Antropología 15.

### 9. Dataset / objetos
- `respuestas_sociologia = 18`;
- `respuestas_antropologia = 15`.

### 10. Texto para el estudiante
**Situación.** La encuesta recibió:

- 18 respuestas de Sociología;
- 15 respuestas de Antropología.

El primer objeto ya está creado.

**Tarea.** Crea el objeto `respuestas_antropologia` con el valor correcto. Después consulta los dos objetos para comprobar qué quedó guardado.

### 11. Modelo mental que queremos construir
`NOMBRE + <- + VALOR → OBJETO`, seguido de `NOMBRE → CONSULTA`.

### 12. Código trabajado / ejemplo
La primera línea actúa como ejemplo visible:

```r
respuestas_sociologia <- 18
```

### 13. Starter code propuesto
```r
respuestas_sociologia <- 18

# crea respuestas_antropologia aquí


# consulta los dos objetos
```

### 14. Acción esperada
Escribir una asignación para `respuestas_antropologia` con valor `15` y consultar ambos objetos.

### 15. Solución canónica
```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

respuestas_sociologia
respuestas_antropologia
```

### 16. Resultado esperado
Existen ambos objetos con valores `18` y `15`, y pueden consultarse.

### 17. Criterio semántico de éxito
Debe existir `respuestas_sociologia` con valor numérico `18` y `respuestas_antropologia` con valor numérico `15`. La comprobación futura debería registrar que ambos objetos fueron evaluados como expresiones de consulta después de su creación; la estructura no se valida mediante comparación textual literal.

### 18. Estrategias alternativas válidas
Pueden variar espacios y líneas en blanco. Puede consultar los objetos en cualquier orden. El nombre `respuestas_antropologia` y su valor `15` son obligatorios porque forman parte de la tarea.

### 19. Error esperado / misconception
- escribir `15 <- respuestas_antropologia` invirtiendo la dirección;
- escribir el valor correcto con un nombre diferente;
- modificar la asignación de Sociología en lugar de crear la de Antropología;
- escribir solo `15` sin guardarlo.

### 20. Feedback si está correcto
**Bien.** Ya puedes crear un objeto sin que la asignación esté completamente escrita por ti y comprobar su contenido usando el nombre.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si aparece `15` pero no existe `respuestas_antropologia`:

> Viste el valor correcto, pero todavía no lo guardaste con el nombre solicitado. Crea el objeto usando `<-`.

### 22. Hint 1
Necesitas guardar `15` usando el nombre `respuestas_antropologia`.

### 23. Hint 2
Recuerda la estructura del ejercicio anterior: `nombre <- valor`.

### 24. Hint 3
Escribe `respuestas_antropologia <- 15`. Después ejecuta `respuestas_sociologia` y `respuestas_antropologia` para consultarlos.

### 25. Predicción antes de ejecutar
No necesaria.

### 26. Tipo de ejercicio
Completion problem.

### 27. Andamiaje
Alto: una asignación completa funciona como modelo; la segunda debe producirse.

### 28. Carga cognitiva
**Baja-media.** No hay sintaxis nueva; el esfuerzo está en recuperar la estructura de asignación y aplicar el nombre/valor correctos.

### 29. Fading
Se retira una asignación completa respecto de E3. En E5 las asignaciones estarán dadas y el estudiante deberá producir una nueva expresión que reutilice ambos objetos.

### 30. Recuperación futura
E5–E8 continúan recuperando `<-` y objetos. M2+ constituye recuperación espaciada.

### 31. Riesgo de aprendizaje superficial
Copiar visualmente la primera línea cambiando palabras puede permitir resolver E4 con comprensión parcial. E5 mitiga ese riesgo porque exige usar los objetos como componentes de una nueva operación.

### 32. Criterio de transferencia
Más adelante debe poder crear objetos con nombres y valores distintos sin disponer de una línea paralela para copiar.

### 33. Notas para implementación futura
El valor `15` debe aparecer explícitamente en la consigna; nunca depender de una solución invisible. Los comentarios del starter orientan la estructura, pero no se ejecutan como respuesta.

---

## M1-E5 — Reutiliza lo guardado

### 1. Rol pedagógico
PRÁCTICA / producción guiada.

### 2. Por qué existe
Construye una de las capacidades centrales del módulo: un objeto no sirve solo para conservar un valor; puede reutilizarse dentro de una nueva instrucción. Esta idea prepara el trabajo reproducible posterior.

### 3. Capacidad antes
Puede crear y consultar objetos con valores individuales.

### 4. Capacidad después
Puede usar objetos existentes como partes de una operación nueva y guardar el resultado en otro objeto.

### 5. Prerrequisitos
E1–E4: `+`, `<-`, objetos y consulta.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Modelo mental nuevo:** se consolida la reutilización: el código puede referirse a objetos en vez de reescribir sus valores.
- **Decisión nueva:** identificar que el total debe construirse a partir de los dos objetos existentes.

### 7. Recuperaciones
Recuperación inmediata de suma, objetos y asignación.

### 8. Contexto sustantivo
Queremos calcular el total de respuestas a partir de los conteos ya guardados para Sociología y Antropología.

### 9. Dataset / objetos
```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15
```

Objeto nuevo esperado: `total_respuestas`.

### 10. Texto para el estudiante
**Situación.** Los dos conteos ya están guardados en objetos.

**Tarea.** Crea `total_respuestas` sumando **los objetos** `respuestas_sociologia` y `respuestas_antropologia`. No escribas `33` directamente. Después consulta `total_respuestas`.

### 11. Modelo mental que queremos construir
`OBJETO A + OBJETO B → NUEVO RESULTADO → NUEVO OBJETO`.

La clave es que el cálculo depende de la información ya guardada.

### 12. Código trabajado / ejemplo
No se entrega la suma resuelta. Los dos objetos fuente funcionan como preparación completa de los datos.

### 13. Starter code propuesto
```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

# calcula total_respuestas usando los objetos anteriores
```

### 14. Acción esperada
Crear `total_respuestas` mediante la suma de ambos objetos y consultarlo.

### 15. Solución canónica
```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

### 16. Resultado esperado
`total_respuestas` vale `33` y proviene de la suma de los dos objetos fuente.

### 17. Criterio semántico de éxito
Se deben verificar dos niveles:

1. **Resultado:** existe `total_respuestas` y vale numéricamente `33`.
2. **Estrategia:** la expresión que produce `total_respuestas` depende de `respuestas_sociologia` y `respuestas_antropologia`; `total_respuestas <- 33` no es suficiente.

El futuro grader puede verificar esa dependencia mediante inspección semántica de la expresión o mediante una prueba oculta que cambie temporalmente los valores fuente y compruebe que el total se actualiza al reejecutar. No debe comparar una cadena literal de código.

### 18. Estrategias alternativas válidas
Son válidas expresiones equivalentes como:

```r
total_respuestas <- respuestas_antropologia + respuestas_sociologia
```

También son válidos espacios y saltos de línea diferentes. Deben aparecer ambos objetos fuente en el cálculo.

### 19. Error esperado / misconception
- `total_respuestas <- 33`;
- `18 + 15` sin reutilizar los objetos;
- consultar uno de los objetos pero no crear el total;
- sobrescribir uno de los objetos fuente con el total.

### 20. Feedback si está correcto
**Bien.** `total_respuestas` se calcula a partir de objetos que ya existían. Si cambia un dato fuente y vuelves a ejecutar el script, el cálculo puede actualizarse sin que tengas que reemplazar manualmente el total.

Después del éxito, plantear:

> Si `respuestas_antropologia` cambiara de 15 a 16 y ejecutaras nuevamente todo el código, ¿qué debería ocurrir con `total_respuestas`?

Respuesta conceptual esperada: debería pasar de 33 a 34 al reejecutar el cálculo.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si usa `33`, `18 + 15` u otra forma hardcodeada:

> El total es correcto, pero aquí queremos practicar **reutilización**. Haz que `total_respuestas` dependa de los dos objetos ya guardados, no de números escritos otra vez.

### 22. Hint 1
Los dos valores que necesitas ya tienen nombre. No necesitas volver a escribir `18` ni `15`.

### 23. Hint 2
Puedes usar nombres de objetos a ambos lados de `+`, igual que antes usaste números.

### 24. Hint 3
Usa `total_respuestas <- respuestas_sociologia + respuestas_antropologia` y después consulta `total_respuestas`.

### 25. Predicción antes de ejecutar
No se exige antes de la primera solución. Después del éxito se utiliza la pregunta de cambio `15 → 16` para comprobar el modelo de dependencia y comenzar a construir una intuición de reproducibilidad.

### 26. Tipo de ejercicio
Producción guiada.

### 27. Andamiaje
Medio-alto: los objetos fuente están creados, pero la expresión objetivo no se muestra.

### 28. Carga cognitiva
**Media.** El estudiante mantiene activos dos objetos, la asignación, la suma y la idea de dependencia entre valores. No hay sintaxis nueva.

### 29. Fading
Respecto de E4, se retira el modelo directo de asignación paralela. En E5 el estudiante decide cómo combinar conocimientos ya disponibles para producir un objeto derivado.

### 30. Recuperación futura
La reutilización de objetos se vuelve infraestructura desde M2 en adelante y debe recuperarse repetidamente sin explicaciones completas.

### 31. Riesgo de aprendizaje superficial
Alto si el grader acepta solamente `total_respuestas == 33`. Por eso la dependencia respecto de ambos objetos es parte obligatoria del criterio de éxito.

### 32. Criterio de transferencia
La capacidad se considerará disponible cuando pueda construir más adelante un resultado a partir de objetos distintos sin que la consigna le diga explícitamente “usa los objetos anteriores”.

### 33. Notas para implementación futura
Este ejercicio requiere semantic grading de estrategia, no solo de estado final. No penalizar orden de operandos. La pregunta `15 → 16` puede resolverse como selección conceptual breve o feedback interactivo; no introduce sintaxis nueva.

---

## M1-E6 — Número o texto

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce únicamente la diferencia práctica entre representar una cantidad y representar texto. Se elimina de M1 cualquier introducción formal de valores lógicos para no combinar dos representaciones nuevas en la misma pantalla.

### 3. Capacidad antes
Puede crear, consultar y reutilizar objetos numéricos.

### 4. Capacidad después
Puede guardar correctamente un número sin comillas y un texto entre comillas en situaciones simples.

### 5. Prerrequisitos
Objeto, `<-` y consulta de E3–E5.

### 6. Gran novedad
- **Sintaxis nueva:** comillas dobles para texto.
- **Modelo mental nuevo:** `21` representa una cantidad; `"21"` representa texto.
- **Decisión nueva:** decidir si el valor solicitado es una cantidad o un texto.

### 7. Recuperaciones
Recupera asignación y objetos.

### 8. Contexto sustantivo
Guardar la edad de una persona y el nombre de su carrera.

### 9. Dataset / objetos
Ejemplo:
- `edad = 20`;
- `carrera = "Historia"`.

Producción solicitada:
- `edad = 21`;
- `carrera = "Sociología"`.

### 10. Texto para el estudiante
**Situación.** Los objetos pueden guardar información distinta.

Observa:

```r
edad <- 20
carrera <- "Historia"
```

`20` es una cantidad. `"Historia"` es texto, por eso necesita comillas.

**Tarea.** Cambia la información para guardar:

- `21` en `edad`;
- `"Sociología"` en `carrera`.

Después consulta ambos objetos.

Recuerda: `21` y `"21"` no representan lo mismo para R.

### 11. Modelo mental que queremos construir
`CANTIDAD → SIN COMILLAS` y `TEXTO → ENTRE COMILLAS`.

### 12. Código trabajado / ejemplo
```r
edad <- 20
carrera <- "Historia"
```

### 13. Starter code propuesto
```r
# guarda 21 en edad


# guarda Sociología en carrera


# consulta ambos objetos
```

### 14. Acción esperada
Crear `edad <- 21` y `carrera <- "Sociología"`, y consultar ambos objetos.

### 15. Solución canónica
```r
edad <- 21
carrera <- "Sociología"

edad
carrera
```

### 16. Resultado esperado
`edad` contiene el número `21`; `carrera` contiene el texto `"Sociología"`.

### 17. Criterio semántico de éxito
- existe `edad` con valor numérico `21`;
- existe `carrera` con valor de texto `"Sociología"`;
- no basta con que ambos se vean visualmente parecidos: `edad <- "21"` debe considerarse representación incorrecta para esta tarea.

El grader puede inspeccionar el tipo interno sin enseñar al estudiante funciones de inspección de tipos.

### 18. Estrategias alternativas válidas
Se aceptan comillas simples o dobles si el runtime las trata como texto equivalente y la plataforma decide permitir ambas. La solución canónica usa comillas dobles para mantener una convención única visible. No se requieren funciones como `class()` ni `typeof()`.

### 19. Error esperado / misconception
- `edad <- "21"`;
- `carrera <- Sociología` sin comillas;
- asumir que las comillas son decoración y no cambian la representación.

### 20. Feedback si está correcto
**Bien.** Guardaste una cantidad como número y un nombre como texto. Las comillas le indican a R que un valor debe tratarse como texto.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si `edad` contiene `"21"`:

> Se ve como 21, pero está guardado como texto. Para representar una cantidad en este ejercicio, escribe `21` sin comillas.

Si `carrera` no está entre comillas:

> `Sociología` es texto. Escríbelo entre comillas para que R lo reconozca como un valor de texto.

### 22. Hint 1
Pregunta para cada valor: ¿representa una **cantidad** o una **palabra/nombre**?

### 23. Hint 2
Las cantidades se escriben sin comillas; el texto se escribe entre comillas.

### 24. Hint 3
Escribe `edad <- 21` y `carrera <- "Sociología"`. Después consulta `edad` y `carrera`.

### 25. Predicción antes de ejecutar
Opcional y breve: preguntar cuál de estas dos formas representa una cantidad, `21` o `"21"`, antes de producir el código. No convertirla en una etapa obligatoria si añade fricción innecesaria.

### 26. Tipo de ejercicio
Worked example breve + producción guiada.

### 27. Andamiaje
Medio-alto: se muestra un par de ejemplos y se pide producir un par equivalente con valores nuevos.

### 28. Carga cognitiva
**Baja-media.** La única novedad sustantiva es el papel de las comillas. La asignación y los objetos ya fueron practicados.

### 29. Fading
Se recupera `<-` sin volver a explicarlo paso a paso. El nuevo apoyo se concentra exclusivamente en número vs texto.

### 30. Recuperación futura
E7 recupera inmediatamente número vs texto mediante debugging. Las representaciones reaparecerán después al trabajar con vectores y datos. Los valores lógicos quedan explícitamente pospuestos hasta M3.

### 31. Riesgo de aprendizaje superficial
Memorizar “palabras llevan comillas” sin comprender que `"21"` también es texto. La comparación `21` vs `"21"` debe quedar visible.

### 32. Criterio de transferencia
La habilidad estará disponible cuando pueda representar correctamente otros números y textos sin que la consigna le recuerde explícitamente las comillas.

### 33. Notas para implementación futura
No introducir `TRUE`, `FALSE`, `logical`, `boolean`, `class()` ni `typeof()`. El grader sí puede usar información de tipo internamente. Mantener una convención visible de comillas dobles aunque se acepten equivalentes semánticos.

---

## M1-E7 — Lee el error antes de corregir

### 1. Rol pedagógico
RECUPERACIÓN + debugging guiado.

### 2. Por qué existe
Recupera de forma integrada número/texto, objetos y reutilización. Además introduce una actitud operativa hacia los errores: un mensaje de error puede ser una pista sobre qué parte del código revisar.

### 3. Capacidad antes
Puede reutilizar objetos y distinguir una cantidad numérica de un texto entre comillas.

### 4. Capacidad después
Puede reconocer un error sencillo causado por representar un número como texto, corregir el dato y volver a ejecutar el cálculo sin sustituirlo por un resultado hardcodeado.

### 5. Prerrequisitos
E5: reutilización de objetos. E6: número vs texto.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Modelo mental nuevo:** el error se usa como información, pero no se exige interpretar autónomamente terminología técnica del mensaje.
- **Decisión nueva:** localizar cuál de los valores está representado de manera incompatible con la suma.

### 7. Recuperaciones
Recuperación inmediata/intramódulo de `<-`, número/texto y reutilización. No se clasifica como spaced retrieval.

### 8. Contexto sustantivo
Dos conteos de respuestas deberían sumarse, pero uno fue guardado accidentalmente como texto.

### 9. Dataset / objetos
Starter defectuoso:

```r
respuestas_sociologia <- 18
respuestas_antropologia <- "15"
total_respuestas <- respuestas_sociologia + respuestas_antropologia
```

### 10. Texto para el estudiante
**Situación.** Queremos sumar dos conteos de respuestas, pero el código contiene un problema.

Antes de ejecutarlo, compara estas dos partes:

```r
18
```

y

```r
"15"
```

¿Notas una diferencia en cómo están escritas?

Ahora ejecuta el código.

**Un error no significa que hayas roto R. Los errores son parte normal de programar y pueden darnos pistas.**

No necesitas descifrar cada palabra del mensaje técnico. Revisa cómo está representado cada dato, corrige únicamente el problema y vuelve a ejecutar el cálculo.

### 11. Modelo mental que queremos construir
`ERROR → REVISAR DATOS/CÓDIGO → IDENTIFICAR DIFERENCIA RELEVANTE → CORREGIR → REEJECUTAR`.

### 12. Código trabajado / ejemplo
No se agrega un ejemplo de corrección porque revelaría la respuesta. El propio starter defectuoso es el material de debugging.

### 13. Starter code propuesto
```r
respuestas_sociologia <- 18
respuestas_antropologia <- "15"
total_respuestas <- respuestas_sociologia + respuestas_antropologia
```

### 14. Acción esperada
Ejecutar, reconocer que `"15"` está guardado como texto, quitar las comillas, mantener el cálculo mediante objetos y volver a ejecutar.

### 15. Solución canónica
```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15
total_respuestas <- respuestas_sociologia + respuestas_antropologia

total_respuestas
```

### 16. Resultado esperado
`respuestas_antropologia` queda como número `15` y `total_respuestas` vale `33` mediante la suma de ambos objetos.

### 17. Criterio semántico de éxito
Debe comprobarse simultáneamente que:

- `respuestas_sociologia` vale numéricamente `18`;
- `respuestas_antropologia` vale numéricamente `15`, no texto;
- `total_respuestas` vale `33`;
- `total_respuestas` depende de los dos objetos fuente.

No es suficiente `total_respuestas <- 33`. La dependencia puede comprobarse por inspección semántica o prueba oculta con valores fuente perturbados.

### 18. Estrategias alternativas válidas
Se acepta cualquier corrección que transforme el segundo conteo en un valor numérico y conserve el cálculo a partir de ambos objetos. En este nivel no se introducirán funciones de conversión; la estrategia esperada es corregir la representación original quitando las comillas.

### 19. Error esperado / misconception
- hardcodear `33`;
- cambiar la suma en vez del dato problemático;
- borrar un objeto para evitar el error;
- mantener `"15"` pensando que las comillas no importan;
- interpretar el error como señal de que “R no funciona”.

### 20. Feedback si está correcto
**Bien.** Usaste el error como una pista: uno de los conteos estaba escrito como texto. Corregiste el dato y conservaste el cálculo con los objetos. Ese ciclo de detectar, corregir y volver a ejecutar es parte normal de programar.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si escribe `total_respuestas <- 33`:

> El total es correcto, pero evitaste el problema. Corrige el objeto que contiene `"15"` y conserva la suma entre los dos objetos.

Si modifica la suma pero deja `"15"`:

> La operación que queremos sigue siendo una suma. Revisa cómo está escrito el segundo conteo antes de cambiar el cálculo.

### 22. Hint 1
Compara `18` con `"15"`. ¿Cuál de los dos está escrito como texto?

### 23. Hint 2
Las comillas hacen que `"15"` sea texto. Para usarlo como cantidad en esta suma, el valor debe quedar sin comillas.

### 24. Hint 3
Cambia la segunda línea a `respuestas_antropologia <- 15` y vuelve a ejecutar la suma con los dos objetos.

### 25. Predicción antes de ejecutar
Sí. Antes de ejecutar, pedir que observe `18` y `"15"` y detecte si están representados de la misma manera. No se exige predecir el texto exacto del error.

### 26. Tipo de ejercicio
Debugging guiado / error-driven learning.

### 27. Andamiaje
Medio: el problema no se señala por número de línea, pero las pistas orientan gradualmente hacia la representación incorrecta.

### 28. Carga cognitiva
**Media.** Debe mantener activos objetos, suma, número/texto y el mensaje de error. La carga se controla evitando exigir interpretación autónoma del texto técnico de R.

### 29. Fading
E7 retira la consigna procedural directa: el estudiante debe diagnosticar cuál conocimiento previo necesita recuperar para corregir el código.

### 30. Recuperación futura
La actitud hacia errores debe reaparecer cuando ocurran de manera auténtica. La recuperación espaciada de objetos y asignación comienza en M2 y continúa posteriormente.

### 31. Riesgo de aprendizaje superficial
Puede aprender solo “quitar comillas arregla este ejercicio”. E8 cambia el contexto y obliga a representar correctamente texto y números desde cero, reduciendo ese riesgo.

### 32. Criterio de transferencia
Más adelante debe poder inspeccionar un error sencillo y revisar primero datos, nombres o sintaxis conocida antes de asumir que el sistema falló.

### 33. Notas para implementación futura
No validar el texto exacto del mensaje de error, que puede variar por runtime o versión. El feedback debe normalizar el error sin infantilizar al estudiante. No introducir todavía conversión explícita con funciones nuevas.

---

## M1-E8 — Encuesta piloto

### 1. Rol pedagógico
INTEGRACIÓN.

### 2. Por qué existe
Cierra M1 combinando, con menos apoyo, las capacidades nucleares: crear objetos, distinguir número/texto, reutilizar objetos y consultar un resultado. Debe ofrecer evidencia de integración y preparar la necesidad conceptual de M2.

### 3. Capacidad antes
Puede ejecutar, modificar, asignar, consultar, reutilizar y corregir un error simple de representación con apoyo decreciente.

### 4. Capacidad después
Puede construir un pequeño script desde una situación descrita en lenguaje natural, guardar distintos valores y derivar un resultado nuevo reutilizando objetos.

### 5. Prerrequisitos
Todo M1-E1 a M1-E7. No usa contenidos de M2.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Modelo mental nuevo:** ninguno; integra los ya construidos.
- **Decisión nueva:** descomponer una situación en cuatro objetos y decidir qué valores deben escribirse como texto o como números.

### 7. Recuperaciones
Integra recuperación inmediata de `<-`, consulta, suma, reutilización y número/texto.

### 8. Contexto sustantivo
Una encuesta piloto llamada **“Encuesta de vida universitaria”** obtuvo 14 respuestas de Sociología y 11 de Antropología.

### 9. Dataset / objetos
Objetos requeridos:

- `estudio = "Encuesta de vida universitaria"`;
- `respuestas_sociologia = 14`;
- `respuestas_antropologia = 11`;
- `total_respuestas = 25`, calculado a partir de los dos objetos anteriores.

### 10. Texto para el estudiante
**Situación.** Una encuesta piloto llamada **“Encuesta de vida universitaria”** recibió:

- 14 respuestas de estudiantes de Sociología;
- 11 respuestas de estudiantes de Antropología.

**Tarea.** Construye un pequeño script que:

1. guarde el nombre del estudio en `estudio`;
2. guarde cada conteo en `respuestas_sociologia` y `respuestas_antropologia`;
3. cree `total_respuestas` usando los dos objetos anteriores;
4. consulte `total_respuestas`.

No necesitas ninguna herramienta nueva: todo lo necesario apareció en los ejercicios anteriores.

### 11. Modelo mental que queremos construir
`SITUACIÓN → IDENTIFICAR INFORMACIÓN → GUARDAR EN OBJETOS → REUTILIZAR → PRODUCIR RESULTADO → CONSULTAR`.

### 12. Código trabajado / ejemplo
No hay código trabajado adicional. Mostrar una solución completa aquí destruiría la función integradora.

### 13. Starter code propuesto
```r
# Guarda el nombre del estudio


# Guarda las respuestas de cada carrera


# Calcula el total usando los objetos anteriores


# Consulta total_respuestas
```

### 14. Acción esperada
Producir las tres asignaciones iniciales, crear el total mediante reutilización y consultar `total_respuestas`.

### 15. Solución canónica
```r
estudio <- "Encuesta de vida universitaria"
respuestas_sociologia <- 14
respuestas_antropologia <- 11

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

### 16. Resultado esperado
- `estudio` contiene el texto correcto;
- `respuestas_sociologia` contiene el número `14`;
- `respuestas_antropologia` contiene el número `11`;
- `total_respuestas` contiene `25` y deriva de los dos conteos;
- al consultar `total_respuestas`, se observa `25`.

### 17. Criterio semántico de éxito
El futuro grader debe comprobar:

1. existe `estudio` y contiene exactamente el texto solicitado;
2. `respuestas_sociologia` es numérico y vale `14`;
3. `respuestas_antropologia` es numérico y vale `11`;
4. `total_respuestas` es numérico y vale `25`;
5. la construcción de `total_respuestas` depende de `respuestas_sociologia` y `respuestas_antropologia`, no de un literal `25` ni de `14 + 11` escritos nuevamente;
6. cuando la infraestructura lo permita, `total_respuestas` fue consultado después de su creación.

La dependencia debe validarse semánticamente o mediante perturbación oculta de los objetos fuente, no mediante comparación literal del código.

### 18. Estrategias alternativas válidas
Puede cambiar el orden de las tres primeras asignaciones. La suma puede invertir el orden de los objetos. Se permiten espacios y saltos de línea diferentes. Los nombres requeridos deben conservarse porque forman parte del contrato de la actividad.

### 19. Error esperado / misconception
- olvidar comillas en el nombre del estudio;
- escribir `"14"` o `"11"` como texto;
- hardcodear `total_respuestas <- 25`;
- calcular `14 + 11` sin reutilizar objetos;
- crear los objetos correctos pero no consultar el total.

### 20. Feedback si está correcto
**Bien.** Construiste un pequeño script con las ideas centrales de M1: guardaste información con nombres, distinguiste texto de cantidades, reutilizaste objetos para producir un nuevo resultado y consultaste ese resultado.

Cierre conceptual:

> Hasta ahora cada objeto ha guardado un valor. Pero una encuesta tiene muchas personas. ¿Tendríamos que crear un objeto distinto para cada respuesta? En el siguiente módulo necesitaremos una forma de guardar **varios valores relacionados juntos**.

### 21. Feedback si el resultado es correcto pero la estrategia no
Si `total_respuestas` vale 25 pero está hardcodeado:

> El total es correcto, pero debe construirse a partir de `respuestas_sociologia` y `respuestas_antropologia`. Así el cálculo puede actualizarse si cambian los datos.

Si el nombre del estudio aparece sin comillas:

> El nombre del estudio es texto. Revisa cómo representamos textos en E6.

Si los conteos están entre comillas:

> Los conteos representan cantidades. Guárdalos como números, sin comillas.

### 22. Hint 1
Divide el problema en partes: un nombre de estudio, dos conteos y un total. Decide primero cuáles son texto y cuáles son cantidades.

### 23. Hint 2
Crea primero `estudio`, `respuestas_sociologia` y `respuestas_antropologia` con `<-`. Después usa los dos conteos para construir el total.

### 24. Hint 3
La estructura final puede seguir este patrón:

```r
estudio <- "Encuesta de vida universitaria"
respuestas_sociologia <- 14
respuestas_antropologia <- 11
total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

### 25. Predicción antes de ejecutar
No se exige una predicción separada. La tarea ya requiere varias decisiones conocidas y debe priorizar integración autónoma.

### 26. Tipo de ejercicio
Integración.

### 27. Andamiaje
Bajo para el nivel del módulo: solo se entregan comentarios estructurales y nombres requeridos; no hay asignaciones resueltas.

### 28. Carga cognitiva
**Media.** Debe coordinar cuatro objetos y dos representaciones conocidas, pero no aparece sintaxis nueva. Los comentarios dividen la tarea en etapas para evitar una página completamente en blanco.

### 29. Fading
Es el punto final del fading de M1: el estudiante recibe el problema, los productos esperados y una estructura mínima, pero debe producir el código relevante.

### 30. Recuperación futura
M2 debe recuperar `<-`, objetos y consulta al introducir varios valores. Los módulos posteriores continúan reutilizando asignación y objetos como infraestructura, constituyendo la recuperación espaciada principal.

### 31. Riesgo de aprendizaje superficial
El mayor riesgo es hardcodear `25`. El grading debe comprobar dependencia de los objetos fuente. El cambio de valores y contexto respecto de E5 evita memorizar el resultado anterior.

### 32. Criterio de transferencia
La integración se considerará disponible cuando, en módulos posteriores, pueda crear y reutilizar objetos dentro de contextos nuevos sin recibir nuevamente el recorrido de M1.

### 33. Notas para implementación futura
No introducir `TRUE/FALSE` ni `c()` en este cierre. Mantener el starter como comentarios y espacios vacíos. El feedback final debe activar explícitamente el puente conceptual hacia M2 sin enseñar todavía la solución de “varios valores”.

---

# Cierre conceptual de M1 y puente a M2

Al finalizar M1, mostrar una transición breve:

> Hasta ahora cada objeto guarda un valor.
>
> Pero una encuesta tiene muchas personas.
>
> ¿Tendríamos que crear un objeto distinto para cada una?
>
> Necesitamos una forma de guardar **varios valores relacionados juntos**.

La transición termina ahí. No mostrar todavía `c()`, vectores ni selección por posición. Esa necesidad abre M2 — **Trabajar con varios valores**.

# Declaración de lock

M1 queda pedagógicamente cerrado con 8 ejercicios. La sintaxis nueva visible se limita a `+`, `<-` y comillas para texto. Las capacidades consolidadas son ejecución básica, edición, asignación, consulta, reutilización y distinción práctica entre número y texto. `TRUE/FALSE` y el tipo lógico se posponen para M3. El módulo termina exactamente en el prerrequisito que necesita M2: poder trabajar con objetos que contienen un único valor.
