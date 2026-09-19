# Social R — Módulo 2
## Trabajar con varios valores

> Documento pedagógico canónico. Versión definitiva para implementación posterior.

## 1. Propósito del módulo

Este módulo extiende la idea de objeto aprendida en M1: un objeto puede contener **varios valores relacionados**. El estudiante aprende a crear vectores, resumirlos, localizar elementos por posición, seleccionar varios y comprender la correspondencia entre dos vectores. La meta no es memorizar comandos, sino pasar de “un valor” a “varios valores relacionados”.

## 2. Perfil de entrada

La persona ya puede crear y consultar objetos, usar `<-`, sumar objetos numéricos, reconocer número/texto/verdadero-falso y corregir un error sencillo. No conoce `c()`, vectores, `sum()` ni `[]`.

## 3. Resultado de salida

Al finalizar, debería poder crear un vector con `c()`, reconocer vectores de distintos tipos, obtener un total con `sum()`, seleccionar uno o varios elementos por posición y combinar dos vectores numéricos entendiendo la correspondencia posición a posición.

## 4. Contenidos incluidos

- `c()` como forma funcional de combinar varios valores;
- concepto informal de vector;
- vectores numéricos, de texto y lógicos;
- `sum()` como resumen elemental;
- elemento y posición;
- selección con `[]`;
- selección múltiple con `c()` dentro de `[]`;
- suma de vectores posición a posición;
- diferencia funcional entre `()` y `[]`.

## 5. Contenidos explícitamente pospuestos

Se posponen `names()`, selección por nombre, `2:4` como habilidad formal, `mean()`, `median()`, `sd()`, comparaciones (`>`, `==`, etc.), selección lógica, data frames y herramientas de `dplyr`.

## 6. Principios pedagógicos particulares del módulo

- `c()` se observa antes de producirse.
- Los tipos se recuperan desde M1, no se reenseñan desde cero.
- `sum()` se introduce como función con propósito transparente.
- La posición se enseña antes de la suma vector + vector.
- `[]` aparece antes del error deliberado `x(3)`.
- E9 integra sin sintaxis nueva.

## 7. Mapa de progresión

**UN VALOR → VARIOS VALORES → VECTOR → CREAR → TIPOS → RESUMIR → POSICIÓN → SELECCIONAR → CORRESPONDENCIA ENTRE VECTORES → DEPURAR → INTEGRAR**

---

# Ejercicio 1 — De un valor a varios

## 1. Función pedagógica en la secuencia

**Antes:** asocia un objeto con un valor. **Después:** comprende que un objeto puede contener varios valores relacionados y reconoce `c()` como herramienta para combinarlos.

## 2. Objetivo de aprendizaje en R

Ejecutar y consultar un vector ya construido con `c()`.

## 3. Idea sobre datos

Varios valores de la misma característica pueden agruparse y tratarse como una colección coherente.

## 4. Pregunta o situación sustantiva

Cinco personas tardaron 25, 40, 35, 50 y 30 minutos en llegar a su lugar de estudio o trabajo.

## 5. Prerrequisitos recuperados

Objetos, `<-`, números, consulta por nombre, ejecución y consola.

## 6. Concepto nuevo

`c()` y el término **vector**, introducido después de mostrar la necesidad de agrupar valores.

## 7. Contenido visible para el estudiante

Hasta ahora guardábamos un valor en cada objeto. Pero si tenemos cinco tiempos de viaje, crear `tiempo_1`, `tiempo_2`, `tiempo_3`… sería poco práctico.

R permite guardar varios valores relacionados dentro de un mismo objeto. `c()` **combina** esos valores. A una colección como esta la llamaremos **vector**.

## 8. Objetivo visible

> Observar cómo un objeto puede guardar varios valores relacionados.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta la línea que crea `tiempos_viaje`.
2. Después ejecuta `tiempos_viaje`.
3. Observa cuántos valores aparecen y qué representan.

## 10. Starter code definitivo

```r
# Tiempos de viaje de cinco personas, en minutos
tiempos_viaje <- c(25, 40, 35, 50, 30)

# Muestra los valores guardados
tiempos_viaje
```

## 11. Acción esperada paso a paso

1. Ejecutar la asignación.
2. Ejecutar la consulta.
3. Reconocer cinco valores.
4. Interpretarlos como cinco tiempos relacionados.

## 12. Resultado esperado en consola

```text
> tiempos_viaje <- c(25, 40, 35, 50, 30)

> tiempos_viaje
[1] 25 40 35 50 30
```

## 13. Interpretación esperada

> `tiempos_viaje` contiene cinco tiempos relacionados guardados juntos.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
tiempos_viaje
```

## 15. Habilidad objetivo vs. respuesta computacional

No se exige producir `c()` todavía. La habilidad objetivo es ejecutar, consultar e interpretar el objeto como varios valores.

## 16. Checks semánticos recomendados

- Existe `tiempos_viaje`.
- Contiene exactamente `c(25,40,35,50,30)` en ese orden.
- Se consulta el objeto.
- No exigir modificación.

## 17. Estados de respuesta relevantes

- **Estado 1:** no ejecutó la asignación.
- **Estado 2:** creó el vector, pero no lo consultó.
- **Estado 3:** creó y consultó → completo.

## 18. Errores previsibles

- Consultar antes de crear.
- Modificar innecesariamente valores.
- Interpretar `c()` como parte del nombre del objeto.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Consulta antes de asignar | Olvida crear → consultar | R todavía no conoce `tiempos_viaje`. Ejecuta primero la línea donde se crea. |
| Modifica valores | Cree que debe escribir código nuevo | En este primer ejercicio no necesitas cambiar los datos. Ejecuta el ejemplo y observa qué guarda el objeto. |
| Pregunta qué es `c()` | Necesita significado funcional | Por ahora piensa en `c()` como una forma de combinar varios valores dentro de un mismo objeto. |

## 20. Pista 1 — conceptual

> Primero ejecuta la línea que guarda los cinco tiempos juntos.

## 21. Pista 2 — sintaxis

> `c(25, 40, 35, 50, 30)` combina los cinco valores; después consulta el objeto.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)
tiempos_viaje
```

## 23. Mensaje de éxito

> **Consultaste tu primer vector.**

## 24. Transición al siguiente ejercicio

> Ya viste un vector construido. Ahora crearás uno nuevo siguiendo el mismo patrón.

## 25. Nivel de andamiaje

**Muy alto**. la nueva sintaxis aparece completamente resuelta.

## 26. Carga cognitiva

**Baja-media**. aparecen `c()` y vector, pero no se exige producirlos.

## 27. Justificación pedagógica

El primer contacto con `c()` surge de una necesidad concreta y extiende directamente la idea de objeto de M1.


---

# Ejercicio 2 — Crea tu primer vector

## 1. Función pedagógica en la secuencia

**Antes:** reconoce un vector construido. **Después:** escribe un vector numérico siguiendo un modelo reciente y lo consulta.

## 2. Objetivo de aprendizaje en R

Crear un vector numérico con `<-` y `c()`.

## 3. Idea sobre datos

Una misma característica observada en varias personas puede representarse con valores reunidos en un solo objeto.

## 4. Pregunta o situación sustantiva

Un nuevo grupo registra tiempos de viaje de 20, 35, 45, 25 y 30 minutos.

## 5. Prerrequisitos recuperados

Objeto, `<-`, consulta, números y ejemplo de `c()` de E1.

## 6. Concepto nuevo

Producción consciente de `c()` con paréntesis y comas.

## 7. Contenido visible para el estudiante

Ahora construirás el vector tú misma/o.

Los tiempos del nuevo grupo son **20, 35, 45, 25 y 30 minutos**. Queremos guardarlos juntos en `tiempos_viaje`.

## 8. Objetivo visible

> Crear un vector numérico con cinco tiempos de viaje.

## 9. Instrucciones visibles / Tu tarea

1. Crea `tiempos_viaje` con los cinco valores en el orden indicado.
2. Usa `c()` para combinarlos.
3. Ejecuta `tiempos_viaje` para comprobar su contenido.

## 10. Starter code definitivo

```r
# Guarda los cinco tiempos de viaje en un solo objeto


# Muestra el vector
tiempos_viaje
```

## 11. Acción esperada paso a paso

1. Escribir `tiempos_viaje <- c(20, 35, 45, 25, 30)`.
2. Ejecutar.
3. Consultar el objeto.
4. Verificar el orden.

## 12. Resultado esperado en consola

```text
> tiempos_viaje <- c(20, 35, 45, 25, 30)

> tiempos_viaje
[1] 20 35 45 25 30
```

## 13. Interpretación esperada

> El objeto contiene cinco observaciones de la misma característica y conserva su orden.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(20, 35, 45, 25, 30)
tiempos_viaje
```

## 15. Habilidad objetivo vs. respuesta computacional

Crear cinco objetos separados evita la habilidad objetivo: reunirlos en un único vector con `c()`.

## 16. Checks semánticos recomendados

- Existe `tiempos_viaje`.
- Vector numérico con 20,35,45,25,30 en ese orden.
- La creación usa `c()`.
- Se consulta el objeto.

## 17. Estados de respuesta relevantes

- **Estado 1:** no existe el objeto.
- **Estado 2:** valores separados o vector incompleto.
- **Estado 3:** vector correcto sin consulta.
- **Estado 4:** vector correcto y consultado.

## 18. Errores previsibles

- Olvidar `c()`.
- Omitir coma.
- Paréntesis sin cerrar.
- Alterar el orden.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Olvida `c()` | No agrupa valores | Necesitamos combinar los cinco valores dentro de un solo objeto. Usa `c(...)`. |
| Falta coma | No separa elementos | Dentro de `c()`, cada valor debe separarse del siguiente con una coma. |
| Paréntesis sin cerrar | Construcción incompleta | Abriste `c(`, pero necesitas cerrarlo con `)`. |
| Orden distinto | No conserva orden | Conserva el orden indicado: 20, 35, 45, 25, 30. |

## 20. Pista 1 — conceptual

> Necesitas guardar los cinco tiempos dentro de un solo objeto.

## 21. Pista 2 — sintaxis

> La estructura es `nombre <- c(valor1, valor2, ...)`.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje <- c(20, 35, ___, 25, 30)
```

## 23. Mensaje de éxito

> **Creaste tu primer vector.**

## 24. Transición al siguiente ejercicio

> Los vectores también pueden guardar otros tipos de información que ya conoces.

## 25. Nivel de andamiaje

**Alto**. el modelo acaba de aparecer y la consulta está preparada.

## 26. Carga cognitiva

**Baja-media**. solo se produce `c()` con comas/paréntesis.

## 27. Justificación pedagógica

La producción ocurre inmediatamente después del worked example, con recuperación de asignar y consultar.


---

# Ejercicio 3 — Varios valores, distintas formas de información

## 1. Función pedagógica en la secuencia

**Antes:** crea un vector numérico. **Después:** extiende la idea a número, texto y verdadero/falso.

## 2. Objetivo de aprendizaje en R

Reconocer y completar vectores numéricos, de texto y lógicos con `c()`.

## 3. Idea sobre datos

Una característica puede observarse en varias personas y conservar una forma coherente de información.

## 4. Pregunta o situación sustantiva

Tres personas tienen edades, carreras y situaciones laborales registradas en el mismo orden.

## 5. Prerrequisitos recuperados

Número/texto/verdadero-falso de M1, comillas, `TRUE/FALSE`, `c()` y consulta.

## 6. Concepto nuevo

Generalización de `c()` a `character` y `logical`; no se enseña coerción.

## 7. Contenido visible para el estudiante

Un vector no sirve solo para números.

Podemos guardar varias edades, varias carreras o varias respuestas de verdadero/falso. Lo importante es reconocer cómo se escribe cada forma de información.

## 8. Objetivo visible

> Reconocer y construir vectores con números, texto y verdadero/falso.

## 9. Instrucciones visibles / Tu tarea

1. Deja `edades` tal como está.
2. Cambia la primera carrera a `"Sociología"`.
3. Crea `trabaja` con `TRUE`, `FALSE`, `TRUE`.
4. Ejecuta y consulta los tres objetos.

## 10. Starter code definitivo

```r
# Edades
edades <- c(21, 22, 20)

# Carreras
carreras <- c("Historia", "Historia", "Antropología")

# ¿Trabaja actualmente?
# Crea aquí el vector trabaja


# Muestra los tres objetos
edades
carreras
trabaja
```

## 11. Acción esperada paso a paso

1. Mantener edades.
2. Modificar primera carrera.
3. Crear `trabaja <- c(TRUE, FALSE, TRUE)`.
4. Ejecutar consultas.

## 12. Resultado esperado en consola

```text
> edades
[1] 21 22 20

> carreras
[1] "Sociología" "Historia" "Antropología"

> trabaja
[1] TRUE FALSE TRUE
```

## 13. Interpretación esperada

> Los tres objetos contienen varios valores, pero representan cantidades, texto o verdadero/falso.

## 14. Solución interna de referencia

```r
edades <- c(21, 22, 20)
carreras <- c("Sociología", "Historia", "Antropología")
trabaja <- c(TRUE, FALSE, TRUE)

edades
carreras
trabaja
```

## 15. Habilidad objetivo vs. respuesta computacional

No se evalúa memorización de nombres técnicos; sí la representación correcta. `"TRUE"` no equivale a `TRUE`.

## 16. Checks semánticos recomendados

- Edades numéricas correctas.
- Carreras de texto correctas.
- `trabaja` lógico correcto.
- Tres elementos y orden conservado.

## 17. Estados de respuesta relevantes

- **Estado 1:** falta `trabaja`.
- **Estado 2:** tipos mal representados.
- **Estado 3:** dos objetos correctos.
- **Estado 4:** tres vectores correctos.

## 18. Errores previsibles

- Texto sin comillas.
- `"TRUE"/"FALSE"`.
- `true/false`.
- Crear valores separados.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Texto sin comillas | Olvida representación de texto | Las carreras son texto. Escríbelas entre comillas dentro de `c()`. |
| Logical con comillas | Convierte logical en texto | Las comillas convierten `TRUE/FALSE` en texto. Quítalas. |
| Minúsculas | Sintaxis logical incorrecta | En R usamos `TRUE` y `FALSE` en mayúsculas. |
| Valores separados | No aplica vector | Queremos guardar las tres respuestas juntas en `trabaja`. Usa `c()`. |

## 20. Pista 1 — conceptual

> Recuerda número, texto y verdadero/falso del módulo anterior.

## 21. Pista 2 — sintaxis

> El texto lleva comillas; `TRUE` y `FALSE` no. Para varios valores usa `c(...)`.

## 22. Pista 3 — casi resuelta

```r
carreras <- c("Sociología", "Historia", "Antropología")
trabaja <- c(TRUE, FALSE, ___)
```

## 23. Mensaje de éxito

> **Extendiste la idea de vector a distintas formas de información.**

## 24. Transición al siguiente ejercicio

> Ahora usaremos un vector numérico para obtener un único total.

## 25. Nivel de andamiaje

**Alto**. uno completo, uno para modificar y uno para completar.

## 26. Carga cognitiva

**Baja-media**. recupera tipos conocidos.

## 27. Justificación pedagógica

Evita tres ejercicios redundantes y distribuye recuperación sin convertir tipos en teoría.


---

# Ejercicio 4 — Obtener un total

## 1. Función pedagógica en la secuencia

**Antes:** guarda varios valores. **Después:** utiliza todos para producir un único resultado con `sum()`.

## 2. Objetivo de aprendizaje en R

Aplicar `sum()` a un vector numérico y guardar el resultado.

## 3. Idea sobre datos

Una colección puede resumirse mediante un total cuando la pregunta lo requiere.

## 4. Pregunta o situación sustantiva

Una encuesta recibió 18, 22, 15, 25 y 20 respuestas durante cinco jornadas.

## 5. Prerrequisitos recuperados

Vector numérico, `c()`, objeto, `<-`, consulta y suma.

## 6. Concepto nuevo

`sum()` como función que suma todos los valores de un vector.

## 7. Contenido visible para el estudiante

Tenemos las respuestas de cinco jornadas. En vez de sumarlas una por una, R puede usar `sum()` sobre el vector completo.

La pregunta: **¿cuántas respuestas se recibieron en total?**

## 8. Objetivo visible

> Usar `sum()` para obtener el total de un vector numérico.

## 9. Instrucciones visibles / Tu tarea

1. Usa `sum()` con `respuestas_diarias`.
2. Guarda el resultado en `total_respuestas`.
3. Ejecuta `total_respuestas`.

## 10. Starter code definitivo

```r
respuestas_diarias <- c(18, 22, 15, 25, 20)

# Calcula el total de respuestas


# Muestra el resultado
total_respuestas
```

## 11. Acción esperada paso a paso

1. Ejecutar el vector.
2. Crear `total_respuestas <- sum(respuestas_diarias)`.
3. Consultar.

## 12. Resultado esperado en consola

```text
> total_respuestas <- sum(respuestas_diarias)

> total_respuestas
[1] 100
```

## 13. Interpretación esperada

> Se recibieron 100 respuestas en total.

## 14. Solución interna de referencia

```r
respuestas_diarias <- c(18, 22, 15, 25, 20)

total_respuestas <- sum(respuestas_diarias)
total_respuestas
```

## 15. Habilidad objetivo vs. respuesta computacional

Hardcodear 100 o sumar manualmente obtiene el resultado, pero evita practicar `sum()` sobre el vector.

## 16. Checks semánticos recomendados

- `total_respuestas` vale 100.
- Se crea con `sum(respuestas_diarias)`.
- Se consulta.

## 17. Estados de respuesta relevantes

- **Estado 1:** falta total.
- **Estado 2:** 100 por hardcodeo/suma manual.
- **Estado 3:** usa sum pero no guarda/consulta.
- **Estado 4:** usa `sum()` y completa.

## 18. Errores previsibles

- `sum <- respuestas_diarias`.
- `sum respuestas_diarias`.
- `sum(18,22,...)`.
- Hardcodear 100.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Hardcodea 100 | Resultado correcto, función no practicada | 100 es correcto. Ahora obtén ese total usando `sum()` sobre `respuestas_diarias`. |
| Suma manual | Evita el vector | Ya tienes los valores guardados juntos. Usa `respuestas_diarias` dentro de `sum()`. |
| Sin paréntesis | No reconoce llamada | `sum()` necesita el objeto dentro de sus paréntesis. |
| No guarda | Falta asignación | El cálculo funciona. Ahora guarda el resultado en `total_respuestas`. |

## 20. Pista 1 — conceptual

> Todos los valores ya están dentro de `respuestas_diarias`.

## 21. Pista 2 — sintaxis

> La estructura es `sum(nombre_del_vector)` y puedes guardar el resultado con `<-`.

## 22. Pista 3 — casi resuelta

```r
total_respuestas <- sum(respuestas_diarias)
```

## 23. Mensaje de éxito

> **Resumiste varios valores en un total.**

## 24. Transición al siguiente ejercicio

> A veces no queremos usar todos los valores: necesitamos recuperar uno concreto. Para eso importa la posición.

## 25. Nivel de andamiaje

**Medio**. el vector está preparado; la función se produce por primera vez.

## 26. Carga cognitiva

**Media**. aparece `sum()` con un propósito muy transparente.

## 27. Justificación pedagógica

Introduce una primera función analítica simple sin abrir aún estadística descriptiva.


---

# Ejercicio 5 — Elegir un valor

## 1. Función pedagógica en la secuencia

**Antes:** trabaja con el vector completo. **Después:** comprende que cada elemento ocupa una posición y puede recuperarlo con `[]`.

## 2. Objetivo de aprendizaje en R

Seleccionar un elemento por posición con corchetes.

## 3. Idea sobre datos

El orden permite localizar una observación específica dentro de un vector.

## 4. Pregunta o situación sustantiva

Queremos saber cuánto tardó la tercera persona.

## 5. Prerrequisitos recuperados

Vector, consulta y orden.

## 6. Concepto nuevo

Elemento, posición y `vector[posición]`; primera posición = 1.

## 7. Contenido visible para el estudiante

Los valores mantienen un orden. Cada uno ocupa una **posición**.

En `tiempos_viaje`, el primer valor está en la posición 1, el segundo en la 2, etc. Queremos **solo el tercer tiempo**.

## 8. Objetivo visible

> Seleccionar un elemento de un vector usando su posición.

## 9. Instrucciones visibles / Tu tarea

1. Observa el orden.
2. Selecciona la posición 3.
3. Ejecuta la expresión.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# Muestra solo el tercer tiempo
```

## 11. Acción esperada paso a paso

1. Ejecutar vector.
2. Escribir `tiempos_viaje[3]`.
3. Ejecutar y observar 35.

## 12. Resultado esperado en consola

```text
> tiempos_viaje[3]
[1] 35
```

## 13. Interpretación esperada

> El tercer elemento es 35; la tercera persona tardó 35 minutos.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje[3]
```

## 15. Habilidad objetivo vs. respuesta computacional

Escribir 35 da el valor, pero no lo recupera desde el vector.

## 16. Checks semánticos recomendados

- Selección sobre `tiempos_viaje`.
- Posición 3.
- Resultado 35.

## 17. Estados de respuesta relevantes

- **Estado 1:** no intenta selección.
- **Estado 2:** literal o posición incorrecta.
- **Estado 3:** `tiempos_viaje[3]` → completo.

## 18. Errores previsibles

- `tiempos_viaje(3)`.
- `[0]`.
- `[2]`.
- Escribir 35.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Paréntesis | Confunde selección | Para elegir una posición usamos corchetes `[]`, no paréntesis. |
| Posición 0 | Supone indexación desde 0 | En R, la primera posición es 1. |
| Posición incorrecta | No vincula orden/posición | Cuenta los valores desde 1 y localiza el tercero. |
| Literal 35 | Resultado correcto, estrategia incompleta | 35 es correcto. Ahora recupéralo desde `tiempos_viaje` usando su posición. |

## 20. Pista 1 — conceptual

> Queremos el valor que está tercero.

## 21. Pista 2 — sintaxis

> La estructura es `nombre_del_vector[posición]`.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje[3]
```

## 23. Mensaje de éxito

> **Seleccionaste un elemento por su posición.**

## 24. Transición al siguiente ejercicio

> Ahora combinarás varias posiciones en una misma selección.

## 25. Nivel de andamiaje

**Alto-medio**. el vector está listo y solo se construye una expresión breve.

## 26. Carga cognitiva

**Media**. aparecen posición y `[]` sobre contexto conocido.

## 27. Justificación pedagógica

La posición se enseña antes de operaciones entre vectores porque será la base de correspondencia.


---

# Ejercicio 6 — Elegir varios valores

## 1. Función pedagógica en la secuencia

**Antes:** selecciona una posición. **Después:** combina varias posiciones con `c()` dentro de `[]`.

## 2. Objetivo de aprendizaje en R

Seleccionar múltiples elementos por posición usando `vector[c(...)]`.

## 3. Idea sobre datos

Podemos construir un subconjunto explícito cuando conocemos las posiciones.

## 4. Pregunta o situación sustantiva

Queremos recuperar la segunda y la cuarta persona.

## 5. Prerrequisitos recuperados

`c()`, vector, posición y `[]`.

## 6. Concepto nuevo

Composición de `c()` y `[]`.

## 7. Contenido visible para el estudiante

Los corchetes también permiten pedir **más de una posición**.

Usa `c()` para combinar las posiciones **2 y 4** dentro de los corchetes.

## 8. Objetivo visible

> Seleccionar dos elementos de un vector indicando sus posiciones.

## 9. Instrucciones visibles / Tu tarea

1. Selecciona 2 y 4.
2. Combina las posiciones con `c()`.
3. Ejecuta.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# Muestra los tiempos de las personas 2 y 4
```

## 11. Acción esperada paso a paso

1. Ejecutar vector.
2. Escribir `tiempos_viaje[c(2, 4)]`.
3. Observar 40 y 50.

## 12. Resultado esperado en consola

```text
> tiempos_viaje[c(2, 4)]
[1] 40 50
```

## 13. Interpretación esperada

> Las posiciones 2 y 4 contienen 40 y 50 minutos.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje[c(2, 4)]
```

## 15. Habilidad objetivo vs. respuesta computacional

`c(40,50)` reproduce los valores, pero no los selecciona desde el objeto.

## 16. Checks semánticos recomendados

- Selección sobre `tiempos_viaje`.
- Posiciones 2 y 4.
- Resultado 40,50.
- Usa `c()` dentro de `[]`.

## 17. Estados de respuesta relevantes

- **Estado 1:** no intenta.
- **Estado 2:** usa `[2,4]` o una sola posición.
- **Estado 3:** hardcodea valores.
- **Estado 4:** `[c(2,4)]` → completo.

## 18. Errores previsibles

- `[2,4]`.
- `c(40,50)` dentro de corchetes.
- Dos selecciones separadas.
- Hardcodear valores.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| `[2,4]` | No combina posiciones | Combina las posiciones con `c()` dentro de los corchetes. |
| Usa 40,50 como posiciones | Confunde valor/posición | Dentro de los corchetes necesitamos posiciones, no los valores esperados. |
| Dos selecciones | No integra selección múltiple | Tus selecciones funcionan. Ahora pide ambas posiciones en una sola expresión. |
| Hardcodea | Resultado correcto, estrategia incompleta | 40 y 50 son correctos. Ahora selecciónalos desde el vector. |

## 20. Pista 1 — conceptual

> Necesitas pedir dos posiciones: 2 y 4.

## 21. Pista 2 — sintaxis

> Combínalas con `c(2, 4)` dentro de `[]`.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje[c(2, 4)]
```

## 23. Mensaje de éxito

> **Seleccionaste varios elementos en una sola expresión.**

## 24. Transición al siguiente ejercicio

> Ya entiendes las posiciones. Ahora veremos qué ocurre cuando dos vectores describen información correspondiente en el mismo orden.

## 25. Nivel de andamiaje

**Medio**. combina dos recursos conocidos.

## 26. Carga cognitiva

**Media**. la dificultad está en la composición `c()` + `[]`.

## 27. Justificación pedagógica

Consolida el modelo de posición sin añadir `2:4`, que no aporta una capacidad conceptual nueva.


---

# Ejercicio 7 — Combinar valores posición a posición

## 1. Función pedagógica en la secuencia

**Antes:** comprende posiciones. **Después:** entiende que una operación entre dos vectores relaciona elementos en la misma posición.

## 2. Objetivo de aprendizaje en R

Sumar dos vectores numéricos y guardar el vector resultante.

## 3. Idea sobre datos

Dos vectores pueden describir a las mismas personas en el mismo orden y corresponder posición a posición.

## 4. Pregunta o situación sustantiva

Para cuatro personas conocemos horas de trabajo remunerado y cuidado.

## 5. Prerrequisitos recuperados

Vectores, posiciones, `+`, objetos y `<-`.

## 6. Concepto nuevo

Operación vector + vector interpretada como correspondencia.

## 7. Contenido visible para el estudiante

Tenemos dos vectores de las **mismas cuatro personas y en el mismo orden**.

Al sumarlos, R combina el primer valor con el primero, el segundo con el segundo, y así sucesivamente.

## 8. Objetivo visible

> Combinar dos vectores entendiendo la correspondencia entre sus posiciones.

## 9. Instrucciones visibles / Tu tarea

1. Suma `horas_trabajo` y `horas_cuidado`.
2. Guarda en `horas_totales`.
3. Ejecuta e interpreta los cuatro valores.

## 10. Starter code definitivo

```r
horas_trabajo <- c(8, 6, 7, 5)
horas_cuidado <- c(2, 4, 1, 3)

# Suma ambos vectores posición a posición


# Muestra el resultado
horas_totales
```

## 11. Acción esperada paso a paso

1. Ejecutar ambos vectores.
2. Crear `horas_totales <- horas_trabajo + horas_cuidado`.
3. Consultar.

## 12. Resultado esperado en consola

```text
> horas_totales
[1] 10 10 8 8
```

## 13. Interpretación esperada

> R produjo un total por persona: primero+primero, segundo+segundo, etc.

## 14. Solución interna de referencia

```r
horas_trabajo <- c(8, 6, 7, 5)
horas_cuidado <- c(2, 4, 1, 3)

horas_totales <- horas_trabajo + horas_cuidado
horas_totales
```

## 15. Habilidad objetivo vs. respuesta computacional

Hardcodear el vector final o producir un único total no demuestra correspondencia posición a posición.

## 16. Checks semánticos recomendados

- `horas_totales` = c(10,10,8,8).
- Se crea reutilizando ambos vectores con `+`.
- Se consulta.

## 17. Estados de respuesta relevantes

- **Estado 1:** falta resultado.
- **Estado 2:** usa `sum()` y obtiene un único total.
- **Estado 3:** hardcodea vector.
- **Estado 4:** suma ambos vectores.

## 18. Errores previsibles

- Usar `sum()`.
- Hardcodear c(10,10,8,8).
- Sumar una sola posición.
- Alterar el orden.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Un único total | Confunde resumen/correspondencia | Aquí queremos un total para cada persona. Suma directamente los dos vectores. |
| Hardcodea vector | Evita correspondencia | Los resultados son correctos. Ahora haz que R los construya sumando ambos objetos. |
| Una posición | No generaliza | No necesitas seleccionar una posición por vez. Suma los dos vectores completos. |
| Orden alterado | Rompe correspondencia | Conserva el mismo orden en ambos vectores. |

## 20. Pista 1 — conceptual

> Cada posición de un vector corresponde a la misma persona en el otro.

## 21. Pista 2 — sintaxis

> Usa el mismo `+` conocido, ahora entre dos nombres de vectores.

## 22. Pista 3 — casi resuelta

```r
horas_totales <- horas_trabajo + horas_cuidado
```

## 23. Mensaje de éxito

> **Combinaste dos vectores posición a posición.**

## 24. Transición al siguiente ejercicio

> Ya usaste paréntesis en funciones y corchetes para seleccionar. Ahora corregirás una confusión entre ambas formas.

## 25. Nivel de andamiaje

**Medio**. los vectores están dados; la novedad es la interpretación.

## 26. Carga cognitiva

**Media**. sin símbolo nuevo, pero con una intuición de correspondencia importante.

## 27. Justificación pedagógica

Aparece después de posición para evitar un prerrequisito oculto.


---

# Ejercicio 8 — Paréntesis o corchetes

## 1. Función pedagógica en la secuencia

**Antes:** ha usado `()` y `[]` con sentido. **Después:** diagnostica y corrige la confusión entre ambas formas.

## 2. Objetivo de aprendizaje en R

Corregir `tiempos_viaje(3)` a `tiempos_viaje[3]`.

## 3. Idea sobre datos

Seleccionar una posición no equivale a tratar el objeto como una función.

## 4. Pregunta o situación sustantiva

Queremos recuperar el tercer tiempo, pero el script usa paréntesis.

## 5. Prerrequisitos recuperados

`c()`, `sum()`, `[]`, posición y experiencia previa con errores.

## 6. Concepto nuevo

Ninguno; depuración de sintaxis conocida.

## 7. Contenido visible para el estudiante

Este código intenta mostrar el tercer tiempo, pero utiliza la sintaxis equivocada.

Primero **ejecútalo tal como está**. Después corrígelo usando lo que ya sabes sobre selección.

## 8. Objetivo visible

> Distinguir cuándo usar paréntesis y cuándo usar corchetes.

## 9. Instrucciones visibles / Tu tarea

1. Ejecuta `tiempos_viaje(3)`.
2. Observa el error.
3. Cambia los símbolos necesarios.
4. Ejecuta de nuevo.

## 10. Starter code definitivo

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

# Este código tiene un problema
tiempos_viaje(3)
```

## 11. Acción esperada paso a paso

1. Ejecutar versión errónea.
2. Sustituir `()` por `[]`.
3. Ejecutar `tiempos_viaje[3]`.

## 12. Resultado esperado en consola

Antes aparecerá un error equivalente a tratar `tiempos_viaje` como función. Después:

```text
> tiempos_viaje[3]
[1] 35
```

## 13. Interpretación esperada

> Los paréntesis aparecen en llamadas como `c()` y `sum()`; los corchetes seleccionan elementos.

## 14. Solución interna de referencia

```r
tiempos_viaje <- c(25, 40, 35, 50, 30)

tiempos_viaje[3]
```

## 15. Habilidad objetivo vs. respuesta computacional

Escribir 35 evita el error, pero no corrige la confusión de sintaxis.

## 16. Checks semánticos recomendados

- Código final sin error.
- Selección equivalente a `[3]`.
- Resultado 35.

## 17. Estados de respuesta relevantes

- **Estado 1:** conserva paréntesis.
- **Estado 2:** escribe 35.
- **Estado 3:** corrige a corchetes.

## 18. Errores previsibles

- Mantener `()`.
- Escribir `c(3)`.
- Cambiar 3 por 35.
- Modificar el vector.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| Mantiene `()` | Confunde llamada/selección | Para elegir una posición usa corchetes `[]`. |
| Escribe 35 | Evita habilidad objetivo | 35 es correcto, pero queremos recuperarlo desde el vector. |
| Usa `c(3)` | Confunde combinar/seleccionar | `c()` combina valores; no selecciona por sí solo. |
| Modifica vector | Busca error en lugar equivocado | Los valores están bien. Revisa los símbolos después del nombre. |

## 20. Pista 1 — conceptual

> El vector está correcto. Recuerda cómo pedíamos una posición.

## 21. Pista 2 — sintaxis

> La estructura es `nombre_del_vector[posición]`.

## 22. Pista 3 — casi resuelta

```r
tiempos_viaje[3]
```

## 23. Mensaje de éxito

> **Corregiste la selección usando la sintaxis adecuada.**

## 24. Transición al siguiente ejercicio

> Ya conoces todas las piezas del módulo. El desafío final las combinará.

## 25. Nivel de andamiaje

**Medio**. la solución requiere un cambio mínimo.

## 26. Carga cognitiva

**Media**. hay fricción por el error, sin concepto nuevo.

## 27. Justificación pedagógica

El error aparece cuando `()` y `[]` ya tienen significado funcional, por lo que consolida en vez de confundir.


---

# Ejercicio 9 — Mini desafío: trabajar con varios valores

## 1. Función pedagógica en la secuencia

**Antes:** maneja habilidades por separado. **Después:** combina vectores, resume y selecciona valores dentro de un script estructurado.

## 2. Objetivo de aprendizaje en R

Integrar suma de vectores, `sum()` y selección por una o varias posiciones.

## 3. Idea sobre datos

Dos vectores correspondientes pueden generar nueva información; luego esa información puede resumirse o explorarse.

## 4. Pregunta o situación sustantiva

Cuatro personas informaron horas de trabajo remunerado y cuidado.

## 5. Prerrequisitos recuperados

Todo M2 y objetos de M1.

## 6. Concepto nuevo

Ninguno.

## 7. Contenido visible para el estudiante

En este desafío trabajarás con horas de **trabajo remunerado** y **cuidado** de cuatro personas.

Los dos vectores ya están creados. Completa el script para construir las horas totales, obtener un total general y recuperar posiciones concretas.

## 8. Objetivo visible

> Integrar combinación, resumen y selección de vectores.

## 9. Instrucciones visibles / Tu tarea

1. Crea `horas_totales` sumando los dos vectores.
2. Crea `total_horas` con `sum(horas_totales)`.
3. Crea `horas_persona_3` con el tercer valor.
4. Crea `horas_personas_2_4` con posiciones 2 y 4.
5. Ejecuta las consultas.

## 10. Starter code definitivo

```r
horas_trabajo <- c(8, 5, 7, 6)
horas_cuidado <- c(3, 4, 2, 5)

# Crea horas_totales


# Calcula el total general


# Guarda las horas de la tercera persona


# Guarda las horas de las personas 2 y 4


# Muestra los resultados
horas_totales
total_horas
horas_persona_3
horas_personas_2_4
```

## 11. Acción esperada paso a paso

1. Sumar vectores.
2. Aplicar `sum()`.
3. Seleccionar `[3]`.
4. Seleccionar `[c(2,4)]`.
5. Consultar.

## 12. Resultado esperado en consola

```text
> horas_totales
[1] 11 9 9 11

> total_horas
[1] 40

> horas_persona_3
[1] 9

> horas_personas_2_4
[1] 9 11
```

## 13. Interpretación esperada

> El script produce un vector por persona, un total general y dos selecciones por posición.

## 14. Solución interna de referencia

```r
horas_trabajo <- c(8, 5, 7, 6)
horas_cuidado <- c(3, 4, 2, 5)

horas_totales <- horas_trabajo + horas_cuidado
total_horas <- sum(horas_totales)
horas_persona_3 <- horas_totales[3]
horas_personas_2_4 <- horas_totales[c(2, 4)]

horas_totales
total_horas
horas_persona_3
horas_personas_2_4
```

## 15. Habilidad objetivo vs. respuesta computacional

Hardcodear resultados produce estados correctos, pero no demuestra las habilidades integradas.

## 16. Checks semánticos recomendados

- `horas_totales` = c(11,9,9,11) desde ambos vectores.
- `total_horas` = 40 con `sum()`.
- `horas_persona_3` = 9 desde `[3]`.
- `horas_personas_2_4` = c(9,11) desde `[c(2,4)]`.

## 17. Estados de respuesta relevantes

- **Estado 1:** solo vectores iniciales.
- **Estado 2:** algunas transformaciones.
- **Estado 3:** hardcodeo o habilidad faltante.
- **Estado 4:** cuatro piezas construidas correctamente.

## 18. Errores previsibles

- Usar `sum()` para `horas_totales`.
- Hardcodear.
- Seleccionar desde objeto equivocado.
- Usar `[2,4]`.

## 19. Feedback diagnóstico por error

| Error o estado | Confusión que revela | Feedback final |
|---|---|---|
| `horas_totales` es un número | Confunde total por persona/general | Primero necesitamos un valor por persona. Suma directamente los dos vectores. |
| Hardcodea | Evita reutilización | Los valores son correctos, pero construye los resultados desde los objetos disponibles. |
| Vector equivocado | No sigue pregunta | Las selecciones pedidas corresponden a `horas_totales`. |
| `[2,4]` | No combina posiciones | Combina las posiciones con `c()` dentro de los corchetes. |

## 20. Pista 1 — conceptual

> Construye primero `horas_totales`. Los demás resultados pueden salir de ese objeto.

## 21. Pista 2 — sintaxis

> Necesitarás `+`, luego `sum()`, `[3]` y `[c(2, 4)]`.

## 22. Pista 3 — casi resuelta

```r
horas_totales <- horas_trabajo + horas_cuidado
total_horas <- sum(horas_totales)
horas_persona_3 <- horas_totales[___]
```

## 23. Mensaje de éxito

> **Integraste las principales operaciones del módulo con vectores.**

## 24. Transición al siguiente ejercicio

> Ya puedes elegir valores cuando conoces sus posiciones. El próximo módulo preguntará qué hacer cuando quieres seleccionar según una condición y no conoces las posiciones.

## 25. Nivel de andamiaje

**Bajo dentro del módulo**. el starter mantiene contexto y nombres, pero deja cuatro construcciones.

## 26. Carga cognitiva

**Media**. integra habilidades ya practicadas sin sintaxis nueva.

## 27. Justificación pedagógica

Cierra M2 exactamente en la frontera que necesita M3: seleccionar por posición funciona, pero aún falta seleccionar según una pregunta.


---

# Auditoría final del módulo

## Auditoría de secuencia

| Ejercicio | Capacidad antes | Capacidad después | Sintaxis nueva | Carga | Andamiaje |
|---|---|---|---|---|---|
| E1 | Objeto con un valor | Reconoce varios valores | `c()` dada | Baja-media | Muy alto |
| E2 | Reconoce vector | Crea vector | `c()` producida | Baja-media | Alto |
| E3 | Vector numérico | Generaliza tipos | Ninguna | Baja-media | Alto |
| E4 | Varios valores | Resume en total | `sum()` | Media | Medio |
| E5 | Vector completo | Selecciona posición | `[]` | Media | Alto-medio |
| E6 | Una posición | Selecciona varias | `[c(...)]` | Media | Medio |
| E7 | Comprende posiciones | Combina vectores | Ninguna | Media | Medio |
| E8 | Conoce `()`/`[]` | Depura confusión | Ninguna | Media | Medio |
| E9 | Habilidades separadas | Integra script | Ninguna | Media | Bajo |

## Auditoría de prerrequisitos

M2 recupera `<-`, objetos, tipos, `+` y consulta desde M1. `c()` se observa en E1 antes de producirse en E2. `sum()` aparece tras establecer vector. `[]` aparece en E5; suma vector + vector recién en E7, cuando posición ya tiene significado.

## Auditoría de fading

El andamiaje vuelve a alto con `c()`, luego baja gradualmente hacia integración. Las novedades (`sum()`, `[]`) aparecen con datos y contexto ya preparados.

## Auditoría de recuperación

Objetos y consulta reaparecen constantemente; tipos se recuperan en E3; `+` vuelve en E7; `c()` reaparece en E2, E3 y E6/E9; posición se recupera desde E5 hasta E9.

## Auditoría de errores

Los errores progresan desde construcción de `c()` a valor vs posición y finalmente `()` vs `[]`.

## Prueba de transferencia final

```r
horas_estudio <- c(2, 4, 3, 5, 1)

total <- sum(horas_estudio)

horas_estudio[4]
horas_estudio[c(2, 5)]
```

Debería poder explicar qué contiene el vector, qué hace `sum()` y qué significan las posiciones.

## Nota de continuidad longitudinal

M2 termina deliberadamente sin comparaciones. M3 podrá abrir con la limitación de conocer posiciones.
