# Social R — Módulo 13
## De la pregunta al análisis

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Posición curricular
M13 es el último módulo del curso. No introduce nueva estadística, nuevos procedimientos ni nueva sintaxis analítica. Su función es integrar y transferir lo aprendido en M1–M12.

### Puente M12 → M13
M12 termina con:

> Ya aprendimos rutas diferentes según el tipo de variables y la pregunta:
> describir una variable,
> relacionar dos cantidades
> o estudiar la asociación entre categorías.
>
> Hasta ahora, cada módulo nos indicó qué familia de problema estábamos trabajando.
>
> Pero en una investigación real nadie nos dice de antemano
> qué función debemos ejecutar.
>
> **¿Cómo pasamos de una pregunta nueva**
> **a una estrategia completa de análisis?**

M13 comienza exactamente desde esa necesidad.

### Capacidad antes
Puede resolver procedimientos por familia con apoyo decreciente y distinguir descripción, asociación cuantitativa, asociación categórica, magnitud, evidencia e incertidumbre.

### Capacidad después
Puede recibir una pregunta y una base nuevas, identificar variables y tipos, preparar los datos pertinentes, revisar missing, elegir una estrategia entre las familias trabajadas, ejecutar el análisis de manera reproducible e interpretar el resultado sin exceder la evidencia.

### Pregunta central
> Frente a una pregunta nueva, ¿cómo decido qué datos necesito, qué análisis corresponde y qué significa el resultado?

### Modelo mental nuclear
```text
PREGUNTA
↓
¿QUÉ QUIERO SABER?
↓
VARIABLES
↓
¿QUÉ REPRESENTAN SUS VALORES?
↓
CASOS PERTINENTES
↓
MISSING RELEVANTE
↓
PREPARAR
↓
REPRESENTAR / DESCRIBIR
↓
ELEGIR FAMILIA
↓
ELEGIR MÉTODO
↓
EJECUTAR
↓
INTERPRETAR
↓
LIMITAR CONCLUSIONES
```

### Principio central
```text
APRENDER R
≠
MEMORIZAR FUNCIONES
```

La ruta final del curso es:

```text
PREGUNTA
→ DATOS
→ DECISIONES
→ ANÁLISIS
→ INTERPRETACIÓN
```

### Familias que M13 recupera
El mapa completo solo se muestra **después del primer intento de M13-E1**.

```text
UNA CATEGÓRICA
→ distribución categórica

UNA CUANTITATIVA
→ distribución / centro / dispersión

DOS CUANTITATIVAS
→ scatterplot
→ forma
→ Pearson / Spearman / ninguno

BINARIA 0/1 + CUANTITATIVA
→ Pearson punto-biserial

DOS CATEGÓRICAS
→ tabla
→ denominador
→ Chi-cuadrado
→ Cramér's V
```

### Política de novedad
M13 contiene **cero grandes novedades**.

```text
NOVEDAD = 0
PRÁCTICA = 0
RECUPERACIÓN = 1
INTEGRACIÓN = 1
TRANSFERENCIA = 3
```

Porcentaje local de gran novedad: **0 %**.

### Sintaxis recuperable
```r
<-
c()
[]
$
|>
>
==
filter()
select()
head()
str()
is.na()
sum()
table()
prop.table()
mean()
median()
sd()
hist()
plot()
cor()
cor.test()
chisq.test()
```

Parámetros/estrategias funcionales ya aprendidas:

```r
na.rm = TRUE
use = "complete.obs"
use = "pairwise.complete.obs"
method = "pearson"
method = "spearman"
```

Cramér's V continúa siendo calculado por la plataforma.

### Sintaxis que NO se introduce
```text
complete.cases()
ifelse()
mutate()
recode()
case_when()
group_by()
summarise()
arrange()
lm()
t.test()
aov()
fisher.test()
shapiro.test()
rank()
matrix()
diag()
rowSums()
colSums()
sqrt()
dim()
min()
```

No se introduce helper propio para Cramér's V ni paquete externo.

### Política de títulos
Los títulos internos mantienen la trazabilidad curricular.

Los títulos visibles no revelan de antemano la familia estadística.

| ID | Título interno | Título visible | Rol |
|---|---|---|---|
| M13-E1 | ¿Qué tipo de problema es? | ¿Qué camino seguir? | RECUPERACIÓN |
| M13-E2 | Prepara antes de analizar | Antes de analizar | INTEGRACIÓN |
| M13-E3 | Responde una pregunta cuantitativa | Estudio y autoeficacia | TRANSFERENCIA |
| M13-E4 | Responde una pregunta categórica | Movilidad y participación | TRANSFERENCIA |
| M13-E5 | Checkpoint E: nueva base, nueva pregunta | Checkpoint E — Participación y confianza | TRANSFERENCIA / CHECKPOINT |

### Política de hints
Todas las pistas están cerradas al inicio y se revelan una por una:

```text
HINT 1
→ concepto / pregunta

HINT 2
→ estructura / familia

HINT 3
→ sintaxis casi completa
```

Pedir una pista no invalida automáticamente el aprendizaje.

### Política de ejecución y evaluación
```text
Ctrl+Enter
→ ejecutar / explorar / observar

Comprobar respuesta
→ evaluar
```

La exploración razonable no se penaliza.

### Política de semantic grading
La implementación futura debe inspeccionar:

```text
PREGUNTA
+
VARIABLES
+
TIPOS
+
CASOS
+
PREPARACIÓN
+
MISSING
+
REPRESENTACIÓN
+
MÉTODO
+
OBJETOS
+
RESULTADOS
+
INTERPRETACIÓN
+
DEPENDENCIAS
```

No debe comparar strings literales de código.

### Dataset lock principal
Nombre:

```text
encuesta_vida_universitaria
```

Contexto:

> Encuesta sintética sobre experiencias y vida universitaria.

N = 48.

| Variable | Tipo conceptual | Rol | Missing |
|---|---|---|---:|
| `id` | identificador | no analítico | 0 |
| `jornada` | categórica | filtro | 0 |
| `horas_estudio` | cuantitativa | focal | 0 |
| `autoeficacia_academica` | cuantitativa | focal | 2 |
| `horas_sueno` | cuantitativa | recuperación/distractor | 4 |
| `transporte_campus` | categórica | focal | 0 |
| `participa_organizacion` | categórica binaria | focal | 0 |
| `trabaja_01` | categórica binaria codificada 0/1 | recuperación | 0 |

Contrato:

```text
trabaja_01
0 = No
1 = Sí
```

`id` nunca se trata como variable cuantitativa sustantiva.

### Datos exactos — `encuesta_vida_universitaria`
```text
id jornada     horas_estudio autoeficacia_academica horas_sueno transporte_campus participa_organizacion trabaja_01
1  Diurna      11.0          52.4                    8.0         Bus               No                    1
2  Diurna      16.0          69.2                    7.5         Bus               No                    1
3  Diurna      12.5          87.0                    7.8         Bus               Sí                    0
4  Diurna       3.5          36.6                    7.7         Activo            Sí                    1
5  Diurna      18.0          77.6                    7.4         Bus               Sí                    1
6  Diurna       4.0          62.9                    NA          Bus               No                    0
7  Diurna      17.5          87.0                    7.5         Metro             No                    1
8  Diurna      13.0          58.7                    7.6         Metro             Sí                    1
9  Diurna       7.5          61.8                    7.7         Bus               No                    0
10 Diurna       8.5          80.8                    7.1         Activo            No                    1
11 Diurna      15.5          87.1                    7.5         Bus               Sí                    1
12 Diurna      18.5          91.2                    7.4         Metro             Sí                    0
13 Diurna       6.0          62.9                    7.1         Activo            Sí                    1
14 Diurna       9.0          46.1                    7.6         Metro             No                    1
15 Diurna      15.0          73.4                    7.1         Metro             Sí                    0
16 Diurna       8.0          52.4                    7.3         Metro             Sí                    1
17 Diurna       5.0          71.3                    7.4         Metro             No                    1
18 Diurna      14.5          89.2                    6.8         Activo            Sí                    0
19 Diurna       3.0          58.7                    NA          Bus               No                    1
20 Diurna       9.5          74.4                    7.0         Bus               No                    1
21 Diurna      14.0          62.9                    6.8         Bus               No                    0
22 Diurna      16.5          91.2                    7.3         Activo            No                    1
23 Diurna       4.5          43.0                    6.8         Bus               No                    1
24 Diurna      10.5          74.4                    7.0         Metro             No                    0
25 Diurna      11.5          80.8                    7.0         Bus               No                    1
26 Diurna      13.5          76.6                    6.5         Activo            Sí                    1
27 Diurna      12.0          62.9                    6.9         Metro             No                    0
28 Diurna       5.5          36.6                    6.7         Activo            Sí                    1
29 Diurna       7.0          46.1                    6.5         Activo            Sí                    1
30 Diurna      17.0          62.9                    6.9         Bus               No                    0
31 Diurna      10.0          60.8                    6.5         Activo            Sí                    1
32 Diurna       6.5          72.4                    6.7         Metro             No                    1
33 Vespertina   5.0          52.0                    6.7         Bus               Sí                    0
34 Vespertina   7.5          61.0                    6.2         Bus               No                    1
35 Vespertina   4.5          49.0                    6.5         Metro             No                    1
36 Vespertina   9.0          68.0                    6.4         Metro             No                    0
37 Vespertina   6.0          NA                      NA          Bus               Sí                    1
38 Vespertina  10.5          72.0                    6.6         Activo            Sí                    1
39 Vespertina   8.0          64.0                    6.2         Bus               No                    0
40 Vespertina  12.0          76.0                    6.3         Bus               No                    1
41 Vespertina   5.5          54.0                    6.4         Activo            No                    1
42 Vespertina  11.0          73.0                    5.9         Metro             Sí                    0
43 Vespertina   7.0          59.0                    6.2         Metro             No                    1
44 Vespertina  13.0          NA                      NA          Bus               No                    1
45 Vespertina   6.5          58.0                    5.8         Metro             Sí                    0
46 Vespertina   9.5          69.0                    6.3         Activo            Sí                    1
47 Vespertina   8.5          66.0                    5.9         Metro             Sí                    1
48 Vespertina  14.0          82.0                    6.0         Bus               No                    0
```

Distribuciones contractuales:

```text
jornada:
Diurna = 32
Vespertina = 16

autoeficacia_academica:
NA en IDs 37 y 44 → 2

horas_sueno:
NA en IDs 6, 19, 37 y 44 → 4
```

El resto de las variables no contiene missing.

### Dataset lock del Checkpoint E
Nombre:

```text
encuesta_vinculos_barriales
```

Contexto:

> Encuesta sintética sobre trabajo, participación vecinal y confianza comunitaria.

N = 40.

| Variable | Tipo conceptual | Rol |
|---|---|---|
| `id` | identificador | distractor |
| `ocupado` | categórica | filtro |
| `participa_vecinal_01` | categórica binaria 0/1 | focal |
| `confianza_comunitaria` | cuantitativa | focal |
| `zona` | categórica | distractor |
| `minutos_traslado` | cuantitativa | distractor |
| `ingreso_miles` | cuantitativa | distractor |

Contrato:

```text
participa_vecinal_01
0 = No
1 = Sí
```

### Datos exactos — `encuesta_vinculos_barriales`
```text
id ocupado participa_vecinal_01 confianza_comunitaria zona        minutos_traslado ingreso_miles
1  Sí      0                    47                    Centro      25               700
2  Sí      1                    70                    Periferia   40               850
3  Sí      0                    48                    Rural       55               620
4  Sí      0                    63                    Centro      30               760
5  Sí      1                    55                    Periferia   45               910
6  Sí      0                    65                    Centro      35               680
7  Sí      1                    61                    Periferia   60               820
8  Sí      0                    52                    Rural       28               740
9  Sí      1                    53                    Centro      50               890
10 Sí      1                    64                    Periferia   42               650
11 Sí      0                    70                    Centro      33               780
12 Sí      1                    63                    Periferia   47               930
13 Sí      0                    45                    Rural       52               710
14 Sí      1                    67                    Centro      38               840
15 Sí      0                    61                    Periferia   58               600
16 Sí      0                    56                    Centro      26               770
17 Sí      0                    59                    Periferia   44               880
18 Sí      0                    50                    Rural       49               690
19 Sí      0                    67                    Centro      36               810
20 Sí      1                    76                    Periferia   54               950
21 Sí      1                    78                    Centro      31               720
22 Sí      1                    72                    Periferia   46               860
23 Sí      0                    54                    Rural       57               640
24 Sí      1                    59                    Centro      29               790
25 Sí      0                    58                    Periferia   43               900
26 Sí      1                    57                    Centro      39               730
27 Sí      1                    66                    Periferia   61               870
28 Sí      0                    55                    Rural       34               670
29 Sí      1                    69                    Centro      48               830
30 Sí      0                    42                    Periferia   53               920
31 No      0                    50                    Centro      27               NA
32 No      1                    62                    Periferia   41               450
33 No      0                    NA                    Rural       56               500
34 No      0                    48                    Centro      32               NA
35 No      1                    64                    Periferia   45               520
36 No      0                    55                    Centro      37               480
37 No      1                    60                    Periferia   59               550
38 No      0                    52                    Rural       30               470
39 No      0                    NA                    Centro      51               NA
40 No      1                    58                    Periferia   40               510
```

En la base completa:

```text
confianza_comunitaria:
2 NA, ambos entre personas no ocupadas

ingreso_miles:
3 NA, variable distractora
```

Después de filtrar `ocupado == "Sí"`, las dos variables focales del Checkpoint no contienen missing.

### Política de missing
M13 recupera:

```text
MISSING RELEVANTE AL ANÁLISIS
```

No:

```text
ELIMINAR TODOS LOS NA
```

La pregunta define primero qué casos y variables importan; después se revisa el missing pertinente.

### Política de descriptivos
Los descriptivos reaparecen en E1 como reconocimiento de familia. No se crea un nuevo ejercicio productivo descriptivo.

### Política de matrices
La matriz de correlaciones de M11 no reaparece como ruta principal. M13 prioriza pregunta focal → análisis focal.

### Política punto-biserial
Se recupera en E1 y se utiliza en Checkpoint E:

```text
VARIABLE BINARIA
↓
SIGUE SIENDO CATEGÓRICA
↓
CODIFICACIÓN 0/1
+
CUANTITATIVA
↓
PEARSON
↓
CASO PUNTO-BISERIAL
```

### Política de no causalidad
Debe aparecer explícitamente en E3, E4 y E5:

> Este análisis describe/evalúa una asociación; por sí solo no identifica un efecto causal.

### Número de ejercicios
5

### Mapa del módulo
| ID | Título visible | Rol | Gran novedad | Dataset | Carga |
|---|---|---|---|---|---|
| M13-E1 | ¿Qué camino seguir? | RECUPERACIÓN | ninguna | tarjetas / base principal | media |
| M13-E2 | Antes de analizar | INTEGRACIÓN | ninguna | `encuesta_vida_universitaria` | media |
| M13-E3 | Estudio y autoeficacia | TRANSFERENCIA | ninguna | `datos_estudio_diurno` | media-alta |
| M13-E4 | Movilidad y participación | TRANSFERENCIA | ninguna | `encuesta_vida_universitaria` | media-alta |
| M13-E5 | Checkpoint E — Participación y confianza | TRANSFERENCIA / CHECKPOINT | ninguna | `encuesta_vinculos_barriales` | alta por autonomía |

---
## M13-E1 — ¿Qué tipo de problema es?

**Título visible:** ¿Qué camino seguir?


### 1. Rol pedagógico
RECUPERACIÓN.


### 2. Por qué existe
M13 debe retirar la ayuda de los módulos anteriores, que ya indicaban la familia de problema. E1 recupera el mapa completo antes de pedir producción, pero obliga a decidir desde la pregunta y el significado de las variables, no desde palabras clave.


### 3. Capacidad antes
Conoce por separado las familias descriptivas, correlacionales, punto-biseriales y categóricas trabajadas en M7–M12.


### 4. Capacidad después
Puede identificar variables relevantes, clasificarlas conceptualmente, elegir una familia de análisis y justificar esa elección en cinco situaciones distintas.


### 5. Prerrequisitos
M1–M12 completos; especialmente tipos de variables, correlación, punto-biserial, tabla de contingencia y descriptivos.


### 6. Gran novedad
Ninguna. E1 es retrieval practice. No presenta una nueva familia ni una nueva función.


### 7. Recuperaciones
- una categórica;
- una cuantitativa;
- dos cuantitativas;
- binaria 0/1 + cuantitativa;
- dos categóricas;
- número ≠ necesariamente cantidad.


### 8. Contexto sustantivo
Cinco preguntas breves sobre vida universitaria, todas comprensibles sin conocimiento disciplinar adicional.


### 9. Dataset / objetos
Las tarjetas usan variables de `encuesta_vida_universitaria`. No se requiere manipular el data frame en este ejercicio. El mapa completo permanece oculto hasta el primer intento.


### 10. Texto para estudiante
En los módulos anteriores ya sabías qué familia de problema estabas practicando. Ahora queremos decidir a partir de la pregunta.

Para cada situación responde:

```text
Variables:
Tipo(s):
Familia:
¿Por qué?
```

**A.** Queremos describir cómo se distribuye el medio principal de transporte al campus.

**B.** Queremos describir el centro y la dispersión de las horas de sueño reportadas.

**C.** Entre estudiantes de jornada diurna, queremos saber si quienes dedican más horas semanales al estudio tienden a reportar mayor o menor autoeficacia académica.

**D.** Queremos saber si la participación en organizaciones estudiantiles se distribuye de la misma manera entre los distintos medios de transporte.

**E.** Queremos saber si trabajar —codificado `0 = No`, `1 = Sí`— se asocia con las horas de sueño.


### 11. Modelo mental
```text
PREGUNTA
↓
VARIABLES
↓
¿QUÉ REPRESENTAN?
↓
TIPOS
↓
FAMILIA DE ANÁLISIS
↓
JUSTIFICACIÓN
```


### 12. Representación / código trabajado
No hay código productivo. Después del primer intento puede mostrarse progresivamente:

```text
UNA CATEGÓRICA
→ distribución categórica

UNA CUANTITATIVA
→ distribución / centro / dispersión

DOS CUANTITATIVAS
→ mirar patrón antes de decidir Pearson/Spearman

DOS CATEGÓRICAS
→ tabla y asociación

BINARIA 0/1 + CUANTITATIVA
→ caso punto-biserial
```


### 13. Starter code
No aplica. La respuesta es conceptual y estructurada.


### 14. Acción esperada
Completar las cuatro partes de la respuesta para cada uno de los cinco escenarios.


### 15. Solución canónica
**A**
```text
Variable: transporte_campus
Tipo: categórica
Familia: descripción categórica
Razón: una sola variable categórica
```

**B**
```text
Variable: horas_sueno
Tipo: cuantitativa
Familia: descripción cuantitativa
Razón: queremos centro y dispersión de una cantidad
```

**C**
```text
horas_estudio → cuantitativa
autoeficacia_academica → cuantitativa
Familia: asociación entre dos cantidades
Razón: queremos estudiar cómo varían conjuntamente
```

No elegir Pearson/Spearman todavía sin mirar el patrón.

**D**
```text
transporte_campus → categórica
participa_organizacion → categórica
Familia: asociación entre dos categóricas
```

**E**
```text
trabaja_01 → categórica binaria 0/1
horas_sueno → cuantitativa
Familia: binaria + cuantitativa → Pearson punto-biserial
```


### 16. Resultado esperado
Cinco clasificaciones justificadas. No se exige escribir nombres exactos de funciones cuando la familia conceptual está correctamente identificada.


### 17. Criterio semántico de éxito
Para cada tarjeta comprobar:
- variables relevantes;
- tipo conceptual correcto;
- familia compatible;
- razón coherente;
- en C no selecciona Pearson/Spearman antes del gráfico;
- en E reconoce que `0/1` sigue representando categorías.


### 18. Estrategias alternativas válidas
Se aceptan expresiones equivalentes como “distribución de una categórica”, “descriptivos cuantitativos” o “relación entre dos cantidades”. La evaluación debe privilegiar el significado, no una etiqueta literal.


### 19. Error esperado / misconception
- “relación” = correlación automáticamente;
- cualquier variable numérica = cuantitativa;
- `0/1` = cantidad;
- elegir test por una palabra clave;
- decidir Pearson antes de observar la forma.


### 20. Feedback correcto
> Bien. Elegiste la ruta desde la pregunta y el significado de las variables, no desde el nombre de una función.


### 21. Feedback resultado correcto / estrategia incorrecta
Si responde solo “correlación” o “Chi²”:

> La familia puede coincidir, pero falta mostrar por qué: identifica las variables y qué representan sus valores.

Si clasifica `trabaja_01` como cuantitativa:

> Que una categoría esté almacenada como 0/1 no la convierte en una cantidad.


### 22. Hint 1
> Todavía no busques una función. Identifica primero qué variables necesita la pregunta y qué representan sus valores.


### 23. Hint 2
> Pregunta si tienes una variable o dos, y si sus valores representan categorías o cantidades.


### 24. Hint 3
> Usa el mapa de familias que aparece después del primer intento y compáralo con la combinación de tipos de cada escenario.


### 25. Predicción
No requiere ejecución. La predicción consiste en anticipar la familia antes de ver el mapa completo.


### 26. Tipo de ejercicio
Clasificación/decisión con retrieval practice.


### 27. Andamiaje
Medio-alto: estructura de respuesta visible; mapa de decisión oculto hasta el primer intento.


### 28. Carga cognitiva
Media. Cinco escenarios permiten recuperar todas las familias centrales sin convertir E1 en una evaluación extensa.


### 29. Fading
La estructura conceptual es explícita en E1; desde E2 disminuye la ayuda y comienza la producción.


### 30. Recuperación futura
Se recupera en E2–E5.


### 31. Riesgo de aprendizaje superficial
Usar el mapa como árbol mecánico sin leer la pregunta ni el significado de las variables.


### 32. Criterio de transferencia
Puede clasificar correctamente un escenario con nombres de variables distintos y justificar la ruta sin que la consigna nombre la función.


### 33. Notas de implementación futura
Las cinco tarjetas pueden presentarse una a una. Después del primer intento se habilita el mapa de decisión como apoyo. Perturbation test: cambiar el tipo conceptual o la formulación de una tarjeta debe cambiar la respuesta correcta. Las pistas permanecen cerradas y se abren de una en una.


---
## M13-E2 — Prepara antes de analizar

**Título visible:** Antes de analizar


### 1. Rol pedagógico
INTEGRACIÓN.


### 2. Por qué existe
Evita el patrón “pregunta → test”. Obliga a integrar filtro, selección y revisión de missing con una finalidad analítica explícita antes de ejecutar cualquier procedimiento estadístico.


### 3. Capacidad antes
Puede filtrar, seleccionar variables y revisar missing por separado.


### 4. Capacidad después
Puede preparar una muestra analítica definida por una pregunta, conservar solo las variables necesarias y comprobar el missing relevante.


### 5. Prerrequisitos
M4–M6, M13-E1, `filter()`, `select()`, `|>`, `$`, `is.na()` y `sum()`.


### 6. Gran novedad
Ninguna. Integra operaciones conocidas.


### 7. Recuperaciones
```text
PREGUNTA
→ CASOS
→ VARIABLES
→ MISSING
→ OBJETO PREPARADO
```


### 8. Contexto sustantivo
Estudio y autoeficacia académica en estudiantes de jornada diurna.


### 9. Dataset / objetos
Base:

```text
encuesta_vida_universitaria
N = 48
```

Objeto esperado:

```text
datos_estudio_diurno
```

con 32 filas y 2 columnas.


### 10. Texto para estudiante
En el siguiente ejercicio estudiaremos, **entre estudiantes de jornada diurna**, si las horas semanales de estudio se relacionan con el puntaje de autoeficacia académica.

Antes de analizar:

1. conserva únicamente los casos pertinentes;
2. conserva únicamente las variables necesarias;
3. revisa si esas variables tienen datos ausentes.

Todavía no realices el análisis estadístico.


### 11. Modelo mental
```text
PREGUNTA
↓
¿QUIÉNES ENTRAN?
↓
¿QUÉ VARIABLES NECESITO?
↓
PREPARAR
↓
¿HAY MISSING RELEVANTE?
↓
OBJETO LISTO
```


### 12. Representación / código trabajado
No se muestra la solución completa antes del intento. La interfaz puede recordar que el pipeline `|>` permite que una operación alimente a la siguiente.


### 13. Starter code
```r
# conserva únicamente los casos relevantes
# y las variables necesarias


# revisa si las variables del análisis
# tienen datos ausentes
```


### 14. Acción esperada
Filtrar jornada Diurna, seleccionar `horas_estudio` y `autoeficacia_academica`, guardar el objeto y contar missing de ambas variables.


### 15. Solución canónica
```r
datos_estudio_diurno <- encuesta_vida_universitaria |>
  filter(jornada == "Diurna") |>
  select(
    horas_estudio,
    autoeficacia_academica
  )

sum(is.na(datos_estudio_diurno$horas_estudio))

sum(is.na(datos_estudio_diurno$autoeficacia_academica))
```


### 16. Resultado esperado
```text
datos_estudio_diurno:
32 filas
2 columnas

missing:
horas_estudio = 0
autoeficacia_academica = 0
```

La base completa contiene dos `NA` en autoeficacia (IDs 37 y 44), pero ambos pertenecen a jornada Vespertina y no forman parte de la población analítica definida por la pregunta.


### 17. Criterio semántico de éxito
Comprobar:
- depende de `encuesta_vida_universitaria`;
- conserva exclusivamente `jornada == "Diurna"`;
- N final = 32;
- conserva exactamente las dos variables focales o un objeto semánticamente equivalente;
- missing focal = 0/0;
- no ejecuta todavía correlación/test;
- no hardcoding.


### 18. Estrategias alternativas válidas
Se acepta seleccionar antes y filtrar después si la estrategia produce exactamente la misma muestra y mantiene disponible `jornada` hasta completar el filtro. También se admite otro nombre de objeto.


### 19. Error esperado / misconception
- eliminar todos los `NA` de la base antes de leer la pregunta;
- mantener las 48 personas;
- seleccionar variables distractoras;
- ejecutar `cor.test()` antes de preparar;
- reconstruir manualmente los 32 valores.


### 20. Feedback correcto
> Bien. Primero definiste la población y las variables de la pregunta; después comprobaste el missing que realmente importa para este análisis.


### 21. Feedback resultado correcto / estrategia incorrecta
Si elimina filas por `horas_sueno`:

> Esa variable no forma parte de la pregunta. No debemos excluir casos por missing en una variable que este análisis no utiliza.

Si escribe manualmente una base de 32 filas:

> El resultado puede coincidir, pero debe depender de la base original para seguir funcionando si cambian los datos.


### 22. Hint 1
> ¿Qué parte de la pregunta indica qué personas deben entrar al análisis?


### 23. Hint 2
> Después de definir los casos, conserva solo `horas_estudio` y `autoeficacia_academica`.


### 24. Hint 3
```r
encuesta_vida_universitaria |>
  filter(jornada == "Diurna") |>
  select(
    horas_estudio,
    autoeficacia_academica
  )
```


### 25. Predicción
> ¿Esperas conservar las 48 personas? No: la pregunta restringe el análisis a jornada diurna.


### 26. Tipo de ejercicio
Integración de preparación de datos.


### 27. Andamiaje
Medio.


### 28. Carga cognitiva
Media: casos + variables + missing, sin análisis estadístico todavía.


### 29. Fading
E2 conserva comentarios estructurales. E3 recibe el objeto preparado y reduce la guía.


### 30. Recuperación futura
Se recupera en E3 y E5.


### 31. Riesgo de aprendizaje superficial
Aprender una secuencia fija `filter |> select` sin comprender que la pregunta define qué casos y variables conservar.


### 32. Criterio de transferencia
Puede preparar otra muestra analítica a partir de una pregunta nueva, incluso cuando los missing de la base completa no coincidan con los missing de la muestra pertinente.


### 33. Notas de implementación futura
Semantic grading debe inspeccionar población, variables, dimensiones y missing, no strings. Perturbation test: cambiar la jornada de un caso debe cambiar N; convertir un valor focal a `NA` debe cambiar el conteo. No penalizar `head()`/`str()` exploratorios.


---
## M13-E3 — Responde una pregunta cuantitativa

**Título visible:** Estudio y autoeficacia


### 1. Rol pedagógico
TRANSFERENCIA.


### 2. Por qué existe
Comprueba si el estudiante puede recuperar la ruta completa de dos cuantitativas sin que la consigna diga correlación, Pearson o Spearman.


### 3. Capacidad antes
Dispone de `datos_estudio_diurno`, reconoce tipos y conoce scatterplot, Pearson, Spearman y `cor.test()`.


### 4. Capacidad después
Puede representar dos cantidades, elegir Pearson desde la forma observada, ejecutar inferencia e interpretar patrón, magnitud, evidencia e incertidumbre.


### 5. Prerrequisitos
M9–M10 y M13-E2.


### 6. Gran novedad
Ninguna.


### 7. Recuperaciones
`plot()`, forma, Pearson/Spearman, `cor.test()`, p, IC, magnitud ≠ evidencia ≠ incertidumbre, asociación ≠ causalidad.


### 8. Contexto sustantivo
Horas de estudio y autoeficacia académica entre estudiantes de jornada diurna.


### 9. Dataset / objetos
```text
datos_estudio_diurno
N = 32
```

Variables:
`horas_estudio`, `autoeficacia_academica`.


### 10. Texto para estudiante
Entre estudiantes de jornada diurna, ¿quienes dedican más horas semanales al estudio tienden a reportar mayor o menor autoeficacia académica?

Construye una respuesta que:

1. represente conjuntamente las dos variables;
2. utilice la forma observada para decidir el método;
3. evalúe la asociación;
4. interprete el patrón, la magnitud, la evidencia y la incertidumbre;
5. indique qué no puedes concluir.


### 11. Modelo mental
```text
PREGUNTA
↓
DOS CANTIDADES
↓
SCATTERPLOT
↓
FORMA
↓
APROXIMADAMENTE LINEAL
↓
PEARSON
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
El scatterplot contractual debe describirse como:

```text
ascendente
+
aproximadamente lineal
+
dispersión moderada
+
sin curvatura monotónica dominante
+
sin un punto aislado que determine toda la asociación
```

Por eso Pearson es adecuado para resumir la asociación lineal en este caso.


### 13. Starter code
```r
# representa conjuntamente las dos variables


# elige un método a partir de la forma observada


# evalúa la asociación


# interpreta el resultado
```


### 14. Acción esperada
Generar scatterplot, describirlo, elegir Pearson, ejecutar `cor.test()` y redactar una interpretación prudente.


### 15. Solución canónica
```r
plot(
  datos_estudio_diurno$horas_estudio,
  datos_estudio_diurno$autoeficacia_academica
)

cor.test(
  datos_estudio_diurno$horas_estudio,
  datos_estudio_diurno$autoeficacia_academica,
  method = "pearson"
)
```


### 16. Resultado esperado
```text
N = 32

Pearson r = 0.6514835763
t = 4.7034371502
df = 30
p = 0.0000537600951

IC 95 %:
[0.3917924734,
 0.8150287693]
```

Referencia interna no evaluada:

```text
Spearman rho ≈ 0.6519683463
```

`cor()` previo es válido pero no obligatorio.


### 17. Criterio semántico de éxito
Comprobar:
- usa `datos_estudio_diurno`;
- representa las variables correctas;
- el gráfico aparece conceptualmente antes de la decisión;
- describe dirección/forma de manera compatible;
- elige Pearson por la forma, no solo por ser números;
- estimate/p/IC correctos con tolerancia;
- distingue magnitud/evidencia/incertidumbre;
- no causalidad;
- no hardcoding.


### 18. Estrategias alternativas válidas
`cor()` antes de `cor.test()` es válido pero redundante. Puede usar nombres de objetos distintos. Una justificación que describa claramente la linealidad observada es suficiente aunque no use la frase exacta “aproximadamente lineal”.


### 19. Error esperado / misconception
- dos numéricas → Pearson automáticamente;
- ejecutar coeficiente antes de mirar el gráfico;
- usar p como magnitud;
- interpretar r como porcentaje;
- interpretar el IC como rango de puntajes individuales;
- causalidad.


### 20. Feedback correcto
> Bien. La elección de Pearson está justificada por la forma aproximadamente lineal del patrón, y separaste coeficiente, p-value e incertidumbre.


### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene el mismo r sin gráfico:

> El número coincide, pero aquí la decisión de método también es parte del objetivo. Necesitamos observar la forma antes de justificar Pearson.

Si reporta solo p:

> El p-value no describe por sí solo la dirección ni la magnitud de la asociación.


### 22. Hint 1
> Antes de elegir un coeficiente, representa conjuntamente las dos variables.


### 23. Hint 2
> El patrón es ascendente y aproximadamente lineal; recupera el método que resume asociación lineal.


### 24. Hint 3
```r
plot(
  datos_estudio_diurno$horas_estudio,
  datos_estudio_diurno$autoeficacia_academica
)

cor.test(
  datos_estudio_diurno$horas_estudio,
  datos_estudio_diurno$autoeficacia_academica,
  method = "pearson"
)
```


### 25. Predicción
> Según el gráfico, ¿esperas una asociación positiva, negativa o cercana a cero? Positiva.


### 26. Tipo de ejercicio
Transferencia cuantitativa integrada.


### 27. Andamiaje
Bajo.


### 28. Carga cognitiva
Media-alta: gráfico + método + inferencia, sin missing adicional.


### 29. Fading
Solo comentarios generales; las funciones ya no se nombran en la consigna.


### 30. Recuperación futura
Sus principios inferenciales se recuperan en E5 mediante otra configuración.


### 31. Riesgo de aprendizaje superficial
Ejecutar Pearson como reflejo automático ante dos columnas numéricas.


### 32. Criterio de transferencia
Puede recibir otras dos cantidades, mirar primero la forma y elegir el método coherente sin que la consigna lo nombre.


### 33. Notas de implementación futura
Perturbation test: modificar varios valores de autoeficacia debe cambiar gráfico, r, p e IC. Grader debe tolerar redondeo. `t` y `df` pueden aparecer en output pero no necesitan una interpretación sustantiva nueva. No penalizar exploración adicional razonable.


---
## M13-E4 — Responde una pregunta categórica

**Título visible:** Movilidad y participación


### 1. Rol pedagógico
TRANSFERENCIA.


### 2. Por qué existe
Comprueba si el estudiante puede recuperar M12 completo sin que la consigna nombre tabla, porcentajes por fila, Chi-cuadrado o Cramér's V.


### 3. Capacidad antes
Reconoce dos categóricas y conoce tabla de contingencia, denominadores, expected, Chi-cuadrado y V.


### 4. Capacidad después
Puede derivar la orientación y el denominador desde una pregunta sustantiva, ejecutar el test, revisar expected y separar patrón, evidencia y magnitud.


### 5. Prerrequisitos
M12 completo y M13-E1.


### 6. Gran novedad
Ninguna.


### 7. Recuperaciones
`table(x,y)`, `prop.table(tabla,1)`, `chisq.test()`, `$expected`, independencia, p ≠ magnitud, Cramér's V, no causalidad.


### 8. Contexto sustantivo
Movilidad al campus y participación en organizaciones estudiantiles.


### 9. Dataset / objetos
Base completa:

```text
encuesta_vida_universitaria
N = 48
```

Variables sin missing:
`transporte_campus`, `participa_organizacion`.


### 10. Texto para estudiante
**Dentro de cada medio principal de transporte al campus**, ¿la participación en organizaciones estudiantiles se distribuye de la misma manera?

Construye una respuesta que:

1. organice conjuntamente las variables;
2. compare los grupos con el denominador que corresponde a la pregunta;
3. evalúe la asociación;
4. revise lo que esperaba el test;
5. distinga patrón, evidencia y magnitud;
6. indique qué no puedes concluir causalmente.


### 11. Modelo mental
```text
PREGUNTA
↓
DOS CATEGÓRICAS
↓
TABLA
↓
“DENTRO DE CADA TRANSPORTE”
↓
TRANSPORTE EN FILAS
↓
margin = 1
↓
CHI²
↓
EXPECTED
↓
p + V
↓
INTERPRETACIÓN
```


### 12. Representación / código trabajado
La orientación contractual es:

```text
filas → transporte_campus
columnas → participa_organizacion
```

La frase “dentro de cada medio de transporte” determina que cada fila sea su propio 100 %.


### 13. Starter code
```r
# organiza conjuntamente las variables


# compara los grupos usando el denominador
# que corresponde a la pregunta


# evalúa la asociación


# revisa qué esperaba el test
```


### 14. Acción esperada
Construir tabla, producir proporciones por fila, ejecutar Chi-cuadrado, revisar expected e interpretar Cramér's V calculado por la plataforma.


### 15. Solución canónica
```r
tabla_participacion <- table(
  encuesta_vida_universitaria$transporte_campus,
  encuesta_vida_universitaria$participa_organizacion
)

prop.table(
  tabla_participacion,
  1
)

prueba_participacion <- chisq.test(
  tabla_participacion
)

prueba_participacion

prueba_participacion$expected
```


### 16. Resultado esperado
Observed:

```text
         No  Sí
Activo    3   9
Bus      15   5
Metro     9   7
```

Row proportions:

```text
Activo   0.2500  0.7500
Bus      0.7500  0.2500
Metro    0.5625  0.4375
```

Expected:

```text
         No      Sí
Activo   6.75    5.25
Bus     11.25    8.75
Metro    9.00    7.00
```

Todos los expected son ≥5.

```text
χ² = 7.6190476190
df = 2
p = 0.0221587282
Cramér's V = 0.3984095364
```


### 17. Criterio semántico de éxito
Comprobar:
- dos variables correctas;
- transporte en filas;
- participación en columnas;
- tabla 3×2 correcta;
- `margin=1` o estrategia equivalente;
- porcentajes correctos;
- `chisq.test()` sobre conteos, no porcentajes;
- expected correctos y revisados;
- p y V separados;
- V no porcentaje ni signo;
- no causalidad;
- no hardcoding.


### 18. Estrategias alternativas válidas
Una tabla transpuesta es informativamente equivalente solo si el estudiante adapta correctamente el denominador y la interpretación. Para el contrato canónico se prefiere transporte en filas porque hace visible la frase “dentro de cada transporte”.


### 19. Error esperado / misconception
- codificar transporte 1/2/3 y correlacionar;
- usar porcentajes globales;
- usar `margin=2` sin cambiar la pregunta;
- aplicar `chisq.test()` a porcentajes;
- no revisar expected;
- p = magnitud;
- V con signo;
- causalidad.


### 20. Feedback correcto
> Bien. La pregunta determinó el denominador: comparaste dentro de cada transporte, revisaste expected y separaste porcentajes, p y V.


### 21. Feedback resultado correcto / estrategia incorrecta
Si usa una tabla de porcentajes dentro de `chisq.test()`:

> El test debe partir de los conteos observados. Los porcentajes sirven para interpretar el patrón.

Si reporta solo p:

> Falta describir cómo se distribuyen las categorías y separar evidencia de magnitud.


### 22. Hint 1
> ¿Qué dos variables responden la pregunta y qué representan sus valores?


### 23. Hint 2
> La frase “dentro de cada medio de transporte” te dice qué grupos deben sumar 100 %.


### 24. Hint 3
```text
table(...)
→ prop.table(..., 1)
→ chisq.test(...)
→ $expected
```


### 25. Predicción
> ¿Los porcentajes de participación “Sí” parecen iguales entre Activo, Bus y Metro? No.


### 26. Tipo de ejercicio
Transferencia categórica integrada.


### 27. Andamiaje
Bajo.


### 28. Carga cognitiva
Media-alta: denominador + inferencia + magnitud, sin missing adicional.


### 29. Fading
Comentarios mínimos; no se nombran las funciones en la consigna.


### 30. Recuperación futura
Cierra la ruta categórica; no tiene recuperación posterior dentro del núcleo.


### 31. Riesgo de aprendizaje superficial
Reconocer dos categóricas pero ejecutar mecánicamente Chi-cuadrado sin decidir denominador ni revisar expected.


### 32. Criterio de transferencia
Puede recibir otras dos categóricas y construir tabla, porcentajes, test e interpretación desde una pregunta sustantiva.


### 33. Notas de implementación futura
Cramér's V debe calcularse dinámicamente desde la tabla actual. Perturbation test: cambiar varias categorías de participación debe actualizar tabla, proporciones, χ², p y V. No introducir Yates: la tabla es 3×2. Grader debe tolerar orientación equivalente solo si el denominador y la interpretación son coherentes.


---
## M13-E5 — Checkpoint E: nueva base, nueva pregunta

**Título visible:** Checkpoint E — Participación y confianza


### 1. Rol pedagógico
TRANSFERENCIA / CHECKPOINT E.


### 2. Por qué existe
Es la evaluación final de transferencia de Social R: base nueva, pregunta nueva, variables distractoras y ninguna etiqueta que revele la familia analítica.


### 3. Capacidad antes
Ha completado E1–E4 y dispone de toda la arquitectura de decisión del curso.


### 4. Capacidad después
Puede construir autónomamente una estrategia reproducible en un contexto nuevo, desde la población analítica hasta la interpretación inferencial.


### 5. Prerrequisitos
M5, M6, M10, M11 y M13-E1–E4.


### 6. Gran novedad
Ninguna. La dificultad procede de decidir, integrar y justificar.


### 7. Recuperaciones
`filter()`, `select()`, missing relevante, variable binaria 0/1, Pearson punto-biserial, `cor.test()`, p, IC, no causalidad.


### 8. Contexto sustantivo
Trabajo, participación vecinal y confianza comunitaria.


### 9. Dataset / objetos
Base nueva:

```text
encuesta_vinculos_barriales
N = 40
```

Pregunta focal restringe la población a personas ocupadas.

Variables:
`ocupado`,
`participa_vecinal_01`,
`confianza_comunitaria`.


### 10. Texto para estudiante
**Entre las personas ocupadas**, ¿participar en una organización vecinal se asocia con el puntaje de confianza comunitaria?

En la base:

```text
participa_vecinal_01
0 = No
1 = Sí
```

Construye una respuesta completa. Decide qué casos y variables necesitas, revisa los datos ausentes relevantes, elige una estrategia conocida y explica qué puedes y qué no puedes concluir.


### 11. Modelo mental
```text
PREGUNTA
↓
PERSONAS OCUPADAS
↓
VARIABLES NECESARIAS
↓
0/1 = BINARIA CATEGÓRICA
+
CONFIANZA = CUANTITATIVA
↓
MISSING
↓
PEARSON PUNTO-BISERIAL
↓
cor.test()
↓
r + p + IC
↓
INTERPRETAR CÓDIGO 1
↓
NO CAUSALIDAD
```


### 12. Representación / código trabajado
No se entrega ejemplo resuelto antes del intento. Un gráfico exploratorio razonable es válido, pero no es requisito nuclear porque una de las variables es binaria y el objetivo de transferencia es reconocer la configuración punto-biserial ya aprendida.


### 13. Starter code
```r
# identifica los casos y variables necesarios


# prepara los datos


# revisa los datos ausentes relevantes


# analiza la pregunta


# interpreta qué puedes y qué no puedes concluir
```


### 14. Acción esperada
Filtrar ocupados, seleccionar las dos variables focales, revisar missing, reconocer la binaria 0/1, ejecutar Pearson como punto-biserial e interpretar r, p e IC.


### 15. Solución canónica
```r
datos_checkpoint <- encuesta_vinculos_barriales |>
  filter(ocupado == "Sí") |>
  select(
    participa_vecinal_01,
    confianza_comunitaria
  )

sum(is.na(datos_checkpoint$participa_vecinal_01))

sum(is.na(datos_checkpoint$confianza_comunitaria))

cor.test(
  datos_checkpoint$participa_vecinal_01,
  datos_checkpoint$confianza_comunitaria,
  method = "pearson"
)
```


### 16. Resultado esperado
```text
N total = 40
N ocupado = 30
N analítico = 30

missing focal:
participa_vecinal_01 = 0
confianza_comunitaria = 0

distribución:
0 = 16
1 = 14

medias descriptivas de referencia:
0 = No  → 55.75
1 = Sí  → 65.00

Pearson punto-biserial:
r = 0.5168168103
t = 3.1944285021
df = 28
p = 0.0034534621

IC 95 %:
[0.1923645585,
 0.7394124666]
```


### 17. Criterio semántico de éxito
Comprobar:
- filtra `ocupado == "Sí"`;
- N analítico = 30;
- selecciona las dos variables focales;
- reconoce `participa_vecinal_01` como categórica binaria;
- missing focal = 0/0;
- utiliza Pearson como punto-biserial;
- estimate/p/IC correctos con tolerancia;
- interpreta el signo considerando `1 = Sí`;
- no causalidad;
- depende de los datos;
- no hardcoding.


### 18. Estrategias alternativas válidas
Se aceptan otros nombres de objetos, `cor()` como exploración previa y gráficos exploratorios razonables. No se exige calcular las medias de grupos. La solución debe seguir siendo reproducible y responder exactamente a la población ocupada.


### 19. Error esperado / misconception
- usar las 40 personas;
- `0/1` = variable cuantitativa;
- reconstruir vectores manualmente;
- reportar solo p;
- ignorar la codificación del signo;
- interpretar r como porcentaje;
- causalidad.


### 20. Feedback correcto
> Bien. Definiste correctamente la población, reconociste la variable binaria pese a su codificación 0/1 y construiste una interpretación que separa asociación, evidencia e incertidumbre.


### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene el mismo r con vectores escritos manualmente:

> El valor coincide, pero el análisis debe depender de la base y del filtro para seguir funcionando si cambian los datos.

Si trata `participa_vecinal_01` como una cantidad:

> `0` y `1` identifican dos grupos. Pearson funciona aquí como el caso punto-biserial, no porque la variable se haya vuelto continua.


### 22. Hint 1
> Empieza por la población indicada en la pregunta. Después identifica qué representan realmente los valores de las variables focales.


### 23. Hint 2
> Una variable representa dos grupos codificados 0/1 y la otra es cuantitativa. Ya trabajaste esta combinación.


### 24. Hint 3
```r
datos_checkpoint <- encuesta_vinculos_barriales |>
  filter(ocupado == "Sí") |>
  select(
    participa_vecinal_01,
    confianza_comunitaria
  )

cor.test(
  datos_checkpoint$participa_vecinal_01,
  datos_checkpoint$confianza_comunitaria,
  method = "pearson"
)
```


### 25. Predicción
> Si el grupo codificado `1 = Sí` presenta en general puntajes mayores, ¿qué signo esperas? Positivo.


### 26. Tipo de ejercicio
Checkpoint de transferencia final.


### 27. Andamiaje
Muy bajo. Starter casi vacío y pistas solo a solicitud.


### 28. Carga cognitiva
Alta por autonomía, no por sintaxis nueva.


### 29. Fading
Máximo del curso: base nueva + pregunta nueva + configuración no rotulada.


### 30. Recuperación futura
No tiene recuperación posterior dentro del núcleo; constituye transferencia final.


### 31. Riesgo de aprendizaje superficial
Buscar una palabra clave o copiar una receta anterior sin identificar población, tipos y significado de la codificación.


### 32. Criterio de transferencia
Dominio suficiente cuando convergen:

```text
RUTA CORRECTA
+
PREPARACIÓN CORRECTA
+
RESULTADO DERIVADO DE DATOS
+
INTERPRETACIÓN COHERENTE
+
NO HARDCODING
```

Consultar sintaxis mediante una pista no invalida automáticamente el dominio conceptual.


### 33. Notas de implementación futura
Perturbation test fuerte: cambiar 1 estado de ocupación, 1–2 códigos de participación y 2–3 puntajes debe actualizar N, r, p e IC. El grader debe inspeccionar estado final y dependencias, no penalizar exploración razonable. `sessionInfo()` queda fuera de este grader.


---

# Criterio de dominio del Checkpoint E

## Dominio conceptual
Debe poder identificar:
- pregunta;
- población;
- variables;
- tipos;
- familia analítica.

## Dominio técnico
Debe poder:
- preparar la muestra;
- revisar missing;
- ejecutar un análisis reproducible.

## Dominio interpretativo
Debe integrar:
- signo;
- magnitud;
- evidencia;
- incertidumbre;
- no causalidad.

## Dominio suficiente
```text
RUTA CORRECTA
+
PREPARACIÓN CORRECTA
+
RESULTADO CORRECTO DERIVADO DE DATOS
+
INTERPRETACIÓN COHERENTE
+
NO HARDCODING
```

No se asigna nota ni porcentaje en este diseño.

# Retención final del curso

## Debe poder hacer sin ayuda conceptual
```text
pregunta
→ variables
→ tipos
→ casos
→ preparación
→ análisis
→ interpretación
```

## Puede consultar sintaxis
Es aceptable consultar:

```text
margin = 1
method = "pearson"
method = "spearman"
```

Consultar sintaxis **no implica falta de comprensión**.

## Debe saber interpretar
- frecuencias y proporciones;
- centro y dispersión;
- scatterplots;
- r/rho;
- p-value;
- intervalos de confianza;
- observed/expected;
- Cramér's V.

## Debe saber qué NO concluir
```text
asociación ≠ causalidad
p ≠ probabilidad de H0
p pequeño ≠ efecto grande
0/1 ≠ automáticamente cantidad
```

## No esperamos que domine todavía
- regresión;
- t-tests;
- ANOVA;
- modelos generalizados;
- imputación;
- inferencia causal;
- tests formales de supuestos;
- múltiples comparaciones;
- programación avanzada;
- tidyverse adicional.

# Cierre exacto del curso

> A lo largo del curso aprendiste funciones de R, pero la meta no era memorizar una lista de comandos.
>
> Una estrategia de análisis comienza antes de escribir código: parte de una pregunta, identifica qué datos necesita, decide qué casos y variables son pertinentes, revisa cómo están representados y elige una herramienta que responda a esa pregunta.
>
> **Aprender R no es memorizar funciones.**
>
> La ruta que queremos conservar es:
>
> **PREGUNTA → DATOS → DECISIONES → ANÁLISIS → INTERPRETACIÓN**
>
> Cuando aparezca una pregunta nueva, no busques primero un comando. Pregunta primero qué necesitas saber, qué representan tus variables, qué información está disponible y qué puede —y qué no puede— sostener el resultado.

# Tarjeta opcional de reproducibilidad

Después de aprobar E5 puede mostrarse:

> **Reproducibilidad**
>
> Si quieres registrar información sobre la versión de R y el entorno utilizado en tu sesión, puedes ejecutar:
>
> ```r
> sessionInfo()
> ```
>
> Esta acción es complementaria y **no forma parte del Checkpoint E ni de su grader**.

Nivel: funcional / opcional.

# Auditoría interna del lock

## Conteo por rol
```text
RECUPERACIÓN = 1
INTEGRACIÓN = 1
TRANSFERENCIA = 3
NOVEDAD = 0
PRÁCTICA = 0
```

## Novedad local
```text
0 %
```

## Datasets
```text
2
```

Base principal:

```text
encuesta_vida_universitaria
N = 48
```

Checkpoint:

```text
encuesta_vinculos_barriales
N = 40
```

## Sintaxis analítica nueva
```text
NINGUNA
```

## Outputs contractuales verificados

### E2
```text
N = 32
missing = 0 / 0
```

### E3
```text
r = 0.6514835763
t = 4.7034371502
df = 30
p = 0.0000537600951
IC 95 % = [0.3917924734, 0.8150287693]
Spearman de referencia = 0.6519683463
```

### E4
```text
Observed:
3  9
15 5
9  7

Expected:
6.75  5.25
11.25 8.75
9.00   7.00

χ² = 7.6190476190
df = 2
p = 0.0221587282
V = 0.3984095364
```

Todos los expected son ≥5.

### E5
```text
N total = 40
N ocupado = 30
missing = 0 / 0
0 = 16
1 = 14
media 0 = 55.75
media 1 = 65.00
r = 0.5168168103
t = 3.1944285021
df = 28
p = 0.0034534621
IC 95 % = [0.1923645585, 0.7394124666]
```

## Hardcoding
- E1: clasificación debe adaptarse si cambia pregunta/tipo.
- E2: objeto debe depender de la base y filtro.
- E3: r/p/IC deben provenir del análisis.
- E4: tabla, p y V deben ser dinámicos.
- E5: N/r/p/IC deben depender del filtro y datos.

## Perturbation tests
- E1: cambiar una tarjeta cambia la familia correcta.
- E2: cambiar jornada o missing cambia objeto/conteos.
- E3: modificar autoeficacia cambia gráfico/r/p/IC.
- E4: modificar participación cambia tabla/proporciones/χ²/p/V.
- E5: modificar ocupación, códigos y confianza cambia N/r/p/IC.

## Fading
```text
E1
clasificación estructurada
↓
E2
comentarios de preparación
↓
E3
comentarios mínimos
↓
E4
comentarios mínimos
↓
E5
starter casi vacío
```

## `sessionInfo()`
```text
opcional
post-checkpoint
fuera del grader
```

## Checkpoint E
```text
base nueva
+
pregunta nueva
+
configuración no rotulada
+
cero sintaxis nueva
```

# Control de consistencia global

| Dimensión | Resultado | Observación |
|---|---|---|
| Puente M12→M13 | APROBADO | procedimientos separados → decidir ruta completa |
| Número de ejercicios | APROBADO | 5 |
| Roles | APROBADO | 1 recuperación, 1 integración, 3 transferencias |
| Grandes novedades | APROBADO | 0 |
| Títulos visibles | APROBADO | no revelan familia |
| Dataset principal | APROBADO | `encuesta_vida_universitaria`, N=48 |
| Dataset Checkpoint | APROBADO | `encuesta_vinculos_barriales`, N=40 |
| E1 | APROBADO | cinco familias + justificación |
| E2 | APROBADO | preparación antes de análisis |
| E3 | APROBADO | gráfico antes de método |
| Pearson/Spearman | APROBADO | Pearson justificado por forma |
| E4 | APROBADO | denominador deriva de pregunta |
| Chi-cuadrado | APROBADO | tabla 3×2, expected adecuados |
| Cramér's V | APROBADO | dinámico/plataforma |
| E5 | APROBADO | base y pregunta nuevas |
| Punto-biserial | APROBADO | recuperado, no nuevo |
| Missing | APROBADO | relevante a la pregunta |
| `sessionInfo()` | APROBADO | opcional y fuera del grader |
| No causalidad | APROBADO | E3, E4 y E5 |
| Semantic grading | APROBADO | propiedades, no strings |
| Hardcoding | APROBADO | protegido |
| Perturbation tests | APROBADO | definidos E1–E5 |
| Pistas | APROBADO | una por una |
| Exploración | APROBADO | no penalizada |
| Fading | APROBADO | apoyo decreciente |
| Cierre | APROBADO | arquitectura mental transferible |

# Issues para revisión humana

## Bloqueantes
Ningún issue pedagógico bloqueante.

## No bloqueantes
El entorno utilizado para construir este archivo no dispone del ejecutable de R. Los valores contractuales de Pearson, sus t/p/IC, Spearman, Chi-cuadrado, expected y Cramér's V fueron recalculados independientemente con fórmulas equivalentes y contrastados con la estructura de salida documentada para `cor.test()` y `chisq.test()`. La implementación futura deberá repetir un smoke test en la versión concreta de R/webR que utilizará la plataforma, principalmente para formato/redondeo del output, no para rediseñar el currículo.

# Declaración de lock

M13 queda cerrado con:

- 5 ejercicios;
- 0 grandes novedades;
- 2 datasets de transferencia;
- 5 familias recuperadas en E1;
- preparación real en E2;
- scatterplot → Pearson → inferencia en E3;
- tabla → denominador → Chi² → expected → V en E4;
- base nueva + punto-biserial en Checkpoint E;
- semantic grading;
- hardcoding protection;
- perturbation tests;
- pistas escalonadas;
- `sessionInfo()` opcional fuera del grader;
- cierre conceptual del curso.

# M13 PEDAGOGICALLY LOCKED

```text
13 / 13 módulos pedagógicamente locked
88 / 88 ejercicios con arquitectura definida
5 / 5 checkpoints cerrados
```

# SOCIAL R — LOS 13 MÓDULOS QUEDAN PEDAGÓGICAMENTE LOCKED

Todavía:

# NO IMPLEMENTAR
