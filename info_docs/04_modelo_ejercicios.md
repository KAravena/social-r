# 04 · Modelo universal de ejercicio

## Fuente de verdad

Cada ejercicio vive como YAML y se valida con `content/exercise.schema.json`.

La primera versión del schema contiene cinco grupos de campos:

1. **Identidad y orden**: `id`, `course`, `module`, `lesson`, `order`.
2. **Pedagogía**: `title`, `context`, `instruction`, `objectives`, `difficulty`, `exercise_type`.
3. **Código**: `starter_code`, `setup_code`, `solution_code`.
4. **Evaluación**: `checks`, `diagnostics`, `success_message`.
5. **Andamiaje/plataforma**: `hints`, `persist_code`, `time_limit_seconds`, `xp`, `next_exercise`.

## Tipos de ejercicio

- `run`: ejecutar/observar.
- `complete`: completar un hueco.
- `modify`: modificar código existente.
- `write`: construir código.
- `interpret`: reservado a ejercicios donde el código es solo parte de la respuesta.

## Objetivos triples

Se mantienen tres objetivos opcionales y separados:

- `objectives.r`: habilidad de R.
- `objectives.data`: idea de datos/estadística.
- `objectives.social`: interpretación o problema sustantivo.

Esta separación evita que el curso termine siendo solo entrenamiento sintáctico.

## Por qué YAML → QMD generado

Para decenas o cientos de ejercicios, escribir directamente bloques Quarto produce repetición y mezcla contenido con implementación. El YAML facilita inventario, auditoría, migración, traducción y validación. El QMD se considera un artefacto de compilación.

## Escape hatch

El schema permite `custom_r` en `checks` para casos que el DSL declarativo no pueda expresar. Debe ser excepcional: primero ampliar checks reutilizables, luego recurrir a código ad hoc.
