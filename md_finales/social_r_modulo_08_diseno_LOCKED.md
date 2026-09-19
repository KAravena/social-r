# Social R — Módulo 8
## Describir cantidades

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede reconocer y describir variables categóricas, preparar datos y revisar missing, pero todavía no sabe cómo describir una variable cuyos valores representan cantidades.

### Capacidad después
Puede reconocer una variable cuantitativa por el significado de sus valores, observar su distribución, describir su centro mediante media y mediana, interpretar su dispersión mediante desviación estándar y elegir un resumen razonable según la distribución y la pregunta.

### Pregunta central
¿Cómo describo una variable cuyos valores representan cantidades sin reducirla automáticamente a un solo número?

### Modelo mental
`¿QUÉ REPRESENTAN LOS VALORES? → CANTIDADES → VARIABLE CUANTITATIVA → MIRAR LA DISTRIBUCIÓN → CENTRO → MEDIA / MEDIANA → COMPARAR → ELEGIR SEGÚN DISTRIBUCIÓN + PREGUNTA → DISPERSIÓN → DESVIACIÓN ESTÁNDAR → PREPARAR / REVISAR MISSING CUANDO CORRESPONDA → INTERPRETAR`

### Principio pedagógico central
M8 no enseña una lista de funciones estadísticas.

No:

```text
VARIABLE NUMÉRICA
↓
mean()
median()
sd()
```

Sí:

```text
¿QUÉ REPRESENTAN LOS VALORES?
↓
CANTIDADES
↓
¿CÓMO SE DISTRIBUYEN?
↓
¿DÓNDE ESTÁ EL CENTRO?
↓
¿QUÉ CENTRO ES MÁS INFORMATIVO AQUÍ?
↓
¿QUÉ TAN DISPERSOS ESTÁN LOS VALORES?
↓
INTERPRETAR
```

La idea nuclear del módulo es:

> **DISTRIBUCIÓN ANTES QUE RECETA.**

### Definición de variable cuantitativa
Una variable es **cuantitativa** cuando sus valores representan cantidades y las diferencias numéricas entre esos valores tienen significado en el contexto.

Ejemplos del curso:

- `edad`;
- `horas_estudio`;
- `horas_cuidado`;
- `minutos_viaje`.

Esto no significa que cualquier columna escrita con números sea cuantitativa.

Por ejemplo:

```text
zona_codigo

1 = Norte
2 = Centro
3 = Sur
```

sigue representando categorías.

Por tanto:

```text
NÚMERO
≠
NECESARIAMENTE CANTIDAD
```

La clasificación continúa dependiendo de lo que representan los valores.

### Habilidades nucleares
Al terminar M8, el estudiante debe poder:

- reconocer una variable cuantitativa por significado;
- distinguir cantidad de código numérico categórico;
- comprender qué significa observar una distribución;
- interpretar un histograma básico;
- distinguir histograma de gráfico de barras categórico;
- comprender la media como medida de centro;
- calcular media mediante `mean()`;
- interpretar una media en las unidades de la variable;
- comprender que una media no tiene que coincidir con un valor observado;
- comprender la mediana como centro del orden;
- calcular mediana mediante `median()`;
- comparar media y mediana;
- reconocer que un valor muy alejado puede modificar fuertemente la media;
- evitar convertir “valor muy alejado → mediana” en regla automática;
- comprender que conocer el centro no describe toda la distribución;
- comprender dispersión;
- calcular desviación estándar mediante `sd()`;
- interpretar la desviación estándar como resumen de dispersión alrededor de la media;
- interpretar `sd()` en las unidades originales de la variable;
- recuperar preparación de casos y variables antes de describir;
- recuperar missing antes de calcular cuando corresponda;
- distinguir N total de N disponible;
- describir autónomamente una variable cuantitativa nueva mediante centro, dispersión e interpretación.

### Habilidades funcionales
`hist()` es una herramienta funcional de apoyo visual.

El estudiante debe:

- reconocerla;
- ejecutarla cuando el código está disponible;
- interpretar qué muestra.

No se exige producción autónoma fuerte de `hist()` después de una semana.

`na.rm = TRUE` sigue siendo una construcción funcional heredada de M6. Se recupera únicamente cuando existe missing y después de diagnosticar cuántos datos faltan.

### Habilidades recuperadas
M8 recupera:

- `c()`;
- objetos;
- `<-`;
- `$`;
- `filter()`;
- `select()`;
- `|>`;
- `is.na()`;
- `sum(is.na())`;
- `na.rm = TRUE`;
- caso/fila;
- variable/columna;
- preparación de subconjuntos;
- distinción entre categoría y cantidad por significado.

Estas habilidades no se reenseñan desde cero.

### Habilidades pospuestas
No se introducen en M8:

- cuantiles;
- `quantile()`;
- IQR;
- `IQR()`;
- rango como función;
- `range()`;
- `summary()` como objetivo;
- varianza;
- `var()`;
- boxplot;
- `boxplot()`;
- `sort()` como herramienta curricular;
- error estándar;
- fórmula de desviación estándar;
- `n - 1`;
- diferencia muestra/población;
- normalidad;
- tests de normalidad;
- z-scores;
- skewness como coeficiente;
- kurtosis;
- reglas formales de outliers;
- trimmed mean;
- winsorization;
- transformación log;
- inferencia;
- scatterplot;
- correlación.

### Sintaxis nueva
- `hist()`;
- `mean()`;
- `median()`;
- `sd()`.

### Sintaxis funcional
- `hist()`;
- `na.rm = TRUE` recuperado desde M6.

### Sintaxis que NO se introduce
No se introducen las siguientes herramientas ni se muestran como código ejecutable:

```text
quantile()
IQR()
range()
summary()
var()
boxplot()
sort()
plot(x, y)
cor()
cor.test()
```

No se introducen nuevas funciones de dplyr.

### Dataset / contrato de datos
M8 conserva exactamente el contrato locked de `encuesta_social_demo`:

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

M8 no modifica ninguna celda.

Variables cuantitativas ya disponibles:

```text
edad
horas_estudio
horas_cuidado
```

`horas_cuidado` contiene missing.

### Política de variables del módulo
M8 no añade ninguna variable nueva a `encuesta_social_demo`.

Los ejercicios utilizan exclusivamente las variables locked, microvectores pedagógicos explícitos y la base nueva de Checkpoint C.

### Objetos pedagógicos auxiliares
Los siguientes microdatos quedan fijados contractualmente para aislar conceptos.

#### M8-E3

```r
minutos_lectura <- c(25, 10, 20, 30, 15, 22, 18)
```

#### M8-E4

```r
viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)

viaje_extremo <- c(20, 22, 24, 25, 26, 28, 120)
```

#### M8-E5

```r
grupo_a <- c(4, 4, 4, 4, 4)

grupo_b <- c(2, 3, 4, 5, 6)
```

Estos objetos:

- no modifican `encuesta_social_demo`;
- son microdatos pedagógicos;
- existen únicamente para hacer visible un concepto aislado;
- deben preservarse en implementación futura salvo cambio deliberado del Markdown locked.

### Dataset de Checkpoint C
M8-E7 utiliza una base nueva:

```text
encuesta_movilidad

id   transporte   minutos_viaje
1    Metro        25
2    Bus          30
3    Metro        32
4    Bus          28
5    Bicicleta    35
6    Metro        27
7    Bus          31
8    A pie        29
9    Metro        34
10   Bus          90
```

No contiene missing.

La variable objetivo es `minutos_viaje`.

### Estrategia de scaffolding
1. E1 formaliza cantidad/cuantiativa y entrega `hist()` completo.
2. E2 entrega un worked example completo de `mean()`.
3. E3 entrega un worked example completo de `median()` con N impar.
4. E4 retira los nombres de las funciones y obliga a recuperar ambos centros.
5. E5 introduce `sd()` mediante un contraste con mismo centro y distinta dispersión, seguido de una completion breve.
6. E6 combina preparación, missing y descriptivos con skeleton parcial.
7. E7 retira los nombres de las funciones y exige producción autónoma sobre una base nueva.

### Estrategia de fading
`LEER DISTRIBUCIÓN → OBSERVAR MEDIA → OBSERVAR MEDIANA → RECUPERAR AMBOS CENTROS → COMPRENDER DISPERSIÓN → INTEGRAR PREPARACIÓN/MISSING → TRANSFERIR`

Más concretamente:

```text
E1
código completo
↓
hist() funcional + lectura

E2
worked example
↓
mean()

E3
worked example
↓
median()

E4
comentarios solamente
↓
mean + median

E5
worked example + completion
↓
sd()

E6
skeleton parcial
↓
preparación + missing + mean + sd

E7
comentarios mínimos
↓
mean + median + sd autónomos
```

### Riesgos cognitivos
- número = variable cuantitativa;
- histograma = gráfico de barras categórico con números;
- una barra de histograma = una persona;
- media = valor más frecuente;
- media = valor que necesariamente aparece en los datos;
- media = punto medio entre mínimo y máximo;
- mediana sin ordenar;
- aprender “valor extremo → siempre mediana”;
- creer que la media es incorrecta cuando cambia por un valor alejado;
- mismo centro = misma distribución;
- `sd()` = error estándar;
- `sd()` = error del cálculo;
- `sd()` = porcentaje;
- olvidar las unidades de `sd()`;
- usar `na.rm = TRUE` automáticamente;
- olvidar N disponible;
- hardcodear resultados numéricos;
- memorizar funciones sin interpretar.

### Política de tolerancia numérica
Los resultados decimales no se comparan como strings.

La implementación futura debe usar comparación numérica con tolerancia apropiada.

No se exige `round()`.

Ejemplos:

```text
37.857142857...
1.581138830...
1.488047618...
4.666666667...
4.163331999...
19.185932346...
```

son resultados válidos sin exigir una cantidad específica de decimales.

### Número de ejercicios
7

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M8-E1 | Mira la distribución | PRÁCTICA / VISUALIZACIÓN FUNCIONAL | formalización de cuantitativa + lectura funcional de `hist()` | significado de variable, barplot como contraste | baja-media |
| M8-E2 | ¿Dónde está el centro? | NOVEDAD | media + `mean()` | vector, `$`, unidades | baja-media |
| M8-E3 | Otro centro posible | NOVEDAD | mediana + `median()` | orden y posición | baja-media |
| M8-E4 | ¿Cuál centro describe mejor? | INTEGRACIÓN | ninguna | `mean()`, `median()` | media |
| M8-E5 | ¿Qué tan distintos son los valores? | NOVEDAD | dispersión + `sd()` | media/mediana | media |
| M8-E6 | Primero prepara, después describe | RECUPERACIÓN | ninguna | M5 + M6 + `mean()` + `sd()` | media-alta |
| M8-E7 | Checkpoint C: describe una variable nueva | TRANSFERENCIA / CHECKPOINT | ninguna | ruta cuantitativa completa | media |

---
## M8-E1 — Mira la distribución

### 1. Rol pedagógico
PRÁCTICA / VISUALIZACIÓN FUNCIONAL.

### 2. Por qué existe
M7 terminó distinguiendo categorías de cantidades, pero dejó deliberadamente para M8 la formalización de la ruta cuantitativa.

E1 debe impedir que el estudiante salte directamente desde “veo números” hacia una función resumen.

Su función es construir:

```text
CANTIDAD
↓
VARIABLE CUANTITATIVA
↓
DISTRIBUCIÓN
↓
MIRAR ANTES DE RESUMIR
```

`hist()` aparece únicamente como herramienta funcional para observar la distribución.

### 3. Capacidad antes
Puede reconocer una variable categórica por significado y sabe que algunos valores representan cantidades, pero todavía no dispone de una ruta explícita para describir esas cantidades.

### 4. Capacidad después
Puede reconocer una variable cuantitativa por significado, explicar qué significa observar su distribución e interpretar funcionalmente un histograma básico sin confundirlo con un gráfico de barras categórico.

### 5. Prerrequisitos
- variable;
- caso;
- `$`;
- lectura de una columna;
- criterio semántico de M7;
- lectura funcional de `barplot()`.

No requiere media, mediana, dispersión ni missing.

### 6. Gran novedad
- **Sintaxis nueva:** `hist()` como micro-novedad funcional.
- **Concepto nuevo:** distribución cuantitativa.
- **Formalización:** variable cuantitativa.
- **Decisión:** observar la distribución antes de reducirla a un número.

No se exige producción autónoma de `hist()`.

### 7. Recuperaciones
Recupera desde M7:

```text
¿QUÉ REPRESENTAN LOS VALORES?
```

y la comparación visual con `barplot()`.

Recupera `$` desde M4.

### 8. Contexto sustantivo
Horas de estudio reportadas por ocho personas de `encuesta_social_demo`.

### 9. Dataset / objetos
Variable:

```r
encuesta_social_demo$horas_estudio
```

Valores:

```text
3, 5, 2, 4, 6, 3, 5, 2
```

Ordenados únicamente para documentación pedagógica:

```text
2, 2, 3, 3, 4, 5, 5, 6
```

No se introduce `sort()`.

### 10. Texto para estudiante
En el módulo anterior describimos variables cuyos valores indicaban categorías.

`horas_estudio` es diferente.

Sus valores indican **cuántas horas** reportó cada persona.

Cuando los valores representan cantidades, hablamos de una **variable cuantitativa**.

Antes de resumirla con un número, conviene observar cómo se distribuyen sus valores.

Ejecuta:

```r
hist(encuesta_social_demo$horas_estudio)
```

Recuerda la diferencia:

```text
GRÁFICO DE BARRAS — M7

una barra
→ una categoría

altura
→ frecuencia de esa categoría
```

```text
HISTOGRAMA — M8

eje horizontal
→ valores de una cantidad

una barra
→ un intervalo de valores

altura
→ cuántos casos caen aproximadamente en ese intervalo
```

Observa el histograma y responde:

- ¿todos los casos tienen exactamente las mismas horas?
- ¿hay valores más bajos y más altos?
- ¿en qué rango general se encuentran las horas?

### 11. Modelo mental
```text
¿QUÉ REPRESENTAN LOS VALORES?
↓
CANTIDADES
↓
VARIABLE CUANTITATIVA
↓
DISTRIBUCIÓN
↓
OBSERVAR ANTES DE RESUMIR
```

### 12. Representación / código trabajado
Código completo:

```r
hist(encuesta_social_demo$horas_estudio)
```

No se personaliza el histograma.

### 13. Starter code
```r
hist(encuesta_social_demo$horas_estudio)
```

### 14. Acción esperada
1. reconocer `horas_estudio` como cuantitativa por significado;
2. ejecutar el histograma;
3. distinguirlo de un barplot categórico;
4. interpretar que los datos ocupan varios valores entre 2 y 6 horas.

### 15. Solución canónica
```r
hist(encuesta_social_demo$horas_estudio)
```

Respuesta conceptual esperada:

> `horas_estudio` representa cantidades. Los valores no son todos iguales y se distribuyen entre 2 y 6 horas.

### 16. Resultado esperado
Un histograma interpretable de:

```text
2, 2, 3, 3, 4, 5, 5, 6
```

No se fija el número exacto de barras como criterio de éxito porque M8 no enseña `breaks`.

### 17. Criterio semántico de éxito
Comprobar principalmente interpretación:

- `horas_estudio` representa cantidades;
- se reconoce como variable cuantitativa;
- el gráfico corresponde a esa variable;
- una barra del histograma representa un intervalo, no una categoría;
- los datos se encuentran entre 2 y 6 horas;
- no todos los casos tienen el mismo valor.

No evaluar estética, número exacto de bins ni personalización.

### 18. Estrategias alternativas válidas
Se acepta cualquier ejecución equivalente de `hist()` sobre `encuesta_social_demo$horas_estudio`.

No es necesario guardar previamente la variable en otro objeto.

No se considera superior una solución con personalización gráfica.

### 19. Error esperado / misconception
- número = cuantitativa automáticamente;
- histograma = barplot para números;
- cada barra = una persona;
- cada barra = un valor individual;
- altura = porcentaje sin revisar qué representa;
- intentar describir media/mediana antes de la pantalla correspondiente.

### 20. Feedback correcto
> Bien. Primero identificaste que `horas_estudio` representa cantidades y utilizaste el histograma para observar cómo se distribuyen antes de resumirlas.

### 21. Feedback resultado correcto / estrategia incorrecta
Si interpreta correctamente el rango pero dice que cada barra es una categoría:

> El rango está bien leído, pero en un histograma una barra no representa una categoría. Agrupa un intervalo de valores de una cantidad.

### 22. Hint 1
Pregunta primero qué representan los números de `horas_estudio`: ¿son códigos de grupos o cantidades de horas?

### 23. Hint 2
Son cantidades. El histograma permite observar cómo se reparten esos valores antes de resumirlos.

### 24. Hint 3
```r
hist(encuesta_social_demo$horas_estudio)
```

### 25. Predicción
Sí, conceptual.

Antes de ejecutar:

> ¿esperas que todas las personas tengan exactamente las mismas horas de estudio?

No se pide predecir la forma exacta del histograma.

### 26. Tipo de ejercicio
Ejecución / observación / interpretación.

### 27. Andamiaje
Alto. El código está completamente entregado y las preguntas dirigen la atención hacia el significado del gráfico.

### 28. Carga cognitiva
Baja-media. Interactúan la formalización de cuantitativa, la idea de distribución y una representación visual nueva; el objeto y el código están dados.

### 29. Fading
No se exige fading sintáctico fuerte de `hist()`. La reducción de apoyo del módulo se concentra en `mean()`, `median()` y `sd()`.

### 30. Recuperación futura
La idea de observar variables antes de asociarlas se recupera desde M9. `hist()` puede requerir recordatorio y eso es compatible con su estatus funcional.

### 31. Riesgo de aprendizaje superficial
Memorizar que “si hay números hago histograma” sin volver a preguntar qué representan. El criterio semántico de M7 debe mantenerse visible.

### 32. Criterio de transferencia
La lectura se considera transferible cuando puede mirar un histograma de otra variable cuantitativa y explicar qué representan el eje horizontal y las barras sin confundirlos con categorías.

### 33. Notas de implementación futura
No evaluar `breaks`, colores, títulos ni estética.

No introducir controles de personalización.

Mantener Ctrl+Enter como ejecución/observación y “Comprobar respuesta” como evaluación conceptual separada.

---
## M8-E2 — ¿Dónde está el centro?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Después de observar toda la distribución, el estudiante necesita una primera forma de resumir dónde se encuentra su centro. E2 introduce la media como respuesta a esa necesidad y no como función aislada.

### 3. Capacidad antes
Puede reconocer una variable cuantitativa y observar cómo se distribuyen sus valores.

### 4. Capacidad después
Puede comprender y calcular la media como una medida de centro que utiliza todos los valores e interpretarla en las unidades de la variable.

### 5. Prerrequisitos
Vector, variable cuantitativa, `$`, ejecución de funciones y lectura de un resultado numérico.

### 6. Gran novedad
- **Sintaxis nueva:** `mean()`.
- **Concepto nuevo:** media.
- **Modelo mental:** centro que utiliza todos los valores.
- **Decisión nueva:** ninguna grande todavía.

### 7. Recuperaciones
Recupera `$`, objeto → función → resultado y la idea de distribución construida en E1.

### 8. Contexto sustantivo
Horas de estudio de `encuesta_social_demo`.

### 9. Dataset / objetos
```text
horas_estudio

3, 5, 2, 4, 6, 3, 5, 2

N = 8
suma = 30
media = 3.75
```

No contiene missing.

### 10. Texto para estudiante
El histograma permite mirar toda la distribución.

Ahora queremos resumir **dónde está su centro**.

Una forma es la **media**.

Imagina que las 30 horas registradas se repartieran por igual entre los 8 casos:

```text
30 / 8 = 3.75
```

Esa idea de reparto igual ayuda a interpretar la media.

En R:

```r
mean(encuesta_social_demo$horas_estudio)
```

produce:

```text
3.75
```

La media es **3.75 horas de estudio**.

Importante:

> Ninguna persona necesita haber reportado exactamente 3.75 horas.
>
> La media puede quedar entre valores observados.

### 11. Modelo mental
```text
TODOS LOS VALORES
↓
UN CENTRO
↓
REPARTIR EL TOTAL EN PARTES IGUALES
↓
MEDIA
```

### 12. Representación / código trabajado
Worked example completo:

```r
mean(encuesta_social_demo$horas_estudio)
```

### 13. Starter code
```r
mean(encuesta_social_demo$horas_estudio)
```

### 14. Acción esperada
1. predecir que la media estará entre 2 y 6;
2. ejecutar;
3. leer 3.75;
4. interpretar 3.75 en horas;
5. reconocer que 3.75 no necesita ser un valor observado.

### 15. Solución canónica
```r
mean(encuesta_social_demo$horas_estudio)
```

### 16. Resultado esperado
```text
3.75
```

Interpretación:

> media = 3.75 horas de estudio.

### 17. Criterio semántico de éxito
Comprobar:

- utiliza `mean()` sobre la variable correcta;
- resultado numérico = 3.75;
- depende del objeto;
- interpreta el resultado como horas;
- no lo interpreta como personas;
- comprende que la media puede no coincidir con un dato observado.

### 18. Estrategias alternativas válidas
Se acepta:

```r
x <- encuesta_social_demo$horas_estudio
mean(x)
```

o cualquier estrategia equivalente que use `mean()` sobre los mismos datos.

No es necesario reconstruir manualmente `sum(x) / N`.

### 19. Error esperado / misconception
- media = valor más frecuente;
- media = valor central del orden;
- media = punto medio entre mínimo y máximo;
- media debe aparecer entre los datos;
- 3.75 personas;
- añadir `na.rm = TRUE` como ritual aunque no exista missing;
- escribir 3.75 directamente.

### 20. Feedback correcto
> Bien. La media utiliza todos los valores para resumir un centro. Aquí es 3.75 horas.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `3.75`:

> El número coincide, pero debe calcularse desde la variable. Si cambian las horas, la media tiene que actualizarse automáticamente.

Si añade `na.rm = TRUE`:

> El resultado coincide, pero aquí no hay datos ausentes. No necesitamos convertir `na.rm = TRUE` en una receta automática.

### 22. Hint 1
Necesitas un número que resuma el centro utilizando todos los valores.

### 23. Hint 2
La función para calcular la media es `mean()`.

### 24. Hint 3
```r
mean(encuesta_social_demo$horas_estudio)
```

### 25. Predicción
> Los valores van de 2 a 6 horas. ¿Esperas que la media esté dentro de ese intervalo?

Respuesta esperada: sí.

### 26. Tipo de ejercicio
Worked example.

### 27. Andamiaje
Alto. La función y la variable están completamente entregadas.

### 28. Carga cognitiva
Baja-media. La única gran novedad es la media; la variable es conocida y no contiene missing.

### 29. Fading
E2 entrega `mean()` completo. E4 retirará el nombre de la función y E7 exigirá producción autónoma.

### 30. Recuperación futura
`mean()` reaparece en E4, E6 y E7; después se recupera al preparar variables para asociaciones y se transfiere en M13.

### 31. Riesgo de aprendizaje superficial
Aprender `mean()` como comando sin interpretar unidades o creer que 3.75 tiene que ser una respuesta individual real.

### 32. Criterio de transferencia
La habilidad estará disponible cuando pueda calcular e interpretar la media de otra variable cuantitativa sin que la consigna entregue la función.

### 33. Notas de implementación futura
Perturbation test recomendado: cambiar uno o más valores y verificar que la media se derive del objeto. No comparar código literal.

---
## M8-E3 — Otro centro posible

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Una sola medida de centro puede convertirse fácilmente en receta. E3 introduce una segunda forma de representar el centro y construye la mediana desde el orden de los valores.

### 3. Capacidad antes
Comprende la media como una medida de centro que utiliza todos los valores.

### 4. Capacidad después
Comprende la mediana como centro del orden y puede calcularla con `median()` en un caso introductorio de N impar.

### 5. Prerrequisitos
Orden y posición desde M2, vectores, ejecución de funciones y concepto de centro desde E2.

### 6. Gran novedad
- **Sintaxis nueva:** `median()`.
- **Concepto nuevo:** mediana.
- **Modelo mental nuevo:** ordenar → centro del orden.
- **Decisión nueva:** reconocer otra forma de resumir centro.

### 7. Recuperaciones
Recupera orden y posición de M2. Contrasta con la media aprendida en E2 sin pedir todavía elección entre ambas.

### 8. Contexto sustantivo
Minutos de lectura diaria en siete casos de ejemplo.

### 9. Dataset / objetos
Objeto pedagógico:

```r
minutos_lectura <- c(25, 10, 20, 30, 15, 22, 18)
```

Orden conceptual:

```text
10, 15, 18, 20, 22, 25, 30
```

N = 7.

Valor central = 20.

### 10. Texto para estudiante
La media utiliza la magnitud de todos los valores.

Existe otra forma de describir el centro.

Observa:

```text
25, 10, 20, 30, 15, 22, 18
```

Si los ordenamos mentalmente:

```text
10, 15, 18, 20, 22, 25, 30
```

hay un valor exactamente en el centro:

```text
20
```

Ese centro se llama **mediana**.

En R:

```r
median(minutos_lectura)
```

No necesitamos aprender una función para ordenar en esta pantalla. El orden es parte de la idea que queremos comprender.

### 11. Modelo mental
```text
ORDENAR LOS VALORES
↓
BUSCAR EL CENTRO DEL ORDEN
↓
MEDIANA
```

### 12. Representación / código trabajado
Objeto disponible:

```r
minutos_lectura <- c(25, 10, 20, 30, 15, 22, 18)
```

Worked example:

```r
median(minutos_lectura)
```

### 13. Starter code
```r
median(minutos_lectura)
```

### 14. Acción esperada
1. observar el vector original;
2. identificar el orden conceptual mostrado;
3. predecir el valor central;
4. ejecutar `median()`;
5. interpretar 20 como centro del orden.

### 15. Solución canónica
```r
median(minutos_lectura)
```

### 16. Resultado esperado
```text
20
```

Interpretación:

> 20 minutos es el valor central cuando los siete valores se ordenan.

### 17. Criterio semántico de éxito
Comprobar:

- utiliza `median()`;
- utiliza el objeto correcto;
- resultado = 20;
- comprende “centro del orden”;
- no sustituye la tarea por la media;
- no hardcodea 20.

### 18. Estrategias alternativas válidas
Se acepta guardar el vector en otro objeto equivalente y aplicar `median()`.

No se exige `sort()` y no se considera necesario producir manualmente la posición central.

### 19. Error esperado / misconception
- escoger el cuarto valor de la secuencia original sin ordenar;
- confundir mediana con media;
- confundir mediana con valor más frecuente;
- creer que siempre debe existir un único valor central incluso con N par;
- introducir `sort()` innecesariamente.

### 20. Feedback correcto
> Bien. La mediana depende del orden de los valores. Con siete observaciones, 20 queda exactamente en el centro.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `20`:

> El valor coincide, pero debe derivarse de los datos. En otro vector el centro puede cambiar.

Si obtiene 20 por una operación distinta:

> El resultado coincide, pero esta pantalla evalúa la mediana como centro del orden y su cálculo mediante `median()`.

### 22. Hint 1
Ordena mentalmente los valores de menor a mayor y busca qué queda en el centro.

### 23. Hint 2
La función que calcula la mediana es `median()`.

### 24. Hint 3
```r
median(minutos_lectura)
```

### 25. Predicción
> Después de ordenar los siete valores, ¿qué valor queda exactamente en el centro?

Respuesta: 20.

### 26. Tipo de ejercicio
Worked example conceptual + ejecución.

### 27. Andamiaje
Alto. Se muestra explícitamente el orden y se entrega la función.

### 28. Carga cognitiva
Baja-media. El uso de N impar evita introducir simultáneamente el caso de dos valores centrales.

### 29. Fading
E3 entrega `median()` completo. E4 exige recuperarlo sin nombrar la función y E7 lo exige sobre una base nueva.

### 30. Recuperación futura
`median()` se integra en E4, se produce autónomamente en E7 y se recupera al conocer variables antes de asociaciones y en M13.

### 31. Riesgo de aprendizaje superficial
Memorizar “mediana = valor del medio” sin comprender que el centro se define después de ordenar.

### 32. Criterio de transferencia
La habilidad está disponible cuando puede aplicar `median()` a otra variable e interpretar el resultado como centro del orden, incluso si el nombre/contexto cambia.

### 33. Notas de implementación futura
No introducir `sort()`, fórmula de posiciones ni caso N par como gran novedad en esta pantalla. Perturbation test recomendado.

---
## M8-E4 — ¿Cuál centro describe mejor?

### 1. Rol pedagógico
INTEGRACIÓN.

### 2. Por qué existe
Media y mediana no deben quedar como dos comandos paralelos sin propósito. E4 crea una situación en que ambas medidas cuentan historias diferentes y obliga a relacionar la elección del centro con la distribución y la pregunta.

### 3. Capacidad antes
Puede calcular e interpretar media y mediana en ejemplos separados.

### 4. Capacidad después
Puede recuperar ambas medidas, comparar su sensibilidad ante un valor muy alejado y justificar cuál resulta más informativa para describir un tiempo típico sin declarar incorrecta a la otra.

### 5. Prerrequisitos
`mean()`, `median()`, vectores, interpretación de centro y lectura básica de distribución.

### 6. Gran novedad
No hay sintaxis nueva. La demanda es integrar dos medidas conocidas y tomar una decisión contextual.

### 7. Recuperaciones
Recupera `c()`, objetos, `mean()`, `median()` y la idea de distribución de E1.

### 8. Contexto sustantivo
Tiempos de viaje en dos grupos pedagógicos casi idénticos.

### 9. Dataset / objetos
```r
viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)

viaje_extremo <- c(20, 22, 24, 25, 26, 28, 120)
```

Solo cambia:

```text
30 → 120
```

### 10. Texto para estudiante
Observa dos grupos de tiempos de viaje:

```text
viaje_regular
20, 22, 24, 25, 26, 28, 30

viaje_extremo
20, 22, 24, 25, 26, 28, 120
```

La mayoría de los valores es la misma.

Solo cambia el último:

```text
30 → 120
```

Antes de calcular:

> ¿qué medida esperas que cambie más: la media o la mediana?

Calcula los dos centros en ambos grupos.

Después responde:

> Si queremos describir un tiempo de viaje típico en `viaje_extremo`, ¿qué centro resulta más informativo y por qué?

### 11. Modelo mental
```text
DISTRIBUCIÓN
↓
DOS CENTROS
↓
VALOR MUY ALEJADO
↓
MEDIA CAMBIA MUCHO
MEDIANA CAMBIA POCO
↓
ELEGIR SEGÚN DISTRIBUCIÓN + PREGUNTA
```

### 12. Representación / código trabajado
No se entrega la solución. Los dos vectores quedan definidos y visibles.

### 13. Starter code
```r
viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)

viaje_extremo <- c(20, 22, 24, 25, 26, 28, 120)

# calcula la media de viaje_regular


# calcula la mediana de viaje_regular


# calcula la media de viaje_extremo


# calcula la mediana de viaje_extremo
```

### 14. Acción esperada
1. predecir cuál centro cambiará más;
2. producir media y mediana de `viaje_regular`;
3. producir media y mediana de `viaje_extremo`;
4. comparar;
5. justificar una elección para “tiempo típico”.

### 15. Solución canónica
```r
mean(viaje_regular)
median(viaje_regular)

mean(viaje_extremo)
median(viaje_extremo)
```

### 16. Resultado esperado
```text
viaje_regular
media   = 25
mediana = 25

viaje_extremo
media   = 37.857142857...
mediana = 25
```

En texto puede mostrarse:

```text
media de viaje_extremo ≈ 37.86 minutos
```

No exigir redondeo.

### 17. Criterio semántico de éxito
Comprobar:

- cuatro resultados derivados de los objetos;
- usa `mean()`;
- usa `median()`;
- 25 / 25 para `viaje_regular`;
- ≈37.857 / 25 para `viaje_extremo`;
- reconoce que la media cambia más;
- reconoce que la mediana permanece 25;
- relaciona el cambio con 120;
- para “tiempo típico”, justifica la mediana desde la distribución;
- no declara que la media sea incorrecta;
- no convierte “valor alejado → mediana” en regla universal.

### 18. Estrategias alternativas válidas
Se aceptan cálculos equivalentes de ambas medidas sobre cada objeto.

La interpretación puede usar expresiones como “valor muy alejado”, “caso muy alto” o equivalentes sin exigir el término técnico outlier.

### 19. Error esperado / misconception
- media siempre mejor;
- mediana siempre mejor;
- 120 hace que la media sea “incorrecta”;
- si media y mediana difieren hay un error;
- elegir sin mencionar distribución;
- hardcodear los cuatro resultados.

### 20. Feedback correcto
> Bien. La media usa la magnitud de todos los valores y por eso 120 la desplaza mucho. La mediana depende del orden y permanece en 25. La elección depende de qué queremos describir.

### 21. Feedback resultado correcto / estrategia incorrecta
Si elige mediana solo porque “siempre se usa con valores extremos”:

> La elección coincide en este contexto, pero evita convertirla en regla automática. La razón está en esta distribución y en la pregunta por un tiempo típico.

### 22. Hint 1
Compara qué ocurre con cada centro cuando solo cambia el último valor.

### 23. Hint 2
Recupera las dos funciones de centro que aprendiste en E2 y E3.

### 24. Hint 3
```r
mean(viaje_regular)
median(viaje_regular)

mean(viaje_extremo)
median(viaje_extremo)
```

### 25. Predicción
> ¿Qué centro cambiará más cuando 30 se reemplaza por 120?

Respuesta esperada: la media.

### 26. Tipo de ejercicio
Integración + decisión.

### 27. Andamiaje
Medio. Los objetos están dados, pero las funciones no aparecen en los comentarios.

### 28. Carga cognitiva
Media. No hay sintaxis nueva; la dificultad proviene de coordinar dos medidas e interpretar una diferencia sustantiva.

### 29. Fading
Respecto de E2/E3 se retiran los nombres de las funciones. E7 volverá a exigir ambas sin nombrarlas.

### 30. Recuperación futura
La comparación centro/distribución reaparece en Checkpoint C y como conocimiento previo antes de asociaciones.

### 31. Riesgo de aprendizaje superficial
Aprender una regla binaria “outlier = mediana”. El feedback debe preservar que la media sigue describiendo el balance aritmético de todos los valores.

### 32. Criterio de transferencia
Debe poder justificar una elección de centro en una distribución nueva observando la estructura de los datos y la pregunta, no una palabra clave.

### 33. Notas de implementación futura
Usar tolerancia numérica para 37.857142857. Perturbation test: sustituir 120 por otro valor alto y verificar que la solución siga dependiendo de los objetos.

---
## M8-E5 — ¿Qué tan distintos son los valores?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Centro no basta para describir una distribución. E5 construye esa necesidad mostrando dos grupos con exactamente el mismo centro pero distinta separación entre sus valores.

### 3. Capacidad antes
Puede describir y comparar el centro mediante media y mediana.

### 4. Capacidad después
Puede comprender dispersión, calcular desviación estándar mediante `sd()` e interpretarla en las unidades de la variable.

### 5. Prerrequisitos
Media, mediana, vectores, interpretación numérica y comparación de grupos.

### 6. Gran novedad
- **Sintaxis nueva:** `sd()`.
- **Concepto nuevo:** dispersión.
- **Medida nueva:** desviación estándar.
- **Decisión nueva:** reconocer que centro y dispersión son información complementaria.

### 7. Recuperaciones
Recupera media/mediana únicamente para demostrar que dos distribuciones pueden compartir centro.

### 8. Contexto sustantivo
Microdatos pedagógicos sin contexto complejo para aislar la idea de dispersión. Después se aplica `sd()` a `horas_estudio`.

### 9. Dataset / objetos
```r
grupo_a <- c(4, 4, 4, 4, 4)

grupo_b <- c(2, 3, 4, 5, 6)
```

Ambos:

```text
media = 4
mediana = 4
```

Desviaciones estándar:

```text
grupo_a → 0
grupo_b → 1.581138830...
```

### 10. Texto para estudiante
Observa:

```text
Grupo A
4, 4, 4, 4, 4

Grupo B
2, 3, 4, 5, 6
```

Los dos grupos tienen:

```text
media = 4
mediana = 4
```

Pregunta:

> Si ambos tienen el mismo centro, ¿son realmente iguales?

No.

En A todos los valores son iguales.

En B los valores se separan alrededor de 4.

Necesitamos describir otra propiedad:

# DISPERSIÓN

La **desviación estándar** resume cuánto se separan los valores alrededor de su media.

Cuando comparamos la misma variable en la misma unidad:

> una desviación estándar mayor indica mayor dispersión.

Ejecuta:

```r
sd(grupo_a)

sd(grupo_b)
```

Después aplica la misma herramienta a `horas_estudio`.

### 11. Modelo mental
```text
MISMO CENTRO
≠
MISMA DISTRIBUCIÓN
↓
¿QUÉ TAN SEPARADOS ESTÁN LOS VALORES?
↓
DISPERSIÓN
↓
DESVIACIÓN ESTÁNDAR
↓
sd()
```

### 12. Representación / código trabajado
Worked example:

```r
sd(grupo_a)

sd(grupo_b)
```

Después completion sobre la variable real.

### 13. Starter code
```r
sd(grupo_a)

sd(grupo_b)

# ahora calcula la desviación estándar de horas_estudio
sd(_____________________________)
```

### 14. Acción esperada
1. predecir si dos grupos con igual media pueden tener distinta dispersión;
2. ejecutar `sd()` en ambos grupos;
3. interpretar 0 frente a ≈1.58;
4. completar `sd()` para `horas_estudio`;
5. interpretar el resultado en horas.

### 15. Solución canónica
```r
sd(grupo_a)

sd(grupo_b)

sd(encuesta_social_demo$horas_estudio)
```

### 16. Resultado esperado
```text
sd(grupo_a)
= 0

sd(grupo_b)
≈ 1.581138830

sd(encuesta_social_demo$horas_estudio)
≈ 1.488047618
```

Interpretación de la última:

> desviación estándar ≈ 1.49 horas.

### 17. Criterio semántico de éxito
Comprobar:

- `sd(grupo_a)` = 0;
- `sd(grupo_b)` ≈ 1.581;
- reconoce B como más disperso;
- comprende que A tiene sd 0 porque todos sus valores son iguales;
- produce `sd(encuesta_social_demo$horas_estudio)`;
- resultado ≈1.488;
- interpreta las unidades como horas;
- no llama a sd “error”.

### 18. Estrategias alternativas válidas
Se acepta guardar `horas_estudio` en un objeto antes de aplicar `sd()`.

No se exige calcular manualmente la desviación estándar ni conocer su fórmula.

### 19. Error esperado / misconception
- misma media = misma distribución;
- sd = error estándar;
- sd = error del análisis;
- sd = rango;
- sd = porcentaje;
- sd = cantidad de casos;
- sd mayor = datos “peores”;
- olvidar unidades;
- intentar usar `var()`.

### 20. Feedback correcto
> Bien. Los grupos comparten el mismo centro, pero B tiene mayor dispersión. `sd()` permite resumir esa diferencia.

### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene valores correctos pero interpreta sd como error:

> Los cálculos coinciden, pero la desviación estándar no es un error del análisis. Resume cuánto se dispersan los valores alrededor de la media.

### 22. Hint 1
El centro ya es igual en ambos grupos. Falta describir cuánto se separan sus valores.

### 23. Hint 2
La función que resume esta dispersión es `sd()`.

### 24. Hint 3
```r
sd(grupo_a)
sd(grupo_b)

sd(encuesta_social_demo$horas_estudio)
```

### 25. Predicción
> Si dos grupos tienen la misma media, ¿pueden tener distinta dispersión?

Respuesta: sí.

Después: ¿qué grupo esperas que tenga mayor `sd()`?

Respuesta: B.

### 26. Tipo de ejercicio
Worked example + completion.

### 27. Andamiaje
Alto en el primer contraste y medio en la aplicación a `horas_estudio`.

### 28. Carga cognitiva
Media. Se introduce una propiedad nueva de la distribución y una función nueva, pero con un contraste deliberadamente simple.

### 29. Fading
E5 entrega `sd()` en el primer contraste y exige completar la aplicación. E6 y E7 exigirán recuperarlo con menos apoyo.

### 30. Recuperación futura
`sd()` se recupera en E6, se produce en E7 y vuelve a utilizarse al conocer variables antes de asociación y en M13.

### 31. Riesgo de aprendizaje superficial
Memorizar que “sd grande = malo” o tratarlo como error estándar. Las unidades y el contraste entre A/B deben mantenerse visibles.

### 32. Criterio de transferencia
Debe poder comparar dispersión entre dos conjuntos de la misma variable y explicar qué significa una `sd()` mayor sin recurrir a la fórmula.

### 33. Notas de implementación futura
No introducir varianza, `n - 1` ni población/muestra. Usar tolerancia numérica. Perturbation tests recomendados.

---
## M8-E6 — Primero prepara, después describe

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
M8 no debe enseñar descriptivos como si siempre llegaran sobre un vector limpio. E6 recupera la ruta real del curso: preparar los casos pertinentes, revisar missing y recién después calcular centro y dispersión.

### 3. Capacidad antes
Puede calcular media, mediana y desviación estándar en datos ya preparados.

### 4. Capacidad después
Puede preparar un subconjunto, diagnosticar missing y calcular media y dispersión sobre los valores disponibles sin confundir N total con N disponible.

### 5. Prerrequisitos
Desde M5:

- `filter()`;
- `select()`;
- `|>`.

Desde M6:

- `is.na()`;
- `sum(is.na())`;
- `na.rm = TRUE`;
- N total vs N disponible.

Desde M8:

- `mean()`;
- `sd()`.

### 6. Gran novedad
Ninguna. Toda la sintaxis ya está disponible. La dificultad proviene de coordinar habilidades en el orden correcto.

### 7. Recuperaciones
M5 + M6 + M8. No se exige `median()` para evitar acumulación innecesaria.

### 8. Contexto sustantivo
Horas de cuidado entre personas que no trabajan.

### 9. Dataset / objetos
Usar `encuesta_social_demo`.

Condición:

```r
trabaja == "No"
```

Casos pertinentes:

```text
1, 3, 4, 7
```

Objeto final:

```text
datos_no_trabajan

id   horas_cuidado
1    6
3    0
4    8
7    NA
```

N total = 4.

Missing = 1.

N disponible = 3.

### 10. Texto para estudiante
Queremos describir las **horas de cuidado de las personas que no trabajan**.

Primero prepara los datos.

Crea un objeto llamado `datos_no_trabajan` que:

- conserve solo las personas que no trabajan;
- conserve únicamente `id` y `horas_cuidado`.

Después:

1. revisa cuántos valores de `horas_cuidado` faltan;
2. indica cuántos valores quedan disponibles;
3. calcula la media usando los valores disponibles;
4. calcula la desviación estándar usando los valores disponibles.

No agregues automáticamente una opción para omitir missing.

Primero debes saber cuántos datos faltan.

### 11. Modelo mental
```text
PREGUNTA SUSTANTIVA
↓
QUÉ CASOS
↓
filter()
↓
QUÉ VARIABLES
↓
select()
↓
REVISAR MISSING
↓
CONTAR
↓
N DISPONIBLE
↓
MEDIA + DISPERSIÓN
↓
INTERPRETAR
```

### 12. Representación / código trabajado
No hay worked example completo. El starter contiene únicamente el skeleton de preparación.

### 13. Starter code
```r
datos_no_trabajan <- encuesta_social_demo |>
  filter(__________________) |>
  select(____, ____________)

# cuenta cuántos valores faltan


# calcula la media con los valores disponibles


# calcula la dispersión con los valores disponibles
```

### 14. Acción esperada
1. completar el pipeline;
2. consultar/reconocer el subconjunto;
3. contar missing;
4. reconocer N disponible = 3;
5. calcular media con disponibles;
6. calcular sd con disponibles;
7. interpretar que ambos descriptivos utilizan 3 valores, no 4.

### 15. Solución canónica
```r
datos_no_trabajan <- encuesta_social_demo |>
  filter(trabaja == "No") |>
  select(id, horas_cuidado)

sum(is.na(datos_no_trabajan$horas_cuidado))

mean(datos_no_trabajan$horas_cuidado, na.rm = TRUE)

sd(datos_no_trabajan$horas_cuidado, na.rm = TRUE)
```

### 16. Resultado esperado
Subconjunto:

```text
id   horas_cuidado
1    6
3    0
4    8
7    NA
```

Missing:

```text
1
```

N disponible:

```text
3
```

Media:

```text
4.666666667...
```

Desviación estándar:

```text
4.163331999...
```

En texto:

```text
media ≈ 4.67 horas
sd    ≈ 4.16 horas
```

No exigir redondeo.

### 17. Criterio semántico de éxito
Comprobar:

- objeto `datos_no_trabajan`;
- filtro semántico `trabaja == "No"`;
- pipe nativo;
- selección de `id` y `horas_cuidado`;
- casos 1, 3, 4, 7;
- el `NA` permanece;
- conteo de missing depende de `is.na()`;
- missing = 1;
- N disponible = 3;
- media depende de `mean(..., na.rm = TRUE)`;
- sd depende de `sd(..., na.rm = TRUE)`;
- resultados correctos con tolerancia;
- interpreta que ambos descriptivos usan tres valores;
- no hardcoding.

### 18. Estrategias alternativas válidas
Se aceptan pipelines equivalentes que produzcan exactamente el mismo subconjunto mediante `filter()` y `select()`.

Se acepta guardar `datos_no_trabajan$horas_cuidado` en un vector intermedio antes de calcular.

La estrategia debe conservar el diagnóstico de missing antes de omitirlo.

### 19. Error esperado / misconception
- filtrar por posiciones 1,3,4,7;
- olvidar `select()`;
- creer que preparar elimina missing;
- calcular sin revisar missing;
- añadir `na.rm = TRUE` como reflejo automático;
- afirmar N = 4 para los descriptivos;
- tratar 0 como missing;
- hardcodear 1, 4.67 o 4.16;
- añadir mediana aunque no se solicita.

### 20. Feedback correcto
> Bien. Preparaste el grupo correcto, verificaste el missing y calculaste media y dispersión con los tres valores disponibles.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea filas:

> Esos casos coinciden con esta versión de los datos, pero el subconjunto debe depender de `trabaja == "No"`.

Si usa `na.rm = TRUE` sin diagnosticar:

> El cálculo puede coincidir, pero falta una decisión importante: antes de omitir valores ausentes debes saber cuántos faltan y cuántos entrarán al cálculo.

Si dice N = 4:

> El subconjunto tiene cuatro casos, pero `horas_cuidado` solo tiene tres valores disponibles.

### 22. Hint 1
Primero prepara el grupo correcto y conserva la variable que quieres describir. Después revisa si faltan datos.

### 23. Hint 2
Recupera `filter()` y `select()`. Después usa `is.na()` para diagnosticar antes de calcular con disponibles.

### 24. Hint 3
```r
datos_no_trabajan <- encuesta_social_demo |>
  filter(trabaja == "No") |>
  select(id, horas_cuidado)

sum(is.na(datos_no_trabajan$horas_cuidado))

mean(datos_no_trabajan$horas_cuidado, na.rm = TRUE)

sd(datos_no_trabajan$horas_cuidado, na.rm = TRUE)
```

### 25. Predicción
No se añade una fase separada. La tarea ya exige varias decisiones recuperadas.

### 26. Tipo de ejercicio
Recuperación integrada.

### 27. Andamiaje
Medio. El pipeline tiene huecos y los descriptivos aparecen solo como comentarios semánticos.

### 28. Carga cognitiva
Media-alta. Es la pantalla con mayor integración previa al checkpoint, pero no contiene sintaxis nueva y omite mediana deliberadamente.

### 29. Fading
Retira los nombres de `mean()`, `sd()` e `is.na()` de la consigna y deja solo un skeleton parcial del pipeline.

### 30. Recuperación futura
La secuencia preparar → revisar missing → describir se reutiliza al conocer variables antes de asociaciones en M9–M13.

### 31. Riesgo de aprendizaje superficial
Aprender que `na.rm = TRUE` es parte fija de `mean()`/`sd()`. La validación debe exigir diagnóstico de missing antes del cálculo.

### 32. Criterio de transferencia
La integración está disponible cuando el estudiante puede preparar otro grupo, diagnosticar sus ausencias y calcular descriptivos sobre los valores disponibles sin filas ni resultados manuales.

### 33. Notas de implementación futura
Perturbation tests muy recomendados: cambiar quién trabaja, mover NA, cambiar horas_cuidado y reordenar filas. El grader debe separar pipeline, missing y descriptivos.

---
## M8-E7 — Checkpoint C: describe una variable nueva

### 1. Rol pedagógico
TRANSFERENCIA / CHECKPOINT.

### 2. Por qué existe
Checkpoint C debe demostrar que el estudiante puede reconocer una cantidad nueva, producir las medidas nucleares de M8 sin que se nombren las funciones e interpretar centro y dispersión en una base distinta.

### 3. Capacidad antes
Ha trabajado distribución, media, mediana, elección de centro, dispersión y recuperación de preparación/missing.

### 4. Capacidad después
Puede describir autónomamente una variable cuantitativa nueva mediante media, mediana, desviación estándar e interpretación contextual, dejando lista la capacidad previa que M9 necesita.

### 5. Prerrequisitos
Criterio categoría/cantidad, `mean()`, `median()`, `sd()`, lectura funcional de histograma y razonamiento media vs mediana.

### 6. Gran novedad
Ninguna. Es transferencia y checkpoint. La dificultad está en elegir y coordinar herramientas ya aprendidas.

### 7. Recuperaciones
Recupera M7 solo como decisión de entrada: `minutos_viaje` representa cantidades. Recupera las habilidades nucleares de M8. No recupera missing porque E6 ya lo hizo.

### 8. Contexto sustantivo
Tiempos de traslado en una pequeña encuesta de movilidad.

### 9. Dataset / objetos
Base nueva:

```text
encuesta_movilidad

id   transporte   minutos_viaje
1    Metro        25
2    Bus          30
3    Metro        32
4    Bus          28
5    Bicicleta    35
6    Metro        27
7    Bus          31
8    A pie        29
9    Metro        34
10   Bus          90
```

Variable objetivo:

```text
minutos_viaje
```

No contiene missing.

N = 10.

### 10. Texto para estudiante
Queremos describir cuánto tardan las personas de `encuesta_movilidad` en llegar.

Primero responde:

> **¿`minutos_viaje` representa categorías o cantidades?**

Observa su distribución.

Después:

1. calcula las dos medidas de centro trabajadas en este módulo;
2. calcula la medida de dispersión aprendida;
3. compara los dos centros;
4. explica cuál describe mejor un tiempo de viaje típico en estos datos y por qué;
5. interpreta la dispersión en las unidades de la variable.

No se indican las funciones.

Decide qué herramientas ya conoces.

### 11. Modelo mental
```text
VARIABLE NUEVA
↓
¿QUÉ REPRESENTAN LOS VALORES?
↓
CANTIDADES
↓
DISTRIBUCIÓN
↓
DOS CENTROS
↓
COMPARAR
↓
DISPERSIÓN
↓
INTERPRETAR
```

### 12. Representación / código trabajado
`hist()` puede entregarse como apoyo visual:

```r
hist(encuesta_movilidad$minutos_viaje)
```

No forma parte del dominio sintáctico central del checkpoint.

No se entrega worked example para los descriptivos.

### 13. Starter code
```r
# calcula los dos centros aprendidos


# calcula la dispersión
```

### 14. Acción esperada
1. reconocer `minutos_viaje` como cuantitativa;
2. observar la distribución con apoyo;
3. producir media;
4. producir mediana;
5. producir sd;
6. comparar media y mediana;
7. relacionar la diferencia con 90;
8. elegir/justificar un centro típico;
9. interpretar sd en minutos.

### 15. Solución canónica
```r
mean(encuesta_movilidad$minutos_viaje)

median(encuesta_movilidad$minutos_viaje)

sd(encuesta_movilidad$minutos_viaje)
```

### 16. Resultado esperado
Valores:

```text
25, 30, 32, 28, 35, 27, 31, 29, 34, 90
```

Media:

```text
36.1
```

Mediana:

```text
30.5
```

Desviación estándar muestral de R:

```text
19.185932346...
```

En texto:

```text
sd ≈ 19.19 minutos
```

Interpretación conceptual esperada:

- la mayoría de los tiempos se encuentra aproximadamente entre 25 y 35 minutos;
- 90 está muy alejado del resto;
- la media se desplaza hacia arriba;
- la mediana cambia menos;
- para describir el centro del conjunto principal de tiempos, 30.5 resulta más informativa;
- la media no es incorrecta;
- la dispersión es considerable y se expresa en minutos.

### 17. Criterio semántico de éxito
Evaluar por componentes.

**Tipo**
- `minutos_viaje` = cantidades / variable cuantitativa por significado.

**Media**
- usa `mean()`;
- variable correcta;
- 36.1.

**Mediana**
- usa `median()`;
- variable correcta;
- 30.5.

**Dispersión**
- usa `sd()`;
- ≈19.1859;
- interpreta en minutos.

**Decisión**
- reconoce 90 como valor muy alejado;
- relaciona ese valor con el desplazamiento de la media;
- reconoce que la mediana es menos sensible;
- justifica desde la distribución y la pregunta;
- no afirma que la media esté “mal”.

**Estrategia**
- depende de los datos;
- no hardcoding.

### 18. Estrategias alternativas válidas
Se acepta guardar la variable en un vector:

```r
minutos <- encuesta_movilidad$minutos_viaje
mean(minutos)
median(minutos)
sd(minutos)
```

Se acepta ejecutar además `hist()` voluntariamente.

No se exige `hist()` para aprobar el checkpoint.

### 19. Error esperado / misconception
- clasificar por almacenamiento y no significado;
- producir solo una medida de centro;
- olvidar dispersión;
- llamar “promedio” únicamente a mediana;
- elegir mediana sin justificar;
- decir que media 36.1 es incorrecta;
- sd = error;
- sd = 19.19 %;
- hardcodear 36.1, 30.5 y 19.1859;
- intentar resolver una ruta categórica con `table()`.

### 20. Feedback correcto
> Bien. Reconociste una variable cuantitativa nueva, calculaste sus dos centros y su dispersión y relacionaste la diferencia entre media y mediana con la forma de los datos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea:

> Los números coinciden, pero deben calcularse desde `encuesta_movilidad$minutos_viaje`.

Si elige mediana como regla:

> La elección puede ser razonable aquí, pero debe justificarse por la distribución y el valor 90, no por una regla automática.

Si interpreta sd como porcentaje:

> La desviación estándar está en las mismas unidades de `minutos_viaje`: minutos.

### 22. Hint 1
Necesitas describir el centro y la dispersión de una variable cuantitativa. Trabajaste dos centros distintos.

### 23. Hint 2
Recupera las funciones utilizadas para media, mediana y desviación estándar.

### 24. Hint 3
```r
mean(encuesta_movilidad$minutos_viaje)

median(encuesta_movilidad$minutos_viaje)

sd(encuesta_movilidad$minutos_viaje)
```

### 25. Predicción
No se agrega una fase independiente. La observación de la distribución y la comparación de centros ya obligan a razonar antes de interpretar.

### 26. Tipo de ejercicio
Checkpoint / transferencia cercana.

### 27. Andamiaje
Bajo. La consigna no nombra `mean()`, `median()` ni `sd()`.

### 28. Carga cognitiva
Media. No hay missing, filtro ni sintaxis nueva; la dificultad se concentra en decidir, producir e interpretar.

### 29. Fading
Es el punto de menor apoyo de M8: solo quedan comentarios semánticos y un histograma funcional opcional.

### 30. Recuperación futura
M9 parte de la capacidad de describir una cuantitativa por separado. M13 exigirá volver a elegir y producir descriptivos dentro de una ruta completa.

### 31. Riesgo de aprendizaje superficial
Memorizar que una diferencia grande media/mediana obliga siempre a usar mediana. El checkpoint debe evaluar justificación contextual.

### 32. Criterio de transferencia
Existe transferencia cuando puede repetir la ruta sobre otra base cuantitativa, con otros valores, sin que se nombren las funciones y sin hardcoding.

### 33. Notas de implementación futura
`hist()` no forma parte del grading sintáctico central.

No incluir missing.

Usar tolerancia numérica.

Perturbation test obligatorio recomendado:

- cambiar 90;
- cambiar un valor central;
- reordenar filas.

El código semántico debe seguir funcionando.


---

# Cierre conceptual de M8 y puente a M9

Después de Checkpoint C mostrar exactamente la necesidad:

> Ya podemos describir una cantidad por separado:
>
> mirar cómo se distribuye,
> resumir dónde está su centro
> y describir qué tan dispersos están sus valores.
>
> Pero muchas preguntas no tratan una sola característica.
>
> Queremos saber, por ejemplo,
> si las personas que estudian más horas
> también presentan valores mayores o menores en otra cantidad.
>
> **¿Cómo estudiamos dos cantidades al mismo tiempo?**

La transición termina ahí.

M8 NO introduce todavía:

- scatterplot;
- `plot(x, y)`;
- pares `(x, y)` como contenido formal;
- correlación;
- `cor()`;
- dirección de asociación;
- fuerza de asociación;
- forma de relación bivariada;
- causalidad.

# Retención esperada después de una semana

## Comprensión
Debe explicar:

> una variable cuantitativa representa cantidades y no se define simplemente porque esté escrita con números.

Debe comprender:

> primero conviene mirar la distribución.

Debe explicar:

```text
media
→ centro que utiliza todos los valores

mediana
→ centro del orden

desviación estándar
→ dispersión alrededor de la media
```

Debe comprender:

- que una media puede no coincidir con un valor observado;
- que valores muy alejados pueden modificar fuertemente la media;
- que la mediana suele ser menos sensible;
- que ninguna medida de centro es automáticamente la mejor en todo contexto;
- que centro y dispersión describen aspectos diferentes;
- que `sd()` conserva las unidades de la variable.

## Producción
Con poca ayuda debe poder producir:

```r
mean(x)
median(x)
sd(x)
```

## Herramienta funcional
Puede requerir recordatorio de:

```r
hist()
```

Eso es aceptable.

## Missing
Debe recuperar la secuencia:

```text
DETECTAR
↓
CONTAR
↓
N DISPONIBLE
↓
DECIDIR
↓
CALCULAR
```

antes de utilizar `na.rm = TRUE` cuando exista missing.

# Auditoría del módulo

## Conteo por rol
- PRÁCTICA / VISUALIZACIÓN FUNCIONAL: 1
- NOVEDAD: 3
- INTEGRACIÓN: 1
- RECUPERACIÓN: 1
- TRANSFERENCIA / CHECKPOINT: 1

## Porcentaje local de gran novedad
3 de 7 ≈ 42.9 %.

No se reclasifica artificialmente M8-E3.

`median()` y el concepto de mediana son realmente nuevos.

El control de novedad se interpreta a nivel de la arquitectura global de 88 ejercicios y, dentro de M8, cada pantalla conserva como máximo una gran unidad de aprendizaje.

## Trayectoria de habilidades

```text
hist()
encuentro funcional M8-E1
→ nivel funcional
```

```text
mean()
encuentro M8-E2
→ integración M8-E4
→ recuperación M8-E6
→ producción M8-E7
→ preparación M9
→ transferencia M13
```

```text
median()
encuentro M8-E3
→ integración M8-E4
→ producción M8-E7
→ preparación M9
→ transferencia M13
```

```text
sd()
encuentro M8-E5
→ recuperación M8-E6
→ producción M8-E7
→ recuperación M9
→ transferencia M13
```

```text
filter()/select()/|>
recuperación M8-E6
```

```text
is.na()/na.rm
recuperación M8-E6
```

## Habilidades nucleares consolidadas relativamente
- variable cuantitativa por significado;
- distribución;
- media;
- mediana;
- comparación de centros;
- elección contextual básica;
- dispersión;
- desviación estándar;
- interpretación en unidades;
- preparación/missing antes de describir.

## Habilidad funcional
- `hist()`.

## Habilidades pospuestas
- cuantiles;
- IQR;
- rango como herramienta formal;
- varianza;
- boxplot;
- fórmula de sd;
- error estándar;
- normalidad;
- outlier rules;
- inferencia;
- asociación bivariada;
- correlación.

## Riesgos de sobrecarga controlados
- E1 usa una variable conocida y entrega `hist()`.
- E2 usa una variable completa sin missing.
- E3 usa N impar.
- E4 no introduce sintaxis nueva.
- E5 crea la necesidad de dispersión antes de `sd()`.
- E6 integra habilidades previas pero omite mediana deliberadamente.
- E7 elimina missing y preparación para concentrarse en dominio cuantitativo.

## Checkpoint
Sí: M8-E7.

Checkpoint C diagnostica principalmente M8.

M7 se recupera únicamente como decisión de entrada:

```text
¿categoría o cantidad?
```

No se vuelve a evaluar toda la ruta categórica.

# Contrato de datos

## `encuesta_social_demo`
M8 preserva exactamente el contrato locked heredado de M7.

No añade nuevas columnas a `encuesta_social_demo`.

## Objetos pedagógicos
Quedan locked:

```r
minutos_lectura <- c(25, 10, 20, 30, 15, 22, 18)

viaje_regular <- c(20, 22, 24, 25, 26, 28, 30)

viaje_extremo <- c(20, 22, 24, 25, 26, 28, 120)

grupo_a <- c(4, 4, 4, 4, 4)

grupo_b <- c(2, 3, 4, 5, 6)
```

## `encuesta_movilidad`
La base de Checkpoint C queda locked pedagógicamente como:

```text
id   transporte   minutos_viaje
1    Metro        25
2    Bus          30
3    Metro        32
4    Bus          28
5    Bicicleta    35
6    Metro        27
7    Bus          31
8    A pie        29
9    Metro        34
10   Bus          90
```

Cualquier implementación futura debe preservar estos valores o actualizar deliberadamente el Markdown locked y todos sus outputs/graders.

# Declaración de lock

M8 queda pedagógicamente cerrado con 7 ejercicios.

- **Sintaxis nuclear introducida:** `mean()`, `median()`, `sd()`.
- **Habilidad funcional introducida:** `hist()`.
- **Conceptos nucleares:** variable cuantitativa por significado, distribución, media, mediana, elección contextual de centro, dispersión y desviación estándar.
- **Recuperación de missing:** M8-E6 con diagnóstico antes de `na.rm = TRUE`.
- **Checkpoint:** M8-E7 con `mean()` + `median()` + `sd()` autónomos sobre una base nueva.
- **Habilidades pospuestas:** cuantiles, IQR, varianza, boxplot, normalidad, error estándar, inferencia y asociación bivariada.
- **Recuperación futura:** M9–M13 utilizan centro/dispersión para conocer variables antes de asociarlas.
- **Puente a M9:** describir una cantidad por separado → estudiar dos cantidades conjuntamente.

# M8 PEDAGOGICALLY LOCKED
