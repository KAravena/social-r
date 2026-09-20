"""Social R - Canonical High-Density Student Microcopy (All 88 Exercises)

Audited, concise microcopy designed to maximize pedagogical density,
guarantee strict autocontention with compact markdown microtables,
and foster active student production without giving away code answers.
"""
from __future__ import annotations

STUDENT_MICROCOPY: dict[str, dict[str, str]] = {
    "intro-r-01-001": {
        "context": "Dos grupos respondieron una encuesta: uno aportó 18 respuestas y otro 12. R evalúa instrucciones y muestra el resultado en la consola.",
        "instruction": "Coloca el cursor en la línea con `18 + 12`, presiona **Ctrl + Enter** y observa el resultado `30` en la **Consola R**.",
        "objective": "Ejecutar una instrucción con Ctrl + Enter y localizar el resultado en la consola."
    },
    "intro-r-01-002": {
        "context": "El segundo grupo actualizó su conteo a **15** respuestas. Al modificar una instrucción y reejecutarla, R recalcula el resultado.",
        "instruction": "Cambia el segundo valor a `15` en la suma y ejecuta para obtener el total actualizado.",
        "objective": "Modificar un valor en una instrucción existente y reejecutar para actualizar el resultado."
    },
    "intro-r-01-003": {
        "context": "Para conservar un valor y reutilizarlo, lo guardamos en un **objeto** con `<-`:\n\n`respuestas <- 33`\n\nLa asignación guarda el valor sin imprimirlo. Para consultar su contenido, escribe el nombre del objeto: `respuestas`.",
        "instruction": "1. Ejecuta la asignación para guardar el valor en el objeto `respuestas`.\n2. Ejecuta la consulta de `respuestas` para comprobar su contenido en la consola.",
        "objective": "Guardar un valor en un objeto con `<-` y consultar su contenido por su nombre."
    },
    "intro-r-01-004": {
        "context": "La encuesta recibió 18 respuestas de Sociología y 15 de Antropología. El primer objeto ya está creado:\n\n`respuestas_sociologia <- 18`",
        "instruction": "Crea el objeto `respuestas_antropologia` para guardar las 15 respuestas. Luego consulta ambos objetos para comprobar sus valores.",
        "objective": "Crear un objeto con `<-` y consultar múltiples objetos."
    },
    "intro-r-01-005": {
        "context": "Los objetos guardados pueden reutilizarse en nuevas operaciones y almacenarse en otro objeto para continuar el análisis.",
        "instruction": "Crea `total_respuestas` sumando `respuestas_sociologia` y `respuestas_antropologia`. Luego consúltalo.",
        "objective": "Operar con objetos existentes y almacenar el resultado en un nuevo objeto."
    },
    "intro-r-01-006": {
        "context": "Los objetos guardan distintos tipos de información:\n\n- **Números**: van sin comillas (`20`).\n- **Texto**: va entre comillas (`\"Historia\"`).",
        "instruction": "Asigna `21` a `edad` y `\"Sociología\"` a `carrera`. Luego consulta ambos objetos.",
        "objective": "Distinguir números de texto respetando el uso de comillas."
    },
    "intro-r-01-007": {
        "context": "Los errores en R son mensajes informativos, no fallas permanentes. Aquí intentamos sumar un número con un texto:\n\n`18 + \"15\"`\n\nR no puede operar matemáticamente con texto entre comillas.",
        "instruction": "Corrige `respuestas_antropologia` quitando las comillas para guardarlo como número. Luego ejecuta la suma para calcular `total_respuestas`.",
        "objective": "Identificar y corregir un error de tipo numérico almacenado como texto."
    },
    "intro-r-01-008": {
        "context": "Una encuesta piloto llamada **“Encuesta de vida universitaria”** recibió 14 respuestas de Sociología y 11 de Antropología.",
        "instruction": "Construye un script autónomo que:\n1. Guarde el nombre del estudio en `estudio`.\n2. Guarde los conteos en `respuestas_sociologia` (14) y `respuestas_antropologia` (11).\n3. Sume ambos objetos en `total_respuestas` y consúltalo.",
        "objective": "Integrar texto, números y reutilización de objetos en un script completo."
    },
    "intro-r-02-001": {
        "context": "Para guardar varios valores juntos en un solo objeto usamos un **vector** mediante `c()`:\n\n`tiempos_viaje <- c(25, 40, 35, 50, 30)`\n\n`c()` combina los valores conservando su orden (1°: 25, 2°: 40, 3°: 35, etc.).",
        "instruction": "Ejecuta la asignación de `tiempos_viaje` y consúltalo para observar los cinco valores ordenados dentro del vector.",
        "objective": "Crear un vector con `c()` y comprender que almacena múltiples valores ordenados."
    },
    "intro-r-02-002": {
        "context": "Cinco personas informaron estos tiempos de viaje en minutos: **20, 35, 45, 25 y 30**, en ese orden.",
        "instruction": "Reúne los cinco tiempos en un solo vector usando `c()`, guárdalo en `tiempos_viaje` y consúltalo.",
        "objective": "Construir un vector numérico con valores en un orden determinado."
    },
    "intro-r-02-003": {
        "context": "Las funciones en R reciben datos entre paréntesis y devuelven un resultado:\n\n`sum(respuestas_diarias)`\n\n`sum()` recibe un vector completo y suma todos sus elementos.\n\nDatos de la semana: `respuestas_diarias <- c(18, 22, 15, 25, 20)`.",
        "instruction": "Aplica la función `sum()` sobre `respuestas_diarias` para calcular el total acumulado y guárdalo en `total_respuestas`.",
        "objective": "Aplicar una función como `sum()` a un vector completo y guardar el resultado."
    },
    "intro-r-02-004": {
        "context": "Para recuperar un valor según su posición usamos corchetes `[]`. En R las posiciones comienzan en 1:\n\n`tiempos_viaje[3]` recupera el tercer valor (`35`), no el número 3.\n\nVector observado: `tiempos_viaje <- c(25, 40, 35, 50, 30)`.",
        "instruction": "Usa corchetes de posición para extraer el tercer valor de `tiempos_viaje`.",
        "objective": "Recuperar un valor individual de un vector usando corchetes de posición `[]`."
    },
    "intro-r-02-005": {
        "context": "Para recuperar varias posiciones pasamos un vector dentro de los corchetes:\n\n`tiempos_viaje[c(2, 5)]`\n\nExtrae los valores de las posiciones 2 y 5 (`40` y `30`).",
        "instruction": "Usa corchetes y `c()` para seleccionar simultáneamente los tiempos de las posiciones 2 y 5 en `tiempos_viaje`.",
        "objective": "Seleccionar múltiples posiciones de un vector combinando `[]` y `c()`."
    },
    "intro-r-02-006": {
        "context": "Cinco estudiantes informaron que estudiaron **2, 4, 3, 5 y 1** horas, en ese orden.",
        "instruction": "1. Guarda los cinco valores juntos en `horas_estudio`.\n2. Calcula la suma de todos los valores y guárdala en `total`.\n3. Recupera la cuarta observación y guárdala en `cuarta`.",
        "objective": "Integrar creación, suma y selección por posición de un vector."
    },
    "intro-r-02-007": {
        "context": "Durante cinco semanas se registraron estas participaciones: **3, 1, 4, 2 y 5**, en ese orden.",
        "instruction": "1. Guarda los cinco valores en `participacion`.\n2. Calcula el total acumulado usando `sum()` y guárdalo en `total`.\n3. Extrae las semanas 2 y 5 usando corchetes y guárdalas en `seleccion`.",
        "objective": "Resolver agregación y selección sobre un vector con autonomía."
    },
    "intro-r-03-001": {
        "context": "Hasta ahora buscabas valores por su posición. Con R también podemos formular **preguntas de comparación** sobre los datos:\n\n`35 > 30` → `TRUE`\n`25 > 30` → `FALSE`\n\n`>` se lee **“es mayor que”**.\n\n`TRUE` indica que la afirmación se cumple; `FALSE`, que no se cumple. Ambos son **valores lógicos** producidos por R al evaluar la pregunta.",
        "instruction": "Ejecuta las dos comparaciones en el editor y comprueba cómo responde R con `TRUE` y `FALSE` en la consola.",
        "objective": "Interpretar comparaciones con `>`, `TRUE` y `FALSE`."
    },
    "intro-r-03-002": {
        "context": "Al comparar un vector con un valor, R evalúa la condición elemento por elemento en el mismo orden:\n\n`tiempos_viaje > 30`\n\nVector: `c(25, 40, 35, 50, 30)`.",
        "instruction": "Pregunta cuáles tiempos en `tiempos_viaje` superan los 30 minutos usando el operador `>`.",
        "objective": "Evaluar una condición lógica sobre un vector completo produciendo un vector de TRUE/FALSE."
    },
    "intro-r-03-003": {
        "context": "El resultado de una comparación es un vector lógico que podemos guardar en un objeto para reutilizarlo:\n\n`supera_30 <- tiempos_viaje > 30`\n\nGuarda la respuesta lógica (`TRUE`/`FALSE`) de cada posición.",
        "instruction": "Evalúa qué tiempos son mayores a 30, guarda el vector lógico resultante en `supera_30` y consúltalo.",
        "objective": "Guardar el resultado de una comparación lógica en un objeto para reutilizarlo."
    },
    "intro-r-03-004": {
        "context": "Cuando pasamos un vector de `TRUE` y `FALSE` dentro de los corchetes `[]`, R conserva las posiciones donde hay `TRUE` y descarta las posiciones donde hay `FALSE`:\n\n`tiempos_viaje[supera_30]`",
        "instruction": "Usa el vector lógico `supera_30` dentro de los corchetes para seleccionar los tiempos mayores a 30 en `tiempos_viaje`.",
        "objective": "Filtrar elementos de un vector utilizando un vector lógico dentro de corchetes `[]`."
    },
    "intro-r-03-005": {
        "context": "Podemos escribir la condición directamente dentro de los corchetes en un solo paso:\n\n`vector[vector > valor]`\n\nVector observado: `horas_estudio <- c(2, 5, 3, 6, 4)`.",
        "instruction": "Filtra en un solo paso las observaciones de `horas_estudio` que sean mayores a 4 usando corchetes.",
        "objective": "Filtrar un vector combinando corchetes y una condición lógica en un solo paso."
    },
    "intro-r-03-006": {
        "context": "Para comparar texto usamos el operador de igualdad exacta `==` (doble signo igual):\n\n`carreras == \"Sociología\"`\n\nVector: `carreras <- c(\"Sociología\", \"Historia\", \"Sociología\", \"Antropología\")`.\n\n`==` evalúa igualdad; `=` se reserva para argumentos.",
        "instruction": "1. Evalúa qué elementos de `carreras` son iguales a `\"Sociología\"` y guarda la respuesta en `es_sociologia`.\n2. Usa `es_sociologia` dentro de corchetes para seleccionar únicamente esas carreras de `carreras`.",
        "objective": "Comparar texto con `==` y seleccionar elementos de un vector categórico."
    },
    "intro-r-03-007": {
        "context": "Se registraron las sesiones de estudio de cinco estudiantes: **6, 12, 8, 15 y 10** sesiones.",
        "instruction": "1. Guarda las cinco sesiones en un vector llamado `sesiones`.\n2. Crea el vector lógico `mas_de_ocho` preguntando qué sesiones superan 8.\n3. Usa `mas_de_ocho` para seleccionar las sesiones correspondientes y guárdalas en `seleccionadas`.",
        "objective": "Integrar formulación de preguntas lógicas y selección condicional con autonomía."
    },
    "intro-r-04-001": {
        "context": "Una fila reúne la información de una persona. Una columna reúne los valores de una misma característica (por ejemplo, la edad).\n\nEn análisis de datos, solemos llamar **caso** a cada fila y **variable** a cada columna.\n\nEn R, una tabla que organiza casos y variables se llama **data frame**:\n\n| persona | edad | horas_estudio | carrera |\n|:---|---:|---:|:---|\n| Persona 1 | 20 | 3 | Sociología |\n| Persona 2 | 22 | 5 | Historia |\n| Persona 3 | 19 | 2 | Antropología |\n| Persona 4 | 21 | 4 | Sociología |",
        "instruction": "Observa la tabla en el panel izquierdo y guarda en `edad_persona_2` la edad de la persona que estudia 5 horas (Persona 2).",
        "objective": "Reconocer qué información muestra una fila y qué información muestra una columna en un data frame."
    },
    "intro-r-04-002": {
        "context": "Al leer una base de datos:\n\n- Una **fila** recorre un mismo caso (una persona) y muestra todas sus características.\n- Una **columna** recorre una misma variable para todos los casos, funcionando como un vector.\n\nAquí tienes la encuesta de cuatro personas:\n\n| persona | edad | horas_estudio | carrera |\n|:---|---:|---:|:---|\n| Persona 1 | 20 | 3 | Sociología |\n| Persona 2 | 22 | 5 | Historia |\n| Persona 3 | 19 | 2 | Antropología |\n| Persona 4 | 21 | 4 | Sociología |",
        "instruction": "Mirando la tabla en el panel izquierdo:\n\n1. Guarda las cuatro edades en `edades_encuesta` como un vector.\n2. Guarda las cuatro horas de estudio en `horas_encuesta` como un vector.",
        "objective": "Distinguir la lectura por filas (casos) de la lectura por columnas (variables) y extraer vectores."
    },
    "intro-r-04-003": {
        "context": "Una base de datos real puede contener miles de filas. Para obtener un vistazo inicial sin imprimirla completa usamos `head()`:\n\n`head(encuesta_social_demo)`\n\nPor defecto, `head()` muestra las primeras 6 filas de la base.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| ... | ... | ... | ... | ... |",
        "instruction": "1. Ejecuta `head(encuesta_social_demo)` para ver las primeras filas en la consola.\n2. Cuenta cuántas filas muestra por defecto y guarda ese número en `filas_visibles`.",
        "objective": "Explorar las primeras filas de una base con `head()` y observar su resultado."
    },
    "intro-r-04-004": {
        "context": "Para pedirle a R una columna completa de la base usamos el operador `$`: `base$variable`.\n\nPor ejemplo:\n\n`encuesta_social_demo$edad`\n\nrecupera todas las edades como un vector.\n\nEsta es una muestra de las primeras filas de `encuesta_social_demo`:\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| ... | ... | ... | ... | ... |",
        "instruction": "Siguiendo el ejemplo anterior:\n\n1. Extrae la variable `horas_estudio` de `encuesta_social_demo`.\n2. Extrae la variable `carrera` de `encuesta_social_demo`.",
        "objective": "Extraer variables de un data frame usando el operador `$` y reconocer que retornan como vectores."
    },
    "intro-r-04-005": {
        "context": "`str()` da una radiografía rápida de una base: cantidad de filas, columnas, nombres y tipo de almacenamiento técnico (`num`, `chr`, etc.):\n\n`str(encuesta_social_demo)`\n\nNo necesitas memorizar los códigos técnicos. Lo fundamental es que `str()` te ayuda a conocer qué variables existen en la base antes de analizarlas.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| ... | ... | ... | ... | ... |",
        "instruction": "1. Ejecuta `str(encuesta_social_demo)` para ver sus variables en la consola.\n2. Conociendo el nombre de la variable de empleo (`trabaja`), extráela con `$` y guárdala en `situacion_laboral`.",
        "objective": "Inspeccionar la estructura de una base con `str()` y recuperar una columna observada con `$`."
    },
    "intro-r-04-006": {
        "context": "Dispones de una base sobre movilidad llamada `encuesta_barrio`:\n\n| persona | edad | transporte | minutos_viaje |\n|:---|---:|:---|---:|\n| 1 | 34 | Bus | 45 |\n| 2 | 27 | Metro | 30 |\n| 3 | 41 | Bus | 50 |\n| 4 | 22 | Bicicleta | 20 |",
        "instruction": "Usando lo aprendido en el módulo:\n\n1. Extrae la variable `minutos_viaje` de `encuesta_barrio` y guárdala en `tiempos`.\n2. Extrae la variable `transporte` de `encuesta_barrio` y guárdala en `medios`.",
        "objective": "Transferir de forma autónoma la lectura e identificación de variables y extracción con `$` a una nueva base."
    },
    "intro-r-05-001": {
        "context": "En el Módulo 3 hicimos preguntas a vectores. En el Módulo 4 aprendimos que una columna de una base se extrae como un vector con `$`. Ahora juntamos ambas ideas para formular preguntas sobre una base.\n\nBase disponible `encuesta_social_demo`:\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Formula una pregunta lógica con el operador `$` y `>` para saber qué edades en `encuesta_social_demo` son mayores a 21.",
        "objective": "Formular una condición lógica sobre una columna de un data frame con `$`."
    },
    "intro-r-05-002": {
        "context": "Al evaluar una condición en una tabla, cada respuesta `TRUE` puede conservar la fila completa con todas sus variables:\n\n`mayores_21 <- encuesta_social_demo$edad > 21`\n`encuesta_social_demo[mayores_21, ]`\n\nLa coma `,` después de la condición indica a R que conserve todas las columnas de esas personas.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "1. Guarda en `mayores_21` la condición que identifica a quienes tienen más de 21 años.\n2. Indexa las filas de la tabla con `encuesta_social_demo[mayores_21, ]` para observar las personas completas conservadas.",
        "objective": "Comprender cómo una condición lógica conserva casos completos en una base."
    },
    "intro-r-05-003": {
        "context": "La función `filter()` del paquete `dplyr` simplifica el filtrado de casos:\n\n`filter(base, condicion)`\n\nDentro de `filter()` escribimos directamente el nombre de la variable sin repetir `base$`.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Usa `filter()` sobre `encuesta_social_demo` para conservar únicamente a las personas que dedican más de 3 horas de estudio.",
        "objective": "Filtrar casos de un data frame usando `filter()` y condiciones directas."
    },
    "intro-r-05-004": {
        "context": "Para filtrar por una categoría de texto usamos `==` con el valor exacto entre comillas:\n\n`filter(base, variable == \"Categoría\")`\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Aplica `filter()` para conservar únicamente a las personas cuya carrera sea `\"Sociología\"`.",
        "objective": "Filtrar casos evaluando una condición de igualdad de texto con `==`."
    },
    "intro-r-05-005": {
        "context": "El operador pipe `|>` pasa los datos de una etapa a la siguiente:\n\n`base |> filter(condicion)`\n\nPermite leer las transformaciones de izquierda a derecha sin modificar la base original guardada en memoria.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Encadena `encuesta_social_demo` con el pipe `|>` hacia `filter()` para conservar a quienes trabajan (`trabaja == \"Sí\"`).",
        "objective": "Encadenar una transformación con el pipe `|>` preservando la base original."
    },
    "intro-r-05-006": {
        "context": "Mientras `filter()` elige **casos (filas)**, `select()` elige **variables (columnas)** por su nombre:\n\n- `filter(edad > 20)` → conserva filas\n- `select(edad, carrera)` → conserva columnas\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Usa `select()` sobre `encuesta_social_demo` para conservar únicamente las variables `edad` y `carrera`.",
        "objective": "Seleccionar variables de un data frame por su nombre usando `select()`."
    },
    "intro-r-05-007": {
        "context": "El pipe permite encadenar múltiples decisiones en un flujo de lectura continuo:\n\n```r\nbase |>\n  filter(condicion) |>\n  select(var1, var2)\n```\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---|\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Construye un pipeline con `|>` que primero filtre a las personas que trabajan (`trabaja == \"Sí\"`) y luego seleccione las variables `edad` y `carrera`.",
        "objective": "Combinar `filter()` y `select()` en un pipeline encadenado con `|>`."
    },
    "intro-r-05-008": {
        "context": "**Checkpoint B — Bases y preparación**\n\nPara una investigación social necesitamos trabajar con las personas que estudian en `encuesta_jovenes`. De ellas necesitamos su edad y comuna:\n\n| id | edad | estudia | comuna | transporte |\n|:---|---:|:---|:---|:---||\n| 1 | 18 | Sí | Norte | Bus |\n| 2 | 20 | No | Centro | Metro |\n| 3 | 19 | Sí | Sur | Bicicleta |\n| 4 | 22 | Sí | Centro | Bus |\n| 5 | 21 | No | Norte | Metro |\n| 6 | 23 | Sí | Sur | Metro |\n| 7 | 19 | No | Norte | Bus |\n| 8 | 24 | Sí | Centro | Bicicleta |",
        "instruction": "Construye un flujo con `|>` que filtre a quienes estudian, seleccione las variables `edad` y `comuna`, y guarde el resultado en `datos_preparados`.",
        "objective": "Preparar un subconjunto de datos combinando `filter()` y `select()` de forma autónoma."
    },
    "intro-r-06-001": {
        "context": "En encuestas sociales es común que algunas personas no respondan. En R, la ausencia de información se representa con `NA` (sin comillas):\n\n- `0`: es un valor observado (reportó cero horas).\n- `NA`: el dato no está disponible (desconocido).\n\nVector disponible: `horas_cuidado <- c(6, 0, NA, 8, 4)`.",
        "instruction": "Ejecuta `horas_cuidado` y observa en la consola la diferencia entre el valor observado `0` y el dato ausente `NA`.",
        "objective": "Identificar `NA` como ausencia de dato y distinguirlo del valor numérico `0`."
    },
    "intro-r-06-002": {
        "context": "Para detectar datos ausentes usamos `is.na()`. Devuelve `TRUE` donde falta información y `FALSE` donde hay un valor disponible:\n\n`is.na(c(6, 0, NA))` → `FALSE, FALSE, TRUE`\n\nVector: `horas_cuidado <- c(6, 0, NA, 8, 4)`.",
        "instruction": "Aplica `is.na()` sobre `horas_cuidado` para identificar qué posiciones contienen datos ausentes.",
        "objective": "Detectar valores ausentes en un vector mediante la función lógica `is.na()`."
    },
    "intro-r-06-003": {
        "context": "En operaciones aritméticas, R trata a `TRUE` como 1 y a `FALSE` como 0. Por eso podemos contar cuántos datos faltan sumando los valores lógicos:\n\n`sum(is.na(vector))`\n\nVector: `horas_cuidado <- c(6, 0, NA, 8, 4)`.",
        "instruction": "Cuenta cuántos valores ausentes hay en `horas_cuidado` combinando `sum()` e `is.na()`.",
        "objective": "Contar la cantidad de valores ausentes combinando `sum()` e `is.na()`."
    },
    "intro-r-06-004": {
        "context": "Si un vector contiene `NA`, `sum()` o `mean()` devuelven `NA` porque el total exacto se desconoce. Para operar con los valores efectivamente disponibles agregamos `na.rm = TRUE`:\n\n`mean(vector, na.rm = TRUE)`\n\nVector: `horas_cuidado <- c(6, 0, NA, 8, 4)`.",
        "instruction": "Calcula el promedio de las horas de cuidado disponibles aplicando `mean()` con el argumento `na.rm = TRUE`.",
        "objective": "Calcular estadísticas sobre datos disponibles usando el argumento `na.rm = TRUE`."
    },
    "intro-r-06-005": {
        "context": "Disponemos de `encuesta_social_demo` con horas de cuidado:\n\n| id | edad | carrera | horas_estudio | trabaja | horas_cuidado |\n|:---|---:|:---|---:|:---|:---|\n| 1 | 20 | Sociología | 3 | No | 6 |\n| 2 | 22 | Historia | 5 | Sí | NA |\n| 3 | 19 | Antropología | 2 | No | 0 |\n| 4 | 21 | Sociología | 4 | No | 8 |\n| 5 | 24 | Trabajo Social | 6 | Sí | 4 |\n| 6 | 23 | Antropología | 3 | Sí | 5 |\n| 7 | 20 | Historia | 5 | No | NA |\n| 8 | 25 | Sociología | 2 | Sí | 7 |",
        "instruction": "1. Prepara `datos_trabajan` filtrando a quienes trabajan (`trabaja == \"Sí\"`) y seleccionando `id` y `horas_cuidado`.\n2. Cuenta cuántos valores ausentes hay en `horas_cuidado` de ese subgrupo usando `sum(is.na())`.",
        "objective": "Preparar datos y diagnosticar valores ausentes en el grupo obtenido."
    },
    "intro-r-06-006": {
        "context": "En `encuesta_barrio` registramos los minutos de traslado de seis residentes:\n\n| id | minutos_viaje | transporte |\n|:---|---:|:---|\n| 1 | 35 | Bus |\n| 2 | NA | Metro |\n| 3 | 50 | Bus |\n| 4 | 20 | Bicicleta |\n| 5 | NA | Metro |\n| 6 | 40 | Bus |",
        "instruction": "1. Cuenta cuántos datos faltan en `minutos_viaje` usando `sum(is.na())`.\n2. Calcula el tiempo total de viaje de los casos disponibles usando `sum()` con `na.rm = TRUE`.",
        "objective": "Diagnosticar valores ausentes y calcular estadísticas con datos disponibles de forma autónoma."
    },
    "intro-r-07-001": {
        "context": "Para elegir el análisis correcto debemos distinguir dos tipos de información:\n\n- **Categoría**: nombres, grupos o etiquetas (ej. carrera, zona).\n- **Cantidad**: mediciones numéricas donde tiene sentido sumar o promediar (ej. horas, edad).",
        "instruction": "Clasifica cada variable asignando `\"categoria\"` o `\"cantidad\"` a `tipo_carrera`, `tipo_horas` y `tipo_zona_codigo`.",
        "objective": "Diferenciar variables categóricas de cuantitativas por su significado sustantivo."
    },
    "intro-r-07-002": {
        "context": "Para resumir una variable categórica contamos cuántos casos hay en cada grupo mediante una tabla de frecuencias:\n\n`table(base$variable)`\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---||\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Construye la tabla de frecuencias de la variable `carrera` en `encuesta_social_demo` y guárdala en `tabla_carrera`.",
        "objective": "Construir e interpretar una tabla de frecuencias con `table()`."
    },
    "intro-r-07-003": {
        "context": "Para saber qué fracción del total representa cada categoría convertimos la tabla en **proporciones** con `prop.table()`:\n\n`prop.table(tabla)`\n\nCada valor va de 0 a 1 y todas las celdas suman 1.0.",
        "instruction": "Aplica `prop.table()` a `tabla_carrera` para calcular la proporción de estudiantes en cada disciplina.",
        "objective": "Calcular proporciones a partir de una tabla de frecuencias con `prop.table()`."
    },
    "intro-r-07-004": {
        "context": "Para facilitar la comunicación social, multiplicamos las proporciones por 100 y obtenemos porcentajes directos:\n\n`prop.table(tabla) * 100`",
        "instruction": "1. Guarda en `tabla_carrera` el conteo de frecuencias de `carrera`.\n2. Calcula los porcentajes multiplicando las proporciones por 100.",
        "objective": "Calcular frecuencias y proporciones sobre una variable categórica."
    },
    "intro-r-07-005": {
        "context": "Un **gráfico de barras** muestra visualmente la distribución de una variable categórica:\n\n`barplot(tabla)`\n\nCada barra representa una categoría y su altura refleja la frecuencia observada.",
        "instruction": "Genera el gráfico de barras de `tabla_carrera` usando la función `barplot()`.",
        "objective": "Visualizar la distribución de frecuencias de una variable categórica con `barplot()`."
    },
    "intro-r-07-006": {
        "context": "En `encuesta_campus` consultamos la satisfacción de ocho estudiantes:\n\n| id | transporte | carrera | satisfaccion |\n|:---|:---|:---|:---|\n| 1 | Metro | Sociología | Alta |\n| 2 | Bus | Historia | Media |\n| 3 | Bicicleta | Antropología | Alta |\n| 4 | Metro | Sociología | Baja |\n| 5 | A pie | Trabajo Social | Media |\n| 6 | Bus | Antropología | Alta |\n| 7 | Metro | Historia | Media |\n| 8 | Bicicleta | Sociología | Alta |",
        "instruction": "1. Construye la tabla de frecuencias de `satisfaccion` y guárdala en `tabla_satisfaccion`.\n2. Calcula sus proporciones con `prop.table()` y genera su gráfico con `barplot()`.",
        "objective": "Describir una variable categórica nueva combinando tabla, proporciones y gráfico de barras."
    },
    "intro-r-08-001": {
        "context": "Para explorar una variable cuantitativa observamos cómo se reparten sus valores mediante un **histograma**:\n\n`hist(base$variable)`\n\nEl eje horizontal muestra intervalos continuos y la altura de cada barra refleja cuántos casos caen en ese rango.\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---||\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Genera un histograma de la variable `horas_estudio` en `encuesta_social_demo` usando `hist()`.",
        "objective": "Visualizar la distribución de una variable cuantitativa con un histograma mediante `hist()`."
    },
    "intro-r-08-002": {
        "context": "La **media** resume el centro repartiendo la suma total de valores por igual entre todos los casos:\n\n`mean(base$variable)`\n\nSe expresa en la misma unidad de medida (horas de estudio).\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---||\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Calcula la media de `horas_estudio` en `encuesta_social_demo` usando la función `mean()`.",
        "objective": "Calcular e interpretar la media aritmética de una variable con `mean()`."
    },
    "intro-r-08-003": {
        "context": "La **mediana** es el valor que ocupa la posición central una vez ordenados los datos de menor a mayor:\n\n`median(vector)`\n\nDeja exactamente el 50% de las observaciones por debajo y el 50% por encima.\n\nTiempos registrados: `minutos_lectura <- c(15, 20, 25, 30, 45, 60, 120)`.",
        "instruction": "Calcula la mediana de `minutos_lectura` usando la función `median()`.",
        "objective": "Calcular e interpretar la mediana como medida de centro basada en el orden con `median()`."
    },
    "intro-r-08-004": {
        "context": "Compara dos grupos donde solo cambia un valor extremo:\n\n- `viaje_regular`: 20, 22, 24, 25, 26, 28, **30**\n- `viaje_con_accidente`: 20, 22, 24, 25, 26, 28, **120**\n\nLa media es sensible a valores extremos, mientras que la mediana es resistente (robusta).",
        "instruction": "Calcula la media y la mediana de `viaje_con_accidente` y observa cómo la media se distorsiona mientras la mediana permanece estable.",
        "objective": "Evaluar la sensibilidad de la media y la robustez de la mediana ante valores extremos."
    },
    "intro-r-08-005": {
        "context": "Dos grupos pueden tener la misma media pero comportarse muy diferente. La **desviación estándar** mide qué tan dispersos están los datos respecto a su media:\n\n`sd(vector)`\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---||\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "Observa la dispersión en los grupos de prueba y calcula la desviación estándar de `horas_estudio` en `encuesta_social_demo` usando `sd()`.",
        "objective": "Calcular e interpretar la desviación estándar con `sd()` como medida de dispersión."
    },
    "intro-r-08-006": {
        "context": "En investigación preparamos los datos antes de describirlos. Queremos analizar a las personas que no trabajan (`trabaja == \"No\"`):\n\n| id | edad | carrera | horas_estudio | trabaja |\n|:---|---:|:---|---:|:---||\n| 1 | 20 | Sociología | 3 | No |\n| 2 | 22 | Historia | 5 | Sí |\n| 3 | 19 | Antropología | 2 | No |\n| 4 | 21 | Sociología | 4 | No |\n| 5 | 24 | Trabajo Social | 6 | Sí |\n| 6 | 23 | Antropología | 3 | Sí |\n| 7 | 20 | Historia | 5 | No |\n| 8 | 25 | Sociología | 2 | Sí |",
        "instruction": "1. Guarda en `datos_no_trabajan` el subgrupo filtrado de quienes no trabajan.\n2. Calcula la media y la desviación estándar de `horas_estudio` en ese subgrupo.",
        "objective": "Filtrar un subgrupo y calcular media y dispersión sobre los datos disponibles."
    },
    "intro-r-08-007": {
        "context": "**Checkpoint C — Describir una variable cuantitativa**\n\nDescribe la variable `minutos_viaje` de `encuesta_movilidad`. Nota que el caso 10 demoró 90 minutos por una contingencia:\n\n| id | transporte | minutos_viaje |\n|:---|:---|---:|\n| 1 | Metro | 25 |\n| 2 | Bus | 30 |\n| 3 | Metro | 32 |\n| 4 | Bus | 28 |\n| 5 | Bicicleta | 35 |\n| 6 | Metro | 27 |\n| 7 | Bus | 31 |\n| 8 | A pie | 29 |\n| 9 | Metro | 34 |\n| 10 | Bus | 90 |",
        "instruction": "Describe completamente `minutos_viaje` en `encuesta_movilidad`: calcula su media, su mediana y su desviación estándar.",
        "objective": "Analizar autónomamente una variable cuantitativa mediante centro y dispersión."
    },
    "intro-r-09-001": {
        "context": "Para analizar si dos cantidades se relacionan, debemos observar ambos valores en la *misma* persona.\n\nFila 3 de `encuesta_social`: 3 horas de estudio y puntaje 58 en métodos.",
        "instruction": "Guarda en `par_persona_3` el vector `c(x, y)` con las horas de estudio (3) y el puntaje (58) de la persona 3.",
        "objective": "Identificar un caso bivariado como un par de coordenadas (x, y)."
    },
    "intro-r-09-002": {
        "context": "En un **gráfico de dispersión (scatterplot)** cada persona se representa como un punto en el plano:\n\n`plot(base$variable_x, base$variable_y)`\n\nBase `encuesta_social` (12 casos):\n\n| id | horas_estudio | puntaje_metodos | horas_trabajo | trabaja |\n|:---|---:|---:|---:|:---|\n| 1 | 2 | 59 | 20 | Sí |\n| 2 | 4 | 68 | 35 | Sí |\n| 3 | 3 | 58 | 0 | No |\n| 4 | 6 | 64 | 25 | Sí |\n| 5 | 5 | 62 | 40 | Sí |\n| 6 | 8 | 75 | 0 | No |\n| ... | ... | ... | ... | ... |",
        "instruction": "Genera el gráfico de dispersión con `plot()` ubicando `horas_estudio` en el eje horizontal y `puntaje_metodos` en el eje vertical.",
        "objective": "Generar e interpretar un diagrama de dispersión bivariado con `plot(x, y)`."
    },
    "intro-r-09-003": {
        "context": "La dirección de una relación describe cómo varía una cantidad cuando la otra aumenta:\n\n- **Positiva**: a mayor X, mayor Y (asciende de izquierda a derecha).\n- **Negativa**: a mayor X, menor Y (desciende de izquierda a derecha).\n\n*Nota fundamental: Asociación empírica no demuestra causalidad.*",
        "instruction": "Observa los gráficos de referencia y clasifica la dirección asignando `\"positiva\"` o `\"negativa\"` a `direccion_a` y `direccion_b`.",
        "objective": "Identificar la dirección de una relación en un scatterplot distinguiéndola de causalidad."
    },
    "intro-r-09-004": {
        "context": "Dos relaciones pueden ir en la misma dirección pero exhibir diferente dispersión alrededor de una trayectoria.",
        "instruction": "Observa los gráficos A y B. Asigna `\"A\"` o `\"B\"` a `grafico_mas_concentrado` según cuál muestra los puntos más alineados.",
        "objective": "Evaluar forma, fuerza y presencia de valores atípicos en un diagrama de dispersión."
    },
    "intro-r-09-005": {
        "context": "El **coeficiente de correlación de Pearson ($r$)** resume la fuerza y dirección de una relación lineal en un número entre -1 y +1:\n\n`cor(base$x, base$y)`\n\nCercano a +1 indica fuerte relación positiva; cercano a 0, ausencia de relación lineal.\n\nBase `encuesta_social` disponible.",
        "instruction": "Calcula el coeficiente de correlación de Pearson entre `horas_estudio` y `puntaje_metodos` en `encuesta_social` usando `cor()`.",
        "objective": "Calcular e interpretar el coeficiente de correlación lineal de Pearson con `cor()`."
    },
    "intro-r-09-006": {
        "context": "Antes de correlacionar debemos aislar el grupo pertinente. Queremos estudiar horas de trabajo e ingreso únicamente entre quienes efectivamente trabajan (`trabaja == \"Sí\"`):\n\n| id | horas_trabajo | ingreso_miles | trabaja |\n|:---|---:|---:|:---|\n| 1 | 20 | 420 | Sí |\n| 2 | 35 | 650 | Sí |\n| 3 | 0 | 300 | No |\n| 4 | 25 | 380 | Sí |\n| 5 | 40 | 720 | Sí |\n| ... | ... | ... | ... |",
        "instruction": "1. Filtra a quienes trabajan (`trabaja == \"Sí\"`) y guarda el subgrupo en `datos_trabajan`.\n2. Calcula la correlación entre `horas_trabajo` e `ingreso_miles` en ese subgrupo.",
        "objective": "Manejar preparación de datos y calcular correlación sobre el grupo pertinente."
    },
    "intro-r-09-007": {
        "context": "En `encuesta_lectura` registramos los minutos dedicados a leer y el puntaje de comprensión de 10 participantes:\n\n| id | minutos_lectura | puntaje_comprension |\n|:---|---:|---:|\n| 1 | 15 | 50 |\n| 2 | 35 | 57 |\n| 3 | 25 | 66 |\n| 4 | 55 | 84 |\n| 5 | 20 | 59 |\n| 6 | 50 | 69 |\n| 7 | 30 | 68 |\n| 8 | 60 | 83 |\n| 9 | 40 | 55 |\n| 10 | 45 | 62 |",
        "instruction": "1. Genera el gráfico de dispersión con `plot()` entre minutos de lectura y puntaje de comprensión.\n2. Calcula el coeficiente de correlación lineal con `cor()`.",
        "objective": "Analizar autónomamente una relación bivariada combinando gráfico de dispersión y correlación de Pearson."
    },
    "intro-r-10-001": {
        "context": "No todas las relaciones siguen una línea recta. Si una relación es monótona curva, el orden o jerarquía de los casos se conserva perfectamente.\n\nEl coeficiente de **Spearman** evalúa rangos y orden en lugar de distancias métricas:\n\n`cor(x, y, method = \"spearman\")`\n\nVectores: `x_curva <- 1:8`, `y_curva <- c(2, 5, 11, 20, 36, 65, 118, 215)`.",
        "instruction": "Observa el cálculo de Pearson en el editor ($r \\approx 0.88$) y calcula la correlación de Spearman para comprobar que el orden se preserva al 100% ($r_s = 1.0$).",
        "objective": "Distinguir una relación lineal de una relación monótona no lineal y reconocer el uso de Spearman."
    },
    "intro-r-10-002": {
        "context": "Cuando una relación conserva el orden de los casos aunque sea curva, Spearman devuelve valores cercanos a 1 porque evalúa rangos:\n\n`cor(x, y, method = \"spearman\")`\n\nVectores disponibles `x_curva` e `y_curva`.",
        "instruction": "Calcula el coeficiente de Spearman entre `x_curva` e `y_curva` indicando el argumento `method = \"spearman\"`.",
        "objective": "Calcular e interpretar el coeficiente de correlación de Spearman basado en rangos."
    },
    "intro-r-10-003": {
        "context": "Criterio de elección según la trayectoria visual:\n\n- **Aproximadamente recta**: Pearson.\n- **Monótona curva**: Spearman.\n- **En forma de U o no monótona**: ninguno como resumen lineal único.",
        "instruction": "Observa los tres gráficos del panel y asigna `\"pearson\"`, `\"spearman\"` o `\"ninguno\"` a `metodo_a`, `metodo_b` y `metodo_c`.",
        "objective": "Elegir justificadamente entre Pearson y Spearman a partir de la forma observada en el scatterplot."
    },
    "intro-r-10-004": {
        "context": "Para evaluar si la correlación observada en una muestra aporta evidencia creíble sobre una relación en la población usamos `cor.test()`:\n\n`cor.test(x, y)`\n\nEntrega: estimación muestral (`estimate`), valor p (`p-value`) e intervalo de confianza (`conf.int`).\n\nBase `encuesta_social` disponible.",
        "instruction": "Aplica la prueba de correlación inferencial con `cor.test()` entre `horas_estudio` y `puntaje_metodos` en `encuesta_social`.",
        "objective": "Ejecutar una prueba de correlación con `cor.test()` e identificar sus componentes clave."
    },
    "intro-r-10-005": {
        "context": "En inferencia estadística:\n\n- **Hipótesis nula ($H_0$)**: no hay correlación en la población ($r = 0$).\n- **p-value**: mide qué tan compatibles son los datos observados con $H_0$. Un valor pequeño indica que los datos observados serían muy raros si no hubiera relación real.",
        "instruction": "Evalúa cada afirmación asignando `TRUE` o `FALSE` a `afirmacion_probabilidad_h0` e `afirmacion_incompatibilidad`.",
        "objective": "Comprender la hipótesis nula en correlación y el p-value como medida de compatibilidad con $H_0$."
    },
    "intro-r-10-006": {
        "context": "No confundas **magnitud** ($r$) con **evidencia** ($p$):\n\nDos muestras pueden tener la misma correlación ($r = 0.50$), pero con mayor tamaño muestral ($N$) el p-value es más pequeño y la estimación es más precisa.",
        "instruction": "Compara el Estudio A ($n = 10$) y el Estudio B ($n = 500$). Asigna `\"Estudio A\"` o `\"Estudio B\"` a `estudio_menor_p` y a `estudio_mayor_precision`.",
        "objective": "Diferenciar magnitud del efecto, significación inferencial y precisión según el tamaño muestral."
    },
    "intro-r-10-007": {
        "context": "En `encuesta_social` queremos analizar si la edad se asocia con las horas de estudio:\n\n| id | edad | horas_estudio | puntaje_metodos |\n|:---|---:|---:|---:|\n| 1 | 20 | 2 | 59 |\n| 2 | 22 | 4 | 68 |\n| 3 | 19 | 3 | 58 |\n| 4 | 21 | 6 | 64 |\n| 5 | 24 | 5 | 62 |\n| ... | ... | ... | ... |",
        "instruction": "1. Genera el gráfico de dispersión con `plot()` entre edad y horas de estudio.\n2. Ejecuta la prueba de correlación con `cor.test()` entre ambas variables.",
        "objective": "Conducir una evaluación correlacional completa: gráfico, elección de método y prueba de hipótesis."
    },
    "intro-r-10-008": {
        "context": "**Checkpoint D — Decidir y evaluar una correlación**\n\nEn `encuesta_emprendimiento` observamos que las ventas crecen de forma fuertemente acelerada según los años del negocio:\n\n| id | antiguedad_anos | ventas_mensuales |\n|:---|---:|---:|\n| 1 | 1 | 100 |\n| 2 | 2 | 110 |\n| 3 | 3 | 120 |\n| 4 | 4 | 140 |\n| 5 | 5 | 180 |\n| 6 | 6 | 300 |\n| 7 | 7 | 800 |\n| 8 | 8 | 3000 |",
        "instruction": "Evalúa la relación monótona entre `antiguedad_anos` y `ventas_mensuales` aplicando la prueba de correlación de Spearman (`method = \"spearman\"`) con `cor.test()`.",
        "objective": "Decidir el método de correlación pertinente y evaluar su evidencia inferencial de forma integrada."
    },
    "intro-r-11-001": {
        "context": "Para analizar relaciones entre múltiples cantidades numéricas, primero seleccionamos únicamente las columnas cuantitativas relevantes:\n\n| id | edad | horas_estudio | horas_ocio | trabaja_01 | ingreso_miles |\n|:---|---:|---:|---:|---:|---:|\n| 1 | 20 | 2 | 6.0 | 1 | 420 |\n| 2 | 22 | 4 | 5.2 | 1 | 650 |\n| 3 | 19 | 3 | 6.1 | 0 | 300 |\n| 4 | 21 | 6 | 5.0 | 1 | 380 |\n| 5 | 24 | 5 | 5.8 | 1 | 720 |\n| ... | ... | ... | ... | ... | ... |",
        "instruction": "Selecciona las variables `edad`, `horas_estudio` y `horas_ocio` desde `encuesta_social` usando `select()` y guarda el data frame en `analisis`.",
        "objective": "Seleccionar un conjunto de variables cuantitativas sustantivas para análisis multivariado."
    },
    "intro-r-11-002": {
        "context": "Al aplicar `cor()` a una tabla con varias columnas numéricas, R calcula una **matriz de correlaciones** donde cada celda muestra la correlación entre una fila y una columna:\n\n`cor(tabla, method = \"pearson\")`",
        "instruction": "Calcula la matriz de correlaciones de la base `analisis` que preparaste en el ejercicio anterior.",
        "objective": "Calcular e interpretar una matriz de correlaciones bivariadas con `cor()`."
    },
    "intro-r-11-003": {
        "context": "Propiedades de una matriz de correlaciones:\n\n- **Diagonal**: vale 1.0 porque cada variable se correlaciona consigo misma.\n- **Simetría de espejo**: la correlación entre A y B es idéntica a la de B y A.",
        "instruction": "En una matriz de 3 variables numéricas, ¿cuántos pares de correlación *únicos* e informativos existen (sin diagonal ni repeticiones)? Guarda ese número en `pares_unicos`.",
        "objective": "Interpretar la estructura de una matriz de correlaciones reconociendo simetría y pares únicos."
    },
    "intro-r-11-004": {
        "context": "Cuando hay datos ausentes en algunas variables de la matriz:\n\n- `complete.obs`: elimina cualquier fila que tenga un `NA` en alguna variable.\n- `pairwise.complete.obs`: calcula cada par de correlación usando todos los casos disponibles para ese par específico.\n\nBase `seguimiento` con mediciones incompletas:\n\n| id | horas_estudio | horas_sueno | estres |\n|:---|---:|---:|---:|\n| 1 | 2 | 8.1 | 3 |\n| 2 | 4 | 7.4 | 5 |\n| 3 | 3 | NA | 4 |\n| 4 | 6 | 7.8 | 6 |\n| 5 | 5 | 6.9 | NA |\n| ... | ... | ... | ... |",
        "instruction": "Calcula la matriz de correlaciones de `seguimiento` usando el argumento `use = \"pairwise.complete.obs\"`.",
        "objective": "Comparar la eliminación por lista frente a eliminación por pares en matrices de correlación."
    },
    "intro-r-11-005": {
        "context": "Una variable binaria (0 = No, 1 = Sí) puede correlacionarse con una cantidad métrica (**correlación punto-biserial**). El signo indica qué grupo tiene promedios más altos según la categoría codificada con 1:\n\n| id | trabaja_01 | ingreso_miles |\n|:---|---:|---:|\n| 1 | 1 | 420 |\n| 2 | 1 | 650 |\n| 3 | 0 | 300 |\n| 4 | 1 | 380 |\n| 5 | 1 | 720 |\n| ... | ... | ... |",
        "instruction": "Calcula la correlación entre la variable binaria `trabaja_01` y el `ingreso_miles` en `encuesta_social` usando `cor()`.",
        "objective": "Calcular e interpretar una correlación punto-biserial con una variable dicotómica codificada 0/1."
    },
    "intro-r-11-006": {
        "context": "Queremos analizar de forma conjunta tres variables en `encuesta_social`: `trabaja_01`, `ingreso_miles` y `horas_ocio`.\n\nBase `encuesta_social` disponible.",
        "instruction": "1. Guarda en `analisis_final` la selección de `trabaja_01`, `ingreso_miles` y `horas_ocio`.\n2. Calcula su matriz de correlaciones con `cor()`.\n3. Evalúa la inferencia entre `trabaja_01` y `horas_ocio` usando `cor.test()`.",
        "objective": "Utilizar una matriz de correlaciones para responder una pregunta sustantiva específica con respaldo inferencial."
    },
    "intro-r-12-001": {
        "context": "Para estudiar la relación entre dos variables cualitativas, construimos una **tabla de contingencia (cruzada)**:\n\n`table(base$variable_fila, base$variable_columna)`\n\nDistribución en `encuesta_participacion` (60 casos):\n\n| Participación | Metro | Bus | Bicicleta | Total |\n|:---|---:|---:|---:|---:|\n| **Participa** | 12 | 20 | 8 | 40 |\n| **No participa** | 3 | 10 | 7 | 20 |\n| **Total** | 15 | 30 | 15 | 60 |",
        "instruction": "Cruza `participacion_organizacion` y `transporte_campus` en `encuesta_participacion` con `table()`, guárdala en `tabla` y muéstrala en consola.",
        "objective": "Construir una tabla de contingencia bidimensional con `table(x, y)`."
    },
    "intro-r-12-002": {
        "context": "Como los grupos tienen tamaños diferentes (40 que participan vs 20 que no), debemos comparar **porcentajes condicionales por fila**:\n\n`prop.table(tabla, margin = 1) * 100`\n\nCada fila suma exactamente 100%.",
        "instruction": "Calcula las proporciones por fila de `tabla` usando `prop.table()` con el argumento `margin = 1`.",
        "objective": "Calcular porcentajes condicionales por fila en una tabla de contingencia."
    },
    "intro-r-12-003": {
        "context": "Dos variables son **independientes** si la distribución de una no cambia según la categoría de la otra:\n\nEn el total de la muestra, 15 de 60 personas usan Metro (el **25%**). Si no hubiera relación, esperaríamos ese mismo 25% en ambos grupos.",
        "instruction": "Si el transporte fuera completamente independiente de la participación, ¿qué porcentaje de usuarios de Metro esperaríamos en cada grupo? Revisa el porcentaje global en el texto y guárdalo en `porcentaje_esperado_metro`.",
        "objective": "Comprender el concepto de independencia estadística y distinguir frecuencias observadas de esperadas."
    },
    "intro-r-12-004": {
        "context": "La **prueba de Chi-cuadrado ($\\chi^2$) de independencia** compara las frecuencias observadas contra las que esperaríamos si no hubiera asociación:\n\n`prueba <- chisq.test(tabla)`\n\n$H_0$: las variables son independientes en la población.",
        "instruction": "Ejecuta la prueba de Chi-cuadrado sobre `tabla`, guárdala en `prueba` y muéstrala en la consola.",
        "objective": "Ejecutar la prueba de chi-cuadrado de independencia con `chisq.test()` e interpretar $H_0$ y p-value."
    },
    "intro-r-12-005": {
        "context": "El objeto retornado por `chisq.test()` contiene tanto las frecuencias reales (`prueba$observed`) como las frecuencias esperadas teóricas (`prueba$expected`).",
        "instruction": "Consulta primero las frecuencias observadas (`prueba$observed`) y luego las frecuencias esperadas (`prueba$expected`).",
        "objective": "Inspeccionar las frecuencias esperadas de una prueba chi-cuadrado con `$expected` para validar sus supuestos."
    },
    "intro-r-12-006": {
        "context": "Un p-value pequeño indica evidencia contra la independencia, pero no mide la fuerza de la asociación:\n\n- **Tabla 1**: Diferencias mínimas del 2% entre grupos con muestra masiva ($p = 0.03$).\n- **Tabla 2**: Diferencias sustantivas del 25% entre grupos con muestra moderada ($p = 0.01$).",
        "instruction": "Compara ambas tablas significativas. Asigna `\"Tabla 1\"` o `\"Tabla 2\"` a `tabla_asociacion_mas_fuerte` según cuál muestra una asociación sustantivamente más intensa.",
        "objective": "Distinguir entre significación estadística y magnitud sustantiva de una asociación."
    },
    "intro-r-12-007": {
        "context": "En `encuesta_comunidad` consultamos a 80 personas sobre su `zona_residencia` (Norte, Centro, Sur) y su nivel de `actividad_comunitaria` (Alta, Media, Baja):\n\n| id | zona_residencia | actividad_comunitaria |\n|:---|:---|:---|\n| 1 | Norte | Alta |\n| 2 | Centro | Media |\n| 3 | Sur | Baja |\n| ... | ... | ... |",
        "instruction": "1. Construye la tabla cruzada entre `zona_residencia` y `actividad_comunitaria` y guárdala en `tabla_comunidad`.\n2. Calcula las proporciones por fila con `prop.table()`.\n3. Ejecuta `chisq.test()` sobre la tabla, guárdala en `prueba_comunidad` y consulta sus frecuencias esperadas.",
        "objective": "Analizar autónomamente la asociación entre dos variables categóricas: tabla, proporciones y chi-cuadrado."
    },
    "intro-r-13-001": {
        "context": "Antes de analizar debemos identificar el tipo de variables y la técnica adecuada:\n\n- **Cuantitativo**: cantidades medibles continuas (promedios, correlaciones).\n- **Categórico**: grupos o clasificaciones cualitativas (tablas cruzadas, Chi-cuadrado).\n\nPreguntas de estudio:\n- Problema 1: ¿Dedicar más horas de estudio se asocia con mayor autoeficacia académica?\n- Problema 2: ¿El medio de transporte se asocia con la participación estudiantil?",
        "instruction": "Clasifica cada problema asignando `\"cuantitativo\"` o `\"categorico\"` a `problema_1` y `problema_2`.",
        "objective": "Seleccionar la técnica estadística adecuada a partir de la pregunta y el tipo de variables involucradas."
    },
    "intro-r-13-002": {
        "context": "En `encuesta_vida_universitaria` analizaremos a los estudiantes de jornada diurna:\n\n| id | jornada | horas_estudio | autoeficacia_academica | transporte_campus | participa_organizacion |\n|:---|:---|---:|---:|:---|:---|\n| 1 | Diurna | 2 | 59 | Metro | Sí |\n| 2 | Diurna | 4 | 68 | Bus | No |\n| 3 | Diurna | 3 | 58 | Bicicleta | Sí |\n| 4 | Diurna | 6 | 64 | Bus | No |\n| 5 | Diurna | 5 | 62 | Metro | No |\n| 6 | Diurna | 8 | 75 | Bus | Sí |\n| ... | ... | ... | ... | ... | ... |",
        "instruction": "1. Filtra a los estudiantes de jornada diurna (`jornada == \"Diurna\"`), selecciona `horas_estudio` y `autoeficacia_academica`, y guarda el resultado en `datos_estudio_diurno`.\n2. Cuenta los valores ausentes en ambas variables usando `sum(is.na())`.",
        "objective": "Preparar una submuestra reproducible filtrando casos, seleccionando variables y diagnosticando ausencias."
    },
    "intro-r-13-003": {
        "context": "Con los datos preparados en `datos_estudio_diurno`, respondemos la pregunta sobre horas de estudio y autoeficacia académica.",
        "instruction": "1. Genera el gráfico de dispersión con `plot()` entre horas de estudio y autoeficacia.\n2. Ejecuta la prueba de correlación inferencial de Pearson con `cor.test()`.",
        "objective": "Conducir e interpretar un análisis bivariado cuantitativo completo: visualización, inferencia y alcance."
    },
    "intro-r-13-004": {
        "context": "Ahora analizamos el Problema 2 sobre `transporte_campus` y `participa_organizacion` en `encuesta_vida_universitaria`.",
        "instruction": "1. Construye la tabla cruzada entre transporte y participación, y guárdala en `tabla_participacion`.\n2. Calcula los porcentajes por fila con `prop.table()`.\n3. Ejecuta la prueba de Chi-cuadrado con `chisq.test()`, guárdala en `prueba_participacion` y consulta sus frecuencias esperadas.",
        "objective": "Conducir e interpretar un análisis bivariado categórico completo: tabla, porcentajes condicionales y chi-cuadrado."
    },
    "intro-r-13-005": {
        "context": "**Checkpoint E — Integración final: Nueva base, nueva pregunta**\n\nEn `encuesta_vinculos_barriales` investigamos si entre las personas ocupadas, participar en organizaciones vecinales se asocia con la confianza comunitaria:\n\n| id | ocupado | participa_vecinal_01 | confianza_comunitaria |\n|:---|:---|---:|---:|\n| 1 | Sí | 1 | 7 |\n| 2 | Sí | 0 | 8 |\n| 3 | Sí | 1 | 6 |\n| 4 | Sí | 1 | 9 |\n| 5 | Sí | 0 | 5 |\n| 6 | No | 1 | 8 |\n| ... | ... | ... | ... |",
        "instruction": "1. Prepara `datos_checkpoint` filtrando a quienes están ocupados (`ocupado == \"Sí\"`) y seleccionando `participa_vecinal_01` y `confianza_comunitaria`.\n2. Evalúa la correlación entre ambas variables en ese subgrupo aplicando `cor.test()`.",
        "objective": "Diseñar y ejecutar de forma autónoma una ruta analítica completa en un contexto nuevo."
    }
}
