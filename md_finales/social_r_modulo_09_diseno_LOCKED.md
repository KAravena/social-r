# Social R — Módulo 9
## Ver relaciones entre dos cantidades

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede describir una variable cuantitativa por separado mediante distribución, centro y dispersión.

### Capacidad después
Puede vincular dos variables cuantitativas por caso, representar sus pares mediante un scatterplot, describir dirección, forma y grado de concentración del patrón, y resumir una asociación lineal mediante el coeficiente de correlación de Pearson, sin interpretarlo como causalidad.

### Pregunta central
¿Cómo puedo estudiar si dos cantidades cambian juntas?

### Modelo mental
`MISMO CASO → DOS VALORES → PAR (x, y) → PUNTO → SCATTERPLOT → PATRÓN → DIRECCIÓN + FORMA + CONCENTRACIÓN → CORRELACIÓN LINEAL → r → INTERPRETAR JUNTO AL GRÁFICO`

### Principio pedagógico central
M9 no enseña:

```text
TENGO DOS COLUMNAS
↓
cor()
↓
NÚMERO
↓
CONCLUSIÓN
```

Enseña:

```text
¿SON DOS CANTIDADES?
↓
¿PERTENECEN AL MISMO CASO?
↓
FORMO PARES
↓
REPRESENTO LOS PARES
↓
MIRO EL PATRÓN
↓
DESCRIBO DIRECCIÓN / FORMA / CONCENTRACIÓN
↓
RESUMO LA ASOCIACIÓN LINEAL CON r
↓
INTERPRETO GRÁFICO + r
```

Principio nuclear:

> **EL NÚMERO NO REEMPLAZA AL GRÁFICO.**

La ruta estable del módulo es:

```text
GRÁFICO
↓
DESCRIBIR
↓
r
↓
INTERPRETAR EN CONJUNTO
```

Cuando existe missing:

```text
DETECTAR
↓
CONTAR
↓
IDENTIFICAR PARES COMPLETOS
↓
USAR LA MISMA MUESTRA ANALÍTICA
↓
GRAFICAR
↓
CORRELACIONAR
```

### Habilidades nucleares
Al terminar M9, el estudiante debe poder:

- reconocer que una relación entre dos variables conserva la correspondencia por caso;
- comprender que dos valores del mismo caso forman un par;
- utilizar la notación `(x, y)` en el nivel funcional necesario;
- comprender que cada punto de un scatterplot representa un caso;
- reconocer que en `plot(x, y)` la primera variable va al eje horizontal y la segunda al vertical;
- producir un scatterplot mediante `plot(x, y)`;
- reconocer una dirección positiva;
- reconocer una dirección negativa;
- reconocer que una nube puede no mostrar una dirección lineal clara;
- describir la forma general de un patrón;
- comparar qué tan concentrados o dispersos están los puntos alrededor de una tendencia;
- inspeccionar si existe algún punto muy alejado del patrón;
- comprender que dirección y concentración son propiedades distintas;
- comprender que una nube más inclinada no implica automáticamente una correlación más marcada;
- comprender que el gráfico debe mirarse antes de interpretar un coeficiente;
- comprender qué resume el coeficiente de correlación lineal de Pearson;
- producir `cor(x, y)` en datos completos;
- reconocer que el coeficiente de Pearson se encuentra entre -1 y +1;
- interpretar el signo de `r` como dirección;
- interpretar qué tan lejos está `r` de 0 como información sobre cuán marcada es la asociación lineal;
- evitar thresholds universales rígidos para clasificar correlaciones;
- comprender que un `r` cercano a 0 indica poca asociación lineal, no necesariamente ausencia de cualquier patrón;
- comprender que `r` no es una pendiente;
- comprender que `r` no es un porcentaje;
- comprender que `r` no se expresa en las unidades originales de las variables;
- distinguir correlación de causalidad;
- comprender que, con missing, un caso necesita ambos valores disponibles para formar un par completo;
- distinguir casos del subgrupo de pares analíticos completos;
- comprender que gráfico y correlación deben describir la misma muestra analítica;
- recuperar `filter()`, `select()`, `|>`, `is.na()` y `sum(is.na())` dentro de un problema bivariado;
- transferir `plot()` + `cor()` a una base nueva sin que la consigna nombre las funciones.

### Habilidad funcional
La opción:

```r
use = "complete.obs"
```

es una construcción funcional para correlaciones con missing.

El estudiante debe comprender su significado, pero puede necesitar recordatorio de su escritura exacta después de una semana.

No se considera habilidad nuclear equivalente a `plot()` o `cor()`.

### Habilidades recuperadas
M9 recupera:

- fila = caso;
- columna = variable;
- `$`;
- objetos;
- `<-`;
- variables cuantitativas por significado;
- lectura de una distribución;
- atención a valores muy alejados;
- `filter()`;
- `select()`;
- `|>`;
- `is.na()`;
- `sum(is.na())`;
- N total vs N disponible;
- preparación reproducible de datos.

M9 no vuelve a enseñar media, mediana ni desviación estándar como contenido nuevo.

### Habilidades pospuestas
No se introducen en M9:

- `cor.test()`;
- `method = "spearman"`;
- Spearman como método formal;
- Kendall;
- rangos como fundamento de Spearman;
- hipótesis nula;
- p-values;
- intervalos de confianza;
- significancia estadística;
- pruebas de supuestos formales;
- regresión;
- pendiente como parámetro;
- intercepto;
- R²;
- varianza explicada;
- matrices de correlación;
- múltiples correlaciones;
- correlación parcial;
- causalidad formal;
- teoría avanzada de mecanismos de missing.

### Sintaxis nueva
- `plot(x, y)`;
- `cor(x, y)`.

### Sintaxis funcional
- `use = "complete.obs"`.

### Sintaxis que NO se introduce
No se introducen como código ejecutable:

```text
cor.test()
method = "spearman"
complete.cases()
!
lm()
```

### Dataset / vista contractual de M9
M9 inaugura `encuesta_social`, la base principal de M9–M12.

Este módulo fija únicamente una **vista contractual de M9**. Los módulos posteriores pueden añadir nuevas columnas, pero no modificar silenciosamente las siguientes columnas ni sus valores:

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

Contrato:

> M9 fija estas columnas y valores como parte del contrato pedagógico de `encuesta_social`.
>
> M10–M12 pueden ampliar la base con nuevas variables, pero no modificar silenciosamente estas columnas ni sus valores.

### Variables nucleares de E1–E5
La pareja introductoria es:

```text
horas_estudio
puntaje_metodos
```

Ambas variables:

- representan cantidades inequívocamente;
- tienen 12 pares completos;
- no contienen missing;
- producen un patrón positivo visible pero no perfecto;
- permiten introducir scatterplot y correlación sin decisiones adicionales de missing.

Coeficiente contractual:

```text
r de Pearson = 0.7500757095661253
```

En texto puede mostrarse:

```text
r ≈ 0.75
```

### Objetos pedagógicos auxiliares
M9-E3 utiliza tres patrones de seis pares para aislar la lectura de dirección.

#### Patrón positivo

```r
x_pos <- c(1, 2, 3, 4, 5, 6)
y_pos <- c(2, 3, 5, 4, 7, 8)
```

Referencia interna:

```text
r ≈ 0.9460139136
```

El coeficiente no se muestra al estudiante en E3.

#### Patrón negativo

```r
x_neg <- c(1, 2, 3, 4, 5, 6)
y_neg <- c(8, 7, 5, 6, 3, 2)
```

Referencia interna:

```text
r ≈ -0.9460139136
```

El coeficiente no se muestra al estudiante en E3.

#### Sin dirección lineal clara

```r
x_sin_direccion <- c(1, 2, 3, 4, 5, 6)
y_sin_direccion <- c(4, 7, 2, 6, 3, 5)
```

Referencia interna:

```text
r ≈ -0.0857142857
```

El coeficiente no se muestra al estudiante en E3.

M9-E4 utiliza dos patrones con la misma dirección general pero diferente concentración.

#### Patrón A

```r
x_a <- c(1, 2, 3, 4, 5, 6, 7, 8)
y_a <- c(2.2, 2.8, 4.1, 4.4, 5.8, 6.1, 7.4, 7.9)
```

Referencia interna:

```text
r ≈ 0.9934106276
```

#### Patrón B

```r
x_b <- c(1, 2, 3, 4, 5, 6, 7, 8)
y_b <- c(1, 5, 2, 6, 4, 8, 5, 9)
```

Referencia interna:

```text
r ≈ 0.7703288865
```

Los coeficientes de E4 se mantienen como referencia interna y no se muestran antes de introducir `cor()`.

### Dataset de transferencia
M9-E7 utiliza:

```text
encuesta_lectura

id   minutos_lectura   puntaje_comprension
1    15                50
2    35                57
3    25                66
4    55                84
5    20                59
6    50                69
7    30                68
8    60                83
9    40                55
10   45                62
```

No contiene missing.

Coeficiente contractual:

```text
r de Pearson = 0.760025069611547
```

### Política de missing bivariado
En M9, missing se recupera solo después de introducir `cor()` con datos completos.

Modelo:

```text
UNA VARIABLE
→ valor disponible / NA

DOS VARIABLES
→ necesito DOS valores disponibles
→ par completo
```

Ruta obligatoria:

```text
DETECTAR
↓
CONTAR
↓
RECONOCER PARES COMPLETOS
↓
GRAFICAR LOS PARES
↓
CORRELACIONAR LOS MISMOS PARES
```

`use = "complete.obs"` no se presenta como receta automática.

### Política de causalidad
M9 usa lenguaje de **asociación**, **tendencia** y **cambio conjunto**.

No se afirma:

> x causa y.

Regla visible:

```text
ASOCIACIÓN
≠
CAUSALIDAD
```

La primera protección aparece en E3 y se consolida en E5–E7.

### Política de interpretación de `r`
M9 fija seis ideas:

```text
1. r está entre -1 y +1.

2. signo
   → dirección.

3. distancia respecto de 0
   → cuán marcada es la asociación lineal.

4. r no es porcentaje.

5. r no es pendiente.

6. correlación no demuestra causalidad.
```

Además:

> un `r` cercano a 0 indica poca asociación lineal y no descarta automáticamente otros patrones.

No se enseñan thresholds universales.

### Política de tolerancia numérica
Los coeficientes no se comparan como texto.

La implementación futura debe usar tolerancia numérica.

No se exige `round()`.

### Estrategia de scaffolding
1. E1 hace visible caso → par sin código.
2. E2 convierte un par en punto e introduce `plot()` mediante worked example.
3. E3 practica dirección con gráficos ya disponibles.
4. E4 profundiza la lectura visual sin sintaxis nueva.
5. E5 introduce `cor()` sobre datos completos después del scatterplot.
6. E6 integra preparación + missing + pares completos + gráfico + correlación.
7. E7 retira los nombres de las funciones y transfiere a una base nueva.

### Estrategia de fading
`CASO → PAR → PUNTO → DIRECCIÓN → LECTURA RICA → r → MISSING BIVARIADO → TRANSFERENCIA`

En detalle:

```text
E1
representación completamente guiada
↓
caso → par

E2
worked example
↓
par → punto → plot()

E3
gráficos entregados
↓
dirección

E4
gráficos entregados
↓
lectura más rica

E5
worked example
↓
cor() + r

E6
skeleton parcial
↓
filter/select + missing + plot + cor

E7
comentarios mínimos
↓
plot + cor autónomos
```

### Riesgos cognitivos
- tratar las dos columnas como listas independientes y romper los pares;
- emparejar valores de casos distintos;
- creer que cada punto representa una variable y no un caso;
- invertir x/y sin comprender los ejes;
- asociar dirección positiva con causalidad;
- asociar dirección negativa con “relación mala”;
- confundir pendiente visual con concentración/fuerza de asociación;
- mirar solo `r` e ignorar la forma del scatterplot;
- interpretar `r` como porcentaje;
- interpretar `r` como pendiente;
- atribuir a `r` las unidades originales;
- asumir que `r ≈ 0` significa ausencia de cualquier relación;
- usar thresholds rígidos de fuerza;
- ignorar missing al formar pares;
- confundir número de casos del subgrupo con número de pares completos;
- creer que `use = "complete.obs"` modifica o limpia la base;
- hardcodear coeficientes o coordenadas;
- reconstruir manualmente vectores que ya existen en la base.

### Número de ejercicios
7

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M9-E1 | Dos valores de la misma persona | NOVEDAD | caso → par | fila = caso | baja |
| M9-E2 | Cada persona se vuelve un punto | NOVEDAD | par → punto + `plot(x, y)` | `$`, cuantitativas | media |
| M9-E3 | ¿Hacia dónde va la relación? | PRÁCTICA | ninguna | lectura de scatterplot | baja-media |
| M9-E4 | No basta con la dirección | PRÁCTICA | ninguna | dirección | media |
| M9-E5 | Resume el patrón con un número | NOVEDAD | `cor()` + r de Pearson | scatterplot | media |
| M9-E6 | Prepara los pares antes de correlacionar | RECUPERACIÓN | micro-novedad funcional `use = "complete.obs"` | M5 + M6 + `plot()` + `cor()` | media-alta |
| M9-E7 | Otra pregunta, otra base | TRANSFERENCIA | ninguna | ruta bivariada completa | media |

---
## M9-E1 — Dos valores de la misma persona

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
M8 terminó describiendo una cantidad por separado. Para estudiar dos cantidades juntas, primero hay que conservar una idea ya conocida desde M4: la fila representa al mismo caso.

E1 evita que el estudiante trate dos columnas como listas independientes. Construye el modelo que sostendrá todo el módulo:

```text
MISMO CASO
↓
DOS VALORES
↓
PAR
```

Sin esta idea, `plot()` y `cor()` pueden convertirse en recetas que destruyen la correspondencia entre personas.

### 3. Capacidad antes
Puede describir una variable cuantitativa por separado y comprende fila = caso.

### 4. Capacidad después
Puede identificar los dos valores cuantitativos que pertenecen a un mismo caso, representarlos como un par `(x, y)` y explicar por qué no deben mezclarse valores de casos distintos.

### 5. Prerrequisitos
- fila = caso;
- columna = variable;
- variable cuantitativa por significado;
- lectura de una tabla;
- correspondencia entre posiciones/casos.

No requiere `plot()` ni `cor()`.

### 6. Gran novedad
- **Sintaxis nueva:** ninguna productiva.
- **Concepto nuevo:** par de valores del mismo caso.
- **Notación nueva:** `(x, y)` en sentido funcional mínimo.
- **Decisión nueva:** preservar la correspondencia por fila.

### 7. Recuperaciones
Recupera directamente de M4 la idea `FILA = CASO` y de M8 que `horas_estudio` y `puntaje_metodos` representan cantidades.

### 8. Contexto sustantivo
Horas de estudio y puntaje en un curso de métodos para personas de `encuesta_social`.

### 9. Dataset / objetos
Mostrar solo los primeros cuatro casos de la vista contractual:

```text
id   horas_estudio   puntaje_metodos
1    2               59
2    4               68
3    3               58
4    6               64
```

Representación:

```text
caso 1 → (2, 59)
caso 2 → (4, 68)
caso 3 → (3, 58)
caso 4 → (6, 64)
```

### 10. Texto para estudiante
Hasta ahora describíamos una cantidad por separado.

Ahora queremos estudiar dos cantidades al mismo tiempo.

La clave es que cada persona aporta **dos valores que deben permanecer juntos**.

Observa:

```text
caso 1 → 2 horas de estudio + 59 puntos
caso 2 → 4 horas de estudio + 68 puntos
caso 3 → 3 horas de estudio + 58 puntos
```

Podemos representar el caso 3 como:

```text
(3, 58)
```

Ese par contiene dos características de la **misma persona**.

Responde:

1. ¿Qué dos valores forman el par del caso 3?
2. ¿Podríamos combinar las 3 horas del caso 3 con los 68 puntos del caso 2?
3. ¿Qué ocurriría si cambiáramos el orden de `puntaje_metodos` sin mover al mismo tiempo `horas_estudio`?

### 11. Modelo mental
```text
FILA
=
MISMO CASO

↓

DOS VARIABLES DE ESA FILA

↓

PAR
```

Regla:

```text
x DEL CASO i
+
y DEL CASO i
=
PAR DEL CASO i
```

### 12. Representación / código trabajado
No se requiere código productivo.

Representación clave:

```text
caso 3

horas_estudio = 3
puntaje_metodos = 58

↓

(3, 58)
```

Representación incorrecta:

```text
x del caso 3
+
y del caso 2

↓

NO ES EL PAR DE NINGUNO DE ESOS CASOS
```

### 13. Starter code
No se requiere editor productivo en E1.

### 14. Acción esperada
- identificar `(3, 58)`;
- rechazar `(3, 68)` como par válido del caso 3;
- explicar que ambos valores deben provenir de la misma fila;
- comprender que reordenar solo una variable rompe los pares originales.

### 15. Solución canónica
```text
caso 3 → (3, 58)
```

No:

```text
(3, 68)
```

Respuesta conceptual:

> Reordenar una sola variable destruye la correspondencia original entre las dos cantidades.

### 16. Resultado esperado
Identifica correctamente los pares y explica la correspondencia por caso.

### 17. Criterio semántico de éxito
Comprobar:

- caso 3 → `(3, 58)`;
- ambos valores pertenecen a la misma fila;
- rechaza emparejar casos distintos;
- comprende `UN CASO → UN PAR`;
- comprende que reordenar solo una variable cambia la relación original.

### 18. Estrategias alternativas válidas
Se aceptan explicaciones equivalentes que preserven la identidad del caso. No se exige utilizar literalmente las palabras “par ordenado” ni terminología geométrica.

### 19. Error esperado / misconception
- tratar ambas columnas como listas independientes;
- combinar valores de filas diferentes;
- pensar que tener los mismos valores marginales basta para conservar una relación;
- interpretar `(x, y)` como una fórmula;
- creer que el orden de una sola variable puede cambiarse sin consecuencias.

### 20. Feedback correcto
> Exacto. Los dos valores del par pertenecen a la misma persona. Esa correspondencia es la que debemos conservar durante todo el análisis.

### 21. Feedback resultado correcto / estrategia incorrecta
Si identifica `(3,58)` solo por memoria:

> El par coincide, pero la regla importante es recuperarlo desde la misma fila. Si cambia el orden de los casos, debes seguir buscando los dos valores del mismo caso.

Si propone `(3,68)`:

> Esos dos números existen en la tabla, pero pertenecen a personas distintas. Una relación bivariada conserva los valores del mismo caso.

### 22. Hint 1
Mira una sola fila.

### 23. Hint 2
Esa fila contiene las dos cantidades de una misma persona.

### 24. Hint 3
Para el caso 3: `(3, 58)`.

### 25. Predicción
No hay predicción de código.

Pregunta conceptual:

> ¿Qué par pertenece al caso 3?

### 26. Tipo de ejercicio
Interpretación guiada.

### 27. Andamiaje
Muy alto. La tabla, los casos y la notación están completamente visibles.

### 28. Carga cognitiva
Baja. Solo interactúan fila/caso, dos variables y la noción de par.

### 29. Fading
E1 muestra pares explícitamente. E2 retira esa representación completa y obliga a reconocer que cada par se convierte en un punto.

### 30. Recuperación futura
La correspondencia por caso se recupera en todos los ejercicios de M9, en matrices de M11 y en las rutas completas de M13.

### 31. Riesgo de aprendizaje superficial
Memorizar `(3,58)` sin comprender que el principio general es mantener juntos los valores de una misma fila.

### 32. Criterio de transferencia
La habilidad estará disponible cuando pueda identificar correctamente pares en otra tabla con otras variables y detectar que una permutación unilateral destruye la correspondencia.

### 33. Notas de implementación futura
No evaluar mediante código. Puede utilizarse una selección visual de filas/pares. La comprobación debe evaluar correspondencia, no memoria de posiciones.

---
## M9-E2 — Cada persona se vuelve un punto

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
E1 construyó los pares. E2 transforma esa representación en un scatterplot.

La función no debe aparecer como una operación mágica:

```text
PAR
↓
PUNTO
```

es el puente conceptual que justifica `plot(x, y)`.

### 3. Capacidad antes
Comprende que cada caso aporta un par de cantidades que debe mantenerse unido.

### 4. Capacidad después
Puede interpretar un par como un punto, comprender los ejes de un scatterplot y ejecutar `plot(x, y)` con las variables correctas.

### 5. Prerrequisitos
Caso, par, variables cuantitativas, `$`, ejecución de código.

### 6. Gran novedad
- **Sintaxis nueva:** `plot(x, y)`.
- **Concepto nuevo:** un par se representa mediante un punto.
- **Decisión nueva:** primera variable → eje horizontal; segunda → eje vertical.

Estas piezas forman una única unidad: **convertir pares en puntos**.

### 7. Recuperaciones
Recupera `$`, variables cuantitativas y `UN CASO → UN PAR` de E1.

### 8. Contexto sustantivo
Horas de estudio y puntaje de métodos en los 12 casos completos de `encuesta_social`.

### 9. Dataset / objetos
Usar:

```r
encuesta_social$horas_estudio
encuesta_social$puntaje_metodos
```

Caso de referencia:

```text
caso 3 → (3, 58)
```

Los 12 pares están completos.

### 10. Texto para estudiante
Cada caso ya tiene un par.

Ahora podemos representar cada par como un punto.

Para el caso 3:

```text
(3, 58)
```

significa:

```text
3 horas de estudio
→ eje horizontal

58 puntos
→ eje vertical
```

En R:

```r
plot(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

La primera variable ocupa el eje horizontal.

La segunda ocupa el eje vertical.

Cada punto del gráfico representa **una persona/caso con sus dos valores**.

### 11. Modelo mental
```text
CASO
↓
PAR (x, y)
↓
x → horizontal
y → vertical
↓
PUNTO
↓
TODOS LOS PUNTOS
↓
SCATTERPLOT
```

### 12. Representación / código trabajado
Antes de ejecutar:

```text
caso 3
↓
(3,58)
↓
punto aproximadamente en
x = 3
y = 58
```

Código trabajado:

```r
plot(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 13. Starter code
```r
plot(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 14. Acción esperada
1. predecir la ubicación aproximada del caso 3;
2. ejecutar;
3. reconocer eje x y eje y;
4. reconocer que aparecen 12 puntos;
5. explicar qué representa un punto.

### 15. Solución canónica
```r
plot(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 16. Resultado esperado
Scatterplot con 12 puntos.

```text
eje horizontal → horas_estudio
eje vertical   → puntaje_metodos

caso 3         → aproximadamente (3,58)
```

### 17. Criterio semántico de éxito
Comprobar:

- utiliza `plot()`;
- base correcta;
- x = `horas_estudio`;
- y = `puntaje_metodos`;
- scatterplot;
- 12 pares;
- comprende que cada punto representa un caso;
- identifica `(3,58)` como el punto del caso 3;
- no hardcoding.

### 18. Estrategias alternativas válidas
Se acepta:

```r
x <- encuesta_social$horas_estudio
y <- encuesta_social$puntaje_metodos
plot(x, y)
```

No se requiere personalización gráfica.

### 19. Error esperado / misconception
- punto = variable;
- punto = grupo;
- punto = promedio;
- creer que cada punto representa un solo valor;
- invertir ejes sin comprender qué cambió;
- reconstruir manualmente los dos vectores;
- intentar añadir una línea de regresión.

### 20. Feedback correcto
> Bien. Cada punto conserva los dos valores de un mismo caso: horas de estudio en horizontal y puntaje en vertical.

### 21. Feedback resultado correcto / estrategia incorrecta
Si reconstruye manualmente los vectores:

> El gráfico puede verse igual, pero debe depender de las columnas de la base para actualizarse si cambian los datos.

Si intercambia x/y:

> Sigue siendo un scatterplot de las mismas dos variables, pero esta tarea fija `horas_estudio` en horizontal y `puntaje_metodos` en vertical para mantener una lectura común.

### 22. Hint 1
Cada caso aporta dos valores que forman un punto.

### 23. Hint 2
La primera variable va al eje horizontal y la segunda al vertical.

### 24. Hint 3
```r
plot(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 25. Predicción
Sí.

> ¿Dónde aparecerá aproximadamente el punto del caso 3?

Respuesta:

```text
x = 3
y = 58
```

### 26. Tipo de ejercicio
Worked example + ejecución/observación.

### 27. Andamiaje
Alto. El código está completo y un caso concreto se localiza antes de mirar la nube.

### 28. Carga cognitiva
Media. Interactúan par, punto, dos ejes y una función nueva. No se introduce correlación.

### 29. Fading
E2 entrega `plot()` completo. E6 lo recupera dentro de un problema preparado y E7 lo exige sin nombrarlo.

### 30. Recuperación futura
`plot()` se recupera en E6/E7, M10 y M13.

### 31. Riesgo de aprendizaje superficial
Aprender `plot(columna1, columna2)` como forma gráfica sin poder explicar qué representa un punto.

### 32. Criterio de transferencia
Puede producir e interpretar un scatterplot de dos variables nuevas manteniendo x/y y pares correctos.

### 33. Notas de implementación futura
No evaluar estética, `main`, `xlab`, `ylab`, colores ni `pch`. La comprobación debe centrarse en variables, ejes, pares y tipo de gráfico.

---
## M9-E3 — ¿Hacia dónde va la relación?

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
Una vez comprendido qué representa un scatterplot, el estudiante necesita aprender a leer una primera propiedad del patrón: su dirección. E3 evita introducir `cor()` antes de que la dirección tenga significado visual.

### 3. Capacidad antes
Puede leer un scatterplot como una colección de pares/casos.

### 4. Capacidad después
Puede distinguir dirección positiva, negativa y ausencia de una dirección lineal clara sin atribuir causalidad.

### 5. Prerrequisitos
Punto, scatterplot, eje x/eje y y lectura izquierda→derecha.

### 6. Gran novedad
No hay nueva sintaxis. Se practica la lectura conceptual de dirección.

### 7. Recuperaciones
Recupera la interpretación de puntos y ejes de E2.

### 8. Contexto sustantivo
Tres patrones abstractos deliberadamente simples para aislar la dirección.

### 9. Dataset / objetos
Los gráficos se generan con los microdatos locked:

```r
x_pos <- c(1, 2, 3, 4, 5, 6)
y_pos <- c(2, 3, 5, 4, 7, 8)

x_neg <- c(1, 2, 3, 4, 5, 6)
y_neg <- c(8, 7, 5, 6, 3, 2)

x_sin_direccion <- c(1, 2, 3, 4, 5, 6)
y_sin_direccion <- c(4, 7, 2, 6, 3, 5)
```

Los coeficientes correspondientes son referencias internas y no se muestran.

### 10. Texto para estudiante
Mira cada nube de puntos de izquierda a derecha.

No preguntes todavía cuánto vale la correlación.

Pregunta:

> Cuando `x` aumenta, ¿qué tiende a ocurrir con `y`?

Clasifica los tres gráficos:

```text
A
¿x ↑ y tiende a ↑?

B
¿x ↑ y tiende a ↓?

C
¿no aparece una tendencia ascendente o descendente clara?
```

Usaremos tres respuestas:

```text
dirección positiva
dirección negativa
sin dirección lineal clara
```

Importante:

> Una asociación describe cómo cambian juntas dos variables.
>
> El gráfico por sí solo no demuestra que una variable cause la otra.

### 11. Modelo mental
```text
MIRAR DE IZQUIERDA A DERECHA
↓
x ↑
↓
¿QUÉ TIENDE A HACER y?

y ↑
→ dirección positiva

y ↓
→ dirección negativa

sin tendencia clara
→ sin dirección lineal clara
```

### 12. Representación / código trabajado
Los tres scatterplots se muestran ya generados. No se requiere código nuevo.

### 13. Starter code
No se requiere starter code productivo.

### 14. Acción esperada
Clasificar A, B y C y justificar cada respuesta en términos de tendencia.

### 15. Solución canónica
```text
A → dirección positiva
B → dirección negativa
C → sin dirección lineal clara
```

### 16. Resultado esperado
Clasificación correcta de los tres patrones y explicación no causal.

### 17. Criterio semántico de éxito
Comprobar:

- A = positiva;
- B = negativa;
- C = sin dirección lineal clara;
- negativa no se interpreta como “mala”;
- positiva no se interpreta como causalidad;
- no obliga a C a ser positiva o negativa.

### 18. Estrategias alternativas válidas
Se aceptan expresiones como “sube”, “baja”, “tendencia ascendente/descendente” si la interpretación conceptual es correcta.

### 19. Error esperado / misconception
- negativa = relación mala;
- positiva = x causa y;
- clasificar C a la fuerza;
- mirar un punto aislado en vez del patrón;
- asumir que todos los puntos deben seguir exactamente la tendencia.

### 20. Feedback correcto
> Bien. La dirección resume una tendencia del conjunto de puntos, no el comportamiento exacto de cada caso.

### 21. Feedback resultado correcto / estrategia incorrecta
Si responde positiva porque “y es grande”:

> La clasificación coincide, pero la dirección depende de cómo cambia y a medida que x aumenta, no de que los valores de y sean altos.

Si dice que B es “mala”:

> Negativa describe hacia dónde cambia y cuando x aumenta; no es un juicio de valor.

### 22. Hint 1
Lee el gráfico de izquierda a derecha.

### 23. Hint 2
Pregunta qué tiende a pasar con y cuando x aumenta.

### 24. Hint 3
A sube; B baja; C no muestra una dirección lineal clara.

### 25. Predicción
No requiere fase independiente. La clasificación visual es la actividad central.

### 26. Tipo de ejercicio
Clasificación / interpretación visual.

### 27. Andamiaje
Medio. Las opciones conceptuales están dadas, pero la clasificación no.

### 28. Carga cognitiva
Baja-media. No hay sintaxis nueva; se coordinan ejes y tendencia.

### 29. Fading
E3 retira el código trabajado y exige leer el patrón. E4 pedirá una lectura más rica.

### 30. Recuperación futura
Dirección se recupera en E4–E7, M10 y M13.

### 31. Riesgo de aprendizaje superficial
Convertir dirección en una etiqueta visual sin explicar qué tiende a ocurrir con y cuando x aumenta.

### 32. Criterio de transferencia
Puede clasificar la dirección en una nube nueva sin conocer previamente el coeficiente.

### 33. Notas de implementación futura
Los tres gráficos deben utilizar escalas suficientemente comparables para que la clasificación se base en el patrón y no en artefactos visuales.

---
## M9-E4 — No basta con la dirección

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
E3 podría dejar la impresión de que describir una relación consiste solo en decir positiva o negativa.

E4 demuestra que dos nubes pueden compartir dirección y, aun así, mostrar patrones muy distintos.

Prepara el significado posterior de la magnitud de `r` sin introducir `r`.

### 3. Capacidad antes
Puede clasificar la dirección general de un scatterplot.

### 4. Capacidad después
Puede distinguir dirección de concentración, observar forma general y revisar si existen puntos muy alejados antes de resumir numéricamente una relación.

### 5. Prerrequisitos
Scatterplot, dirección positiva/negativa y lectura de una nube completa.

### 6. Gran novedad
No hay sintaxis nueva. Se profundiza la lectura visual del patrón.

### 7. Recuperaciones
Recupera dirección de E3 y la atención a valores alejados desarrollada conceptualmente en M8.

### 8. Contexto sustantivo
Dos relaciones abstractas positivas con diferente concentración alrededor de una tendencia aproximadamente lineal.

### 9. Dataset / objetos
Gráfico A:

```r
x_a <- c(1, 2, 3, 4, 5, 6, 7, 8)
y_a <- c(2.2, 2.8, 4.1, 4.4, 5.8, 6.1, 7.4, 7.9)
```

Referencia interna:

```text
r ≈ 0.9934106276
```

Gráfico B:

```r
x_b <- c(1, 2, 3, 4, 5, 6, 7, 8)
y_b <- c(1, 5, 2, 6, 4, 8, 5, 9)
```

Referencia interna:

```text
r ≈ 0.7703288865
```

No mostrar todavía los coeficientes.

### 10. Texto para estudiante
Los dos gráficos tienen dirección positiva.

Pero no cuentan exactamente la misma historia.

Observa:

```text
A
los puntos siguen muy de cerca una tendencia aproximadamente lineal

B
los puntos también tienden a subir,
pero están bastante más dispersos
```

Antes de resumir una relación, revisaremos cuatro preguntas:

```text
1. ¿HACIA DÓNDE VA?
   → dirección

2. ¿QUÉ FORMA TIENE?
   → aproximadamente lineal / curva / otra

3. ¿QUÉ TAN CONCENTRADOS ESTÁN LOS PUNTOS?
   → más o menos cerca de una tendencia

4. ¿HAY ALGÚN PUNTO MUY ALEJADO DEL PATRÓN?
```

No todos los patrones claros son lineales.

Un patrón curvo también puede contener información importante.

Por eso mirar el gráfico sigue siendo necesario.

### 11. Modelo mental
```text
DIRECCIÓN
↓
NO BASTA

↓

FORMA
+
CONCENTRACIÓN
+
PUNTOS MUY ALEJADOS
```

Idea central:

```text
MISMA DIRECCIÓN
≠
MISMA CONCENTRACIÓN
```

### 12. Representación / código trabajado
Los gráficos A y B están generados. No se muestra `cor()` ni se pide calcular coeficientes.

### 13. Starter code
No se requiere starter code productivo.

### 14. Acción esperada
- reconocer que ambos patrones son positivos;
- identificar A como más concentrado;
- identificar B como más disperso;
- observar que dirección y concentración son distintas;
- utilizar la rutina dirección/forma/concentración/puntos alejados.

### 15. Solución canónica
```text
A → positiva y muy concentrada alrededor de una tendencia lineal
B → positiva, pero más dispersa
```

Conclusión:

> Conocer la dirección no basta.

### 16. Resultado esperado
Descripción comparativa correcta sin calcular `r`.

### 17. Criterio semántico de éxito
Comprobar:

- ambos = dirección positiva;
- A = más concentrado;
- B = más disperso;
- no confunde inclinación con concentración;
- reconoce que la forma debe observarse;
- comprende que un punto muy alejado puede importar.

### 18. Estrategias alternativas válidas
Se aceptan expresiones como “más ajustado”, “menos disperso”, “los puntos siguen más de cerca la tendencia”, siempre que no se conviertan en thresholds numéricos.

### 19. Error esperado / misconception
- misma dirección = misma relación;
- mayor pendiente visual = asociación más fuerte;
- un único punto define la relación;
- solo importa positiva/negativa;
- creer que cualquier patrón debe ser lineal.

### 20. Feedback correcto
> Bien. Ambos patrones son positivos, pero A está mucho más concentrado alrededor de una tendencia aproximadamente lineal.

### 21. Feedback resultado correcto / estrategia incorrecta
Si elige A porque “la línea sube más”:

> A sí muestra un patrón más marcado, pero no por la inclinación. La diferencia importante es qué tan cerca siguen los puntos una tendencia.

Si ignora la forma:

> La dirección es solo una parte de la lectura. Un patrón puede ser claro y no ser lineal.

### 22. Hint 1
Ambos suben. Busca otra diferencia.

### 23. Hint 2
Mira qué tan cerca están los puntos de una tendencia aproximadamente lineal.

### 24. Hint 3
A está más concentrado; B está más disperso.

### 25. Predicción
> ¿Qué gráfico esperas que muestre la asociación lineal más marcada?

Respuesta: A.

### 26. Tipo de ejercicio
Interpretación comparativa.

### 27. Andamiaje
Medio. Las preguntas de inspección están dadas; la comparación debe producirla el estudiante.

### 28. Carga cognitiva
Media. No hay sintaxis nueva; interactúan dirección, forma y concentración.

### 29. Fading
E4 retira totalmente la sintaxis y obliga a interpretar antes de introducir el resumen numérico en E5.

### 30. Recuperación futura
La rutina visual se recupera en E5–E7, M10 y M13.

### 31. Riesgo de aprendizaje superficial
Memorizar “más junto = fuerte” sin comprender que se habla de concentración alrededor de una tendencia lineal y que la forma también importa.

### 32. Criterio de transferencia
Puede comparar dos scatterplots nuevos considerando algo más que el signo de la tendencia.

### 33. Notas de implementación futura
No mostrar los r de A/B en la interfaz antes de E5. Mantener escalas comparables y evitar que la inclinación sea el indicio dominante.

---
## M9-E5 — Resume el patrón con un número

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Después de construir pares, puntos, dirección y lectura rica del scatterplot, el estudiante ya tiene una necesidad genuina de resumen numérico.

E5 introduce `cor()` únicamente después del gráfico y con datos completos, de modo que missing no compita con el significado de `r`.

### 3. Capacidad antes
Puede producir/leer un scatterplot y describir dirección, forma y concentración.

### 4. Capacidad después
Puede calcular e interpretar descriptivamente el coeficiente de correlación lineal de Pearson mediante `cor()` y relacionarlo con el scatterplot.

### 5. Prerrequisitos
Par, scatterplot, dirección, forma, concentración y ausencia de missing en las dos variables.

### 6. Gran novedad
- **Sintaxis nueva:** `cor(x, y)`.
- **Concepto nuevo:** coeficiente de correlación lineal de Pearson `r`.
- **Decisión nueva:** interpretar el coeficiente junto al gráfico.

Missing queda completamente fuera.

### 7. Recuperaciones
Recupera el scatterplot principal y la rutina visual de E2–E4.

### 8. Contexto sustantivo
Horas de estudio y puntaje de métodos en 12 casos completos.

### 9. Dataset / objetos
Usar:

```r
encuesta_social$horas_estudio
encuesta_social$puntaje_metodos
```

12 pares completos.

Coeficiente contractual:

```text
0.7500757095661253
```

### 10. Texto para estudiante
Ya miramos el scatterplot.

Vimos una tendencia:

```text
positiva
+
aproximadamente lineal
+
visible pero no perfecta
```

Ahora queremos resumir numéricamente esa **asociación lineal**.

En este módulo trabajaremos con el coeficiente de correlación lineal de **Pearson**.

Es el coeficiente que `cor()` calcula por defecto.

Antes de ejecutar:

> ¿esperas que `r` sea positivo, negativo o cercano a 0?

Después ejecuta:

```r
cor(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

Más adelante aprenderemos por qué no siempre corresponde utilizar el mismo coeficiente.

### 11. Modelo mental
```text
SCATTERPLOT
↓
PATRÓN APROXIMADAMENTE LINEAL
↓
CORRELACIÓN DE PEARSON
↓
r
↓
SIGNO + MAGNITUD
↓
INTERPRETAR JUNTO AL GRÁFICO
```

### 12. Representación / código trabajado
```r
cor(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

Escala conceptual:

```text
-1 ---------------- 0 ---------------- +1
```

### 13. Starter code
```r
cor(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 14. Acción esperada
1. predecir el signo;
2. ejecutar;
3. leer `r`;
4. interpretar signo;
5. interpretar magnitud lineal sin thresholds rígidos;
6. conectar con scatterplot;
7. rechazar porcentaje, pendiente y causalidad.

### 15. Solución canónica
```r
cor(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 16. Resultado esperado
```text
0.7500757095661253
```

En texto:

```text
r ≈ 0.75
```

Interpretación:

> Asociación lineal positiva y claramente visible, aunque no perfecta.

### 17. Criterio semántico de éxito
Comprobar:

- `cor()`;
- variables correctas;
- 12 pares completos;
- `r ≈ 0.7500757096`;
- signo positivo;
- interpreta asociación lineal;
- conecta con el scatterplot;
- no utiliza thresholds rígidos;
- no interpreta como porcentaje;
- no interpreta como pendiente;
- no añade unidades;
- no afirma causalidad;
- no hardcodea.

### 18. Estrategias alternativas válidas
Se acepta:

```r
x <- encuesta_social$horas_estudio
y <- encuesta_social$puntaje_metodos
cor(x, y)
```

No se considera necesario indicar `method = "pearson"` en este primer encuentro porque Pearson es el default y M10 desarrollará la elección de método.

### 19. Error esperado / misconception
- `r = 0.75` = 75 %;
- `r = 0.75` = pendiente de 0.75;
- `r` tiene unidades de horas o puntos;
- `r` positivo = estudiar más causa mejor puntaje;
- “0.75 es fuerte porque supera 0.5” como regla universal;
- `r` cerca de 0 = ausencia de toda relación posible;
- mirar solo `r` e ignorar el gráfico;
- hardcodear 0.75.

### 20. Feedback correcto
> Bien. `r ≈ 0.75` resume una asociación lineal positiva coherente con el scatterplot. El coeficiente complementa al gráfico; no lo reemplaza.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `0.75`:

> El número coincide aproximadamente, pero debe calcularse desde las dos variables.

Si dice “75 %”:

> `r = 0.75` no es un porcentaje.

Si interpreta pendiente:

> `r` no indica cuántos puntos cambia el puntaje por cada hora adicional.

Si concluye causalidad:

> La correlación describe asociación, no demuestra que una variable cause la otra.

### 22. Hint 1
Ya observaste el patrón. Ahora necesitas resumir numéricamente su asociación lineal.

### 23. Hint 2
La función trabajada para ese resumen es `cor()`.

### 24. Hint 3
```r
cor(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos
)
```

### 25. Predicción
Sí, obligatoria:

> ¿esperas `r` positivo, negativo o cercano a 0?

Respuesta:

```text
positivo
```

No pedir decimal exacto.

### 26. Tipo de ejercicio
Worked example + interpretación.

### 27. Andamiaje
Alto. La función y las variables están dadas.

### 28. Carga cognitiva
Media. La única gran novedad es `cor()` + significado de `r`; missing se excluye deliberadamente.

### 29. Fading
E5 entrega `cor()` completo. E6 lo recupera dentro de una ruta multietapa y E7 lo exige sin nombrarlo.

### 30. Recuperación futura
`cor()` reaparece en E6/E7, M10, M11 y M13.

### 31. Riesgo de aprendizaje superficial
Convertir correlación en una etiqueta numérica desconectada de la forma del scatterplot.

### 32. Criterio de transferencia
Puede calcular e interpretar `r` sobre otra pareja completa y justificar el resultado junto a un scatterplot.

### 33. Notas de implementación futura
Usar tolerancia numérica.

No introducir missing.

Puede incluirse una nota visual conceptual con:

```text
x = -3 -2 -1 0 1 2 3
y =  9  4  1 0 1 4 9
```

para mostrar que un patrón curvo claro puede tener Pearson `r = 0`; no pedir código ni convertirlo en nuevo objetivo.

---
## M9-E6 — Prepara los pares antes de correlacionar

### 1. Rol pedagógico
RECUPERACIÓN, con micro-novedad funcional `use = "complete.obs"`.

### 2. Por qué existe
E5 introdujo `cor()` con datos completos.

E6 recupera una realidad ya conocida desde M6: pueden faltar valores. En una relación bivariada la unidad analítica es el par, por lo que necesitamos saber qué casos tienen disponibles **ambas** cantidades.

También recupera M5 dentro de una pregunta sustantiva real.

### 3. Capacidad antes
Puede preparar subconjuntos, diagnosticar missing, producir un scatterplot y calcular una correlación en datos completos.

### 4. Capacidad después
Puede preparar un subgrupo, diagnosticar missing bivariado, reconocer el número de pares completos y hacer que gráfico y correlación describan la misma muestra analítica.

### 5. Prerrequisitos
Desde M5:

- `filter()`;
- `select()`;
- `|>`.

Desde M6:

- `NA`;
- `is.na()`;
- `sum(is.na())`;
- N total vs N disponible.

Desde M9:

- par;
- `plot()`;
- `cor()`;
- asociación ≠ causalidad.

### 6. Gran novedad
No hay gran novedad curricular.

Micro-novedad funcional:

```r
use = "complete.obs"
```

Su significado debe comprenderse, pero no se exige recuerdo autónomo fuerte.

### 7. Recuperaciones
Recupera preparación de M5, missing de M6 y `plot()`/`cor()` de M9. No exige media, mediana ni desviación estándar.

### 8. Contexto sustantivo
Entre las personas que trabajan, estudiar cómo se relacionan horas de trabajo semanal y horas de sueño.

### 9. Dataset / objetos
Partir de la vista contractual de `encuesta_social`.

Después de filtrar `trabaja == "Sí"`:

```text
id   horas_trabajo   horas_sueno
1    20              8.4
2    35              7.7
4    25              7.6
5    40              7.6
7    30              NA
8    45              7.1
10   38              7.7
12   32              7.4
```

Casos del subgrupo:

```text
8
```

Missing:

```text
horas_trabajo → 0
horas_sueno   → 1
```

Pares completos:

```text
7
```

Coeficiente con pares completos:

```text
-0.7600015202458091
```

### 10. Texto para estudiante
Queremos responder:

> Entre las personas que trabajan,
> ¿cómo se relacionan las horas de trabajo semanal
> y las horas de sueño?

Primero prepara los datos:

- conserva solo quienes trabajan;
- conserva `id`, `horas_trabajo` y `horas_sueno`.

Después:

1. revisa cuántos valores faltan en cada cantidad;
2. determina cuántos casos pueden formar un par completo;
3. representa la relación;
4. calcula la correlación utilizando los pares completos;
5. interpreta el resultado.

Importante:

> Tener 8 personas en el subgrupo no significa automáticamente tener 8 pares disponibles.

### 11. Modelo mental
```text
PREGUNTA
↓
SUBGRUPO
↓
DOS VARIABLES
↓
REVISAR MISSING
↓
¿TIENE x?
¿TIENE y?
↓
SI TIENE AMBOS
→ PAR COMPLETO
↓
MISMA MUESTRA ANALÍTICA
↓
SCATTERPLOT
+
CORRELACIÓN
```

### 12. Representación / código trabajado
La nueva opción se introduce solo después del diagnóstico:

```r
cor(
  datos_trabajan$horas_trabajo,
  datos_trabajan$horas_sueno,
  use = "complete.obs"
)
```

Significado:

> usar únicamente casos donde ambas variables tienen valores disponibles para este cálculo.

### 13. Starter code
```r
datos_trabajan <- encuesta_social |>
  filter(__________________) |>
  select(____, _____________, ____________)

# revisa cuántos valores faltan en cada cantidad


# representa la relación


# calcula la correlación usando los pares completos
```

### 14. Acción esperada
1. completar pipeline;
2. contar missing de ambas variables;
3. identificar 7 pares completos;
4. producir scatterplot;
5. calcular correlación con observaciones completas;
6. interpretar signo;
7. explicar que la base no fue modificada.

### 15. Solución canónica
```r
datos_trabajan <- encuesta_social |>
  filter(trabaja == "Sí") |>
  select(id, horas_trabajo, horas_sueno)

sum(is.na(datos_trabajan$horas_trabajo))

sum(is.na(datos_trabajan$horas_sueno))

plot(
  datos_trabajan$horas_trabajo,
  datos_trabajan$horas_sueno
)

cor(
  datos_trabajan$horas_trabajo,
  datos_trabajan$horas_sueno,
  use = "complete.obs"
)
```

### 16. Resultado esperado
Subgrupo:

```text
8 casos
```

Missing:

```text
horas_trabajo = 0
horas_sueno   = 1
```

Pares completos:

```text
7
```

Scatterplot:

```text
7 puntos analíticos completos
```

Correlación:

```text
-0.7600015202458091
```

En texto:

```text
r ≈ -0.76
```

Interpretación:

> Entre los siete pares completos, más horas de trabajo tienden a aparecer junto con menos horas de sueño.

### 17. Criterio semántico de éxito
Comprobar:

- objeto `datos_trabajan`;
- `filter(trabaja == "Sí")`;
- `select(id, horas_trabajo, horas_sueno)`;
- casos 1,2,4,5,7,8,10,12;
- 0 missing en `horas_trabajo`;
- 1 missing en `horas_sueno`;
- 7 pares completos;
- scatterplot correcto;
- gráfico y correlación describen los mismos pares;
- `cor()` correcto;
- `use = "complete.obs"`;
- `r ≈ -0.7600015202`;
- interpretación negativa;
- no causalidad;
- fuente intacta;
- no hardcoding.

### 18. Estrategias alternativas válidas
Se acepta guardar las dos variables en objetos después de preparar `datos_trabajan`.

Se aceptan estrategias semánticamente equivalentes siempre que:

- dependan de los datos;
- preserven el mismo subgrupo;
- diagnostiquen missing antes de omitir;
- gráfico y correlación usen los mismos pares completos.

No introducir `!` ni `complete.cases()` como alternativas curriculares.

### 19. Error esperado / misconception
- 8 casos = 8 pares;
- 0 horas = missing;
- ignorar el NA;
- calcular correlación sin decidir qué casos entran;
- creer que `use = "complete.obs"` limpia la base;
- reconstruir manualmente los 7 pares;
- utilizar `na.rm = TRUE` dentro de `cor()`;
- añadir media/mediana/sd innecesariamente;
- concluir causalidad.

### 20. Feedback correcto
> Bien. Preparaste el subgrupo, revisaste los missing y usaste los siete pares completos para representar y resumir la misma relación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si dice 8 pares:

> El subgrupo tiene 8 personas, pero una no tiene `horas_sueno`. Solo 7 casos aportan ambos valores.

Si usa `complete.obs` sin diagnosticar:

> El cálculo puede funcionar, pero falta una decisión importante: primero debes saber cuántos datos faltan y cuántos pares entrarán.

Si cree que se borró la fila:

> La opción afecta a este cálculo; no elimina el `NA` ni modifica `datos_trabajan` o `encuesta_social`.

### 22. Hint 1
Para formar un punto necesitas disponibles ambas cantidades del mismo caso.

### 23. Hint 2
Primero prepara el subgrupo y revisa los missing. Después trabaja con los pares completos.

### 24. Hint 3
```r
cor(
  datos_trabajan$horas_trabajo,
  datos_trabajan$horas_sueno,
  use = "complete.obs"
)
```

### 25. Predicción
No hay fase separada. La tarea ya exige varias decisiones recuperadas.

### 26. Tipo de ejercicio
Recuperación integrada.

### 27. Andamiaje
Medio. El pipeline contiene huecos y las operaciones bivariadas aparecen solo como comentarios semánticos.

### 28. Carga cognitiva
Media-alta. Coordina M5 + M6 + M9, pero no introduce una nueva habilidad nuclear.

### 29. Fading
Respecto de E5, se retira la función `cor()` del starter. E7 retirará también la preparación/missing para concentrarse en transferencia bivariada.

### 30. Recuperación futura
La idea de pares completos se recupera en M10–M11 y M13. `use = "complete.obs"` puede requerir recordatorio.

### 31. Riesgo de aprendizaje superficial
Aprender `use = "complete.obs"` como receta sin saber cuántos pares se excluyen o por qué.

### 32. Criterio de transferencia
Puede preparar otro subgrupo, diagnosticar missing bivariado y mantener una muestra analítica coherente entre gráfico y correlación.

### 33. Notas de implementación futura
Perturbation tests muy recomendados:

- cambiar quién trabaja;
- mover el NA;
- añadir/quitar un NA;
- modificar horas;
- reordenar filas.

El grader debe evaluar por componentes.

No introducir `complete.cases()` ni `!`.

---
## M9-E7 — Otra pregunta, otra base

### 1. Rol pedagógico
TRANSFERENCIA.

### 2. Por qué existe
El cierre debe demostrar que el estudiante puede reconocer dos cantidades nuevas, producir autónomamente la representación gráfica y el resumen lineal, y explicar los límites de la conclusión sin que la consigna nombre las funciones.

### 3. Capacidad antes
Ha recorrido caso→par→punto→scatterplot→lectura visual→correlación y recuperó missing bivariado.

### 4. Capacidad después
Puede transferir `plot()` + `cor()` + interpretación conjunta a una base nueva sin sintaxis indicada.

### 5. Prerrequisitos
Variables cuantitativas, par, scatterplot, dirección, forma, concentración, `plot()`, `cor()` y asociación ≠ causalidad.

### 6. Gran novedad
Ninguna. Es transferencia.

### 7. Recuperaciones
Recupera las capacidades centrales de E1–E5. Missing no se incluye porque ya fue recuperado en E6.

### 8. Contexto sustantivo
Tiempo de lectura y puntaje de comprensión en una nueva encuesta de diez casos.

### 9. Dataset / objetos
```text
encuesta_lectura

id   minutos_lectura   puntaje_comprension
1    15                50
2    35                57
3    25                66
4    55                84
5    20                59
6    50                69
7    30                68
8    60                83
9    40                55
10   45                62
```

Sin missing.

Coeficiente contractual:

```text
0.760025069611547
```

### 10. Texto para estudiante
Queremos estudiar si el tiempo de lectura y el puntaje de comprensión parecen cambiar juntos.

Obtén evidencia para responder:

1. representa gráficamente la relación;
2. describe la dirección y la forma general del patrón;
3. obtén un resumen numérico de la asociación lineal;
4. interpreta el signo y la magnitud del resultado;
5. explica qué NO podemos concluir solamente con estos datos.

No se indican las funciones.

Decide qué herramientas del módulo necesitas.

### 11. Modelo mental
```text
BASE NUEVA
↓
DOS CANTIDADES
↓
MISMOS CASOS
↓
PARES
↓
SCATTERPLOT
↓
DIRECCIÓN + FORMA + CONCENTRACIÓN
↓
r
↓
INTERPRETAR
↓
RECONOCER LÍMITES
```

### 12. Representación / código trabajado
No se entrega worked example. El estudiante dispone únicamente de la base y la consigna.

### 13. Starter code
```r
# representa la relación entre las dos cantidades


# resume numéricamente la asociación lineal
```

### 14. Acción esperada
1. reconocer ambas variables como cuantitativas;
2. producir scatterplot;
3. describir patrón positivo aproximadamente lineal con dispersión;
4. producir correlación;
5. interpretar `r ≈ 0.76`;
6. rechazar porcentaje, pendiente y causalidad.

### 15. Solución canónica
```r
plot(
  encuesta_lectura$minutos_lectura,
  encuesta_lectura$puntaje_comprension
)

cor(
  encuesta_lectura$minutos_lectura,
  encuesta_lectura$puntaje_comprension
)
```

### 16. Resultado esperado
Scatterplot:

```text
10 puntos
dirección general positiva
forma aproximadamente lineal
dispersión visible
```

Correlación:

```text
0.760025069611547
```

En texto:

```text
r ≈ 0.76
```

Interpretación esperada:

> Los casos con más minutos de lectura tienden a presentar puntajes mayores de comprensión. La asociación lineal es positiva y claramente visible, aunque no perfecta. Este resultado no demuestra causalidad.

### 17. Criterio semántico de éxito
Evaluar por componentes.

**Variables**
- ambas representan cantidades.

**Scatterplot**
- base correcta;
- x = `minutos_lectura`;
- y = `puntaje_comprension`;
- 10 pares;
- `plot()`.

**Correlación**
- `cor()`;
- variables correctas;
- `r ≈ 0.7600250696`;
- tolerancia numérica.

**Interpretación**
- dirección positiva;
- aproximadamente lineal;
- dispersión visible;
- magnitud contextual;
- no porcentaje;
- no pendiente;
- no causalidad.

**Estrategia**
- depende de la base;
- no hardcoding;
- no vectores reconstruidos manualmente.

### 18. Estrategias alternativas válidas
Se acepta:

```r
x <- encuesta_lectura$minutos_lectura
y <- encuesta_lectura$puntaje_comprension

plot(x, y)
cor(x, y)
```

No se exige personalización gráfica.

No se exige missing porque la base está completa.

### 19. Error esperado / misconception
- elegir ruta categórica;
- producir solo el gráfico;
- producir solo `r`;
- invertir la interpretación del signo;
- `0.76 = 76 %`;
- `0.76 = pendiente`;
- afirmar causalidad;
- reconstruir manualmente ambos vectores;
- hardcodear el coeficiente.

### 20. Feedback correcto
> Bien. Representaste los mismos pares visualmente y numéricamente, interpretaste la asociación lineal y mantuviste separados asociación y causalidad.

### 21. Feedback resultado correcto / estrategia incorrecta
Si solo entrega `r`:

> El coeficiente no reemplaza al scatterplot. Necesitamos comprobar visualmente dirección, forma y concentración.

Si hardcodea:

> El número coincide, pero debe calcularse desde `encuesta_lectura`.

Si concluye causalidad:

> Estos datos muestran asociación. No bastan para afirmar que más lectura cause un puntaje mayor.

### 22. Hint 1
Primero convierte cada par en un punto. Después resume numéricamente el patrón lineal.

### 23. Hint 2
Recupera las dos herramientas centrales del módulo: una gráfica y una numérica.

### 24. Hint 3
```r
plot(
  encuesta_lectura$minutos_lectura,
  encuesta_lectura$puntaje_comprension
)

cor(
  encuesta_lectura$minutos_lectura,
  encuesta_lectura$puntaje_comprension
)
```

### 25. Predicción
No se añade una predicción ritual. La interpretación del scatterplot antes del coeficiente cumple la función de razonamiento previo.

### 26. Tipo de ejercicio
Transferencia cercana.

### 27. Andamiaje
Bajo. Solo quedan dos comentarios estructurales.

### 28. Carga cognitiva
Media. No hay sintaxis nueva ni missing; la dificultad está en seleccionar herramientas e interpretar.

### 29. Fading
Máximo fading del módulo: la consigna no nombra `plot()` ni `cor()`.

### 30. Recuperación futura
M10 parte de esta capacidad; M11 y M13 vuelven a utilizar scatterplots/correlaciones con menos instrucciones.

### 31. Riesgo de aprendizaje superficial
Memorizar “dos numéricas = cor()” y omitir la inspección gráfica o los límites de la conclusión.

### 32. Criterio de transferencia
Existe transferencia cuando puede repetir la ruta sobre otra base cuantitativa y explicar conjuntamente patrón gráfico, `r` y límites causales.

### 33. Notas de implementación futura
Perturbation tests recomendados:

- reordenar filas completas → `r` no cambia;
- cambiar un puntaje → gráfico y `r` cambian;
- romper los pares → la relación cambia.

No introducir inferencia.


---

# Cierre conceptual de M9 y puente a M10

Cerrar M9 con:

> Ya podemos representar dos cantidades mediante un scatterplot,
> describir su patrón
> y resumir una asociación lineal con el coeficiente de Pearson.
>
> Pero no todos los patrones tienen la misma forma.
>
> Un solo coeficiente no necesariamente describe igual de bien
> todas las relaciones.
>
> **¿Cómo decidimos qué correlación utilizar**
> **y qué evidencia tenemos sobre la asociación observada?**

Detenerse ahí.

M9 no introduce todavía:

- Spearman;
- rangos;
- `method = "spearman"`;
- `cor.test()`;
- H0;
- p-value;
- intervalos de confianza;
- significancia.

# Retención esperada después de una semana

## Comprensión
Debe explicar:

> dos cantidades se relacionan porque sus dos valores pertenecen al mismo caso.

Debe recordar:

> cada punto de un scatterplot representa un caso.

Debe reconocer:

```text
dirección positiva
dirección negativa
sin dirección lineal clara
```

Debe revisar antes de interpretar:

```text
dirección
forma
concentración
puntos muy alejados
```

Debe comprender:

```text
signo de r
→ dirección

distancia respecto de 0
→ cuán marcada es la asociación lineal
```

Debe recordar:

```text
r ≠ pendiente
r ≠ porcentaje
r no tiene las unidades originales
correlación ≠ causalidad
```

Debe comprender:

> un `r` cercano a 0 no descarta necesariamente un patrón no lineal.

## Producción
Con poca ayuda debe poder producir:

```r
plot(x, y)
```

y:

```r
cor(x, y)
```

## Missing
Debe recordar:

> para formar un punto y calcular una correlación necesitamos un par completo.

Puede requerir recordatorio de:

```r
use = "complete.obs"
```

Eso es aceptable porque es funcional.

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 3
- PRÁCTICA: 2
- RECUPERACIÓN: 1
- TRANSFERENCIA: 1
- INTEGRACIÓN: 0

## Porcentaje local de gran novedad
3 de 7 ≈ 42.9 %.

No se modifican etiquetas artificialmente.

El control de novedad se interpreta en la arquitectura global de 88 ejercicios.

Cada pantalla de M9 conserva como máximo una gran unidad de aprendizaje.

## Trayectoria de habilidades

```text
plot()
encuentro M9-E2
→ lectura/práctica M9-E3/E4
→ recuperación M9-E6
→ producción M9-E7
→ recuperación M10
→ transferencia M13
```

```text
cor()
encuentro M9-E5
→ recuperación M9-E6
→ producción M9-E7
→ elección M10
→ recuperación M11
→ transferencia M13
```

```text
use = "complete.obs"
encuentro funcional M9-E6
→ puede requerir recordatorio posterior
```

```text
filter()/select()/|>
recuperación M9-E6
```

```text
is.na()
recuperación M9-E6
```

## Habilidades nucleares consolidadas relativamente
- caso → par;
- par → punto;
- scatterplot;
- `plot()`;
- dirección;
- forma;
- concentración;
- inspección de puntos alejados;
- correlación lineal;
- Pearson descriptivo;
- `cor()`;
- lectura del signo;
- magnitud lineal sin thresholds rígidos;
- gráfico + coeficiente;
- asociación ≠ causalidad;
- pares completos;
- misma muestra analítica.

## Habilidad funcional
- `use = "complete.obs"`.

## Habilidades pospuestas
- Spearman;
- `method = "spearman"`;
- `cor.test()`;
- hipótesis nula;
- p-values;
- intervalos de confianza;
- significancia;
- regresión;
- pendiente/intercepto como parámetros;
- R²;
- matrices de correlación;
- múltiples correlaciones;
- causalidad formal.

## Riesgos de sobrecarga controlados
- E1 no contiene código.
- E2 no contiene correlación.
- E3/E4 no contienen sintaxis nueva.
- E5 no contiene missing.
- E6 integra varias habilidades, pero `complete.obs` es solo funcional y no recupera descriptivos univariados.
- E7 elimina missing y preparación para concentrarse en transferencia de `plot()` + `cor()`.

## Checkpoint
No.

M9 prepara Checkpoint D de M10.

# Contrato de datos

## `encuesta_social`
M9 fija la vista contractual:

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

M10–M12 pueden añadir columnas, pero no cambiar estas sin actualización deliberada del contrato.

## `encuesta_lectura`
La base de transferencia queda locked como:

```text
id   minutos_lectura   puntaje_comprension
1    15                50
2    35                57
3    25                66
4    55                84
5    20                59
6    50                69
7    30                68
8    60                83
9    40                55
10   45                62
```

# Declaración de lock

M9 queda pedagógicamente cerrado con 7 ejercicios.

- **Sintaxis nuclear introducida:** `plot(x, y)`, `cor(x, y)`.
- **Habilidad funcional introducida:** `use = "complete.obs"`.
- **Conceptos nucleares:** caso → par → punto, scatterplot, dirección, forma, concentración, asociación lineal, Pearson `r`, interpretación conjunta gráfico + coeficiente.
- **Missing bivariado:** E6 con diagnóstico → pares completos → misma muestra analítica.
- **Producción final:** M9-E7 produce autónomamente `plot()` + `cor()` en una base nueva.
- **Habilidades pospuestas:** Spearman, `cor.test()`, inferencia, regresión y matrices.
- **Recuperación futura:** M10–M11 y M13.
- **Puente a M10:** describir una asociación lineal → decidir qué correlación utilizar e introducir evidencia inferencial.

# M9 PEDAGOGICALLY LOCKED
