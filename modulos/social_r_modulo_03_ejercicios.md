# Social R — Módulo 3
## Comparar y elegir valores

> Documento pedagógico canónico. Versión rediseñada definitiva para implementación posterior.

## 1. Propósito del módulo

Este módulo transforma la selección por posición aprendida en el Módulo 2 en una nueva capacidad: **elegir valores según una pregunta**.

Hasta ahora, el estudiante podía escribir:

```r
tiempos_viaje[3]
```

o:

```r
tiempos_viaje[c(2, 4)]
```

si conocía de antemano las posiciones que quería recuperar.

A partir de este módulo aprenderá a formular preguntas como:

> ¿Qué tiempos superan 30 minutos?

y a convertir esa pregunta en código:

```r
tiempos_viaje > 30
```

R responderá una vez por cada valor mediante `TRUE` o `FALSE`. Después, esas respuestas podrán guardarse y utilizarse dentro de `[]` para conservar únicamente los valores que cumplen.

La progresión conceptual central es:

**POSICIÓN → PREGUNTA → TRUE/FALSE → UNA RESPUESTA POR VALOR → GUARDAR RESPUESTAS → TRUE CONSERVA / FALSE DEJA FUERA → SELECCIONAR SEGÚN LA PREGUNTA**

El propósito no es memorizar operadores lógicos. Es construir un modelo mental reutilizable para el trabajo posterior con datos reales.

---

## 2. Perfil de entrada

Al comenzar este módulo, la persona ya puede:

- ejecutar código con Ctrl + Enter;
- crear y consultar objetos;
- utilizar `<-`;
- reconocer números, texto y valores `TRUE/FALSE`;
- crear vectores con `c()`;
- consultar vectores;
- comprender que cada elemento ocupa una posición;
- seleccionar un elemento con `[]`;
- seleccionar varias posiciones con `[c(...)]`;
- comprender de manera inicial la correspondencia posición a posición.

Por ejemplo, puede comprender:

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje[3]

tiempos_viaje[c(2, 4)]
```

No se asume que estas habilidades estén automatizadas. El módulo recupera explícitamente la selección por posición antes de introducir comparaciones.

---

## 3. Resultado de salida

Al finalizar el módulo, el estudiante debería poder comprender y producir aproximadamente:

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

tiempos_viaje[supera_30]
```

y explicar, en lenguaje cotidiano:

> R pregunta para cada tiempo si supera 30. Obtiene una respuesta TRUE/FALSE para cada valor, guarda esas respuestas y luego conserva los tiempos que corresponden a TRUE.

También debería reconocer de manera guiada que `==` permite formular una pregunta de igualdad sobre texto:

```r
carreras == "Sociología"
```

La selección de un vector utilizando una condición construida con **otro** vector queda deliberadamente fuera de este módulo.

---

## 4. Resultados de aprendizaje

Al finalizar, el estudiante debería poder:

1. Leer `>` como una pregunta del tipo “¿es mayor que?”.
2. Comprender que una comparación aplicada a un vector produce una respuesta `TRUE/FALSE` para cada valor.
3. Relacionar cada `TRUE/FALSE` con el valor de la misma posición.
4. Guardar esas respuestas en un objeto mediante `<-`.
5. Utilizar esas respuestas dentro de `[]` para conservar los valores que cumplen la pregunta.
6. Comprender que la pregunta sigue funcionando aunque cambien los valores y, por tanto, no necesita memorizar posiciones.
7. Reconocer de manera guiada que `==` permite preguntar si un texto es igual a otro.

Los puntos 1–6 son el núcleo del módulo. El punto 7 es una extensión secundaria y guiada.

---

## 5. Contenidos incluidos

- comparación simple con `>`;
- `TRUE/FALSE` como resultados de una comparación;
- comparación de un vector completo con un valor;
- correspondencia explícita valor ↔ respuesta;
- almacenamiento de respuestas mediante `<-`;
- selección con `vector[condicion]`;
- diferencia entre seleccionar mediante posiciones y seleccionar mediante una pregunta;
- `==` como comparación de igualdad sobre texto;
- transferencia del ciclo pregunta → respuestas → selección a un contexto nuevo.

---

## 6. Contenidos explícitamente pospuestos

No se enseñan como objetivos en este módulo:

```r
<
>=
<=
!=
```

Tampoco:

```r
x[x > 30]
```

como forma compacta obligatoria.

También se posponen:

```r
&
|
```

y:

- selección de un vector mediante una condición creada con otro vector;
- data frames;
- filas;
- columnas;
- `filter()`;
- `dplyr`;
- `mean()`;
- estadística descriptiva formal;
- combinaciones de condiciones;
- terminología como “máscara booleana” o “indexación lógica”.

---

## 7. Principios pedagógicos particulares del módulo

1. **La necesidad aparece antes que el operador.**  
   El módulo comienza recordando que seleccionar por posición requiere saber dónde está el dato.

2. **TRUE y FALSE se interpretan antes de formalizarse.**  
   Primero son respuestas cotidianas: “se cumple / no se cumple”.

3. **Una respuesta por cada valor debe hacerse visible.**  
   La correspondencia entre vector y respuestas no queda implícita.

4. **Guardar precede a seleccionar.**  
   El estudiante primero comprende qué contiene `supera_30`.

5. **La primera selección mediante condición es un worked example.**  
   No se exige descubrir por sí solo `vector[condicion]`.

6. **Después del worked example aparece un completion problem.**  
   La práctica inicial exige completar solo una pieza.

7. **La producción completa llega recién cuando el mecanismo fue observado y practicado.**

8. **El desafío final contiene una sola pregunta, una sola condición y una sola selección.**

9. **La selección cruzada entre vectores se posterga.**  
   Se retomará cuando el curso introduzca casos, variables u organización tabular de datos.

---

## 8. Mapa de progresión

**CONOZCO POSICIONES → NECESITO HACER UNA PREGUNTA → `>` PRODUCE TRUE/FALSE → R RESPONDE UNA VEZ POR VALOR → GUARDO LAS RESPUESTAS → TRUE CONSERVA / FALSE DEJA FUERA → COMPLETO UNA SELECCIÓN → PRODUZCO EL CICLO COMPLETO → TRANSFIERO A TEXTO → TRANSFIERO A DATOS NUEVOS**

---

# Ejercicio 1 — De posiciones a preguntas

## 1. Función pedagógica en la secuencia

**Antes:** puede elegir valores si conoce sus posiciones.

**Después:** comprende por qué necesita una nueva estrategia y reconoce `>` como una forma de hacer una pregunta a R.

## 2. Objetivo de aprendizaje en R

Ejecutar e interpretar comparaciones simples con `>`.

## 3. Idea sobre datos

No siempre conocemos de antemano qué posiciones nos interesan. Podemos formular una regla sobre los valores y preguntar si cada caso la cumple.

## 4. Pregunta o situación sustantiva

Tenemos tiempos de viaje y queremos responder:

> ¿Un viaje supera 30 minutos?

Antes de preguntar por todos los viajes, comenzamos con dos casos individuales.

## 5. Prerrequisitos recuperados

- ejecución con Ctrl + Enter;
- números;
- `TRUE/FALSE`;
- lectura de resultados en consola;
- selección por posición como problema de partida.

## 6. Concepto nuevo

`>` como pregunta “¿es mayor que?”.

## 7. Contenido visible para el estudiante

Hasta ahora elegíamos valores indicando su posición.

Pero a veces no sabemos de antemano **dónde** están los valores que buscamos.

Podemos hacerle una pregunta a R.

Lee:

```r
35 > 30
```

como:

> **¿35 es mayor que 30?**

R responde con `TRUE` o `FALSE`.

## 8. Objetivo visible

> Interpretar `>` como una pregunta que R responde con TRUE o FALSE.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `35 > 30`.
2. Ejecuta `25 > 30`.
3. Observa que R entrega una respuesta diferente en cada caso.

## 10. Starter code definitivo

```r
# ¿35 minutos es mayor que 30?
35 > 30

# ¿25 minutos es mayor que 30?
25 > 30
```

## 11. Acción esperada paso a paso

1. Ubicar el cursor en `35 > 30`.
2. Ejecutar con Ctrl + Enter.
3. Observar `TRUE`.
4. Ejecutar `25 > 30`.
5. Observar `FALSE`.
6. Relacionar las respuestas con el significado de la pregunta.

## 12. Resultado esperado en consola

```text
> 35 > 30
[1] TRUE

> 25 > 30
[1] FALSE
```

## 13. Interpretación esperada

> `TRUE` significa que la pregunta se cumple: 35 sí es mayor que 30.

> `FALSE` significa que no se cumple: 25 no es mayor que 30.

El estudiante no necesita interpretar formalmente `[1]`.

## 14. Solución interna de referencia

```r
35 > 30
25 > 30
```

## 15. Habilidad objetivo vs. respuesta computacional

Escribir directamente:

```r
TRUE
FALSE
```

produce los mismos valores visibles, pero evita formular las preguntas mediante `>`.

La habilidad objetivo es **hacer la comparación**, no adivinar la respuesta.

## 16. Checks semánticos recomendados

- se ejecuta una comparación equivalente a `35 > 30`;
- se ejecuta una comparación equivalente a `25 > 30`;
- los resultados son `TRUE` y `FALSE`;
- no exigir otros operadores;
- no exigir guardar resultados.

## 17. Estados de respuesta relevantes

- **Estado 1:** no ejecutó comparaciones.
- **Estado 2:** ejecutó solo una comparación.
- **Estado 3:** invirtió alguno de los lados o escribió `TRUE/FALSE` directamente.
- **Estado 4:** ejecutó e interpretó ambas comparaciones.

## 18. Errores previsibles

- `30 > 35`;
- `30 > 25`;
- utilizar `+`;
- escribir `TRUE` o `FALSE` directamente;
- pensar que `>` significa “la flecha apunta al número más grande”.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| `30 > 35` | Invierte la pregunta | La pregunta es **“¿35 es mayor que 30?”**. Deja 35 a la izquierda y 30 a la derecha. |
| Usa `+` | Calcula en vez de comparar | Aquí no queremos calcular un total. Queremos preguntarle a R si un valor es mayor que otro. |
| Escribe `TRUE` | Entrega respuesta sin comparación | TRUE es la respuesta correcta para 35, pero queremos que R llegue a ella mediante `35 > 30`. |
| Solo ejecuta un caso | No contrasta respuestas | Ejecuta también el segundo caso. Así podrás observar cuándo R responde FALSE. |

## 20. Pista 1 — conceptual

> Lee `>` con palabras: “es mayor que”.

## 21. Pista 2 — sintaxis/estructura

> La estructura es `valor > valor`.

## 22. Pista 3 — casi resuelta

```r
35 > 30
25 > 30
```

## 23. Mensaje de éxito

> **Usaste `>` para hacer dos preguntas y observaste respuestas TRUE y FALSE.**

## 24. Transición

> Ya sabemos preguntar por un valor. Ahora haremos la misma pregunta para todos los valores de un vector.

## 25. Nivel de andamiaje

**Muy alto.** Las dos comparaciones están completamente escritas.

## 26. Carga cognitiva

**Baja.** Solo aparece `>` como elemento nuevo; `TRUE/FALSE` ya son conocidos.

## 27. Justificación pedagógica

Mostrar un caso verdadero y uno falso evita que el estudiante interprete `TRUE` como un comportamiento fijo de `>`. Además, la apertura recupera explícitamente el límite de la selección por posición, haciendo visible la necesidad del módulo.

---

# Ejercicio 2 — La misma pregunta para todos

## 1. Función pedagógica en la secuencia

**Antes:** comprende que `>` puede responder TRUE o FALSE para un valor.

**Después:** comprende que R puede hacer la misma pregunta para cada elemento de un vector y producir una respuesta por posición.

## 2. Objetivo de aprendizaje en R

Ejecutar e interpretar una comparación aplicada a un vector completo.

## 3. Idea sobre datos

Una misma pregunta puede aplicarse sistemáticamente a varias observaciones.

## 4. Pregunta o situación sustantiva

Cinco personas tardaron:

```text
25, 40, 35, 50 y 30 minutos
```

en sus viajes.

Queremos saber:

> ¿Qué tiempos superan 30 minutos?

## 5. Prerrequisitos recuperados

- vector;
- posición;
- `>`;
- `TRUE/FALSE`;
- ejecución y consulta.

## 6. Concepto nuevo

Comparación aplicada a todos los valores de un vector.

La expresión puede describirse internamente como comparación vectorizada, pero el término no es necesario en la interfaz.

## 7. Contenido visible para el estudiante

No necesitamos preguntar por cada tiempo por separado.

Si escribimos:

```r
tiempos_viaje > 30
```

R repite la pregunta:

> **¿este tiempo supera 30?**

para cada valor.

Por eso obtendremos **una respuesta por cada tiempo**.

| Tiempo | ¿Supera 30? |
|---:|:---|
| 25 | FALSE |
| 40 | TRUE |
| 35 | TRUE |
| 50 | TRUE |
| 30 | FALSE |

## 8. Objetivo visible

> Hacer la misma pregunta para todos los valores de un vector.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `tiempos_viaje`.
2. Ejecuta `tiempos_viaje > 30`.
3. Compara cada tiempo con la respuesta que ocupa la misma posición.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# ¿Qué tiempos superan 30 minutos?
tiempos_viaje > 30
```

## 11. Acción esperada paso a paso

1. Ejecutar la asignación del vector.
2. Consultar `tiempos_viaje` si desea observarlo.
3. Ejecutar `tiempos_viaje > 30`.
4. Observar cinco respuestas.
5. Relacionar cada respuesta con el tiempo de la misma posición.

## 12. Resultado esperado en consola

```text
> tiempos_viaje > 30
[1] FALSE TRUE TRUE TRUE FALSE
```

## 13. Interpretación esperada

El estudiante debería poder reconstruir:

- 25 → FALSE;
- 40 → TRUE;
- 35 → TRUE;
- 50 → TRUE;
- 30 → FALSE.

También debería comprender que `30 > 30` es `FALSE`, porque la pregunta dice **mayor que**, no “mayor o igual”.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje > 30
```

## 15. Habilidad objetivo vs. respuesta computacional

Escribir:

```r
c(FALSE, TRUE, TRUE, TRUE, FALSE)
```

reproduce el resultado, pero evita formular la pregunta sobre los datos.

La habilidad objetivo es que R produzca las respuestas mediante:

```r
tiempos_viaje > 30
```

## 16. Checks semánticos recomendados

- `tiempos_viaje` conserva los valores esperados;
- se evalúa el vector completo contra 30;
- se usa `>`;
- resultado lógico equivalente a `c(FALSE, TRUE, TRUE, TRUE, FALSE)`;
- no exigir guardar todavía;
- no aceptar `>=` como equivalente.

## 17. Estados de respuesta relevantes

- **Estado 1:** no ejecuta la comparación.
- **Estado 2:** compara solo un elemento.
- **Estado 3:** hardcodea las respuestas o utiliza `>=`.
- **Estado 4:** compara el vector completo con `> 30`.

## 18. Errores previsibles

- `tiempos_viaje[3] > 30`;
- `tiempos_viaje >= 30`;
- esperar un solo `TRUE`;
- hardcodear el vector lógico;
- interpretar que TRUE/FALSE son nuevos datos independientes de los tiempos.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Compara un solo valor | No generaliza la pregunta | Queremos hacer la misma pregunta a los **cinco tiempos**. Usa `tiempos_viaje` completo. |
| Usa `>=` | Cambia la pregunta | La pregunta es “¿supera 30?”, por eso usamos `>`. El valor 30 no debe contar como TRUE. |
| Espera una respuesta | No comprende correspondencia | Hay cinco tiempos y R responde una vez por cada uno. Busca cinco respuestas en la consola. |
| Hardcodea TRUE/FALSE | Evita la comparación | Las respuestas coinciden, pero queremos que R las produzca comparando `tiempos_viaje` con 30. |

## 20. Pista 1 — conceptual

> Imagina que R pregunta “¿supera 30?” cinco veces, una por posición.

## 21. Pista 2 — sintaxis/estructura

> Usa el nombre completo del vector a la izquierda de `>`.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje > 30
```

## 23. Mensaje de éxito

> **R respondió una vez por cada tiempo y relacionaste cada TRUE/FALSE con su valor.**

## 24. Transición

> Ya tenemos cinco respuestas. En el siguiente ejercicio las guardaremos para poder reutilizarlas.

## 25. Nivel de andamiaje

**Muy alto.** La comparación completa ya está en el starter.

## 26. Carga cognitiva

**Baja-media.** No aparece un operador nuevo; la novedad es comprender la correspondencia uno a uno.

## 27. Justificación pedagógica

La mediación visual explícita evita uno de los saltos problemáticos del diseño anterior: el estudiante no debe inferir solo qué TRUE corresponde a qué valor.

---

# Ejercicio 3 — Guardar las respuestas

## 1. Función pedagógica en la secuencia

**Antes:** observa cinco respuestas TRUE/FALSE.

**Después:** puede guardar esas respuestas con un nombre y explicar qué contiene ese objeto.

## 2. Objetivo de aprendizaje en R

Asignar el resultado de una comparación vectorial a un objeto y consultarlo.

## 3. Idea sobre datos

El resultado de una pregunta también es información que puede guardarse y reutilizarse.

## 4. Pregunta o situación sustantiva

Seguimos preguntando:

> ¿Qué tiempos superan 30 minutos?

Ahora queremos conservar las respuestas para usarlas después.

## 5. Prerrequisitos recuperados

- `<-`;
- objetos;
- asignar vs. consultar;
- vector;
- `>`;
- `TRUE/FALSE`.

## 6. Concepto nuevo

Una serie de respuestas TRUE/FALSE puede guardarse como un objeto que representa una pregunta.

El término **condición** puede introducirse después de haber observado el contenido.

## 7. Contenido visible para el estudiante

La expresión:

```r
tiempos_viaje > 30
```

produce cinco respuestas.

Podemos guardarlas:

```r
supera_30 <- tiempos_viaje > 30
```

El nombre `supera_30` se puede leer como una pregunta:

> **¿supera 30?**

Importante: `supera_30` no contiene los tiempos. Contiene las respuestas `TRUE/FALSE`.

## 8. Objetivo visible

> Guardar las respuestas TRUE/FALSE para poder reutilizarlas.

## 9. Instrucciones visibles / Tu tarea

1. Completa la línea que crea `supera_30`.
2. Ejecuta la asignación.
3. Ejecuta `supera_30` para ver qué quedó guardado.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# Guarda las respuestas a: ¿supera 30?
supera_30 <-


# Muestra las respuestas guardadas
supera_30
```

## 11. Acción esperada paso a paso

1. Ejecutar `tiempos_viaje`.
2. Completar:

```r
supera_30 <- tiempos_viaje > 30
```

3. Ejecutar la asignación.
4. Ejecutar `supera_30`.
5. Observar el vector lógico resultante.

## 12. Resultado esperado en consola

```text
> supera_30 <- tiempos_viaje > 30

> supera_30
[1] FALSE TRUE TRUE TRUE FALSE
```

## 13. Interpretación esperada

> `supera_30` contiene una respuesta para cada tiempo.

El estudiante debería poder explicar:

- primera respuesta FALSE → 25 no supera 30;
- segunda TRUE → 40 sí;
- tercera TRUE → 35 sí;
- cuarta TRUE → 50 sí;
- quinta FALSE → 30 no.

Después de comprender esto, puede introducirse suavemente:

> Estas respuestas guardadas representan una **condición**.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

supera_30
```

## 15. Habilidad objetivo vs. respuesta computacional

Esto:

```r
supera_30 <- c(FALSE, TRUE, TRUE, TRUE, FALSE)
```

produce el estado correcto, pero no demuestra que la persona sabe construir las respuestas preguntando por `tiempos_viaje`.

También es incompleto ejecutar:

```r
tiempos_viaje > 30
```

sin guardar el resultado.

## 16. Checks semánticos recomendados

- existe `supera_30`;
- es logical;
- longitud 5;
- valores equivalentes a `c(FALSE, TRUE, TRUE, TRUE, FALSE)`;
- deriva de `tiempos_viaje > 30`;
- se consulta explícitamente `supera_30`;
- no exigir forma compacta ni otros comparadores.

## 17. Estados de respuesta relevantes

- **Estado 1:** no existe `supera_30`.
- **Estado 2:** ejecuta comparación pero no la guarda.
- **Estado 3:** hardcodea las respuestas.
- **Estado 4:** construye `supera_30` correctamente pero no lo consulta.
- **Estado 5:** construye y consulta correctamente.

## 18. Errores previsibles

- `supera_30 <- tiempos_viaje`;
- `supera_30 <- c(FALSE, TRUE, TRUE, TRUE, FALSE)`;
- `supera_30 <- "tiempos_viaje > 30"`;
- ejecutar solo `tiempos_viaje > 30`;
- llamar al objeto con un nombre que haga parecer que contiene los valores seleccionados.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Guarda `tiempos_viaje` | Confunde datos con respuestas | `supera_30` debe guardar las respuestas a “¿supera 30?”, no los minutos originales. |
| Hardcodea TRUE/FALSE | Resultado correcto, estrategia incompleta | Las respuestas coinciden. Ahora haz que R las produzca comparando `tiempos_viaje` con 30. |
| Comillas | Convierte código en texto | Queremos que R evalúe la comparación. Escribe `tiempos_viaje > 30` sin comillas. |
| Compara pero no guarda | Falta reutilización | La pregunta ya funciona. Ahora guarda esas respuestas en `supera_30` usando `<-`. |
| No consulta | No verifica contenido | `supera_30` ya está creado. Escribe su nombre en una línea para ver qué contiene. |

## 20. Pista 1 — conceptual

> A la derecha de `<-` debe ir la pregunta que ya usaste en el ejercicio anterior.

## 21. Pista 2 — sintaxis/estructura

> La forma es `nombre <- vector > valor`.

## 22. Pista 3 — casi resuelta

```r
supera_30 <- tiempos_viaje > 30
```

## 23. Mensaje de éxito

> **Guardaste las respuestas TRUE/FALSE y comprobaste qué contiene `supera_30`.**

## 24. Transición

> Ya tenemos las respuestas guardadas. Ahora veremos cómo pueden ayudarnos a quedarnos solo con algunos tiempos.

## 25. Nivel de andamiaje

**Alto.** El estudiante completa una sola asignación con una estructura que ya conoce.

## 26. Carga cognitiva

**Baja-media.** No aparece sintaxis nueva; la principal novedad es conceptual.

## 27. Justificación pedagógica

Separar “hacer la pregunta” de “usar las respuestas para seleccionar” evita introducir demasiadas relaciones a la vez. Además, el nombre `supera_30` hace visible que el objeto contiene respuestas, no tiempos seleccionados.

---

# Ejercicio 4 — TRUE conserva, FALSE deja fuera

## 1. Función pedagógica en la secuencia

**Antes:** tiene un vector de datos y un objeto con respuestas TRUE/FALSE.

**Después:** comprende, mediante un worked example, cómo esas respuestas pueden utilizarse dentro de `[]` para conservar ciertos valores.

## 2. Objetivo de aprendizaje en R

Ejecutar e interpretar una selección con:

```r
vector[condicion]
```

sin tener que producir todavía esa estructura.

## 3. Idea sobre datos

Cada respuesta TRUE/FALSE ocupa una posición que corresponde a un valor del vector original.

Dentro de `[]`:

- `TRUE` conserva el valor de esa posición;
- `FALSE` lo deja fuera.

## 4. Pregunta o situación sustantiva

Queremos pasar de saber **qué tiempos cumplen** a quedarnos efectivamente con esos tiempos.

## 5. Prerrequisitos recuperados

- `[]`;
- posición;
- `supera_30`;
- `TRUE/FALSE`;
- correspondencia posición a posición.

## 6. Concepto nuevo

Uso de una condición dentro de `[]` para seleccionar valores.

El término técnico “selección lógica” puede quedar en documentación interna. No es necesario en la interfaz.

## 7. Contenido visible para el estudiante

Ya tenemos:

```text
TIEMPOS      25     40     35     50     30
RESPUESTAS   FALSE  TRUE   TRUE   TRUE   FALSE
```

Ahora R puede usar esas respuestas dentro de `[]`.

Piensa así:

> **TRUE → conserva el tiempo de esta posición**  
> **FALSE → déjalo fuera**

Por eso:

```r
tiempos_viaje[supera_30]
```

conservará 40, 35 y 50.

## 8. Objetivo visible

> Observar cómo TRUE y FALSE permiten seleccionar valores.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `supera_30`.
2. Observa sus cinco respuestas.
3. Ejecuta `tiempos_viaje[supera_30]`.
4. Compara qué posiciones tenían TRUE y qué tiempos quedaron.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

# Primero mira las respuestas
supera_30

# Ahora usa esas respuestas para conservar los tiempos que cumplen
tiempos_viaje[supera_30]
```

## 11. Acción esperada paso a paso

1. Ejecutar la asignación de `tiempos_viaje`.
2. Ejecutar la asignación de `supera_30`.
3. Consultar `supera_30`.
4. Observar `FALSE TRUE TRUE TRUE FALSE`.
5. Ejecutar `tiempos_viaje[supera_30]`.
6. Observar `40 35 50`.
7. Relacionar ambos resultados.

## 12. Resultado esperado en consola

```text
> supera_30
[1] FALSE TRUE TRUE TRUE FALSE

> tiempos_viaje[supera_30]
[1] 40 35 50
```

## 13. Interpretación esperada

> R conservó los tiempos de las posiciones donde `supera_30` tenía TRUE.

El estudiante debería poder explicar la correspondencia:

```text
25     40     35     50     30
FALSE  TRUE   TRUE   TRUE   FALSE
       ↓      ↓      ↓
       40     35     50
```

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

supera_30 <- tiempos_viaje > 30

supera_30
tiempos_viaje[supera_30]
```

## 15. Habilidad objetivo vs. respuesta computacional

Este es un worked example.

No se exige todavía que el estudiante escriba `tiempos_viaje[supera_30]` desde cero.

La habilidad objetivo es **comprender el mecanismo**.

Si modifica el código para usar posiciones:

```r
tiempos_viaje[c(2, 3, 4)]
```

obtendrá el mismo resultado, pero perderá el objetivo del ejercicio.

## 16. Checks semánticos recomendados

- se consulta `supera_30`;
- se ejecuta `tiempos_viaje[supera_30]`;
- resultado equivalente a `c(40, 35, 50)`;
- no exigir producción autónoma;
- no exigir forma compacta `tiempos_viaje[tiempos_viaje > 30]`.

## 17. Estados de respuesta relevantes

- **Estado 1:** no ejecuta las respuestas.
- **Estado 2:** ejecuta `supera_30` pero no la selección.
- **Estado 3:** reemplaza condición por posiciones.
- **Estado 4:** ejecuta ambas expresiones e interpreta la relación.

## 18. Errores previsibles

- `supera_30[tiempos_viaje]`;
- `tiempos_viaje[c(2, 3, 4)]`;
- pensar que `supera_30` contiene los tiempos;
- ejecutar solo la última línea sin observar primero las respuestas;
- interpretar `FALSE` como valor numérico cero.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| `supera_30[tiempos_viaje]` | Invierte datos y respuestas | Los valores que queremos conservar están en `tiempos_viaje`. `supera_30` solo indica qué posiciones cumplen. |
| Usa posiciones | Evita el nuevo mecanismo | Las posiciones 2, 3 y 4 producen el mismo resultado aquí. En este ejercicio queremos observar cómo TRUE/FALSE pueden hacer esa selección. |
| Confunde contenido | Cree que `supera_30` guarda minutos | Ejecuta primero `supera_30`. Verás que contiene respuestas TRUE/FALSE, no tiempos. |
| No observa condición | Omite mediación conceptual | Mira primero `supera_30`. Después compara sus TRUE con los tiempos que aparecen en la selección. |

## 20. Pista 1 — conceptual

> Mira qué posiciones tienen TRUE. Esos son los valores que R conservará.

## 21. Pista 2 — sintaxis/estructura

> Los tiempos quedan afuera de los corchetes; las respuestas van dentro.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje[supera_30]
```

## 23. Mensaje de éxito

> **Observaste cómo TRUE conserva valores y FALSE los deja fuera.**

## 24. Transición

> Ya viste el mecanismo completo. Ahora completarás tú una selección similar.

## 25. Nivel de andamiaje

**Muy alto.** Todo el código relevante está dado.

## 26. Carga cognitiva

**Media.** La relación entre dos vectores por posición es conceptualmente importante, pero la producción de código es mínima.

## 27. Justificación pedagógica

Este worked example resuelve el principal salto del diseño anterior. La persona construye el modelo mental antes de que el sistema le exija producir la sintaxis.

---

# Ejercicio 5 — Ahora selecciona tú

## 1. Función pedagógica en la secuencia

**Antes:** observó cómo `vector[condicion]` conserva los valores asociados a TRUE.

**Después:** puede completar una selección utilizando un objeto de respuestas ya creado.

## 2. Objetivo de aprendizaje en R

Completar correctamente:

```r
vector[condicion]
```

cuando la condición ya existe.

## 3. Idea sobre datos

Una pregunta ya respondida puede reutilizarse para seleccionar los datos que cumplen.

## 4. Pregunta o situación sustantiva

Los tiempos cambiaron:

```text
20, 45, 25, 50 y 35
```

La pregunta sigue siendo:

> ¿Qué tiempos superan 30 minutos?

`supera_30` ya está creado. Solo falta usar sus respuestas para seleccionar.

## 5. Prerrequisitos recuperados

- `[]`;
- `supera_30`;
- TRUE conserva / FALSE deja fuera;
- lectura de objetos.

## 6. Concepto nuevo

Ninguno. Es práctica controlada del mecanismo de E4.

## 7. Contenido visible para el estudiante

La pregunta ya está respondida:

```r
supera_30 <- tiempos_viaje > 30
```

Ahora completa solamente qué debe ir dentro de `[]`.

Recuerda:

> `supera_30` contiene una respuesta TRUE/FALSE para cada tiempo.

## 8. Objetivo visible

> Usar unas respuestas ya guardadas para seleccionar los tiempos que cumplen.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta las primeras líneas.
2. Mira `supera_30`.
3. Reemplaza `_____` por el objeto que contiene las respuestas.
4. Ejecuta `viajes_seleccionados`.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(20, 45, 25, 50, 35)

supera_30 <- tiempos_viaje > 30

# Mira las respuestas
supera_30

# Usa esas respuestas para seleccionar
viajes_seleccionados <- tiempos_viaje[_____]

viajes_seleccionados
```

## 11. Acción esperada paso a paso

1. Ejecutar `tiempos_viaje`.
2. Ejecutar `supera_30 <- tiempos_viaje > 30`.
3. Consultar `supera_30`.
4. Observar:

```text
FALSE TRUE FALSE TRUE TRUE
```

5. Reemplazar `_____` por `supera_30`.
6. Ejecutar la asignación de `viajes_seleccionados`.
7. Consultar el resultado.

## 12. Resultado esperado en consola

```text
> supera_30
[1] FALSE TRUE FALSE TRUE TRUE

> viajes_seleccionados
[1] 45 50 35
```

## 13. Interpretación esperada

> Los valores 45, 50 y 35 quedaron seleccionados porque sus posiciones correspondían a TRUE.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(20, 45, 25, 50, 35)

supera_30 <- tiempos_viaje > 30

supera_30

viajes_seleccionados <- tiempos_viaje[supera_30]

viajes_seleccionados
```

## 15. Habilidad objetivo vs. respuesta computacional

Estas alternativas producen el resultado correcto, pero evitan la habilidad objetivo:

```r
viajes_seleccionados <- c(45, 50, 35)
```

```r
viajes_seleccionados <- tiempos_viaje[c(2, 4, 5)]
```

La respuesta debe reconocerse como numéricamente correcta pero pedagógicamente incompleta.

## 16. Checks semánticos recomendados

- `supera_30` correcto y derivado de la comparación;
- `viajes_seleccionados` equivalente a `c(45, 50, 35)`;
- selección realizada desde `tiempos_viaje` usando `supera_30`;
- no aceptar posiciones como estrategia equivalente;
- no exigir forma compacta.

## 17. Estados de respuesta relevantes

- **Estado 1:** no completa `_____`.
- **Estado 2:** escribe posiciones.
- **Estado 3:** hardcodea los valores finales.
- **Estado 4:** usa objeto incorrecto.
- **Estado 5:** usa `supera_30` correctamente.

## 18. Errores previsibles

- `tiempos_viaje[c(2, 4, 5)]`;
- `c(45, 50, 35)`;
- `supera_30[tiempos_viaje]`;
- `tiempos_viaje[tiempos_viaje]`;
- dejar `_____`;
- escribir `"supera_30"` con comillas.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Usa posiciones | Regresa a estrategia anterior | Esas posiciones funcionan con estos valores. Aquí queremos usar las respuestas TRUE/FALSE que ya guardaste en `supera_30`. |
| Hardcodea | Entrega datos sin seleccionar | 45, 50 y 35 son correctos. Ahora haz que R los seleccione usando `supera_30`. |
| Invierte objetos | No distingue datos/condición | Los tiempos están en `tiempos_viaje`. Las respuestas que deciden cuáles conservar están en `supera_30`. |
| Usa comillas | Trata nombre como texto | `supera_30` es un objeto. Escríbelo sin comillas dentro de `[]`. |

## 20. Pista 1 — conceptual

> Dentro de los corchetes debe ir el objeto que contiene TRUE/FALSE.

## 21. Pista 2 — sintaxis/estructura

> La forma es `datos[respuestas]`.

## 22. Pista 3 — casi resuelta

```r
viajes_seleccionados <- tiempos_viaje[supera_30]
```

## 23. Mensaje de éxito

> **Usaste las respuestas guardadas para seleccionar los tiempos que cumplen.**

## 24. Transición

> Hasta ahora parte del código estaba preparado. En el siguiente ejercicio construirás tú la pregunta y la selección.

## 25. Nivel de andamiaje

**Alto-medio.** Solo se completa la pieza central dentro de `[]`.

## 26. Carga cognitiva

**Baja-media.** No hay sintaxis nueva y la persona toma una sola decisión.

## 27. Justificación pedagógica

El completion problem reduce el espacio de búsqueda después del worked example. Permite practicar el mecanismo sin exigir todavía reconstruir todo el ciclo.

---

# Ejercicio 6 — La pregunta sigue funcionando

## 1. Función pedagógica en la secuencia

**Antes:** completa una selección cuando la condición ya está creada.

**Después:** construye de manera relativamente autónoma el ciclo completo pregunta → respuestas → selección.

## 2. Objetivo de aprendizaje en R

Crear una condición con `>` y utilizarla dentro de `[]` para seleccionar valores.

## 3. Idea sobre datos

La pregunta sigue siendo válida aunque los valores cambien. Por eso una condición es más general que memorizar posiciones.

## 4. Pregunta o situación sustantiva

Ahora los tiempos son:

```text
45, 20, 35, 25 y 50
```

Queremos responder exactamente la misma pregunta:

> ¿Qué tiempos superan 30 minutos?

No necesitamos buscar manualmente sus posiciones.

## 5. Prerrequisitos recuperados

- comparación vectorial;
- `<-`;
- `supera_30`;
- `[]`;
- TRUE/FALSE como selector.

## 6. Concepto nuevo

Ninguno sintáctico.

La nueva capacidad es **generalizar la estrategia** cuando cambian los datos.

## 7. Contenido visible para el estudiante

Los valores cambiaron, pero la pregunta sigue siendo la misma:

> **¿Qué tiempos superan 30 minutos?**

No busques manualmente sus posiciones.

Haz que R responda la pregunta y luego usa esas respuestas para seleccionar.

## 8. Objetivo visible

> Construir una pregunta y usar sus respuestas para seleccionar valores nuevos.

## 9. Instrucciones visibles / Tu tarea

1. Crea `supera_30` preguntando si cada tiempo supera 30.
2. Crea `viajes_seleccionados` usando `supera_30` dentro de `[]`.
3. Ejecuta `viajes_seleccionados`.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(45, 20, 35, 25, 50)

# ¿Qué tiempos superan 30?
supera_30 <-


# Usa esas respuestas para seleccionar
viajes_seleccionados <-


# Muestra el resultado
viajes_seleccionados
```

## 11. Acción esperada paso a paso

1. Ejecutar el vector.
2. Completar:

```r
supera_30 <- tiempos_viaje > 30
```

3. Ejecutar y, si necesita, consultar `supera_30`.
4. Completar:

```r
viajes_seleccionados <- tiempos_viaje[supera_30]
```

5. Ejecutar.
6. Consultar `viajes_seleccionados`.

## 12. Resultado esperado en consola

Si consulta la condición:

```text
> supera_30
[1] TRUE FALSE TRUE FALSE TRUE
```

Resultado final:

```text
> viajes_seleccionados
[1] 45 35 50
```

## 13. Interpretación esperada

> Aunque los valores cambiaron de posición, la pregunta `tiempos_viaje > 30` volvió a identificar correctamente 45, 35 y 50.

La idea central:

> **las posiciones pueden cambiar; la pregunta sigue siendo la misma.**

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(45, 20, 35, 25, 50)

supera_30 <- tiempos_viaje > 30

viajes_seleccionados <-
  tiempos_viaje[supera_30]

viajes_seleccionados
```

## 15. Habilidad objetivo vs. respuesta computacional

Esto:

```r
viajes_seleccionados <- tiempos_viaje[c(1, 3, 5)]
```

produce el resultado correcto para estos datos, pero no construye una regla reutilizable.

También es incompleto:

```r
supera_30 <- c(TRUE, FALSE, TRUE, FALSE, TRUE)
```

porque evita formular la pregunta desde `tiempos_viaje`.

## 16. Checks semánticos recomendados

- `supera_30` existe;
- es logical y correcto;
- deriva de `tiempos_viaje > 30`;
- `viajes_seleccionados` equivale a `c(45, 35, 50)`;
- la selección utiliza `supera_30`;
- distinguir posiciones/hardcodeo como estrategia parcial;
- no exigir forma compacta.

## 17. Estados de respuesta relevantes

- **Estado 1:** no crea ninguno de los objetos.
- **Estado 2:** crea condición pero no selección.
- **Estado 3:** hardcodea condición o posiciones.
- **Estado 4:** selección correcta pero condición incorrecta/no derivada de datos.
- **Estado 5:** ciclo completo correcto.

## 18. Errores previsibles

- `supera_30 <- c(TRUE, FALSE, TRUE, FALSE, TRUE)`;
- `viajes_seleccionados <- tiempos_viaje[c(1, 3, 5)]`;
- `supera_30 <- tiempos_viaje >= 30`;
- `viajes_seleccionados <- supera_30[tiempos_viaje]`;
- seleccionar desde objeto equivocado;
- cambiar el vector para que coincida con posiciones previas.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Hardcodea condición | Evita la pregunta | Las respuestas TRUE/FALSE son correctas. Ahora haz que R las produzca con `tiempos_viaje > 30`. |
| Usa posiciones | No generaliza | 1, 3 y 5 funcionan ahora. Queremos que el código siga respondiendo aunque los tiempos cambien de posición. Usa `supera_30`. |
| Usa `>=` | Cambia criterio | La pregunta sigue siendo “¿supera 30?”. Usa `>`. |
| Invierte datos/condición | Confunde roles | `tiempos_viaje` contiene los datos; `supera_30` indica cuáles conservar. |
| Solo crea condición | Ciclo incompleto | La pregunta ya está respondida. Ahora usa esas respuestas dentro de `[]` para seleccionar los tiempos. |

## 20. Pista 1 — conceptual

> Primero responde la pregunta. Después usa esas respuestas para seleccionar.

## 21. Pista 2 — sintaxis/estructura

> Necesitas estas dos formas: `nombre <- vector > valor` y `resultado <- vector[respuestas]`.

## 22. Pista 3 — casi resuelta

```r
supera_30 <- tiempos_viaje > 30

viajes_seleccionados <-
  tiempos_viaje[supera_30]
```

## 23. Mensaje de éxito

> **Construiste una regla que sigue funcionando aunque cambien los valores.**

## 24. Transición

> Hasta ahora preguntamos por cantidades. También podemos hacer preguntas de igualdad sobre texto.

## 25. Nivel de andamiaje

**Medio.** Los nombres y la estructura de la tarea están dados, pero las dos expresiones centrales quedan al estudiante.

## 26. Carga cognitiva

**Media.** Integra habilidades ya practicadas sin agregar sintaxis nueva.

## 27. Justificación pedagógica

La idea valiosa del antiguo ejercicio “No memorices las posiciones” se conserva, pero ya no se presenta como comparación compleja entre estrategias. Se demuestra mediante producción con datos nuevos, después de worked example y completion problem.

---

# Ejercicio 7 — También podemos preguntar por texto

## 1. Función pedagógica en la secuencia

**Antes:** domina de manera inicial el ciclo numérico con `>`.

**Después:** reconoce que la misma lógica de pregunta/respuesta puede aplicarse a texto mediante `==`.

## 2. Objetivo de aprendizaje en R

Comparar valores de texto con `==` y guardar las respuestas.

## 3. Idea sobre datos

No todas las preguntas son sobre cantidades. También podemos preguntar si una categoría es igual a un valor específico.

## 4. Pregunta o situación sustantiva

Tenemos cuatro carreras:

```text
Sociología, Historia, Sociología y Antropología
```

Queremos preguntar:

> ¿Esta carrera es Sociología?

## 5. Prerrequisitos recuperados

- vectores de texto;
- comillas;
- `TRUE/FALSE`;
- comparación aplicada a un vector;
- `<-`;
- objeto como conjunto de respuestas.

## 6. Concepto nuevo

`==` como operador de igualdad:

> **¿es igual a?**

También se recupera la diferencia:

- `<-` = guardar;
- `==` = comparar.

## 7. Contenido visible para el estudiante

Hasta ahora preguntamos:

```r
tiempos_viaje > 30
```

es decir:

> **¿es mayor que 30?**

También podemos preguntar por texto.

Para saber si cada carrera es `"Sociología"`, usamos:

```r
carreras == "Sociología"
```

Lee `==` como:

> **¿es igual a?**

Recuerda:

```text
<-  guarda
==  compara
```

## 8. Objetivo visible

> Preguntar si cada valor de texto es igual a una categoría.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `carreras`.
2. Completa `es_sociologia` usando `==`.
3. Ejecuta `es_sociologia`.
4. Observa qué posiciones contienen TRUE.

## 10. Starter code definitivo

```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)

# ¿Qué valores son iguales a "Sociología"?
es_sociologia <-


# Muestra las respuestas
es_sociologia
```

## 11. Acción esperada paso a paso

1. Ejecutar `carreras`.
2. Completar:

```r
es_sociologia <- carreras == "Sociología"
```

3. Ejecutar la asignación.
4. Consultar `es_sociologia`.
5. Relacionar TRUE con las posiciones 1 y 3.

## 12. Resultado esperado en consola

```text
> es_sociologia
[1] TRUE FALSE TRUE FALSE
```

## 13. Interpretación esperada

> Las posiciones 1 y 3 contienen `"Sociología"`, por eso allí aparece TRUE.

El ejercicio no exige utilizar `es_sociologia` para seleccionar otra variable.

## 14. Solución interna de referencia

```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)

es_sociologia <-
  carreras == "Sociología"

es_sociologia
```

## 15. Habilidad objetivo vs. respuesta computacional

Hardcodear:

```r
es_sociologia <- c(TRUE, FALSE, TRUE, FALSE)
```

produce el resultado correcto, pero evita practicar `==`.

También sería prematuro resolver el problema mediante posiciones:

```r
carreras[c(1, 3)]
```

porque la habilidad objetivo es formular una pregunta de igualdad.

## 16. Checks semánticos recomendados

- `es_sociologia` existe;
- es logical;
- valores `TRUE FALSE TRUE FALSE`;
- deriva de `carreras == "Sociología"`;
- `"Sociología"` se trata como texto;
- no enseñar `=` como asignación alternativa;
- no exigir selección de otro vector;
- no introducir `!=`.

## 17. Estados de respuesta relevantes

- **Estado 1:** no crea `es_sociologia`.
- **Estado 2:** texto sin comillas.
- **Estado 3:** usa `=` o confunde `<-` con `==`.
- **Estado 4:** hardcodea respuestas.
- **Estado 5:** construye y consulta correctamente.

## 18. Errores previsibles

- `carreras == Sociología`;
- `carreras = "Sociología"`;
- `es_sociologia == carreras == "Sociología"`;
- hardcodear lógicos;
- usar `>`;
- seleccionar las posiciones 1 y 3 directamente.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Texto sin comillas | Olvida cómo representar texto | `Sociología` es texto. Escríbelo como `"Sociología"`. |
| Usa `=` | Confunde igualdad | Para preguntar si dos valores son iguales usamos `==`. |
| Usa `==` para asignar | Confunde guardar/comparar | Usa `<-` para guardar el resultado en `es_sociologia`. Dentro de la expresión, usa `==` para comparar. |
| Hardcodea | Evita la pregunta | Las respuestas son correctas. Haz que R las produzca comparando `carreras` con `"Sociología"`. |
| Usa posiciones | Evita `==` | Las posiciones 1 y 3 contienen Sociología, pero aquí queremos que R las identifique mediante una pregunta de igualdad. |

## 20. Pista 1 — conceptual

> La pregunta es: “¿cada carrera es igual a Sociología?”.

## 21. Pista 2 — sintaxis/estructura

> Usa `==` entre el vector y el texto.

## 22. Pista 3 — casi resuelta

```r
es_sociologia <-
  carreras == "Sociología"
```

## 23. Mensaje de éxito

> **Usaste `==` para hacer una pregunta de igualdad sobre texto.**

## 24. Transición

> Ya sabes formular preguntas sobre números y texto. El desafío final volverá al ciclo central y lo aplicará en un contexto nuevo.

## 25. Nivel de andamiaje

**Alto.** Aparece un operador nuevo, por lo que se entrega todo el contexto y la estructura de la tarea.

## 26. Carga cognitiva

**Baja-media.** La lógica pregunta → TRUE/FALSE ya es conocida; solo cambia el operador y el tipo de dato.

## 27. Justificación pedagógica

`==` se conserva como extensión secundaria porque transfiere una estructura ya consolidada sin introducir selección cruzada. El andamiaje vuelve a subir deliberadamente ante la nueva sintaxis.

---

# Ejercicio 8 — Mini desafío: encuentra los valores que cumplen

## 1. Función pedagógica en la secuencia

**Antes:** ha practicado pregunta → respuestas → selección con tiempos de viaje.

**Después:** transfiere autónomamente el ciclo central a nuevos datos, nuevos nombres y un nuevo umbral.

## 2. Objetivo de aprendizaje en R

Construir una condición con `>` y utilizarla para seleccionar valores en un contexto nuevo.

## 3. Idea sobre datos

Una misma estrategia puede reutilizarse para distintas preguntas y distintos datos.

## 4. Pregunta o situación sustantiva

Cinco personas declararon estas horas semanales de cuidado:

```text
6, 12, 8, 15 y 10
```

Queremos responder:

> **¿Qué valores superan 10 horas?**

## 5. Prerrequisitos recuperados

- vectores;
- `>`;
- `<-`;
- `TRUE/FALSE`;
- `[]`;
- condición guardada;
- selección mediante condición.

## 6. Concepto nuevo

Ninguno.

Este ejercicio mide transferencia del ciclo central.

## 7. Contenido visible para el estudiante

Ya no trabajaremos con tiempos de viaje.

Cinco personas declararon estas horas semanales de cuidado:

**6, 12, 8, 15 y 10 horas.**

Queremos encontrar:

> **¿Qué valores superan 10 horas?**

Hazlo en dos pasos:

1. guarda las respuestas TRUE/FALSE;
2. usa esas respuestas para seleccionar los valores.

## 8. Objetivo visible

> Transferir el ciclo pregunta → respuestas → selección a nuevos datos.

## 9. Instrucciones visibles / Tu tarea

1. Completa `supera_10` preguntando si cada valor de `horas_cuidado` supera 10.
2. Completa `horas_seleccionadas` usando `supera_10` dentro de `[]`.
3. Ejecuta `horas_seleccionadas`.
4. Interpreta el resultado.

## 10. Starter code definitivo

```r
horas_cuidado <- c(6, 12, 8, 15, 10)

# ¿Qué valores superan 10?
supera_10 <-


# Selecciona esos valores
horas_seleccionadas <-


# Muestra el resultado
horas_seleccionadas
```

## 11. Acción esperada paso a paso

1. Ejecutar `horas_cuidado`.
2. Completar:

```r
supera_10 <- horas_cuidado > 10
```

3. Ejecutar la condición.
4. Completar:

```r
horas_seleccionadas <-
  horas_cuidado[supera_10]
```

5. Ejecutar.
6. Consultar `horas_seleccionadas`.
7. Interpretar `12 15`.

## 12. Resultado esperado en consola

Si consulta la condición:

```text
> supera_10
[1] FALSE TRUE FALSE TRUE FALSE
```

Resultado final:

```text
> horas_seleccionadas
[1] 12 15
```

## 13. Interpretación esperada

> De los cinco valores, 12 y 15 son los únicos que superan 10 horas.

También debe comprender por qué 10 queda fuera:

> la pregunta es “¿supera 10?”, no “¿es 10 o más?”.

## 14. Solución interna de referencia

```r
horas_cuidado <- c(6, 12, 8, 15, 10)

supera_10 <-
  horas_cuidado > 10

horas_seleccionadas <-
  horas_cuidado[supera_10]

horas_seleccionadas
```

## 15. Habilidad objetivo vs. respuesta computacional

Estas respuestas son computacionalmente correctas pero pedagógicamente incompletas:

```r
horas_seleccionadas <- c(12, 15)
```

```r
horas_seleccionadas <- horas_cuidado[c(2, 4)]
```

```r
supera_10 <- c(FALSE, TRUE, FALSE, TRUE, FALSE)
```

El objetivo es construir la pregunta desde los datos y reutilizar sus respuestas.

## 16. Checks semánticos recomendados

- `horas_cuidado` conserva `c(6, 12, 8, 15, 10)`;
- `supera_10` es logical correcto;
- deriva de `horas_cuidado > 10`;
- `horas_seleccionadas` equivale a `c(12, 15)`;
- se obtiene mediante `horas_cuidado[supera_10]`;
- distinguir hardcodeo y posiciones como estrategia parcial;
- no exigir `==`;
- no exigir forma compacta;
- no introducir operadores nuevos.

## 17. Estados de respuesta relevantes

- **Estado 1:** no crea condición.
- **Estado 2:** crea condición pero no selección.
- **Estado 3:** hardcodea condición.
- **Estado 4:** usa posiciones o hardcodea resultado.
- **Estado 5:** ciclo completo correcto.

## 18. Errores previsibles

- `horas_cuidado >= 10`;
- `supera_10 <- c(FALSE, TRUE, FALSE, TRUE, FALSE)`;
- `horas_seleccionadas <- horas_cuidado[c(2, 4)]`;
- `horas_seleccionadas <- c(12, 15)`;
- invertir datos y condición;
- usar `== 10`.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión | Feedback final |
|---|---|---|
| Usa `>=` | Cambia la pregunta | Queremos valores que **superen** 10. Usa `>` para que 10 quede fuera. |
| Hardcodea condición | Evita formular pregunta | Las respuestas TRUE/FALSE coinciden. Ahora haz que R las produzca preguntando si `horas_cuidado` supera 10. |
| Usa posiciones | Regresa a selección conocida | Las posiciones 2 y 4 funcionan con estos datos. El desafío es encontrar los valores mediante la pregunta. |
| Hardcodea resultado | Resultado correcto, estrategia incompleta | 12 y 15 son correctos. Ahora usa `supera_10` para que R los seleccione desde `horas_cuidado`. |
| Invierte objetos | Confunde datos/condición | Los valores están en `horas_cuidado`; `supera_10` contiene las respuestas que indican cuáles conservar. |

## 20. Pista 1 — conceptual

> Resuelve una cosa a la vez: primero pregunta “¿supera 10?”, después usa esas respuestas para seleccionar.

## 21. Pista 2 — sintaxis/estructura

> La primera línea usa `>`. La segunda usa `[]`.

## 22. Pista 3 — casi resuelta

```r
supera_10 <-
  horas_cuidado > 10

horas_seleccionadas <-
  horas_cuidado[supera_10]
```

## 23. Mensaje de éxito

> **Formulaste una pregunta sobre nuevos datos y utilizaste sus respuestas para seleccionar los valores que cumplen.**

## 24. Transición

> Ya puedes pasar de seleccionar posiciones conocidas a hacer preguntas sobre los valores y usar las respuestas para decidir cuáles conservar.

## 25. Nivel de andamiaje

**Medio-bajo dentro del módulo.** El contexto, los objetos y los comentarios están dados, pero el estudiante debe construir las dos expresiones centrales.

## 26. Carga cognitiva

**Media.** Integra habilidades ya practicadas, pero mantiene una sola pregunta, una sola condición y una sola selección.

## 27. Justificación pedagógica

El desafío evalúa transferencia real cambiando contexto, vector, umbral y nombres sin apilar dos pipelines ni introducir selección entre vectores. La autonomía aumenta sin elevar innecesariamente la carga.

---

# Auditoría final del módulo

## 1. Auditoría de secuencia

| Ejercicio | Capacidad antes | Capacidad después | Sintaxis nueva | Carga | Andamiaje |
|---|---|---|---|---|---|
| E1 — De posiciones a preguntas | Selecciona por posición | Interpreta una pregunta con `>` | `>` | Baja | Muy alto |
| E2 — La misma pregunta para todos | Compara un valor | Relaciona una respuesta con cada valor | `vector > valor` | Baja-media | Muy alto |
| E3 — Guardar las respuestas | Observa TRUE/FALSE | Guarda y consulta respuestas | Ninguna nueva | Baja-media | Alto |
| E4 — TRUE conserva, FALSE deja fuera | Tiene respuestas guardadas | Comprende `vector[condicion]` | `vector[condicion]` dado | Media | Muy alto |
| E5 — Ahora selecciona tú | Comprende mecanismo | Completa selección por condición | Ninguna nueva | Baja-media | Alto-medio |
| E6 — La pregunta sigue funcionando | Completa selección | Produce condición + selección | Ninguna nueva | Media | Medio |
| E7 — También podemos preguntar por texto | Domina pregunta numérica | Formula igualdad sobre texto | `==` | Baja-media | Alto |
| E8 — Mini desafío | Habilidades separadas | Transfiere ciclo completo | Ninguna nueva | Media | Medio-bajo |

Ningún ejercicio alcanza carga media-alta o alta.

---

## 2. Auditoría de prerrequisitos

### E1

Recupera:

- `TRUE/FALSE`;
- ejecución;
- idea de selección por posición como punto de partida.

Introduce solamente `>`.

### E2

Utiliza:

- vector ya conocido;
- `>` de E1.

La única novedad conceptual es que la pregunta se repite para todos los valores.

### E3

Utiliza:

- comparación vectorial de E2;
- `<-` y consulta aprendidos en M1.

No incorpora nueva sintaxis.

### E4

Utiliza:

- `supera_30` de E3;
- `[]` aprendido en M2;
- correspondencia posición a posición.

La sintaxis nueva se presenta como worked example, no como producción.

### E5

Practica exactamente el mecanismo observado en E4.

No hay prerrequisito oculto.

### E6

Integra E3 + E5:

- crear respuestas;
- usar respuestas para seleccionar.

La producción completa aparece después de observación y completion problem.

### E7

Recupera:

- comparación vectorial;
- texto con comillas;
- TRUE/FALSE;
- asignación.

Solo agrega `==`.

### E8

Recupera el ciclo central E3–E6 y lo transfiere a un nuevo contexto.

No exige `==` ni selección cruzada.

**Resultado:** no se identifican prerrequisitos circulares ni saltos ocultos.

---

## 3. Auditoría de fading

La progresión de apoyo es:

```text
E1  OBSERVAR Y EJECUTAR
↓
E2  OBSERVAR, EJECUTAR Y RELACIONAR
↓
E3  COMPLETAR UNA ASIGNACIÓN
↓
E4  OBSERVAR UN NUEVO MECANISMO
↓
E5  COMPLETAR LA PIEZA CENTRAL
↓
E6  PRODUCIR EL CICLO COMPLETO
↓
E7  NUEVA SINTAXIS CON APOYO ALTO
↓
E8  TRANSFERIR EL CICLO CON MENOR APOYO
```

Este fading evita el problema del diseño anterior, donde la primera aparición de `vector[condicion]` ya exigía producción.

El aumento de apoyo en E7 es deliberado porque aparece `==`.

---

## 4. Auditoría de recuperación

| Habilidad previa | Recuperación |
|---|---|
| `TRUE/FALSE` de M1 | E1, E2, E3, E4 |
| `<-` y objetos | E3, E5, E6, E7, E8 |
| consulta de objetos | E3, E4, E5, E7 |
| vectores | todos los ejercicios desde E2 |
| posiciones | E1 como contraste; E4 como correspondencia |
| `[]` de M2 | E4, E5, E6, E8 |
| texto y comillas | E7 |
| correspondencia posición a posición | E2 y E4 |

La recuperación ocurre dentro de tareas nuevas y no mediante repetición aislada.

---

## 5. Auditoría de errores

La progresión de errores se organiza así:

### Primer tramo — comparación

Errores:

- invertir `>`;
- usar operador incorrecto;
- esperar una sola respuesta.

Confusión diagnosticada:

> cómo se formula y aplica una pregunta.

### Segundo tramo — guardar respuestas

Errores:

- confundir datos con condición;
- hardcodear TRUE/FALSE;
- no consultar el objeto.

Confusión diagnosticada:

> qué contiene el nuevo objeto.

### Tercer tramo — seleccionar

Errores:

- invertir datos y condición;
- volver a posiciones;
- hardcodear resultados.

Confusión diagnosticada:

> cómo TRUE/FALSE decide qué conservar.

### Cuarto tramo — transferencia

Errores:

- usar `>=`;
- copiar posiciones;
- usar `=` en vez de `==`;
- omitir comillas en texto.

No se introduce un error deliberado adicional: los errores naturales del proceso son suficientes.

---

## 6. Auditoría de intuitividad

Escala:

- **Q1:** entiende qué pregunta se responde;
- **Q2:** entiende qué debe hacer;
- **Q3:** entiende por qué el código responde;
- **Q4:** puede anticipar aproximadamente el resultado;
- **Q5:** puede interpretar el resultado.

Cada dimensión vale 0–2.

| Ejercicio | Q1 | Q2 | Q3 | Q4 | Q5 | Total |
|---|---:|---:|---:|---:|---:|---:|
| E1 — De posiciones a preguntas | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E2 — La misma pregunta para todos | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E3 — Guardar las respuestas | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E4 — TRUE conserva, FALSE deja fuera | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E5 — Ahora selecciona tú | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E6 — La pregunta sigue funcionando | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E7 — También podemos preguntar por texto | 2 | 2 | 2 | 2 | 2 | **10/10** |
| E8 — Mini desafío | 2 | 2 | 2 | 2 | 2 | **10/10** |

La puntuación no pretende ser una medida psicométrica. Funciona como control de diseño: ningún ejercicio depende de adivinar una relación que todavía no haya sido construida.

---

## 7. Auditoría de carga cognitiva

| Ejercicio | Sintaxis nueva | Concepto nuevo | Objetos activos principales | Producción solicitada | Carga |
|---|---|---|---:|---|---|
| E1 | `>` | comparación como pregunta | 0 | ninguna | **Baja** |
| E2 | `vector > valor` | una respuesta por valor | 1 | ninguna | **Baja-media** |
| E3 | ninguna | guardar respuestas | 2 | una línea | **Baja-media** |
| E4 | `vector[condicion]` dado | TRUE conserva / FALSE deja fuera | 2 | ninguna | **Media** |
| E5 | ninguna | reutilizar condición en `[]` | 3 | completar un fragmento | **Baja-media** |
| E6 | ninguna | generalizar ciclo completo | 3 | dos expresiones | **Media** |
| E7 | `==` | igualdad sobre texto | 2 | una expresión guiada | **Baja-media** |
| E8 | ninguna | transferencia | 3 | dos expresiones | **Media** |

No hay ejercicios de carga media-alta ni alta.

---

## 8. Prueba de transferencia final

Después de completar el módulo, el estudiante debería comprender sin haber visto exactamente este ejemplo:

```r
horas_estudio <- c(2, 4, 3, 5, 1)

muchas_horas <-
  horas_estudio > 3

horas_estudio[muchas_horas]
```

Interpretación esperada:

> R pregunta para cada valor si supera 3. Guarda una respuesta TRUE/FALSE para cada uno en `muchas_horas`. Después usa esas respuestas para conservar 4 y 5.

Resultado esperado:

```text
[1] 4 5
```

Esta prueba mantiene la misma arquitectura mental, pero cambia:

- nombre del vector;
- valores;
- umbral;
- nombre de la condición.

---

## 9. Contenidos trasladados deliberadamente a módulos posteriores

La siguiente capacidad queda **fuera del Módulo 3**:

```r
carreras <- c(
  "Sociología",
  "Historia",
  "Sociología",
  "Antropología"
)

horas_estudio <- c(4, 2, 5, 3)

es_sociologia <-
  carreras == "Sociología"

horas_estudio[es_sociologia]
```

No se elimina del recorrido de Social R.

Se traslada deliberadamente porque exige comprender una idea adicional:

> dos características diferentes pertenecen a los mismos casos y mantienen correspondencia entre posiciones.

Esta capacidad será más intuitiva cuando el curso introduzca explícitamente:

- casos;
- observaciones;
- variables;
- organización tabular de datos.

Así, M3 termina consolidando una sola arquitectura:

```text
TENGO VARIOS VALORES
↓
FORMULO UNA PREGUNTA
↓
R RESPONDE TRUE/FALSE
↓
GUARDO LAS RESPUESTAS
↓
USO LAS RESPUESTAS PARA SELECCIONAR
```

antes de ampliar esa lógica a estructuras de datos más complejas.

---

# Verificación final del diseño

- [x] Exactamente 8 ejercicios.
- [x] Títulos en el orden aprobado.
- [x] `>` aparece primero sobre valores individuales.
- [x] La comparación vectorial aparece después.
- [x] La correspondencia valor ↔ TRUE/FALSE es explícita.
- [x] El objeto lógico utiliza `supera_30`.
- [x] E4 es un worked example.
- [x] E5 es un completion problem.
- [x] E6 exige construir condición + selección.
- [x] `==` aparece recién en E7.
- [x] E7 no utiliza una condición para seleccionar otro vector.
- [x] E8 contiene una sola pregunta.
- [x] E8 contiene una sola condición.
- [x] E8 contiene una sola selección.
- [x] La selección cruzada entre vectores no es objetivo.
- [x] No se exige `x[x > valor]`.
- [x] No se introducen `<`, `>=`, `<=`, `!=`, `&` ni `|`.
- [x] Ningún ejercicio tiene carga media-alta o alta.

---

# Cierre pedagógico

Al terminar este módulo, el estudiante no debería pensar:

> “Aprendí a poner un objeto logical dentro de corchetes.”

La comprensión deseada es:

> **Tengo varios valores.**

↓

> **Puedo hacerles una pregunta.**

↓

> **R responde TRUE o FALSE para cada uno.**

↓

> **Puedo guardar esas respuestas.**

↓

> **Puedo utilizarlas para quedarme con los valores que cumplen.**

Ese modelo mental constituye la fuente de verdad pedagógica del Módulo 3 rediseñado.
