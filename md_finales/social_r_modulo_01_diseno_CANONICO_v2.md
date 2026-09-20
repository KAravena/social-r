# Social R — Módulo 1: Empezar a pensar con R
## Diseño Pedagógico Canónico Actualizado (v2.0)
### Autocontención, Práctica Activa, Fading y Lenguaje Directo para Principiantes

---

### Estado
Diseño pedagógico canónico — **CANÓNICO v2** — sustituye pedagógicamente a la versión preliminar LOCKED manteniendo estricta trazabilidad curricular.

### Capacidad antes
El estudiante se enfrenta por primera vez a un entorno de programación interactivo (R y WebR).

### Capacidad después
Comprende la interacción mediante comandos, ejecuta y modifica operaciones aritméticas, asigna valores a objetos con `<-`, reutiliza objetos en nuevos cálculos, distingue tipos elementales (números sin comillas vs texto entre comillas), interpreta errores de sintaxis y resuelve autónomamente un registro piloto en el checkpoint.

### Pregunta central
¿Cómo nos comunicamos con R para darle instrucciones, conservar resultados y distinguir diferentes tipos de información?

### Modelo mental
`COMANDO EN EDITOR → CTRL+ENTER → R EVALÚA → RESULTADO EN CONSOLA`
`VALOR → <- → NOMBRE DE OBJETO (MEMORIA) → OPERAR CON EL OBJETO`
`NÚMEROS = SIN COMILLAS (CÁLCULO) | TEXTOS = CON COMILLAS (ETIQUETAS)`

---

## Datasets Contractuales y Objetos del Módulo

* **E01–E02**: Aritmética interactiva de investigación (`18 + 12`, `25 + 15`).
* **E03–E05**: Objetos de conteo (`respuestas <- 33`, `asistentes <- 45`).
* **E06**: Tipos de datos (`edad <- 20`, `estudiante <- "Ana"`).
* **E07**: Detección y corrección de error de delimitador (`mensaje <- "Bienvenidos a R"`).
* **E08 (Checkpoint)**: Registro piloto (`participantes <- 30`, `tasa_respuesta <- 0.85`).

---

## Especificación Detallada de los 8 Ejercicios

### M1-E1 — Tu primera instrucción
* **Rol**: Worked example intencional / Primera exposición.
* **Autocontención**: Todo el contexto se explica en el panel.
* **Contexto**: R funciona ejecutando instrucciones precisas. Escribes el código en el editor de la derecha y presionas **Ctrl + Enter** (o el botón **Ejecutar**) para que R resuelva el cálculo en la consola.
* **Tarea**: Ejecuta la instrucción `18 + 12` y observa el resultado `[1] 30` en la consola.
* **Starter code**:
  ```r
  18 + 12
  ```
* **Solución**:
  ```r
  18 + 12
  ```
* **Checks**:
  - `result_equals`: `30`.

---

### M1-E2 — Cambia la respuesta
* **Rol**: Práctica guiada (modificación activa).
* **Contexto**: Un script de R permite editar instrucciones antes de ejecutarlas. Si llegaron 25 cuestionarios por la mañana y 15 por la tarde, podemos cambiar los números para calcular el nuevo total.
* **Tarea**: Modifica la suma en el editor para calcular `25 + 15` y ejecútala.
* **Starter code**:
  ```r
  # Cambia esta suma para calcular 25 + 15:
  18 + 12
  ```
* **Solución**:
  ```r
  25 + 15
  ```
* **Checks**:
  - `result_equals`: `40`.

---

### M1-E3 — Guardar para después
* **Rol**: Worked example + inspección activa.
* **Contexto**: Para no perder un resultado usamos el operador de asignación `<-`. Le asigna un nombre al valor para guardarlo en la memoria de R:
  `respuestas <- 33`
  Para ver qué contiene un objeto guardado, escribimos su nombre en una línea y lo ejecutamos.
* **Tarea**:
  1. Guarda el valor `33` en `respuestas`.
  2. En la siguiente línea escribe `respuestas` para consultar su contenido en la consola.
* **Starter code**:
  ```r
  # 1. Guarda el valor 33 en respuestas:
  respuestas <- 33

  # 2. Escribe el nombre del objeto para consultarlo en la consola:

  ```
* **Solución**:
  ```r
  respuestas <- 33
  respuestas
  ```
* **Checks**:
  - `object_exists`: `respuestas`.
  - `object_value`: `respuestas == 33`.

---

### M1-E4 — Crea un objeto tú
* **Rol**: Práctica guiada (creación sin solución regalada).
* **Contexto**: El operador `<-` se lee como una flecha hacia la izquierda: toma lo que está a la derecha y lo guarda con el nombre de la izquierda.
* **Tarea**: En un taller comunitario participaron 45 personas. Guarda ese número en un objeto llamado `asistentes`.
* **Starter code**:
  ```r
  # Guarda el número de asistentes (45) en el objeto asistentes:

  ```
* **Solución**:
  ```r
  asistentes <- 45
  ```
* **Checks**:
  - `object_exists`: `asistentes`.
  - `object_value`: `asistentes == 45`.

---

### M1-E5 — Reutiliza lo guardado
* **Rol**: Práctica activa (operar con objetos en memoria).
* **Contexto**: Una vez guardado en memoria, puedes usar el nombre del objeto en cualquier operación matemática, tal como si fuera el número original.
* **Tarea**: Dispones del objeto `asistentes` con valor 45. Multiplícalo por 2 para proyectar la asistencia al próximo encuentro.
* **Starter code**:
  ```r
  # Multiplica el objeto asistentes por 2:

  ```
* **Solución**:
  ```r
  asistentes * 2
  ```
* **Checks**:
  - `result_equals`: `90`.

---

### M1-E6 — Número o texto
* **Rol**: Práctica guiada (distinción de tipos).
* **Contexto**: R distingue entre dos tipos elementales de información:
  - **Números**: van sin comillas (`20`) y permiten hacer operaciones matemáticas.
  - **Texto**: va entre comillas (`"Ana"`) y se usa para nombres, etiquetas o categorías.
* **Tarea**:
  1. Guarda la edad `20` en el objeto `edad`.
  2. Guarda el nombre `"Ana"` en el objeto `estudiante`.
* **Starter code**:
  ```r
  # 1. Guarda la edad 20 en edad (sin comillas):


  # 2. Guarda el nombre "Ana" en estudiante (con comillas):

  ```
* **Solución**:
  ```r
  edad <- 20
  estudiante <- "Ana"
  ```
* **Checks**:
  - `object_exists`: `edad`, `estudiante`.
  - `object_value`: `edad == 20`.
  - `object_value`: `estudiante == "Ana"`.

---

### M1-E7 — Lee el error antes de corregir
* **Rol**: Práctica de diagnóstico y corrección guiada.
* **Contexto**: Cuando una instrucción no sigue las reglas de R, aparece un mensaje de error. Por ejemplo, si abres una comilla pero no la cierras, R no sabe dónde termina el texto.
* **Tarea**: Observa el código incompleto en el editor, ciérrale la comilla que le falta al texto `"Bienvenidos a R"` y ejecuta la instrucción corregida.
* **Starter code**:
  ```r
  # A este texto le falta cerrar la comilla al final.
  # Agrega la comilla de cierre y ejecuta:
  mensaje <- "Bienvenidos a R
  ```
* **Solución**:
  ```r
  mensaje <- "Bienvenidos a R"
  ```
* **Checks**:
  - `object_exists`: `mensaje`.
  - `object_value`: `mensaje == "Bienvenidos a R"`.

---

### M1-E8 — Encuesta piloto (Checkpoint)
* **Rol**: Mini-transferencia e integración autónoma.
* **Contexto**: En una prueba piloto de una encuesta social registraste 30 participantes y una tasa de respuesta de 0.85 (85%).
* **Tarea**:
  1. Guarda los 30 participantes en el objeto `participantes`.
  2. Guarda la tasa de respuesta (0.85) en el objeto `tasa_respuesta`.
* **Starter code**:
  ```r
  # 1. Guarda los 30 participantes en el objeto participantes:


  # 2. Guarda la tasa de respuesta 0.85 en el objeto tasa_respuesta:

  ```
* **Solución**:
  ```r
  participantes <- 30
  tasa_respuesta <- 0.85
  ```
* **Checks**:
  - `object_exists`: `participantes`, `tasa_respuesta`.
  - `object_value`: `participantes == 30`.
  - `object_value`: `tasa_respuesta == 0.85`.
