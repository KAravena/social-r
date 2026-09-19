# 06 · Modelo de progreso

## MVP

No crear usuarios ni backend. Usar almacenamiento local del navegador.

Quarto Live ya soporta `persist: true` para conservar código editado. Social R necesita una capa propia para estado pedagógico del curso.

## Estado mínimo recomendado

```json
{
  "status": "not_started | in_progress | completed",
  "attempts": 0,
  "hintsUsed": 0,
  "updatedAt": "ISO-8601"
}
```

No guardar una máquina de estados excesivamente granular. Los eventos pueden conservar detalle analítico sin convertir cada evento en un estado persistente.

## Interfaz

```text
ProgressStore
├── get(exerciseId)
├── save(exerciseId, patch)
└── clear(exerciseId)

LocalProgressStore implements ProgressStore
RemoteProgressStore implements ProgressStore   # futuro
```

## Eventos

- `exercise_started`
- `code_run`
- `answer_correct`
- `answer_incorrect`
- `hint_opened`
- `exercise_completed`
- `module_completed`

## Limitación detectada

Quarto Live no documenta actualmente un contrato público de eventos de plataforma para "exercise completed". Su código fuente sí utiliza eventos DOM internos y clases de feedback, pero basarse directamente en ese DOM sería frágil.

Decisión: mantener un `SocialREventBus` propio y construir un adaptador versionado después de la prueba del runtime. No contaminar YAML ni ProgressStore con selectores internos de Quarto Live.
