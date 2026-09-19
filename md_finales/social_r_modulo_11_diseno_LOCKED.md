# Social R — Módulo 11
## Trabajar con varias correlaciones

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede analizar e interpretar una relación entre dos variables y elegir el coeficiente apropiado para ese par.

### Capacidad después
Puede preparar varias variables, construir y leer una matriz de correlaciones, distinguir diagonal, simetría y pares únicos, comprender cómo cambia la muestra analítica cuando hay missing por pares, interpretar una correlación entre una variable binaria 0/1 y una cuantitativa, y utilizar la matriz para localizar un par sustantivamente relevante que luego evalúa con `cor.test()`.

### Pregunta central
¿Cómo organizo e interpreto varias relaciones sin contar dos veces la misma información ni olvidar qué casos utiliza cada correlación?

### Modelo mental
```text
UNA RELACIÓN
↓
VARIAS VARIABLES
↓
SELECCIONAR
↓
TODAS LAS PAREJAS
↓
MATRIZ
↓
UNA CELDA = UN PAR
↓
DIAGONAL + SIMETRÍA
↓
PARES ÚNICOS
↓
MISSING
↓
MISMO N / DISTINTO N
↓
BINARIA + CUANTITATIVA
↓
PREGUNTA SUSTANTIVA
↓
PAR RELEVANTE
↓
cor.test()
↓
INTERPRETAR
```

### Principio conceptual central
M11 no enseña:

```text
MUCHAS VARIABLES
↓
MUCHOS NÚMEROS
```

Enseña:

```text
VARIAS VARIABLES
↓
TODOS SUS PARES
↓
UNA ESTRUCTURA PARA ORGANIZARLOS
```

Una matriz de correlaciones es una **representación de relaciones por pares**. No es una tabla mágica, no reemplaza mirar la forma de los pares y no es una matriz de tests.

### Habilidades nucleares
Al finalizar M11, el estudiante debe poder:

- seleccionar varias variables que responden a una pregunta sustantiva;
- excluir identificadores como `id` aunque estén almacenados numéricamente;
- comprender que varias variables generan varias combinaciones por pares;
- construir una matriz de correlaciones Pearson con `cor(dataframe, method = "pearson")`;
- leer una celda como la intersección de la variable de una fila y una columna;
- explicar por qué la diagonal vale 1;
- explicar por qué la matriz es simétrica;
- identificar los pares únicos sin contarlos dos veces;
- comprender que una matriz organiza coeficientes pero no muestra la forma de cada relación;
- comprender que una única matriz aplica el mismo método a todos los pares;
- reconocer que un par particular puede requerir volver a inspeccionar su forma;
- comprender `complete.obs` en contexto multivariado;
- comprender que `pairwise.complete.obs` puede usar N diferentes para distintos pares;
- interpretar el N de cada par cuando la plataforma lo hace visible;
- evitar la regla “pairwise es mejor porque usa más casos”;
- comprender que una variable 0/1 puede seguir siendo categórica;
- interpretar Pearson entre una binaria 0/1 y una cuantitativa como caso punto-biserial;
- comprender que invertir los códigos 0 y 1 invierte el signo y conserva `|r|`;
- evitar generalizar el caso 0/1 a códigos arbitrarios de tres o más categorías;
- utilizar una matriz para organizar el panorama y no para seleccionar post hoc “el r más grande”;
- identificar el par definido por una pregunta sustantiva;
- recuperar `cor.test()` para evaluar inferencialmente ese par;
- mantener separadas asociación e inferencia de causalidad.

### Habilidades funcionales
Son funcionales, no nucleares:

- recordar la cadena exacta `use = "pairwise.complete.obs"`;
- ejecutar dos matrices ya preparadas para comparar estrategias de missing;
- reconocer el término **correlación punto-biserial** después de comprender su significado;
- reconocer que `cor()` también puede producir matrices con otros métodos, aunque M11 utilice matrices Pearson.

### Habilidades recuperadas
M11 recupera:

- significado de variable;
- `select()`;
- `|>`;
- `$`;
- `NA`;
- pares completos;
- `use = "complete.obs"`;
- `cor()`;
- Pearson;
- `method = "pearson"`;
- `cor.test()`;
- magnitud;
- p-value;
- intervalo de confianza;
- correlación ≠ causalidad;
- número ≠ necesariamente cantidad.

### Habilidades pospuestas
No se introducen:

- `matrix()`;
- `diag()`;
- `upper.tri()`;
- `lower.tri()`;
- indexación matricial compleja;
- loops;
- `apply`;
- `pairs()`;
- matrices de p-values;
- `Hmisc::rcorr`;
- `psych::corr.test`;
- `corrplot`;
- heatmaps;
- clustering;
- correcciones por comparaciones múltiples;
- Bonferroni;
- FDR;
- teoría de matrices positivas semidefinidas;
- eigenvalues;
- recodificación productiva con `ifelse()`, `mutate()`, `recode()` o `case_when()`;
- fórmula manual del punto-biserial;
- equivalencia con t-test como objetivo curricular;
- tablas de contingencia;
- Chi-cuadrado;
- Cramér's V.

### Sintaxis nueva
Sintaxis productiva principal:

```r
cor(
  analisis,
  method = "pearson"
)
```

Sintaxis funcional nueva:

```r
use = "pairwise.complete.obs"
```

### Sintaxis recuperada
```r
select()
|>
cor()
cor.test()
$
```

También se recupera funcionalmente:

```r
use = "complete.obs"
```

### Sintaxis que NO se introduce
```text
matrix()
diag()
upper.tri()
lower.tri()
pairs()
complete.cases()
ifelse()
mutate()
recode()
case_when()
```

Tampoco se introducen `!`, `&`, loops ni herramientas especializadas de matrices.

### Contrato de datos — `encuesta_social`
M11 hereda sin modificar ninguna celda de M9:

```text
id   horas_estudio   puntaje_metodos   trabaja   horas_trabajo   horas_sueno
1    2               59                Sí        20              8.4
2    4               68                Sí        35              7.7
3    3               58                No        NA              8.0
4    6               64                Sí        25              7.6
5    5               62                Sí        40              7.6
6    8               75                No        NA              8.1
7    7               65                Sí        30              NA
8    10              64                Sí        45              7.1
9    9               74                No        NA              7.5
10   11              84                Sí        38              7.7
11   4               59                No        NA              7.9
12   6               73                Sí        32              7.4
```

M11 hereda sin modificar ninguna celda de M10:

```text
id   edad   horas_ocio
1    20     6.0
2    22     5.2
3    19     6.1
4    21     5.0
5    24     5.8
6    23     5.4
7    20     5.6
8    25     5.2
9    27     5.0
10   26     4.8
11   22     5.5
12   24     5.1
```

M11 añade y bloquea:

```text
id   trabaja_01   ingreso_miles
1    1            420
2    1            650
3    0            300
4    1            380
5    1            720
6    0            450
7    1            500
8    1            800
9    0            520
10   1            620
11   0            350
12   1            550
```

Contrato de `trabaja_01`:

```text
0 = No
1 = Sí
```

Debe coincidir exactamente con `trabaja`.

`ingreso_miles` representa ingreso personal mensual en miles de pesos y no contiene missing.

Desde M11, `trabaja_01` e `ingreso_miles` quedan locked.

### Identificadores
`id` contiene números, pero identifica casos. No representa una cantidad sustantiva que deba incluirse automáticamente en una matriz correlacional.

Modelo:

```text
NUMÉRICO EN R
≠
VARIABLE CUANTITATIVA RELEVANTE PARA LA PREGUNTA
```

### Política de matrices
Primer encuentro:

- exactamente 3 variables;
- exactamente una matriz 3×3;
- sin missing;
- Pearson explícito;
- matriz tratada como output para leer.

No se programa sobre la matriz.

### Política Pearson / Spearman
M11 utiliza matrices Pearson en los ejercicios nucleares.

Código explícito:

```r
cor(
  analisis,
  method = "pearson"
)
```

Nota pedagógica:

> `cor()` también puede construir matrices con otros métodos como Spearman. En este módulo usamos Pearson porque los pares seleccionados fueron diseñados para este tipo de resumen.

Una matriz aplica el mismo método a todos sus pares. Por ello:

```text
MATRIZ
≠
GARANTÍA DE QUE TODOS LOS PARES
TIENEN LA MISMA FORMA
```

Si un par concreto presenta una forma especial, debe volver a inspeccionarse individualmente.

### Política matriz / gráficos
```text
MATRIZ
→ ORGANIZA COEFICIENTES

SCATTERPLOT
→ MUESTRA LA FORMA
```

Por tanto:

```text
MATRIZ
≠
REEMPLAZO DE TODOS LOS GRÁFICOS
```

### Política de celda
```text
FILA
+
COLUMNA
↓
DOS VARIABLES
↓
UNA CORRELACIÓN
```

### Política de diagonal
```text
cor(x, x)
=
1
```

La diagonal compara cada variable consigo misma. Los `1` no constituyen relaciones sustantivas entre variables diferentes.

### Política de simetría
```text
cor(A, B)
=
cor(B, A)
```

Las dos mitades de la matriz repiten los mismos pares en orden inverso.

### Política de pares únicos
Con tres variables:

```text
A-B
A-C
B-C
```

hay 3 relaciones únicas entre variables distintas.

No se introduce fórmula combinatoria.

### Primera matriz contractual
Objeto:

```r
analisis <- encuesta_social |>
  select(
    edad,
    horas_estudio,
    horas_ocio
  )
```

Matriz Pearson:

```text
                    edad  horas_estudio  horas_ocio
edad            1.000000      0.758853    -0.692947
horas_estudio   0.758853      1.000000    -0.729961
horas_ocio     -0.692947     -0.729961     1.000000
```

Valores de referencia:

```text
edad × horas_estudio
= 0.7588525333

edad × horas_ocio
= -0.6929468984

horas_estudio × horas_ocio
= -0.7299614749
```

### Política de missing
E2–E3 trabajan sin missing.

E4 utiliza una microbase separada para que el missing no tenga el significado estructural de `horas_trabajo`.

E5–E6 vuelven a datos completos.

### Microbase E4 — `encuesta_seguimiento`
```text
caso   horas_estudio   horas_sueno   estres
1      2               8.1           3
2      4               7.4           5
3      3               NA            4
4      6               7.8           6
5      5               6.9           NA
6      8               7.2           8
7      7               6.5           5
8      10              NA            7
9      9               7.0           NA
10     6               7.6           4
```

`caso` es identificador y no entra en la matriz.

La plataforma preentrega:

```text
seguimiento
```

con solo:

```text
horas_estudio
horas_sueno
estres
```

### Política `complete.obs`
En una matriz:

```text
complete.obs
↓
SOLO FILAS COMPLETAS
EN TODAS LAS VARIABLES
↓
MISMA MUESTRA
PARA TODAS LAS CORRELACIONES
```

Casos completos en E4:

```text
1, 2, 4, 6, 7, 10
```

N común:

```text
6
```

### Matriz `complete.obs`
```text
                horas_estudio  horas_sueno   estres
horas_estudio      1.000000     -0.666358   0.776631
horas_sueno       -0.666358      1.000000  -0.384418
estres             0.776631     -0.384418   1.000000
```

Valores:

```text
estudio-sueno  = -0.6663582389
estudio-estres =  0.7766309483
sueno-estres   = -0.3844180472
```

### Política `pairwise.complete.obs`
Modelo:

```text
A-B
→ completos en A y B

A-C
→ completos en A y C

B-C
→ completos en B y C
```

Concepto nuclear:

```text
CADA PAR
PUEDE TENER
UN N DIFERENTE
```

La cadena sintáctica es funcional y puede necesitar recordatorio.

### N exacto por par
```text
estudio-sueno
N = 8

estudio-estres
N = 8

sueno-estres
N = 6
```

La plataforma debe hacer visible este N. El estudiante no programa una matriz de N.

### Matriz `pairwise.complete.obs`
```text
                horas_estudio  horas_sueno   estres
horas_estudio      1.000000     -0.602202   0.820768
horas_sueno       -0.602202      1.000000  -0.384418
estres             0.820768     -0.384418   1.000000
```

Valores:

```text
estudio-sueno  = -0.6022023190
estudio-estres =  0.8207677343
sueno-estres   = -0.3844180472
```

### Cautela pairwise
```text
MÁS CASOS UTILIZADOS
≠
AUTOMÁTICAMENTE MEJOR
```

Pairwise permite aprovechar pares disponibles, pero distintas celdas pueden representar grupos diferentes de personas. M11 no entra en propiedades algebraicas avanzadas de matrices pairwise.

### Política binaria 0/1
```text
VARIABLE BINARIA
↓
SIGUE SIENDO CATEGÓRICA
↓
CODIFICACIÓN 0/1
```

`trabaja_01` no es una cantidad de trabajo.

### Política punto-biserial
```text
BINARIA 0/1
+
CUANTITATIVA
↓
PEARSON
↓
CASO PUNTO-BISERIAL
```

La intuición se presenta antes que el nombre técnico.

### Contrato E5
```text
0 = No
1 = Sí
```

Con `ingreso_miles`:

```text
cor(trabaja_01, ingreso_miles)
= 0.5622172593
```

Medias:

```text
No trabaja
= 405

Sí trabaja
= 580
```

### Política de inversión 0/1
Codificación original:

```text
0 = No
1 = Sí
r = +0.5622172593
```

Codificación invertida:

```text
0 = Sí
1 = No
r = -0.5622172593
```

Por tanto:

```text
SIGNO
→ CAMBIA

|r|
→ SE MANTIENE
```

### Protección contra generalización
```text
1 = Norte
2 = Centro
3 = Sur
```

no convierte `zona_codigo` en una cantidad ni autoriza automáticamente Pearson.

### Política de inferencia
La matriz organiza coeficientes:

```text
cor(dataframe)
→ COEFICIENTES
```

No produce automáticamente:

```text
p-values
IC
tests
```

Para una pregunta inferencial sobre un par:

```r
cor.test(
  x,
  y,
  method = "pearson"
)
```

### Política de selección inferencial
No:

```text
MATRIZ
↓
BUSCAR r MÁS GRANDE
↓
TESTEARLO
```

Sí:

```text
PREGUNTA SUSTANTIVA PREESPECIFICADA
↓
MATRIZ ORGANIZA
↓
IDENTIFICAR EL PAR DE LA PREGUNTA
↓
cor.test()
```

### Contrato E6
Objeto:

```r
analisis_final <- encuesta_social |>
  select(
    trabaja_01,
    ingreso_miles,
    horas_ocio
  )
```

Matriz:

```text
                trabaja_01  ingreso_miles  horas_ocio
trabaja_01        1.000000      0.562217    -0.192051
ingreso_miles     0.562217      1.000000    -0.355722
horas_ocio       -0.192051     -0.355722     1.000000
```

Valores de referencia:

```text
trabaja_01 × ingreso_miles
= 0.5622172593

trabaja_01 × horas_ocio
= -0.1920506626

ingreso_miles × horas_ocio
= -0.3557215859
```

Pregunta focal:

> ¿Existe evidencia de asociación entre trabajar y las horas de ocio diario?

Test contractual:

```text
r = -0.1920506626
t = -0.6188371660
df = 10
p = 0.5498599414

95 % IC:
[-0.68991149,
  0.42915122]
```

### Estrategia de scaffolding
1. E1 recupera selección sustantiva.
2. E2 introduce la matriz con código completamente trabajado.
3. E3 enseña a leer estructura sin nueva sintaxis.
4. E4 entrega dos llamadas completas y centra la carga en missing/N.
5. E5 entrega un worked example conceptual para binaria + cuantitativa.
6. E6 retira nombres de funciones y exige la ruta integrada.

### Estrategia de fading
```text
E1
select incompleto
↓
E2
worked matrix
↓
E3
matriz dada
↓
E4
dos llamadas dadas
↓
E5
worked conceptual
↓
E6
comentarios mínimos
```

### Riesgos cognitivos
- incluir `id` porque es numérico;
- creer que una matriz 3×3 contiene 9 relaciones sustantivas;
- leer diagonal como hallazgo;
- contar A-B y B-A dos veces;
- interpretar signo negativo como “malo”;
- creer que una matriz reemplaza scatterplots;
- olvidar que una matriz aplica un mismo método a todos los pares;
- creer que `cor()` entrega p-values;
- suponer que todos los pares usan el mismo N bajo pairwise;
- creer que pairwise es automáticamente mejor;
- creer que 0/1 vuelve cuantitativa una variable;
- generalizar Pearson a códigos arbitrarios 1/2/3;
- olvidar que la codificación determina el signo del punto-biserial;
- seleccionar el mayor `r` y testearlo sin pregunta previa;
- interpretar p grande como prueba de H0;
- inferir causalidad.

### Número de ejercicios
6

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Dataset | Carga |
|---|---|---|---|---|---|
| M11-E1 | Elige las variables relevantes | RECUPERACIÓN | ninguna | `encuesta_social` | baja-media |
| M11-E2 | Varias relaciones a la vez | NOVEDAD | matriz de correlaciones | `analisis` | media |
| M11-E3 | No leas dos veces la misma relación | PRÁCTICA | ninguna | matriz E2 | baja-media |
| M11-E4 | No todos los pares usan los mismos casos | NOVEDAD | N por par / pairwise | `encuesta_seguimiento` | media-alta |
| M11-E5 | Cuando una variable tiene dos categorías | NOVEDAD | binaria 0/1 + cuantitativa | `encuesta_social` | media |
| M11-E6 | Lee una matriz para responder una pregunta | TRANSFERENCIA | ninguna | `encuesta_social` | media-alta |

---
## M11-E1 — Elige las variables relevantes

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
M11 necesita varias columnas antes de introducir una matriz, pero la preparación no debe convertirse en una novedad. E1 recupera `select()` dentro de una pregunta real y refuerza una distinción conceptual importante: una columna puede estar almacenada como números y aun así no ser una variable cuantitativa sustantiva para el análisis.

### 3. Capacidad antes
Puede seleccionar variables y comprende qué significa una variable cuantitativa.

### 4. Capacidad después
Puede preparar un data frame de tres variables cuantitativas relevantes para una pregunta y excluir un identificador numérico.

### 5. Prerrequisitos
`select()`, `|>`, objetos, significado de variable, `encuesta_social`.

### 6. Gran novedad
Ninguna gran novedad. La decisión recuperada es qué variables pertenecen realmente a la pregunta.

### 7. Recuperaciones
- `select()` de M5;
- pipe `|>`;
- “número ≠ necesariamente cantidad” de M7/M8;
- contrato de `encuesta_social`.

### 8. Contexto sustantivo
Queremos explorar conjuntamente cómo se relacionan la edad, las horas de estudio y las horas de ocio diario.

### 9. Dataset / objetos
Base: `encuesta_social`.

Variables solicitadas:

```text
edad
horas_estudio
horas_ocio
```

Objeto de salida:

```text
analisis
```

Debe contener 12 filas × 3 columnas.

### 10. Texto para estudiante
Queremos explorar conjuntamente tres características de las personas de `encuesta_social`:

- edad;
- horas de estudio;
- horas de ocio diario.

Prepara un objeto llamado `analisis` que conserve únicamente esas tres variables.

Fíjate en que `id` también contiene números. Sin embargo, esos números solo identifican personas: **no representan una cantidad que queramos relacionar**.

### 11. Modelo mental
```text
PREGUNTA
↓
¿QUÉ VARIABLES RESPONDEN A ESA PREGUNTA?
↓
SELECCIONAR
↓
DEJAR FUERA IDENTIFICADORES
```

### 12. Representación / código trabajado
No se entrega la solución completa. La estructura del pipe y `select()` ya son habilidades previas.

### 13. Starter code
```r
analisis <- encuesta_social |>
  select(
    # elige las tres variables relevantes
  )
```

### 14. Acción esperada
Completar `select()` con `edad`, `horas_estudio` y `horas_ocio`, ejecutar y consultar el objeto si necesita verificarlo.

### 15. Solución canónica
```r
analisis <- encuesta_social |>
  select(
    edad,
    horas_estudio,
    horas_ocio
  )
```

### 16. Resultado esperado
Un data frame con:

```text
12 filas
3 columnas

edad
horas_estudio
horas_ocio
```

No debe contener `id`.

### 17. Criterio semántico de éxito
Comprobar:

- existe `analisis`;
- depende de `encuesta_social`;
- tiene 12 filas;
- tiene exactamente las 3 variables solicitadas;
- no incluye `id`;
- no reconstruye manualmente los datos.

### 18. Estrategias alternativas válidas
Se acepta un objeto equivalente con las tres columnas en otro orden si la tarea semántica está satisfecha. La solución canónica mantiene el orden de la pregunta.

### 19. Error esperado / misconception
- incluir `id` porque “también es numérico”;
- añadir columnas no solicitadas;
- construir manualmente un data frame;
- seleccionar por posición en lugar de por variables sustantivas.

### 20. Feedback correcto
> Bien. Preparaste exactamente las tres variables relevantes y dejaste fuera `id`, que identifica casos pero no representa una cantidad sustantiva.

### 21. Feedback resultado correcto / estrategia incorrecta
Si reconstruye manualmente:

> El objeto final coincide, pero queremos que siga dependiendo de `encuesta_social`. Recupera `select()` para que el análisis se actualice si cambian los datos.

Si incluye `id`:

> `id` contiene números, pero esos números identifican personas. No representan una cantidad sustantiva que queramos correlacionar.

### 22. Hint 1
> ¿Qué tres características aparecen explícitamente en la pregunta?

### 23. Hint 2
> Recupera `select()` para conservar únicamente las columnas necesarias.

### 24. Hint 3
```r
analisis <- encuesta_social |>
  select(
    edad,
    horas_estudio,
    horas_ocio
  )
```

### 25. Predicción
No se requiere una fase separada.

### 26. Tipo de ejercicio
Recuperación productiva.

### 27. Andamiaje
Medio. La estructura está dada, pero las variables deben recuperarse y decidirse.

### 28. Carga cognitiva
Baja-media. Interactúan pregunta, selección, significado de variable y exclusión de un identificador.

### 29. Fading
E1 entrega estructura parcial; E2 entrega el nuevo comando completo; E6 retirará las funciones.

### 30. Recuperación futura
E6 y M13.

### 31. Riesgo de aprendizaje superficial
Tratar toda columna numérica como candidata automática a correlación.

### 32. Criterio de transferencia
Puede preparar otro conjunto de variables solicitado sustantivamente sin incluir identificadores por su apariencia numérica.

### 33. Notas de implementación futura
El grader debe inspeccionar columnas y dependencia de la base, no comparar código literal. Si el orden de columnas no es objetivo, no penalizarlo.

---

## M11-E2 — Varias relaciones a la vez

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Hasta ahora `cor()` resumía un solo par. E2 introduce una representación para organizar todas las correlaciones entre varias variables sin ejecutarlas una por una.

### 3. Capacidad antes
Dispone de `analisis` con tres variables cuantitativas completas y sabe interpretar Pearson para un par.

### 4. Capacidad después
Puede producir una matriz Pearson 3×3 y comprender que cada celda combina una variable de una fila con una variable de una columna.

### 5. Prerrequisitos
E1, `cor()`, Pearson, filas/columnas, idea de par.

### 6. Gran novedad
```text
VARIAS VARIABLES
↓
TODAS LAS PAREJAS
↓
MATRIZ DE CORRELACIONES
```

La gran novedad no es meramente que `cor()` acepte un data frame: es entender qué representa el resultado.

### 7. Recuperaciones
`cor()` y `method = "pearson"` de M9–M10.

### 8. Contexto sustantivo
Edad, horas de estudio y horas de ocio diario.

### 9. Dataset / objetos
Objeto:

```text
analisis
```

con:

```text
edad
horas_estudio
horas_ocio
```

Sin missing.

### 10. Texto para estudiante
Con un par de variables obteníamos un solo coeficiente.

Ahora tenemos tres variables.

Antes de ejecutar, predice:

> Si cada variable aparece como fila y como columna, ¿cuántas filas y columnas esperas en el resultado?

Después ejecuta el ejemplo.

No intentes interpretar todavía todas las celdas. Primero aprende qué representa **una** celda.

### 11. Modelo mental
```text
3 VARIABLES
↓
TODAS LAS COMBINACIONES POR PARES
↓
MATRIZ 3 × 3

FILA
+
COLUMNA
↓
UN PAR
↓
UN COEFICIENTE
```

### 12. Representación / código trabajado
Representación previa:

```text
                    edad   horas_estudio   horas_ocio
edad
horas_estudio
horas_ocio
```

Destacar conceptualmente:

```text
fila edad
+
columna horas_estudio
↓
cor(edad, horas_estudio)
```

Código:

```r
cor(
  analisis,
  method = "pearson"
)
```

### 13. Starter code
```r
cor(
  analisis,
  method = "pearson"
)
```

### 14. Acción esperada
Predecir 3×3, ejecutar el código y localizar al menos una celda a partir de sus nombres de fila y columna.

### 15. Solución canónica
```r
cor(
  analisis,
  method = "pearson"
)
```

### 16. Resultado esperado
```text
                    edad  horas_estudio  horas_ocio
edad            1.000000      0.758853    -0.692947
horas_estudio   0.758853      1.000000    -0.729961
horas_ocio     -0.692947     -0.729961     1.000000
```

Valores de referencia:

```text
edad-estudio = 0.7588525333
edad-ocio = -0.6929468984
estudio-ocio = -0.7299614749
```

### 17. Criterio semántico de éxito
Comprobar:

- usa `analisis`;
- usa Pearson;
- produce matriz 3×3;
- valores correctos;
- reconoce que una celda representa un par;
- no interpreta la matriz como p-values;
- no hardcoding.

### 18. Estrategias alternativas válidas
`cor(analisis)` produce los mismos coeficientes porque Pearson es el default, pero la solución pedagógicamente preferida explicita `method = "pearson"`. Una solución alternativa puede aceptarse si el estudiante identifica correctamente el método.

### 19. Error esperado / misconception
- creer que 9 celdas son 9 relaciones sustantivas;
- creer que los 1 son los hallazgos principales;
- creer que la matriz contiene p-values;
- asumir que la matriz muestra la forma de las relaciones;
- interpretar filas como casos.

### 20. Feedback correcto
> Bien. La matriz organiza correlaciones entre variables: cada celda combina la variable de una fila con la de una columna.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe manualmente una matriz:

> Los números coinciden, pero la matriz debe derivarse de `analisis`.

Si afirma que es una tabla de tests:

> `cor()` está mostrando coeficientes. No aparecen aquí p-values ni intervalos.

### 22. Hint 1
> Piensa en una tabla donde las mismas tres variables aparecen en filas y columnas.

### 23. Hint 2
> La intersección entre una fila y una columna corresponde a una pareja de variables.

### 24. Hint 3
```r
cor(
  analisis,
  method = "pearson"
)
```

### 25. Predicción
> Con tres variables, el resultado tendrá 3 filas y 3 columnas.

### 26. Tipo de ejercicio
Worked example + ejecución/observación.

### 27. Andamiaje
Alto. El código está completamente entregado.

### 28. Carga cognitiva
Media. Interactúan tres variables, pares, filas, columnas, matriz y método ya conocido.

### 29. Fading
E2 entrega la llamada. E3 elimina código nuevo y exige leer la estructura.

### 30. Recuperación futura
E3, E6 y M13.

### 31. Riesgo de aprendizaje superficial
Aprender `cor(dataframe)` como truco sin comprender qué representa cada celda.

### 32. Criterio de transferencia
Puede mirar una matriz con otros nombres de variables y localizar qué dos variables corresponden a una celda.

### 33. Notas de implementación futura
Resaltar visualmente una fila y una columna para mostrar la intersección. No introducir heatmaps ni `pairs()` como habilidad.

---

## M11-E3 — No leas dos veces la misma relación

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Una matriz 3×3 puede parecer contener nueve relaciones. E3 enseña por qué la diagonal y la simetría reducen la información sustantiva a tres pares únicos.

### 3. Capacidad antes
Puede producir una matriz y leer una celda como un par.

### 4. Capacidad después
Puede explicar diagonal y simetría, identificar tres pares únicos y evitar contar dos veces la misma relación.

### 5. Prerrequisitos
E2, `cor(A,B)`, significado de Pearson.

### 6. Gran novedad
Ninguna gran sintaxis nueva. Es práctica estructural de la representación recién introducida.

### 7. Recuperaciones
Idea de par de M9 y magnitud/signo de Pearson.

### 8. Contexto sustantivo
La misma matriz `edad`–`horas_estudio`–`horas_ocio`.

### 9. Dataset / objetos
Se utiliza el output de E2 sin modificar datos ni introducir objetos nuevos.

### 10. Texto para estudiante
La matriz tiene nueve celdas, pero no contiene nueve relaciones diferentes.

Obsérvala y responde:

1. ¿Por qué los tres valores de la diagonal son 1?
2. ¿Por qué `edad × horas_estudio` aparece en dos posiciones?
3. ¿Cuántas relaciones distintas existen entre las tres variables?
4. Entre esos pares únicos, ¿cuál tiene mayor `|r|`?
5. ¿Eso lo convierte automáticamente en el par “más importante” para una investigación?

### 11. Modelo mental
```text
DIAGONAL
→ VARIABLE CONSIGO MISMA
→ 1

A-B
=
B-A
→ MISMA RELACIÓN
→ MATRIZ SIMÉTRICA

3 VARIABLES
→ 3 PARES ÚNICOS
```

### 12. Representación / código trabajado
Usar la matriz de E2 y, en la interfaz futura, resaltar:

- diagonal;
- un par sobre la diagonal;
- su reflejo debajo de la diagonal.

No introducir nuevo código.

### 13. Starter code
No se requiere starter code. El objeto de trabajo es la matriz ya producida.

### 14. Acción esperada
Explicar diagonal y simetría, listar los tres pares únicos y comparar sus magnitudes sin convertir esa comparación en ranking de importancia.

### 15. Solución canónica
```text
Diagonal:
edad-edad
estudio-estudio
ocio-ocio
→ 1

Pares únicos:
edad-estudio
edad-ocio
estudio-ocio

Total:
3
```

Magnitudes:

```text
|edad-estudio| ≈ 0.759
|edad-ocio| ≈ 0.693
|estudio-ocio| ≈ 0.730
```

Mayor `|r|`:

```text
edad-estudio
```

Pero:

```text
MAYOR |r|
≠
MÁS IMPORTANTE AUTOMÁTICAMENTE
```

### 16. Resultado esperado
Comprende que las 9 celdas contienen 3 diagonales y 6 celdas fuera de diagonal que representan 3 pares repetidos.

### 17. Criterio semántico de éxito
Comprobar:

- diagonal = variable consigo misma;
- diagonal = 1;
- A-B = B-A;
- identifica simetría;
- lista 3 pares únicos;
- identifica correctamente mayor `|r|`;
- no interpreta signo negativo como “malo”;
- no equipara mayor `|r|` con importancia sustantiva.

### 18. Estrategias alternativas válidas
Puede leer el triángulo superior o inferior. No se exige una mitad específica porque ambas contienen los mismos pares.

### 19. Error esperado / misconception
- 9 relaciones diferentes;
- 6 relaciones fuera de diagonal;
- diagonal = relaciones perfectas importantes;
- A-B y B-A son hallazgos diferentes;
- r negativo = peor relación;
- mayor |r| = variable más importante.

### 20. Feedback correcto
> Exacto. La diagonal compara cada variable consigo misma y la matriz repite cada par a ambos lados de la diagonal. Por eso solo hay tres pares únicos.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice “ignoro la mitad porque sí”:

> La estrategia práctica funciona, pero necesitamos la razón: `cor(A,B)` y `cor(B,A)` representan el mismo par.

Si elige el mayor `|r|` como “más importante”:

> Ese par tiene mayor magnitud observada, pero la importancia depende de la pregunta de investigación, no solo del tamaño del coeficiente.

### 22. Hint 1
> Mira primero qué variable aparece en la fila y cuál en la columna.

### 23. Hint 2
> ¿Qué ocurre cuando fila y columna contienen la misma variable? ¿Y qué cambia entre A-B y B-A?

### 24. Hint 3
> La diagonal vale 1; fuera de ella, cuenta A-B solo una vez aunque también aparezca como B-A.

### 25. Predicción
> Antes de contar las celdas, ¿cuántos pares diferentes crees que pueden formarse con tres variables?

### 26. Tipo de ejercicio
Interpretación estructural.

### 27. Andamiaje
Medio. La matriz está visible; el estudiante produce la explicación.

### 28. Carga cognitiva
Baja-media. Interactúan diagonal, simetría y pares únicos.

### 29. Fading
Se retira el código nuevo y se exige comprender la representación.

### 30. Recuperación futura
E6 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar “lee solo un triángulo” sin comprender por qué.

### 32. Criterio de transferencia
Puede identificar pares únicos en otra matriz pequeña aunque cambien nombres y orden de variables.

### 33. Notas de implementación futura
La interfaz puede sombrear diagonal y reflejar un par con una línea o animación, pero el sombreado es apoyo visual, no contenido de R.

---

## M11-E4 — No todos los pares usan los mismos casos

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Cuando una matriz contiene missing, la elección de estrategia cambia qué personas participan en cada coeficiente. E4 hace visible ese problema sin introducir programación adicional.

### 3. Capacidad antes
Comprende matriz, pares únicos y pares completos en análisis bivariado.

### 4. Capacidad después
Puede explicar la diferencia entre eliminación por casos completos y eliminación por pares, leer el N usado en cada par y reconocer que pairwise no es automáticamente superior.

### 5. Prerrequisitos
E2–E3, M6 missing, M9 pares completos, `use = "complete.obs"` funcional.

### 6. Gran novedad
Concepto nuclear:

```text
PAIRWISE
→ CADA PAR PUEDE USAR CASOS DIFERENTES
→ N PUEDE CAMBIAR
```

Sintaxis funcional:

```r
use = "pairwise.complete.obs"
```

### 7. Recuperaciones
`NA`, casos completos y `use = "complete.obs"`.

### 8. Contexto sustantivo
Seguimiento de horas de estudio, horas de sueño y estrés. Se usa una microbase separada para que los `NA` no tengan el significado estructural de `horas_trabajo`.

### 9. Dataset / objetos
Microbase visible:

```text
caso   horas_estudio   horas_sueno   estres
1      2               8.1           3
2      4               7.4           5
3      3               NA            4
4      6               7.8           6
5      5               6.9           NA
6      8               7.2           8
7      7               6.5           5
8      10              NA            7
9      9               7.0           NA
10     6               7.6           4
```

La plataforma preentrega `seguimiento` con solo las tres variables analíticas.

### 10. Texto para estudiante
Ahora sí aparecen datos ausentes.

Compararemos dos formas de construir la matriz.

Primera:

> conservar únicamente las filas completas en **todas** las variables.

Segunda:

> para cada pareja, utilizar los casos que tienen datos en **esas dos** variables.

Antes de mirar los coeficientes, céntrate en una pregunta:

> ¿todos los pares estarán usando las mismas personas?

Ejecuta ambos ejemplos y utiliza la tabla de N que aparece junto al resultado.

### 11. Modelo mental
```text
complete.obs
↓
FILA COMPLETA EN TODAS
↓
MISMO N PARA TODOS LOS PARES

pairwise.complete.obs
↓
CADA PAR REVISA SUS DOS VARIABLES
↓
N PUEDE CAMBIAR ENTRE PARES
```

### 12. Representación / código trabajado
Worked comparison:

```r
cor(
  seguimiento,
  use = "complete.obs",
  method = "pearson"
)
```

y:

```r
cor(
  seguimiento,
  use = "pairwise.complete.obs",
  method = "pearson"
)
```

Junto a pairwise, mostrar:

| Par | N |
|---|---:|
| estudio–sueño | 8 |
| estudio–estrés | 8 |
| sueño–estrés | 6 |

### 13. Starter code
```r
cor(
  seguimiento,
  use = "complete.obs",
  method = "pearson"
)

cor(
  seguimiento,
  use = "pairwise.complete.obs",
  method = "pearson"
)
```

### 14. Acción esperada
Ejecutar ambas llamadas, comparar N y matrices, y explicar por qué pairwise puede usar muestras diferentes para cada celda.

### 15. Solución canónica
No hay producción sintáctica autónoma. La solución consiste en ejecutar las llamadas dadas e interpretar correctamente:

```text
complete.obs
→ N común = 6

pairwise:
estudio-sueno → N = 8
estudio-estres → N = 8
sueno-estres → N = 6
```

### 16. Resultado esperado
Complete:

```text
                horas_estudio  horas_sueno   estres
horas_estudio      1.000000     -0.666358   0.776631
horas_sueno       -0.666358      1.000000  -0.384418
estres             0.776631     -0.384418   1.000000
```

Pairwise:

```text
                horas_estudio  horas_sueno   estres
horas_estudio      1.000000     -0.602202   0.820768
horas_sueno       -0.602202      1.000000  -0.384418
estres             0.820768     -0.384418   1.000000
```

N:

```text
complete → 6 para todos
pairwise → 8, 8, 6
```

### 17. Criterio semántico de éxito
Comprobar:

- complete usa las 6 filas completas en todas las variables;
- pairwise usa N=8, N=8 y N=6 según el par;
- comprende por qué los coeficientes pueden cambiar;
- entiende que dos celdas pairwise pueden describir conjuntos distintos de personas;
- no interpreta NA como 0;
- no afirma que pairwise sea automáticamente mejor.

### 18. Estrategias alternativas válidas
Se acepta una explicación apoyada en la tabla visible o señalando directamente las filas disponibles. No se requiere calcular N con código.

### 19. Error esperado / misconception
- complete elimina missing por separado para cada par;
- pairwise usa “todos los casos” para todos los pares;
- todos los coeficientes de una matriz usan siempre el mismo N;
- pairwise siempre es mejor;
- los `NA` se convierten en 0;
- comparar directamente coeficientes sin advertir diferencias de muestra.

### 20. Feedback correcto
> Bien. Con pairwise cada relación puede estar calculada sobre un conjunto distinto de casos. Por eso el N forma parte del contexto necesario para leer la matriz.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice “pairwise es mejor porque usa 8”:

> Pairwise puede aprovechar más casos en algunos pares, pero también hace que diferentes coeficientes se basen en personas distintas. “Más casos” no resuelve automáticamente qué estrategia es preferible.

Si intenta usar `complete.cases()`:

> No necesitamos nueva sintaxis para esta pantalla. La tabla de N ya hace visible qué casos entran en cada par.

### 22. Hint 1
> Mira qué filas tienen datos disponibles para cada pareja.

### 23. Hint 2
> `complete.obs` exige que la fila esté completa en todas las variables seleccionadas.

### 24. Hint 3
> `pairwise.complete.obs` revisa cada pareja por separado, así que el N puede cambiar entre celdas.

### 25. Predicción
> ¿Esperas que `pairwise.complete.obs` utilice necesariamente el mismo N para todos los pares? No.

### 26. Tipo de ejercicio
Worked comparison + interpretación.

### 27. Andamiaje
Muy alto. Las dos llamadas están dadas y la plataforma muestra los N.

### 28. Carga cognitiva
Media-alta. Interactúan missing, tres variables, tres pares, dos estrategias y N; por eso no se exige producción sintáctica.

### 29. Fading
La sintaxis pairwise queda funcional; E6 no la recupera para evitar sobrecarga.

### 30. Recuperación futura
M13 puede recuperar el principio “revisa qué casos entran”, aunque no necesariamente la cadena exacta.

### 31. Riesgo de aprendizaje superficial
Memorizar “pairwise usa más datos” como criterio de elección universal.

### 32. Criterio de transferencia
Puede mirar otra matriz con missing y preguntar qué casos/N sustentan cada coeficiente antes de compararlos.

### 33. Notas de implementación futura
No introducir propiedades de matrices positivas semidefinidas. Esa cautela queda para el instructor. La plataforma debe hacer visible N por par sin exigir nueva programación.

---

## M11-E5 — Cuando una variable tiene dos categorías

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
El curso ya enseñó que una categoría puede estar codificada con números. E5 muestra un caso especial relevante: una categórica con exactamente dos grupos codificada 0/1 puede participar en Pearson con una cuantitativa sin dejar de ser categórica.

### 3. Capacidad antes
Distingue significado de almacenamiento/codificación y conoce Pearson.

### 4. Capacidad después
Puede interpretar una correlación punto-biserial, explicar el papel de la codificación y prever qué ocurre al invertir 0 y 1.

### 5. Prerrequisitos
M7 categorías, M9 Pearson, signo/magnitud, M11 lectura de correlación.

### 6. Gran novedad
```text
BINARIA 0/1
+
CUANTITATIVA
↓
PEARSON
↓
CASO PUNTO-BISERIAL
```

La etiqueta técnica aparece después de construir la intuición.

### 7. Recuperaciones
“Número ≠ necesariamente cantidad” y Pearson.

### 8. Contexto sustantivo
Trabajar (Sí/No) e ingreso personal mensual.

### 9. Dataset / objetos
Variables locked nuevas:

```text
trabaja_01
0 = No
1 = Sí
```

```text
ingreso_miles
420, 650, 300, 380, 720, 450, 500, 800, 520, 620, 350, 550
```

Medias:

```text
No trabaja = 405
Sí trabaja = 580
```

La interfaz puede preentregar `trabaja_invertido` solo para la demostración de inversión:

```text
0 = Sí
1 = No
```

### 10. Texto para estudiante
`trabaja_01` contiene números:

```text
0 = No
1 = Sí
```

Pero esos números siguen representando **dos categorías**.

No existe una “cantidad de trabajar” igual a 0 o 1.

Ahora relacionaremos esta variable con `ingreso_miles`.

Antes de ejecutar:

> Si `1 = Sí` y quienes trabajan tienen en promedio ingresos más altos, ¿qué signo esperarías?

Ejecuta Pearson y después observa qué ocurre cuando intercambiamos el significado de 0 y 1.

Solo al final nombraremos este caso especial.

### 11. Modelo mental
```text
DOS CATEGORÍAS
↓
CODIFICACIÓN 0/1
↓
SIGUE SIENDO CATEGÓRICA

BINARIA 0/1
+
CUANTITATIVA
↓
PEARSON

DESPUÉS:
CASO PUNTO-BISERIAL
```

### 12. Representación / código trabajado
Primero:

```r
cor(
  encuesta_social$trabaja_01,
  encuesta_social$ingreso_miles,
  method = "pearson"
)
```

Después, con una codificación invertida preentregada:

```r
cor(
  trabaja_invertido,
  encuesta_social$ingreso_miles,
  method = "pearson"
)
```

### 13. Starter code
```r
cor(
  encuesta_social$trabaja_01,
  encuesta_social$ingreso_miles,
  method = "pearson"
)
```

### 14. Acción esperada
Predecir signo, ejecutar, interpretar el coeficiente, comparar con la codificación invertida y explicar por qué `|r|` se conserva.

### 15. Solución canónica
Codificación original:

```text
0 = No
1 = Sí
r = +0.5622172593
```

Invertida:

```text
0 = Sí
1 = No
r = -0.5622172593
```

Conclusión:

```text
signo cambia
|r| se mantiene
```

Nombre técnico posterior:

> correlación punto-biserial.

### 16. Resultado esperado
```text
r = 0.5622172593
```

y:

```text
r_invertido = -0.5622172593
```

Interpretación sustantiva:

> Con `1 = Sí`, los ingresos más altos aparecen relativamente más entre quienes trabajan; en esta muestra el grupo que trabaja tiene media 580 y el grupo que no trabaja media 405.

### 17. Criterio semántico de éxito
Comprobar:

- `trabaja_01` se clasifica como categórica binaria;
- comprende 0/1 como códigos;
- Pearson correcto;
- r correcto;
- signo interpretado respecto del grupo 1;
- inversión produce signo contrario;
- magnitud absoluta igual;
- reconoce el término punto-biserial;
- no generaliza a tres categorías;
- no causalidad.

### 18. Estrategias alternativas válidas
Puede explicar el coeficiente comparando los grupos o hablando del grupo codificado 1. No necesita utilizar la fórmula del punto-biserial.

### 19. Error esperado / misconception
- 1 significa “más trabajo”;
- 0/1 transforma la variable en cuantitativa;
- cualquier categórica numérica puede entrar en Pearson;
- signo positivo significa grupo “mejor”;
- signo negativo significa “mala” asociación;
- invertir código cambia la intensidad;
- confundir asociación con causalidad.

### 20. Feedback correcto
> Exacto. `trabaja_01` sigue representando dos grupos. Pearson resume aquí la relación entre pertenecer al grupo codificado 1 y los valores de la variable cuantitativa; este caso se conoce como punto-biserial.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice que `trabaja_01` es cuantitativa:

> Los números son códigos de dos categorías. La variable no representa “cuánto trabaja” una persona.

Si interpreta el signo sin mencionar codificación:

> El signo depende de cuál grupo ocupa el código 1. Si invertimos 0 y 1, el signo también se invierte.

Si generaliza a `1=Norte, 2=Centro, 3=Sur`:

> Allí los números son códigos arbitrarios de tres categorías. El valor 3 no significa “más zona” que 1.

### 22. Hint 1
> Pregunta primero qué significa `0` y qué significa `1`.

### 23. Hint 2
> Compara qué grupo tiene, en promedio, valores más altos de ingreso.

### 24. Hint 3
> Con `1 = Sí`, valores mayores de ingreso asociados relativamente al grupo Sí producirán un coeficiente positivo.

### 25. Predicción
> Con `1 = Sí` y mayor ingreso promedio entre quienes trabajan, esperamos signo positivo.

### 26. Tipo de ejercicio
Worked example conceptual.

### 27. Andamiaje
Alto. La llamada se entrega; la dificultad está en significado y codificación.

### 28. Carga cognitiva
Media. Interactúan variable categórica, código 0/1, Pearson, signo y nuevo nombre técnico.

### 29. Fading
E5 entrega el análisis; E6 incorpora la binaria en una tarea integrada sin explicar nuevamente toda la lógica.

### 30. Recuperación futura
E6 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar “0/1 = Pearson” sin comprender que es un caso especial de una variable verdaderamente dicotómica.

### 32. Criterio de transferencia
Puede interpretar otra variable binaria 0/1 con una cuantitativa y adaptar el signo a la codificación.

### 33. Notas de implementación futura
No enseñar a recodificar. `trabaja_invertido` puede ser objeto preparado solo para demostrar la inversión. Mostrar también `zona_codigo` como contraejemplo de 3 categorías.

---

## M11-E6 — Lee una matriz para responder una pregunta

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
E6 integra preparación, matriz, lectura, caso binario e inferencia, pero evita missing para que la transferencia no se convierta en una acumulación excesiva de decisiones.

### 3. Capacidad antes
Puede preparar variables, construir/leer una matriz, comprender binaria + cuantitativa y utilizar `cor.test()` para un par.

### 4. Capacidad después
Puede usar una matriz como herramienta de organización dentro de una pregunta sustantiva y realizar inferencia sobre el par preespecificado sin seleccionar post hoc el coeficiente más grande.

### 5. Prerrequisitos
E1–E5 y M10.

### 6. Gran novedad
Ninguna. El ejercicio integra habilidades previas.

### 7. Recuperaciones
- `select()`;
- `|>`;
- `cor()`;
- matriz;
- pares únicos;
- binaria 0/1;
- Pearson;
- `cor.test()`;
- p-value;
- IC;
- causalidad.

### 8. Contexto sustantivo
Trabajo, ingreso y horas de ocio. La pregunta inferencial está definida antes de mirar qué correlación tiene mayor magnitud.

### 9. Dataset / objetos
Variables completas:

```text
trabaja_01
ingreso_miles
horas_ocio
```

Pregunta focal:

> ¿Existe evidencia de asociación entre trabajar y las horas de ocio diario?

Par focal:

```text
trabaja_01 × horas_ocio
```

### 10. Texto para estudiante
Queremos estudiar conjuntamente:

- trabajar;
- ingreso;
- horas de ocio.

Además tenemos una pregunta específica:

> **¿Existe evidencia de asociación entre trabajar y las horas de ocio diario?**

Haz lo siguiente:

1. prepara las tres variables;
2. organiza sus correlaciones;
3. localiza en la matriz el par que responde a la pregunta;
4. evalúa inferencialmente ese par;
5. interpreta magnitud, evidencia e incertidumbre;
6. explica qué no permite concluir el análisis.

La pregunta ya está definida antes de mirar la matriz. No elijas un par solo porque tenga el coeficiente más grande.

### 11. Modelo mental
```text
PREGUNTA PREESPECIFICADA
↓
SELECCIONAR VARIABLES
↓
MATRIZ
↓
ORGANIZAR EL PANORAMA
↓
UBICAR PAR DE LA PREGUNTA
↓
cor.test()
↓
r + p + IC
↓
INTERPRETAR
↓
NO CAUSALIDAD
```

### 12. Representación / código trabajado
No se muestra solución completa antes de intentar. La matriz aparece únicamente después de ejecutar el código del estudiante.

### 13. Starter code
```r
# prepara las variables relevantes


# organiza sus correlaciones


# evalúa el par que responde a la pregunta
```

### 14. Acción esperada
Preparar `analisis_final`, producir la matriz Pearson, identificar `trabaja_01 × horas_ocio`, ejecutar `cor.test()` y producir una interpretación completa.

### 15. Solución canónica
```r
analisis_final <- encuesta_social |>
  select(
    trabaja_01,
    ingreso_miles,
    horas_ocio
  )

cor(
  analisis_final,
  method = "pearson"
)

cor.test(
  encuesta_social$trabaja_01,
  encuesta_social$horas_ocio,
  method = "pearson"
)
```

### 16. Resultado esperado
Matriz:

```text
                trabaja_01  ingreso_miles  horas_ocio
trabaja_01        1.000000      0.562217    -0.192051
ingreso_miles     0.562217      1.000000    -0.355722
horas_ocio       -0.192051     -0.355722     1.000000
```

Test focal:

```text
r = -0.1920506626
t = -0.6188371660
df = 10
p = 0.5498599414

95 % IC:
[-0.68991149,
  0.42915122]
```

Interpretación modelo:

> La asociación observada entre trabajar y las horas de ocio es pequeña y negativa con `1 = Sí`. En esta muestra, quienes trabajan presentan ligeramente menos horas de ocio. El p-value es relativamente grande, por lo que los datos siguen siendo compatibles con el escenario nulo de correlación poblacional igual a cero. El intervalo es amplio e incluye valores negativos, cercanos a cero y positivos. El análisis no demuestra causalidad.

### 17. Criterio semántico de éxito
**Preparación**
- tres variables correctas;
- depende de `encuesta_social`.

**Matriz**
- 3×3;
- Pearson;
- coeficientes correctos.

**Pregunta focal**
- identifica `trabaja_01` y `horas_ocio`;
- no selecciona el mayor `r`.

**Inferencia**
- `cor.test()`;
- Pearson;
- r ≈ -0.1920507;
- p ≈ 0.5498599;
- IC ≈ [-0.6899115, 0.4291512].

**Interpretación**
- asociación pequeña;
- signo referido a `1 = Sí`;
- no p = probabilidad de H0;
- no “no existe relación”;
- no causalidad;
- no hardcoding.

### 18. Estrategias alternativas válidas
Puede crear objetos intermedios para el par focal o ejecutar un `cor()` adicional antes de `cor.test()`. La matriz puede tener las columnas en otro orden si contiene exactamente las tres variables y la interpretación localiza correctamente el par.

### 19. Error esperado / misconception
- testear `trabaja_01 × ingreso_miles` solo porque tiene mayor |r|;
- creer que la matriz ya incluye p-values;
- usar pairwise sin missing;
- concluir “no hay relación” porque p > .05;
- decir que H0 es verdadera;
- interpretar signo negativo como valoración;
- olvidar la codificación 0/1;
- causalidad;
- hardcoding.

### 20. Feedback correcto
> Bien. Utilizaste la matriz para organizar el panorama, pero la pregunta sustantiva —no el tamaño del coeficiente— determinó qué par debía evaluarse inferencialmente.

### 21. Feedback resultado correcto / estrategia incorrecta
Si testea el mayor `r`:

> La matriz permite comparar descriptivamente varios pares, pero la pregunta inferencial ya estaba definida. Debes evaluar `trabaja_01 × horas_ocio`.

Si dice “no existe asociación”:

> Un p relativamente grande no demuestra que la correlación poblacional sea exactamente cero. Describe los datos como compatibles con ese escenario y reporta también el coeficiente y el intervalo.

### 22. Hint 1
> ¿Qué dos variables aparecen explícitamente en la pregunta inferencial?

### 23. Hint 2
> La matriz organiza todas las relaciones, pero el test debe aplicarse al par que responde a esa pregunta.

### 24. Hint 3
```r
cor.test(
  encuesta_social$trabaja_01,
  encuesta_social$horas_ocio,
  method = "pearson"
)
```

### 25. Predicción
No hay fase separada. Identificar el par focal antes de ejecutar `cor.test()` cumple la función de decisión previa.

### 26. Tipo de ejercicio
Transferencia integrada.

### 27. Andamiaje
Medio-bajo. Solo permanecen comentarios estructurales y hints escalonadas.

### 28. Carga cognitiva
Media-alta. Integra selección, matriz, binaria, pregunta e inferencia; missing se excluye deliberadamente.

### 29. Fading
Máximo fading de M11: las funciones no se nombran en la consigna y el par debe derivarse de la pregunta.

### 30. Recuperación futura
M13 y evaluación objetivo.

### 31. Riesgo de aprendizaje superficial
Convertir la matriz en un dispositivo de búsqueda de “la correlación ganadora” y testear después de mirar los resultados.

### 32. Criterio de transferencia
Puede recibir otra pregunta con tres variables, organizar la matriz y aplicar inferencia únicamente al par sustantivamente definido.

### 33. Notas de implementación futura
El grader debe distinguir el par testado de los otros pares. No penalizar una consulta adicional de la matriz. No introducir correcciones múltiples ni matriz de p-values.

---

# Retención esperada después de una semana

## Debe comprender sin ayuda
Debe poder explicar:

> una matriz organiza correlaciones entre pares de variables.

Debe comprender:

```text
CELDA
→ fila + columna
→ un par
```

```text
DIAGONAL
→ variable consigo misma
→ 1
```

```text
SIMETRÍA
→ A-B = B-A
```

```text
3 VARIABLES
→ 3 PARES ÚNICOS
```

Debe comprender:

> una matriz no reemplaza mirar la forma de una relación.

Debe comprender:

```text
complete.obs
→ misma muestra para todos los coeficientes
```

```text
pairwise
→ cada par puede tener N diferente
```

Debe comprender:

```text
0/1
→ puede seguir siendo categórica
```

Debe comprender:

```text
binaria 0/1 + cuantitativa
→ Pearson
→ caso punto-biserial
```

Debe recordar:

```text
invertir 0/1
→ cambia signo
→ conserva |r|
```

Debe comprender:

```text
MATRIZ
≠
TABLA DE p-VALUES
```

y:

```text
MAYOR r
≠
PAR QUE DEBO TESTEAR AUTOMÁTICAMENTE
```

## Debe producir con poca ayuda
```r
analisis <- base |>
  select(var1, var2, var3)

cor(
  analisis,
  method = "pearson"
)
```

Debe recuperar para un par concreto:

```r
cor.test(
  x,
  y,
  method = "pearson"
)
```

## Puede requerir recordatorio sintáctico
```r
use = "pairwise.complete.obs"
```

Eso es aceptable porque su nivel es funcional.

## No esperamos que recuerde todavía
- programación matricial;
- `upper.tri()` / `lower.tri()`;
- matrices de p-values;
- correcciones múltiples;
- `pairs()`;
- paquetes especializados;
- fórmula del punto-biserial;
- propiedades algebraicas de matrices pairwise.

# Cierre conceptual M11 → M12

Cerrar exactamente con:

> Ya podemos organizar varias correlaciones entre cantidades
> y también vimos un caso especial:
> una variable categórica con **dos grupos**, codificada como 0/1,
> puede relacionarse con una cantidad mediante Pearson.
>
> Pero esa situación dependía de que una de las variables
> siguiera siendo cuantitativa.
>
> **¿Qué hacemos cuando las dos variables representan categorías?**

Detenerse ahí.

No introducir todavía:

```r
table(x, y)
chisq.test()
```

Ni:

- tabla de contingencia;
- porcentajes condicionales;
- independencia;
- observado/esperado;
- Chi-cuadrado;
- Cramér's V.

# Auditoría interna del lock

## Conteo por rol
- RECUPERACIÓN: 1
- NOVEDAD: 3
- PRÁCTICA: 1
- TRANSFERENCIA: 1

## Porcentaje local de novedad
3 de 6 = 50 %.

Se mantiene porque el control de novedad del curso es global y el plan maestro permanece en 39.8 % de novedad.

## Trayectoria de matriz
```text
E1
preparar 3 variables
↓
E2
primer encuentro matriz
↓
E3
leer diagonal/simetría/pares únicos
↓
E4
comprender N y missing
↓
E6
usar matriz dentro de una pregunta
```

## Trayectoria de missing
```text
M6
NA
↓
M9
pares completos
↓
M11-E4
complete vs pairwise
↓
N por par
```

## Trayectoria binaria
```text
M7
número ≠ necesariamente cantidad
↓
M11-E5
0/1 sigue siendo categórica
↓
Pearson
↓
punto-biserial
↓
M11-E6
recuperación integrada
```

## Trayectoria inferencial
```text
M10
cor.test()
↓
M11-E6
pregunta preespecificada
↓
par focal
↓
cor.test()
```

# Control técnico verificado

Los cálculos del contrato fueron reproducidos con las mismas fórmulas estadísticas que utiliza Pearson y contrastados con la documentación oficial de `stats::cor` y `stats::cor.test`.

## E2
```text
edad-estudio
= 0.7588525333

edad-ocio
= -0.6929468984

estudio-ocio
= -0.7299614749
```

## E4 complete
```text
N común
= 6

estudio-sueno
= -0.6663582389

estudio-estres
= 0.7766309483

sueno-estres
= -0.3844180472
```

## E4 pairwise
```text
N:
8
8
6

estudio-sueno
= -0.6022023190

estudio-estres
= 0.8207677343

sueno-estres
= -0.3844180472
```

## E5
```text
cor(trabaja_01, ingreso_miles)
= 0.5622172593
```

Codificación invertida:

```text
= -0.5622172593
```

Medias:

```text
No trabaja = 405
Sí trabaja = 580
```

## E6
Matriz:

```text
trabaja_01 × ingreso_miles
= 0.5622172593

trabaja_01 × horas_ocio
= -0.1920506626

ingreso_miles × horas_ocio
= -0.3557215859
```

Test focal:

```text
r = -0.1920506626
t = -0.6188371660
df = 10
p = 0.5498599414

95 % IC:
[-0.68991149,
  0.42915122]
```

La evaluación futura debe utilizar tolerancia numérica y no comparar strings redondeados.

# Declaración de lock

M11 queda pedagógicamente cerrado con 6 ejercicios.

- **Sintaxis nuclear:** `cor(dataframe, method = "pearson")`.
- **Sintaxis funcional nueva:** `use = "pairwise.complete.obs"`.
- **Sintaxis recuperada:** `select()`, `|>`, `cor()`, `cor.test()`, `$`, `use = "complete.obs"`.
- **Matriz:** celda = par; diagonal = variable consigo misma; simetría = par repetido; tres variables = tres pares únicos.
- **Matrices vs gráficos:** la matriz organiza coeficientes y no reemplaza examinar la forma.
- **Missing:** `complete.obs` mantiene una misma muestra; pairwise puede cambiar N por par.
- **Pairwise:** herramienta funcional, no recomendación universal.
- **Binaria:** 0/1 puede seguir siendo categórica.
- **Punto-biserial:** Pearson entre binaria 0/1 y cuantitativa.
- **Codificación:** invertir 0/1 invierte signo y conserva `|r|`.
- **E6:** matriz para organizar + pregunta preespecificada + `cor.test()` del par focal.
- **Contrato de datos:** M11 añade `trabaja_01` e `ingreso_miles`.
- **Recuperación futura:** M13.
- **Puente M12:** binaria + cuantitativa → dos categóricas.

# M11 PEDAGOGICALLY LOCKED
