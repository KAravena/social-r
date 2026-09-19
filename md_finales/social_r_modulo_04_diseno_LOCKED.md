# Social R — Módulo 4
## Entender una base de datos

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Comprende vectores como una característica observada en varios casos y puede trabajar con ellos mediante posiciones y condiciones.

### Capacidad después
Comprende cómo varias características de los mismos casos se organizan en filas y columnas, distingue caso/fila y variable/columna, inspecciona una base y puede recuperar una variable mediante `$` como vector.

### Pregunta central
¿Cómo organizamos varias características de los mismos casos y cómo recuperamos una variable de esa base?

### Modelo mental
`UN VECTOR = UNA CARACTERÍSTICA DE VARIOS CASOS → VARIOS VECTORES = VARIAS CARACTERÍSTICAS DE LOS MISMOS CASOS → ALINEAR POR CASO → FILA = CASO → COLUMNA = VARIABLE → DATA FRAME → BASE $ VARIABLE → VECTOR`

### Habilidades nucleares
Al terminar M4, el estudiante debe poder:

- comprender que varias características pueden corresponder a los mismos casos;
- conservar la correspondencia entre posiciones de distintas características;
- comprender fila como información de un caso a través de varias características;
- comprender columna como valores de una variable a través de varios casos;
- utilizar “caso” como término general después del ejemplo concreto de personas;
- utilizar “variable” como término de una característica registrada en una base;
- distinguir en el nivel necesario un objeto de R de una variable dentro de una base;
- reconocer un data frame como una estructura tabular que organiza varias variables para los mismos casos;
- leer una fila;
- leer una columna;
- recuperar una variable mediante `$`;
- comprender que una columna extraída vuelve a ser un vector.

### Habilidades funcionales
`head()` y `str()` son herramientas funcionales secundarias de inspección.

- `head()` permite mirar las primeras filas de una base.
- `str()` permite obtener una radiografía rápida de su estructura y localizar nombres de variables.

No se exige el mismo nivel de autonomía que para `$`.

### Habilidades recuperadas
M4 recupera desde M1–M3:

- objetos;
- `<-`;
- números y texto;
- `c()`;
- vectores;
- orden;
- posición;
- consulta;
- condiciones y selección como conocimientos disponibles, aunque M4 no los combina todavía con `$`.

### Sintaxis nueva
- `head()`;
- `$`;
- `str()`.

### Sintaxis que NO se introduce
No se introducen:

- `data.frame()`;
- `filter()`;
- `select()`;
- `|>`;
- construcción manual de data frames;
- missing;
- funciones descriptivas;
- condiciones múltiples;
- factores;
- listas;
- coerción;
- clases internas;
- clasificación estadística formal mediante códigos de almacenamiento.

### Dataset
M4 utiliza dos niveles de datos:

1. **Microtabla pedagógica E1–E2:** cuatro personas y tres características completamente visibles.
2. **Vista pedagógica contractual de `encuesta_social_demo` para E3–E5:** ocho casos y cinco variables visibles.

Para M4 se fija esta vista:

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

Estos valores constituyen el contrato pedagógico de M4 para outputs y grading. El dataset lock global de M4–M8 sigue siendo una tarea separada del plan maestro; si ese lock futuro modifica estos valores, deberá actualizar deliberadamente este Markdown antes de implementación.

M4-E6 utiliza una base de transferencia distinta:

```text
encuesta_barrio

persona   edad   transporte   minutos_viaje
1         34     Bus          45
2         27     Metro        30
3         41     Bus          50
4         22     Bicicleta    20
```

### Estrategia de scaffolding
1. Partir desde vectores ya conocidos.
2. Alinear varios vectores por persona.
3. Reorganizar visualmente como tabla.
4. Nombrar caso/fila, variable/columna y data frame después de comprender la estructura.
5. Pasar a `encuesta_social_demo` mediante `head()`.
6. Introducir `$` como habilidad nuclear con worked example y producción inmediata.
7. Introducir `str()` como inspección funcional restringida.
8. Transferir a una base nueva.

### Estrategia de fading
`REPRESENTACIÓN ANOTADA → LECTURA CONCEPTUAL → INSPECCIÓN GUIADA → ACCESO GUIADO + PRODUCCIÓN → INSPECCIÓN RESTRINGIDA → TRANSFERENCIA`

### Riesgos cognitivos
- memorizar fila = horizontal y columna = vertical sin comprender su significado;
- perder la correspondencia entre posiciones de diferentes características;
- confundir “objeto de R” con “variable de una base”;
- creer que una fila y una columna son estructuras equivalentes;
- creer que `$edad` devuelve un solo número;
- memorizar `$` como símbolo sin comprender base → variable → vector;
- considerar `head()` o `str()` habilidades nucleares;
- interpretar `num`, `int` o `chr` como clasificación estadística;
- hardcodear una columna en vez de extraerla desde la base;
- no reconocer que una columna extraída vuelve a comportarse como vector.

### Número de ejercicios
6

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M4-E1 | Varias características de las mismas personas | NOVEDAD | varias características alineadas por caso | vectores, orden, posiciones | baja-media |
| M4-E2 | Lee una fila y una columna | PRÁCTICA | ninguna; profundiza caso/variable | modelo de E1 | baja-media |
| M4-E3 | Mira los primeros casos | PRÁCTICA / INSPECCIÓN FUNCIONAL | micro-novedad `head()` | data frame, filas/casos | baja-media |
| M4-E4 | Una variable dentro de la base | NOVEDAD | `$` | columna, variable, vector | baja-media |
| M4-E5 | ¿Qué contiene la base? | RECUPERACIÓN / INSPECCIÓN FUNCIONAL | micro-novedad `str()` | base, variables, `$` conceptualmente | media |
| M4-E6 | Otra encuesta | TRANSFERENCIA | ninguna | caso/variable, `$` | media |

---

## M4-E1 — Varias características de las mismas personas

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Construye el puente entre el mundo conocido de los vectores y una estructura tabular. El estudiante necesita comprender primero por qué varias características de las mismas personas deben mantenerse alineadas antes de aprender nombres como fila, columna, variable o data frame.

### 3. Capacidad antes
Puede comprender un vector como varios valores relacionados y sabe que su orden importa.

### 4. Capacidad después
Comprende que varios vectores pueden representar características distintas de las mismas personas, que sus posiciones deben corresponder y que esa información puede reorganizarse como una tabla.

### 5. Prerrequisitos
- vector;
- orden;
- posición;
- números;
- texto.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** varias características de los mismos casos pueden alinearse.
- **Decisión nueva:** seguir al mismo caso a través de distintas características.

Los términos caso, variable y data frame se nombran solo después de construir la representación.

### 7. Recuperaciones
Recupera `c()`, orden y posiciones desde M2. No exige producir código.

### 8. Contexto sustantivo
Una pequeña encuesta a cuatro estudiantes.

### 9. Dataset / objetos
Vectores conceptuales:

```r
edad <- c(20, 22, 19, 21)
horas_estudio <- c(3, 5, 2, 4)
carrera <- c("Sociología", "Historia", "Antropología", "Sociología")
```

Representación alineada:

```text
persona           1             2             3              4
edad             20            22            19             21
horas_estudio     3             5             2              4
carrera          Sociología    Historia      Antropología    Sociología
```

Representación tabular:

```text
             edad   horas_estudio   carrera
Persona 1      20         3         Sociología
Persona 2      22         5         Historia
Persona 3      19         2         Antropología
Persona 4      21         4         Sociología
```

### 10. Texto para estudiante
Hasta ahora trabajamos con una característica a la vez.

Por ejemplo:

```r
edad <- c(20, 22, 19, 21)
```

Ese vector contiene una edad para cada una de cuatro personas.

También podríamos tener:

```r
horas_estudio <- c(3, 5, 2, 4)
```

y respuestas de carrera.

Lo importante es que **la misma posición entre los vectores corresponde a la misma persona**:

```text
persona           1             2             3              4
edad             20            22            19             21
horas_estudio     3             5             2              4
carrera          Sociología    Historia      Antropología    Sociología
```

Podemos reorganizar esa información así:

```text
             edad   horas_estudio   carrera
Persona 1      20         3         Sociología
Persona 2      22         5         Historia
Persona 3      19         2         Antropología
Persona 4      21         4         Sociología
```

Ahora cada línea reúne varias características de la misma persona.

En esta encuesta cada fila representa una persona. De manera más general, llamamos **caso** a la unidad representada por una fila.

Cada columna reúne una característica para todos los casos. En una base de datos llamamos **variable** a esa característica.

En R, una estructura tabular como esta puede organizarse como un **data frame**.

**Pregunta 1.** La persona que informó 5 horas de estudio, ¿qué edad tiene?

**Pregunta 2.** ¿Por qué sabemos que esa edad y esas horas pertenecen a la misma persona?

### 11. Modelo mental
`VARIOS VECTORES → MISMAS POSICIONES = MISMOS CASOS → TABLA → FILAS/CASOS + COLUMNAS/VARIABLES`

### 12. Representación / código trabajado
La representación central es la transformación visual entre los tres vectores alineados y la microtabla. El código de los vectores se muestra como recordatorio, no como producción.

### 13. Starter code
No hay starter code. Es una actividad conceptual.

### 14. Acción esperada
Responder:

1. `22`;
2. explicar que ambos valores corresponden a la misma persona porque estaban en la misma posición y, al reorganizar la información, quedan en la misma fila.

### 15. Solución canónica
Pregunta 1:

> 22 años.

Pregunta 2:

> Porque los valores de una misma posición correspondían a la misma persona; al organizar los datos como tabla, esas características quedan juntas en la misma fila.

### 16. Resultado esperado
Comprensión explícita de la correspondencia entre características del mismo caso.

### 17. Criterio semántico de éxito
Debe demostrar que:

- identifica correctamente 22;
- relaciona 5 horas y 22 años con la Persona 2;
- justifica la relación mediante misma persona/misma posición/misma fila;
- no se limita a decir que “están cerca” visualmente.

### 18. Estrategias alternativas válidas
Son válidas formulaciones equivalentes como:

- “están en la misma fila”;
- “eran la segunda posición de ambos vectores”;
- “pertenecen al mismo caso”.

La respuesta debe expresar correspondencia, no orientación visual solamente.

### 19. Error esperado / misconception
- combinar datos de personas distintas;
- decir “porque están en la misma columna”;
- memorizar fila como horizontal sin relacionarla con un caso;
- creer que reorganizar la tabla cambia qué valores pertenecen a cada persona.

### 20. Feedback correcto
**Bien.** Seguiste a la misma persona a través de distintas características. Una fila mantiene juntas las características de un mismo caso.

### 21. Feedback resultado correcto / estrategia incorrecta
Si responde 22 pero justifica solo por proximidad visual:

> La edad es correcta. Ahora falta la idea importante: ambos valores pertenecen a la misma persona porque correspondían a la misma posición y quedan juntos en una misma fila.

### 22. Hint 1
Sigue a una sola persona a través de las distintas características.

### 23. Hint 2
Los valores que estaban en la misma posición pertenecen al mismo caso y quedan en la misma fila.

### 24. Hint 3
La persona con 5 horas de estudio está en la segunda fila; en esa misma fila la edad es 22.

### 25. Predicción
No necesaria.

### 26. Tipo de ejercicio
Interpretación conceptual con representación múltiple.

### 27. Andamiaje
Muy alto: representaciones alineadas, tabla completa y vocabulario introducido después de la comprensión.

### 28. Carga cognitiva
**Baja-media.** No hay sintaxis nueva, pero el estudiante reorganiza mentalmente varios vectores en una estructura bidimensional y aprende vocabulario conceptual.

### 29. Fading
E1 mantiene todas las anotaciones. E2 usará la tabla sin la explicación paso a paso y exigirá distinguir fila/caso y columna/variable.

### 30. Recuperación futura
E2 consolida el modelo; E4 conecta variable/columna con `$`; M5–M13 usarán caso y variable como infraestructura.

### 31. Riesgo de aprendizaje superficial
Memorizar pares terminológicos sin comprender alineación por caso. Las dos preguntas conceptuales deben evaluar correspondencia, no solo vocabulario.

### 32. Criterio de transferencia
Debe poder reconocer más adelante que, en otra base, valores de una misma fila pertenecen al mismo caso aunque cambien nombres y características.

### 33. Notas de implementación futura
La interfaz debería mantener visibles ambas representaciones o permitir alternarlas sin scroll largo. No evaluar esta pantalla mediante código. No enseñar `data.frame()`.

---

## M4-E2 — Lee una fila y una columna

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Convierte el modelo construido en E1 en lectura activa. Obliga a distinguir dos formas diferentes de recorrer una base: seguir un caso a través de varias características o seguir una variable a través de varios casos.

### 3. Capacidad antes
Comprende que varias características de los mismos casos pueden organizarse en filas y columnas.

### 4. Capacidad después
Puede leer una fila como un caso con varias características y una columna como una variable con valores para varios casos.

### 5. Prerrequisitos
- modelo de E1;
- caso;
- variable;
- fila;
- columna;
- vector.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno grande; profundiza caso/fila y variable/columna.
- **Decisión nueva:** reconocer si una pregunta exige mantener fijo el caso o la característica.

### 7. Recuperaciones
Recupera la microtabla y el concepto de vector al leer una columna completa.

### 8. Contexto sustantivo
La misma microencuesta de cuatro personas.

### 9. Dataset / objetos
```text
             edad   horas_estudio   carrera
Persona 1      20         3         Sociología
Persona 2      22         5         Historia
Persona 3      19         2         Antropología
Persona 4      21         4         Sociología
```

### 10. Texto para estudiante
Hay dos maneras importantes de leer una base.

Si recorres una **fila**, mantienes el mismo caso y observas sus distintas características.

Si recorres una **columna**, mantienes la misma característica y observas sus valores para distintos casos.

Observa:

```text
             edad   horas_estudio   carrera
Persona 1      20         3         Sociología
Persona 2      22         5         Historia
Persona 3      19         2         Antropología
Persona 4      21         4         Sociología
```

**Pregunta 1.** ¿Qué sabemos de la Persona 3?

**Pregunta 2.** ¿Qué edades aparecen en la encuesta?

Hasta ahora hemos hablado principalmente de **objetos de R**: nombres que guardan información.

Dentro de una base de datos usamos además la palabra **variable** para referirnos a una característica registrada como columna.

Una variable de una base puede extraerse más adelante y volver a aparecer como un vector.

### 11. Modelo mental
`FILA → MISMO CASO, VARIAS CARACTERÍSTICAS`

`COLUMNA → MISMA VARIABLE, VARIOS CASOS`

### 12. Representación / código trabajado
Solo la microtabla. No se introduce código.

### 13. Starter code
No hay starter code.

### 14. Acción esperada
Pregunta 1:

- edad 19;
- horas_estudio 2;
- carrera Antropología.

Pregunta 2:

- 20, 22, 19, 21.

### 15. Solución canónica
Pregunta 1:

> La Persona 3 tiene 19 años, estudia 2 horas y respondió Antropología.

Pregunta 2:

> 20, 22, 19 y 21.

### 16. Resultado esperado
Lectura correcta de una fila completa y de una columna completa.

### 17. Criterio semántico de éxito
Comprobar por separado:

- lectura de fila: reúne correctamente las tres características de Persona 3;
- lectura de columna: recupera solo los cuatro valores de edad;
- comprende que la fila mantiene fijo el caso;
- comprende que la columna mantiene fija la variable.

### 18. Estrategias alternativas válidas
No se exige una redacción literal. Se aceptan listas o frases equivalentes, siempre que no mezcle casos o variables.

### 19. Error esperado / misconception
- leer una columna cuando se pregunta por una persona;
- mezclar valores de dos filas;
- definir fila únicamente como “horizontal”;
- llamar variable a cualquier objeto sin distinguir contexto de base de datos;
- creer que fila y columna son intercambiables.

### 20. Feedback correcto
**Bien.** Para describir a una persona seguiste una fila; para recuperar todas las edades seguiste una columna. Eso distingue caso y variable.

### 21. Feedback resultado correcto / estrategia incorrecta
Si identifica correctamente los datos pero explica solo “horizontal/vertical”:

> La orientación visual ayuda, pero necesitamos el significado: una fila mantiene el mismo caso; una columna mantiene la misma variable.

### 22. Hint 1
Pregunta si la consigna mantiene fija a la persona o a la característica.

### 23. Hint 2
Una fila mantiene fijo el caso; una columna mantiene fija la variable.

### 24. Hint 3
Para Persona 3 lee toda la tercera fila. Para edades lee completa la columna `edad`.

### 25. Predicción
No necesaria.

### 26. Tipo de ejercicio
Clasificación/lectura conceptual.

### 27. Andamiaje
Alto: tabla completamente visible y preguntas concretas.

### 28. Carga cognitiva
**Baja-media.** No hay sintaxis nueva. La dificultad consiste en estabilizar cuatro términos relacionados y asociarlos a dos formas de lectura con significado.

### 29. Fading
Se retira la representación previa de vectores alineados. El estudiante trabaja directamente con la tabla.

### 30. Recuperación futura
E4 recuperará columna/variable; E6 exigirá identificar ambos conceptos en una base nueva; M5 los usa para filtrar casos y seleccionar variables.

### 31. Riesgo de aprendizaje superficial
Responder preguntas puntuales sin haber construido el contraste caso-variable. El grading debe mantener separados ambos componentes.

### 32. Criterio de transferencia
Debe poder leer después una fila y una columna de una base distinta con otras características.

### 33. Notas de implementación futura
No convertir “celda” en objetivo nuclear. Puede usarse en explicaciones puntuales, pero el foco evaluado es fila/caso y columna/variable.

---

## M4-E3 — Mira los primeros casos

### 1. Rol pedagógico
PRÁCTICA / INSPECCIÓN FUNCIONAL.

### 2. Por qué existe
Marca el paso desde una microtabla pedagógica completamente visible hacia una base real del curso. Introduce `head()` únicamente como solución a una necesidad auténtica: mirar una parte inicial sin imprimir toda la base.

### 3. Capacidad antes
Puede interpretar filas/casos y columnas/variables en una tabla pequeña.

### 4. Capacidad después
Puede ejecutar `head()` para obtener un vistazo inicial de una base y comprende que ese resultado representa solo las primeras filas.

### 5. Prerrequisitos
- objeto;
- data frame;
- fila/caso;
- columna/variable;
- ejecución de funciones con paréntesis.

### 6. Gran novedad
- **Sintaxis funcional nueva:** `head()`.
- **Concepto nuevo:** inspección parcial de una base.
- **Decisión nueva:** ninguna.

`head()` es una micro-novedad funcional, no una gran habilidad curricular.

### 7. Recuperaciones
Recupera función con paréntesis y el modelo de data frame.

### 8. Contexto sustantivo
Primera inspección de `encuesta_social_demo`.

### 9. Dataset / objetos
Vista contractual para M4:

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

### 10. Texto para estudiante
Hasta ahora usamos una tabla pequeña porque podíamos verla completa.

A partir de ahora trabajaremos con una base llamada:

```r
encuesta_social_demo
```

Esta vista pedagógica contiene ocho casos, pero una base real puede tener muchas más filas.

Para empezar a conocerla no siempre necesitamos mostrarla completa.

Podemos ejecutar:

```r
head(encuesta_social_demo)
```

`head()` muestra las primeras filas de la base.

Antes de ejecutar, piensa:

> ¿esperas ver toda la base o solo una parte?

Ejecuta y observa.

### 11. Modelo mental
`BASE COMPLETA → head(base) → PRIMERAS FILAS / PRIMEROS CASOS`

### 12. Representación / código trabajado
```r
head(encuesta_social_demo)
```

### 13. Starter code
```r
head(encuesta_social_demo)
```

### 14. Acción esperada
Ejecutar `head(encuesta_social_demo)` y reconocer que se observan solo las primeras filas.

### 15. Solución canónica
```r
head(encuesta_social_demo)
```

### 16. Resultado esperado
Con la vista contractual de M4, las seis primeras filas:

```text
id   edad   carrera          horas_estudio   trabaja
1    20     Sociología       3                No
2    22     Historia         5                Sí
3    19     Antropología     2                No
4    21     Sociología       4                No
5    24     Trabajo Social   6                Sí
6    23     Antropología     3                Sí
```

El formato exacto de impresión puede variar; semánticamente deben ser las primeras seis filas.

### 17. Criterio semántico de éxito
Comprobar que:

- se usa `head()` sobre `encuesta_social_demo`;
- el resultado contiene las primeras filas de esa base;
- el estudiante identifica el output como vista parcial;
- no concluye que la base completa tiene seis casos.

### 18. Estrategias alternativas válidas
Para esta actividad funcional, `head(encuesta_social_demo)` es la construcción objetivo. No se exige una redacción exacta de la explicación.

### 19. Error esperado / misconception
- creer que `head()` modifica la base;
- creer que crea otra base nueva;
- creer que la base tiene solo las filas mostradas;
- memorizar `head()` sin comprender el propósito.

### 20. Feedback correcto
**Bien.** `head()` te dio un vistazo a los primeros casos sin necesitar mostrar toda la base.

### 21. Feedback resultado correcto / estrategia incorrecta
Si imprime el objeto completo y después responde mirando las primeras filas:

> Pudiste observar los datos, pero la herramienta de esta pantalla es `head()`: permite pedir directamente un vistazo inicial sin imprimir toda la base.

### 22. Hint 1
Necesitas mirar el comienzo de la base, no modificarla.

### 23. Hint 2
`head()` recibe dentro de los paréntesis el objeto que quieres inspeccionar.

### 24. Hint 3
```r
head(encuesta_social_demo)
```

### 25. Predicción
Opcional pero recomendada:

> ¿verás toda la base o solo una parte?

### 26. Tipo de ejercicio
Ejecución/observación funcional.

### 27. Andamiaje
Muy alto: función entregada completa y propósito explícito.

### 28. Carga cognitiva
**Baja-media.** Aparece una función nueva, pero con propósito simple y sin decisiones analíticas.

### 29. Fading
No se exige producir `head()` de memoria. E4 cambiará el foco hacia la habilidad nuclear `$`.

### 30. Recuperación futura
`head()` reaparece funcionalmente en M13. La idea de inspeccionar una base continúa en todo el curso.

### 31. Riesgo de aprendizaje superficial
Convertir `head()` en comando ritual al abrir cualquier objeto. El texto debe mantener visible el problema que resuelve: obtener una vista inicial.

### 32. Criterio de transferencia
Más adelante debe reconocer para qué sirve `head()` aunque pueda necesitar una pista para recordar su nombre.

### 33. Notas de implementación futura
La salida puede depender de cómo se imprima el data frame en webR. Evaluar filas/contenido, no texto de consola literal.

---

## M4-E4 — Una variable dentro de la base

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Introduce la habilidad sintáctica nuclear de M4: recuperar por nombre una variable/columna que vive dentro de una base. Conecta directamente el data frame con el concepto conocido de vector.

### 3. Capacidad antes
Comprende caso/fila y variable/columna y puede inspeccionar las primeras filas de una base.

### 4. Capacidad después
Puede leer y producir `base$variable`, comprender que recupera la columna completa y reconocer que el resultado vuelve a ser un vector.

### 5. Prerrequisitos
- objeto;
- data frame;
- variable/columna;
- vector;
- nombres exactos;
- consulta.

### 6. Gran novedad
- **Sintaxis nueva:** `$`.
- **Concepto nuevo:** una variable nombrada puede extraerse de una base.
- **Decisión nueva:** mínima en el worked example; producción guiada inmediata después.

### 7. Recuperaciones
Recupera columna/variable de E1–E2 y vector de M2.

### 8. Contexto sustantivo
Extraer variables de `encuesta_social_demo`.

### 9. Dataset / objetos
Objeto:

`encuesta_social_demo`

Variables relevantes:

- `edad`;
- `horas_estudio`.

Valores contractuales:

```text
edad:
20 22 19 21 24 23 20 25

horas_estudio:
3 5 2 4 6 3 5 2
```

### 10. Texto para estudiante
Ya sabemos que una columna representa una variable.

Ahora queremos recuperar una columna desde la base.

Observa:

```r
encuesta_social_demo$edad
```

Puedes leerlo como:

> dentro de `encuesta_social_demo`, quiero la variable `edad`.

La estructura es:

```text
encuesta_social_demo $ edad
          │             │
          │             └─ variable que quiero
          └─────────────── base donde está
```

Antes de ejecutar:

> ¿qué esperas obtener: una fila, una columna completa o un solo número?

Ejecuta.

El resultado es la columna completa `edad`.

Y una idea importante:

> cuando extraemos una columna de esta manera, volvemos a obtener un **vector**.

Compara:

```text
x[3]
→ una posición dentro de un vector

base$edad
→ una variable nombrada dentro de una base
```

Ahora te toca.

**Tarea.** Extrae `horas_estudio` desde `encuesta_social_demo`.

### 11. Modelo mental
`BASE $ VARIABLE → COLUMNA → VECTOR`

### 12. Representación / código trabajado
Worked example:

```r
encuesta_social_demo$edad
```

Output conceptual:

```text
20 22 19 21 24 23 20 25
```

### 13. Starter code
```r
# extrae horas_estudio desde encuesta_social_demo
```

### 14. Acción esperada
Producir una expresión con `$` que recupere la variable `horas_estudio`.

### 15. Solución canónica
```r
encuesta_social_demo$horas_estudio
```

### 16. Resultado esperado
```text
3 5 2 4 6 3 5 2
```

### 17. Criterio semántico de éxito
Comprobar que:

- se accede a `horas_estudio` desde `encuesta_social_demo`;
- se utiliza `$`;
- el resultado contiene los ocho valores de la columna en el orden correcto;
- el resultado depende de la base;
- no se reconstruye manualmente el vector.

**Perturbation test útil:** modificar internamente uno de los valores de la columna y verificar que la misma expresión devuelve el valor actualizado.

### 18. Estrategias alternativas válidas
Para este encuentro, la estrategia objetivo es explícitamente `$`. Otras formas de extracción de columnas no cuentan como equivalentes pedagógicos aunque produzcan el mismo resultado, porque `$` es la habilidad nuclear a aprender.

### 19. Error esperado / misconception
- escribir manualmente `c(3, 5, 2, 4, 6, 3, 5, 2)`;
- creer que `$horas_estudio` devuelve un solo caso;
- usar un nombre inexistente;
- confundir `base$variable` con posición;
- escribir solo `horas_estudio` como si fuese un objeto independiente ya creado.

### 20. Feedback correcto
**Bien.** Pediste una variable por su nombre dentro de la base. El resultado es la columna completa y vuelve a ser un vector.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea el vector:

> Los valores coinciden, pero los escribiste manualmente. Queremos recuperarlos desde `encuesta_social_demo` para que el código siga funcionando si cambian los datos.

Si devuelve un solo valor:

> `$horas_estudio` recupera la columna completa, no la respuesta de una sola persona.

Si usa nombre incorrecto:

> Después de `$` debe ir el nombre exacto de una variable que exista dentro de `encuesta_social_demo`.

### 22. Hint 1
¿En qué base está guardada la variable que necesitas?

### 23. Hint 2
`$` conecta el nombre de la base con el nombre de la variable.

### 24. Hint 3
```r
encuesta_social_demo$horas_estudio
```

### 25. Predicción
Sí.

Antes del worked example:

> ¿`encuesta_social_demo$edad` devolverá una fila, una columna completa o un solo número?

### 26. Tipo de ejercicio
Worked example + producción inmediata.

### 27. Andamiaje
Alto: significado de `$` completamente anotado; luego producción con otra variable.

### 28. Carga cognitiva
**Baja-media.** Hay una nueva construcción sintáctica importante, pero el concepto de columna ya fue construido y no se combina todavía con condiciones.

### 29. Fading
Worked example con `edad` → producción con `horas_estudio`. M5-E1 recuperará `$` sin reenseñarlo desde cero y lo combinará con una condición.

### 30. Recuperación futura
M5-E1 práctica `$`; M5-E4 producción; M6–M12 recuperación; M13 transferencia.

### 31. Riesgo de aprendizaje superficial
Memorizar `$` como separador visual. La lectura verbal “dentro de esta base quiero esta variable” y la conexión columna → vector son obligatorias.

### 32. Criterio de transferencia
Debe poder producir `otra_base$otra_variable` en E6 sin que la consigna vuelva a explicar el símbolo.

### 33. Notas de implementación futura
No combinar todavía `$` con `>`, `==`, filtrado o selección de filas. El objetivo es aislar acceso a variable. El grader debe validar dependencia de la base y estrategia `$`.

---

## M4-E5 — ¿Qué contiene la base?

### 1. Rol pedagógico
RECUPERACIÓN / INSPECCIÓN FUNCIONAL.

### 2. Por qué existe
Introduce una herramienta funcional de inspección sin desplazar el foco conceptual. Permite obtener una radiografía rápida de la organización del objeto y localizar nombres de variables, recuperando al mismo tiempo el modelo caso-variable.

### 3. Capacidad antes
Comprende la organización básica de una base y puede extraer una variable mediante `$`.

### 4. Capacidad después
Puede ejecutar `str()` con apoyo y localizar variables dentro de su salida sin confundir códigos de almacenamiento con tipos estadísticos.

### 5. Prerrequisitos
- data frame;
- variable/columna;
- nombres de variables;
- ejecución de funciones.

### 6. Gran novedad
- **Sintaxis funcional nueva:** `str()`.
- **Concepto nuevo:** una función puede describir la estructura general de un objeto.
- **Decisión nueva:** leer selectivamente la salida.

`str()` es una micro-novedad funcional. La gran capacidad curricular sigue siendo comprender la base y acceder a variables.

### 7. Recuperaciones
Recupera:

- data frame;
- variables/columnas;
- nombres `edad`, `carrera`, `horas_estudio`, `trabaja`;
- la idea de inspeccionar antes de analizar.

### 8. Contexto sustantivo
Inspección de `encuesta_social_demo`.

### 9. Dataset / objetos
Misma vista contractual de ocho casos y cinco variables.

Objeto:

`encuesta_social_demo`

### 10. Texto para estudiante
Ya puedes mirar las primeras filas y extraer una variable.

Otra pregunta útil al recibir una base es:

> ¿cómo está organizada?

R puede mostrar una descripción rápida con:

```r
str(encuesta_social_demo)
```

No necesitas comprender todo lo que aparece.

Por ahora fíjate solo en:

1. que el objeto contiene varias variables;
2. los nombres de esas variables;
3. que R muestra además información técnica sobre cómo almacena sus valores.

Puedes ver abreviaciones como `int`, `num` o `chr`.

**No necesitas memorizarlas en este módulo.**

Y, sobre todo:

> esos códigos describen cómo R almacena valores; no equivalen automáticamente a clasificar una variable como cuantitativa o categórica.

Esa clasificación se trabajará después a partir de lo que la variable representa.

Ejecuta:

```r
str(encuesta_social_demo)
```

Después responde:

- ¿aparece una variable llamada `edad`?
- ¿aparece una variable llamada `carrera`?
- ¿aparece una variable llamada `horas_estudio`?

### 11. Modelo mental
`BASE → str(base) → RADIOGRAFÍA RÁPIDA → LOCALIZAR VARIABLES`

### 12. Representación / código trabajado
```r
str(encuesta_social_demo)
```

No se reproduce ni se exige memorizar un output literal de `str()` porque puede variar en detalles de impresión según la estructura concreta y versión de R. El material implementado debe destacar visualmente los nombres de las columnas.

### 13. Starter code
```r
str(encuesta_social_demo)
```

### 14. Acción esperada
Ejecutar `str()` y localizar `edad`, `carrera` y `horas_estudio` en la descripción.

### 15. Solución canónica
```r
str(encuesta_social_demo)
```

Respuestas conceptuales:

- `edad`: sí;
- `carrera`: sí;
- `horas_estudio`: sí.

### 16. Resultado esperado
Una descripción estructural del objeto que incluye las variables:

- `id`;
- `edad`;
- `carrera`;
- `horas_estudio`;
- `trabaja`.

No se evalúa la interpretación de códigos de almacenamiento.

### 17. Criterio semántico de éxito
Comprobar que:

- `str()` se ejecuta sobre `encuesta_social_demo`;
- el estudiante localiza correctamente los nombres pedidos;
- no necesita interpretar ni clasificar `int`, `num`, `chr`;
- si se le pregunta, distingue “cómo R almacena” de “qué significa estadísticamente la variable”.

### 18. Estrategias alternativas válidas
La actividad funcional pretende reconocer `str()`. Para las preguntas sobre presencia de variables, otras inspecciones podrían producir la misma información, pero no sustituyen el encuentro con `str()` en esta pantalla.

### 19. Error esperado / misconception
- afirmar `chr = categórica`;
- afirmar `num/int = cuantitativa` como regla general;
- intentar memorizar toda la salida;
- creer que `str()` modifica la base;
- creer que el objetivo es calcular algo.

### 20. Feedback correcto
**Bien.** Usaste `str()` como una vista rápida de la estructura y localizaste las variables de la base sin convertir los códigos técnicos de almacenamiento en tipos estadísticos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si identifica las variables pero afirma equivalencias estadísticas desde los códigos:

> Localizaste correctamente las variables. Corrige solo una idea: `chr`, `num` o `int` describen almacenamiento en R; todavía no estamos clasificando estadísticamente las variables.

### 22. Hint 1
Busca los nombres de las columnas dentro de la salida.

### 23. Hint 2
No necesitas interpretar las abreviaciones técnicas para responder.

### 24. Hint 3
Ejecuta:

```r
str(encuesta_social_demo)
```

y busca `edad`, `carrera` y `horas_estudio`.

### 25. Predicción
No necesaria.

### 26. Tipo de ejercicio
Inspección funcional guiada.

### 27. Andamiaje
Alto: función completa, contrato explícito sobre qué leer y qué ignorar.

### 28. Carga cognitiva
**Media.** El output de `str()` contiene información extraña para principiantes; la carga se controla restringiendo explícitamente los elementos relevantes.

### 29. Fading
No exige producción autónoma de `str()`. E6 cambia de base y concentra la transferencia en estructura + `$`.

### 30. Recuperación futura
`str()` reaparece funcionalmente en M13. La distinción entre almacenamiento y significado estadístico protege M7–M8.

### 31. Riesgo de aprendizaje superficial
Convertir abreviaciones técnicas en etiquetas estadísticas. Esta pantalla debe incluir obligatoriamente la advertencia que separa ambos planos.

### 32. Criterio de transferencia
Más adelante debe reconocer que `str()` sirve para obtener una descripción rápida de otro objeto, aunque pueda requerir ayuda para recordar el nombre de la función.

### 33. Notas de implementación futura
No evaluar `int`, `num`, `chr`, clase, atributos ni factores. Si el output de webR difiere visualmente, el grader debe usar propiedades estructurales/nombres, no texto literal.

---

## M4-E6 — Otra encuesta

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
Comprueba si el estudiante puede trasladar el modelo caso-variable y la sintaxis `$` a una base nueva, con nombres y valores diferentes, sin convertir la tarea en una repetición literal de `encuesta_social_demo`.

### 3. Capacidad antes
Comprende caso/fila, variable/columna, data frame, inspección funcional y acceso a una variable mediante `$`.

### 4. Capacidad después
Puede interpretar una base pequeña nueva y recuperar una variable por su nombre mediante `$`, explicando qué representa el resultado.

### 5. Prerrequisitos
- fila/caso;
- columna/variable;
- data frame;
- `$`;
- vector.

`head()` y `str()` no son requisitos para aprobar esta transferencia.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** ninguno.
- **Decisión nueva:** reconocer la estructura en un contexto diferente y elegir `$` para recuperar una variable.

### 7. Recuperaciones
Recupera todos los conceptos nucleares de M4 y `$`.

### 8. Contexto sustantivo
Encuesta de movilidad barrial.

### 9. Dataset / objetos
Objeto ya disponible:

`encuesta_barrio`

```text
persona   edad   transporte   minutos_viaje
1         34     Bus          45
2         27     Metro        30
3         41     Bus          50
4         22     Bicicleta    20
```

### 10. Texto para estudiante
Ahora cambia la base.

Dispones de:

```text
encuesta_barrio

persona   edad   transporte   minutos_viaje
1         34     Bus          45
2         27     Metro        30
3         41     Bus          50
4         22     Bicicleta    20
```

**Pregunta 1.** ¿Qué representa una fila de esta base?

**Pregunta 2.** ¿Qué representa la columna `transporte`?

**Pregunta 3.** Escribe código para recuperar todos los valores de `minutos_viaje`.

No necesitas usar `head()` ni `str()` para aprobar. Decide a partir de la estructura que ya conoces.

### 11. Modelo mental
`BASE NUEVA → MISMA ESTRUCTURA CASO/VARIABLE → BASE $ VARIABLE → VECTOR`

### 12. Representación / código trabajado
No hay worked example con `encuesta_barrio`. El cambio de contexto es parte de la transferencia.

### 13. Starter code
```r
# recupera la variable minutos_viaje desde encuesta_barrio
```

### 14. Acción esperada
Responder:

1. una fila representa una persona/caso con sus distintas características;
2. `transporte` es una variable/característica observada para todos los casos;
3. producir `encuesta_barrio$minutos_viaje`.

### 15. Solución canónica
Respuestas conceptuales:

> Una fila reúne las características de una persona/caso.

> La columna `transporte` es una variable que contiene el medio de transporte de cada caso.

Código:

```r
encuesta_barrio$minutos_viaje
```

### 16. Resultado esperado
```text
45 30 50 20
```

### 17. Criterio semántico de éxito
Comprobar dos componentes.

**Conceptual**
- interpreta fila como caso;
- interpreta columna `transporte` como variable.

**Código**
- utiliza `$` sobre `encuesta_barrio`;
- solicita `minutos_viaje`;
- obtiene `45 30 50 20`;
- no reconstruye manualmente el vector.

**Perturbation test recomendado:** modificar los valores de `minutos_viaje` y verificar que la misma expresión devuelve la columna actualizada.

### 18. Estrategias alternativas válidas
Las respuestas conceptuales pueden redactarse de diferentes maneras. En código, `$` es la estrategia objetivo porque M4 está consolidando esa construcción; otras formas de extracción no sustituyen el criterio pedagógico.

### 19. Error esperado / misconception
- definir fila solo como horizontal;
- decir que `transporte` representa un caso;
- escribir `c(45, 30, 50, 20)`;
- intentar acceder a `encuesta_social_demo`;
- usar un nombre de columna inexistente;
- creer que `encuesta_barrio$minutos_viaje` devuelve un solo valor.

### 20. Feedback correcto
**Bien.** La base cambió, pero la organización es la misma: cada fila representa un caso, cada columna una variable, y pudiste recuperar una variable nueva por su nombre.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea:

> Los valores coinciden, pero los escribiste manualmente. Recupera la variable desde `encuesta_barrio` para que el código dependa de la base.

Si confunde fila/columna:

> Si sigues una persona a través de varias características estás leyendo una fila. Si sigues una característica a través de varios casos estás leyendo una columna.

### 22. Hint 1
Decide primero si cada pregunta se refiere a un caso o a una variable.

### 23. Hint 2
Para recuperar una variable necesitas el nombre de la base y el nombre de la columna.

### 24. Hint 3
```r
encuesta_barrio$minutos_viaje
```

### 25. Predicción
No necesaria.

### 26. Tipo de ejercicio
Transferencia conceptual + código.

### 27. Andamiaje
Medio-bajo: la base y las preguntas están visibles, pero no se vuelve a explicar `$`.

### 28. Carga cognitiva
**Media.** Integra varios conceptos y exige cambiar de contexto, pero no añade sintaxis ni operaciones nuevas.

### 29. Fading
Es el punto final del módulo: desaparecen las anotaciones de `$`, cambia la base y la tarea combina interpretación con producción.

### 30. Recuperación futura
M5–M13 utilizarán `$` y la idea caso/variable como infraestructura. M5-E1 recupera inmediatamente acceso a columna + condición.

### 31. Riesgo de aprendizaje superficial
Resolver solo por parecido superficial con E4. El componente conceptual obliga a demostrar que el estudiante reconoce la estructura, no solo la secuencia de símbolos.

### 32. Criterio de transferencia
Demuestra transferencia si puede interpretar otra base y producir `otra_base$otra_variable` sin que la consigna nombre explícitamente `$`.

### 33. Notas de implementación futura
`encuesta_barrio` debe existir en el entorno con exactamente los cuatro casos descritos para que el grader sea determinista. No introducir `filter()`, `select()` ni pipe.

---

# Cierre conceptual de M4 y puente a M5

Después de completar E6:

> Ahora sabemos cómo está organizada una base:
>
> cada fila representa un caso,
> cada columna representa una variable,
> y podemos recuperar una variable con `$`.
>
> Pero muchas veces no queremos trabajar con toda la base.
>
> ¿Qué hacemos si queremos quedarnos solo con algunas personas
> o solo con algunas variables?

La transición termina ahí.

M4 NO debe mostrar todavía:

```r
filter()
select()
|>
```

# Retención esperada después de una semana

## Comprensión
El estudiante debería poder explicar:

```text
fila → caso
columna → variable
```

en sentido conceptual y no meramente espacial.

## Reconocimiento
Debe reconocer un data frame como una estructura que organiza varias variables para los mismos casos.

## Producción
Con poca ayuda debería poder producir:

```r
base$variable
```

y comprender que obtiene la columna completa como vector.

## Habilidades funcionales
Puede requerir recordatorio del nombre de:

```r
head()
str()
```

No se espera el mismo nivel de autonomía que para `$`.

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 2
- PRÁCTICA: 1
- PRÁCTICA / INSPECCIÓN FUNCIONAL: 1
- RECUPERACIÓN / INSPECCIÓN FUNCIONAL: 1
- TRANSFERENCIA: 1

## Porcentaje de gran novedad
2 de 6 ejercicios: 33,3 %.

Las apariciones de `head()` y `str()` se consideran micro-novedades funcionales, no grandes novedades curriculares.

## Habilidades nucleares consolidadas en el nivel esperado
- correspondencia entre características del mismo caso;
- fila/caso;
- columna/variable;
- data frame;
- `$` en producción inicial;
- columna extraída como vector.

## Habilidades funcionales
- `head()`;
- `str()`.

## Recuperación futura
- `$`: M5-E1 práctica, M5-E4 producción, M6–M12 recuperación, M13 transferencia.
- `head()` y `str()`: recuperación funcional posterior, especialmente M13.
- caso/variable: infraestructura desde M5 hasta M13.

## Riesgos de sobrecarga controlados
- vocabulario aparece después de la representación;
- `head()` no se convierte en objetivo nuclear;
- `$` se introduce sin condición adicional;
- `str()` tiene contrato explícito de lectura restringida;
- E6 no exige `head()` ni `str()`.

## Checkpoint
No.

# Contrato de datos pendiente

El plan maestro mantiene pendiente un dataset lock global para `encuesta_social_demo`.

M4 fija únicamente una vista pedagógica contractual de ocho casos para que sus outputs y futuros graders sean deterministas.

Antes de implementar conjuntamente M4–M8 debe existir una decisión explícita:

- preservar estos valores dentro del dataset lock global; o
- actualizar deliberadamente este Markdown y sus outputs.

Esto no bloquea el diseño pedagógico de M4, pero sí debe resolverse antes de implementación final de los datasets compartidos.

# Declaración de lock

M4 queda pedagógicamente cerrado con 6 ejercicios.

- **Sintaxis introducida:** `head()`, `$`, `str()`.
- **Habilidad sintáctica nuclear:** `$`.
- **Habilidades funcionales:** `head()`, `str()`.
- **Conceptos nucleares:** varias características alineadas, caso/fila, variable/columna, data frame, columna como vector.
- **Sintaxis deliberadamente excluida:** `data.frame()`, `filter()`, `select()`, `|>`.
- **Recuperación futura:** M5–M13.
- **Puente a M5:** comprender una base → necesidad de quedarse con algunos casos o algunas variables.

# M4 PEDAGOGICALLY LOCKED
