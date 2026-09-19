# Social R — Módulo 12
## Relacionar categorías

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede describir variables categóricas, analizar relaciones cuantitativas y comprende H0, p-value y la diferencia entre evidencia y magnitud.

### Capacidad después
Puede construir y leer una tabla de contingencia, elegir porcentajes adecuados según la pregunta, razonar independencia mediante observado y esperado, ejecutar e interpretar un test Chi-cuadrado, revisar sus frecuencias esperadas y separar evidencia estadística de magnitud mediante Cramér's V.

### Pregunta central
¿Cómo estudiamos si dos variables categóricas aparecen asociadas y qué tan marcada es esa asociación?

### Modelo mental
```text
DOS CATEGÓRICAS
↓
TABLA
↓
CELDA = COMBINACIÓN
↓
PREGUNTA
↓
DENOMINADOR
↓
PORCENTAJES
↓
INDEPENDENCIA
↓
OBSERVADO
VS
ESPERADO
↓
χ²
↓
H0 + p
↓
EVIDENCIA
≠
MAGNITUD
↓
CRAMÉR'S V
↓
INTERPRETACIÓN SUSTANTIVA
↓
NO CAUSALIDAD
```

### Principio conceptual central
M12 no enseña:

```text
DOS CATEGÓRICAS
↓
chisq.test()
↓
p < .05
↓
“HAY RELACIÓN”
```

Enseña:

```text
¿CÓMO SE DISTRIBUYEN JUNTAS?
↓
TABLA
↓
¿QUÉ PORCENTAJE RESPONDE LA PREGUNTA?
↓
¿QUÉ VERÍAMOS BAJO INDEPENDENCIA?
↓
OBSERVADO VS ESPERADO
↓
¿QUÉ TAN INCOMPATIBLE ES CON H0?
↓
χ² + p
↓
¿QUÉ TAN MARCADA ES LA ASOCIACIÓN?
↓
CRAMÉR'S V
```

### Habilidades nucleares
Al finalizar M12, el estudiante debe poder:

- reconocer cuándo dos variables son categóricas;
- evitar convertir categorías nominales en códigos 1/2/3 para correlacionarlas;
- construir una tabla bidimensional con `table(x, y)`;
- comprender que el primer argumento de `table()` aparece en filas y el segundo en columnas;
- interpretar una celda como una combinación de dos categorías;
- comprender que una tabla de contingencia contiene conteos;
- elegir el denominador correcto a partir de la pregunta sustantiva;
- producir porcentajes por fila con `prop.table(tabla, 1)`;
- distinguir conteo y porcentaje cuando los grupos tienen tamaños diferentes;
- comprender independencia;
- distinguir observado y esperado;
- comprender de dónde surge una frecuencia esperada;
- interpretar `chisq.test()` como evaluación de discrepancias O–E respecto de independencia;
- recuperar H0 y p-value sin reinterpretarlos;
- revisar `prueba$observed` y `prueba$expected`;
- reconocer cuándo los valores esperados del ejemplo son suficientemente cómodos para la aproximación introductoria;
- separar evidencia estadística de magnitud;
- interpretar Cramér's V como magnitud estandarizada de asociación;
- comprender que Cramér's V no tiene signo ni es un porcentaje;
- volver a porcentajes y O/E para describir la forma sustantiva del patrón;
- mantener asociación separada de causalidad.

### Habilidades funcionales
Quedan a nivel funcional:

- `prop.table(tabla, 2)` como contraste para preguntas dentro de columnas;
- `prop.table(tabla)` como proporción respecto del total general;
- lectura de `df` en el output de `chisq.test()`;
- reconocimiento de `$observed` y `$expected` como componentes del objeto de test;
- fórmula conceptual de Chi-cuadrado;
- fórmula conceptual de Cramér's V;
- cálculo de Cramér's V proporcionado por la plataforma.

### Habilidades recuperadas
M12 recupera:

- `table()` y `prop.table()` de M7;
- `$` de M4;
- significado de variable categórica;
- conteo ≠ proporción;
- número ≠ necesariamente cantidad;
- H0 y p-value de M10;
- evidencia ≠ magnitud;
- asociación ≠ causalidad;
- la protección de M11 frente a códigos numéricos arbitrarios.

### Habilidades pospuestas
No se introducen:

- `fisher.test()`;
- `correct = FALSE`;
- simulación Monte Carlo;
- corrección de Yates como contenido de estudiante;
- residuos Pearson;
- residuos estandarizados;
- análisis post-hoc;
- correcciones por comparaciones múltiples;
- odds ratios;
- regresión logística;
- modelos log-lineales;
- funciones helper propias;
- paquetes externos para tamaño de efecto;
- `sqrt()`, `dim()` o `min()` como nueva sintaxis productiva;
- cálculo manual completo de χ²;
- cálculo manual/programático completo de Cramér's V.

### Sintaxis nueva
Nueva habilidad nuclear:

```r
chisq.test(tabla)
```

Nuevo uso nuclear de una función conocida:

```r
table(x, y)
```

Nueva aplicación productiva de una función conocida:

```r
prop.table(tabla, 1)
```

### Sintaxis recuperada
```r
table()
prop.table()
$
<-
```

### Sintaxis que NO se introduce
```text
fisher.test()
correct = FALSE
simulate.p.value =
sqrt()
dim()
min()
residuals
stdres
rowSums()
colSums()
```

### Continuidad M11 → M12
M11 termina con la necesidad:

> Ya podemos organizar varias correlaciones entre cantidades
> y también vimos un caso especial:
> una variable categórica con **dos grupos**, codificada como 0/1,
> puede relacionarse con una cantidad mediante Pearson.
>
> Pero esa situación dependía de que una de las variables
> siguiera siendo cuantitativa.
>
> **¿Qué hacemos cuando las dos variables representan categorías?**

M12 comienza exactamente ahí.

### Contrato de datos
M12 **no modifica `encuesta_social`**.

La base principal es nueva:

```text
encuesta_participacion
N = 60
```

Variables:

```text
id
participacion_organizacion
transporte_campus
```

Categorías:

```text
participacion_organizacion:
- No participa
- Participa

transporte_campus:
- Activo
- Bus
- Metro
```

No contiene missing.

Datos caso por caso:

```text
id  participacion_organizacion  transporte_campus
1   No participa                Activo
2   No participa                Activo
3   No participa                Activo
4   No participa                Activo
5   No participa                Activo
6   No participa                Activo
7   No participa                Bus
8   No participa                Bus
9   No participa                Bus
10  No participa                Bus
11  No participa                Bus
12  No participa                Bus
13  No participa                Bus
14  No participa                Bus
15  No participa                Bus
16  No participa                Bus
17  No participa                Bus
18  No participa                Bus
19  No participa                Bus
20  No participa                Bus
21  No participa                Bus
22  No participa                Bus
23  No participa                Bus
24  No participa                Bus
25  No participa                Bus
26  No participa                Bus
27  No participa                Bus
28  No participa                Bus
29  No participa                Bus
30  No participa                Bus
31  No participa                Bus
32  No participa                Metro
33  No participa                Metro
34  No participa                Metro
35  No participa                Metro
36  No participa                Metro
37  No participa                Metro
38  No participa                Metro
39  No participa                Metro
40  No participa                Metro
41  Participa                   Activo
42  Participa                   Activo
43  Participa                   Activo
44  Participa                   Activo
45  Participa                   Activo
46  Participa                   Activo
47  Participa                   Activo
48  Participa                   Activo
49  Participa                   Activo
50  Participa                   Bus
51  Participa                   Bus
52  Participa                   Bus
53  Participa                   Bus
54  Participa                   Bus
55  Participa                   Metro
56  Participa                   Metro
57  Participa                   Metro
58  Participa                   Metro
59  Participa                   Metro
60  Participa                   Metro
```

Este dataset queda locked para M12.

### Tabla observada principal
```text
                         Activo Bus Metro Total
No participa                  6  25     9    40
Participa                     9   5     6    20
Total                        15  30    15    60
```

### Política de tablas
Código canónico:

```r
tabla <- table(
  encuesta_participacion$participacion_organizacion,
  encuesta_participacion$transporte_campus
)
```

Regla:

```text
PRIMER ARGUMENTO
→ FILAS

SEGUNDO ARGUMENTO
→ COLUMNAS
```

Modelo:

```text
FILA + COLUMNA
↓
COMBINACIÓN DE DOS CATEGORÍAS
↓
CONTEO DE CASOS
```

El término **tabla de contingencia** aparece después de comprender la tabla bidimensional.

### Protección frente a códigos arbitrarios
No:

```text
Activo = 1
Bus = 2
Metro = 3
↓
cor()
```

Sí:

```text
CATEGÓRICA
+
CATEGÓRICA
↓
table()
```

### Política de porcentajes
La pregunta determina el denominador.

Pregunta nuclear:

> Dentro de cada grupo de participación, ¿cómo se distribuye el transporte?

Como participación está en las filas:

```r
prop.table(
  tabla,
  1
)
```

Output:

```text
                         Activo    Bus   Metro
No participa              0.150  0.625   0.225
Participa                 0.450  0.250   0.300
```

Cada fila suma 1.

Ejemplo obligatorio:

```text
Metro:

No participa
9 casos
22.5 %

Participa
6 casos
30.0 %
```

Por tanto:

```text
MAYOR CONTEO
≠
MAYOR PORCENTAJE
```

### Porcentajes por columna
Quedan funcionales:

```r
prop.table(
  tabla,
  2
)
```

Output:

```text
                         Activo       Bus       Metro
No participa              0.40       0.833333   0.60
Participa                 0.60       0.166667   0.40
```

Sirven para mostrar:

```text
CAMBIAR LA PREGUNTA
↓
CAMBIA EL DENOMINADOR
```

### Proporción global
`prop.table(tabla)` divide por N=60 y puede responder otra pregunta. No se presenta como “incorrecta”; se presenta como una proporción con un denominador distinto.

### Política de independencia
Definición locked:

> Dos variables son independientes cuando conocer la categoría de una no cambia la distribución que esperamos de la otra.

En la base principal, la distribución global de transporte es:

```text
Activo = 15/60 = 25 %
Bus    = 30/60 = 50 %
Metro  = 15/60 = 25 %
```

Bajo independencia, esperaríamos aproximadamente esa misma distribución dentro de cada grupo de participación.

### Política de observado
> Lo observado es lo que realmente apareció en nuestra tabla.

Observed:

```text
                         Activo Bus Metro
No participa                  6  25     9
Participa                     9   5     6
```

### Política de esperado
> Lo esperado es el número de casos que esperaríamos aproximadamente en cada combinación si las dos variables fueran independientes, conservando los tamaños observados de filas y columnas.

Fórmula conceptual:

```text
esperado
=
(total de la fila × total de la columna)
/
total general
```

Solo se calcula manualmente una celda:

```text
No participa × Activo

40 × 15 / 60
=
10
```

Tabla esperada:

```text
                         Activo Bus Metro
No participa                 10  20    10
Participa                     5  10     5
```

### Política Chi-cuadrado
Modelo:

```text
OBSERVADO
VS
ESPERADO
↓
DISCREPANCIAS
↓
SE ACUMULAN
↓
χ²
```

Fórmula únicamente funcional:

```text
χ² =
Σ (O − E)² / E
```

No se memoriza ni se calcula manualmente.

### Política H0 / p
H0:

```text
las dos variables son independientes
en la población
```

p-value conserva el significado aprendido en M10:

```text
p
→ compatibilidad de los datos
  con el escenario nulo
```

No es la probabilidad de H0 y `1-p` no es la probabilidad de asociación.

### Test principal
```r
prueba <- chisq.test(tabla)

prueba
```

Valores contractuales:

```text
X-squared = 8.85
df = 2
p-value = 0.01197421130080363
```

### Política de supuestos / aproximación
M12 instala únicamente estas cautelas:

1. cada persona aporta una sola observación/celda;
2. las categorías de cada variable son mutuamente excluyentes;
3. antes de interpretar mecánicamente el test, se revisan los esperados.

Los ejemplos nucleares se diseñan con todos los expected ≥5.

Esto se presenta como una **regla introductoria de revisión de nuestros ejemplos**, no como condición matemática universal “si y solo si”.

### Política Yates
M12 utiliza tablas 2×3 y 3×2 en sus tests nucleares.

Por tanto no se introduce:

```text
correct = FALSE
```

ni la corrección de continuidad de Yates como contenido del estudiante.

### Política `$observed` / `$expected`
E5 recupera `$`:

```r
prueba$observed
prueba$expected
```

No introduce residuos.

### Política de evidencia y magnitud
```text
χ² + p
→ evidencia respecto de independencia

Cramér's V
→ magnitud estandarizada
```

### Política Cramér's V
M12 utiliza:

# CRAMÉR'S V

No Phi como medida central.

Cálculo:

# FUNCIONAL Y PROPORCIONADO POR LA PLATAFORMA

Interpretación:

# NUCLEAR

Fórmula visible una sola vez:

```text
V =
√[
  χ² /
  {N × min(r−1, c−1)}
]
```

No se introduce sintaxis productiva para calcularla.

Escala pedagógica:

```text
0
→ menor asociación en esta escala

valores mayores
→ asociación más marcada

1
→ extremo superior de la escala
```

No se usan umbrales universales `.10/.30/.50`.

Cramér's V:

- no es porcentaje;
- no tiene signo;
- no demuestra causalidad;
- no reemplaza porcentajes ni O/E para describir cómo se organiza el patrón.

### Contraste de evidencia y magnitud — E6
Tabla A:

```text
               Activo Bus Metro
No participa       6   25    9
Participa          9    5    6
```

```text
N = 60
χ² = 8.85
df = 2
p = 0.01197421130080363
V = 0.3840572873934304
```

Tabla B:

```text
               Activo Bus Metro
No participa      12   50   18
Participa         18   10   12
```

```text
N = 120
χ² = 17.7
df = 2
p = 0.000143381736276293069
V = 0.3840572873934304
```

Las proporciones y V son idénticos; N, χ² y p cambian.

### Base de transferencia — `encuesta_comunidad`
N=80.

Variables:

```text
id
zona_residencia
actividad_comunitaria
```

Categorías:

```text
zona_residencia:
- Centro
- Periferia
- Rural

actividad_comunitaria:
- No
- Sí
```

No missing.

Datos caso por caso:

```text
id  zona_residencia  actividad_comunitaria
1   Centro          No
2   Centro          No
3   Centro          No
4   Centro          No
5   Centro          No
6   Centro          No
7   Centro          No
8   Centro          No
9   Centro          No
10  Centro          No
11  Centro          No
12  Centro          No
13  Centro          No
14  Centro          No
15  Centro          No
16  Centro          No
17  Centro          No
18  Centro          No
19  Centro          No
20  Centro          No
21  Centro          No
22  Centro          No
23  Centro          No
24  Centro          Sí
25  Centro          Sí
26  Centro          Sí
27  Centro          Sí
28  Centro          Sí
29  Centro          Sí
30  Centro          Sí
31  Periferia       No
32  Periferia       No
33  Periferia       No
34  Periferia       No
35  Periferia       No
36  Periferia       No
37  Periferia       No
38  Periferia       No
39  Periferia       No
40  Periferia       No
41  Periferia       No
42  Periferia       No
43  Periferia       Sí
44  Periferia       Sí
45  Periferia       Sí
46  Periferia       Sí
47  Periferia       Sí
48  Periferia       Sí
49  Periferia       Sí
50  Periferia       Sí
51  Periferia       Sí
52  Periferia       Sí
53  Periferia       Sí
54  Periferia       Sí
55  Periferia       Sí
56  Periferia       Sí
57  Periferia       Sí
58  Periferia       Sí
59  Periferia       Sí
60  Periferia       Sí
61  Rural           No
62  Rural           No
63  Rural           No
64  Rural           No
65  Rural           No
66  Rural           No
67  Rural           No
68  Rural           No
69  Rural           No
70  Rural           No
71  Rural           Sí
72  Rural           Sí
73  Rural           Sí
74  Rural           Sí
75  Rural           Sí
76  Rural           Sí
77  Rural           Sí
78  Rural           Sí
79  Rural           Sí
80  Rural           Sí
```

### Resultados contractuales de E7
Observed:

```text
             No  Sí
Centro       23   7
Periferia    12  18
Rural        10  10
```

Row proportions:

```text
Centro       0.766667  0.233333
Periferia    0.400000  0.600000
Rural        0.500000  0.500000
```

Expected:

```text
             No       Sí
Centro       16.875   13.125
Periferia    16.875   13.125
Rural        11.250    8.750
```

Test:

```text
χ² = 8.61798941798942
df = 2
p = 0.01344706101113657
V = 0.3282146671385478
```

### Estrategia de scaffolding
1. E1 entrega el primer cruce completo.
2. E2 deja un `margin` por completar y centra la dificultad en el denominador.
3. E3 retira sintaxis nueva y construye independencia/esperados de forma conceptual.
4. E4 entrega `chisq.test()` como worked example.
5. E5 pide abrir el objeto del test con `$`.
6. E6 compara dos resultados sin nueva sintaxis.
7. E7 retira nombres de funciones y exige la ruta completa.

### Estrategia de fading
```text
E1
worked table
↓
E2
completion del margin
↓
E3
representación conceptual guiada
↓
E4
worked chi-square
↓
E5
completion observed/expected
↓
E6
interpretación comparativa
↓
E7
comentarios mínimos
```

### Riesgos cognitivos
- confundir fila y columna;
- tratar una celda como una sola categoría;
- comparar conteos entre grupos de tamaños diferentes;
- elegir el margin antes de leer la pregunta;
- tratar “expected” como predicción futura;
- pensar que independencia significa ausencia de cualquier relación imaginable;
- interpretar χ² como una correlación;
- interpretar p como probabilidad de H0;
- confundir p con magnitud;
- creer que Cramér's V tiene signo;
- interpretar V como porcentaje;
- no revisar esperados;
- inferir causalidad.

### Número de ejercicios
7

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Dataset | Carga |
|---|---|---|---|---|---|
| M12-E1 | Dos variables categóricas | NOVEDAD | frecuencias conjuntas / `table(x,y)` | `encuesta_participacion` | media |
| M12-E2 | Comparar porcentajes | PRÁCTICA | ninguna grande | misma | media |
| M12-E3 | ¿Qué esperaríamos sin asociación? | NOVEDAD | independencia + expected | misma | media-alta |
| M12-E4 | Medir observado vs esperado | NOVEDAD | Chi-cuadrado / `chisq.test()` | misma | media-alta |
| M12-E5 | Mira lo que esperaba la prueba | PRÁCTICA | ninguna | misma | media |
| M12-E6 | ¿Significativo significa grande? | RECUPERACIÓN | ninguna grande | tablas A/B | media |
| M12-E7 | Otra asociación categórica | TRANSFERENCIA | ninguna | `encuesta_comunidad` | media-alta |

---
## M12-E1 — Dos variables categóricas

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
M7 enseñó a contar una sola variable categórica. M12 necesita extender esa idea sin convertir las categorías en números arbitrarios: ahora queremos contar combinaciones de categorías de dos variables.

### 3. Capacidad antes
Puede reconocer variables categóricas y usar `table(x)` para obtener frecuencias de una variable.

### 4. Capacidad después
Puede construir y leer una tabla bidimensional de frecuencias conjuntas con `table(x, y)` y explicar qué representan filas, columnas y una celda.

### 5. Prerrequisitos
M7, `$`, objetos, significado de categoría y puente M11→M12.

### 6. Gran novedad
```text
UNA CATEGÓRICA
→ table(x)

DOS CATEGÓRICAS
→ table(x, y)
→ FRECUENCIAS CONJUNTAS
```

La gran novedad es conceptual: representar conjuntamente dos categóricas.

### 7. Recuperaciones
`table()`, `$`, número ≠ necesariamente cantidad y asociación ≠ causalidad.

### 8. Contexto sustantivo
Participación en organizaciones y medio principal de transporte al campus.

### 9. Dataset / objetos
Base:

```text
encuesta_participacion
N = 60
```

Variables:

```text
participacion_organizacion
transporte_campus
```

Objeto de salida:

```text
tabla
```

### 10. Texto para estudiante
Hasta ahora contamos categorías de una variable a la vez.

Ahora las dos características representan categorías:

- participación en organizaciones;
- medio principal de transporte al campus.

No necesitamos convertirlas en números.

Queremos saber **cuántas personas aparecen en cada combinación**.

Antes de ejecutar, predice qué forma tendrá la tabla si la primera variable tiene 2 categorías y la segunda 3.

### 11. Modelo mental
```text
DOS CATEGÓRICAS
↓
FILAS + COLUMNAS
↓
CELDA
=
COMBINACIÓN DE DOS CATEGORÍAS
↓
CONTEO
```

### 12. Representación / código trabajado
Worked example completo:

```r
tabla <- table(
  encuesta_participacion$participacion_organizacion,
  encuesta_participacion$transporte_campus
)

tabla
```

Después de leer al menos una celda, introducir el término:

> Esta tabla que cruza dos variables categóricas se llama **tabla de contingencia**.

### 13. Starter code
```r
tabla <- table(
  encuesta_participacion$participacion_organizacion,
  encuesta_participacion$transporte_campus
)

tabla
```

### 14. Acción esperada
Predecir 2×3, ejecutar el código y explicar qué representa una celda, por ejemplo `Participa × Activo = 9`.

### 15. Solución canónica
```r
tabla <- table(
  encuesta_participacion$participacion_organizacion,
  encuesta_participacion$transporte_campus
)

tabla
```

### 16. Resultado esperado
```text
                         Activo Bus Metro
No participa                  6  25     9
Participa                     9   5     6
```

Dimensiones:

```text
2 × 3
```

### 17. Criterio semántico de éxito
Comprobar:

- existe `tabla`;
- depende de `encuesta_participacion`;
- cruza exactamente las dos variables correctas;
- participación está en filas;
- transporte en columnas;
- dimensiones 2×3;
- conteos correctos;
- interpreta una celda;
- no hardcoding;
- no convierte categorías a 1/2/3 para `cor()`.

### 18. Estrategias alternativas válidas
Una tabla transpuesta contiene la misma información asociativa, pero no satisface la orientación específica de esta pantalla porque E2 depende de que participación esté en filas. El feedback debe diferenciar “información equivalente” de “contrato del ejercicio”.

### 19. Error esperado / misconception
- creer que cada fila representa una persona;
- pensar que una celda es una sola categoría;
- creer que la tabla contiene porcentajes;
- codificar `Activo=1, Bus=2, Metro=3` y correlacionar;
- intercambiar filas/columnas sin advertir que cambiará el denominador de E2.

### 20. Feedback correcto
> Bien. Cada celda cuenta personas que pertenecen simultáneamente a una categoría de participación y una categoría de transporte.

### 21. Feedback resultado correcto / estrategia incorrecta
Si codifica categorías y usa `cor()`:

> Esos números serían etiquetas, no cantidades. Para dos variables categóricas queremos contar sus combinaciones.

Si transpone la tabla:

> El cruce contiene la misma información, pero aquí necesitamos participación en filas porque la siguiente pregunta comparará dentro de esos grupos.

### 22. Hint 1
> En M7 usaste `table()` para una variable. Ahora necesitas contar combinaciones de dos.

### 23. Hint 2
> `table()` puede recibir dos variables: la primera formará las filas y la segunda las columnas.

### 24. Hint 3
```r
tabla <- table(
  encuesta_participacion$participacion_organizacion,
  encuesta_participacion$transporte_campus
)
```

### 25. Predicción
> Participación tiene 2 categorías y transporte 3: esperamos una tabla 2×3.

### 26. Tipo de ejercicio
Worked example + ejecución/observación.

### 27. Andamiaje
Alto. La sintaxis se entrega completa y la dificultad se concentra en leer la representación.

### 28. Carga cognitiva
Media: dos variables, filas, columnas, celda y frecuencia conjunta.

### 29. Fading
E1 entrega el código completo; E2 deja incompleto el `margin`; E7 retirará nombres de funciones.

### 30. Recuperación futura
E2–E5, E7 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar `table(x,y)` sin comprender que cada celda es una intersección de dos categorías.

### 32. Criterio de transferencia
Puede recibir otras dos categóricas y construir/leer una tabla cruzada sin convertirlas en cantidades.

### 33. Notas de implementación futura
Resaltar visualmente una sola celda y sus etiquetas de fila/columna. Ctrl+Enter ejecuta; “Comprobar respuesta” evalúa semánticamente el objeto.

---

## M12-E2 — Comparar porcentajes

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Los dos grupos de participación tienen tamaños diferentes (40 y 20). Comparar conteos directamente puede responder mal una pregunta formulada “dentro de cada grupo”.

### 3. Capacidad antes
Puede construir la tabla 2×3 y leer sus conteos.

### 4. Capacidad después
Puede elegir el denominador a partir de la pregunta y producir proporciones por fila con `prop.table(tabla, 1)`.

### 5. Prerrequisitos
E1, `prop.table()` de M7, conteo ≠ proporción.

### 6. Gran novedad
Ninguna gran novedad. La micro-novedad funcional es usar `margin = 1` en una tabla bidimensional.

### 7. Recuperaciones
`prop.table()`, porcentajes y lectura de filas.

### 8. Contexto sustantivo
Queremos comparar cómo se distribuye el transporte **dentro de cada grupo de participación**.

### 9. Dataset / objetos
Objeto `tabla` de E1, con totales de fila 40 y 20.

### 10. Texto para estudiante
La pregunta ahora es:

> **Dentro de cada grupo de participación, ¿cómo se distribuye el transporte?**

Antes de elegir código, identifica el denominador.

Si la pregunta dice “dentro de cada grupo de participación” y participación está en las filas, cada fila debe convertirse en su propio 100 %.

Completa el argumento que falta.

### 11. Modelo mental
```text
PREGUNTA
↓
¿DENTRO DE QUÉ GRUPO?
↓
ESE GRUPO DEFINE EL DENOMINADOR
↓
FILAS
↓
margin = 1
```

### 12. Representación / código trabajado
Mostrar totales visuales:

```text
No participa → 40
Participa    → 20
```

y después el completion problem.

### 13. Starter code
```r
prop.table(
  tabla,
  ___
)
```

### 14. Acción esperada
Completar `1`, ejecutar e interpretar al menos un contraste entre conteo y porcentaje.

### 15. Solución canónica
```r
prop.table(
  tabla,
  1
)
```

### 16. Resultado esperado
```text
                         Activo    Bus   Metro
No participa              0.150  0.625   0.225
Participa                 0.450  0.250   0.300
```

Cada fila suma aproximadamente 1.

### 17. Criterio semántico de éxito
Comprobar:

- usa `tabla`;
- divide por filas;
- proporciones correctas;
- cada fila suma 1 con tolerancia;
- interpreta el denominador;
- distingue conteo y porcentaje;
- no hardcoding.

### 18. Estrategias alternativas válidas
Una estrategia equivalente que divide cada fila por su total sería conceptualmente correcta, pero no debe requerir nueva sintaxis. La solución canónica es `prop.table(tabla, 1)`.

### 19. Error esperado / misconception
- usar `prop.table(tabla)` y asumir que responde la misma pregunta;
- usar `margin = 2`;
- comparar solo conteos;
- creer que la tabla debe sumar 1 completa;
- pensar que un conteo mayor implica un porcentaje mayor.

### 20. Feedback correcto
> Bien. La pregunta era “dentro de cada grupo de participación”, por eso cada fila es su propio denominador.

### 21. Feedback resultado correcto / estrategia incorrecta
Si usa proporción global:

> Esas proporciones son válidas respecto del total de 60 personas, pero la pregunta pide comparar **dentro de cada grupo**.

Si usa columnas:

> `margin = 2` respondería una pregunta distinta: dentro de cada transporte, ¿cómo se distribuye la participación?

### 22. Hint 1
> La pregunta dice “dentro de cada grupo de participación”.

### 23. Hint 2
> Participación está en las filas; cada fila debe sumar 100 %.

### 24. Hint 3
```r
prop.table(
  tabla,
  1
)
```

### 25. Predicción
> Con porcentajes por fila, cada fila —no toda la tabla— debe sumar 100 %.

### 26. Tipo de ejercicio
Completion problem + interpretación.

### 27. Andamiaje
Medio.

### 28. Carga cognitiva
Media: conteos, denominador, filas y porcentajes.

### 29. Fading
Se retira una parte de la sintaxis. E3 retirará código nuevo y pedirá razonamiento conceptual.

### 30. Recuperación futura
E3, E7 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar `1 = filas` sin volver a la pregunta que define el denominador.

### 32. Criterio de transferencia
Puede decidir si una nueva pregunta requiere porcentajes por fila, columna o total general.

### 33. Notas de implementación futura
Usar el contraste Metro como evidencia:

```text
No participa: 9 casos, 22.5 %
Participa: 6 casos, 30.0 %
```

Esto debe quedar visible para instalar `conteo ≠ porcentaje`. `margin=2` puede mostrarse después como contraste funcional, no como segunda producción obligatoria.

---

## M12-E3 — ¿Qué esperaríamos sin asociación?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Chi-cuadrado no debe aparecer como un botón. Antes, el estudiante necesita un escenario de referencia: cómo se vería la tabla si conocer participación no cambiara la distribución de transporte.

### 3. Capacidad antes
Puede leer la tabla observada y comparar distribuciones por fila.

### 4. Capacidad después
Puede explicar independencia, distinguir observado/esperado y calcular conceptualmente una frecuencia esperada a partir de los marginales.

### 5. Prerrequisitos
E1–E2, porcentajes y marginales visibles.

### 6. Gran novedad
```text
INDEPENDENCIA
+
FRECUENCIA ESPERADA
```

### 7. Recuperaciones
Distribución porcentual y lectura de tabla.

### 8. Contexto sustantivo
Participación organizacional y transporte.

### 9. Dataset / objetos
Misma tabla principal; marginal global de transporte 25 % / 50 % / 25 %.

### 10. Texto para estudiante
Mira primero las 60 personas juntas:

```text
Activo = 25 %
Bus    = 50 %
Metro  = 25 %
```

Imagina ahora un escenario donde participación y transporte fueran independientes.

En ese escenario, conocer si una persona participa o no **no cambiaría la distribución que esperamos de transporte**.

Por eso esperaríamos aproximadamente 25/50/25 dentro de cada grupo.

Llamaremos **observado** a lo que realmente apareció y **esperado** a lo que correspondería aproximadamente bajo independencia.

### 11. Modelo mental
```text
DISTRIBUCIÓN GLOBAL
↓
INDEPENDENCIA
↓
MISMA DISTRIBUCIÓN ESPERADA EN CADA GRUPO
↓
FRECUENCIAS ESPERADAS
↓
COMPARAR O VS E
```

### 12. Representación / código trabajado
No hay nueva función.

Worked calculation de una sola celda:

```text
No participa × Activo

total fila = 40
total columna = 15
N = 60

esperado
=
40 × 15 / 60
=
10
```

Después revelar la tabla esperada completa.

### 13. Starter code
No se requiere código productivo. El entorno muestra tabla observada, marginales y un espacio de razonamiento.

### 14. Acción esperada
Explicar independencia, calcular la celda worked y clasificar observed/expected sin introducir todavía Chi-cuadrado.

### 15. Solución canónica
```text
Independencia:
conocer participación no cambia la distribución esperada de transporte.

Esperado No participa × Activo:
40 × 15 / 60 = 10
```

### 16. Resultado esperado
Tabla expected:

```text
                         Activo Bus Metro
No participa                 10  20    10
Participa                     5  10     5
```

### 17. Criterio semántico de éxito
Comprobar:

- independencia correctamente explicada;
- observed ≠ expected;
- expected no es predicción futura;
- celda trabajada = 10;
- reconoce que expected depende de marginales;
- no introduce Chi-cuadrado como respuesta todavía.

### 18. Estrategias alternativas válidas
Puede derivar la celda mediante `40 × 25 % = 10` o mediante `40 × 15 / 60 = 10`. Ambas expresan el mismo razonamiento.

### 19. Error esperado / misconception
- expected = lo que debería moralmente ocurrir;
- expected = predicción futura;
- independencia = “no tienen nada que ver en ningún sentido”;
- repartir N en seis partes iguales;
- ignorar marginales;
- calcular las seis celdas como objetivo memorístico.

### 20. Feedback correcto
> Bien. El esperado conserva los tamaños observados de filas y columnas y pregunta cómo se combinarían bajo independencia.

### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene 10 dividiendo 60/6:

> Aquí coincide por casualidad en una celda, pero el esperado no reparte siempre por igual. Debe usar los marginales.

Si dice “esperado es lo que ocurrirá”:

> Es un escenario de referencia bajo independencia, no una predicción temporal.

### 22. Hint 1
> Mira primero la distribución global de transporte: 25 %, 50 %, 25 %.

### 23. Hint 2
> Bajo independencia esperaríamos esa misma distribución dentro de cada grupo de participación.

### 24. Hint 3
> Para una celda: total de fila × total de columna / N.

### 25. Predicción
> Si en el total solo 25 % usa transporte activo, bajo independencia no esperaríamos 45 % activo únicamente entre quienes participan.

### 26. Tipo de ejercicio
Interpretación conceptual guiada.

### 27. Andamiaje
Muy alto. Solo una celda se calcula manualmente.

### 28. Carga cognitiva
Media-alta: marginales, independencia, observed y expected.

### 29. Fading
E3 retira código y concentra el esfuerzo en el modelo mental. E4 volverá a entregar el nuevo procedimiento completamente.

### 30. Recuperación futura
E4–E5, E7 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar la fórmula del esperado sin comprender que representa un escenario de independencia.

### 32. Criterio de transferencia
Puede explicar qué significaría independencia y construir un esperado sencillo en otra tabla.

### 33. Notas de implementación futura
Mostrar marginales visualmente. No pedir las seis celdas manuales. Terminar con: “¿Cómo resumimos todas estas discrepancias en una sola evaluación?”

---

## M12-E4 — Medir observado vs esperado

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
E3 dejó seis discrepancias O–E. E4 introduce una herramienta para resumirlas y recuperar la lógica inferencial de H0/p sin reenseñarla desde cero.

### 3. Capacidad antes
Comprende independencia y observed/expected.

### 4. Capacidad después
Puede ejecutar `chisq.test(tabla)` e interpretar χ², H0 y p sin confundir evidencia con magnitud.

### 5. Prerrequisitos
E3 y M10.

### 6. Gran novedad
Sintaxis:

```r
chisq.test()
```

Modelo:

```text
O-E
↓
χ²
↓
H0
↓
p
```

### 7. Recuperaciones
H0, p-value, evidencia ≠ magnitud y no causalidad.

### 8. Contexto sustantivo
La misma tabla de participación × transporte.

### 9. Dataset / objetos
Objeto `tabla` de E1; objeto de salida `prueba`.

### 10. Texto para estudiante
Ya tenemos seis comparaciones entre observado y esperado.

Chi-cuadrado resume esas discrepancias en un único estadístico.

Nuestra hipótesis nula será:

> participación y transporte son independientes en la población.

Ejecuta el ejemplo y separa tres cosas:

1. qué resume χ²;
2. qué nos dice p sobre compatibilidad con H0;
3. qué **todavía no** sabemos sobre la magnitud de la asociación.

### 11. Modelo mental
```text
OBSERVADO
VS
ESPERADO
↓
DISCREPANCIAS
↓
χ²
↓
H0: INDEPENDENCIA
↓
p
↓
EVIDENCIA

PERO:
p ≠ MAGNITUD
```

### 12. Representación / código trabajado
Código trabajado:

```r
prueba <- chisq.test(
  tabla
)

prueba
```

Puede mostrarse funcionalmente:

```text
χ² =
Σ (O − E)² / E
```

sin cálculo manual.

### 13. Starter code
```r
prueba <- chisq.test(
  tabla
)

prueba
```

### 14. Acción esperada
Ejecutar, identificar χ²/df/p y escribir una interpretación inferencial prudente.

### 15. Solución canónica
```r
prueba <- chisq.test(
  tabla
)

prueba
```

### 16. Resultado esperado
```text
X-squared = 8.85
df = 2
p-value = 0.01197421130080363
```

### 17. Criterio semántico de éxito
Comprobar:

- `prueba` deriva de `chisq.test(tabla)`;
- χ² correcto;
- df correcto;
- p correcto;
- H0 = independencia;
- p no se interpreta como probabilidad de H0;
- p no se interpreta como magnitud;
- no causalidad;
- no hardcoding.

### 18. Estrategias alternativas válidas
`chisq.test(tabla)` sin guardar primero el objeto produce el mismo test, pero guardar `prueba` es preferible porque E5 necesita acceder a sus componentes.

### 19. Error esperado / misconception
- χ² = correlación;
- χ² con dirección positiva/negativa;
- p≈.012 = 1.2 % de probabilidad de independencia;
- 1-p = probabilidad de asociación;
- p<.05 = efecto grande;
- p pequeño = causalidad;
- calcular χ² manualmente como objetivo.

### 20. Feedback correcto
> Bien. El p-value indica baja compatibilidad con el escenario nulo de independencia, pero todavía no indica cuán marcada es la asociación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si reporta solo “significativo”:

> Falta explicar qué escenario evalúa el test y separar evidencia de magnitud.

Si dice “hay 98.8 % de probabilidad de asociación”:

> El p-value no es una probabilidad posterior de que exista asociación.

### 22. Hint 1
> Ya tienes la tabla de conteos observados. Necesitas un test de independencia para esa tabla.

### 23. Hint 2
> El procedimiento debe comparar globalmente observed con expected.

### 24. Hint 3
```r
prueba <- chisq.test(tabla)
```

### 25. Predicción
> Antes de ejecutar: las discrepancias O–E no son todas cercanas a cero, así que no esperamos un χ² igual a 0. No predigas el p exacto.

### 26. Tipo de ejercicio
Worked example inferencial.

### 27. Andamiaje
Alto.

### 28. Carga cognitiva
Media-alta: χ², H0, p y output. Por eso tamaño de efecto se pospone a E6.

### 29. Fading
Código completamente dado; E5 exigirá extraer componentes y E7 recuperará el test sin nombrarlo.

### 30. Recuperación futura
E5, E7 y M13.

### 31. Riesgo de aprendizaje superficial
Convertir `chisq.test()` en un generador ritual de p-values.

### 32. Criterio de transferencia
Puede reconocer que una tabla de dos categóricas necesita evaluar independencia y explicar correctamente la salida del test.

### 33. Notas de implementación futura
La tabla es 2×3 para evitar introducir la corrección de continuidad 2×2. No usar `correct = FALSE`. `df` se muestra como output funcional, sin cálculo manual.

---

## M12-E5 — Mira lo que esperaba la prueba

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
E5 conecta el objeto inferencial con el razonamiento conceptual de E3: el test guarda los conteos observados y los esperados bajo independencia.

### 3. Capacidad antes
Puede ejecutar el test y comprende expected conceptualmente.

### 4. Capacidad después
Puede recuperar `$observed`/`$expected`, comparar celdas y revisar que los esperados del ejemplo no sean pequeños.

### 5. Prerrequisitos
E3–E4 y `$`.

### 6. Gran novedad
Ninguna gran novedad.

### 7. Recuperaciones
`$`, observed/expected e independencia.

### 8. Contexto sustantivo
Mismo test de participación × transporte.

### 9. Dataset / objetos
Objeto `prueba` creado en E4.

### 10. Texto para estudiante
El p-value no es lo único que guarda `prueba`.

Queremos volver a la pregunta conceptual:

> ¿qué apareció realmente y qué esperaba el test bajo independencia?

Mira ambos componentes y compara algunas celdas.

Después revisa una condición básica del ejemplo: ¿aparecen frecuencias esperadas pequeñas?

### 11. Modelo mental
```text
prueba
↓
$observed
→ lo ocurrido

$expected
→ escenario de independencia

COMPARAR
↓
PATRÓN SUSTANTIVO
```

### 12. Representación / código trabajado
Mostrar lado a lado observed y expected una vez ejecutados. No mostrar residuos ni contribuciones estandarizadas.

### 13. Starter code
```r
prueba$observed

prueba$________
```

### 14. Acción esperada
Completar `expected`, ejecutar y describir al menos una celda O>E y una O<E.

### 15. Solución canónica
```r
prueba$observed

prueba$expected
```

### 16. Resultado esperado
Observed:

```text
                         Activo Bus Metro
No participa                  6  25     9
Participa                     9   5     6
```

Expected:

```text
                         Activo Bus Metro
No participa                 10  20    10
Participa                     5  10     5
```

### 17. Criterio semántico de éxito
Comprobar:

- usa el objeto `prueba`;
- extrae expected;
- identifica todos los expected ≥5;
- identifica al menos una celda O>E;
- identifica al menos una O<E;
- no usa residuos;
- no causalidad.

### 18. Estrategias alternativas válidas
Puede consultar solo `$expected` si already tiene la tabla observada visible; sin embargo, la solución canónica usa ambos para hacer explícito el contraste.

### 19. Error esperado / misconception
- expected = una segunda muestra;
- expected = predicción futura;
- revisar conteos observados en vez de expected para la aproximación;
- interpretar O>E como efecto causal;
- buscar residuos antes de comprender O/E.

### 20. Feedback correcto
> Bien. Volviste desde el test al patrón que lo genera: observed muestra lo ocurrido; expected muestra el escenario de independencia.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice “No participa + Bus causa el resultado”:

> Podemos describir que hay más casos observados que esperados, pero eso no identifica una causa.

Si no revisa expected:

> Antes de interpretar mecánicamente el test, mira los valores que el propio test esperaba bajo H0.

### 22. Hint 1
> `prueba` guarda más componentes que el p-value.

### 23. Hint 2
> Recupera `$`, igual que cuando extraías una variable de una base.

### 24. Hint 3
```r
prueba$expected
```

### 25. Predicción
> ¿Esperas que `$expected` sea idéntico a `$observed`? No: si lo fuera, las discrepancias serían 0.

### 26. Tipo de ejercicio
Completion problem + interpretación.

### 27. Andamiaje
Medio.

### 28. Carga cognitiva
Media: objeto de test, observed, expected y cautela sobre esperados.

### 29. Fading
El código se reduce a completar un componente. E6 eliminará producción sintáctica nueva y E7 exigirá toda la ruta.

### 30. Recuperación futura
E7 y M13.

### 31. Riesgo de aprendizaje superficial
Tratar `$expected` como un output accesorio sin conectarlo con independencia.

### 32. Criterio de transferencia
Puede inspeccionar expected en otro test y usarlo para contextualizar el resultado antes de interpretar p.

### 33. Notas de implementación futura
Instalar solo tres cautelas: casos independientes, categorías mutuamente excluyentes y revisión de expected. En los ejemplos nucleares todos los expected son ≥5. Si R emitiera una advertencia de aproximación en otro dataset, no debe ignorarse; los métodos alternativos quedan pospuestos.

---

## M12-E6 — ¿Significativo significa grande?

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
M10 ya separó evidencia y magnitud. E6 recupera esa distinción en asociación categórica y le asigna una medida de magnitud sin añadir nueva programación.

### 3. Capacidad antes
Puede interpretar p en Chi-cuadrado y comprende observed/expected.

### 4. Capacidad después
Puede distinguir evidencia de magnitud usando p y Cramér's V y explicar por qué el mismo patrón proporcional puede tener p-values distintos con distinto N.

### 5. Prerrequisitos
M10, E4–E5.

### 6. Gran novedad
Ninguna gran novedad. `Cramér's V` es una micro-novedad funcional de vocabulario e interpretación.

### 7. Recuperaciones
Evidencia ≠ magnitud y efecto del volumen de información sobre la evidencia.

### 8. Contexto sustantivo
Mismo patrón de participación × transporte con N=60 y N=120.

### 9. Dataset / objetos
Dos tablas de conteos mostradas lado a lado. No se exige reconstruir microdatos ni programar V.

### 10. Texto para estudiante
Mira dos estudios con **exactamente las mismas proporciones**.

En el segundo hay el doble de casos, pero el patrón relativo es idéntico.

La plataforma muestra dos resultados para cada tabla:

- p-value: evidencia respecto de independencia;
- Cramér's V: magnitud estandarizada de la asociación.

Responde:

1. ¿cambió la forma del patrón?
2. ¿cambió V?
3. ¿cambió p?
4. ¿la segunda asociación es “más grande” solo porque p es menor?

### 11. Modelo mental
```text
MISMAS PROPORCIONES
↓
MISMA MAGNITUD
↓
MISMO V

MÁS N
↓
MÁS INFORMACIÓN
↓
χ² / p PUEDEN CAMBIAR

p
≠
MAGNITUD
```

### 12. Representación / código trabajado
Tarjeta A:

```text
N = 60
p = 0.01197421130080363
V = 0.3840572873934304
```

Tarjeta B:

```text
N = 120
p = 0.000143381736276293069
V = 0.3840572873934304
```

Mostrar una sola vez, como explicación y no como tarea:

```text
V =
√[
  χ² /
  {N × min(r−1, c−1)}
]
```

### 13. Starter code
No se requiere código productivo. La plataforma muestra las dos tablas y los resultados calculados dinámicamente.

### 14. Acción esperada
Comparar proporciones, N, p y V, y formular la distinción evidencia/magnitud.

### 15. Solución canónica
```text
Las proporciones son iguales.
V es igual.
N cambia.
p cambia.

Conclusión:
un p más pequeño no implica una asociación más grande.
```

### 16. Resultado esperado
Tabla A:

```text
N = 60
χ² = 8.85
df = 2
p = 0.01197421130080363
V = 0.3840572873934304
```

Tabla B:

```text
N = 120
χ² = 17.7
df = 2
p = 0.000143381736276293069
V = 0.3840572873934304
```

### 17. Criterio semántico de éxito
Comprobar:

- reconoce mismas proporciones;
- reconoce mismo V;
- reconoce distinto N;
- reconoce distinto p;
- no concluye mayor efecto por menor p;
- no interpreta V como porcentaje;
- no asigna signo a V;
- vuelve a porcentajes para describir el patrón.

### 18. Estrategias alternativas válidas
Puede explicar la invariancia de V verbalmente sin mencionar la fórmula. La fórmula no es objetivo de producción.

### 19. Error esperado / misconception
- p menor = asociación mayor;
- χ² mayor = efecto necesariamente mayor;
- V=.384 = 38.4 % de personas;
- V positivo = dirección positiva;
- V identifica qué categoría “causa” el patrón;
- introducir potencia formal.

### 20. Feedback correcto
> Exacto. Las dos tablas tienen la misma asociación proporcional y el mismo Cramér's V, aunque la evidencia estadística cambia al aumentar N.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice “B es más fuerte porque p es menor”:

> Compara V y los porcentajes: son iguales. Lo que cambió fue la cantidad de información.

Si dice “V es positivo”:

> Cramér's V no tiene dirección positiva/negativa. Para saber cómo se configura el patrón debes mirar porcentajes y O/E.

### 22. Hint 1
> Compara primero las proporciones, no el p-value.

### 23. Hint 2
> Después compara Cramér's V: ¿cambió?

### 24. Hint 3
> Si proporciones y V son iguales pero N cambia, p puede cambiar sin que la magnitud sea distinta.

### 25. Predicción
> Si duplicamos todos los conteos manteniendo exactamente las mismas proporciones, la forma del patrón no debería cambiar.

### 26. Tipo de ejercicio
Recuperación conceptual comparativa.

### 27. Andamiaje
Medio.

### 28. Carga cognitiva
Media: N, p, V y evidencia/magnitud; no hay nueva sintaxis.

### 29. Fading
Se retira la programación y se exige interpretación. E7 pedirá recuperar toda la ruta analítica.

### 30. Recuperación futura
E7 y M13.

### 31. Riesgo de aprendizaje superficial
Aprender V como otro número ritual sin comprender que su función es diferente de p y que no describe por sí solo la forma del patrón.

### 32. Criterio de transferencia
Puede recibir otro test categórico y reportar por separado patrón descriptivo, evidencia y magnitud.

### 33. Notas de implementación futura
Cramér's V debe calcularse dinámicamente a partir de la tabla actual. No hardcodear `.384`. No crear helper visible, no cargar paquetes y no introducir umbrales rígidos.

---

## M12-E7 — Otra asociación categórica

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
Es la primera vez en M12 que una consigna nueva exige recuperar por sí sola la ruta completa sin nombrar las funciones.

### 3. Capacidad antes
Dispone de toda la ruta categórica: tabla, porcentajes, independencia, Chi-cuadrado, expected y magnitud.

### 4. Capacidad después
Puede analizar autónomamente una asociación entre dos categóricas en una base nueva y separar patrón, evidencia, magnitud y causalidad.

### 5. Prerrequisitos
E1–E6.

### 6. Gran novedad
Ninguna.

### 7. Recuperaciones
`table()`, `prop.table()`, `chisq.test()`, `$expected`, p, Cramér's V y no causalidad.

### 8. Contexto sustantivo
Zona de residencia y participación en actividades comunitarias.

### 9. Dataset / objetos
Base nueva:

```text
encuesta_comunidad
N = 80
```

Variables:

```text
zona_residencia
actividad_comunitaria
```

Sin missing.

### 10. Texto para estudiante
Queremos estudiar si la participación en actividades comunitarias se distribuye de la misma manera entre distintas zonas de residencia.

Analiza la relación entre ambas variables categóricas.

Tu respuesta debe:

1. organizar conjuntamente las categorías;
2. comparar los grupos con porcentajes adecuados;
3. evaluar la asociación;
4. revisar los valores esperados antes de interpretar el test;
5. distinguir evidencia estadística de magnitud;
6. explicar qué patrón sustantivo muestran los porcentajes;
7. indicar qué no podemos concluir causalmente.

No se indica qué funciones debes usar.

### 11. Modelo mental
```text
PREGUNTA
↓
DOS CATEGÓRICAS
↓
TABLA
↓
PORCENTAJES ADECUADOS
↓
TEST DE INDEPENDENCIA
↓
REVISAR EXPECTED
↓
p + V
↓
PATRÓN + EVIDENCIA + MAGNITUD
↓
NO CAUSALIDAD
```

### 12. Representación / código trabajado
No se entrega ejemplo resuelto. Los comentarios del starter solo separan etapas.

### 13. Starter code
```r
# organiza conjuntamente las dos variables


# compara los grupos con porcentajes adecuados


# evalúa la asociación


# revisa los valores esperados antes de interpretar
```

### 14. Acción esperada
Crear la tabla, producir porcentajes por fila, ejecutar el test, revisar expected e interpretar el V mostrado por la plataforma.

### 15. Solución canónica
```r
tabla_comunidad <- table(
  encuesta_comunidad$zona_residencia,
  encuesta_comunidad$actividad_comunitaria
)

prop.table(
  tabla_comunidad,
  1
)

prueba_comunidad <- chisq.test(
  tabla_comunidad
)

prueba_comunidad

prueba_comunidad$expected
```

### 16. Resultado esperado
Observed:

```text
             No  Sí
Centro       23   7
Periferia    12  18
Rural        10  10
```

Row proportions:

```text
Centro       0.766667  0.233333
Periferia    0.400000  0.600000
Rural        0.500000  0.500000
```

Expected:

```text
             No       Sí
Centro       16.875   13.125
Periferia    16.875   13.125
Rural        11.250    8.750
```

Test:

```text
χ² = 8.61798941798942
df = 2
p = 0.01344706101113657
```

Plataforma:

```text
Cramér's V = 0.3282146671385478
```

### 17. Criterio semántico de éxito
Comprobar:

- tabla 3×2 correcta;
- zona en filas;
- actividad en columnas;
- porcentajes por fila;
- test correcto;
- expected revisado;
- todos expected >5;
- χ²/df/p correctos;
- interpreta V como magnitud;
- V no porcentaje ni signo;
- describe patrón por zona;
- no causalidad;
- no hardcoding.

### 18. Estrategias alternativas válidas
Puede guardar las proporciones en un objeto intermedio o consultar `$observed` además de `$expected`. La ruta debe seguir siendo reproducible y coherente con la pregunta.

### 19. Error esperado / misconception
- codificar zona 1/2/3 y correlacionar;
- usar porcentajes globales;
- usar columnas como denominador sin justificarlo;
- no revisar expected;
- interpretar p como magnitud;
- dar signo a V;
- concluir que la zona causa participación.

### 20. Feedback correcto
> Bien. Separaste la descripción del patrón, la evidencia contra independencia y la magnitud, y mantuviste la interpretación en términos de asociación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si llega a los números escribiendo la tabla manualmente:

> El resultado coincide, pero la ruta debe depender de `encuesta_comunidad` para seguir funcionando si cambian los datos.

Si reporta solo p:

> Falta describir qué patrón muestran las proporciones y reportar la magnitud mediante V.

### 22. Hint 1
> Ambas variables son categóricas: empieza organizando sus combinaciones.

### 23. Hint 2
> La pregunta compara la actividad **dentro de cada zona**, así que decide el denominador desde esa frase.

### 24. Hint 3
> Después de la tabla y los porcentajes, recupera el test de independencia y revisa sus esperados.

### 25. Predicción
> Antes del test: las proporciones de “Sí” no parecen iguales entre Centro, Periferia y Rural.

### 26. Tipo de ejercicio
Transferencia integrada.

### 27. Andamiaje
Bajo.

### 28. Carga cognitiva
Media-alta, pero sin novedad ni missing.

### 29. Fading
Máximo M12: la consigna no nombra funciones y el starter contiene solo comentarios.

### 30. Recuperación futura
M13-E1, M13-E4 y Checkpoint E.

### 31. Riesgo de aprendizaje superficial
Buscar una palabra clave para elegir `chisq.test()` sin justificar el tipo de variables, el denominador o la interpretación.

### 32. Criterio de transferencia
Puede recibir otra base y pregunta con dos categóricas y construir una respuesta completa sin instrucciones de función.

### 33. Notas de implementación futura
El grader debe evaluar objetos/resultados y decisiones semánticas, no código literal. V debe calcularse dinámicamente desde `tabla_comunidad`. Las pistas se abren una a una.

---

# Retención esperada después de una semana

## Debe comprender sin ayuda
Debe poder explicar:

```text
DOS CATEGÓRICAS
→ TABLA DE CONTINGENCIA
```

Debe comprender:

```text
CELDA
→ combinación de dos categorías
```

Debe comprender:

```text
PORCENTAJE
→ depende del denominador
```

Debe explicar:

```text
INDEPENDENCIA
→ conocer una categoría
  no cambia la distribución esperada
  de la otra
```

Debe distinguir:

```text
OBSERVADO
VS
ESPERADO
```

Debe comprender:

```text
χ²
→ discrepancia global O-E
```

Debe distinguir:

```text
p
→ evidencia

V
→ magnitud
```

Debe recordar:

```text
V
→ no tiene signo
→ no es porcentaje
```

Debe comprender:

```text
ASOCIACIÓN
≠
CAUSALIDAD
```

## Debe producir con poca ayuda
```r
tabla <- table(x, y)

prop.table(
  tabla,
  1
)

prueba <- chisq.test(tabla)

prueba$expected
```

## Puede necesitar recordatorio sintáctico
```text
margin = 1
vs
margin = 2
```

y el nombre exacto:

```text
$expected
```

Cramér's V no tiene sintaxis productiva en el núcleo.

## No esperamos que recuerde todavía
- fórmula completa de χ²;
- fórmula de df;
- fórmula programática de Cramér's V;
- corrección de Yates;
- Fisher exacto;
- Monte Carlo;
- residuos;
- comparaciones post-hoc;
- correcciones múltiples;
- odds ratios;
- regresión logística;
- modelos log-lineales.

# Cierre conceptual M12 → M13

Cerrar exactamente con:

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

Detenerse ahí.

No introducir todavía:

- árbol de decisión;
- dataset final;
- Checkpoint E;
- funciones de M13;
- ejercicios M13.

# Auditoría interna del lock

## Conteo por rol
- NOVEDAD: 3
- PRÁCTICA: 2
- RECUPERACIÓN: 1
- INTEGRACIÓN: 0
- TRANSFERENCIA: 1

## Porcentaje local de novedad
3 de 7 = 42.9 %.

Esto no altera la arquitectura global del curso, donde la novedad se controla a nivel de los 88 ejercicios.

## Trayectoria de categorías
```text
M7
una categórica
↓
frecuencias / proporciones
↓
M12-E1
dos categóricas
↓
tabla de contingencia
```

## Trayectoria de porcentajes
```text
conteos
↓
pregunta
↓
denominador
↓
porcentajes por fila
↓
interpretación
```

## Trayectoria inferencial
```text
M10
H0 / p
↓
M12-E3
independencia
↓
observado / esperado
↓
M12-E4
χ² / p
```

## Trayectoria magnitud
```text
M10
evidencia ≠ magnitud
↓
M12-E6
p ≠ V
↓
M12-E7
patrón + evidencia + magnitud
```

# Control técnico verificado

## Base principal
Observed:

```text
6 25 9
9  5 6
```

Expected:

```text
10 20 10
5  10  5
```

Resultados:

```text
χ² = 8.85
df = 2
p = 0.01197421130080363
V = 0.3840572873934304
```

## E6 — tabla B
```text
χ² = 17.7
df = 2
p = 0.000143381736276293069
V = 0.3840572873934304
```

Se verifica:

```text
V_A = V_B
```

## E7
Observed:

```text
23 7
12 18
10 10
```

Expected:

```text
16.875 13.125
16.875 13.125
11.250  8.750
```

Resultados:

```text
χ² = 8.617989417989419
df = 2
p = 0.01344706101113657
V = 0.3282146671385478
```

Todos los expected de los tests nucleares son ≥5.

# Semantic grading global

La implementación futura debe evaluar:

- tipos de variables;
- orientación de la tabla;
- conteos;
- significado de una celda;
- denominador;
- margen;
- proporciones;
- independencia;
- observed;
- expected;
- test;
- χ²;
- df;
- p;
- revisión de expected;
- evidencia;
- magnitud;
- interpretación de V;
- ausencia de signo de V;
- no causalidad;
- dependencia real de los datos;
- protección contra hardcoding.

No comparar código literal.

# Hardcoding global
- E1: no aceptar tabla manual.
- E2: no aceptar porcentajes literales.
- E3: expected debe depender de marginales.
- E4: χ²/p deben provenir del test.
- E5: expected debe provenir de `prueba`.
- E6: V debe calcularse dinámicamente en la plataforma.
- E7: toda la ruta debe depender de `encuesta_comunidad`.

# Perturbation tests
- E1: cambiar categorías → cambia tabla.
- E2: cambiar composición de filas → cambian proporciones.
- E3: cambiar marginales → cambian expected.
- E4: mover casos entre celdas → cambian χ²/p.
- E5: cambiar tabla → cambian observed/expected.
- E6: escalar conteos con proporciones fijas → V se mantiene y p cambia.
- E7: modificar asociación → cambian tabla, porcentajes, test y V.

# Issues para implementación futura
Ningún issue pedagógico bloqueante.

Nota no bloqueante:

> Cramér's V será calculado por la plataforma y no por sintaxis productiva del estudiante. La implementación deberá garantizar que el valor provenga dinámicamente de la tabla actual y nunca de un literal hardcodeado.

# Declaración de lock

M12 queda pedagógicamente cerrado con 7 ejercicios.

- **Datasets:** `encuesta_participacion` (N=60) y `encuesta_comunidad` (N=80).
- **Tabla de contingencia:** `table(x, y)`.
- **Porcentajes:** pregunta → denominador → `prop.table(tabla, 1)` como producción nuclear.
- **Independencia:** conocer una categoría no cambia la distribución esperada de la otra.
- **Observed/expected:** ambos se conectan directamente con el test.
- **Chi-cuadrado:** discrepancia global entre observado y esperado.
- **H0/p:** recuperan la lógica inferencial de M10.
- **Condiciones:** independencia de casos, categorías excluyentes y revisión de expected.
- **Yates:** deliberadamente fuera del núcleo.
- **Magnitud:** Cramér's V, cálculo funcional de plataforma e interpretación nuclear.
- **E6:** mismo patrón/V, distinto N/p.
- **E7:** transferencia completa sin funciones nombradas.
- **Missing:** no aparece en M12.
- **Sintaxis pospuesta:** Fisher, Yates, residuos, paquetes, helpers y cálculo programático de V.
- **Puente M13:** procedimientos separados → elegir una ruta completa.

# M12 PEDAGOGICALLY LOCKED
