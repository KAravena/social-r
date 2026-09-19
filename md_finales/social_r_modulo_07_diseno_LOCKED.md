# Social R — Módulo 7
## Describir categorías

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede preparar una variable, revisar si contiene datos ausentes y decidir trabajar con los valores disponibles, pero todavía no decide cómo describirla según lo que representan sus valores.

### Capacidad después
Puede reconocer cuándo una variable representa categorías, obtener frecuencias y proporciones, distinguir frecuencia, proporción y porcentaje e interpretar una distribución categórica.

### Pregunta central
¿Cómo describo una variable cuyos valores representan categorías?

### Modelo mental
`¿QUÉ REPRESENTAN LOS VALORES? → CATEGORÍAS → CONTAR CASOS → FRECUENCIAS → COMPARAR CON EL TOTAL → PROPORCIONES → INTERPRETAR → VISUALIZAR COMO APOYO → TRANSFERIR`

### Principio conceptual central
Una variable es categórica por **lo que representan sus valores**, no por la apariencia de esos valores ni por la forma técnica en que R los almacena.

La pregunta nuclear del módulo es:

> ¿Qué representan estos valores para los casos?

No:

> ¿Son números o texto?

### Definición operativa de variable categórica
Una variable es **categórica** cuando sus valores indican a qué categoría, grupo o tipo pertenece cada caso.

M7 formaliza el concepto **variable categórica**. Para contrastarlo utiliza la expresión “variable cuyos valores representan una cantidad”. La formalización de la ruta cuantitativa se deja para M8.

### Habilidades nucleares
Al terminar M7, el estudiante debe poder:

- reconocer una variable categórica por el significado de sus valores;
- explicar por qué una variable numéricamente codificada puede seguir siendo categórica;
- evitar identificar automáticamente texto con categórica y número con cantidad;
- obtener frecuencias mediante `table()`;
- interpretar frecuencia como número de casos en una categoría;
- reutilizar una tabla de frecuencias guardada en un objeto;
- obtener proporciones mediante `prop.table()`;
- interpretar una proporción respecto de un total de referencia;
- distinguir frecuencia, proporción y porcentaje;
- explicar que `0.375` es una proporción y que `37.5 %` expresa esa misma relación sobre 100;
- reconocer que las frecuencias del conjunto suman el número total de casos;
- reconocer que las proporciones del conjunto completo suman 1;
- producir autónomamente `table()` y `prop.table()` en una variable categórica nueva;
- interpretar sustantivamente cuál categoría aparece más y qué parte del total representa.

### Habilidad funcional
`barplot()` es una herramienta funcional de apoyo visual.

El estudiante debe poder ejecutar e interpretar un gráfico de barras cuando el código está disponible, pero no se exige el mismo nivel de recuerdo autónomo que para `table()` o `prop.table()`.

### Habilidades recuperadas
M7 recupera:

- objeto y consulta;
- `<-`;
- `$`;
- vector;
- caso y variable;
- data frame;
- lectura de una base;
- interpretación de outputs;
- preparación previa de datos;
- conciencia de missing desde M6.

M7 no reenseña esas capacidades.

### Habilidades pospuestas
No se introducen todavía:

- clasificación nominal/ordinal;
- factores;
- niveles;
- escalas de medición formales;
- variables dummy;
- clasificación binaria formal;
- `sort()`;
- `factor()`;
- `levels()`;
- `useNA`;
- tablas de contingencia;
- Chi-cuadrado;
- descriptivos cuantitativos;
- histogramas;
- media;
- mediana;
- desviación estándar.

### Sintaxis nueva
- `table()`;
- `prop.table()`.

### Sintaxis funcional
- `barplot()`.

### Sintaxis que NO se introduce
No se introduce sintaxis adicional para ordenar, recodificar, formatear porcentajes, personalizar gráficos o manejar missing dentro de `table()`.

### Storage type ≠ significado estadístico
M7 no utiliza `str()`, `class()` ni `typeof()` para clasificar variables.

No se enseña:

```text
chr = categórica
num = cuantitativa
```

La clasificación se basa en el significado de los valores para los casos.

### Dataset / contrato de datos
M7 conserva exactamente el contrato de `encuesta_social_demo` heredado de M6:

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

M7 no modifica ninguna variable, valor, codificación o missing de este objeto.

### Variable principal de E2–E5
La variable principal es `carrera`.

Valores:

```text
Sociología
Historia
Antropología
Sociología
Trabajo Social
Antropología
Historia
Sociología
```

Frecuencias semánticas:

```text
Antropología   → 2
Historia       → 2
Sociología     → 3
Trabajo Social → 1
```

Proporciones:

```text
Antropología   → 0.250
Historia       → 0.250
Sociología     → 0.375
Trabajo Social → 0.125
```

Porcentajes equivalentes:

```text
Antropología   → 25 %
Historia       → 25 %
Sociología     → 37.5 %
Trabajo Social → 12.5 %
```

Total de referencia:

```text
N = 8
```

### Política de missing
M7 no reabre la enseñanza de missing.

Texto de continuidad recomendado:

> Ya sabemos que los datos ausentes deben revisarse antes de describir.
>
> En estos ejercicios usaremos variables categóricas sin `NA` para concentrarnos en cómo describir categorías.

No se introduce sintaxis nueva para incluir, excluir o mostrar missing dentro de tablas.

### Base de transferencia
M7-E6 utiliza un objeto distinto:

```text
encuesta_campus

id   transporte
1    Metro
2    Bus
3    Bicicleta
4    Metro
5    A pie
6    Bus
7    Metro
8    Bicicleta
```

Frecuencias:

```text
A pie       → 1
Bicicleta   → 2
Bus         → 2
Metro       → 3
```

Proporciones:

```text
A pie       → 0.125
Bicicleta   → 0.250
Bus         → 0.250
Metro       → 0.375
```

### Estrategia de scaffolding
1. Clasificación conceptual guiada por significado.
2. Worked example completo de `table()`.
3. Completion con `prop.table()`.
4. Recuperación productiva de ambas funciones solo desde comentarios.
5. Visualización funcional con código entregado.
6. Transferencia en base nueva sin nombrar las funciones.

### Estrategia de fading
`CLASIFICAR CON APOYO → OBSERVAR table() → COMPLETAR prop.table() → RECUPERAR AMBAS → INTERPRETAR barplot() → PRODUCIR AUTÓNOMAMENTE EN BASE NUEVA`

### Riesgos cognitivos
- decidir categoría/cantidad por la apariencia texto/número;
- creer que todo número representa una cantidad;
- confundir frecuencia con proporción;
- interpretar una proporción sin considerar el denominador;
- creer que `prop.table()` devuelve porcentajes literalmente;
- leer el orden de impresión de categorías como ranking;
- hardcodear conteos o proporciones;
- pensar que cada barra representa una persona;
- interpretar la altura de una barra de frecuencias como porcentaje;
- convertir `barplot()` en el centro de la descripción categórica;
- memorizar resultados concretos de `carrera` en vez de derivarlos de los datos.

### Número de ejercicios
6

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M7-E1 | ¿Cantidad o categoría? | NOVEDAD | variable categórica por significado | variable, valores, casos | baja-media |
| M7-E2 | ¿Cuántas personas respondieron cada cosa? | NOVEDAD | `table()` + frecuencia | `$`, `<-` | baja-media |
| M7-E3 | Del conteo a la proporción | NOVEDAD | `prop.table()` + denominador | objeto tabla, frecuencia | media |
| M7-E4 | Cuenta no es lo mismo que porcentaje | PRÁCTICA | ninguna | `table()`, `prop.table()` | media |
| M7-E5 | Ver la distribución | PRÁCTICA / VISUALIZACIÓN FUNCIONAL | micro-novedad funcional `barplot()` | tabla de frecuencias | baja-media |
| M7-E6 | Describe otra variable categórica | TRANSFERENCIA | ninguna | clasificación, `table()`, `prop.table()` | media |

---
## M7-E1 — ¿Cantidad o categoría?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
M7 no puede comenzar con una función descriptiva sin que el estudiante entienda primero **qué tipo de pregunta descriptiva corresponde al significado de una variable**.

E1 construye un criterio semántico estable:

> una variable es categórica porque sus valores representan grupos, tipos o categorías.

También destruye una heurística superficial que produciría errores en M7, M8 y módulos posteriores:

```text
texto → categórica
número → cantidad
```

### 3. Capacidad antes
Puede recuperar una variable, leer sus valores y revisar si contiene missing, pero todavía no dispone de un criterio explícito para decidir cuándo describir categorías.

### 4. Capacidad después
Puede reconocer una variable categórica por significado, distinguirla de una variable cuyos valores representan cantidades y reconocer que números también pueden funcionar como códigos categóricos.

### 5. Prerrequisitos
- variable;
- caso;
- columna;
- lectura de valores;
- números y texto;
- comprensión básica de una encuesta.

No requiere ninguna función nueva.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna.
- **Concepto nuevo:** variable categórica definida por significado.
- **Decisión nueva:** preguntar qué representan los valores antes de decidir cómo describirlos.

Existe una sola gran novedad conceptual.

### 7. Recuperaciones
Recupera:

- variable desde M4;
- valores;
- caso;
- lectura sustantiva de una columna.

No recupera `str()` porque el almacenamiento no es el criterio de clasificación.

### 8. Contexto sustantivo
Tres ejemplos de encuesta:

1. carrera;
2. horas de estudio;
3. zona geográfica codificada numéricamente.

### 9. Dataset / objetos
Ejemplo A:

```text
carrera

Sociología
Historia
Antropología
Trabajo Social
```

Ejemplo B:

```text
horas_estudio

3
5
2
4
```

Ejemplo C:

```text
zona_codigo

1 = Norte
2 = Centro
3 = Sur
```

`zona_codigo` es una representación conceptual para clasificar significado; no necesita incorporarse a `encuesta_social_demo`.

### 10. Texto para estudiante
Ya sabemos preparar una variable y revisar si faltan datos.

Antes de decidir **cómo describirla**, necesitamos preguntar:

> **¿qué representan sus valores?**

Observa `carrera`:

```text
Sociología
Historia
Antropología
Trabajo Social
```

Estos valores no indican cuánto tiene una persona. Indican a qué categoría pertenece.

Ahora observa `horas_estudio`:

```text
3
5
2
4
```

Aquí los valores sí indican una cantidad: horas.

Pero cuidado: ver números no basta.

```text
zona_codigo

1 = Norte
2 = Centro
3 = Sur
```

Aquí 1, 2 y 3 funcionan como **códigos de categorías**.

Responde:

1. ¿`carrera` representa categorías o cantidades?
2. ¿`horas_estudio` representa categorías o cantidades?
3. ¿`zona_codigo` representa categorías o cantidades?
4. ¿El valor 3 de `zona_codigo` significa “tres veces más zona” que el valor 1?

### 11. Modelo mental
```text
MIRAR LOS VALORES
↓
PREGUNTAR QUÉ REPRESENTAN
↓
GRUPOS / TIPOS
→ CATEGORÍAS

CUÁNTO
→ CANTIDADES
```

Regla explícita:

```text
SIGNIFICADO
>
APARIENCIA
```

### 12. Representación / código trabajado
No se requiere código productivo.

Puede utilizarse una comparación visual de tres tarjetas:

```text
carrera       → grupos
horas_estudio → cuánto
zona_codigo   → grupos codificados con números
```

### 13. Starter code
No aplica.

La pantalla debe ser conceptual y no abrir un editor solo para simular productividad.

### 14. Acción esperada
Clasificar los tres ejemplos y justificar la clasificación a partir del significado de los valores.

### 15. Solución canónica
```text
carrera
→ categórica

horas_estudio
→ representa una cantidad

zona_codigo
→ categórica
```

Respuesta a la pregunta diagnóstica:

```text
3 no significa tres veces más zona que 1.
Los números son códigos de categorías.
```

### 16. Resultado esperado
El estudiante puede formular una explicación equivalente a:

> Una variable es categórica cuando sus valores indican categorías, grupos o tipos. Que los valores estén escritos con números o texto no decide la clasificación.

### 17. Criterio semántico de éxito
Comprobar:

- `carrera` clasificada como categórica;
- `horas_estudio` clasificada como cantidad;
- `zona_codigo` clasificada como categórica;
- rechazo explícito de “3 es tres veces 1” en el ejemplo de zona;
- justificación basada en significado.

No considerar suficiente:

> carrera es categórica porque tiene texto.

### 18. Estrategias alternativas válidas
Se aceptan expresiones como:

- grupo;
- tipo;
- categoría;
- etiqueta sustantiva;

siempre que el criterio sea semántico.

Para `horas_estudio`, se acepta “cantidad”, “cantidad de horas” o equivalente.

### 19. Error esperado / misconception
- texto = categórica;
- número = cantidad;
- zona 3 > zona 1 en sentido sustantivo;
- usar información técnica de almacenamiento como criterio;
- creer que una categoría tiene que estar escrita con palabras.

### 20. Feedback correcto
Bien. La clasificación depende de **qué representan los valores**. `carrera` y `zona_codigo` indican categorías; `horas_estudio` indica una cantidad.

### 21. Feedback resultado correcto / estrategia incorrecta
Si clasifica `carrera` correctamente porque “es texto”:

> La clasificación coincide, pero la razón no es que aparezca texto. Una variable también puede usar números como códigos de categorías. La pregunta importante es qué representan sus valores.

### 22. Hint 1
Pregunta qué significa cada valor para una persona.

### 23. Hint 2
¿El valor indica **cuánto** tiene el caso o **a qué grupo** pertenece?

### 24. Hint 3
`carrera` y `zona_codigo` indican grupos; `horas_estudio` indica una cantidad.

### 25. Predicción
No se usa una predicción de código. La clasificación de los ejemplos ya funciona como actividad diagnóstica.

### 26. Tipo de ejercicio
Clasificación / decisión conceptual.

### 27. Andamiaje
Alto.

Los tres ejemplos están completamente visibles y contrastados.

### 28. Carga cognitiva
Baja-media.

No hay sintaxis nueva. La carga proviene de abandonar una regla superficial y adoptar un criterio semántico.

### 29. Fading
E1 entrega tres ejemplos contrastantes. E6 recuperará el criterio con una variable nueva y sin explicar nuevamente la distinción.

### 30. Recuperación futura
El criterio categoría/cantidad reaparece inmediatamente en M8 y posteriormente en M12/M13 cuando el estudiante debe elegir una ruta analítica.

`table()` y `prop.table()` se recuperarán en M12 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar ejemplos concretos:

```text
carrera = categórica
horas = cantidad
```

sin comprender el criterio.

`zona_codigo` existe específicamente para impedir esa estrategia.

### 32. Criterio de transferencia
Existe transferencia cuando el estudiante puede clasificar una variable con nombres y valores diferentes, incluidos códigos numéricos, a partir de lo que representan sus valores.

### 33. Notas de implementación futura
Usar una interacción conceptual como clasificación, matching o selección múltiple con justificación breve.

No invocar `str()`, `class()` ni `typeof()` en el grader.

---
## M7-E2 — ¿Cuántas personas respondieron cada cosa?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Después de reconocer que `carrera` representa categorías aparece una necesidad descriptiva auténtica:

> ¿cuántos casos pertenecen a cada categoría?

E2 introduce `table()` como respuesta directa a esa necesidad y construye el significado de **frecuencia** antes de exigir producción autónoma.

### 3. Capacidad antes
Puede reconocer que `carrera` es categórica y recuperar una variable mediante `$`.

### 4. Capacidad después
Puede ejecutar e interpretar una tabla de frecuencias y comprender que cada valor indica cuántos casos pertenecen a una categoría.

### 5. Prerrequisitos
- variable categórica;
- `$`;
- objeto;
- `<-`;
- consulta de un objeto;
- lectura de outputs.

### 6. Gran novedad
- **Sintaxis nueva:** `table()`.
- **Concepto nuevo:** frecuencia.
- **Decisión nueva:** contar casos por categoría.

Sintaxis y concepto forman una sola unidad funcional: `table()` responde “¿cuántos casos hay en cada categoría?”.

### 7. Recuperaciones
Recupera:

- `encuesta_social_demo$carrera`;
- `<-`;
- creación y consulta de objetos;
- caso/variable.

### 8. Contexto sustantivo
Distribución de carreras en `encuesta_social_demo`.

### 9. Dataset / objetos
Variable:

```r
encuesta_social_demo$carrera
```

Valores contractuales:

```text
Sociología
Historia
Antropología
Sociología
Trabajo Social
Antropología
Historia
Sociología
```

Objeto nuevo que se crea:

```text
tabla_carrera
```

### 10. Texto para estudiante
Ya identificamos que `carrera` representa categorías.

Ahora queremos responder:

> **¿cuántas personas hay en cada carrera?**

Antes de ejecutar, mira los ocho casos:

> ¿qué carrera esperas que aparezca más veces?

Podemos pedir a R que cuente cada categoría:

```r
tabla_carrera <- table(encuesta_social_demo$carrera)

tabla_carrera
```

El número de casos que aparece en cada categoría se llama **frecuencia**.

Importante:

> El orden en que R muestra las categorías no indica cuál es más frecuente ni cuál es más importante.
>
> Para comparar categorías, mira sus conteos.

### 11. Modelo mental
```text
VARIABLE CATEGÓRICA
↓
CATEGORÍAS
↓
CONTAR CASOS EN CADA UNA
↓
FRECUENCIAS
```

### 12. Representación / código trabajado
Worked example completo:

```r
tabla_carrera <- table(encuesta_social_demo$carrera)

tabla_carrera
```

Interpretación visual:

```text
Antropología   → 2 casos
Historia       → 2 casos
Sociología     → 3 casos
Trabajo Social → 1 caso
```

### 13. Starter code
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

tabla_carrera
```

### 14. Acción esperada
1. predecir la categoría más frecuente;
2. ejecutar el código;
3. identificar cuántos casos hay en cada categoría;
4. identificar la categoría con mayor frecuencia;
5. interpretar correctamente el término frecuencia.

### 15. Solución canónica
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

tabla_carrera
```

Respuesta interpretativa:

```text
Sociología es la categoría más frecuente.
Frecuencia de Sociología = 3 casos.
```

### 16. Resultado esperado
Asociaciones semánticas:

```text
Antropología   → 2
Historia       → 2
Sociología     → 3
Trabajo Social → 1
```

No fijar el orden impreso como criterio pedagógico.

### 17. Criterio semántico de éxito
Comprobar:

- existe una tabla derivada de `encuesta_social_demo$carrera`;
- las cuatro categorías están presentes;
- cada categoría se asocia a su frecuencia correcta;
- Sociología se identifica como más frecuente con 3 casos;
- la estrategia depende de la variable real;
- no se acepta una secuencia de conteos escrita manualmente como evidencia de `table()`.

Perturbation test recomendado:

- reordenar filas: frecuencias no cambian;
- cambiar la carrera de un caso: frecuencias sí cambian.

### 18. Estrategias alternativas válidas
Se acepta:

```r
table(encuesta_social_demo$carrera)
```

sin guardar el objeto si la tarea se evalúa solo por la tabla.

Sin embargo, la solución canónica guarda `tabla_carrera` porque E3 necesita reutilizarla y porque recuperar `<-` tiene valor pedagógico.

### 19. Error esperado / misconception
- confundir frecuencia con porcentaje;
- interpretar la primera categoría impresa como la más importante;
- creer que el orden de salida es un ranking;
- escribir `c(2, 2, 3, 1)` manualmente;
- contar visualmente y entregar el resultado sin usar `table()` cuando la habilidad sintáctica es objetivo.

### 20. Feedback correcto
Bien. `table()` contó cuántos casos pertenecen a cada categoría. Sociología aparece 3 veces y es la categoría más frecuente.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe los conteos manualmente:

> Los conteos coinciden, pero deben calcularse desde `carrera`. Si cambia una respuesta, la tabla debe actualizarse automáticamente.

Si identifica la primera categoría como “más frecuente” por posición:

> El orden en que R imprime las categorías no es un ranking. Compara los números de cada categoría.

### 22. Hint 1
Necesitas contar cuántos casos aparecen en cada categoría.

### 23. Hint 2
`table()` recibe una variable y produce un conteo por categoría.

### 24. Hint 3
```r
tabla_carrera <- table(encuesta_social_demo$carrera)
```

### 25. Predicción
Sí.

Antes de ejecutar:

> ¿Qué carrera esperas que tenga la frecuencia más alta?

Respuesta esperada: Sociología.

### 26. Tipo de ejercicio
Worked example.

### 27. Andamiaje
Alto.

La función, variable y asignación están entregadas.

### 28. Carga cognitiva
Baja-media.

La única gran novedad es construir una tabla de frecuencias; `$` y `<-` ya son conocimientos disponibles.

### 29. Fading
E2 entrega `table()` completo.

E4 retirará el nombre de la función.

E6 exigirá producirla en una base nueva.

### 30. Recuperación futura
`table()` se practica en M7-E4, se produce autónomamente en M7-E6, se recupera en M12-E1 y se transfiere nuevamente en M13.

### 31. Riesgo de aprendizaje superficial
Memorizar:

```text
Sociología = 3
```

sin comprender que 3 fue calculado desde los ocho casos.

El perturbation test y el requisito de dependencia de la variable protegen contra esto.

### 32. Criterio de transferencia
La habilidad estará disponible cuando pueda producir una tabla de frecuencias para una variable categórica nueva sin recibir `table()` en la consigna.

### 33. Notas de implementación futura
El grader debe comparar asociaciones categoría → frecuencia y no una cadena impresa literal, porque el orden de presentación puede variar.

---
## M7-E3 — Del conteo a la proporción

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Una frecuencia responde:

> ¿cuántos casos?

Pero no expresa directamente qué parte del total representan esos casos.

E3 introduce la proporción como una descripción relativa y hace explícito su denominador.

### 3. Capacidad antes
Puede construir e interpretar `tabla_carrera` como tabla de frecuencias.

### 4. Capacidad después
Puede convertir una tabla de frecuencias en proporciones mediante `prop.table()` e interpretar cada proporción respecto del total de casos considerados.

### 5. Prerrequisitos
- `tabla_carrera`;
- frecuencia;
- N total = 8;
- objetos reutilizables;
- lectura de decimales básicos.

### 6. Gran novedad
- **Sintaxis nueva:** `prop.table()`.
- **Concepto nuevo:** proporción.
- **Decisión nueva:** relacionar una frecuencia con su total de referencia.

El foco no está en volver a producir `table()`, sino en transformar una tabla ya conocida.

### 7. Recuperaciones
Recupera:

- objeto `tabla_carrera`;
- frecuencia;
- consulta de objetos;
- interpretación de casos.

### 8. Contexto sustantivo
La misma distribución de `carrera` para mantener estable el contexto mientras cambia el tipo de resumen.

### 9. Dataset / objetos
Entrada:

```text
tabla_carrera
```

con:

```text
Antropología   → 2
Historia       → 2
Sociología     → 3
Trabajo Social → 1
```

Total:

```text
N = 8
```

### 10. Texto para estudiante
Ya sabemos que Sociología aparece en 3 casos.

Ahora podemos hacer otra pregunta:

> **¿qué parte del total representan esos 3 casos?**

Para Sociología:

```text
3 casos
de
8 casos totales

↓
3 / 8

↓
0.375

↓
37.5 %
```

`0.375` es una **proporción**.

`37.5 %` es esa misma relación expresada sobre 100.

Para obtener las proporciones de toda la tabla usamos:

```r
prop.table(tabla_carrera)
```

Importante:

> `prop.table()` devuelve proporciones.
>
> No devuelve porcentajes escritos con el símbolo `%`.

Antes de ejecutar:

> Si Sociología tiene 3 de 8 casos, ¿esperas una proporción menor o mayor que 0.5?

### 11. Modelo mental
```text
FRECUENCIA
↓
¿QUÉ PARTE DEL TOTAL REPRESENTA?
↓
FRECUENCIA / TOTAL
↓
PROPORCIÓN
```

Relación de representaciones:

```text
3 casos
→ frecuencia

3 de 8
→ relación con el total

0.375
→ proporción

37.5 %
→ porcentaje equivalente
```

### 12. Representación / código trabajado
Completion:

```r
prop.table(____________)
```

Representación conceptual adicional:

```text
Antropología   2/8 → 0.250 → 25 %
Historia       2/8 → 0.250 → 25 %
Sociología     3/8 → 0.375 → 37.5 %
Trabajo Social 1/8 → 0.125 → 12.5 %
```

### 13. Starter code
```r
prop.table(____________)
```

### 14. Acción esperada
1. predecir si 3/8 es menor o mayor que 0.5;
2. completar el nombre del objeto;
3. ejecutar;
4. interpretar la proporción de Sociología;
5. identificar N=8 como denominador.

### 15. Solución canónica
```r
prop.table(tabla_carrera)
```

### 16. Resultado esperado
Asociaciones:

```text
Antropología   → 0.250
Historia       → 0.250
Sociología     → 0.375
Trabajo Social → 0.125
```

Conceptualmente:

```text
0.250 + 0.250 + 0.375 + 0.125 = 1
```

No se introduce código nuevo para comprobar esa suma.

### 17. Criterio semántico de éxito
Comprobar:

- se utiliza `prop.table()` sobre una tabla válida;
- las categorías se asocian a las proporciones correctas;
- Sociología se interpreta como 3/8;
- 0.375 se interpreta como proporción;
- 37.5 % se reconoce como porcentaje equivalente;
- N=8 se identifica como denominador;
- no se hardcodean los decimales.

No comparar la cantidad de dígitos impresos.

### 18. Estrategias alternativas válidas
Se acepta:

```r
prop.table(table(encuesta_social_demo$carrera))
```

porque produce proporciones semánticamente correctas desde los datos.

La solución canónica sigue usando `tabla_carrera` para reforzar reutilización y aislar la nueva función.

### 19. Error esperado / misconception
- interpretar 0.375 como 0.375 personas;
- decir que `prop.table()` devuelve porcentajes;
- olvidar que la proporción depende de N;
- dividir por un total incorrecto;
- escribir proporciones manualmente;
- creer que 0.375 y 37.5 son el mismo número sin cambio de escala.

### 20. Feedback correcto
Bien. La frecuencia de Sociología es 3 casos y su proporción es 0.375 porque representa 3 de los 8 casos, equivalente a 37.5 %.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe los decimales manualmente:

> Los valores coinciden, pero deben derivarse de la tabla. Si cambian las frecuencias, las proporciones también deben cambiar.

Si llama “porcentaje” a 0.375:

> `0.375` es una proporción. Expresada sobre 100 equivale a `37.5 %`.

### 22. Hint 1
Ahora quieres saber qué parte del total representa cada conteo.

### 23. Hint 2
`prop.table()` transforma una tabla de frecuencias en proporciones.

### 24. Hint 3
```r
prop.table(tabla_carrera)
```

### 25. Predicción
Sí.

> Si Sociología tiene 3 de 8 casos, ¿la proporción será menor o mayor que 0.5?

Respuesta: menor.

### 26. Tipo de ejercicio
Worked/completion.

### 27. Andamiaje
Medio-alto.

La función está visible, pero el objeto debe recuperarse y la interpretación debe ser producida.

### 28. Carga cognitiva
Media.

Interactúan:

- función nueva;
- frecuencia previa;
- denominador;
- proporción;
- porcentaje equivalente.

Mantener `carrera` estable evita añadir otra fuente de carga.

### 29. Fading
E3 entrega la estructura de `prop.table()` con un hueco.

E4 retirará los nombres de ambas funciones.

E6 exigirá producción autónoma.

### 30. Recuperación futura
`prop.table()` se practica en M7-E4, se produce en M7-E6, se recupera en M12-E2 y se transfiere en M13.

### 31. Riesgo de aprendizaje superficial
Aprender que `prop.table()` “hace decimales” sin comprender el total de referencia.

La representación `3 de 8 → 0.375` debe permanecer central.

### 32. Criterio de transferencia
Debe poder interpretar una proporción en otra variable preguntándose explícitamente “¿de qué total?” y producirla desde una tabla de frecuencias nueva.

### 33. Notas de implementación futura
No exigir coincidencia exacta de impresión decimal.

El grader debe comparar valores con tolerancia y mantener las asociaciones categoría → proporción.

---
## M7-E4 — Cuenta no es lo mismo que porcentaje

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
E2 y E3 introdujeron las dos herramientas centrales por separado.

E4 debe convertirlas en una secuencia productiva y asegurar que el estudiante comprenda que:

```text
frecuencia ≠ proporción ≠ porcentaje como notación
```

La pantalla también introduce un contraste de denominadores para mostrar por qué una misma frecuencia puede representar partes distintas de dos grupos.

### 3. Capacidad antes
Puede interpretar `table()` y completar `prop.table(tabla_carrera)` con apoyo.

### 4. Capacidad después
Puede recuperar ambas funciones con comentarios semánticos, producir frecuencias y proporciones e interpretar la diferencia entre “cuántos” y “qué parte del total”.

### 5. Prerrequisitos
- variable categórica;
- `table()`;
- frecuencia;
- `prop.table()`;
- proporción;
- porcentaje como expresión sobre 100;
- denominador.

### 6. Gran novedad
No hay gran sintaxis nueva.

La demanda aumenta por:

- recuperación de dos herramientas;
- producción con menos apoyo;
- decisión interpretativa.

El contraste 2/4 vs 2/8 es un ejemplo conceptual, no una nueva técnica.

### 7. Recuperaciones
Recupera:

- `table()`;
- `prop.table()`;
- `<-`;
- `encuesta_social_demo$carrera`;
- N=8;
- interpretación frecuencia/proporción.

### 8. Contexto sustantivo
Se mantiene `carrera` para que la dificultad provenga de recuperar y coordinar las herramientas, no de aprender nuevos datos.

Después se incorpora una microcomparación abstracta entre dos grupos de diferente tamaño.

### 9. Dataset / objetos
Principal:

```r
encuesta_social_demo$carrera
```

Objeto esperado:

```text
tabla_carrera
```

Microcomparación:

```text
Grupo A: 2 de 4
Grupo B: 2 de 8
```

### 10. Texto para estudiante
Una categoría puede describirse con distintos números.

Para Sociología:

```text
frecuencia
= 3 casos

proporción
= 0.375

porcentaje equivalente
= 37.5 %
```

Esos números responden preguntas diferentes:

```text
frecuencia
→ ¿cuántos casos?

proporción
→ ¿qué parte del total?
```

Recupera ahora las dos descripciones de `carrera`.

Después compara:

```text
Grupo A
2 de 4
= 50 %

Grupo B
2 de 8
= 25 %
```

Ambos grupos tienen frecuencia 2.

> ¿Representan esos dos casos la misma parte del grupo?

### 11. Modelo mental
```text
VARIABLE CATEGÓRICA
↓
table()
↓
FRECUENCIA
↓
prop.table()
↓
PROPORCIÓN
↓
INTERPRETAR RESPECTO DE N
```

Contraste:

```text
MISMA FRECUENCIA
+
DISTINTO N
→
DISTINTA PROPORCIÓN
```

### 12. Representación / código trabajado
No se entrega código trabajado completo nuevo.

Solo se recuerda la meta:

```text
carrera
→ conteos
→ proporciones
```

### 13. Starter code
```r
# cuenta los casos de cada carrera y guarda el resultado


# obtén las proporciones de esa tabla
```

### 14. Acción esperada
1. producir `tabla_carrera`;
2. producir sus proporciones;
3. identificar frecuencia y proporción de Sociología;
4. responder qué medida contesta “cuántas personas”;
5. responder qué medida contesta “qué parte del total”;
6. explicar por qué 2/4 y 2/8 tienen proporciones distintas.

### 15. Solución canónica
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

prop.table(tabla_carrera)
```

Interpretaciones:

```text
Sociología:
frecuencia = 3
proporción = 0.375
porcentaje = 37.5 %

Grupo A:
2/4 = 50 %

Grupo B:
2/8 = 25 %
```

### 16. Resultado esperado
Frecuencias:

```text
Antropología   → 2
Historia       → 2
Sociología     → 3
Trabajo Social → 1
```

Proporciones:

```text
Antropología   → 0.250
Historia       → 0.250
Sociología     → 0.375
Trabajo Social → 0.125
```

Interpretación:

```text
frecuencia → cuántos casos
proporción → qué parte del total
```

### 17. Criterio semántico de éxito
Evaluar dos componentes.

**Producción**
- tabla dependiente de `carrera`;
- conteos correctos;
- proporciones derivadas de una tabla válida;
- no hardcoding.

**Interpretación**
- 3 = frecuencia de Sociología;
- 0.375 = proporción de Sociología;
- 37.5 % = porcentaje equivalente;
- N=8 como denominador;
- reconoce que 2/4 y 2/8 tienen igual frecuencia pero distinta proporción.

Perturbation test muy recomendado.

### 18. Estrategias alternativas válidas
Se admite:

```r
tabla_carrera <- table(encuesta_social_demo$carrera)
prop.table(tabla_carrera)
```

y también una composición equivalente que derive ambas salidas desde los datos.

La estrategia debe demostrar ambas habilidades; una lista manual de resultados no cuenta.

### 19. Error esperado / misconception
- frecuencia y proporción son intercambiables;
- 0.375 significa 0.375 casos;
- misma frecuencia implica misma proporción;
- porcentaje y proporción son idénticos en escala;
- hardcoding;
- olvidar el denominador.

### 20. Feedback correcto
Bien. La frecuencia responde cuántos casos hay; la proporción responde qué parte del total representan. Por eso la misma frecuencia puede corresponder a proporciones distintas si cambia el total.

### 21. Feedback resultado correcto / estrategia incorrecta
Si los valores son correctos pero manuales:

> Las cifras coinciden, pero deben calcularse desde los datos. Si cambia una respuesta, frecuencias y proporciones deben actualizarse.

Si responde correctamente 50 % y 25 % sin explicar el total:

> El resultado coincide. La idea clave es que ambas frecuencias son 2, pero los totales son 4 y 8; por eso las proporciones son diferentes.

### 22. Hint 1
Primero obtén los conteos. Después expresa esos conteos respecto del total.

### 23. Hint 2
Recupera las dos herramientas de los ejercicios anteriores.

### 24. Hint 3
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

prop.table(tabla_carrera)
```

### 25. Predicción
No se añade una fase separada.

La comparación 2/4 vs 2/8 cumple la función de provocar razonamiento antes de la explicación.

### 26. Tipo de ejercicio
Producción guiada + interpretación.

### 27. Andamiaje
Medio.

Solo se entregan comentarios semánticos.

### 28. Carga cognitiva
Media.

No hay sintaxis nueva; interactúan recuperación, denominador y distinción conceptual entre tres representaciones.

### 29. Fading
E2: función completa.

E3: completion.

E4: solo comentarios.

E6: base nueva y comentarios mínimos.

### 30. Recuperación futura
Las dos funciones reaparecen juntas en E6, después en M12 y finalmente en M13.

### 31. Riesgo de aprendizaje superficial
Tratar `prop.table()` como una transformación formal de `table()` sin comprender qué pregunta responde.

La comparación con distintos N obliga a interpretar el denominador.

### 32. Criterio de transferencia
Existe transferencia si el estudiante puede explicar por qué iguales conteos no implican iguales proporciones cuando cambian los totales y producir ambas medidas en otra variable.

### 33. Notas de implementación futura
El semantic grader debe separar:

1. tabla;
2. proporciones;
3. respuestas interpretativas.

Así el feedback puede identificar qué componente falló.

---
## M7-E5 — Ver la distribución

### 1. Rol pedagógico
PRÁCTICA / VISUALIZACIÓN FUNCIONAL.

### 2. Por qué existe
Una tabla de frecuencias y un gráfico de barras pueden representar la misma distribución categórica.

E5 desarrolla literacy gráfica básica sin convertir la creación de gráficos en una nueva habilidad central.

La función de `barplot()` es mostrar otra representación de información que ya se comprende numéricamente.

### 3. Capacidad antes
Puede producir e interpretar frecuencias y proporciones de `carrera`.

### 4. Capacidad después
Puede leer un gráfico de barras de frecuencias relacionando cada barra con una categoría y su altura con el número de casos.

### 5. Prerrequisitos
- `tabla_carrera`;
- frecuencia;
- categoría;
- comparación de conteos.

### 6. Gran novedad
No hay gran novedad curricular.

`barplot()` es una micro-novedad funcional.

El modelo estadístico ya existe:

```text
categoría → frecuencia
```

Solo cambia la representación.

### 7. Recuperaciones
Recupera:

- `tabla_carrera`;
- categoría más frecuente;
- frecuencia de Sociología = 3;
- lectura de una distribución categórica.

### 8. Contexto sustantivo
Distribución de carrera en los mismos ocho casos.

Mantener el contexto permite concentrar la atención en la equivalencia tabla ↔ gráfico.

### 9. Dataset / objetos
Objeto:

```text
tabla_carrera
```

derivado de:

```r
table(encuesta_social_demo$carrera)
```

### 10. Texto para estudiante
Ya podemos leer la distribución de `carrera` como una tabla.

También podemos representar **los mismos conteos** visualmente:

```r
barplot(tabla_carrera)
```

En este gráfico:

- cada barra representa una categoría;
- la altura representa su frecuencia.

Antes de ejecutar:

> ¿qué categoría esperas que tenga la barra más alta?

Después de observar el gráfico:

> ¿qué representa la altura de esa barra?

El gráfico no cambia los datos ni crea una nueva medida.

Representa visualmente la misma tabla de frecuencias.

### 11. Modelo mental
```text
TABLA DE FRECUENCIAS
↓
MISMA INFORMACIÓN
↓
GRÁFICO DE BARRAS
```

Lectura:

```text
UNA BARRA
=
UNA CATEGORÍA

ALTURA
=
FRECUENCIA
```

### 12. Representación / código trabajado
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

barplot(tabla_carrera)
```

No se personaliza el gráfico.

### 13. Starter code
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

barplot(tabla_carrera)
```

### 14. Acción esperada
1. predecir la barra más alta;
2. ejecutar el gráfico;
3. identificar Sociología como barra más alta;
4. explicar que la altura corresponde a 3 casos;
5. explicar que cada barra representa una categoría.

### 15. Solución canónica
```r
tabla_carrera <- table(encuesta_social_demo$carrera)

barplot(tabla_carrera)
```

Interpretación:

```text
barra más alta → Sociología
altura → frecuencia 3
```

### 16. Resultado esperado
Gráfico de barras con cuatro categorías y alturas correspondientes a las frecuencias:

```text
Antropología   → 2
Historia       → 2
Sociología     → 3
Trabajo Social → 1
```

No se exige una configuración visual específica.

### 17. Criterio semántico de éxito
Comprobar:

- el gráfico se construye desde una tabla de frecuencias válida;
- existe una barra por categoría;
- la interpretación identifica Sociología como mayor;
- altura de Sociología se interpreta como 3 casos;
- no se interpreta la altura como porcentaje en este gráfico.

No evaluar colores, tipografía, dimensiones o estética.

### 18. Estrategias alternativas válidas
Se acepta:

```r
barplot(table(encuesta_social_demo$carrera))
```

como representación equivalente.

Sin embargo, la solución canónica utiliza `tabla_carrera` para reforzar continuidad entre tabla y gráfico.

### 19. Error esperado / misconception
- cada barra representa una persona;
- altura = porcentaje aunque se graficaron frecuencias;
- barra izquierda = categoría más importante;
- ordenar visualmente como si fuera ranking sustantivo;
- pensar que el gráfico contiene información distinta de la tabla;
- introducir conceptos no pertinentes como pendiente o dispersión.

### 20. Feedback correcto
Bien. Cada barra representa una categoría y su altura representa la frecuencia. Sociología es la barra más alta porque aparece en 3 casos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si identifica Sociología pero dice “37.5” como altura:

> La categoría es correcta, pero este gráfico usa `tabla_carrera`, que contiene frecuencias. La altura de Sociología representa 3 casos.

Si interpreta una barra como una persona:

> Cada barra resume todos los casos de una categoría, no un caso individual.

### 22. Hint 1
El gráfico representa la tabla de frecuencias que ya construiste.

### 23. Hint 2
`barplot()` puede recibir directamente una tabla de conteos.

### 24. Hint 3
```r
barplot(tabla_carrera)
```

### 25. Predicción
Sí.

> ¿Qué categoría tendrá la barra más alta?

Respuesta: Sociología.

### 26. Tipo de ejercicio
Ejecución / observación / interpretación.

### 27. Andamiaje
Alto.

El código está completamente entregado porque `barplot()` es funcional.

### 28. Carga cognitiva
Baja-media.

La única micro-novedad es cambiar de representación; la distribución ya es conocida.

### 29. Fading
No se exige fading productivo de `barplot()`.

El fading central del módulo corresponde a `table()` y `prop.table()`.

### 30. Recuperación futura
`barplot()` no requiere recuperación curricular obligatoria.

La lectura de distribuciones visuales prepara indirectamente M8 y visualizaciones posteriores.

### 31. Riesgo de aprendizaje superficial
Concluir que describir categorías consiste en “hacer un gráfico”.

La pantalla debe recordar que:

```text
tabla + interpretación
= núcleo

barplot
= apoyo visual
```

### 32. Criterio de transferencia
La transferencia visual mínima consiste en poder leer otro gráfico de barras categórico sabiendo qué representa una barra y qué representa su altura, sin recordar necesariamente la sintaxis exacta.

### 33. Notas de implementación futura
No introducir personalización:

- colores;
- títulos;
- `names.arg`;
- `las`;
- `ylim`;
- ordenamiento;
- ggplot;
- temas.

Eliminar por completo cualquier feedback heredado sobre pendiente, dispersión o casos extremos.

---
## M7-E6 — Describe otra variable categórica

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
E6 es la evidencia terminal de M7.

Cambia:

- base;
- nombre de variable;
- categorías;
- contexto;

y retira los nombres de las funciones para comprobar si el estudiante puede recuperar por sí mismo la ruta:

```text
categorías → frecuencias → proporciones → interpretación
```

### 3. Capacidad antes
Puede clasificar una variable categórica, producir frecuencias/proporciones con apoyo decreciente e interpretar un gráfico de barras funcional.

### 4. Capacidad después
Puede recibir una variable categórica nueva, producir autónomamente frecuencias y proporciones e interpretar cuál categoría es más frecuente y qué parte del total representa.

### 5. Prerrequisitos
- criterio categórico por significado;
- `$`;
- `<-`;
- `table()`;
- `prop.table()`;
- frecuencia;
- proporción;
- porcentaje;
- denominador.

### 6. Gran novedad
Ninguna.

La dificultad está en:

- reconocer el tipo de variable;
- elegir herramientas;
- producir código;
- interpretar.

### 7. Recuperaciones
Recupera toda la secuencia nuclear de M7.

`barplot()` no es requisito.

### 8. Contexto sustantivo
Formas de transporte utilizadas para llegar al campus.

### 9. Dataset / objetos
Base nueva disponible:

```text
encuesta_campus

id   transporte
1    Metro
2    Bus
3    Bicicleta
4    Metro
5    A pie
6    Bus
7    Metro
8    Bicicleta
```

No contiene missing en `transporte`.

### 10. Texto para estudiante
Ahora cambia la base.

`encuesta_campus` registra cómo llegan al campus ocho personas.

Primero piensa:

> ¿`transporte` representa categorías o una cantidad?

Después describe la variable.

Obtén:

1. cuántos casos hay en cada forma de transporte;
2. qué proporción del total representa cada categoría;
3. cuál es la forma de transporte más frecuente;
4. qué porcentaje del total representa esa categoría.

No se indican las funciones.

Decide qué herramientas ya conocidas necesitas.

### 11. Modelo mental
```text
VARIABLE NUEVA
↓
¿QUÉ REPRESENTAN LOS VALORES?
↓
CATEGORÍAS
↓
CONTAR
↓
FRECUENCIAS
↓
RELACIONAR CON N
↓
PROPORCIONES
↓
INTERPRETAR
```

### 12. Representación / código trabajado
No hay worked example nuevo.

Solo se muestra la base `encuesta_campus`.

### 13. Starter code
```r
# obtén los conteos por categoría


# obtén después las proporciones
```

### 14. Acción esperada
1. reconocer `transporte` como categórica;
2. producir una tabla de frecuencias;
3. producir proporciones;
4. identificar Metro como categoría más frecuente;
5. interpretar 3 de 8 = 0.375 = 37.5 %.

### 15. Solución canónica
```r
tabla_transporte <- table(encuesta_campus$transporte)

tabla_transporte

prop.table(tabla_transporte)
```

### 16. Resultado esperado
Frecuencias:

```text
A pie       → 1
Bicicleta   → 2
Bus         → 2
Metro       → 3
```

Proporciones:

```text
A pie       → 0.125
Bicicleta   → 0.250
Bus         → 0.250
Metro       → 0.375
```

Interpretación:

```text
Metro
→ 3 casos
→ 3 de 8
→ proporción 0.375
→ 37.5 %
```

### 17. Criterio semántico de éxito
Evaluar por componentes.

**Clasificación**
- `transporte` se reconoce como categórica por significado.

**Frecuencias**
- se derivan de `encuesta_campus$transporte`;
- A pie = 1;
- Bicicleta = 2;
- Bus = 2;
- Metro = 3.

**Proporciones**
- se derivan de una tabla válida;
- A pie = 0.125;
- Bicicleta = 0.250;
- Bus = 0.250;
- Metro = 0.375.

**Interpretación**
- Metro es la categoría más frecuente;
- N=8;
- 3/8 = 0.375;
- 0.375 equivale a 37.5 %.

**Estrategia**
- demuestra `table()` y `prop.table()`;
- no hardcodea resultados.

Perturbation test muy recomendado.

### 18. Estrategias alternativas válidas
Se acepta:

```r
tabla_transporte <- table(encuesta_campus$transporte)
prop.table(tabla_transporte)
```

y también:

```r
table(encuesta_campus$transporte)
prop.table(table(encuesta_campus$transporte))
```

si produce tanto los conteos como las proporciones solicitadas.

No se exige `barplot()`.

### 19. Error esperado / misconception
- elegir una función cuantitativa porque los casos están numerados;
- producir solo frecuencias;
- producir solo proporciones;
- llamar “personas” a 0.375;
- denominar 0.375 “37.5 %” sin reconocer el cambio de escala;
- hardcodear conteos o proporciones;
- memorizar Metro = 3 sin depender de los datos.

### 20. Feedback correcto
Bien. Reconociste una variable categórica nueva, calculaste sus frecuencias y proporciones y pudiste interpretar la categoría más frecuente respecto del total.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea:

> Los valores coinciden, pero deben derivarse de `transporte`. Si cambia una respuesta, la descripción debe actualizarse automáticamente.

Si obtiene solo frecuencias:

> Ya respondiste cuántos casos hay en cada categoría. Falta expresar esos conteos respecto del total.

Si obtiene solo proporciones:

> Las proporciones son correctas, pero la tarea también pide los conteos originales.

### 22. Hint 1
Primero necesitas saber cuántos casos hay en cada categoría. Después, qué parte del total representan.

### 23. Hint 2
Recupera las dos herramientas que usaste para obtener frecuencias y después proporciones.

### 24. Hint 3
```r
tabla_transporte <- table(encuesta_campus$transporte)

prop.table(tabla_transporte)
```

### 25. Predicción
No se agrega una fase separada.

La clasificación inicial de `transporte` y la tarea integrada ya exigen decisión.

### 26. Tipo de ejercicio
Transferencia cercana.

### 27. Andamiaje
Bajo-medio.

Hay dos comentarios semánticos, pero ninguna función está nombrada.

### 28. Carga cognitiva
Media.

No aparece sintaxis nueva. La carga proviene de recuperar y coordinar:

- clasificación;
- frecuencias;
- proporciones;
- interpretación.

### 29. Fading
Trayectoria final:

```text
E1 → concepto guiado
E2 → table() entregado
E3 → prop.table() completion
E4 → comentarios
E5 → función visual entregada
E6 → funciones no nombradas + base nueva
```

### 30. Recuperación futura
`table()` se recupera en M12-E1.

`prop.table()` se recupera en M12-E2.

Ambas deben estar disponibles para elección en M13.

### 31. Riesgo de aprendizaje superficial
Aplicar `table()` y `prop.table()` por imitación sin reconocer por qué corresponden a `transporte`.

La clasificación inicial y la interpretación obligatoria forman parte del criterio de éxito.

### 32. Criterio de transferencia
Existe evidencia de transferencia si el estudiante puede repetir esta ruta en otra base categórica, con diferentes nombres, frecuencias y proporciones, sin que la consigna nombre las funciones.

### 33. Notas de implementación futura
No exigir `barplot()` para aprobar.

El grader debe separar:

1. clasificación;
2. frecuencias;
3. proporciones;
4. interpretación;
5. estrategia.

Así puede ofrecer feedback localizado.

---

# Cierre conceptual de M7 y puente a M8

Después de E6 mostrar:

> Ya sabemos describir una variable cuando sus valores representan categorías:
>
> podemos contar cuántos casos hay en cada una
> y comparar qué parte del total representan.
>
> Pero otras variables no indican grupos.
>
> Indican **cantidades**, como edad u horas de estudio.
>
> ¿Cómo deberíamos describir ese tipo de variable?

La transición termina ahí.

M7 NO introduce todavía:

- histogramas;
- media;
- mediana;
- centro;
- dispersión;
- desviación estándar.

# Retención esperada después de una semana

## Comprensión
Debe explicar:

> una variable es categórica por lo que representan sus valores, no por si aparecen como texto o números.

Debe reconocer:

> un número puede ser un código de categoría.

## Producción
Con poca ayuda debe poder producir:

```r
table(variable)
```

y:

```r
prop.table(tabla)
```

## Interpretación
Debe distinguir:

```text
frecuencia
→ cuántos casos

proporción
→ qué parte del total

porcentaje
→ proporción expresada sobre 100
```

Debe preguntarse por el denominador de una proporción.

## Herramienta funcional
Puede requerir recordatorio para:

```r
barplot()
```

Eso es aceptable.

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 3
- PRÁCTICA: 1
- PRÁCTICA / VISUALIZACIÓN FUNCIONAL: 1
- TRANSFERENCIA: 1

## Porcentaje local de gran novedad
3 de 6 = 50 %.

Esto es compatible con el diseño global porque:

- el criterio de ≤40 % se aplica al recorrido completo;
- E5 contiene solo una micro-novedad funcional;
- cada pantalla mantiene una sola gran unidad de aprendizaje;
- E4 practica;
- E6 transfiere.

## Trayectoria de habilidades

```text
table()
encuentro M7-E2
→ práctica M7-E4
→ producción M7-E6
→ recuperación M12-E1
→ transferencia M13

prop.table()
encuentro M7-E3
→ práctica M7-E4
→ producción M7-E6
→ recuperación M12-E2
→ transferencia M13

barplot()
encuentro M7-E5
→ nivel funcional
```

## Habilidades nucleares consolidadas relativamente
- categórica por significado;
- frecuencia;
- proporción;
- denominador;
- frecuencia vs proporción;
- proporción vs porcentaje;
- `table()`;
- `prop.table()`;
- interpretación de una distribución categórica.

## Habilidad funcional
- `barplot()`.

## Habilidades pospuestas
- formalización de variables cuantitativas;
- histograma;
- media;
- mediana;
- dispersión;
- desviación estándar;
- factores;
- niveles;
- contingencia;
- Chi-cuadrado.

## Riesgos de sobrecarga controlados
- E1 no contiene sintaxis;
- E2 mantiene una sola función nueva;
- E3 reutiliza `tabla_carrera`;
- E4 no introduce sintaxis;
- E5 entrega el código;
- E6 no introduce sintaxis nueva y cambia solo el contexto.

## Checkpoint
No.

M7 no contiene checkpoint formal.

E6 funciona como transferencia intramódulo.

# Contrato de datos

## `encuesta_social_demo`
M7 preserva exactamente el contrato locked de M6.

No añade nuevas columnas a `encuesta_social_demo`.

E2–E5 utilizan `carrera`, que no contiene missing.

## `encuesta_campus`
La base de transferencia de E6 queda fijada pedagógicamente como:

```text
id   transporte
1    Metro
2    Bus
3    Bicicleta
4    Metro
5    A pie
6    Bus
7    Metro
8    Bicicleta
```

Cualquier implementación futura debe preservar estos valores o actualizar deliberadamente el Markdown locked y sus outputs/graders.

# Declaración de lock

M7 queda pedagógicamente cerrado con 6 ejercicios.

- **Sintaxis nuclear introducida:** `table()`, `prop.table()`.
- **Habilidad funcional:** `barplot()`.
- **Conceptos nucleares:** variable categórica por significado, frecuencia, proporción, denominador y porcentaje como expresión de una proporción.
- **Producción final:** `table()` + `prop.table()` autónomos sobre una base nueva.
- **Habilidades pospuestas:** descriptivos cuantitativos, factores, contingencia e inferencia categórica.
- **Recuperación futura:** M12 recupera `table()`/`prop.table()`; M13 exige elegir la ruta categórica.
- **Puente a M8:** categorías ya descritas → ahora surge la necesidad de describir cantidades.

# M7 PEDAGOGICALLY LOCKED
