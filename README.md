# Social R

[![Sitio web](https://img.shields.io/badge/sitio-karavena.github.io%2Fsocial--r-2563eb)](https://karavena.github.io/social-r/)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green.svg)](LICENSE)
[![Quarto](https://img.shields.io/badge/compilado%20con-Quarto-447099)](https://quarto.org)
[![WebR](https://img.shields.io/badge/ejecuci%C3%B3n-WebR-blueviolet)](https://docs.r-wasm.org/webr/latest/)

Social R es un curso interactivo para aprender análisis de datos y programación en R desde cero, orientado a contextos de ciencias sociales. Los ejercicios y evaluaciones se ejecutan directamente en el navegador mediante WebR, sin requerir instalación previa de software ni servidores de cómputo externos.

## Acceso

El curso está disponible públicamente en:

**[https://karavena.github.io/social-r/](https://karavena.github.io/social-r/)**

Permite comenzar a practicar de inmediato desde cualquier navegador moderno de escritorio.

## El curso

El programa abarca 13 módulos estructurados de manera secuencial, sumando 89 ejercicios guiados y 13 desafíos finales con acreditación práctica:

| Módulo | Tema |
| :---: | :--- |
| **01** | Empezar a pensar con R |
| **02** | Trabajar con varios valores |
| **03** | Hacer preguntas a los datos |
| **04** | Entender una base de datos |
| **05** | Seleccionar y filtrar datos |
| **06** | Trabajar cuando faltan datos |
| **07** | Describir categorías |
| **08** | Describir cantidades |
| **09** | Ver relaciones entre dos cantidades |
| **10** | Elegir y evaluar una correlación |
| **11** | Trabajar con varias correlaciones |
| **12** | Relacionar categorías |
| **13** | De la pregunta al análisis |

Cada módulo concluye con un Desafío Final que evalúa la aplicación autónoma de las habilidades aprendidas sobre conjuntos de datos de investigación social.

## Cómo funciona

- **Quarto:** Compila las páginas estáticas del curso y gestiona los bloques interactivos.
- **WebR (WebAssembly):** Ejecuta una instancia completa de R en el navegador del estudiante.
- **Fuentes canónicas:** El contenido pedagógico se define en especificaciones estructuradas en Markdown y se compila a esquemas YAML validados.
- **Persistencia local-first:** El navegador guarda el avance de forma inmediata en el almacenamiento local.
- **Sincronización en la nube:** Un backend en Supabase permite almacenar y recuperar el progreso entre sesiones cuando se utiliza una cuenta de estudiante.

## Progreso

### Invitados
Cualquier persona puede realizar el curso libremente en modo invitado. El avance, las soluciones y las respuestas se almacenan únicamente en el navegador (`localStorage`) del equipo utilizado.

### Estudiantes identificados
Quienes formen parte de una sección académica autorizada pueden identificarse con su RUT/IPE para sincronizar su avance con Supabase. Esto permite:
- Recuperar ejercicios completados y módulos acreditados desde otro navegador o dispositivo.
- Reanudar el trabajo en el último punto registrado.
- Disponer de un respaldo persistente de su actividad en el curso.

El acceso por RUT está pensado para coordinar nóminas de aula cerradas y simplificar el uso diario, no como un sistema de autenticación de alta seguridad.

## Desarrollo local

### Requisitos
- Python 3.10 o superior
- Quarto CLI 1.4 o superior
- Navegador moderno con soporte para WebAssembly

### Preparación del entorno
```bash
# Clonar el repositorio
git clone https://github.com/KAravena/social-r.git
cd social-r

# Instalar dependencias del compilador
pip install -r requirements.txt
```

### Compilación y previsualización
```bash
# 1. Generar esquemas declarativos desde las fuentes canónicas
python engine/generator/generate_all_modules.py

# 2. Compilar estilos, validaciones y documento interactivo
python engine/generator/build.py

# 3. Iniciar servidor de desarrollo local
quarto preview
```

Los mismos pasos se encuentran automatizados en el `Makefile`:
```bash
make preview
```

### Pruebas
Para ejecutar la suite de pruebas automatizadas:
```bash
python -m unittest discover -s tests -v
```

### Publicación
Para generar el sitio estático final en la carpeta `docs/` (servida por GitHub Pages):
```bash
quarto render
```

## Estructura del repositorio

```text
├── content/    # Especificaciones declarativas de módulos y esquemas YAML
├── engine/     # Compilador pedagógico, generadores y validadores
├── js/         # Runtime interactivo, lógica de interfaz y sincronización
├── css/        # Sistema de estilos y tokens visuales de la plataforma
├── supabase/   # Migraciones de base de datos y funciones de soporte
├── scripts/    # Utilidades auxiliares para administración y docencia
├── tests/      # Pruebas unitarias, de integración y validación pedagógica
├── data/       # Conjuntos de datos didácticos y rutinas en R
└── docs/       # Salida estática compilada para despliegue en GitHub Pages
```

## Datos y privacidad

- Las nóminas reales de estudiantes y datos de cursos presenciales no forman parte del repositorio público.
- La configuración sensible y claves de administración se gestionan localmente en `.env`, archivo estrictamente excluido por `.gitignore`.
- Los identificadores de nómina se procesan mediante funciones criptográficas unidireccionales (HMAC) con sal privada antes de su almacenamiento en la base de datos, asociando el progreso a identificadores internos opacos (`UUID`).
- El repositorio no contiene información personal identificable (PII) de estudiantes.

## Licencia

El código de este repositorio se distribuye bajo la licencia MIT. Consulta [LICENSE](LICENSE) para más información.
