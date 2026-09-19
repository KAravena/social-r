# Social R — Módulo 1
## Tus primeros minutos con R

> Documento pedagógico canónico. Versión definitiva para implementación posterior.

## 1. Propósito del módulo

Este módulo constituye el primer contacto con R. No busca enseñar todavía análisis estadístico ni estructuras complejas, sino construir una primera alfabetización computacional: **escribo o modifico código → lo ejecuto → R produce un resultado → puedo interpretarlo, guardarlo, reutilizarlo o corregirlo**. La meta es acumular pequeñas experiencias de éxito antes de introducir un error deliberado.

## 2. Perfil de entrada

La persona puede no haber programado nunca, no distinguir editor y consola, no conocer `<-`, objetos, funciones o tipos de información, y puede sentir ansiedad frente al código. No se presupone vocabulario técnico.

## 3. Resultado de salida

Al finalizar, debería poder ejecutar y modificar código sencillo, crear objetos, distinguir guardar de consultar, reutilizar objetos en una operación, reconocer número/texto/verdadero-falso y corregir un error elemental relacionado con comillas.

## 4. Contenidos incluidos

- ejecución con `Ctrl + Enter`;
- editor, consola y comentarios `#` de forma funcional;
- suma con `+`;
- objetos y asignación con `<-`;
- consulta de objetos escribiendo su nombre;
- reutilización de objetos;
- número, texto y verdadero/falso;
- `numeric`, `character` y `logical` en segundo plano;
- error como información para revisar el código.

## 5. Contenidos explícitamente pospuestos

Se posponen `c()`, vectores, `sum()`, `[]`, comparaciones, `class()`, otros operadores aritméticos, bases de datos y estadística. `[1]` puede aparecer en consola, pero no se convierte en contenido activo.

## 6. Principios pedagógicos particulares del módulo

- Primera victoria antes de teoría.
- E2 modifica antes de pedir producción.
- `<-` aparece como ejemplo resuelto en E3.
- E3 y E4 hacen visible guardar vs consultar.
- E5 muestra para qué sirve reutilizar objetos.
- E6 introduce error después de varios éxitos.
- E7 prioriza significado cotidiano antes de términos técnicos.
- E8 integra sin sintaxis nueva.

## 7. Mapa de progresión

**EJECUTAR → MODIFICAR → GUARDAR → CREAR Y CONSULTAR → REUTILIZAR → DEPURAR → GENERALIZAR TIPOS → INTEGRAR**

---

# Ejercicio 1 — Tu primera instrucción en R

## 1. Función pedagógica en la secuencia

**Antes:** mira el editor sin saber qué ejecutar. **Después:** puede ejecutar una instrucción sencilla con `Ctrl + Enter` y localizar el resultado en la consola.

## 2. Objetivo de aprendizaje en R

Ejecutar una expresión sencilla y distinguir funcionalmente código en el editor de resultado en la consola.

## 3. Idea sobre datos

Una cantidad puede representarse mediante un valor y una pregunta elemental puede resolverse con una operación explícita.

## 4. Pregunta o situación sustantiva

En una encuesta piloto respondieron 18 estudiantes de Sociología y 12 de Antropología. La pregunta es cuántas respuestas hubo en total.

## 5. Prerrequisitos recuperados

Ninguno. Es la primera interacción con código R.

## 6. Concepto nuevo

Editor, consola, ejecución con `Ctrl + Enter`, comentario `#` y uso elemental de `+`, sin formalización innecesaria.

## 7. Contenido visible para el estudiante

R puede hacer cálculos y mostrarte el resultado inmediatamente.

En una encuesta piloto respondieron **18 estudiantes de Sociología** y **12 de Antropología**. El cálculo ya está escrito.

La línea que comienza con `#` es un comentario: explica el código, pero R no la calcula.

## 8. Objetivo visible

> Ejecutar tu primera línea de R y encontrar el resultado en la consola.

## 9. Instrucciones visibles / Tu tarea

1. Coloca el cursor sobre `18 + 12`.
2. Presiona **Ctrl + Enter**.
3. Mira el resultado que aparece en la consola.

## 10. Starter code definitivo

```r
# Respuestas de Sociología + respuestas de Antropología
18 + 12
```

## 11. Acción esperada paso a paso

1. No modificar el código.
2. Ejecutar `18 + 12`.
3. Localizar `30` en la consola.

## 12. Resultado esperado en consola

```text
> 18 + 12
[1] 30
```

Nota opcional: por ahora `[1] 30` puede leerse simplemente como “R devolvió 30”.

## 13. Interpretación esperada

> El resultado 30 representa el total de respuestas recibidas entre ambas carreras.

## 14. Solución interna de referencia

```r
18 + 12
```

## 15. Habilidad objetivo vs. respuesta computacional

No hay una estrategia alternativa que deba penalizarse: el objetivo es ejecutar la expresión ya preparada.

## 16. Checks semánticos recomendados

- La expresión ejecutada produce `30`.
- No exigir modificación.
- No evaluar el significado de `[1]`.

## 17. Estados de respuesta relevantes

- **Estado 1:** no ejecutó → recordar `Ctrl + Enter`.
- **Estado 2:** busca resultado en editor/comentario → orientar a consola.
- **Estado 3:** obtiene 30 → completo.

## 18. Errores previsibles

- Ejecutar solo el comentario.
- Modificar innecesariamente los números.
- Comprobar sin haber ejecutado.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Ejecuta comentario | No distingue comentario/código | `#` indica un comentario. Busca la línea que contiene los números y el signo `+`. |
| Busca resultado en editor | No distingue editor/consola | El código queda en el editor. El resultado aparece abajo, en la consola. |
| Modifica el cálculo | Cree que debe escribir | En este primer ejercicio no necesitas cambiar el código. Ejecuta la línea ya escrita. |
| No ejecutó | No identificó la acción | Coloca el cursor sobre `18 + 12` y presiona Ctrl + Enter. |

## 20. Pista 1 — conceptual

> Busca la línea que contiene dos números y el signo `+`.

## 21. Pista 2 — sintaxis

> Coloca el cursor sobre `18 + 12` y presiona Ctrl + Enter.

## 22. Pista 3 — casi resuelta

> No necesitas escribir nada nuevo: ejecuta `18 + 12`.

## 23. Mensaje de éxito

> **Ejecutaste tu primera instrucción en R.**

## 24. Transición al siguiente ejercicio

> Ahora que ya puedes ejecutar código, cambiarás una parte pequeña y observarás cómo cambia el resultado.

## 25. Nivel de andamiaje

**Muy alto**. todo el código está resuelto.

## 26. Carga cognitiva

**Baja**. solo la ejecución es objetivo activo.

## 27. Justificación pedagógica

La primera experiencia debe producir éxito inmediato y enseñar el ciclo editor → ejecución → consola antes de pedir escritura.


---

# Ejercicio 2 — Haz que el cálculo responda la pregunta

## 1. Función pedagógica en la secuencia

**Antes:** ejecuta código preparado. **Después:** identifica qué parte representa un dato y puede modificarla.

## 2. Objetivo de aprendizaje en R

Editar una expresión existente y volver a ejecutarla.

## 3. Idea sobre datos

Cuando cambia la información, el código que la representa también debe actualizarse.

## 4. Pregunta o situación sustantiva

Antropología ahora tiene 15 respuestas; Sociología continúa con 18.

## 5. Prerrequisitos recuperados

Ejecutar con `Ctrl + Enter`, consola y `+`.

## 6. Concepto nuevo

No hay sintaxis nueva; cambia la acción del estudiante: ahora edita.

## 7. Contenido visible para el estudiante

La información puede cambiar, y el código debe reflejar esos cambios.

Ahora sabemos que respondieron **18 estudiantes de Sociología** y **15 de Antropología**. El cálculo todavía usa el valor anterior de Antropología.

## 8. Objetivo visible

> Modificar un dato del código y obtener el total actualizado.

## 9. Instrucciones visibles / Tu tarea

1. Cambia solamente el número correspondiente a Antropología.
2. Ejecuta la línea.
3. Observa el nuevo total.

## 10. Starter code definitivo

```r
# Total de respuestas
18 + 12
```

## 11. Acción esperada paso a paso

1. Reemplazar `12` por `15`.
2. Ejecutar `18 + 15`.
3. Observar 33.

## 12. Resultado esperado en consola

```text
> 18 + 15
[1] 33
```

## 13. Interpretación esperada

> El nuevo total es 33 respuestas; el código cambió porque cambió uno de los datos.

## 14. Solución interna de referencia

```r
18 + 15
```

## 15. Habilidad objetivo vs. respuesta computacional

La meta es actualizar el dato de Antropología manteniendo 18 para Sociología y `+` como operación.

## 16. Checks semánticos recomendados

- La expresión produce 33.
- Conserva 18.
- Usa 15 para Antropología.

## 17. Estados de respuesta relevantes

- **Estado 1:** mantiene `18 + 12`.
- **Estado 2:** cambia también 18 o elimina `+`.
- **Estado 3:** `18 + 15` ejecutado → completo.

## 18. Errores previsibles

- Mantener 12.
- Cambiar 18.
- Eliminar `+`.
- Editar pero no ejecutar.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Mantiene 12 | No actualizó el dato | Antropología ahora tiene 15 respuestas. ¿Qué número representa ese grupo? |
| Cambia 18 | Modifica información estable | Las respuestas de Sociología siguen siendo 18. Solo cambió Antropología. |
| Omite `+` | Omite la operación | R necesita saber qué operación realizar. Conserva el signo `+`. |
| No reejecuta | No actualiza R | El código ya cambió en el editor. Ahora ejecútalo con Ctrl + Enter. |

## 20. Pista 1 — conceptual

> Solo cambió el número de Antropología.

## 21. Pista 2 — sintaxis

> Conserva `18 +` y modifica el número que sigue.

## 22. Pista 3 — casi resuelta

```r
18 + 15
```

## 23. Mensaje de éxito

> **Actualizaste el código para responder con la nueva información.**

## 24. Transición al siguiente ejercicio

> Ahora aprenderás a guardar información con un nombre para reutilizarla después.

## 25. Nivel de andamiaje

**Alto**. solo cambia un literal.

## 26. Carga cognitiva

**Baja**. no incorpora sintaxis ni vocabulario nuevos.

## 27. Justificación pedagógica

Separa ejecutar de modificar y genera agencia con un cambio mínimo.


---

# Ejercicio 3 — Guardar información

## 1. Función pedagógica en la secuencia

**Antes:** obtiene resultados temporales. **Después:** comprende que R puede guardar un valor bajo un nombre y mostrarlo después.

## 2. Objetivo de aprendizaje en R

Comprender una asignación con `<-` y una consulta por nombre.

## 3. Idea sobre datos

Un valor puede conservarse con un nombre significativo para reutilizarlo.

## 4. Pregunta o situación sustantiva

Ya sabemos que la encuesta recibió 33 respuestas y queremos conservar ese total.

## 5. Prerrequisitos recuperados

Ejecutar líneas, consola y números.

## 6. Concepto nuevo

Objeto, `<-` y consulta por nombre.

## 7. Contenido visible para el estudiante

Ya sabemos que la encuesta recibió **33 respuestas**.

En R podemos guardar ese valor:

`respuestas <- 33`

Puedes leerlo como: **“guarda 33 en un objeto llamado `respuestas`”**.

## 8. Objetivo visible

> Distinguir entre guardar un valor y pedirle a R que lo muestre.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `respuestas <- 33`.
2. Después ejecuta `respuestas`.
3. Compara lo que ocurre en la consola.

## 10. Starter code definitivo

```r
# Guarda el total de respuestas
respuestas <- 33

# Muestra el valor guardado
respuestas
```

## 11. Acción esperada paso a paso

1. Ejecutar asignación.
2. Observar que no imprime 33.
3. Ejecutar `respuestas`.
4. Observar 33.

## 12. Resultado esperado en consola

```text
> respuestas <- 33

> respuestas
[1] 33
```

## 13. Interpretación esperada

> La primera línea guarda; la segunda consulta el objeto y muestra su contenido.

## 14. Solución interna de referencia

```r
respuestas <- 33
respuestas
```

## 15. Habilidad objetivo vs. respuesta computacional

Escribir solo `33` muestra el valor pero no crea el objeto.

## 16. Checks semánticos recomendados

- Existe `respuestas`.
- Es numérico y vale 33.
- No exigir output de la asignación.
- Idealmente verificar consulta independiente.

## 17. Estados de respuesta relevantes

- **Estado 1:** consulta antes de asignar.
- **Estado 2:** guarda, pero espera output automático.
- **Estado 3:** guarda y consulta → completo.

## 18. Errores previsibles

- Consultar antes de crear.
- Escribir solo 33.
- Cambiar el valor.
- Confundir `<-` con comparación.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Consulta antes de crear | No comprende orden | R todavía no conoce `respuestas`. Ejecuta primero la línea donde se crea. |
| Espera output tras `<-` | Confunde guardar/mostrar | La asignación guarda el valor, pero normalmente no lo imprime. Ejecuta después `respuestas`. |
| Solo `33` | Muestra pero no guarda | Eso muestra el número, pero todavía no lo guarda con un nombre. |
| Otro valor | No conserva la información | El total que queremos guardar es 33. |

## 20. Pista 1 — conceptual

> Primero guarda el valor y después pide a R que lo muestre.

## 21. Pista 2 — sintaxis

> Ejecuta `respuestas <- 33` antes de `respuestas`.

## 22. Pista 3 — casi resuelta

```r
respuestas <- 33
respuestas
```

## 23. Mensaje de éxito

> **Guardaste un valor en un objeto y luego lo consultaste.**

## 24. Transición al siguiente ejercicio

> Ya viste cómo se crea un objeto. Ahora escribirás una asignación nueva siguiendo el mismo patrón.

## 25. Nivel de andamiaje

**Muy alto**. la sintaxis nueva está completamente resuelta.

## 26. Carga cognitiva

**Baja-media**. aparecen objeto, `<-` y consulta mediante ejemplo trabajado.

## 27. Justificación pedagógica

Hace visible la distinción guardar/consultar, que será un prerrequisito longitudinal.


---

# Ejercicio 4 — Crea tu primer objeto

## 1. Función pedagógica en la secuencia

**Antes:** comprende una asignación ya escrita. **Después:** crea un objeto nuevo y consulta explícitamente dos objetos.

## 2. Objetivo de aprendizaje en R

Escribir una asignación simple y consultar objetos por nombre.

## 3. Idea sobre datos

Nombres distintos permiten conservar y recuperar cantidades de grupos distintos.

## 4. Pregunta o situación sustantiva

Tenemos 18 respuestas de Sociología y queremos guardar 15 de Antropología.

## 5. Prerrequisitos recuperados

Objeto, `<-`, número, consulta y ejecución.

## 6. Concepto nuevo

Producción de una asignación completa; sin sintaxis nueva.

## 7. Contenido visible para el estudiante

Los nombres de los objetos ayudan a recordar qué información contienen.

Ya guardamos **18 respuestas de Sociología**. Ahora crea el objeto de **15 respuestas de Antropología** y comprueba el contenido de ambos.

## 8. Objetivo visible

> Crear un objeto nuevo y consultar el contenido de los dos objetos de respuestas.

## 9. Instrucciones visibles / Tu tarea

1. Crea `respuestas_antropologia` con `15`.
2. Escribe `respuestas_sociologia` en una línea independiente.
3. Escribe `respuestas_antropologia` en la siguiente.
4. Ejecuta y observa ambos valores.

## 10. Starter code definitivo

```r
# Respuestas recibidas desde Sociología
respuestas_sociologia <- 18

# Crea aquí el objeto con las 15 respuestas de Antropología


# Muestra el contenido de ambos objetos
```

## 11. Acción esperada paso a paso

1. Escribir `respuestas_antropologia <- 15`.
2. Ejecutar asignaciones.
3. Escribir y ejecutar ambos nombres.
4. Observar 18 y 15.

## 12. Resultado esperado en consola

```text
> respuestas_sociologia <- 18

> respuestas_antropologia <- 15

> respuestas_sociologia
[1] 18

> respuestas_antropologia
[1] 15
```

## 13. Interpretación esperada

> Cada nombre recupera la cantidad guardada en ese objeto.

## 14. Solución interna de referencia

```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

respuestas_sociologia
respuestas_antropologia
```

## 15. Habilidad objetivo vs. respuesta computacional

Crear `respuestas_antropologia` no basta: el objetivo también consolida consultar. Ambos objetos deben llamarse como expresiones independientes.

## 16. Checks semánticos recomendados

- Ambos objetos existen, son numéricos y valen 18 y 15.
- Hay consultas independientes de ambos nombres.
- No confundir nombre dentro de asignación con consulta.

## 17. Estados de respuesta relevantes

- **Estado 1:** falta objeto de Antropología.
- **Estado 2:** ambos existen, sin consultas.
- **Estado 3:** consulta solo uno.
- **Estado 4:** ambos correctos y consultados → completo.

## 18. Errores previsibles

- Escribir solo 15.
- Guardar `"15"`.
- Usar otro nombre.
- Consultar solo uno.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Solo 15 | No guarda | Eso muestra el número, pero todavía no lo guarda con un nombre. |
| `"15"` | Cantidad guardada como texto | Queremos una cantidad numérica. El número 15 no necesita comillas. |
| Sin consultas | No consolida mostrar | Los dos objetos ya están creados. Ahora escribe sus nombres en líneas separadas para ver qué contienen. |
| Solo una consulta | Práctica incompleta | Ya mostraste uno. Haz lo mismo con el otro. |
| Nombre distinto | No conserva nombre solicitado | Usa exactamente `respuestas_antropologia`, porque lo reutilizaremos después. |

## 20. Pista 1 — conceptual

> Sigue el patrón de Sociología y recuerda que escribir solo el nombre muestra su contenido.

## 21. Pista 2 — sintaxis

> La estructura es `nombre <- valor`; después escribe cada nombre en una línea propia.

## 22. Pista 3 — casi resuelta

```r
respuestas_antropologia <- 15

respuestas_sociologia
respuestas_antropologia
```

## 23. Mensaje de éxito

> **Creaste y consultaste tus primeros objetos.**

## 24. Transición al siguiente ejercicio

> Ahora tienes dos objetos con información distinta. El siguiente ejercicio mostrará para qué sirve reutilizarlos.

## 25. Nivel de andamiaje

**Alto**. hay un modelo inmediato.

## 26. Carga cognitiva

**Baja-media**. se consolida asignar/consultar sin sintaxis nueva.

## 27. Justificación pedagógica

La repetición es productiva: fortalece la distinción asignar/consultar y prepara la consulta de vectores en M2.


---

# Ejercicio 5 — Combinar información

## 1. Función pedagógica en la secuencia

**Antes:** crea y consulta objetos separados. **Después:** reutiliza objetos en una expresión y guarda un resultado derivado.

## 2. Objetivo de aprendizaje en R

Sumar dos objetos numéricos y asignar el resultado a un tercero.

## 3. Idea sobre datos

Los valores almacenados pueden reutilizarse para construir nueva información.

## 4. Pregunta o situación sustantiva

Queremos calcular el total usando los objetos de Sociología y Antropología.

## 5. Prerrequisitos recuperados

Objetos, `<-`, consulta, `+`, números.

## 6. Concepto nuevo

No hay sintaxis nueva; la novedad es reutilización.

## 7. Contenido visible para el estudiante

Una ventaja de guardar información en objetos es que podemos utilizarla en nuevos cálculos.

Calcula el total **usando `respuestas_sociologia` y `respuestas_antropologia`**, sin volver a escribir 18 y 15.

## 8. Objetivo visible

> Reutilizar dos objetos para crear un nuevo resultado.

## 9. Instrucciones visibles / Tu tarea

1. Suma ambos objetos.
2. Guarda el resultado en `total_respuestas`.
3. Ejecuta `total_respuestas`.

## 10. Starter code definitivo

```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

# Calcula el total utilizando los dos objetos


# Muestra el resultado
```

## 11. Acción esperada paso a paso

1. Escribir la suma con los dos nombres.
2. Guardarla en `total_respuestas`.
3. Consultar el resultado.

## 12. Resultado esperado en consola

```text
> total_respuestas <- respuestas_sociologia + respuestas_antropologia

> total_respuestas
[1] 33
```

## 13. Interpretación esperada

> `total_respuestas` contiene 33, derivado de los valores guardados para ambos grupos.

## 14. Solución interna de referencia

```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

## 15. Habilidad objetivo vs. respuesta computacional

`total_respuestas <- 18 + 15` produce 33, pero evita reutilizar objetos. Debe reconocerse como resultado correcto con objetivo incompleto.

## 16. Checks semánticos recomendados

- `total_respuestas` existe, es numérico y vale 33.
- Su creación reutiliza ambos objetos.
- Se consulta al final.

## 17. Estados de respuesta relevantes

- **Estado 1:** falta total.
- **Estado 2:** suma sin guardar.
- **Estado 3:** 33 con literales → parcial.
- **Estado 4:** reutiliza ambos objetos → completo.

## 18. Errores previsibles

- Usar 18 + 15.
- Sumar sin asignar.
- Omitir `+`.
- Usar nombre inexistente.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| 18 + 15 | Resultado correcto, estrategia incompleta | El resultado es correcto. Ahora intenta aprovechar los objetos que ya creaste. |
| Suma sin guardar | Falta asignación | La suma funciona. Ahora guarda ese resultado en `total_respuestas`. |
| Omite + | No especifica operación | Entre los dos objetos necesitas indicar qué operación debe realizar R. |
| Nombre inexistente | Error de nombre | Revisa los nombres disponibles: `respuestas_sociologia` y `respuestas_antropologia`. |

## 20. Pista 1 — conceptual

> No necesitas volver a escribir 18 y 15: esos valores ya tienen nombres.

## 21. Pista 2 — sintaxis

> Puedes sumar objetos del mismo modo que sumaste números y guardar con `<-`.

## 22. Pista 3 — casi resuelta

```r
total_respuestas <- respuestas_sociologia + ___
total_respuestas
```

## 23. Mensaje de éxito

> **Usaste dos objetos para construir un nuevo resultado.**

## 24. Transición al siguiente ejercicio

> El próximo ejercicio mostrará qué ocurre cuando uno de los valores parece un número, pero R lo interpreta como texto.

## 25. Nivel de andamiaje

**Medio**. el starter entrega objetos, pero no la expresión objetivo.

## 26. Carga cognitiva

**Media**. integra asignación, reutilización, suma y consulta.

## 27. Justificación pedagógica

Da sentido funcional a los objetos y permite distinguir resultado correcto de estrategia objetivo.


---

# Ejercicio 6 — Un error útil: ¿número o texto?

## 1. Función pedagógica en la secuencia

**Antes:** trabaja con código correcto. **Después:** usa un error sencillo como pista para revisar número vs texto.

## 2. Objetivo de aprendizaje en R

Ejecutar código con error, localizar una causa plausible y corregirla.

## 3. Idea sobre datos

La representación de un valor condiciona qué operaciones son posibles.

## 4. Pregunta o situación sustantiva

Antropología quedó registrada como `"15"`, aunque queremos una cantidad numérica.

## 5. Prerrequisitos recuperados

Objetos, suma, asignación, consulta.

## 6. Concepto nuevo

Primer error deliberado por incompatibilidad número/texto.

## 7. Contenido visible para el estudiante

Este código tiene un problema. Antes de corregirlo, observa qué ocurre.

`respuestas_antropologia <- "15"` usa comillas, por lo que R interpreta `"15"` como **texto**.

Ejecuta primero y luego corrige.

## 8. Objetivo visible

> Usar un error para distinguir una cantidad numérica de texto.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta el código sin modificarlo.
2. Observa el error.
3. Cambia `"15"` por `15`.
4. Vuelve a ejecutar y comprueba el total.

## 10. Starter code definitivo

```r
respuestas_sociologia <- 18
respuestas_antropologia <- "15"

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

## 11. Acción esperada paso a paso

1. Ejecutar y observar error.
2. Quitar comillas.
3. Reejecutar asignación, suma y consulta.

## 12. Resultado esperado en consola

```text
> total_respuestas <- respuestas_sociologia + respuestas_antropologia
Error: non-numeric argument to binary operator
```

Después de corregir:

```text
> total_respuestas
[1] 33
```

## 13. Interpretación esperada

> `"15"` y `15` se parecen, pero las comillas convierten el primero en texto.

## 14. Solución interna de referencia

```r
respuestas_sociologia <- 18
respuestas_antropologia <- 15

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

## 15. Habilidad objetivo vs. respuesta computacional

El estado final correcto puede aceptarse, pero la experiencia ideal incluye observar el error antes de corregirlo.

## 16. Checks semánticos recomendados

- Antropología termina como numérico 15.
- `total_respuestas` vale 33.
- El código final no falla.
- Iniciar sin `total_respuestas` heredado.

## 17. Estados de respuesta relevantes

- **Estado 1:** mantiene `"15"`.
- **Estado 2:** corrige editor pero no reejecuta.
- **Estado 3:** corrige y obtiene 33 → completo.

## 18. Errores previsibles

- Mantener comillas.
- Convertir ambos números a texto.
- Corregir sin reejecutar.
- Heredar un total antiguo.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Mantiene `"15"` | No identifica comillas | R sigue viendo `"15"` como texto. Prueba quitando las comillas. |
| Ambos como texto | Cree que dígitos implican número | Aunque contienen dígitos, las comillas hacen que ambos valores sean texto. |
| No reejecuta | No actualiza estado | El código está corregido, pero R todavía necesita ejecutarlo. |
| Total no existe | Consecuencia normal del error | Eso es esperable: R no pudo crear `total_respuestas` porque la suma falló. |

## 20. Pista 1 — conceptual

> Busca el valor que está entre comillas.

## 21. Pista 2 — sintaxis

> Las comillas indican texto. Para una cantidad, escribe el número sin comillas.

## 22. Pista 3 — casi resuelta

```r
respuestas_antropologia <- 15
```

## 23. Mensaje de éxito

> **Encontraste y corregiste el problema de representación.**

## 24. Transición al siguiente ejercicio

> El error mostró que R distingue números y texto. Ahora ampliaremos esa idea a tres formas básicas de información.

## 25. Nivel de andamiaje

**Medio**. el código está construido y la causa está localizada.

## 26. Carga cognitiva

**Media**. aparece el primer error deliberado sobre estructura conocida.

## 27. Justificación pedagógica

Enseña depuración como parte normal del trabajo y no como señal de incapacidad.


---

# Ejercicio 7 — Tres formas de representar información

## 1. Función pedagógica en la secuencia

**Antes:** reconoce número vs texto. **Después:** distingue número, texto y verdadero/falso.

## 2. Objetivo de aprendizaje en R

Asignar correctamente valores numéricos, de texto y lógicos.

## 3. Idea sobre datos

Distintas clases de información requieren representaciones distintas.

## 4. Pregunta o situación sustantiva

Representamos edad, carrera y situación laboral de una persona encuestada.

## 5. Prerrequisitos recuperados

Objetos, `<-`, comillas y número/texto.

## 6. Concepto nuevo

`TRUE/FALSE`; `numeric`, `character`, `logical` aparecen después del significado cotidiano.

## 7. Contenido visible para el estudiante

No toda la información tiene la misma forma.

- una **edad** es una cantidad;
- una **carrera** es texto;
- una respuesta de **sí/no** puede ser verdadero o falso.

En R verás los nombres `numeric`, `character` y `logical`. No necesitas memorizarlos ahora: primero importa reconocer cómo se escribe cada forma.

## 8. Objetivo visible

> Representar correctamente un número, un texto y un valor verdadero/falso.

## 9. Instrucciones visibles / Tu tarea

1. Cambia `edad` a 21.
2. Cambia `carrera` a `"Sociología"`.
3. Cambia `trabaja` a `TRUE`.
4. Ejecuta las tres asignaciones.

## 10. Starter code definitivo

```r
# Edad en años
edad <- 20

# Carrera
carrera <- "Historia"

# ¿Trabaja actualmente?
trabaja <- FALSE
```

## 11. Acción esperada paso a paso

1. 20 → 21.
2. Conservar comillas en Sociología.
3. FALSE → TRUE sin comillas.
4. Ejecutar.

## 12. Resultado esperado en consola

Las asignaciones no imprimen resultados. Si se consultan:

```text
> edad
[1] 21

> carrera
[1] "Sociología"

> trabaja
[1] TRUE
```

## 13. Interpretación esperada

> R representa cantidades, texto y verdadero/falso de maneras distintas.

## 14. Solución interna de referencia

```r
edad <- 21
carrera <- "Sociología"
trabaja <- TRUE
```

## 15. Habilidad objetivo vs. respuesta computacional

Los valores deben tener representación correcta: `"21"` y `"TRUE"` no son equivalentes a 21 y TRUE.

## 16. Checks semánticos recomendados

- `edad` numérico 21.
- `carrera` character `"Sociología"`.
- `trabaja` logical TRUE.
- No usar `class()`.

## 17. Estados de respuesta relevantes

- **Estado 1:** no actualiza todo.
- **Estado 2:** valores visualmente correctos con tipo errado.
- **Estado 3:** dos de tres correctos.
- **Estado 4:** tres correctos → completo.

## 18. Errores previsibles

- `edad <- "21"`.
- `carrera <- Sociología`.
- `trabaja <- "TRUE"`.
- `trabaja <- true`.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| `"21"` | Cantidad como texto | La edad es una cantidad numérica. Escribe 21 sin comillas. |
| Sociología sin comillas | Texto sin comillas | `Sociología` es texto. Escríbelo entre comillas. |
| `"TRUE"` | Logical como texto | Queremos `TRUE`, no el texto `"TRUE"`. Quita las comillas. |
| `true` | Escritura incorrecta | En R usamos `TRUE` y `FALSE` en mayúsculas. |

## 20. Pista 1 — conceptual

> Edad es cantidad, carrera es texto y trabajar puede expresarse como verdadero/falso.

## 21. Pista 2 — sintaxis

> El texto lleva comillas. Los números y `TRUE/FALSE` no.

## 22. Pista 3 — casi resuelta

```r
edad <- 21
carrera <- "Sociología"
trabaja <- ___
```

## 23. Mensaje de éxito

> **Representaste correctamente tres formas básicas de información.**

## 24. Transición al siguiente ejercicio

> El último ejercicio combinará lo aprendido dentro de un pequeño script.

## 25. Nivel de andamiaje

**Medio**. la estructura completa está disponible.

## 26. Carga cognitiva

**Media**. aparece TRUE/FALSE, pero número/texto se recuperan.

## 27. Justificación pedagógica

Generaliza tipos sin usar `class()` y prepara una recuperación útil de logical en M3.


---

# Ejercicio 8 — Mini desafío: una encuesta piloto

## 1. Función pedagógica en la secuencia

**Antes:** practica habilidades por separado. **Después:** integra objetos, tipos y reutilización en un pequeño script.

## 2. Objetivo de aprendizaje en R

Actualizar objetos, construir un resultado desde objetos existentes y consultarlo.

## 3. Idea sobre datos

Varias piezas de información pueden representarse y combinarse para producir un resultado derivado.

## 4. Pregunta o situación sustantiva

Una encuesta piloto tiene nombre, dos conteos y estado de finalización.

## 5. Prerrequisitos recuperados

Todo M1.

## 6. Concepto nuevo

Ninguno.

## 7. Contenido visible para el estudiante

El script tiene valores provisionales y falta el total.

- estudio: `"Encuesta piloto"`;
- Sociología: 14;
- Antropología: 11;
- la recolección terminó.

No necesitas sintaxis nueva.

## 8. Objetivo visible

> Completar un pequeño script reutilizando objetos y formas de información aprendidas.

## 9. Instrucciones visibles / Tu tarea

1. Actualiza los cuatro valores.
2. Crea `total_respuestas` sumando los dos objetos de respuestas.
3. Ejecuta `total_respuestas`.

## 10. Starter code definitivo

```r
# Nombre del estudio
estudio <- ""

# Respuestas recibidas
respuestas_sociologia <- 0
respuestas_antropologia <- 0

# ¿Terminó la recolección?
finalizada <- FALSE

# Calcula aquí el total utilizando los dos objetos


# Muestra el resultado
total_respuestas
```

## 11. Acción esperada paso a paso

1. Actualizar texto.
2. Actualizar conteos.
3. Cambiar a TRUE.
4. Crear total desde ambos objetos.
5. Consultar.

## 12. Resultado esperado en consola

```text
> total_respuestas
[1] 25
```

## 13. Interpretación esperada

> 25 es el total de respuestas de la encuesta piloto.

## 14. Solución interna de referencia

```r
estudio <- "Encuesta piloto"
respuestas_sociologia <- 14
respuestas_antropologia <- 11
finalizada <- TRUE

total_respuestas <- respuestas_sociologia + respuestas_antropologia
total_respuestas
```

## 15. Habilidad objetivo vs. respuesta computacional

`total_respuestas <- 25` o `14 + 11` da el resultado, pero no demuestra reutilización.

## 16. Checks semánticos recomendados

- Todos los objetos tienen valor/tipo correcto.
- `total_respuestas` vale 25.
- El total reutiliza ambos objetos.
- Se consulta el total.

## 17. Estados de respuesta relevantes

- **Estado 1:** valores provisionales.
- **Estado 2:** datos actualizados, falta total.
- **Estado 3:** total hardcodeado → parcial.
- **Estado 4:** integración completa.

## 18. Errores previsibles

- Estudio sin comillas.
- `"TRUE"`.
- Total hardcodeado.
- Usar 14+11 directamente.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Estudio sin comillas | Texto mal representado | El nombre del estudio es texto. Escríbelo entre comillas. |
| `"TRUE"` | Logical convertido en texto | Queremos el valor `TRUE`, no el texto `"TRUE"`. |
| Total 25 directo | Resultado correcto, estrategia incompleta | 25 es correcto. Ahora constrúyelo a partir de los dos objetos de respuestas. |
| 14+11 directo | Evita objetos | El cálculo funciona. Para completar el desafío, reutiliza los objetos donde guardaste esas cantidades. |

## 20. Pista 1 — conceptual

> Actualiza primero las cuatro piezas de información y después combina las dos cantidades.

## 21. Pista 2 — sintaxis

> El texto lleva comillas; números y TRUE no. Para el total, reutiliza ambos nombres.

## 22. Pista 3 — casi resuelta

```r
estudio <- "Encuesta piloto"
respuestas_sociologia <- 14
respuestas_antropologia <- 11
finalizada <- TRUE

total_respuestas <- respuestas_sociologia + ___
```

## 23. Mensaje de éxito

> **Completaste tu primer pequeño script en R.**

## 24. Transición al siguiente ejercicio

> Ya puedes trabajar con valores individuales. En el próximo módulo aprenderás a guardar varios valores relacionados en un mismo objeto.

## 25. Nivel de andamiaje

**Bajo dentro del módulo**. el starter conserva estructura, pero varias decisiones quedan al estudiante.

## 26. Carga cognitiva

**Media**. integra habilidades conocidas sin sintaxis nueva.

## 27. Justificación pedagógica

Cierra con transferencia y sensación de competencia, dejando abierta la necesidad de pasar de un valor a varios.


---

# Auditoría final del módulo

## Auditoría de secuencia

| Ejercicio | Capacidad antes | Capacidad después | Sintaxis nueva | Carga | Andamiaje |
|---|---|---|---|---|---|
| E1 | No sabe ejecutar | Ejecuta y localiza resultado | Ctrl+Enter, `#`, `+` | Baja | Muy alto |
| E2 | Ejecuta | Modifica código | Ninguna | Baja | Alto |
| E3 | Obtiene resultados | Guarda y consulta | `<-` | Baja-media | Muy alto |
| E4 | Comprende asignación | Crea y consulta objetos | Ninguna | Baja-media | Alto |
| E5 | Tiene objetos | Los reutiliza | Ninguna | Media | Medio |
| E6 | Código funciona | Depura número/texto | Comillas | Media | Medio |
| E7 | Distingue número/texto | Representa 3 formas | `TRUE/FALSE` | Media | Medio |
| E8 | Habilidades separadas | Integra script | Ninguna | Media | Bajo |

## Auditoría de prerrequisitos

Todos los ejercicios usan conocimientos ya introducidos. `<-` se muestra en E3 antes de producirse en E4; E6 usa una estructura conocida; E8 no agrega sintaxis.

## Auditoría de fading

El apoyo baja de ejecución resuelta a modificación, worked example, producción con modelo, construcción parcial, depuración guiada e integración.

## Auditoría de recuperación

`Ctrl + Enter`, `<-`, consulta, tipos y reutilización reaparecen de forma distribuida.

## Auditoría de errores

El error deliberado aparece en E6 después de varios éxitos y se centra en una diferencia visible: las comillas.

## Prueba de transferencia final

```r
personas_matutino <- 22
personas_vespertino <- 17

total_personas <- personas_matutino + personas_vespertino

personas_matutino
personas_vespertino
total_personas
```

También debería reconocer `nombre_estudio <- "Uso del tiempo"` y `terminado <- FALSE`.

## Nota de continuidad longitudinal

El final deja abierta la pregunta natural de M2: ¿qué hacer cuando tenemos varios valores relacionados de la misma característica?
