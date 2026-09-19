#!/usr/bin/env python3
"""Social R Generator & Validator v0.4.0 (Modular Architecture)

Builds Quarto Live interactive documents from declarative YAML exercise files.
Generates full-screen (100vw x 100vh) modular workspace with split-screen
pedagogical layout, CodeMirror editor, R Console, progressive hints, independent
module progression, and celebratory stage completions.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


def r_literal(value: Any) -> str:
    """Serialize a Python value into a valid R expression literal."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "c(" + ", ".join(r_literal(v) for v in value) + ")"
    if isinstance(value, dict):
        entries = [f"{k} = {r_literal(v)}" for k, v in value.items()]
        return "list(" + ", ".join(entries) + ")"
    raise TypeError(f"Unsupported expected value for R literal: {value!r}")


def load_exercises(content_dir: Path, schema_path: Path) -> list[dict[str, Any]]:
    """Load and validate all exercise YAML files from content_dir against schema_path."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    exercises: list[dict[str, Any]] = []
    yml_files = sorted(list(content_dir.rglob("*.yml")) + list(content_dir.rglob("*.yaml")))
    exercise_files = [f for f in yml_files if f.name not in ("course.yml", "module.yml", "_course.yml", "_module.yml")]

    if not exercise_files:
        raise ValueError(f"No exercise YAML files found in {content_dir}")

    seen_ids = set()
    errors_list = []

    for path in exercise_files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as err:
            errors_list.append(f"YAML syntax error in {path.name}: {err}")
            continue

        if not isinstance(data, dict):
            errors_list.append(f"{path.name} is not a valid dictionary")
            continue

        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            for e in errors:
                loc = "/".join(map(str, e.path)) if e.path else "root"
                errors_list.append(f"- {path.name} [{loc}]: {e.message}")
            continue

        ex_id = data.get("id")
        if ex_id in seen_ids:
            existing = [x for x in exercises if x["id"] == ex_id]
            if existing and existing[0]["_file"].name == path.name:
                continue
            errors_list.append(f"Duplicate exercise id: '{ex_id}' in {path.name}")
        seen_ids.add(ex_id)

        data["_file"] = path
        data["_source"] = path.name
        exercises.append(data)

    if errors_list:
        raise ValueError("Schema validation errors detected:\n" + "\n".join(errors_list))

    # Determine module metadata, ordering and titles from course.yml and module.yml
    modules_metadata: dict[str, dict[str, Any]] = {}
    module_order_map: dict[str, int] = {}
    module_title_map: dict[str, str] = {}
    module_short_title_map: dict[str, str] = {}
    module_outcomes_map: dict[str, list[str]] = {}

    course_yml_candidates = list(content_dir.rglob("course.yml"))
    if course_yml_candidates:
        try:
            cdata = yaml.safe_load(course_yml_candidates[0].read_text(encoding="utf-8"))
            if isinstance(cdata, dict) and "modules" in cdata:
                for idx, mod in enumerate(cdata["modules"]):
                    if isinstance(mod, dict) and "id" in mod:
                        mid = mod["id"]
                        module_order_map[mid] = idx
                        if "title" in mod:
                            module_title_map[mid] = mod["title"]
        except Exception:
            pass

    for mod_yml in content_dir.rglob("module.yml"):
        try:
            mdata = yaml.safe_load(mod_yml.read_text(encoding="utf-8"))
            if isinstance(mdata, dict) and "id" in mdata:
                mid = mdata["id"]
                if "order" in mdata:
                    module_order_map[mid] = mdata["order"]
                elif mid not in module_order_map:
                    module_order_map[mid] = 99

                if "title" in mdata:
                    module_title_map[mid] = mdata["title"]
                if "short_title" in mdata:
                    module_short_title_map[mid] = mdata["short_title"]
                if "learning_outcomes" in mdata and isinstance(mdata["learning_outcomes"], list):
                    module_outcomes_map[mid] = mdata["learning_outcomes"]

                modules_metadata[mid] = {
                    "id": mid,
                    "title": mdata.get("title", f"Módulo {mid}"),
                    "short_title": mdata.get("short_title", mdata.get("title", f"Módulo {mid}")),
                    "order": mdata.get("order", module_order_map.get(mid, 99)),
                    "description": mdata.get("description", ""),
                    "learning_outcomes": mdata.get("learning_outcomes", []),
                    "exercises": mdata.get("exercises", []),
                }
        except Exception:
            pass

    for ex in exercises:
        mid = ex.get("module", "")
        ex["_module_id"] = mid
        ex["_module_order"] = module_order_map.get(mid, 99)
        ex["_module_title"] = module_title_map.get(mid, f"Módulo: {mid}")
        ex["_module_short_title"] = module_short_title_map.get(mid, ex["_module_title"])
        ex["_module_outcomes"] = module_outcomes_map.get(mid, [])

    exercises.sort(key=lambda x: (x.get("course", ""), x["_module_order"], x.get("order", 0)))

    # Calculate per-module index and total
    module_counts: dict[str, int] = {}
    for ex in exercises:
        mid = ex["_module_id"]
        module_counts[mid] = module_counts.get(mid, 0) + 1

    module_current_idx: dict[str, int] = {}
    for ex in exercises:
        mid = ex["_module_id"]
        idx_in_mod = module_current_idx.get(mid, 0)
        ex["_module_index"] = idx_in_mod
        ex["_module_total"] = module_counts.get(mid, 1)
        module_current_idx[mid] = idx_in_mod + 1

    # Validate navigation references
    id_set = {x["id"] for x in exercises}
    for ex in exercises:
        nxt = None
        if "navigation" in ex and isinstance(ex["navigation"], dict):
            nxt = ex["navigation"].get("next")
        elif "next_exercise" in ex:
            nxt = ex.get("next_exercise")
        if nxt and nxt not in id_set:
            errors_list.append(f"Exercise '{ex['id']}' references non-existent next exercise '{nxt}'")

    if errors_list:
        raise ValueError("Validation errors detected:\n" + "\n".join(errors_list))

    return exercises


def grader_code(ex: dict[str, Any]) -> str:
    """Generate diagnostic-first R evaluation code for Quarto Live."""
    lines = [
        "if (!exists('.checker_args', inherits = TRUE)) .checker_args <- list()",
        "if (!exists('.envir_result', inherits = TRUE)) .envir_result <- globalenv()",
        "feedback <- NULL",
        ".target_env <- if (exists('.envir_result', inherits = FALSE) && !is.null(.envir_result)) .envir_result else globalenv()",
        ".res_val <- if (exists('.result', envir = .target_env, inherits = FALSE)) get('.result', envir = .target_env) else if (exists('.last_value', envir = .target_env, inherits = FALSE)) get('.last_value', envir = .target_env) else if (exists('.result', inherits = FALSE)) get('.result') else if (exists('.last_value', inherits = FALSE)) get('.last_value') else NULL",
        ".user_code <- if (exists('.checker_args', inherits = FALSE) && !is.null(.checker_args$user_code)) .checker_args$user_code else if (exists('.user_code', inherits = FALSE)) .user_code else ''",
        "",
        ".has_standalone_query <- function(code, var_name) {",
        "  if (is.null(code) || nchar(trimws(code)) == 0) return(FALSE)",
        "  exprs <- tryCatch(parse(text = code), error = function(e) NULL)",
        "  if (!is.null(exprs)) {",
        "    for (i in seq_along(exprs)) {",
        "      item <- exprs[[i]]",
        "      if (is.symbol(item) || is.name(item)) {",
        "        if (as.character(item) == var_name) return(TRUE)",
        "      } else if (is.call(item)) {",
        "        op_str <- tryCatch(as.character(item[[1]]), error = function(err) '')",
        "        if (!op_str %in% c('<-', '=')) {",
        "          if (as.character(item) == var_name) return(TRUE)",
        "        }",
        "      }",
        "    }",
        "  }",
        "  pattern <- paste0('(^|\\\\n|;)\\\\s*', var_name, '\\\\s*($|\\\\n|;)')",
        "  return(grepl(pattern, code))",
        "}",
        "",
        "# 1. Diagnósticos prioritarios para errores y conceptos frecuentes",
    ]

    for diag in ex.get("diagnostics", []):
        msg = r_literal(diag["message"])
        typ = r_literal(diag.get("type", "info"))
        lines += [
            f"if (is.null(feedback) && isTRUE({diag['when_r']})) {{",
            f"  feedback <- list(correct = FALSE, type = {typ}, message = {msg})",
            "}",
        ]

    lines += [
        "",
        "# 2. Verificaciones estructuradas (Checks)",
    ]

    for check in ex.get("checks", []):
        typ = check["type"]
        msg = r_literal(check.get("message", "La respuesta todavía no cumple este criterio."))
        if typ == "result_equals":
            expected = r_literal(check["expected"])
            condition = f"!isTRUE(all.equal(.res_val, {expected}))"
        elif typ == "object_exists":
            obj = r_literal(check["object"])
            condition = f"!exists({obj}, envir = .target_env, inherits = FALSE)"
        elif typ == "object_class":
            obj = r_literal(check["object"])
            cls = check["class"]
            if cls == "numeric":
                condition = f"!exists({obj}, envir = .target_env, inherits = FALSE) || !is.numeric(get({obj}, envir = .target_env))"
            elif cls == "character":
                condition = f"!exists({obj}, envir = .target_env, inherits = FALSE) || !is.character(get({obj}, envir = .target_env))"
            elif cls == "logical":
                condition = f"!exists({obj}, envir = .target_env, inherits = FALSE) || !is.logical(get({obj}, envir = .target_env))"
            else:
                condition = f"!exists({obj}, envir = .target_env, inherits = FALSE) || !inherits(get({obj}, envir = .target_env), {r_literal(cls)})"
        elif typ == "object_value":
            obj = r_literal(check["object"])
            expected = r_literal(check["expected"])
            condition = f"!exists({obj}, envir = .target_env, inherits = FALSE) || !isTRUE(all.equal(get({obj}, envir = .target_env), {expected}))"
        elif typ == "standalone_query":
            obj_name = r_literal(check["object"])
            condition = f"!.has_standalone_query(.user_code, {obj_name})"
        elif typ == "custom_r":
            code_expr = check.get("code") or check.get("expr") or check.get("when_r", "TRUE")
            condition = f"!isTRUE({code_expr})"
        else:
            condition = "FALSE"

        lines += [
            f"if (is.null(feedback) && ({condition})) {{",
            f"  feedback <- list(correct = FALSE, type = 'warning', message = {msg})",
            "}",
        ]

    # Success fallback
    success_msg = r_literal(ex.get("success_message", "¡Excelente trabajo! Has completado este ejercicio correctamente."))
    lines += [
        "",
        "# 3. Éxito si no hay feedback de error acumulado",
        "if (is.null(feedback)) {",
        f"  feedback <- list(correct = TRUE, type = 'success', message = {success_msg})",
        "}",
        "feedback",
    ]

    return "\n".join(lines)


def render_hint(ex_id: str, hint: dict[str, Any], hint_idx: int) -> str:
    """Render a single progressive hint card with header and optional code."""
    title = hint.get("title", f"Pista {hint_idx}")
    text = hint.get("text", "")
    code = hint.get("code")

    out = [
        f"::: {{.sr-hint-card #sr-hint-{ex_id}-{hint_idx} data-hint-index=\"{hint_idx}\" hidden=\"\"}}",
        "",
        "```{=html}",
        '<div class="sr-hint-card-header">',
        f'  <span class="sr-hint-card-title">{title}</span>',
        '</div>',
        '<div class="sr-hint-card-body">',
        "```",
        "",
        text,
        "",
    ]
    if code:
        out += [
            "```r",
            code.rstrip(),
            "```",
            "",
        ]
    out += [
        "```{=html}",
        "</div>",
        "```",
        "",
        ":::",
    ]
    return "\n".join(out)


def render_exercise(ex: dict[str, Any], index: int, total_count: int = 25) -> str:
    """Render a single interactive exercise using clean semantic Pandoc fenced divs."""
    order = ex.get("order", index)
    title = ex["title"]
    ex_id = ex["id"]
    hints = ex.get("hints", [])
    hints_count = len(hints)
    active_cls = " .is-active-exercise" if index == 0 else ""

    # Module attributes
    mod_id = ex.get("_module_id", ex.get("module", "primeros-pasos"))
    mod_title = ex.get("_module_title", f"Módulo: {mod_id}")
    mod_short_title = ex.get("_module_short_title", mod_title)
    mod_order = ex.get("_module_order", 1)
    mod_idx = ex.get("_module_index", order)
    mod_total = ex.get("_module_total", 8)
    
    # Pedagogical objectives
    obj_r = ""
    if "learning_objectives" in ex and isinstance(ex["learning_objectives"], dict):
        obj_r = ex["learning_objectives"].get("r", "")
    elif "objectives" in ex and isinstance(ex["objectives"], dict):
        obj_r = ex["objectives"].get("r", "")
    
    show_workflow = ex.get("ui", {}).get("show_workflow_help", False)
    show_objective = ex.get("ui", {}).get("show_objective", True)

    parts = [
        f'::: {{#ex-{ex_id} .social-r-exercise{active_cls} exercise="{ex_id}" data-exercise-id="{ex_id}" data-exercise-order="{mod_idx}" data-exercise-module-index="{mod_idx}" data-exercise-global-index="{index}" data-exercise-title="{title}" data-module-id="{mod_id}" data-module-title="{mod_title}" data-module-short-title="{mod_short_title}" data-module-order="{mod_order}" data-module-total="{mod_total}"}}',
        "",
        "::: {.sr-lesson-panel}",
        "",
        "::: {.sr-lesson-content}",
        "",
        # SECCIÓN 1: EJERCICIO
        "::: {.sr-lesson-section .sr-section-exercise}",
        "",
        "```{=html}",
        '<div class="sr-section-header">',
        '  <div class="sr-section-header-left">',
        '    <svg class="sr-sec-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M11 2H5a1.5 1.5 0 0 0-1.5 1.5v10A1.5 1.5 0 0 0 5 15h6a1.5 1.5 0 0 0 1.5-1.5v-10A1.5 1.5 0 0 0 11 2z"/><path d="M7 2v2.5a.5.5 0 0 0 .5.5H10"/><path d="M5.5 8.5h5M5.5 11.5h3"/></svg>',
        '    <span class="sr-section-title">Ejercicio</span>',
        '  </div>',
        f'  <span class="sr-section-badge">Ejercicio {mod_idx + 1} de {mod_total}</span>',
        '</div>',
        "```",
        "",
        "::: {.sr-section-body}",
        "",
        f"### {title} {{.sr-exercise-title}}",
        "",
    ]

    if ex.get("context"):
        parts += [ex["context"], ""]

    if show_objective and obj_r:
        parts += [
            "```{=html}",
            '<div class="sr-objective-block">',
            '  <div class="sr-objective-header">',
            '    <svg class="sr-target-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="2.5"/><circle cx="8" cy="8" r="0.75" fill="currentColor"/></svg>',
            '    <span class="sr-objective-label">Objetivo</span>',
            '  </div>',
            f'  <div class="sr-objective-text">{obj_r}</div>',
            '</div>',
            "```",
            "",
        ]

    parts += [
        ":::",  # close sr-section-body
        "",
        ":::",  # close sr-section-exercise
        "",
        # SECCIÓN 2: INSTRUCCIONES
        "::: {.sr-lesson-section .sr-section-instructions}",
        "",
        "```{=html}",
        '<div class="sr-section-header">',
        '  <div class="sr-section-header-left">',
        '    <svg class="sr-sec-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="6.5" y1="4" x2="13" y2="4"/><line x1="6.5" y1="8" x2="13" y2="8"/><line x1="6.5" y1="12" x2="13" y2="12"/><circle cx="3.5" cy="4" r="1" fill="currentColor"/><circle cx="3.5" cy="8" r="1" fill="currentColor"/><circle cx="3.5" cy="12" r="1" fill="currentColor"/></svg>',
        '    <span class="sr-section-title">Instrucciones</span>',
        '  </div>',
        '</div>',
        "```",
        "",
        "::: {.sr-section-body}",
        "",
        "#### Tu tarea {.sr-task-heading}",
        "",
        ex["instruction"],
        "",
    ]

    if show_workflow:
        parts += [
            "::: {.sr-workflow-subblock}",
            "",
            "##### Cómo trabajar {.sr-workflow-heading}",
            "",
            "- Escribe tu código en `script.R`.",
            "- Ejecuta con <kbd class=\"sr-kbd\">Ctrl + Enter</kbd>.",
            "- Revisa la **Consola R**.",
            "- Comprueba tu respuesta con **Comprobar respuesta**.",
            "",
            ":::",
            "",
        ]

    parts += [
        ":::",  # close sr-section-body
        "",
        ":::",  # close sr-section-instructions
        "",
        # SECCIÓN 3: AYUDA
        "::: {.sr-lesson-section .sr-section-help}",
        "",
        "```{=html}",
        '<div class="sr-section-header">',
        '  <div class="sr-section-header-left">',
        '    <svg class="sr-sec-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 6.5a2.5 2.5 0 1 1 5 0c0 1-.7 1.7-1.2 2.3h-2.6C6.2 8.2 5.5 7.5 5.5 6.5z"/><path d="M6.5 11.5h3M7 13.5h2"/></svg>',
        '    <span class="sr-section-title">Ayuda</span>',
        '  </div>',
        '</div>',
        "```",
        "",
        "::: {.sr-section-body}",
        "",
        "```{=html}",
        f'<div id="sr-hints-container-{ex_id}" class="sr-hints-container" aria-live="polite">',
        "```",
        "",
        f"::: {{.sr-hints-list #sr-hints-list-{ex_id}}}",
        "",
    ]

    for i, hint in enumerate(hints, 1):
        parts += [render_hint(ex_id, hint, i), ""]

    parts += [
        ":::",  # close sr-hints-list
        "",
        "```{=html}",
        '<div class="sr-help-actions">',
        f'  <button class="sr-hint-toggle-btn" data-exercise-id="{ex_id}" aria-expanded="false" aria-controls="sr-hints-list-{ex_id}"><svg class="sr-btn-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 6.5a2.5 2.5 0 1 1 5 0c0 1-.7 1.7-1.2 2.3h-2.6C6.2 8.2 5.5 7.5 5.5 6.5z"/><path d="M6.5 11.5h3M7 13.5h2"/></svg><span class="sr-hint-btn-text">Ver pista</span></button>'
        if hints_count > 0
        else "",
        '</div>',
        "</div>",  # close sr-hints-container
        "```",
        "",
        ":::",  # close sr-section-body
        "",
        ":::",  # close sr-section-help
        "",
        ":::",  # close sr-lesson-content
        "",
        ":::",  # close sr-lesson-panel
        "",
        "::: {.sr-splitter-h}",
        "",
        ":::",
        "",
        "::: {.sr-coding-panel}",
        "",
        "::: {.sr-editor-panel}",
        "",
        "::: {.sr-editor-header}",
        "",
        "```{=html}",
        '<div class="sr-editor-tab">',
        '  <svg class="sr-r-file-icon" width="14" height="16" viewBox="0 0 16 18" fill="none"><path d="M2.5 2C2.5 1.17 3.17 0.5 4 0.5H10.5L14.5 4.5V16C14.5 16.83 13.83 17.5 13 17.5H4C3.17 17.5 2.5 16.83 2.5 16V2Z" fill="#eff6ff" stroke="#2563eb" stroke-width="1.2"/><path d="M10 0.5V5H14.5" stroke="#2563eb" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><text x="4.5" y="13.2" font-family="JetBrains Mono, monospace" font-size="7.5" font-weight="800" fill="#1d4ed8">R</text></svg>',
        '  <span class="sr-tab-filename">script.R</span>',
        '  <span class="sr-tab-close" aria-hidden="true">×</span>',
        '</div>',
        '<div class="sr-editor-header-actions">',
        '  <span class="sr-shortcut-badge"><svg class="sr-kbd-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1.5" y="3.5" width="13" height="9" rx="2"/><path d="M4 6.5h.01M6.5 6.5h.01M9 6.5h.01M11.5 6.5h.01M4 9.5h.01M11.5 9.5h.01M6.5 9.5h3"/></svg><kbd>Ctrl + Enter</kbd> para ejecutar</span>',
        f'  <button class="sr-btn-reset" data-exercise-id="{ex_id}" title="Restaurar código inicial"><svg class="sr-btn-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 2.5v4h4"/><path d="M3.5 10a5 5 0 1 0 1.2-5.4L2.5 6.5"/></svg>Reiniciar</button>',
        '</div>',
        "```",
        "",
        ":::",  # close sr-editor-header
        "",
        "::: {.sr-editor-body}",
        "",
    ]

    # Setup code if present
    if ex.get("setup_code"):
        parts += [
            "```{webr}",
            "#| setup: true",
            f"#| exercise: {ex_id}",
            ex["setup_code"].rstrip(),
            "```",
            "",
        ]

    # Main starter block
    parts += [
        "```{webr}",
        f"#| exercise: {ex_id}",
        f"#| persist: {str(ex.get('persist_code', True)).lower()}",
        f"#| timelimit: {ex.get('time_limit_seconds', 30)}",
        ex["starter_code"].rstrip(),
        "```",
        "",
        "```{webr}",
        f"#| exercise: {ex_id}",
        "#| check: true",
        grader_code(ex),
        "```",
        "",
        ":::",  # close sr-editor-body
        "",
        "::: {.sr-actions-bar}",
        "```{=html}",
        f'<button class="sr-btn-submit" data-exercise-id="{ex_id}">✓ Comprobar respuesta</button>',
        f'<button class="sr-btn-run d-none" data-exercise-id="{ex_id}" aria-hidden="true" style="display:none !important;">Ejecutar</button>',
        "```",
        ":::",
        "",
        "::: {.sr-console-panel}",
        "",
        "::: {.sr-console-header}",
        "",
        "[Consola R]{.sr-console-title}",
        "",
        "::: {.sr-console-actions}",
        "```{=html}",
        f'<button class="sr-btn-clear-console" data-exercise-id="{ex_id}" title="Limpiar consola">Limpiar</button>',
        "```",
        ":::",
        "",
        ":::",  # close sr-console-header
        "",
        "::: {.sr-console-transcript}",
        ":::",
        "",
        ":::",  # close sr-console-panel
        "",
        "::: {.sr-feedback-container}",
        "```{=html}",
        f'<div id="sr-feedback-card-{ex_id}" class="sr-feedback-card"></div>',
        "```",
        ":::",  # close sr-feedback-container
        "",
        ":::",  # close sr-editor-panel
        "",
        ":::",  # close sr-coding-panel
        "",
        ":::",  # close social-r-exercise
        "",
    ]
    return "\n".join(parts)


def build_document(exercises: list[dict[str, Any]], modules_metadata: dict[str, dict[str, Any]] | None = None) -> str:
    """Build the complete full-screen Quarto live-html document using Pandoc semantic fenced divs."""
    total_count = len(exercises)
    first_title = exercises[0]["title"] if exercises else "Social R"
    first_mod_title = exercises[0].get("_module_title", "Módulo 1: Tus primeros minutos con R") if exercises else "Módulo 1"
    first_mod_short = exercises[0].get("_module_short_title", "Módulo 1") if exercises else "Módulo 1"
    first_mod_total = exercises[0].get("_module_total", 8) if exercises else 8

    if modules_metadata is None:
        modules_metadata = {}
        for ex in exercises:
            mid = ex.get("_module_id", "")
            if mid and mid not in modules_metadata:
                modules_metadata[mid] = {
                    "id": mid,
                    "title": ex.get("_module_title", f"Módulo {mid}"),
                    "short_title": ex.get("_module_short_title", f"Módulo {mid}"),
                    "order": ex.get("_module_order", 1),
                    "learning_outcomes": ex.get("_module_outcomes", []),
                    "total_exercises": ex.get("_module_total", 8),
                }
    modules_json_str = json.dumps(modules_metadata, ensure_ascii=False)

    header = [
        "---",
        'title: "Social R · Workspace"',
        "engine: knitr",
        "page-layout: custom",
        "format:",
        "  live-html:",
        "    toc: false",
        "    code-fold: false",
        "live:",
        "  grading: true",
        "  show-hints: true",
        "  show-solutions: true",
        "webr:",
        "  cell-options:",
        "    completion: true",
        "    startover: true",
        "    persist: true",
        "include-in-header:",
        "  - text: |",
        '      <link rel="stylesheet" href="css/social-r.css?v=0.4.1">',
        "include-after-body:",
        "  - text: |",
        '      <script src="js/platform/event-bus.js"></script>',
        '      <script src="js/platform/progress-store.js"></script>',
        '      <script src="js/app/navigation.js?v=0.4.1"></script>',
        '      <script src="js/app/shell.js?v=0.4.1"></script>',
        '      <script src="js/app/splitters.js"></script>',
        '      <script src="js/app/workspace.js"></script>',
        '      <script src="js/platform/quarto-live-adapter.js"></script>',
        '      <script src="js/social-r.js"></script>',
        "---",
        "",
        "{{< include ./_extensions/r-wasm/live/_knitr.qmd >}}",
        "",
        "::: {#social-r-root .social-r-app}",
        "",
        "```{=html}",
        f'<script id="sr-modules-metadata" type="application/json">{modules_json_str}</script>',
        '<header class="sr-topbar">',
        '  <div class="sr-topbar-left">',
        '    <a href="#" class="sr-logo">Social R</a>',
        '    <span class="sr-breadcrumb-sep">/</span>',
        '    <span class="sr-breadcrumb">Introducción a R</span>',
        '    <span class="sr-breadcrumb-sep">/</span>',
        f'    <span class="sr-breadcrumb-module">{first_mod_title}</span>',
        '  </div>',
        '<div class="sr-topbar-center">',
        '  <button id="sr-btn-prev" class="sr-nav-btn" disabled title="Ejercicio anterior en este módulo">← Anterior</button>',
        '  <button id="sr-outline-trigger" class="sr-outline-trigger" title="Ver esquema del curso">',
        f'    <span id="sr-topbar-mod-pill" class="sr-topbar-mod-pill">Módulo 1</span>',
        '    <span class="sr-topbar-sep-bar" aria-hidden="true">|</span>',
        f'    <span id="sr-topbar-counter" class="sr-topbar-counter">1/{first_mod_total} ·</span>',
        f'    <span id="sr-topbar-title" class="sr-topbar-title">{first_title}</span>',
        '    <svg class="sr-chevron-icon" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4.5l3 3 3-3"/></svg>',
        '  </button>',
        '  <button id="sr-btn-next" class="sr-nav-btn" title="Siguiente ejercicio">Siguiente →</button>',
        '</div>',
        '  <div class="sr-topbar-right">',
        '    <div id="sr-webr-status" class="sr-webr-status" aria-live="polite">',
        '      <span class="sr-status-dot"></span>',
        '      <span id="sr-webr-status-text">Iniciando R...</span>',
        '    </div>',
        '  </div>',
        '</header>',
        '<div id="sr-drawer-backdrop" class="sr-drawer-backdrop">',
        '  <div class="sr-drawer">',
        '    <div class="sr-drawer-header">',
        '      <h3 class="sr-drawer-title">Esquema del curso</h3>',
        '      <button id="sr-drawer-close" class="sr-drawer-close" aria-label="Cerrar esquema">×</button>',
        '    </div>',
        '    <div class="sr-drawer-body">',
        '      <div id="sr-drawer-list" class="sr-drawer-list"></div>',
        '    </div>',
        '  </div>',
        '</div>',
        '<div id="sr-celebration-backdrop" class="sr-celebration-backdrop" aria-hidden="true" style="display: none;">',
        '  <div class="sr-celebration-card" role="dialog" aria-modal="true" aria-labelledby="sr-cel-title">',
        '    <button id="sr-celebration-close" class="sr-celebration-close" aria-label="Cerrar celebración">×</button>',
        '    <div class="sr-celebration-glow"></div>',
        '    <div class="sr-celebration-icon-box">',
        '      <svg class="sr-celebration-check" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">',
        '        <path d="M4 12l5 5L20 6"/>',
        '      </svg>',
        '    </div>',
        '    <div class="sr-celebration-badge">¡Módulo completado!</div>',
        '    <h2 id="sr-cel-title" class="sr-celebration-title">Tus primeros minutos con R</h2>',
        '    <p id="sr-cel-subtitle" class="sr-celebration-subtitle">Has terminado los 8 ejercicios de este módulo.</p>',
        '    <div class="sr-celebration-outcomes">',
        '      <div class="sr-outcomes-heading">Lo que ya dominas:</div>',
        '      <ul id="sr-cel-outcomes-list" class="sr-outcomes-list"></ul>',
        '    </div>',
        '    <div id="sr-cel-next-section" class="sr-celebration-next-section">',
        '      <div class="sr-next-step-label">Siguiente paso sugerido:</div>',
        '      <div id="sr-cel-next-title" class="sr-next-step-title">Módulo 2 · Trabajar con varios valores</div>',
        '      <button id="sr-cel-continue-btn" class="sr-btn-cel-continue">',
        '        <span id="sr-cel-btn-text">Continuar al Módulo 2</span>',
        '        <svg class="sr-arrow-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
        '      </button>',
        '    </div>',
        '  </div>',
        '</div>',
        "```",
        "",
        "::: {.sr-workspace}",
        "",
    ]

    exercise_blocks = []
    for idx, ex in enumerate(exercises):
        exercise_blocks.append(render_exercise(ex, idx, total_count))

    footer = [
        "",
        "::: {.sr-drag-overlay}",
        ":::",
        "",
        ":::",  # close sr-workspace
        "",
        "```{=html}",
        '<footer class="sr-bottombar">',
        '  <div class="sr-bottombar-left">',
        f'    <span id="sr-bottombar-counter" class="sr-bottombar-counter">Módulo 1 · 1 de {first_mod_total}</span>',
        '  </div>',
        '  <div class="sr-bottombar-center">',
        '    <div id="sr-bottom-module-track" class="sr-bottom-module-track"></div>',
        '  </div>',
        '  <div class="sr-bottombar-right">',
        '    <span id="sr-progress-pct" class="sr-progress-pct">0% del curso</span>',
        '  </div>',
        '</footer>',
        "```",
        "",
        ":::",  # close social-r-root
        "",
    ]

    return "\n".join(header + exercise_blocks + footer)


def bundle_css(root_dir: Path) -> None:
    """Bundle all modular CSS stylesheets into a single self-contained social-r.css."""
    css_dir = root_dir / "css"
    site_css_dir = root_dir / "_site" / "css"
    site_css_dir.mkdir(parents=True, exist_ok=True)

    ordered_files = [
        "tokens.css",
        "layout.css",
        "topbar.css",
        "lesson-panel.css",
        "editor.css",
        "output.css",
        "feedback.css",
        "progress.css",
        "responsive.css",
    ]

    bundled_content = [
        "/**\n",
        " * Social R Platform - Unified Master Stylesheet (Bundled v5.0)\n",
        " * Generated automatically by build.py - Self-contained with zero @import waterfall.\n",
        " */\n\n",
    ]

    for fname in ordered_files:
        fpath = css_dir / fname
        if fpath.exists():
            bundled_content.append(f"/* ==========================================================================\n   {fname}\n   ========================================================================== */\n")
            bundled_content.append(fpath.read_text(encoding="utf-8"))
            bundled_content.append("\n\n")

    full_css = "".join(bundled_content)
    (css_dir / "social-r.css").write_text(full_css, encoding="utf-8")
    (site_css_dir / "social-r.css").write_text(full_css, encoding="utf-8")
    for fname in ordered_files:
        fpath = css_dir / fname
        if fpath.exists():
            (site_css_dir / fname).write_text(fpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[OK] Bundled {len(ordered_files)} CSS files into social-r.css ({len(full_css)} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Social R Exercise Generator & Validator v0.4.0")
    parser.add_argument("--content", default="content", help="Directory with exercise YAML files")
    parser.add_argument("--schema", default="content/exercise.schema.json", help="JSON schema path")
    parser.add_argument("--output", default="index.qmd", help="Output QMD file")
    parser.add_argument("--validate", action="store_true", help="Validate YAML exercises and exit")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    content_dir = root / args.content
    schema_path = root / args.schema
    output_path = root / args.output

    print(f"Loading exercises from {content_dir} ...")
    try:
        exercises = load_exercises(content_dir, schema_path)
    except Exception as err:
        print(f"\n[ERROR] Exercise loading / validation failed:\n{err}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] Validated {len(exercises)} exercises successfully.")
    for idx, ex in enumerate(exercises):
        print(
            f"  [{ex.get('_module_index', idx)}] {ex['id']}: '{ex['title']}' "
            f"({len(ex.get('checks', []))} checks, {len(ex.get('diagnostics', []))} diags, {len(ex.get('hints', []))} hints)"
        )

    if args.validate:
        print("\nValidation completed successfully.")
        return

    # Bundle CSS
    bundle_css(root)

    qmd_content = build_document(exercises)
    output_path.write_text(qmd_content, encoding="utf-8")
    print(f"\n[OK] Generated {output_path} ({len(qmd_content.splitlines())} lines)")


if __name__ == "__main__":
    main()
