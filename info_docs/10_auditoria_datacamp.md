# 10 · Auditoría mecánica de las 62 capturas de referencia

Se inspeccionaron las 62 capturas entregadas, distribuidas en seis capítulos (8 + 16 + 10 + 9 + 12 + 7 ejercicios).

## Patrón recurrente observado

La interfaz mantiene una estructura estable:

- panel narrativo con explicación y una tarea breve;
- editor de script con código preparado o parcialmente preparado;
- consola/output separado;
- acciones de ejecutar y enviar respuesta;
- progresión entre ejercicios con poca variación del motor;
- repetición deliberada de una misma habilidad con cambios pequeños en código/contexto.

## Tipos mecánicos observados

1. ejecutar código ya escrito;
2. completar una expresión/objeto;
3. modificar una asignación previa;
4. construir un objeto a partir de componentes;
5. seleccionar/subsetear;
6. calcular un resumen;
7. encadenar varios pasos usando objetos creados antes.

## Implicación arquitectónica

La diversidad visible no requiere un motor distinto por ejercicio. La mayor parte puede modelarse como datos declarativos + checks reutilizables. El motor debe permitir ambientes por ejercicio y, excepcionalmente, ambientes compartidos para secuencias encadenadas.

## Qué no se copia

No se copian textos, datasets, historias, soluciones ni diseño visual. Las capturas se usan únicamente para abstraer mecánicas de interacción y progresión.
