# Social R — Módulo 10
## Elegir y evaluar una correlación

### Estado
Diseño pedagógico canónico — **LOCKED** — preimplementación.

### Capacidad antes
Puede representar dos cantidades, describir visualmente su relación y resumir una asociación lineal mediante Pearson.

### Capacidad después
Puede elegir razonadamente entre Pearson y Spearman en situaciones introductorias, reconocer cuándo ninguno de los dos resume adecuadamente un patrón, y utilizar `cor.test()` para interpretar una asociación distinguiendo magnitud, evidencia estadística e incertidumbre.

### Pregunta central
¿Qué correlación describe mejor el patrón y qué nos dice la evidencia estadística sobre la asociación observada?

### Modelo mental
`PREGUNTA → SCATTERPLOT → DESCRIBIR FORMA → ¿LINEAL? / ¿MONÓTONA? → ELEGIR PEARSON / SPEARMAN / NINGUNO → SI CORRESPONDE cor.test() → COEFICIENTE OBSERVADO + H0 + p + IC CUANDO CORRESPONDA → SEPARAR MAGNITUD / EVIDENCIA / INCERTIDUMBRE → INTERPRETAR → RECONOCER LÍMITES`

### Principio pedagógico central
M10 consolida una regla anterior del curso:

> **MIRAR ANTES DE ELEGIR.**

No:

```text
NOMBRE DE LA VARIABLE
↓
MÉTODO
```

No:

```text
NORMAL
→ PEARSON

NO NORMAL
→ SPEARMAN
```

No:

```text
HAY UN PUNTO MUY ALEJADO
→ SPEARMAN
```

No:

```text
NO ES LINEAL
→ SPEARMAN AUTOMÁTICAMENTE
```

Sí:

```text
SCATTERPLOT
↓
FORMA
↓
TIPO DE ASOCIACIÓN
↓
MÉTODO
```

La elección introductoria queda:

```text
APROXIMADAMENTE LINEAL
→ PEARSON

MONÓTONA PERO CLARAMENTE NO LINEAL
→ SPEARMAN

NO LINEAL Y NO MONÓTONA
→ NINGUNO DE LOS DOS RESUME BIEN POR SÍ SOLO
```

“Ninguno” no significa ausencia de relación. Significa que ninguno de esos dos coeficientes representa adecuadamente por sí solo la forma observada.

### Habilidades nucleares
Al terminar M10, el estudiante debe poder:

- mirar el scatterplot antes de seleccionar un coeficiente;
- explicar que Pearson resume asociación lineal;
- explicar que Spearman es una medida basada en el orden o rango de los casos;
- reconocer una relación monotónica en lenguaje introductorio;
- comprender que una relación monotónica puede ser curva;
- comprender que una relación no lineal no implica automáticamente Spearman;
- reconocer un patrón no monotónico que ni Pearson ni Spearman resumen adecuadamente por sí solos;
- evitar la regla falsa “no normal = Spearman”;
- evitar la regla falsa “punto muy alejado = Spearman”;
- usar `method = "pearson"` y `method = "spearman"` para hacer explícita una elección;
- calcular Spearman mediante `cor(..., method = "spearman")`;
- interpretar el coeficiente de Spearman como `rho` sin tratarlo como porcentaje;
- pasar de una descripción muestral a una pregunta inferencial;
- ejecutar `cor.test()` con el método elegido;
- localizar el estimate y el p-value en un output de `cor.test()`;
- localizar el intervalo de confianza cuando el método/output lo proporciona;
- distinguir correlación observada en la muestra de asociación poblacional;
- formular H0 como un escenario de asociación poblacional igual a cero para el coeficiente utilizado;
- interpretar el p-value como información sobre compatibilidad de los datos con el escenario nulo;
- evitar interpretar p como probabilidad de H0;
- evitar interpretar p como tamaño de la asociación;
- comprender que `.05` es una convención y no una frontera natural;
- reconocer “estadísticamente significativo” como vocabulario secundario y no como conclusión sustantiva;
- interpretar el intervalo de confianza como información sobre incertidumbre/precisión;
- evitar la interpretación “95 % de probabilidad de que el parámetro esté dentro”;
- distinguir magnitud, evidencia estadística e incertidumbre;
- reconocer que una misma magnitud observada puede acompañarse de diferente p e incertidumbre cuando cambia la cantidad de información;
- comprender que Pearson y Spearman no producen exactamente el mismo conjunto de componentes en `cor.test()` de R base;
- mantener correlación e inferencia separadas de causalidad;
- completar de manera autónoma una ruta bivariada en un contexto nuevo.

### Habilidades funcionales
Son funcionales, no nucleares:

- reconocer que `t` y `df` forman parte del output de Pearson sin calcularlos ni interpretarlos;
- reconocer que `cor.test(..., method = "spearman")` de R base no devuelve el mismo intervalo de confianza estándar de Pearson;
- reconocer el término “estadísticamente significativo” sin reducir la interpretación a esa etiqueta.

### Habilidades recuperadas
M10 recupera:

- variable cuantitativa por significado;
- caso → par → punto;
- scatterplot;
- `plot(x, y)`;
- dirección;
- forma;
- concentración;
- inspección de puntos alejados;
- `cor()`;
- Pearson descriptivo;
- signo y magnitud de `r`;
- correlación ≠ causalidad;
- pares completos como conocimiento disponible;
- lectura de objetos y outputs;
- `$`.

M10-E7 no recupera missing para evitar sobrecarga.

### Habilidades pospuestas
No se introducen:

- `rank()` como habilidad;
- fórmula manual de Spearman;
- diferencias de rangos y d²;
- variables ordinales como nueva taxonomía;
- Shapiro-Wilk;
- pruebas de normalidad;
- normalidad bivariada formal;
- diagnóstico formal de supuestos;
- Kendall;
- `exact =`;
- `continuity =`;
- corrección por ties;
- teoría de p-values exactos/asintóticos;
- potencia estadística formal;
- tamaño muestral óptimo;
- regresión;
- pendiente/intercepto como parámetros;
- R²;
- matrices de correlaciones;
- corrección por comparaciones múltiples;
- inferencia causal.

### Sintaxis nueva
- `method = "spearman"` dentro de `cor()`;
- `method = "pearson"` como elección explícita desde M10;
- `cor.test()`.

### Sintaxis recuperada
- `plot()`;
- `cor()`;
- `$`;
- objetos y ejecución.

### Sintaxis que NO se introduce
No se introducen como contenido:

```text
rank()
shapiro.test()
exact =
continuity =
matrix()
lm()
```

### Dataset / contrato de datos
M10 conserva íntegramente la vista contractual de `encuesta_social` fijada por M9:

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

M10 no modifica ninguna de esas celdas.

M10 añade dos nuevas columnas contractuales:

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

Desde M10, `edad` y `horas_ocio` también quedan locked. M11–M12 pueden añadir nuevas columnas, pero no modificar silenciosamente ninguna columna ya fijada.

### Objetos pedagógicos auxiliares
Patrón monotónico curvo de E1–E3:

```r
x_curva <- c(1, 2, 3, 4, 5, 6, 7, 8)

y_curva <- c(
  1, 2, 4, 8, 16, 32, 64, 128
)
```

Propiedades contractuales:

```text
Pearson ≈ 0.8504406503
Spearman = 1
```

Patrón en U de E3:

```r
x_u <- c(
  -4, -3, -2, -1,
   1,  2,  3,  4
)

y_u <- c(
  16, 9, 4, 1,
   1, 4, 9, 16
)
```

Propiedades contractuales:

```text
Pearson = 0
Spearman = 0
```

### Base de transferencia / Checkpoint D
M10-E8 utiliza:

```text
encuesta_emprendimiento

id   antiguedad_anos   ventas_mensuales
1    1                 100
2    2                 110
3    3                 120
4    4                 140
5    5                 180
6    6                 300
7    7                 800
8    8                 3000
```

Sin missing y sin ties.

Referencias:

```text
Pearson ≈ 0.7095690774
Spearman = 1
```

En el test Spearman con ocho pares sin empates y orden perfecto:

```text
S = 0
rho = 1
p ≈ 0.0000496031746
```

### Política Pearson / Spearman
Pearson:

```text
ASOCIACIÓN APROXIMADAMENTE LINEAL
→ PEARSON
```

Spearman:

```text
ASOCIACIÓN MONÓTONA
+
ORDEN/RANGOS
→ SPEARMAN
```

Tercera ruta:

```text
NO LINEAL
+
NO MONÓTONA
→ NINGUNO DE LOS DOS RESUME BIEN POR SÍ SOLO
```

### Política de normalidad
No se enseña:

```text
NORMAL → PEARSON
NO NORMAL → SPEARMAN
```

Las condiciones inferenciales formales quedan pospuestas. La decisión introductoria se construye desde el patrón bivariado que se quiere resumir.

### Política de puntos alejados
No se enseña:

```text
PUNTO MUY ALEJADO → SPEARMAN
```

Un punto alejado activa inspección y cautela, no una regla automática de selección.

### Política de inferencia
La transición conceptual ocurre en E4:

```text
MUESTRA
↓
CORRELACIÓN OBSERVADA
↓
PREGUNTA SOBRE ASOCIACIÓN POBLACIONAL
↓
cor.test()
```

`cor.test()` no se presenta como “cor() + p”.

### Política de H0
Para Pearson:

> Escenario de referencia donde la correlación lineal poblacional es cero.

Para Spearman:

> Escenario de referencia donde la asociación de rangos poblacional medida por Spearman es cero.

No se dice “no existe ninguna relación”.

### Política de p-value
Definición introductoria:

> El p-value indica qué tan incompatibles son los datos observados con el escenario nulo utilizado por el test.

Protecciones:

```text
p ≠ probabilidad de H0
p ≠ tamaño del efecto
p ≠ probabilidad de causalidad
p pequeño ≠ efecto grande
p grande ≠ efecto exactamente 0
```

### Política de .05 y significancia
`.05` se presenta solo como umbral convencional frecuente.

“Estadísticamente significativo” puede aparecer como vocabulario secundario, nunca como interpretación final.

### Política de intervalo de confianza
Para Pearson:

> El intervalo muestra un rango de valores de correlación poblacional compatibles con los datos y con el procedimiento utilizado.

Además:

> Un intervalo más estrecho indica mayor precisión.

No se enseña:

> “Existe 95 % de probabilidad de que la correlación poblacional esté dentro de este intervalo”.

### Política de outputs asimétricos
En R base:

```text
PEARSON
→ estimate + p + IC
```

cuando existen suficientes pares completos.

```text
SPEARMAN
→ rho + p
```

No se exige un IC que la salida estándar no proporciona.

### Política de causalidad
Regla estable:

```text
CORRELACIÓN
+
p PEQUEÑO
≠
CAUSALIDAD
```

### Estrategia de scaffolding
1. E1: diferencia conceptual Pearson/Spearman y sintaxis Spearman completamente trabajada.
2. E2: completion de `method = "spearman"`.
3. E3: elegir entre Pearson/Spearman/ninguno con gráficos.
4. E4: worked example de `cor.test()` Pearson y lectura de output.
5. E5: output dado; interpretar H0/p sin escribir código.
6. E6: comparar outputs con mismo `r` y distinto N.
7. E7: comentarios mínimos; ruta Pearson completa.
8. E8: base nueva; ruta Spearman completa.

### Estrategia de fading
`COMPRENDER → COMPLETAR → ELEGIR → OBSERVAR INFERENCIA → INTERPRETAR H0/p → SEPARAR DIMENSIONES → RECUPERAR RUTA → TRANSFERIR`

### Riesgos cognitivos
- “no normal = Spearman”;
- “no lineal = Spearman”;
- “punto alejado = Spearman”;
- tratar Spearman como “Pearson robusto”;
- confundir monotonicidad con linealidad;
- creer que toda curva es monotónica;
- confundir `rho` con porcentaje;
- elegir método por nombre de variable;
- tratar `cor.test()` como un comando mágico que prueba la relación;
- H0 = “no existe ninguna relación”;
- p-value = probabilidad de H0;
- p-value = probabilidad de azar;
- p pequeño = efecto grande;
- p grande = efecto exactamente cero;
- .05 = frontera natural;
- significativo = importante;
- IC = rango de observaciones;
- IC = 95 % de probabilidad posterior;
- exigir el mismo IC en Spearman;
- confundir magnitud, evidencia e incertidumbre;
- olvidar que inferencia correlacional tampoco demuestra causalidad.

### Número de ejercicios
8

# Mapa del módulo

| ID | Título | Rol | Gran novedad | Recuperación | Carga |
|---|---|---|---|---|---|
| M10-E1 | No todas las relaciones son lineales | NOVEDAD | Pearson lineal vs Spearman monotónico/rangos | M9 scatterplot + Pearson | media |
| M10-E2 | Una relación basada en rangos | PRÁCTICA | ninguna | `cor()` + `method = "spearman"` | baja-media |
| M10-E3 | Elige antes de ejecutar | INTEGRACIÓN | ninguna | forma + Pearson/Spearman | media |
| M10-E4 | De la muestra a la inferencia | NOVEDAD | `cor.test()` + pregunta inferencial | Pearson M9 | media |
| M10-E5 | ¿Qué dice la hipótesis nula? | NOVEDAD | H0 + significado de p | output E4 | media-alta |
| M10-E6 | Magnitud y evidencia son cosas distintas | PRÁCTICA | ninguna | r + p + IC | media |
| M10-E7 | Mira, elige y evalúa | RECUPERACIÓN | ninguna | ruta bivariada completa | media-alta |
| M10-E8 | Checkpoint D: decide y justifica | TRANSFERENCIA / CHECKPOINT | ninguna | M9–M10 | media-alta |

---
## M10-E1 — No todas las relaciones son lineales

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
M9 dejó una pregunta abierta: Pearson resume una asociación lineal, pero no todos los patrones claros tienen forma de recta. E1 crea una necesidad real para Spearman sin presentarlo como sustituto automático de Pearson.

La pantalla debe cambiar la pregunta desde:

```text
¿qué tan lineal es?
```

hacia:

```text
¿se conserva el orden de los casos
aunque la relación sea curva?
```

### 3. Capacidad antes
Puede producir un scatterplot, describir su forma y calcular/interpretar Pearson descriptivamente.

### 4. Capacidad después
Puede distinguir una asociación aproximadamente lineal de una asociación monotónica claramente curva, explicar intuitivamente qué significa conservar el orden de los casos y reconocer Spearman como coeficiente basado en rangos.

### 5. Prerrequisitos
- scatterplot;
- dirección;
- forma;
- Pearson;
- `cor()`;
- coeficiente entre -1 y +1;
- correlación ≠ causalidad.

### 6. Gran novedad
- **Concepto:** asociación monotónica y Spearman basado en orden/rangos.
- **Sintaxis expuesta:** `method = "spearman"`.
- **Decisión:** reconocer por qué un patrón monotónico curvo plantea una pregunta distinta de una relación lineal.

La sintaxis se muestra, pero no se exige producción autónoma.

### 7. Recuperaciones
Recupera explícitamente la pareja `horas_estudio`–`puntaje_metodos` de M9 como ejemplo aproximadamente lineal y la rutina “mirar la forma antes del número”.

### 8. Contexto sustantivo
Contraste entre la relación educacional ya conocida de M9 y un patrón pedagógico abstracto deliberadamente curvo.

### 9. Dataset / objetos
Patrón lineal conocido:

```text
encuesta_social$horas_estudio
encuesta_social$puntaje_metodos
```

Referencia Pearson:

```text
r = 0.7500757095661253
```

Patrón monotónico curvo:

```r
x_curva <- c(1, 2, 3, 4, 5, 6, 7, 8)

y_curva <- c(
  1, 2, 4, 8, 16, 32, 64, 128
)
```

Referencias:

```text
Pearson ≈ 0.8504406503
Spearman = 1
```

Sin missing y sin ties.

### 10. Texto para estudiante
En M9 usamos Pearson para resumir una asociación aproximadamente lineal.

Ahora observa dos patrones.

El primero se parece razonablemente a una recta.

El segundo mantiene una dirección creciente muy clara, pero se curva cada vez más.

En el segundo patrón ocurre algo importante:

```text
casos bajos en x
→ también ocupan posiciones bajas en y

casos altos en x
→ también ocupan posiciones altas en y
```

Las distancias cambian, pero el **orden** se conserva.

A una relación que mantiene una misma dirección general aunque no siga una recta la llamaremos **monótona**.

**Spearman** es un coeficiente basado en el orden o rango de los casos.

En R puede calcularse con:

```r
cor(
  x_curva,
  y_curva,
  method = "spearman"
)
```

Todavía no memorices una regla “curva = Spearman”.

Primero aprende qué propiedad representa Spearman: el orden conjunto.

### 11. Modelo mental
```text
SCATTERPLOT
↓
FORMA

APROXIMADAMENTE LINEAL
→ PEARSON

DIRECCIÓN CONSISTENTE AUNQUE CURVA
→ MONÓTONA
→ ORDEN / RANGOS
→ SPEARMAN
```

### 12. Representación / código trabajado
Representación:

```text
Persona       A   B   C   D   E

x             2   5   8   12  20
orden x       1   2   3   4   5

y             3   4   7   15  40
orden y       1   2   3   4   5
```

Código trabajado:

```r
cor(
  x_curva,
  y_curva,
  method = "spearman"
)
```

### 13. Starter code
No se requiere starter productivo. El código de Spearman se muestra completo como worked example.

### 14. Acción esperada
- comparar los dos scatterplots;
- reconocer cuál es aproximadamente lineal;
- reconocer que el patrón curvo conserva dirección y orden;
- identificar Spearman como coeficiente basado en rangos;
- interpretar el resultado trabajado `rho = 1` sin producir aún la sintaxis.

### 15. Solución canónica
```text
Patrón aproximadamente lineal
→ Pearson

Patrón creciente, curvo y monotónico
→ Spearman puede resumir el orden conjunto
```

Para el patrón curvo trabajado:

```text
rho = 1
```

### 16. Resultado esperado
Comprende que Pearson y Spearman resumen propiedades relacionadas pero no idénticas y que Spearman no se elige únicamente porque algo “no sea lineal”.

### 17. Criterio semántico de éxito
Comprobar que:

- Pearson se asocia con linealidad;
- Spearman se asocia con orden/rangos;
- comprende “monotónico” como dirección general consistente;
- reconoce que una relación monotónica puede ser curva;
- no usa normalidad como criterio;
- no usa un punto alejado como criterio automático;
- no afirma todavía que toda curva requiere Spearman.

### 18. Estrategias alternativas válidas
Se aceptan explicaciones como “mantiene el orden”, “los valores altos siguen siendo altos” o “la tendencia siempre va en la misma dirección” aunque no utilice espontáneamente la palabra `monótona`, siempre que comprenda el concepto.

### 19. Error esperado / misconception
- “no lineal = Spearman”;
- “no normal = Spearman”;
- “Spearman sirve cuando Pearson falla”;
- “Spearman siempre es mejor porque es robusto”;
- confundir rango con diferencia numérica;
- tratar `rho = 1` como 100 %;
- creer que un patrón monotónico debe ser una recta.

### 20. Feedback correcto
> Exacto. El segundo patrón no sigue una recta, pero conserva perfectamente el orden de los casos. Esa es la propiedad que Spearman resume.

### 21. Feedback resultado correcto / estrategia incorrecta
Si elige Spearman porque “no es normal”:

> El método coincide con este ejemplo, pero la razón que buscamos está en la relación conjunta: el patrón es monotónico y conserva el orden.

Si dice “toda curva usa Spearman”:

> No basta con que sea curva. Spearman necesita una tendencia de orden consistente; una curva puede cambiar de dirección.

### 22. Hint 1
> Mira primero la forma general del patrón.

### 23. Hint 2
> Pregunta si los casos altos en `x` también tienden a ocupar posiciones altas en `y`.

### 24. Hint 3
> Una relación curva puede ser monotónica si mantiene la misma dirección general; Spearman resume el orden de esos casos.

### 25. Predicción
Sí.

Primero:

> ¿Cuál patrón se parece más a una recta?

Después:

> Aunque el segundo sea curvo, ¿los casos conservan el mismo orden general?

### 26. Tipo de ejercicio
Comparación conceptual + worked example.

### 27. Andamiaje
Alto. Los gráficos, la tabla de orden y la sintaxis de Spearman se muestran completos.

### 28. Carga cognitiva
Media. Interactúan forma, orden, monotonicidad y un nombre nuevo; no aparece inferencia.

### 29. Fading
E1 muestra la sintaxis completa. E2 elimina el valor de `method` para que el estudiante la complete. E3 retira incluso el nombre del método.

### 30. Recuperación futura
Spearman se practica en E2, se elige en E3, se recupera en Checkpoint D y reaparece en M11/M13 según corresponda.

### 31. Riesgo de aprendizaje superficial
Memorizar “curva = Spearman” sin comprender que la propiedad clave es monotonicidad/orden.

### 32. Criterio de transferencia
Puede mirar una relación nueva y explicar si el orden conjunto constituye una propiedad relevante, sin usar normalidad como atajo.

### 33. Notas de implementación futura
Mostrar los scatterplots con escalas legibles. No introducir `rank()` ni fórmula manual. La interfaz debe dejar claro que el código Spearman de esta pantalla es demostrativo, no un ejercicio de memoria.

---

## M10-E2 — Una relación basada en rangos

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
E1 introdujo la idea y mostró la sintaxis. E2 exige una primera producción parcial para que `method = "spearman"` no quede como reconocimiento pasivo.

### 3. Capacidad antes
Reconoce Spearman como coeficiente basado en rangos y vio una llamada completa a `cor(..., method = "spearman")`.

### 4. Capacidad después
Puede completar una llamada de Spearman e interpretar `rho` como resumen del orden conjunto.

### 5. Prerrequisitos
`cor()`, coeficiente entre -1 y +1, patrón monotónico, orden/rangos.

### 6. Gran novedad
Ninguna grande. Se practica la sintaxis ya expuesta en E1.

### 7. Recuperaciones
Recupera `cor()` de M9 y la interpretación de signo/magnitud; reutiliza los microdatos de E1 para no añadir carga contextual.

### 8. Contexto sustantivo
Patrón monotónico curvo sin missing ni empates.

### 9. Dataset / objetos
```r
x_curva <- c(1, 2, 3, 4, 5, 6, 7, 8)

y_curva <- c(
  1, 2, 4, 8, 16, 32, 64, 128
)
```

Resultado Spearman:

```text
rho = 1
```

### 10. Texto para estudiante
Ya sabemos que este patrón conserva perfectamente el orden de los casos aunque no siga una recta.

Completa la llamada para calcular el coeficiente basado en rangos.

Antes de ejecutar, predice:

> Si el orden se conserva perfectamente y la relación es creciente, ¿esperas un coeficiente negativo, cercano a 0 o positivo cercano a +1?

Después interpreta el resultado.

### 11. Modelo mental
```text
ORDEN EN x
+
ORDEN EN y
↓
SE CONSERVA PERFECTAMENTE
↓
SPEARMAN
↓
rho = 1
```

### 12. Representación / código trabajado
El scatterplot del patrón curvo permanece visible.

Completion:

```r
cor(
  x_curva,
  y_curva,
  method = __________
)
```

### 13. Starter code
```r
cor(
  x_curva,
  y_curva,
  method = __________
)
```

### 14. Acción esperada
Completar `"spearman"`, ejecutar y explicar por qué `rho = 1` no significa una recta perfecta ni 100 %.

### 15. Solución canónica
```r
cor(
  x_curva,
  y_curva,
  method = "spearman"
)
```

### 16. Resultado esperado
```text
1
```

Interpretación:

> `rho = 1` indica que el orden de los casos se conserva perfectamente y en dirección positiva.

### 17. Criterio semántico de éxito
Comprobar:

- `cor()`;
- variables correctas;
- `method = "spearman"`;
- resultado numérico 1;
- interpreta orden positivo perfecto;
- no porcentaje;
- no “recta perfecta”;
- no causalidad;
- no hardcoding.

### 18. Estrategias alternativas válidas
Se acepta:

```r
cor(x_curva, y_curva, method = "spearman")
```

en una línea o con objetos equivalentes que dependan de los mismos datos.

No se requiere escribir `rho` manualmente.

### 19. Error esperado / misconception
- usar `method = "pearson"`;
- escribir `1` sin calcular;
- interpretar `rho = 1` como 100 %;
- interpretar `rho = 1` como pendiente;
- decir “la relación es una recta perfecta”;
- causalidad.

### 20. Feedback correcto
> Bien. Spearman devuelve `rho = 1` porque los casos conservan exactamente el mismo orden creciente.

### 21. Feedback resultado correcto / estrategia incorrecta
Si escribe `1`:

> El número coincide, pero debe derivarse de los datos mediante el coeficiente basado en rangos.

Si dice “100 %”:

> `rho` es un coeficiente entre −1 y +1, no un porcentaje.

Si dice “recta perfecta”:

> El orden es perfecto, pero el patrón es claramente curvo.

### 22. Hint 1
> Mira qué propiedad quieres resumir: el orden de los casos.

### 23. Hint 2
> El coeficiente basado en rangos que acabamos de introducir es Spearman.

### 24. Hint 3
```r
cor(
  x_curva,
  y_curva,
  method = "spearman"
)
```

### 25. Predicción
> Si el orden se conserva perfectamente en dirección creciente, esperamos un coeficiente positivo igual o muy cercano a +1. Aquí será exactamente 1.

### 26. Tipo de ejercicio
Completion problem.

### 27. Andamiaje
Medio-alto. La estructura `cor()` está dada; falta decidir/completar el método.

### 28. Carga cognitiva
Baja-media. No hay nueva idea conceptual ni inferencia.

### 29. Fading
E1 mostró todo; E2 completa el método; E3 retirará la sintaxis y exigirá elegir conceptualmente.

### 30. Recuperación futura
E3 y E8.

### 31. Riesgo de aprendizaje superficial
Asociar Spearman únicamente con escribir `method = "spearman"` sin poder justificar por qué el patrón es monotónico.

### 32. Criterio de transferencia
Puede calcular Spearman en otros vectores cuando la elección ya está justificada por la forma.

### 33. Notas de implementación futura
El grader debe inspeccionar método y dependencia de los datos. Perturbation test: intercambiar dos valores de `y_curva`; `rho` debe dejar de ser 1.

---

## M10-E3 — Elige antes de ejecutar

### 1. Rol pedagógico
INTEGRACIÓN.

### 2. Por qué existe
Evita que M10 se convierta en un árbol binario simplista. Integra forma + significado del coeficiente antes de introducir inferencia.

### 3. Capacidad antes
Conoce Pearson, Spearman y la idea de monotonicidad.

### 4. Capacidad después
Puede elegir entre Pearson, Spearman o “ninguno como resumen único adecuado” a partir de la forma observada y justificar la elección.

### 5. Prerrequisitos
Scatterplot, linealidad, monotonicidad, orden/rangos, Pearson, Spearman.

### 6. Gran novedad
Ninguna sintaxis nueva. La decisión integrada es el objetivo.

### 7. Recuperaciones
Recupera los patrones de M9 y E1–E2.

### 8. Contexto sustantivo
Tres scatterplots contrastantes: aproximadamente lineal, monotónico curvo y forma en U.

### 9. Dataset / objetos
Escenario A:

```text
encuesta_social$horas_estudio
encuesta_social$puntaje_metodos
```

Patrón aproximadamente lineal positivo.

Escenario B:

```r
x_curva <- c(1,2,3,4,5,6,7,8)

y_curva <- c(
  1,2,4,8,16,32,64,128
)
```

Patrón monotónico creciente no lineal.

Escenario C:

```r
x_u <- c(
  -4, -3, -2, -1,
   1,  2,  3,  4
)

y_u <- c(
  16, 9, 4, 1,
   1, 4, 9, 16
)
```

Referencias internas:

```text
Pearson = 0
Spearman = 0
```

### 10. Texto para estudiante
No ejecutes primero.

Mira cada gráfico y decide qué tipo de resumen corresponde.

Tienes tres opciones:

```text
Pearson
Spearman
ninguno de estos dos como resumen único suficiente
```

Para cada escenario explica **por qué**.

Recuerda:

```text
aproximadamente lineal
→ Pearson

monótona pero claramente no lineal
→ Spearman

cambia de dirección
→ ninguno de los dos resume bien por sí solo
```

### 11. Modelo mental
```text
MIRA EL SCATTERPLOT
↓
¿APROXIMADAMENTE LINEAL?
→ PEARSON

¿MONÓTONA PERO CLARAMENTE NO LINEAL?
→ SPEARMAN

¿NO LINEAL Y NO MONÓTONA?
→ NINGUNO COMO RESUMEN ÚNICO
```

### 12. Representación / código trabajado
Se muestran los tres scatterplots. No se muestra código de correlación antes de decidir.

### 13. Starter code
No se requiere starter productivo. La respuesta inicial es una elección justificada.

### 14. Acción esperada
Clasificar A/B/C y producir una justificación basada en la forma, no en normalidad, nombres de variables ni presencia de valores extremos.

### 15. Solución canónica
```text
A → Pearson
porque es aproximadamente lineal.

B → Spearman
porque es monotónica y claramente no lineal.

C → Ninguno como resumen único suficiente
porque cambia de dirección y no es monotónica.
```

### 16. Resultado esperado
Elección correcta y razonada en los tres escenarios.

### 17. Criterio semántico de éxito
Comprobar:

- A → Pearson + justificación lineal;
- B → Spearman + justificación monotónica/orden;
- C → ninguno + justificación no monotónica;
- no usa normalidad como criterio;
- no usa outlier como regla;
- comprende que “ninguno” no significa ausencia de patrón.

### 18. Estrategias alternativas válidas
Se aceptan formulaciones equivalentes de la justificación. En C también es válido decir “miraría el gráfico y buscaría otro tipo de resumen/modelo” sin nombrar técnicas futuras.

### 19. Error esperado / misconception
- toda no linealidad → Spearman;
- toda curva → Spearman;
- “ninguno” = “no hay relación”;
- Pearson porque la variable es numérica;
- Spearman porque “los datos no parecen normales”;
- Spearman porque existe un punto lejano.

### 20. Feedback correcto
> Bien. Elegiste el resumen a partir de la forma de la relación, no mediante una regla superficial.

### 21. Feedback resultado correcto / estrategia incorrecta
Si B = Spearman por “no normal”:

> La elección coincide, pero la razón adecuada es que la relación es monotónica y claramente no lineal.

Si C = Spearman por “es curva”:

> Observa que la U cambia de dirección. No mantiene un orden monotónico de principio a fin.

### 22. Hint 1
> Mira primero la forma de cada nube.

### 23. Hint 2
> Pregunta si la relación mantiene una misma dirección general.

### 24. Hint 3
```text
lineal → Pearson
monótona curva → Spearman
cambia de dirección → ninguno como resumen único
```

### 25. Predicción
La elección antes de ejecutar constituye la predicción.

### 26. Tipo de ejercicio
Clasificación/decisión integrada.

### 27. Andamiaje
Medio. Las tres opciones están visibles, pero el método no está asociado previamente a cada gráfico.

### 28. Carga cognitiva
Media. Coordina forma, linealidad y monotonicidad sin nueva sintaxis.

### 29. Fading
E3 retira la sintaxis y exige razonamiento conceptual. E4 volverá a un worked example porque cambia la pregunta hacia inferencia.

### 30. Recuperación futura
E7 y E8 exigen elegir método sin que la consigna lo nombre.

### 31. Riesgo de aprendizaje superficial
Convertir el esquema en una regla visual automática sin explicar qué propiedad resume cada coeficiente.

### 32. Criterio de transferencia
Puede justificar una elección en un gráfico nuevo y reconocer cuando ninguna de las dos opciones basta.

### 33. Notas de implementación futura
Los tres scatterplots deben mostrarse con suficiente claridad. El grader debe evaluar elección + justificación; no aceptar solo la etiqueta.

---

## M10-E4 — De la muestra a la inferencia

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Hasta E3 la pregunta es descriptiva: qué patrón observamos en estos casos y qué coeficiente lo resume. E4 introduce una pregunta distinta: si los casos constituyen una muestra, qué aporta un procedimiento inferencial respecto de una asociación poblacional.

### 3. Capacidad antes
Puede elegir y calcular un coeficiente descriptivo según la forma.

### 4. Capacidad después
Puede ejecutar un `cor.test()` de Pearson sobre datos conocidos y localizar estimate, p-value e intervalo de confianza sin tener que interpretar todavía toda la teoría inferencial.

### 5. Prerrequisitos
Pearson, `cor()`, scatterplot, muestra como conjunto observado en sentido cotidiano.

### 6. Gran novedad
- **Sintaxis:** `cor.test()`.
- **Cambio conceptual:** descripción muestral → pregunta inferencial.
- **No son novedades de esta pantalla:** interpretación profunda de H0, p e IC; se distribuyen en E5/E6.

### 7. Recuperaciones
Reutiliza exactamente la pareja principal locked de M9 para que `cor.test()` sea la única gran novedad.

### 8. Contexto sustantivo
Horas de estudio y puntaje de métodos en los 12 pares completos de `encuesta_social`.

### 9. Dataset / objetos
```text
horas_estudio:
2,4,3,6,5,8,7,10,9,11,4,6

puntaje_metodos:
59,68,58,64,62,75,65,64,74,84,59,73
```

Pearson descriptivo locked:

```text
r = 0.7500757095661253
```

Sin missing en esta pareja.

### 10. Texto para estudiante
En M9 describimos lo que ocurre en estos 12 casos:

```text
r ≈ 0.75
```

Ahora cambia la pregunta.

Si estos casos forman una muestra, queremos obtener información sobre una posible asociación en la población.

En R podemos utilizar:

```r
cor.test(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos,
  method = "pearson"
)
```

El output contiene varias líneas.

Por ahora localiza solo tres partes:

```text
estimate
p-value
95 percent confidence interval
```

`t`, `df` y otras líneas forman parte del procedimiento, pero todavía no necesitamos interpretarlas.

### 11. Modelo mental
```text
MUESTRA
↓
CORRELACIÓN OBSERVADA
↓
PREGUNTA SOBRE ASOCIACIÓN POBLACIONAL
↓
cor.test()
↓
ESTIMATE + p + IC
```

### 12. Representación / código trabajado
```r
cor.test(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos,
  method = "pearson"
)
```

Output contractual:

```text
estimate = 0.7500757096
t = 3.5865133284
df = 10
p-value = 0.0049577379

95 % IC:
[0.3093322357,
 0.9255542856]
```

### 13. Starter code
```r
cor.test(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos,
  method = "pearson"
)
```

### 14. Acción esperada
Predecir que el estimate será parecido al `r` ya conocido, ejecutar y localizar estimate, p-value e IC.

### 15. Solución canónica
```r
cor.test(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos,
  method = "pearson"
)
```

### 16. Resultado esperado
Aceptar el redondeo de R. Valores de referencia:

```text
estimate ≈ 0.7500757
p ≈ 0.004957738
IC 95 % ≈ [0.3093322, 0.9255543]
```

### 17. Criterio semántico de éxito
Comprobar:

- variables correctas;
- `cor.test()`;
- `method = "pearson"`;
- estimate aproximadamente 0.7500757;
- localiza p aproximadamente 0.00495774;
- localiza IC aproximadamente [0.3093, 0.9256];
- entiende que `t` y `df` no son el foco;
- no hardcoding.

### 18. Estrategias alternativas válidas
Ejecutar `cor()` antes de `cor.test()` es válido pero redundante. No exigirlo.

### 19. Error esperado / misconception
- buscar p como si fuera el coeficiente;
- creer que el IC contiene los puntajes de la muestra;
- intentar interpretar `t`/`df` antes de tiempo;
- concluir causalidad;
- creer que `cor.test()` “prueba que existe relación” sin comprender la nueva pregunta.

### 20. Feedback correcto
> Bien. Encontraste el mismo coeficiente observado y localizaste las dos piezas nuevas que analizaremos a continuación: p-value e intervalo de confianza.

### 21. Feedback resultado correcto / estrategia incorrecta
Si hardcodea los valores:

> El output coincide, pero la habilidad es obtenerlo desde las dos variables mediante `cor.test()`.

Si interpreta p inmediatamente como probabilidad de H0:

> Todavía no lo interpretes así. En el próximo ejercicio construiremos qué pregunta responde el p-value.

### 22. Hint 1
> Ya conoces el coeficiente descriptivo. Ahora necesitamos una herramienta inferencial.

### 23. Hint 2
> La función es `cor.test()` y utiliza las mismas dos variables.

### 24. Hint 3
```r
cor.test(
  encuesta_social$horas_estudio,
  encuesta_social$puntaje_metodos,
  method = "pearson"
)
```

### 25. Predicción
> ¿Esperas que el estimate de `cor.test()` sea parecido al `r ≈ 0.75` que ya obtuvimos? Sí.

### 26. Tipo de ejercicio
Worked example + lectura guiada de output.

### 27. Andamiaje
Muy alto. Función, variables y método están dados.

### 28. Carga cognitiva
Media. La novedad es `cor.test()` + cambio de pregunta; la interpretación teórica se distribuye después.

### 29. Fading
E4 entrega la llamada completa; E7/E8 pedirán elegir y ejecutar sin nombrarla.

### 30. Recuperación futura
E5/E6 interpretan el output; E7/E8 lo producen.

### 31. Riesgo de aprendizaje superficial
Aprender `cor.test()` como “correlación con p” en lugar de reconocer el salto de descripción a inferencia.

### 32. Criterio de transferencia
Puede reconocer en otro output dónde están estimate, p e IC cuando corresponda.

### 33. Notas de implementación futura
Resaltar visualmente estimate, p e IC. No pedir interpretar `t` ni `df`. Grader con tolerancia numérica, no comparación textual.

---

## M10-E5 — ¿Qué dice la hipótesis nula?

### 1. Rol pedagógico
NOVEDAD.

### 2. Por qué existe
Un p-value sin escenario nulo genera reglas mecánicas. E5 construye H0 y p como una sola unidad conceptual antes de discutir precisión.

### 3. Capacidad antes
Puede ejecutar/leer un `cor.test()` y localizar p.

### 4. Capacidad después
Puede formular el escenario nulo para Pearson e interpretar p como compatibilidad de los datos con ese escenario, evitando las misconceptions centrales.

### 5. Prerrequisitos
Output E4, correlación observada vs poblacional en lenguaje básico.

### 6. Gran novedad
H0 + significado del p-value como una única unidad conceptual. No hay sintaxis nueva.

### 7. Recuperaciones
Usa el mismo output de E4 para que la carga sea puramente conceptual.

### 8. Contexto sustantivo
La correlación `horas_estudio`–`puntaje_metodos` ya conocida.

### 9. Dataset / objetos
Output de referencia:

```text
r ≈ 0.7501
p ≈ 0.00496
```

### 10. Texto para estudiante
Para interpretar un p-value necesitamos saber cuál es el escenario de referencia del test.

En este Pearson:

> **H0:** la correlación lineal poblacional es 0.

Esto **no** significa:

> “no existe ninguna relación de ningún tipo”.

Ahora mira:

```text
p ≈ 0.00496
```

Usaremos esta interpretación:

> El p-value indica qué tan incompatibles son los datos observados con el escenario nulo utilizado por el test.

Un p pequeño significa menor compatibilidad de los datos con ese escenario.

No significa:

```text
probabilidad de que H0 sea verdadera
```

ni:

```text
tamaño de la asociación
```

ni:

```text
probabilidad de causalidad
```

### 11. Modelo mental
```text
H0
↓
ESCENARIO NULO

SUPONEMOS ESE ESCENARIO
↓
OBSERVAMOS LOS DATOS
↓
p-VALUE
↓
¿QUÉ TAN COMPATIBLES RESULTAN?
```

### 12. Representación / código trabajado
No hay código nuevo. Se trabaja sobre el output ya obtenido en E4.

### 13. Starter code
No se requiere starter code.

### 14. Acción esperada
Evaluar afirmaciones verdaderas/falsas y explicar por qué.

### 15. Solución canónica
Afirmación A:

> `p = .00496` significa que H0 tiene 0.496 % de probabilidad.

**FALSO.**

Afirmación B:

> El p-value es pequeño respecto de .05, pero eso no indica por sí solo que la asociación sea grande.

**VERDADERO.**

Afirmación C:

> El p-value ayuda a evaluar la compatibilidad de los datos con el escenario nulo.

**VERDADERO.**

Afirmación D:

> Como p < .05, estudiar más causa un mayor puntaje.

**FALSO.**

### 16. Resultado esperado
Comprende H0/p sin convertirlos en certeza, tamaño o causalidad.

### 17. Criterio semántico de éxito
Comprobar:

- H0 = correlación lineal poblacional 0;
- no dice “no existe ninguna relación”;
- p ≠ probabilidad de H0;
- p ≠ tamaño;
- p ≠ causalidad;
- `.05` = convención;
- significancia ≠ importancia.

### 18. Estrategias alternativas válidas
Se aceptan definiciones equivalentes de p que preserven la condicionalidad respecto de H0 y no atribuyan probabilidades posteriores a H0.

### 19. Error esperado / misconception
- p = probabilidad de H0;
- p = probabilidad de “azar”;
- p < .05 = verdad;
- p > .05 = no hay asociación;
- p pequeño = correlación grande;
- p pequeño = causalidad.

### 20. Feedback correcto
> Exacto. El p-value se interpreta respecto del escenario nulo; no es la probabilidad de que H0 sea verdadera ni una medida del tamaño de la asociación.

### 21. Feedback resultado correcto / estrategia incorrecta
Si marca correctamente A como falsa pero dice “porque p es la probabilidad de azar”:

> La respuesta es falsa por una razón más precisa: p se calcula bajo H0 y no representa ni probabilidad de H0 ni probabilidad de que “todo sea azar”.

Si concluye solo “es significativo”:

> Esa etiqueta puede describir la relación con un umbral convencional, pero todavía necesitamos informar magnitud e incertidumbre.

### 22. Hint 1
> Pregunta primero: ¿qué escenario está suponiendo el test?

### 23. Hint 2
> El p-value se interpreta bajo ese escenario; no asigna probabilidad a H0.

### 24. Hint 3
> H0 aquí es correlación lineal poblacional 0; p describe compatibilidad de los datos con ese escenario.

### 25. Predicción
No hay predicción de código.

### 26. Tipo de ejercicio
Interpretación conceptual / diagnóstico de misconceptions.

### 27. Andamiaje
Alto. Las afirmaciones son concretas y el output ya es conocido.

### 28. Carga cognitiva
Media-alta. Coordina H0, p y varias interpretaciones incorrectas; el IC se excluye deliberadamente.

### 29. Fading
E5 no exige sintaxis; E6 pide integrar p con magnitud e IC; E7/E8 lo interpretan en una ruta completa.

### 30. Recuperación futura
E6, E7, E8, M11, M12 y M13.

### 31. Riesgo de aprendizaje superficial
Aprender únicamente `p < .05 = significativo` y saltarse el escenario nulo.

### 32. Criterio de transferencia
Puede interpretar un nuevo p-value sin convertirlo en tamaño, probabilidad de H0 o causalidad.

### 33. Notas de implementación futura
`.05` puede aparecer como umbral convencional.

Texto permitido:

> Bajo un umbral convencional de .05, este resultado suele describirse como estadísticamente significativo.

Añadir inmediatamente:

> Esa etiqueta no indica por sí sola cuánto mide la asociación ni si es sustantivamente importante.

---

## M10-E6 — Magnitud y evidencia son cosas distintas

### 1. Rol pedagógico
PRÁCTICA.

### 2. Por qué existe
E5 protege la interpretación de p, pero todavía falta separar p de magnitud e introducir el IC como incertidumbre. E6 utiliza dos outputs con el mismo `r` y distinto N para aislar esa diferencia.

### 3. Capacidad antes
Comprende H0 y p en nivel introductorio.

### 4. Capacidad después
Puede distinguir magnitud observada, evidencia relativa a H0, cantidad de información e incertidumbre/precisión.

### 5. Prerrequisitos
Pearson `r`, p-value, lectura básica de `cor.test()`.

### 6. Gran novedad
Ninguna gran sintaxis nueva. El IC se profundiza conceptualmente dentro de una práctica interpretativa.

### 7. Recuperaciones
Recupera `r`, p y la presencia del IC observada en E4.

### 8. Contexto sustantivo
Dos estudios hipotéticos con la misma correlación observada pero tamaños muestrales diferentes.

### 9. Dataset / objetos
No se requiere dataset ejecutable.

Estudio A:

```text
N = 12
r = 0.50
p = 0.0978546143

95 % IC:
[-0.10364168,
  0.83445429]
```

Estudio B:

```text
N = 50
r = 0.50
p = 0.0002180125

95 % IC:
[0.25748786,
 0.68325630]
```

### 10. Texto para estudiante
Los dos estudios observan exactamente la misma correlación:

```text
r = 0.50
```

Pero tienen distinta cantidad de información.

Compara:

```text
Estudio A
N = 12
p ≈ 0.0979
IC ≈ [-0.104, 0.834]

Estudio B
N = 50
p ≈ 0.000218
IC ≈ [0.257, 0.683]
```

Responde:

1. ¿Cuál tiene una asociación observada mayor?
2. ¿Cuál tiene menor p-value?
3. ¿Cuál tiene un intervalo más estrecho?
4. ¿Un p-value menor significa una correlación mayor?

### 11. Modelo mental
```text
COEFICIENTE
→ MAGNITUD Y DIRECCIÓN

p-VALUE
→ COMPATIBILIDAD CON H0

IC
→ INCERTIDUMBRE / PRECISIÓN

N
→ CANTIDAD DE INFORMACIÓN
```

### 12. Representación / código trabajado
Dos tarjetas de output lado a lado. No hay código nuevo.

### 13. Starter code
No se requiere starter code.

### 14. Acción esperada
Comparar los outputs y explicar por qué mismo `r` puede acompañarse de p e IC distintos.

### 15. Solución canónica
1. Asociación observada mayor: **ninguno**; ambos tienen `r = 0.50`.
2. Menor p: **Estudio B**.
3. Intervalo más estrecho: **Estudio B**.
4. Un p menor significa correlación mayor: **no**.

### 16. Resultado esperado
Distingue magnitud, evidencia, precisión y cantidad de información.

### 17. Criterio semántico de éxito
Comprobar:

- reconoce misma magnitud;
- reconoce diferente N;
- reconoce diferente p;
- reconoce diferente ancho de IC;
- p menor ≠ r mayor;
- intervalo más estrecho = mayor precisión;
- IC no es rango de observaciones;
- IC 95 % no se interpreta como probabilidad posterior del parámetro.

### 18. Estrategias alternativas válidas
Se aceptan formulaciones equivalentes de “mayor precisión” como “intervalo más estrecho” o “menor incertidumbre”, siempre que no se confunda con efecto mayor.

### 19. Error esperado / misconception
- B tiene efecto mayor porque p es menor;
- B tiene efecto mayor porque el IC es más estrecho;
- IC = rango donde cayó 95 % de la muestra;
- 95 % = probabilidad posterior del parámetro;
- A demuestra que r = 0 porque p > .05;
- introducir potencia formal innecesariamente.

### 20. Feedback correcto
> Exacto. La magnitud observada es la misma. Lo que cambia con la cantidad de información es la evidencia relativa a H0 y la precisión.

### 21. Feedback resultado correcto / estrategia incorrecta
Si responde B a “mayor asociación”:

> Mira primero `r`: ambos estudios tienen exactamente 0.50.

Si interpreta IC como tamaño:

> El ancho del intervalo habla de precisión/incertidumbre, no de que la asociación sea mayor.

### 22. Hint 1
> Compara primero los dos valores de `r`.

### 23. Hint 2
> Después separa N, p y ancho del intervalo.

### 24. Hint 3
> `r` responde cuánto; p e IC responden preguntas diferentes sobre evidencia e incertidumbre.

### 25. Predicción
No se requiere una fase separada.

### 26. Tipo de ejercicio
Interpretación comparativa.

### 27. Andamiaje
Medio. Los outputs están dados y organizados simétricamente.

### 28. Carga cognitiva
Media. Interactúan r, N, p e IC, pero no hay sintaxis nueva.

### 29. Fading
Integra conceptos ya presentados; E7 los usará en una ruta productiva.

### 30. Recuperación futura
E7, M11, M12 y M13.

### 31. Riesgo de aprendizaje superficial
Convertir p o ancho del IC en otra medida de tamaño del efecto.

### 32. Criterio de transferencia
Puede leer un nuevo output y separar “cuánto”, “qué evidencia” y “qué incertidumbre”.

### 33. Notas de implementación futura
Definición visible del IC:

> El intervalo muestra un rango de valores de correlación poblacional compatibles con los datos y con el procedimiento utilizado.

> Un intervalo más estrecho indica mayor precisión.

Nota de protección:

> El 95 % no se interpreta como una probabilidad posterior asignada al parámetro dentro de este intervalo concreto.

Puede observarse que A incluye 0 y B no, pero no convertir esa observación en criterio nuclear.

---

## M10-E7 — Mira, elige y evalúa

### 1. Rol pedagógico
RECUPERACIÓN.

### 2. Por qué existe
Antes del checkpoint, M10 necesita recuperar la ruta completa con menos apoyo y sin missing. E7 utiliza nuevas columnas de la base conocida para integrar scatterplot, elección Pearson e inferencia.

### 3. Capacidad antes
Puede distinguir Pearson/Spearman/ninguno y comprender un output inferencial.

### 4. Capacidad después
Puede ejecutar una ruta Pearson completa desde el scatterplot hasta una interpretación conjunta de magnitud, evidencia e incertidumbre.

### 5. Prerrequisitos
`plot()`, forma, Pearson, `cor.test()`, H0, p, IC, causalidad.

### 6. Gran novedad
Ninguna.

### 7. Recuperaciones
Recupera M9 + M10-E3–E6. No recupera missing para mantener una carga manejable.

### 8. Contexto sustantivo
Edad y horas de ocio diario en `encuesta_social`.

### 9. Dataset / objetos
Columnas nuevas locked:

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

Sin missing.

Referencias:

```text
Pearson r = -0.6929468984
t = -3.0392858131
df = 10
p = 0.0124777785

95 % IC:
[-0.9063916512,
 -0.1976456744]

Spearman ≈ -0.6825407441
```

El método esperado es Pearson.

### 10. Texto para estudiante
Queremos estudiar cómo se relacionan la edad y las horas de ocio diario.

1. representa la relación;
2. describe su forma y dirección;
3. decide qué coeficiente corresponde mejor al patrón;
4. evalúa inferencialmente la asociación;
5. interpreta magnitud, evidencia e incertidumbre;
6. explica qué no podemos concluir.

Las funciones no están indicadas.

Empieza por el gráfico.

### 11. Modelo mental
```text
PREGUNTA
↓
SCATTERPLOT
↓
FORMA APROXIMADAMENTE LINEAL NEGATIVA
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
No se entrega solución trabajada antes de intentar. La base está disponible.

### 13. Starter code
```r
# representa la relación


# elige y ejecuta el análisis inferencial
```

### 14. Acción esperada
Producir scatterplot, justificar Pearson, ejecutar `cor.test()` e interpretar los tres componentes centrales.

### 15. Solución canónica
```r
plot(
  encuesta_social$edad,
  encuesta_social$horas_ocio
)

cor.test(
  encuesta_social$edad,
  encuesta_social$horas_ocio,
  method = "pearson"
)
```

### 16. Resultado esperado
```text
r ≈ -0.6929469
p ≈ 0.01247778

95 % IC:
[-0.9063917,
 -0.1976457]
```

Interpretación:

> La muestra presenta una asociación aproximadamente lineal negativa: las edades mayores tienden a aparecer junto con menos horas de ocio. La correlación observada es aproximadamente −0.69. Los datos son poco compatibles con el escenario de correlación lineal poblacional igual a cero. El intervalo expresa incertidumbre sobre la magnitud poblacional compatible con estos datos. El análisis no demuestra causalidad.

### 17. Criterio semántico de éxito
Comprobar:

- `plot()`;
- variables correctas;
- forma aproximadamente lineal;
- dirección negativa;
- Pearson justificado;
- `cor.test()`;
- `method = "pearson"`;
- estimate correcto;
- p correcto;
- IC correcto;
- interpretación separa magnitud/evidencia/incertidumbre;
- no hardcoding;
- no causalidad.

### 18. Estrategias alternativas válidas
Es válido ejecutar antes:

```r
cor(
  encuesta_social$edad,
  encuesta_social$horas_ocio,
  method = "pearson"
)
```

pero no es obligatorio.

Se aceptan objetos intermedios que dependan de las columnas correctas.

### 19. Error esperado / misconception
- elegir Spearman porque “edad no es normal”;
- omitir el scatterplot;
- ejecutar solo `cor()`;
- reportar solo “p < .05”;
- p = magnitud;
- IC = rango de observaciones;
- causalidad;
- hardcoding.

### 20. Feedback correcto
> Bien. Miraste primero el patrón, justificaste Pearson y separaste magnitud, evidencia e incertidumbre.

### 21. Feedback resultado correcto / estrategia incorrecta
Si obtiene los números con Pearson pero no mira el gráfico:

> El resultado numérico coincide, pero la elección del método debe justificarse desde la forma observada.

Si dice solo “es significativo”:

> Esa etiqueta es insuficiente. Incluye magnitud, p e incertidumbre.

### 22. Hint 1
> Empieza mirando la forma de la relación.

### 23. Hint 2
> El patrón es aproximadamente lineal y negativo.

### 24. Hint 3
```r
cor.test(
  encuesta_social$edad,
  encuesta_social$horas_ocio,
  method = "pearson"
)
```

### 25. Predicción
No se añade una fase separada; la descripción del scatterplot antes de ejecutar cumple esa función.

### 26. Tipo de ejercicio
Recuperación integrada.

### 27. Andamiaje
Medio-bajo. Solo hay comentarios estructurales y pistas escalonadas.

### 28. Carga cognitiva
Media-alta. Integra la ruta completa, pero se excluyen missing y sintaxis nueva.

### 29. Fading
Retira nombres de funciones y método. E8 cambia además la base y el método correcto.

### 30. Recuperación futura
M11 y M13.

### 31. Riesgo de aprendizaje superficial
Saltar directamente a `cor.test()` por reconocer el nombre de las variables o reportar únicamente p.

### 32. Criterio de transferencia
Puede repetir la ruta sobre otra pareja aproximadamente lineal con poco apoyo.

### 33. Notas de implementación futura
El gráfico debe hacer visible un patrón razonablemente lineal negativo con dispersión. Grader con tolerancia numérica. No penalizar un `cor()` previo.

---

## M10-E8 — Checkpoint D: decide y justifica

### 1. Rol pedagógico
TRANSFERENCIA / CHECKPOINT.

### 2. Por qué existe
Diagnostica si el estudiante puede transferir la ruta completa a una base nueva, elegir Spearman por la forma y manejar correctamente un output cuya ruta no incluye IC estándar.

### 3. Capacidad antes
Ha completado M9–M10 y dispone de todos los conceptos necesarios.

### 4. Capacidad después
Demuestra transferencia autónoma: representar, describir, elegir, ejecutar e interpretar una relación monotónica no lineal en una base nueva.

### 5. Prerrequisitos
Todos los objetivos nucleares de M9–M10. No hay contenido nuevo.

### 6. Gran novedad
Ninguna. El checkpoint no introduce sintaxis ni conceptos nuevos.

### 7. Recuperaciones
Recupera `plot()`, Spearman, `cor.test()`, H0/p, interpretación de magnitud y causalidad.

### 8. Contexto sustantivo
Antigüedad de emprendimientos y ventas mensuales.

### 9. Dataset / objetos
```text
encuesta_emprendimiento

id   antiguedad_anos   ventas_mensuales
1    1                 100
2    2                 110
3    3                 120
4    4                 140
5    5                 180
6    6                 300
7    7                 800
8    8                 3000
```

Sin missing.

Sin ties.

Referencias:

```text
Pearson ≈ 0.7095690774
Spearman = 1

Spearman test:
S = 0
rho = 1
p ≈ 0.0000496031746
```

### 10. Texto para estudiante
En esta nueva encuesta queremos estudiar cómo se relacionan la antigüedad del emprendimiento y sus ventas mensuales.

1. representa la relación;
2. describe su forma;
3. elige y justifica el coeficiente que mejor resume ese patrón;
4. evalúa inferencialmente la asociación;
5. interpreta el coeficiente y el p-value;
6. explica qué no permite concluir el análisis.

No se indican funciones ni método.

Puedes abrir pistas si las necesitas. Pedir una pista no invalida el checkpoint.

### 11. Modelo mental
```text
BASE NUEVA
↓
SCATTERPLOT
↓
CRECIENTE + MONÓTONA + CLARAMENTE NO LINEAL
↓
SPEARMAN
↓
cor.test()
↓
rho + p
↓
INTERPRETAR
↓
NO CAUSALIDAD
```

### 12. Representación / código trabajado
No hay código trabajado previo. La base está disponible y el estudiante decide la ruta.

### 13. Starter code
```r
# representa la relación


# elige y evalúa la asociación
```

### 14. Acción esperada
Producir scatterplot, describir monotonicidad/no linealidad, elegir Spearman, ejecutar `cor.test()` y explicar `rho`, p y límites.

### 15. Solución canónica
```r
plot(
  encuesta_emprendimiento$antiguedad_anos,
  encuesta_emprendimiento$ventas_mensuales
)

cor.test(
  encuesta_emprendimiento$antiguedad_anos,
  encuesta_emprendimiento$ventas_mensuales,
  method = "spearman"
)
```

### 16. Resultado esperado
Scatterplot:

```text
creciente
monotónico
claramente no lineal
```

Output de referencia:

```text
S = 0
rho = 1
p ≈ 0.0000496031746
```

No exigir IC.

Interpretación esperada:

> El patrón es creciente y claramente no lineal, pero mantiene perfectamente el orden de los casos. Por eso Spearman es un resumen adecuado de la asociación monotónica. `rho = 1` indica concordancia perfecta de rangos. El p-value es muy pequeño respecto del escenario nulo de asociación de rangos igual a cero. Esto no demuestra que una mayor antigüedad cause mayores ventas.

### 17. Criterio semántico de éxito
Evaluar por componentes.

**Scatterplot**
- base correcta;
- variables correctas.

**Forma**
- positiva/creciente;
- monotónica;
- no lineal.

**Método**
- Spearman;
- justificación por orden/forma.

**Inferencia**
- `cor.test()`;
- `method = "spearman"`;
- rho = 1;
- p aproximadamente 0.00004960317.

**IC**
- no exigir.

**Interpretación**
- rho no es porcentaje;
- p no es probabilidad de H0;
- no causalidad.

**Estrategia**
- depende de los datos;
- no hardcoding.

### 18. Estrategias alternativas válidas
Es válido calcular adicionalmente:

```r
cor(
  encuesta_emprendimiento$antiguedad_anos,
  encuesta_emprendimiento$ventas_mensuales,
  method = "spearman"
)
```

antes de `cor.test()`.

No es obligatorio.

No penalizar redondeos razonables.

### 19. Error esperado / misconception
- Pearson solo porque ambas variables son numéricas;
- Spearman solo porque “no es lineal”, sin mencionar monotonicidad/orden;
- rho = 100 %;
- exigir un IC de Spearman en la salida base;
- p = probabilidad de H0;
- p pequeño = efecto importante;
- causalidad;
- hardcodear rho/p.

### 20. Feedback correcto
> Bien. Elegiste Spearman por la forma monotónica no lineal, interpretaste rho y p, y no exigiste un componente que R base no devuelve en esta ruta.

### 21. Feedback resultado correcto / estrategia incorrecta
Si elige Spearman pero dice solo “porque es curva”:

> La elección coincide, pero la propiedad decisiva es que la curva mantiene una dirección monotónica y conserva el orden.

Si busca un IC:

> En la salida estándar de `cor.test(..., method = "spearman")` de R base no aparece el mismo intervalo de confianza que en Pearson.

Si hardcodea:

> Los números coinciden, pero deben derivarse de la base mediante el análisis.

### 22. Hint 1
> Mira primero la forma y pregunta si mantiene una dirección consistente.

### 23. Hint 2
> Piensa en el coeficiente que trabaja con el orden de los casos.

### 24. Hint 3
```r
cor.test(
  encuesta_emprendimiento$antiguedad_anos,
  encuesta_emprendimiento$ventas_mensuales,
  method = "spearman"
)
```

### 25. Predicción
No se añade un ritual separado; la elección razonada antes de ejecutar es la predicción.

### 26. Tipo de ejercicio
Checkpoint / transferencia.

### 27. Andamiaje
Bajo, con hints escalonadas disponibles y sin penalización.

### 28. Carga cognitiva
Media-alta. Integra decisiones ya aprendidas sin missing ni nueva sintaxis.

### 29. Fading
Máximo fading de M10: base nueva, funciones no nombradas y método no indicado.

### 30. Recuperación futura
M11 recuperará la lógica de correlaciones en múltiples pares; M13 exigirá decidir una ruta completa.

### 31. Riesgo de aprendizaje superficial
Reconocer el ejemplo por su crecimiento exponencial y contestar Spearman de memoria sin justificar monotonicidad.

### 32. Criterio de transferencia
Existe transferencia cuando puede resolver otra relación monotónica no lineal con nombres y valores diferentes, manteniendo la justificación conceptual.

### 33. Notas de implementación futura
Checkpoint formativo:

- hints cerradas al inicio;
- pedir ayuda no invalida la tarea;
- grader ramificado por método;
- ruta Pearson: estimate + p + IC;
- ruta Spearman: rho + p, sin exigir IC;
- perturbation tests:
  - volver el patrón aproximadamente lineal;
  - intercambiar dos ventas;
  - invertir el orden;
  - modificar un valor;
- no comparar código literal.

---


# Cierre conceptual de M10 y puente a M11

Cerrar exactamente con:

> Ya podemos estudiar una relación,
> elegir un coeficiente
> y evaluar la evidencia asociada.
>
> Pero una investigación suele incluir más de dos variables.
>
> Si queremos revisar varias relaciones al mismo tiempo,
> repetir el mismo análisis una por una puede volverse difícil de leer.
>
> **¿Cómo organizamos varias correlaciones a la vez?**

Detenerse ahí.

M10 no introduce todavía:

- matrices de correlaciones;
- diagonal;
- simetría;
- `pairwise.complete.obs`;
- correlación punto-biserial;
- programación matricial.

# Retención esperada después de una semana

## Comprensión
Debe recordar:

```text
Pearson
→ asociación lineal
```

```text
Spearman
→ asociación monotónica basada en orden/rangos
```

Debe recordar:

```text
no lineal
≠
Spearman automáticamente
```

```text
no normal
≠
Spearman automáticamente
```

```text
punto muy alejado
≠
Spearman automáticamente
```

Debe comprender la tercera ruta:

```text
no lineal + no monotónica
→ ninguno de los dos resume bien por sí solo
```

Debe comprender:

```text
coeficiente
→ magnitud/dirección

p
→ compatibilidad con H0

IC
→ incertidumbre/precisión
```

Debe recordar:

```text
p ≠ probabilidad de H0
p pequeño ≠ efecto grande
correlación + p pequeño ≠ causalidad
```

## Producción
Con poca ayuda debe poder producir:

```r
cor(
  x,
  y,
  method = "spearman"
)
```

y:

```r
cor.test(
  x,
  y,
  method = "pearson"
)
```

o:

```r
cor.test(
  x,
  y,
  method = "spearman"
)
```

según la forma observada.

# Auditoría del módulo

## Conteo por rol
- NOVEDAD: 3
- PRÁCTICA: 2
- INTEGRACIÓN: 1
- RECUPERACIÓN: 1
- TRANSFERENCIA / CHECKPOINT: 1

## Porcentaje local de novedad
3 de 8 = 37.5 %.

No se alteran las etiquetas.

## Trayectoria de habilidades

```text
Spearman conceptual
M10-E1
→ práctica sintáctica M10-E2
→ elección M10-E3
→ transferencia M10-E8
```

```text
cor.test()
M10-E4
→ interpretación M10-E5/E6
→ recuperación productiva M10-E7
→ transferencia M10-E8
→ recuperación M11/M13
```

```text
H0 / p
M10-E5
→ contraste M10-E6
→ producción M10-E7/E8
→ recuperación M11/M12/M13
```

```text
IC
M10-E4 observa
→ M10-E6 comprende
→ M10-E7 interpreta
→ no se exige en ruta Spearman E8
```

## Checkpoint D
M10-E8.

No introduce contenido nuevo.

Evalúa:

- scatterplot;
- forma;
- monotonicidad;
- elección;
- Spearman;
- `cor.test()`;
- H0/p;
- interpretación no causal;
- adaptación al output específico del método.

# Contrato de datos

## `encuesta_social`
M10 hereda de M9:

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

M10 añade y fija:

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

M11–M12 pueden añadir variables, pero no modificar las ya locked.

## `encuesta_emprendimiento`
Checkpoint D:

```text
id   antiguedad_anos   ventas_mensuales
1    1                 100
2    2                 110
3    3                 120
4    4                 140
5    5                 180
6    6                 300
7    7                 800
8    8                 3000
```

# Control técnico verificado

Valores utilizados en el diseño:

```text
E1/E2:
Pearson ≈ 0.8504406503218714
Spearman = 1
```

```text
E4:
r = 0.7500757095661256
t = 3.5865133284432784
df = 10
p = 0.0049577378558551865
IC 95 % ≈
[0.3093322357,
 0.9255542856]
```

La diferencia en los últimos decimales respecto de la especificación previa es únicamente de precisión de punto flotante; para grading se utiliza tolerancia.

```text
E6 A:
N = 12
r = 0.50
p = 0.0978546142578125
IC 95 % ≈
[-0.10364168,
 0.83445429]
```

```text
E6 B:
N = 50
r = 0.50
p = 0.000218012471361578
IC 95 % ≈
[0.25748786,
 0.68325630]
```

```text
E7:
r = -0.692946898388918
t = -3.0392858130568103
df = 10
p = 0.012477778474456967
IC 95 % ≈
[-0.90639165,
 -0.19764567]

Spearman ≈ -0.6825407440709865
```

```text
E8:
Pearson ≈ 0.7095690774429321
Spearman = 1
S = 0
p exacto para rho perfecto con n = 8 ≈
0.0000496031746031746
```

# Declaración de lock

M10 queda pedagógicamente cerrado con 8 ejercicios.

- **Sintaxis nueva:** `method = "spearman"`, uso explícito de `method = "pearson"`, `cor.test()`.
- **Sintaxis recuperada:** `plot()`, `cor()`, `$`.
- **Pearson:** asociación aproximadamente lineal.
- **Spearman:** asociación monotónica basada en orden/rangos.
- **Tercera ruta:** patrones no lineales y no monotónicos pueden requerir que ninguno de los dos sea un resumen único suficiente.
- **Inferencia:** muestra → pregunta poblacional → `cor.test()`.
- **p-value:** compatibilidad de datos con H0, no probabilidad de H0 ni tamaño.
- **IC:** incertidumbre/precisión para Pearson cuando R lo proporciona.
- **Asimetría de output:** no se exige IC en la ruta Spearman estándar de R base.
- **Checkpoint D:** M10-E8, base nueva, ruta Spearman autónoma.
- **Contrato de datos:** M10 añade `edad` y `horas_ocio` a `encuesta_social`.
- **Recuperación futura:** M11, M12 y M13.
- **Puente M11:** una relación → varias relaciones.

# M10 PEDAGOGICALLY LOCKED
