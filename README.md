# Social R · Plataforma Educativa Interactiva de R para Ciencias Sociales

Plataforma interactiva para la formación integral en análisis cuantitativo y programación en **R**, diseñada específicamente para estudiantes e investigadores de ciencias sociales.

La ejecución del código R ocurre directamente en el navegador del estudiante mediante **webR (WebAssembly)**, sin necesidad de instalación previa de software ni servidores backend.

---

## 📚 Los 13 Módulos Canónicos (88 Ejercicios)

| Módulo | Título | Foco Metodológico |
| :---: | :--- | :--- |
| **01** | **Empezar a pensar con R** | Instrucciones, cálculos, asignación con `<-`, objetos y lectura de errores. |
| **02** | **Trabajar con varios valores** | Creación de vectores con `c()`, orden, posiciones e indexación `[]`. |
| **03** | **Hacer preguntas a los datos** | Operadores relacionales (`>`, `==`), vectores lógicos y filtrado por condición. |
| **04** | **Entender una base de datos** | Estructura tabular (filas/casos, columnas/variables), data frames y extracción `$`. |
| **05** | **Seleccionar y filtrar datos** | Manipulación de datos con `dplyr` (`filter()`, `select()`) y operador pipe `\|>`. |
| **06** | **Trabajar cuando faltan datos** | Identificación de valores ausentes (`NA`, `is.na()`) y cálculo con `na.rm = TRUE`. |
| **07** | **Describir categorías** | Frecuencias absolutas (`table()`), frecuencias relativas (`prop.table()`) y porcentajes. |
| **08** | **Describir cantidades** | Medidas de tendencia central (media, mediana), dispersión y selección de descriptores. |
| **09** | **Ver relaciones entre dos cantidades** | Diagramas de dispersión, dirección de asociación y coeficiente de correlación de Pearson. |
| **10** | **Elegir y evaluar una correlación** | Correlación de Spearman para rangos, significancia estadística (`cor.test()`) y p-values. |
| **11** | **Trabajar con varias correlaciones** | Matrices de correlación multivariadas con `cor()`, manejo pairwise y variables binarias 0/1. |
| **12** | **Relacionar categorías** | Tablas de contingencia bidimensionales, porcentajes por fila y prueba de chi-cuadrado. |
| **13** | **De la pregunta al análisis** | Proyecto integrador de ciencias sociales: formulación, preparación, modelado y conclusiones. |

---

## 🏛 Arquitectura Técnica

```text
┌─────────────────────────────────┐
│     FUENTES CANÓNICAS LOCKED    │  -> md_finales/social_r_modulo_*.md
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     CONTENIDO ESTRUCTURADO      │  -> content/courses/intro-r/modules/...
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│        GENERADOR PYTHON         │  -> engine/generator/build.py
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     DOCUMENTO QUARTO LIVE       │  -> index.qmd + live-html + webR
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│     SITIO ESTÁTICO / APP WEB    │  -> docs/index.html (HTML + CSS + JS)
└─────────────────────────────────┘
```

---

## 🛠 Requisitos del Sistema

- **Git**
- **Quarto CLI** (v1.4+ o v1.9+)
- **Python 3.10+** (con `pyyaml` y `jsonschema`)
- **Navegador web moderno** (Chrome, Edge, Firefox, Brave o Safari con soporte WebAssembly)

---

## 🚀 Flujo de Trabajo y Comandos

### 1. Instalar dependencias de Python
```bash
pip install pyyaml jsonschema
```

### 2. Generar todos los módulos canónicos desde los LOCKED
```bash
python engine/generator/generate_all_modules.py
```

### 3. Compilar el documento interactivo `index.qmd`
```bash
python engine/generator/build.py
```

### 4. Ejecutar la suite de pruebas automatizadas
```bash
python -m unittest discover -s tests -v
```

### 5. Renderizar el sitio estático (HTML final)
```bash
quarto render index.qmd
```

### 6. Servir localmente
```bash
python -m http.server 8000 --directory docs
```
Abre tu navegador en `http://localhost:8000`.

---

## 📁 Estructura del Repositorio

- `content/`: Especificaciones declarativas en YAML para cursos, módulos y ejercicios (validados contra `exercise.schema.json`).
- `data/`: Definiciones reproducibles de todos los microdatasets y variables en R (`data/datasets.R`).
- `docs/`: Sitio web compilado listo para publicación (e.g. GitHub Pages).
- `engine/`: Scripts del generador Python, parser y compilador de checks y diagnósticos.
- `js/`: Scripts cliente para el control de estado, navegación, pistas progresivas y persistencia en LocalStorage.
- `css/`: Sistema de diseño moderno para la interfaz educativa.
- `md_finales/`: Especificaciones pedagógicas canónicas auditadas (`*_LOCKED.md`).
- `tests/`: Suite de pruebas unitarias y de fidelidad canónica.
