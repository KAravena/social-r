# Social R

> R interactivo para Ciencias Sociales.

Plataforma educativa moderna e interactiva para el aprendizaje de análisis de datos y programación en **R**, orientada a estudiantes e investigadores de ciencias sociales. La ejecución de R ocurre íntegramente en el navegador del estudiante a través de **webR (WebAssembly)**, sin necesidad de instalación de software ni servidores backend.

https://karavena.github.io/social-r/

---

## 🏛 Arquitectura y Fuentes de Verdad

Para mantener la reproducibilidad, el repositorio distingue estrictamente entre **fuentes que se editan** y **archivos generados**:

### Fuentes que se editan manualmente (Source of Truth)
- `md_finales/social_r_modulo_01_diseno_LOCKED.md` a `_13_diseno_LOCKED.md`: Especificación pedagógica canónica completa (21 secciones por ejercicio, consignas, soluciones, checks y pistas).
- `data/datasets.R`: Definición reproducible en R de los datasets pedagógicos de M01 a M13.
- `index.qmd`: Landing page interactiva del curso.
- `css/*.css`: Sistema de tokens y estilos modulares (`tokens.css`, `layout.css`, `editor.css`, etc.).
- `js/**/*.js`: Runtime modular de la aplicación (`app/`, `platform/`, `landing/`, `social-r.js`).
- `engine/generator/*.py`: Motor de generación, parser, validadores y compilador.
- `assets/favicon/`: Assets maestros del favicon y manifest web.
- `scripts/generate_favicons.py`: Script de regeneración de assets de favicon a partir del glifo SVG geométrico.

### Archivos generados (No editar manualmente)
- `content/courses/intro-r/modules/**/*.yml`: Archivos YAML declarativos de módulos y ejercicios (generados por `python engine/generator/generate_all_modules.py`).
- `css/social-r.css`: Hoja de estilos unificada combinada automáticamente por `build.py`.
- `curso.qmd`: Documento Quarto Live interactivo compilado (generado por `python engine/generator/build.py`).
- `docs/`: Directorio de despliegue final para GitHub Pages (generado por `quarto render`).

---

## 📁 Estructura del Repositorio

```text
R-EC/
├── _quarto.yml          # Configuración del proyecto Quarto (output-dir: docs)
├── index.qmd            # Fuente de la Landing Page interactiva
├── curso.qmd            # [Generado] Fuente del entorno de curso Quarto Live
├── README.md            # Documentación del proyecto
├── requirements.txt     # Dependencias Python
├── Makefile             # Comandos de conveniencia
├── .gitignore           # Exclusiones de control de versiones
├── assets/
│   └── favicon/         # Iconos canónicos de la plataforma
├── content/             # [Generado] YAML declarativo de los 88 ejercicios
│   └── exercise.schema.json
├── css/                 # Hojas de estilo modulares y social-r.css unificado
├── js/                  # Runtime JS: app, platform, landing y librerías
├── data/                # Datasets canónicos en R y CSV
├── engine/              # Motor de compilación, microcopy y scripts de verificación
│   └── generator/       # generate_all_modules.py, build.py, student_microcopy.py
├── scripts/             # Scripts de mantenimiento (generate_favicons.py)
├── tests/               # Suite de tests permanentes (unitarios y Playwright E2E)
└── docs/                # [Deploy Output] Build estático servido por GitHub Pages
```

---

## 🚀 Flujo de Trabajo y Comandos

### 1. Requisitos
- **Python 3.10+**
- **Quarto CLI 1.4+**
- Instalar dependencias Python:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Generar Contenido (YAMLs desde Markdown LOCKED)
Extrae los 88 ejercicios de los 13 módulos canónicos y valida contra el schema:
```bash
python engine/generator/generate_all_modules.py
```

### 3. Compilar el Curso (curso.qmd y CSS)
Valida los YAMLs, combina las hojas CSS y compila `curso.qmd`:
```bash
python engine/generator/build.py
```

### 4. Desarrollo Local
Para previsualizar localmente con recarga en vivo:
```bash
quarto preview
```
O bien usando el Makefile:
```bash
make preview
```

### 5. Ejecución de Tests
Ejecutar la suite completa de pruebas permanentes:
```bash
python -m unittest discover -s tests -v
```
Tests individuales:
- Tests del generador: `python -m unittest tests/test_generator.py`
- Fidelidad canónica: `python -m unittest tests/test_canonical_locked_fidelity.py`
- Aprendizajes de fin de módulo: `python -m unittest tests/test_module_completion_outcomes.py`
- Evaluadores semánticos: `python -m unittest tests/test_module_3_semantic_graders.py`
- Integridad de favicons: `python -m unittest tests/test_favicon.py`

### 6. Compilar y Desplegar (Deploy a GitHub Pages)
Compilar la salida estática final hacia `docs/`:
```bash
quarto render
```
El directorio `docs/` contiene el sitio estático completo (`index.html`, `curso.html`, `assets/`, `css/`, `js/`, `site_libs/`), configurado como raíz de publicación en GitHub Pages.

---

## 📚 Módulos del Curso y Estado de Publicación

El currículum completo de Social R comprende **13 módulos canónicos (88 ejercicios)**. La landing page muestra el currículo completo; M1–M5 están publicados y M6–M13 aparecen como preview `En preparación`. Actualmente, el contenido navegable del curso está acotado a los **Módulos 1 a 5 (36 ejercicios)** mientras los módulos 6 a 13 permanecen en revisión pedagógica en el repositorio.

La publicación se controla de forma centralizada en `content/courses/intro-r/course.yml` mediante la directiva `published_through: 5`.

| Módulo | Título | Ejercicios | Estado | Foco Metodológico |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Empezar a pensar con R** | 8 | **Publicado** | Instrucciones, cálculos, asignación con `<-`, objetos y lectura de errores. |
| **02** | **Trabajar con varios valores** | 7 | **Publicado** | Creación de vectores con `c()`, orden, posiciones e indexación `[]`. |
| **03** | **Hacer preguntas a los datos** | 7 | **Publicado** | Operadores relacionales (`>`, `==`), vectores lógicos y filtrado por condición. |
| **04** | **Entender una base de datos** | 6 | **Publicado** | Estructura tabular (filas/casos, columnas/variables), data frames y extracción `$`. |
| **05** | **Seleccionar y filtrar datos** | 8 | **Publicado** | Manipulación de datos con `dplyr` (`filter()`, `select()`) y operador pipe `\|>`. |
| **06** | **Trabajar cuando faltan datos** | 6 | *Standby* | Identificación de valores ausentes (`NA`, `is.na()`) y cálculo con `na.rm = TRUE`. |
| **07** | **Describir categorías** | 6 | *Standby* | Frecuencias absolutas (`table()`), frecuencias relativas (`prop.table()`) y porcentajes. |
| **08** | **Describir cantidades** | 7 | *Standby* | Medidas de tendencia central (media, mediana), dispersión y selección de descriptores. |
| **09** | **Ver relaciones entre dos cantidades** | 7 | *Standby* | Diagramas de dispersión, dirección de asociación y correlación de Pearson. |
| **10** | **Elegir y evaluar una correlación** | 8 | *Standby* | Correlación de Spearman para rangos, significancia estadística (`cor.test()`) y p-values. |
| **11** | **Trabajar con varias correlaciones** | 6 | *Standby* | Matrices de correlación multivariadas con `cor()`, manejo pairwise y variables 0/1. |
| **12** | **Relacionar categorías** | 7 | *Standby* | Tablas de contingencia bidimensionales, porcentajes por fila y prueba chi-cuadrado. |
| **13** | **De la pregunta al análisis** | 5 | *Standby* | Proyecto integrador de ciencias sociales: formulación, preparación, modelado y conclusiones. |

### Preview local de módulos en revisión

Cuando Social R corre en:

localhost
o
127.0.0.1

M06–M13 se habilitan automáticamente para QA.

En producción siguen en standby.

### Reactivación Futura de Módulos
Para publicar un nuevo módulo (por ejemplo, Módulo 6):
1. Modificar `published_through: 6` en `content/courses/intro-r/course.yml` (y `PUBLISHED_THROUGH = 6` en `engine/generator/generate_all_modules.py`).
2. Ejecutar `python engine/generator/generate_all_modules.py` y `python engine/generator/build.py`.
3. Renderizar con `quarto render`.


