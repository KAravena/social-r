"""Social R - Canonical High-Density Student Microcopy (All 88 Exercises)

Audited, concise microcopy designed to maximize pedagogical density,
eliminate redundant prose, and allow exercises to fit without unnecessary scroll.
"""
from __future__ import annotations

STUDENT_MICROCOPY: dict[str, dict[str, str]] = {
    # =========================================================================
    # MÓDULO 1
    # =========================================================================
    "intro-r-01-001": {
        "context": "Dos grupos respondieron una encuesta: uno aportó 18 respuestas y otro 12. R evalúa instrucciones y muestra el resultado en la consola.",
        "instruction": "Coloca el cursor en la línea con `18 + 12`, presiona **Ctrl + Enter** y observa el resultado `30` en la **Consola R**.",
        "objective": "Ejecutar una instrucción con Ctrl + Enter y localizar el resultado en la consola.",
    },
    "intro-r-01-002": {
        "context": "El segundo grupo actualizó su conteo a **15** respuestas. Al modificar una instrucción y reejecutarla, R recalcula el resultado.",
        "instruction": "Cambia `12` por `15` en la suma (`18 + 15`) y ejecuta con **Ctrl + Enter** para obtener el total actualizado.",
        "objective": "Modificar un valor en una instrucción existente y reejecutar para actualizar el resultado.",
    },
    "intro-r-01-003": {
        "context": "Para conservar un valor y reutilizarlo, lo guardamos en un **objeto** con `<-`:\n\n`respuestas <- 33`\n\nLa asignación guarda el valor sin imprimirlo. Para consultar su contenido, escribe el nombre del objeto: `respuestas`.",
        "instruction": "1. Ejecuta `respuestas <- 33` para guardar el valor.\n2. Ejecuta `respuestas` para consultar el contenido guardado.",
        "objective": "Guardar un valor en un objeto con `<-` y consultar su contenido por su nombre.",
    },
    "intro-r-01-004": {
        "context": "La encuesta recibió 18 respuestas de Sociología y 15 de Antropología. El primer objeto ya está creado:\n\n`respuestas_sociologia <- 18`",
        "instruction": "Crea el objeto `respuestas_antropologia` con el valor `15` y consulta ambos objetos para comprobar qué guardó cada uno.",
        "objective": "Crear un objeto con `<-` y consultar múltiples objetos.",
    },
    "intro-r-01-005": {
        "context": "Los objetos guardados pueden reutilizarse en nuevas operaciones y almacenarse en otro objeto para continuar el análisis.",
        "instruction": "Crea `total_respuestas` sumando `respuestas_sociologia + respuestas_antropologia`. Luego consúltalo.",
        "objective": "Operar con objetos existentes y almacenar el resultado en un nuevo objeto.",
    },
    "intro-r-01-006": {
        "context": "Los objetos guardan distintos tipos de información:\n\n- **Números**: van sin comillas (`20`).\n- **Texto**: va entre comillas (`\"Historia\"`).",
        "instruction": "Actualiza los objetos para guardar `21` en `edad` y `\"Sociología\"` en `carrera`. Luego consúltalos.",
        "objective": "Distinguir números de texto respetando el uso de comillas.",
    },
    "intro-r-01-007": {
        "context": "Los errores en R son mensajes informativos, no fallas permanentes. Aquí intentamos sumar un número con un texto:\n\n`18 + \"15\"`\n\nR no puede operar matemáticamente con texto entre comillas.",
        "instruction": "Quita las comillas de `\"15\"` en `respuestas_antropologia` para guardarlo como número, conserva la suma con `respuestas_sociologia` y ejecuta para calcular `total_respuestas`.",
        "objective": "Identificar y corregir un error de tipo numérico almacenado como texto.",
    },
    "intro-r-01-008": {
        "context": "Una encuesta piloto llamada **“Encuesta de vida universitaria”** recibió 14 respuestas de Sociología y 11 de Antropología.",
        "instruction": "Construye un script que:\n1. Guarde el nombre del estudio en `estudio`.\n2. Guarde los conteos en `respuestas_sociologia` (`14`) y `respuestas_antropologia` (`11`).\n3. Sume ambos objetos en `total_respuestas` y consúltalo.",
        "objective": "Integrar texto, números y reutilización de objetos en un script completo.",
    },
    # =========================================================================
    # MÓDULO 2
    # =========================================================================
    "intro-r-02-001": {
        "context": "Para guardar varios valores juntos en un solo objeto usamos un **vector** mediante `c()`:\n\n`tiempos_viaje <- c(25, 40, 35, 50, 30)`\n\n`c()` combina los valores conservando su orden (1°: 25, 2°: 40, 3°: 35, etc.).",
        "instruction": "Ejecuta la asignación de `tiempos_viaje` y consúltalo para observar los cinco valores ordenados dentro del vector.",
        "objective": "Crear un vector con `c()` y comprender que almacena múltiples valores ordenados.",
    },
    "intro-r-02-002": {
        "context": "Cinco personas informaron estos tiempos de viaje en minutos: **20, 35, 45, 25 y 30**, en ese orden.",
        "instruction": "Crea el objeto `tiempos_viaje` con los cinco valores usando `c()` y consúltalo en la consola.",
        "objective": "Construir un vector numérico con valores en un orden determinado.",
    },
    "intro-r-02-003": {
        "context": "Las funciones en R reciben datos entre paréntesis y devuelven un resultado:\n\n`sum(respuestas_diarias)`\n\n`sum()` recibe un vector completo y suma todos sus elementos.",
        "instruction": "Aplica `sum()` a `respuestas_diarias`, guarda el resultado en `total_respuestas` y consúltalo.",
        "objective": "Aplicar una función como `sum()` a un vector completo y guardar el resultado.",
    },
    "intro-r-02-004": {
        "context": "Para recuperar un valor según su posición usamos corchetes `[]`. En R las posiciones comienzan en 1:\n\n`tiempos_viaje[3]` recupera el tercer valor (`35`), no el número 3.",
        "instruction": "Recupera la tercera observación de `tiempos_viaje` ejecutando `tiempos_viaje[3]`.",
        "objective": "Recuperar un valor individual de un vector usando corchetes de posición `[]`.",
    },
    "intro-r-02-005": {
        "context": "Para recuperar varias posiciones pasamos un vector dentro de los corchetes:\n\n`tiempos_viaje[c(2, 5)]`\n\nExtrae los valores de las posiciones 2 y 5 (`40` y `30`).",
        "instruction": "Recupera los tiempos de las posiciones 2 y 5 ejecutando `tiempos_viaje[c(2, 5)]`.",
        "objective": "Seleccionar múltiples posiciones de un vector combinando `[]` y `c()`.",
    },
    "intro-r-02-006": {
        "context": "Cinco estudiantes informaron que estudiaron **2, 4, 3, 5 y 1** horas, en ese orden.",
        "instruction": "1. Guarda los cinco valores juntos en `horas_estudio`.\n2. Calcula la suma de todos los valores y guárdala en `total`.\n3. Recupera la cuarta observación y guárdala en `cuarta`.",
        "objective": "Integrar creación, suma y selección por posición de un vector.",
    },
    "intro-r-02-007": {
        "context": "Durante cinco semanas se registraron estas participaciones: **3, 1, 4, 2 y 5**, en ese orden.",
        "instruction": "1. Guarda los cinco valores en `participacion`.\n2. Calcula el total acumulado y guárdalo en `total`.\n3. Guarda los valores de las semanas 2 y 5 en `seleccion`.",
        "objective": "Resolver agregación y selección sobre un vector con autonomía.",
    },
    # =========================================================================
    # MÓDULO 3
    # =========================================================================
    "intro-r-03-001": {
        "context": "Hasta ahora buscabas valores por su posición. Con R también podemos formular **preguntas de comparación** sobre los datos:\n\n`35 > 30` → `TRUE`\n`25 > 30` → `FALSE`\n\n`>` se lee **“es mayor que”**.\n\n`TRUE` indica que la afirmación se cumple; `FALSE`, que no se cumple. Ambos son **valores lógicos** producidos por R al evaluar la pregunta.",
        "instruction": "Antes de ejecutar, predice el resultado de cada comparación. Luego ejecuta el código en el editor y comprueba cómo responde R.",
        "objective": "Interpretar comparaciones con `>`, `TRUE` y `FALSE`.",
    },
    "intro-r-03-002": {
        "context": "Al comparar un vector con un valor, R evalúa la condición elemento por elemento en el mismo orden:\n\n`tiempos_viaje > 30`\n\n`c(25, 40, 35, 50, 30) > 30` → `FALSE, TRUE, TRUE, TRUE, FALSE`",
        "instruction": "Ejecuta `tiempos_viaje > 30` y comprueba cómo R responde con un `TRUE` o `FALSE` para cada posición.",
        "objective": "Comprender la evaluación vectorizada de una comparación lógica elemento por elemento.",
    },
    "intro-r-03-003": {
        "context": "El resultado de una comparación puede guardarse en un objeto. Como contiene respuestas `TRUE` y `FALSE`, forma una secuencia de respuestas lógicas:\n\n`supera_30 <- tiempos_viaje > 30`\n\nEsta forma de guardar valores lógicos se conoce como vector lógico.",
        "instruction": "Guarda la comparación en `supera_30` y consulta el nuevo objeto con respuestas lógicas.",
        "objective": "Guardar el resultado de una comparación en un objeto.",
    },
    "intro-r-03-004": {
        "context": "Usa el vector de `TRUE` y `FALSE` dentro de los corchetes:\n\n`tiempos_viaje[supera_30]`\n\nR conserva las posiciones marcadas con `TRUE` y deja fuera las que tienen `FALSE`.\n\nSolo permanecen los tiempos mayores a 30 (`40, 35, 50`). Esta forma de elegir valores se llama selección lógica.",
        "instruction": "Ejecuta `tiempos_viaje[supera_30]` y comprueba cómo la selección conserva únicamente los valores donde la respuesta fue `TRUE`.",
        "objective": "Seleccionar elementos de un vector usando respuestas lógicas dentro de `[]`.",
    },
    "intro-r-03-005": {
        "context": "Podemos seleccionar directamente escribiendo la pregunta dentro de los corchetes, sin necesidad de crear un objeto intermedio.",
        "instruction": "Encuentra las horas de estudio que superan 4 seleccionando con corchetes `[]` sobre `horas_estudio`.",
        "objective": "Seleccionar valores combinando corchetes y condición en un solo paso.",
    },
    "intro-r-03-006": {
        "context": "Para comparar texto usamos el operador de igualdad `==` (a diferencia de `<-` que sirve para guardar):\n\n`carreras == \"Sociología\"`\n\nDevuelve `TRUE` donde coincide el texto y `FALSE` donde difiere.",
        "instruction": "1. Guarda `carreras == \"Sociología\"` en `es_sociologia` y consúltalo.\n2. Filtra las observaciones correspondientes con `carreras[es_sociologia]`.",
        "objective": "Comparar categorías con `==` y filtrar elementos por coincidencia de texto.",
    },
    "intro-r-03-007": {
        "context": "Cinco personas registraron **6, 12, 8, 15 y 10** sesiones de participación comunitaria.",
        "instruction": "Usando lo aprendido:\n1. Guarda esos valores en un objeto llamado `sesiones`.\n2. Identifica cuáles son mayores que 8 y guarda esa respuesta en `mas_de_ocho`.\n3. Usa esa respuesta para guardar las sesiones seleccionadas en `seleccionadas`.",
        "objective": "Integrar de forma autónoma el flujo: datos → vector → condición lógica → selección.",
    },
    # =========================================================================
    # MÓDULO 4
    # =========================================================================
    "intro-r-04-001": {
        "context": "Un **data frame** organiza múltiples características de las mismas personas en una tabla:\n\n- **Filas (casos)**: cada fila reúne todas las respuestas de una persona.\n- **Columnas (variables)**: cada columna mide una misma característica para todos los casos.\n\n```text\n             edad   horas_estudio   carrera\nPersona 1      20         3         Sociología\nPersona 2      22         5         Historia\nPersona 3      19         2         Antropología\nPersona 4      21         4         Sociología\n```",
        "instruction": "Revisa la tabla y guarda en `edad_persona_2` la edad de la persona que estudia 5 horas (Persona 2).",
        "objective": "Comprender la estructura de un data frame: filas como casos y columnas como variables.",
    },
    "intro-r-04-002": {
        "context": "Al leer una base:\n\n- Una **fila** muestra varias características de un mismo caso.\n- Una **columna** muestra los valores de una misma variable para todos los casos, funcionando como un vector.",
        "instruction": "Escribe las cuatro edades de la encuesta como un vector y guárdalas en `edades_encuesta`.",
        "objective": "Distinguir la lectura por filas (casos) de la lectura por columnas (variables).",
    },
    "intro-r-04-003": {
        "context": "Una base de datos real puede contener miles de filas. Para explorar su estructura inicial sin imprimirla completa usamos `head()`:\n\n`head(encuesta_social_demo)`\n\nMuestra únicamente las primeras 6 filas.",
        "instruction": "Ejecuta `head(encuesta_social_demo)` y observa las primeras filas y columnas de la base.",
        "objective": "Explorar las primeras filas de una base de datos con `head()`.",
    },
    "intro-r-04-004": {
        "context": "Para extraer una columna de un data frame como vector usamos el operador `$`: `base$variable`.\n\n`encuesta_social_demo$edad`\n\nRecupera todos los valores de la variable `edad` como un vector.",
        "instruction": "Extrae la variable `horas_estudio` de `encuesta_social_demo` usando el operador `$`.",
        "objective": "Extraer una variable de un data frame como vector usando el operador `$`.",
    },
    "intro-r-04-005": {
        "context": "`str()` resume la estructura técnica de una base: cantidad de observaciones, número de variables, nombres y tipo de almacenamiento (`num`, `chr`, etc.):\n\n`str(encuesta_social_demo)`",
        "instruction": "Ejecuta `str(encuesta_social_demo)` y revisa la lista de variables y el número de casos en la consola.",
        "objective": "Inspeccionar la estructura de un data frame usando `str()`.",
    },
    "intro-r-04-006": {
        "context": "Dispones de una base con cuatro observaciones sobre transporte y tiempos de viaje:\n\n```text\nencuesta_barrio\npersona   edad   transporte   minutos_viaje\n1         34     Bus          45\n2         27     Metro        30\n3         41     Bus          50\n4         22     Bicicleta    20\n```",
        "instruction": "Extrae la columna `minutos_viaje` desde `encuesta_barrio` utilizando el operador `$`.",
        "objective": "Extraer una columna de un data frame como vector usando el operador `$`.",
    },
    # =========================================================================
    # MÓDULO 5
    # =========================================================================
    "intro-r-05-001": {
        "context": "En el Módulo 3 hicimos preguntas a vectores. En el Módulo 4 aprendimos que una columna de una base se extrae como un vector con `$`. Ahora juntamos ambas ideas para formular preguntas sobre una base.",
        "instruction": "Pregunta qué edades en `encuesta_social_demo` son mayores que 21 combinando el operador `$` y `> 21`.",
        "objective": "Formular una condición lógica sobre una columna de un data frame con `$`.",
    },
    "intro-r-05-002": {
        "context": "En una base de datos, una respuesta `TRUE` puede conservar la fila completa con todas sus variables:\n\n`mayores_21 <- encuesta_social_demo$edad > 21`\n`encuesta_social_demo[mayores_21, ]`",
        "instruction": "Ejecuta el código en el editor para comprobar cómo la condición `> 21` y cada `TRUE` conservan a la persona completa con todas sus columnas.",
        "objective": "Comprender cómo una condición lógica conserva casos completos en una base.",
    },
    "intro-r-05-003": {
        "context": "`filter()` conserva las filas donde la condición se cumple:\n\n`filter(base, condicion)`\n\nDentro de `filter()` escribimos directamente el nombre de la columna (`edad > 21`) sin necesidad de usar `$`.",
        "instruction": "Ejecuta el pipeline `encuesta_social_demo |> filter(edad > 21)` y comprueba las filas conservadas.",
        "objective": "Filtrar casos de un data frame usando `filter()` y condiciones directas.",
    },
    "intro-r-05-004": {
        "context": "Para filtrar por una categoría de texto usamos `==` con el texto exacto entre comillas:\n\n`filter(base, variable == \"Categoría\")`",
        "instruction": "Filtra `encuesta_social_demo` para conservar únicamente a los estudiantes de Sociología (`carrera == \"Sociología\"`).",
        "objective": "Filtrar casos evaluando una condición de igualdad de texto con `==`.",
    },
    "intro-r-05-005": {
        "context": "El operador pipe `|>` pasa los datos de una etapa a la siguiente:\n\n`base |> filter(condicion)`\n\nEsta operación produce un resultado nuevo sin modificar la base original guardada en memoria.",
        "instruction": "Filtra a los estudiantes de Sociología pasando la base con el pipe: `encuesta_social_demo |> filter(carrera == \"Sociología\")`.",
        "objective": "Encadenar una transformación con el pipe `|>` preservando la base original.",
    },
    "intro-r-05-006": {
        "context": "Mientras `filter()` elige **casos (filas)**, `select()` elige **variables (columnas)** por su nombre:\n\n- `filter(edad > 20)` → conserva filas\n- `select(edad, carrera)` → conserva columnas",
        "instruction": "Selecciona únicamente las columnas `edad` y `carrera` de `encuesta_social_demo` usando `select()`.",
        "objective": "Seleccionar variables de un data frame por su nombre usando `select()`.",
    },
    "intro-r-05-007": {
        "context": "El pipe permite encadenar múltiples decisiones en un flujo de lectura claro:\n\n```r\nbase |>\n  filter(condicion) |>\n  select(var1, var2)\n```",
        "instruction": "Construye un pipeline que primero filtre a las personas que trabajan (`trabaja == \"Sí\"`) y luego seleccione las columnas `edad` y `carrera`.",
        "objective": "Combinar `filter()` y `select()` en un pipeline encadenado con `|>`.",
    },
    "intro-r-05-008": {
        "context": "**Checkpoint B — Bases y preparación**\n\nPara una investigación social necesitamos trabajar solo con las personas que estudian en `encuesta_jovenes`. De ellas necesitamos únicamente su edad y comuna.",
        "instruction": "Construye un flujo con `|>` que conserve a quienes estudian (`estudia == \"Sí\"`), seleccione las variables `edad` y `comuna`, y guarde el resultado en `datos_preparados`.",
        "objective": "Preparar un subconjunto de datos combinando `filter()` y `select()` de forma autónoma.",
    },
    # =========================================================================
    # MÓDULO 6
    # =========================================================================
    "intro-r-06-001": {
        "context": "En encuestas sociales es común que algunas personas no respondan. En R, la ausencia de información se representa con `NA` (sin comillas):\n\n- `0`: es un valor observado (reportó cero).\n- `NA`: el dato no está disponible (desconocido).",
        "instruction": "Consulta el vector `horas_cuidado` y distingue las posiciones con valor observado `0` de las posiciones con dato ausente `NA`.",
        "objective": "Identificar `NA` como ausencia de dato y distinguirlo del valor numérico `0`.",
    },
    "intro-r-06-002": {
        "context": "Para detectar datos ausentes usamos `is.na()`. Devuelve `TRUE` donde falta información y `FALSE` donde hay un valor disponible:\n\n`is.na(c(6, 0, NA))` → `FALSE, FALSE, TRUE`",
        "instruction": "Aplica `is.na(horas_cuidado)` y observa en qué posiciones aparece `TRUE`.",
        "objective": "Detectar valores ausentes en un vector mediante la función lógica `is.na()`.",
    },
    "intro-r-06-003": {
        "context": "En operaciones aritméticas, R trata a `TRUE` como 1 y a `FALSE` como 0. Por eso podemos contar cuántos datos faltan sumando los valores lógicos:\n\n`sum(is.na(vector))`",
        "instruction": "Cuenta los valores ausentes en `horas_cuidado` combinando `sum()` e `is.na()`.",
        "objective": "Contar la cantidad de valores ausentes combinando `sum()` e `is.na()`.",
    },
    "intro-r-06-004": {
        "context": "Si un vector contiene `NA`, `sum()` devuelve `NA` porque el total exacto se desconoce. Para sumar los valores efectivamente registrados usamos `na.rm = TRUE`:\n\n`sum(horas_cuidado, na.rm = TRUE)`",
        "instruction": "Calcula la suma de los valores disponibles en `horas_cuidado` agregando el argumento `na.rm = TRUE`.",
        "objective": "Calcular estadísticas sobre datos disponibles usando el argumento `na.rm = TRUE`.",
    },
    "intro-r-06-005": {
        "context": "Queremos estudiar las horas dedicadas al cuidado de las personas que trabajan en `encuesta_social_demo`.",
        "instruction": "1. Prepara `datos_trabajan` filtrando a quienes trabajan (`trabaja == \"Sí\"`) y seleccionando `id` y `horas_cuidado`.\n2. Cuenta cuántos valores ausentes hay en `horas_cuidado` de ese grupo usando `sum(is.na())`.",
        "objective": "Preparar datos y diagnosticar valores ausentes en el grupo obtenido.",
    },
    "intro-r-06-006": {
        "context": "La base `encuesta_barrio` registra los minutos de viaje de seis personas, pero algunos datos no están disponibles.",
        "instruction": "1. Revisa dónde faltan datos en `minutos_viaje` y cuenta las ausencias.\n2. Calcula el total de minutos de viaje sumando los valores disponibles con `sum()` y `na.rm = TRUE`.",
        "objective": "Diagnosticar valores ausentes y calcular estadísticas con datos disponibles de forma autónoma.",
    },
    # =========================================================================
    # MÓDULO 7
    # =========================================================================
    "intro-r-07-001": {
        "context": "Para elegir el análisis correcto debemos distinguir dos tipos de información:\n\n- **Categoría**: nombres, grupos o etiquetas (ej. carrera, zona).\n- **Cantidad**: mediciones numéricas donde tiene sentido sumar o promediar (ej. horas, edad).",
        "instruction": "Clasifica cada variable asignando `\"categoria\"` o `\"cantidad\"` a `tipo_carrera`, `tipo_horas` y `tipo_zona_codigo`.",
        "objective": "Diferenciar variables categóricas de cuantitativas por su significado sustantivo.",
    },
    "intro-r-07-002": {
        "context": "Para resumir una variable categórica contamos cuántos casos hay en cada grupo mediante una tabla de frecuencias:\n\n`tabla_carrera <- table(encuesta_social_demo$carrera)`\n\nCada número indica la **frecuencia** observada.",
        "instruction": "Construye la tabla de frecuencias de `carrera` usando `table()` y guárdala en `tabla_carrera`.",
        "objective": "Construir e interpretar una tabla de frecuencias con `table()`.",
    },
    "intro-r-07-003": {
        "context": "Para saber qué fracción del total representa cada categoría convertimos la tabla en **proporciones** con `prop.table()`:\n\n`prop.table(tabla_carrera)`\n\nCada valor va de 0 a 1 y la suma de todas las celdas es 1.",
        "instruction": "Calcula las proporciones de cada carrera aplicando `prop.table()` a `tabla_carrera`.",
        "objective": "Calcular proporciones a partir de una tabla de frecuencias con `prop.table()`.",
    },
    "intro-r-07-004": {
        "context": "Una categoría puede describirse por su conteo (frecuencia) o por su peso relativo (proporción o porcentaje respecto al total):\n\n`prop.table(tabla) * 100`",
        "instruction": "1. Cuenta cuántas personas hay por carrera en `encuesta_social_demo$carrera` y guarda la tabla en `tabla_carrera`.\n2. Obtén las proporciones de esa tabla aplicando `prop.table(tabla_carrera)`.",
        "objective": "Calcular frecuencias y proporciones sobre una variable categórica.",
    },
    "intro-r-07-005": {
        "context": "Un **gráfico de barras** muestra visualmente la distribución de una variable categórica:\n\n`barplot(tabla_carrera)`\n\nCada barra representa una categoría y su altura refleja la frecuencia observada.",
        "instruction": "Genera el gráfico de barras de `tabla_carrera` ejecutando `barplot(tabla_carrera)`.",
        "objective": "Visualizar la distribución de frecuencias de una variable categórica con `barplot()`.",
    },
    "intro-r-07-006": {
        "context": "En `encuesta_campus` se consultó el medio de transporte principal de ocho estudiantes.",
        "instruction": "1. Cuenta cuántos estudiantes usan cada transporte en `encuesta_campus$transporte` y guarda la tabla en `tabla_transporte`.\n2. Obtén las proporciones con `prop.table()` y visualiza la distribución con `barplot()`.",
        "objective": "Describir una variable categórica nueva combinando tabla, proporciones y gráfico de barras.",
    },
    # =========================================================================
    # MÓDULO 8
    # =========================================================================
    "intro-r-08-001": {
        "context": "Para explorar una variable cuantitativa observamos cómo se reparten sus valores mediante un **histograma**:\n\n`hist(encuesta_social_demo$horas_estudio)`\n\nEl eje horizontal muestra intervalos continuos y la altura de cada barra refleja cuántos casos caen en ese rango.",
        "instruction": "Genera un histograma de `horas_estudio` con `hist()` y observa la forma de la distribución.",
        "objective": "Visualizar la distribución de una variable cuantitativa con un histograma mediante `hist()`.",
    },
    "intro-r-08-002": {
        "context": "La **media** resume el centro repartiendo la suma total de valores por igual entre todos los casos:\n\n`mean(encuesta_social_demo$horas_estudio)`\n\nLa media se expresa en la misma unidad de medida (horas de estudio).",
        "instruction": "Calcula la media de `horas_estudio` usando `mean()` e interpreta el centro de la distribución.",
        "objective": "Calcular e interpretar la media aritmética de una variable con `mean()`.",
    },
    "intro-r-08-003": {
        "context": "La **mediana** es el valor que ocupa la posición central una vez ordenados los datos de menor a mayor:\n\n`median(minutos_lectura)`\n\nDeja exactamente el 50% de las observaciones por debajo y el 50% por encima.",
        "instruction": "Calcula la mediana de `minutos_lectura` usando `median()` e identifica el valor central.",
        "objective": "Calcular e interpretar la mediana como medida de centro basada en el orden con `median()`.",
    },
    "intro-r-08-004": {
        "context": "Compara dos grupos donde solo cambia un valor extremo:\n\n- `viaje_regular`: 20, 22, 24, 25, 26, 28, **30**\n- `viaje_extremo`: 20, 22, 24, 25, 26, 28, **120**\n\nLa media es sensible a valores extremos, mientras que la mediana es resistente (robusta).",
        "instruction": "Calcula `mean()` y `median()` para `viaje_extremo` y observa cuál describe mejor un tiempo típico.",
        "objective": "Evaluar la sensibilidad de la media y la robustez de la mediana ante valores extremos.",
    },
    "intro-r-08-005": {
        "context": "Dos grupos pueden tener la misma media pero comportarse diferente. La **desviación estándar** mide qué tan dispersos están los datos respecto a su media:\n\n`sd(grupo_a)`\n`sd(grupo_b)`\n\nA mayor dispersión, mayor es la desviación estándar.",
        "instruction": "Calcula la desviación estándar de `grupo_a` y `grupo_b` con `sd()` para comparar su dispersión.",
        "objective": "Calcular e interpretar la desviación estándar con `sd()` como medida de dispersión.",
    },
    "intro-r-08-006": {
        "context": "Queremos describir las horas de cuidado de las personas que no trabajan (`trabaja == \"No\"`) en `encuesta_social_demo`.",
        "instruction": "1. Prepara `datos_no_trabajan` filtrando los casos donde `trabaja == \"No\"`.\n2. Calcula la media de `horas_cuidado` en ese grupo usando `mean()` con `na.rm = TRUE`.",
        "objective": "Filtrar un subgrupo y calcular media y dispersión sobre los datos disponibles.",
    },
    "intro-r-08-007": {
        "context": "**Checkpoint C — Describir una variable cuantitativa**\n\nDescribe la variable `minutos_viaje` de `encuesta_movilidad` evaluando forma, centro y dispersión.",
        "instruction": "Genera el histograma con `hist()`, calcula `mean()`, `median()` y `sd()`, e interpreta qué estadístico resume mejor el centro.",
        "objective": "Analizar autónomamente una variable cuantitativa mediante histograma, centro y dispersión.",
    },
    # =========================================================================
    # MÓDULO 9
    # =========================================================================
    "intro-r-09-001": {
        "context": "En un gráfico de dispersión, cada punto representa a una persona y reúne dos mediciones simultáneas: una en el eje horizontal (x) y otra en el vertical (y).\n\nCaso 3: 3 horas de estudio y puntaje 58 en métodos.",
        "instruction": "Guarda en `par_persona_3` el par `c(x, y)` con las horas de estudio (3) y el puntaje en métodos (58) de la Persona 3.",
        "objective": "Identificar un caso bivariado como un par de coordenadas (x, y).",
    },
    "intro-r-09-002": {
        "context": "En un **diagrama de dispersión (scatterplot)** cada caso se representa como un punto en el plano:\n\n`plot(x, y)`\n\n`plot(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)`",
        "instruction": "Genera el diagrama de dispersión entre `horas_estudio` y `puntaje_metodos` con `plot()`.",
        "objective": "Generar e interpretar un diagrama de dispersión bivariado con `plot(x, y)`.",
    },
    "intro-r-09-003": {
        "context": "La dirección de una relación describe cómo varía una cantidad cuando la otra aumenta:\n\n- **Positiva**: asciende de izquierda a derecha.\n- **Negativa**: desciende de izquierda a derecha.\n- **Sin dirección**: los puntos forman una nube dispersa sin tendencia clara.\n\n*Nota: Asociación no implica causalidad.*",
        "instruction": "Asigna `\"positiva\"`, `\"negativa\"` o `\"sin_direccion\"` a `direccion_a`, `direccion_b` y `direccion_c` según corresponda a cada gráfico.",
        "objective": "Identificar la dirección de una relación en un scatterplot distinguiéndola de causalidad.",
    },
    "intro-r-09-004": {
        "context": "Dos relaciones pueden ir en la misma dirección pero tener distinta concentración de puntos alrededor de una recta.",
        "instruction": "Observa los gráficos A y B. Guarda en `grafico_mas_concentrado` cuál de los dos (`\"A\"` o `\"B\"`) muestra los puntos más alineados alrededor de la recta.",
        "objective": "Evaluar forma, fuerza y presencia de valores atípicos en un diagrama de dispersión.",
    },
    "intro-r-09-005": {
        "context": "El **coeficiente de correlación de Pearson ($r$)** resume la fuerza y dirección de una relación lineal:\n\n`cor(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)`\n\nVaría entre -1 y +1. Valores cercanos a +1 indican asociación lineal positiva fuerte; cercanos a 0, ausencia de asociación lineal.",
        "instruction": "Calcula el coeficiente de Pearson entre `horas_estudio` y `puntaje_metodos` con `cor()` e interpreta su magnitud.",
        "objective": "Calcular e interpretar el coeficiente de correlación lineal de Pearson con `cor()`.",
    },
    "intro-r-09-006": {
        "context": "Para calcular una correlación con datos ausentes debemos conservar únicamente los casos con información en ambas variables:\n\n`cor(x, y, use = \"complete.obs\")`",
        "instruction": "Calcula la correlación de Pearson entre `horas_trabajo` y `horas_sueno` en `encuesta_social` indicando el argumento de pares completos `use = \"complete.obs\"`.",
        "objective": "Manejar datos ausentes bivariados en `cor()` mediante `use = \"complete.obs\"`.",
    },
    "intro-r-09-007": {
        "context": "En `encuesta_lectura` queremos estudiar si los minutos de lectura y la comprensión lectora están asociados linealmente.",
        "instruction": "Genera el scatterplot con `plot()` y calcula el coeficiente de Pearson con `cor()` para evaluar la relación.",
        "objective": "Analizar autónomamente una relación bivariada combinando gráfico de dispersión y correlación de Pearson.",
    },
    # =========================================================================
    # MÓDULO 10
    # =========================================================================
    "intro-r-10-001": {
        "context": "No todas las relaciones siguen una línea recta. Si una relación es creciente pero curva, conserva el orden relativo de los casos (**relación monótona**).\n\nEl coeficiente de **Spearman** resume relaciones monótonas basándose en los rangos (orden) de los datos:\n\n`cor(x, y, method = \"spearman\")`",
        "instruction": "Compara los gráficos de la relación lineal y de la relación curva monótona en los datos.",
        "objective": "Distinguir una relación lineal de una relación monótona no lineal y reconocer el uso de Spearman.",
    },
    "intro-r-10-002": {
        "context": "Cuando una relación conserva el orden de los casos aunque sea curva, Spearman devuelve valores cercanos a 1 porque evalúa rangos y no distancias lineales métricas.",
        "instruction": "Calcula el coeficiente de Spearman para la relación no lineal ejecutando `cor(x_curva, y_curva, method = \"spearman\")`.",
        "objective": "Calcular e interpretar el coeficiente de correlación de Spearman basado en rangos.",
    },
    "intro-r-10-003": {
        "context": "Criterio de elección de coeficiente según la forma de la relación:\n\n- **Aproximadamente lineal**: Pearson.\n- **Monótona curva**: Spearman.\n- **No monótona (cambia de dirección)**: ninguno como resumen único suficiente.",
        "instruction": "Asigna el método adecuado (`\"pearson\"`, `\"spearman\"` o `\"ninguno\"`) a `metodo_a`, `metodo_b` y `metodo_c` para cada escenario.",
        "objective": "Elegir justificadamente entre Pearson y Spearman a partir de la forma observada en el scatterplot.",
    },
    "intro-r-10-004": {
        "context": "Para evaluar si la correlación observada en una muestra aporta evidencia sobre una asociación en la población usamos `cor.test()`:\n\n`cor.test(x, y)`\n\nEntrega: estimación puntual (`estimate`), significación (`p-value`) e intervalo de confianza del 95% (`conf.int`).",
        "instruction": "Ejecuta `cor.test(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)` y localiza estimate, p-value e intervalo de confianza.",
        "objective": "Ejecutar una prueba de correlación con `cor.test()` e identificar sus componentes clave.",
    },
    "intro-r-10-005": {
        "context": "En una prueba de correlación:\n\n- **Hipótesis nula ($H_0$)**: no hay correlación en la población ($r = 0$).\n- **p-value**: mide qué tan compatibles son los datos observados con $H_0$. Un valor p pequeño ($p < 0.05$) indica que los datos son poco compatibles con la ausencia de relación.",
        "instruction": "Evalúa cada afirmación sobre el valor p asignando `TRUE` o `FALSE` a `afirmacion_probabilidad_h0` e `afirmacion_incompatibilidad`.",
        "objective": "Comprender la hipótesis nula en correlación y el p-value como medida de compatibilidad con $H_0$.",
    },
    "intro-r-10-006": {
        "context": "No confundas **magnitud** ($r$) con **evidencia** ($p$):\n\nDos muestras pueden tener la misma correlación ($r = 0.50$), pero con mayor tamaño muestral ($N$) el p-value es más pequeño y el intervalo de confianza es más estrecho y preciso.",
        "instruction": "Compara ambos estudios con r = 0.50. Asigna `\"Estudio A\"` o `\"Estudio B\"` a `estudio_menor_p` y a `estudio_mayor_precision`.",
        "objective": "Diferenciar magnitud del efecto, significación inferencial y precisión según el tamaño muestral.",
    },
    "intro-r-10-007": {
        "context": "En `encuesta_emprendimiento` queremos evaluar la relación entre la antigüedad del negocio y sus ventas mensuales.",
        "instruction": "Genera el scatterplot, evalúa si la relación es lineal o monótona curva y ejecuta `cor.test()` con el método apropiado.",
        "objective": "Conducir una evaluación correlacional completa: gráfico, elección de método y prueba de hipótesis.",
    },
    "intro-r-10-008": {
        "context": "**Checkpoint D — Decidir y evaluar una correlación**\n\nEn `encuesta_emprendimiento` relacionamos los años de antigüedad de 8 negocios con sus ventas mensuales.",
        "instruction": "Evalúa si la relación entre `antiguedad_anos` y `ventas_mensuales` es lineal o curva monótona, y aplica la prueba de correlación adecuada con `cor.test()`.",
        "objective": "Decidir el método de correlación pertinente y evaluar su evidencia inferencial de forma integrada.",
    },
    # =========================================================================
    # MÓDULO 11
    # =========================================================================
    "intro-r-11-001": {
        "context": "Para examinar relaciones entre varias variables cuantitativas preparamos una base que contenga únicamente las variables numéricas de interés (excluyendo identificadores como `id`).",
        "instruction": "Selecciona las variables `edad`, `horas_estudio` y `horas_ocio` de `encuesta_social` con `select()` y guárdalas en `analisis`.",
        "objective": "Seleccionar un conjunto de variables cuantitativas sustantivas para análisis multivariado.",
    },
    "intro-r-11-002": {
        "context": "Al aplicar `cor()` a un conjunto de variables numéricas obtenemos una **matriz de correlaciones**, donde cada celda muestra la correlación entre la variable de la fila y la variable de la columna:\n\n`cor(analisis)`",
        "instruction": "Calcula la matriz de correlaciones de las tres variables ejecutando `cor(analisis)`.",
        "objective": "Calcular e interpretar una matriz de correlaciones bivariadas con `cor()`.",
    },
    "intro-r-11-003": {
        "context": "Propiedades de una matriz de correlaciones:\n\n- **Diagonal**: vale 1 porque cada variable se correlaciona perfectamente consigo misma.\n- **Simetría**: la correlación entre A y B es idéntica a la de B y A. En una matriz 3×3 solo hay tres pares únicos de relaciones.",
        "instruction": "En una matriz de 3 variables, ¿cuántos pares únicos de correlación existen sin contar la diagonal ni repeticiones? Guarda el número en `pares_unicos`.",
        "objective": "Interpretar la estructura de una matriz de correlaciones reconociendo simetría y pares únicos.",
    },
    "intro-r-11-004": {
        "context": "Manejo de datos ausentes en matrices:\n\n- `complete.obs`: elimina cualquier fila con algún `NA` en cualquiera de las variables (muestra uniforme).\n- `pairwise.complete.obs`: calcula cada par usando los casos disponibles para esas dos variables específicas.",
        "instruction": "Calcula la matriz usando `use = \"pairwise.complete.obs\"` y compara los casos utilizados en cada par.",
        "objective": "Comparar la eliminación por lista (`complete.obs`) frente a eliminación por pares (`pairwise.complete.obs`).",
    },
    "intro-r-11-005": {
        "context": "Una variable binaria (0 = No, 1 = Sí) puede correlacionarse con una cantidad métrica (**correlación punto-biserial**). El signo indica qué grupo tiende a tener valores más altos según cómo se codificó el 1.",
        "instruction": "Calcula la correlación entre la variable binaria `trabaja_01` e `ingreso_miles` con `cor()` e interpreta la dirección.",
        "objective": "Calcular e interpretar una correlación punto-biserial con una variable dicotómica codificada 0/1.",
    },
    "intro-r-11-006": {
        "context": "En `seguimiento` queremos evaluar si existe evidencia de asociación entre las horas de estudio y el estrés de las personas.",
        "instruction": "1. Prepara `analisis_final` seleccionando `horas_estudio` y `estres` de `seguimiento`.\n2. Evalúa inferencialmente la correlación entre ambas variables con `cor.test()`.",
        "objective": "Utilizar una matriz de correlaciones para responder una pregunta sustantiva específica con respaldo inferencial.",
    },
    # =========================================================================
    # MÓDULO 12
    # =========================================================================
    "intro-r-12-001": {
        "context": "Para estudiar la relación entre dos variables categóricas construimos una **tabla de contingencia (cruzada)**:\n\n`tabla <- table(encuesta_participacion$participacion_organizacion, encuesta_participacion$transporte_campus)`\n\nCada celda cuenta cuántas personas combinan ambas categorías.",
        "instruction": "Cruza `participacion_organizacion` y `transporte_campus` con `table()` y guarda el resultado en `tabla`.",
        "objective": "Construir una tabla de contingencia bidimensional con `table(x, y)`.",
    },
    "intro-r-12-002": {
        "context": "Para comparar grupos calculamos porcentajes según el denominador adecuado a la pregunta:\n\n- `prop.table(tabla, 1) * 100`: porcentajes por fila (cada fila suma 100%).\n- `prop.table(tabla, 2) * 100`: porcentajes por columna (cada columna suma 100%).",
        "instruction": "Calcula los porcentajes por fila de `tabla` usando `prop.table(tabla, 1) * 100` para comparar el transporte según participación.",
        "objective": "Calcular porcentajes condicionales por fila o columna en una tabla de contingencia.",
    },
    "intro-r-12-003": {
        "context": "Dos variables son **independientes** si la distribución de una no cambia según la categoría de la otra.\n\n- **Frecuencias observadas ($O$)**: conteos reales en los datos.\n- **Frecuencias esperadas ($E$)**: conteos que esperaríamos si no existiera asociación.",
        "instruction": "Si el 25% del total usa Metro (15 de 60 personas), ¿qué porcentaje de usuarios de Metro esperaríamos en cada grupo bajo independencia? Guarda 25, 50 o 75 en `porcentaje_esperado_metro`.",
        "objective": "Comprender el concepto de independencia estadística y distinguir frecuencias observadas de esperadas.",
    },
    "intro-r-12-004": {
        "context": "La **prueba de chi-cuadrado ($\\chi^2$) de independencia** evalúa si las discrepancias entre observados y esperados son mayores a las atribuibles al azar:\n\n`prueba <- chisq.test(tabla)`\n\n$H_0$: las variables son independientes en la población.",
        "instruction": "Ejecuta `chisq.test(tabla)`, guárdalo en `prueba` y revisa el estadístico $\\chi^2$ y su p-value.",
        "objective": "Ejecutar la prueba de chi-cuadrado de independencia con `chisq.test()` e interpretar $H_0$ y p-value.",
    },
    "intro-r-12-005": {
        "context": "Para que la aproximación de chi-cuadrado sea confiable, las frecuencias esperadas no deben ser demasiado pequeñas (habitualmente $E \\ge 5$). Podemos consultarlas con `prueba$expected`.",
        "instruction": "Consulta las frecuencias esperadas calculadas por la prueba ejecutando `prueba$expected`.",
        "objective": "Inspeccionar las frecuencias esperadas de una prueba chi-cuadrado con `$expected` para validar sus supuestos.",
    },
    "intro-r-12-006": {
        "context": "Un p-value pequeño indica evidencia contra la independencia, pero no mide qué tan fuerte es la asociación. El coeficiente **V de Cramér** mide la **magnitud** estandarizada de la relación categórica (de 0 a 1), independiente del tamaño muestral.",
        "instruction": "Compara ambas tablas con prueba significativa. Guarda en `tabla_asociacion_mas_fuerte` cuál de las dos (`\"Tabla 1\"` o `\"Tabla 2\"`) muestra una asociación sustantivamente más concentrada.",
        "objective": "Distinguir entre significación estadística y magnitud sustantiva de una asociación.",
    },
    "intro-r-12-007": {
        "context": "En `encuesta_comunidad` queremos estudiar si la actividad comunitaria se distribuye de manera diferente según la zona de residencia.",
        "instruction": "1. Construye la tabla cruzada entre `zona_residencia` y `actividad_comunitaria` y guárdala en `tabla_comunidad`.\n2. Evalúa la independencia entre ambas variables con `chisq.test()` y guarda el resultado en `prueba_comunidad`.",
        "objective": "Analizar autónomamente la asociación entre dos variables categóricas: tabla, porcentajes y chi-cuadrado.",
    },
    # =========================================================================
    # MÓDULO 13
    # =========================================================================
    "intro-r-13-001": {
        "context": "Para abordar una investigación social debemos identificar el tipo de variables y la técnica adecuada:\n\n- **Cuantitativo**: variables numéricas continuas o discretas (medias, correlaciones).\n- **Categórico**: grupos o clasificaciones (tablas cruzadas, chi-cuadrado).",
        "instruction": "Clasifica el Problema 1 (horas y autoeficacia) y el Problema 2 (transporte y participación) guardando `\"cuantitativo\"` o `\"categorico\"` en `problema_1` y `problema_2`.",
        "objective": "Seleccionar la técnica estadística adecuada a partir de la pregunta y el tipo de variables involucradas.",
    },
    "intro-r-13-002": {
        "context": "En `encuesta_vida_universitaria` analizaremos a los estudiantes de jornada diurna.",
        "instruction": "Filtra los casos de jornada diurna (`jornada == \"Diurna\"`) en `encuesta_vida_universitaria`, selecciona las variables `horas_estudio` y `autoeficacia_academica`, y guarda el resultado en `datos_estudio_diurno`.",
        "objective": "Preparar una submuestra reproducible filtrando casos, seleccionando variables y diagnosticando ausencias.",
    },
    "intro-r-13-003": {
        "context": "Entre estudiantes de jornada diurna queremos evaluar si las horas semanales de estudio se relacionan con la autoeficacia académica.",
        "instruction": "Genera el scatterplot entre `horas_estudio` y `autoeficacia_academica`, ejecuta `cor.test()` de Pearson e interpreta magnitud, evidencia e incertidumbre.",
        "objective": "Conducir e interpretar un análisis bivariado cuantitativo completo: visualización, inferencia y alcance.",
    },
    "intro-r-13-004": {
        "context": "En `encuesta_vida_universitaria` analizamos la relación entre el medio de transporte al campus y la participación en organizaciones estudiantiles.",
        "instruction": "1. Construye la tabla cruzada entre `transporte_campus` y `participa_organizacion` y guárdala en `tabla_participacion`.\n2. Obtén los porcentajes por fila con `prop.table()` usando el argumento de margen 1.\n3. Evalúa la independencia estadística con `chisq.test()` y guarda el resultado en `prueba_participacion`.",
        "objective": "Conducir e interpretar un análisis bivariado categórico completo: tabla, porcentajes condicionales y chi-cuadrado.",
    },
    "intro-r-13-005": {
        "context": "**Checkpoint E — Integración final**\n\nEn `encuesta_vinculos_barriales` investigamos si participar en una organización vecinal se asocia con la confianza comunitaria entre quienes trabajan.",
        "instruction": "1. Prepara `datos_checkpoint` filtrando a quienes están ocupados (`ocupado == \"Sí\"`) y seleccionando `participa_vecinal_01` y `confianza_comunitaria`.\n2. Evalúa la correlación entre ambas variables con `cor.test()`.",
        "objective": "Diseñar y ejecutar de forma autónoma una ruta analítica completa en un contexto nuevo.",
    },
}
