# 05 · Motor de evaluación

## Principio

**No comparar el código del estudiante con una solución literal.** Evaluar el estado producido por R o propiedades relevantes del resultado.

## Checks del prototipo

### `result_equals`

Comprueba `.result` con `all.equal()`.

### `object_exists`

Comprueba que un objeto exista en `.envir_result`.

### `object_value`

Recupera el objeto desde `.envir_result` y compara valor.

### `object_class`

Comprueba propiedades como `is.numeric`, `is.character`, `is.factor`, etc.

### `custom_r`

Escape hatch para una expresión booleana R.

## Extensiones previstas

- `vector_set_equals` y `vector_ordered_equals`.
- `dataframe_columns`.
- `dataframe_nrow`.
- `dataframe_rows_keyed`.
- `function_tests` con entradas/salidas.
- `contains_call` solo cuando usar una función específica sea objetivo pedagógico.
- `ggplot_layers`, `ggplot_mapping`, escalas y geoms mediante inspección del objeto ggplot.

## Diagnósticos

Los `diagnostics` se evalúan antes de checks generales. Sirven para reconocer errores previsibles y devolver un mensaje pedagógico más preciso.

Ejemplo del prototipo:

```text
edad_promedio = "21.4"
        ↓
is.character(...) y valor == "21.4"
        ↓
"El valor es correcto, pero lo guardaste como texto..."
```

## Errores sintácticos y de ejecución

Quarto Live ya realiza un parse check y su grader puede inspeccionar `.evaluate_result` para encontrar condiciones de tipo `error`. No conviene duplicar esa captura en el schema. La plataforma puede añadir un catálogo de traducciones pedagógicas por patrón de error.

## Precedencia propuesta

1. sintaxis/incompletitud del editor;
2. error de ejecución R conocido;
3. diagnóstico pedagógico específico;
4. check estructural requerido;
5. éxito.
