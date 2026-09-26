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
import re
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
    exercise_files = [f for f in yml_files if f.name not in ("course.yml", "module.yml", "_course.yml", "_module.yml", "challenge.yml", "challenge.yaml")]

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
                mod_comp = mdata.get("module_completion", {})
                comp_title = mod_comp.get("title", "Ahora puedes:") if isinstance(mod_comp, dict) else "Ahora puedes:"
                comp_outcomes = mod_comp.get("outcomes", []) if isinstance(mod_comp, dict) else []
                outcomes = comp_outcomes or mdata.get("learning_outcomes", [])

                module_outcomes_map[mid] = outcomes

                modules_metadata[mid] = {
                    "id": mid,
                    "title": mdata.get("title", f"Módulo {mid}"),
                    "short_title": mdata.get("short_title", mdata.get("title", f"Módulo {mid}")),
                    "order": mdata.get("order", module_order_map.get(mid, 99)),
                    "description": mdata.get("description", ""),
                    "learning_outcomes": outcomes,
                    "module_completion": {
                        "title": comp_title,
                        "outcomes": outcomes,
                    },
                    "exercises": mdata.get("exercises", []),
                }
        except Exception:
            pass

    # Strict validation of learning outcomes / module completion (no generic fallback in production)
    FORBIDDEN_PHRASES = ["habilidades nucleares", "análisis reproducible", "módulo ", "svg"]
    validation_errors = []
    for mid, m_meta in modules_metadata.items():
        m_outcomes = m_meta.get("learning_outcomes", [])
        if not m_outcomes:
            validation_errors.append(f"Module '{mid}' has no learning outcomes / module_completion defined!")
            continue
        if len(m_outcomes) < 2 or len(m_outcomes) > 4:
            validation_errors.append(
                f"Module '{mid}' has {len(m_outcomes)} outcomes (must be between 2 and 4)."
            )
        for idx, out in enumerate(m_outcomes):
            out_lower = out.lower()
            for phrase in FORBIDDEN_PHRASES:
                if phrase in out_lower:
                    validation_errors.append(
                        f"Module '{mid}' outcome #{idx + 1} contains forbidden phrase '{phrase}': '{out}'"
                    )

    if validation_errors:
        raise ValueError("Module completion validation failed:\n" + "\n".join(f"  - {err}" for err in validation_errors))

    for ex in exercises:
        mid = ex.get("module", "")
        ex["_module_id"] = mid
        ex["_module_order"] = module_order_map.get(mid, 99)
        ex["_module_title"] = module_title_map.get(mid, f"Módulo: {mid}")
        ex["_module_short_title"] = module_short_title_map.get(mid, ex["_module_title"])
        ex["_module_outcomes"] = module_outcomes_map.get(mid, [])
        ex["_module_comp_title"] = modules_metadata.get(mid, {}).get("module_completion", {}).get("title", "Ahora puedes:")

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


def load_challenges(content_dir: Path, schema_path: Path) -> list[dict[str, Any]]:
    """Load and validate all challenge.yml files from content_dir against schema_path."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    challenges: list[dict[str, Any]] = []
    yml_files = sorted(list(content_dir.rglob("challenge.yml")) + list(content_dir.rglob("challenge.yaml")))

    if not yml_files:
        return []

    # Map module orders and titles
    module_order_map: dict[str, int] = {}
    module_title_map: dict[str, str] = {}
    module_short_title_map: dict[str, str] = {}

    course_yml_candidates = list(content_dir.rglob("course.yml"))
    if course_yml_candidates:
        try:
            cdata = yaml.safe_load(course_yml_candidates[0].read_text(encoding="utf-8"))
            if isinstance(cdata, dict) and "modules" in cdata:
                for idx, mod in enumerate(cdata["modules"]):
                    if isinstance(mod, dict) and "id" in mod:
                        mid = mod["id"]
                        module_order_map[mid] = idx + 1
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
                if "title" in mdata:
                    module_title_map[mid] = mdata["title"]
                if "short_title" in mdata:
                    module_short_title_map[mid] = mdata["short_title"]
        except Exception:
            pass

    errors_list = []
    for path in yml_files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as err:
            errors_list.append(f"YAML syntax error in {path.name}: {err}")
            continue

        if not isinstance(data, dict):
            continue

        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            for e in errors:
                loc = "/".join(map(str, e.path)) if e.path else "root"
                errors_list.append(f"- {path.name} [{loc}]: {e.message}")
            continue

        mid = data.get("module", "")
        data["is_challenge"] = True
        data["_is_challenge"] = True
        data["_file"] = path
        data["_source"] = path.name
        data["_module_id"] = mid
        data["_module_order"] = module_order_map.get(mid, 99)
        data["_module_title"] = module_title_map.get(mid, f"Módulo: {mid}")
        data["_module_short_title"] = module_short_title_map.get(mid, data["_module_title"])
        data["_module_index"] = 99
        data["_module_total"] = 0
        challenges.append(data)

    if errors_list:
        raise ValueError("Challenge validation errors detected:\n" + "\n".join(errors_list))

    challenges.sort(key=lambda x: x["_module_order"])
    return challenges


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
        "  pattern <- paste0('(^|\\\\n|;)[[:space:]]*', var_name, '[[:space:]]*($|\\\\n|;)')",
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


def format_instruction_markdown(text: str) -> str:
    if not text:
        return ""
    # Normalize line endings
    clean_text = text.replace("\r\n", "\n")
    lines = clean_text.split("\n")
    formatted_lines: list[str] = []
    for i, line in enumerate(lines):
        # If this line starts a list (numbered '1.' or bullet '-'), ensure preceded by blank line
        if i > 0 and re.match(r'^\s*(?:1\.|[-*])\s+', line):
            if formatted_lines and formatted_lines[-1].strip() != "":
                formatted_lines.append("")
        formatted_lines.append(line)
    return "\n".join(formatted_lines)


def normalize_markdown_table(table_lines: list[str]) -> list[str]:
    """Normalize a markdown table block:
    - Ensure delimiter row matches the number of columns in header row.
    - Trim trailing extra pipes or malformed delimiter tokens.
    """
    if len(table_lines) < 2:
        return table_lines

    header = table_lines[0].strip()
    delimiter = table_lines[1].strip()

    header_cols = [c.strip() for c in header.strip('|').split('|')]
    n_cols = len(header_cols)

    del_parts = [c.strip() for c in delimiter.strip('|').split('|') if c.strip() != '']

    new_del_parts = []
    for i in range(n_cols):
        if i < len(del_parts):
            raw = del_parts[i]
            left = raw.startswith(':')
            right = raw.endswith(':')
            if left and right:
                norm = ":---:"
            elif right:
                norm = "---:"
            elif left:
                norm = ":---"
            else:
                norm = "---"
            new_del_parts.append(norm)
        else:
            new_del_parts.append("---")

    normalized_delimiter = "| " + " | ".join(new_del_parts) + " |"
    result = [table_lines[0], normalized_delimiter]
    result.extend(table_lines[2:])
    return result


def format_context_markdown(text: str) -> str:
    """Format context markdown:
    - Normalizes lists and blank lines.
    - Identifies markdown tables, normalizes delimiters, and wraps each in ::: {.sr-data-table-wrap}.
    """
    if not text:
        return ""

    clean_text = text.replace("\r\n", "\n")
    lines = clean_text.split("\n")

    output_lines: list[str] = []
    in_table = False
    table_buffer: list[str] = []

    def flush_table():
        nonlocal in_table, table_buffer
        if not table_buffer:
            return
        norm_table = normalize_markdown_table(table_buffer)
        if output_lines and output_lines[-1].strip() != "":
            output_lines.append("")
        output_lines.append("::: {.sr-data-table-wrap}")
        output_lines.extend(norm_table)
        output_lines.append(":::")
        output_lines.append("")
        table_buffer = []
        in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        is_table_row = stripped.startswith("|") and stripped.endswith("|")

        if is_table_row:
            if not in_table:
                if i + 1 < len(lines) and lines[i+1].strip().startswith("|") and "---" in lines[i+1]:
                    in_table = True
                    table_buffer.append(stripped)
                else:
                    output_lines.append(line)
            else:
                table_buffer.append(stripped)
        else:
            if in_table:
                flush_table()
            # If line starts a list, ensure preceded by blank line
            if i > 0 and re.match(r'^\s*(?:1\.|[-*])\s+', line):
                if output_lines and output_lines[-1].strip() != "":
                    output_lines.append("")
            output_lines.append(line)
        i += 1

    if in_table:
        flush_table()

    return "\n".join(output_lines)


def render_exercise(ex: dict[str, Any], index: int, total_count: int = 25, is_challenge: bool = False) -> str:
    """Render a single interactive exercise using clean semantic Pandoc fenced divs."""
    order = ex.get("order", index)
    title = ex["title"]
    ex_id = ex["id"]
    hints = ex.get("hints", [])
    hints_count = len(hints)
    active_cls = " .is-active-exercise" if index == 0 else ""
    is_ch = is_challenge or ex.get("is_challenge", False) or ex.get("_is_challenge", False)
    challenge_cls = " .social-r-challenge" if is_ch else ""
    challenge_attr = ' data-is-challenge="true"' if is_ch else ""

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

    if is_ch:
        badge_html = f'<span class="sr-section-badge sr-section-badge--challenge"><span class="sr-challenge-badge-icon" aria-hidden="true">◇</span> Desafío final</span>'
        section_title = f"Desafío Final · {mod_short_title}"
    else:
        badge_html = f'<span class="sr-section-badge">Ejercicio {mod_idx + 1} de {mod_total}</span>'
        section_title = "Ejercicio"

    parts = [
        f'::: {{#ex-{ex_id} .social-r-exercise{challenge_cls}{active_cls} exercise="{ex_id}" data-exercise-id="{ex_id}" data-exercise-order="{mod_idx}" data-exercise-module-index="{mod_idx}" data-exercise-global-index="{index}" data-exercise-title="{title}" data-module-id="{mod_id}" data-module-title="{mod_title}" data-module-short-title="{mod_short_title}" data-module-order="{mod_order}" data-module-total="{mod_total}"{challenge_attr}}}',
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
        '    <svg class="sr-sec-icon" aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M11 2H5a1.5 1.5 0 0 0-1.5 1.5v10A1.5 1.5 0 0 0 5 15h6a1.5 1.5 0 0 0 1.5-1.5v-10A1.5 1.5 0 0 0 11 2z"/><path d="M7 2v2.5a.5.5 0 0 0 .5.5H10"/><path d="M5.5 8.5h5M5.5 11.5h3"/></svg>',
        f'    <span class="sr-section-title">{section_title}</span>',
        '  </div>',
        f'  {badge_html}',
        '</div>',
        "```",
        "",
        "::: {.sr-section-body}",
        "",
        f"### {title} {{.sr-exercise-title}}",
        "",
    ]

    if ex.get("context"):
        parts += [format_context_markdown(ex["context"]), ""]

    if show_objective and obj_r:
        parts += [
            "```{=html}",
            '<div class="sr-objective-block">',
            '  <div class="sr-objective-header">',
            '    <svg class="sr-target-icon" aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="2.5"/><circle cx="8" cy="8" r="0.75" fill="currentColor"/></svg>',
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
        '    <svg class="sr-sec-icon" aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="6.5" y1="4" x2="13" y2="4"/><line x1="6.5" y1="8" x2="13" y2="8"/><line x1="6.5" y1="12" x2="13" y2="12"/><circle cx="3.5" cy="4" r="1" fill="currentColor"/><circle cx="3.5" cy="8" r="1" fill="currentColor"/><circle cx="3.5" cy="12" r="1" fill="currentColor"/></svg>',
        '    <span class="sr-section-title">Instrucciones</span>',
        '  </div>',
        '</div>',
        "```",
        "",
        "::: {.sr-section-body}",
        "",
        "#### Tu tarea {.sr-task-heading}",
        "",
        format_instruction_markdown(ex["instruction"]),
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
        '    <svg class="sr-sec-icon" aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 6.5a2.5 2.5 0 1 1 5 0c0 1-.7 1.7-1.2 2.3h-2.6C6.2 8.2 5.5 7.5 5.5 6.5z"/><path d="M6.5 11.5h3M7 13.5h2"/></svg>',
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
        '<div class="sr-help-actions" data-tour="hints">',
        f'  <button class="sr-hint-toggle-btn" data-exercise-id="{ex_id}" aria-expanded="false" aria-controls="sr-hints-list-{ex_id}"><svg class="sr-btn-icon" aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 6.5a2.5 2.5 0 1 1 5 0c0 1-.7 1.7-1.2 2.3h-2.6C6.2 8.2 5.5 7.5 5.5 6.5z"/><path d="M6.5 11.5h3M7 13.5h2"/></svg><span class="sr-hint-btn-text">Ver pista</span></button>'
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
        '  <svg class="sr-r-file-icon" aria-hidden="true" focusable="false" width="14" height="16" viewBox="0 0 16 18" fill="none"><path d="M2.5 2C2.5 1.17 3.17 0.5 4 0.5H10.5L14.5 4.5V16C14.5 16.83 13.83 17.5 13 17.5H4C3.17 17.5 2.5 16.83 2.5 16V2Z" fill="#eff6ff" stroke="#2563eb" stroke-width="1.2"/><path d="M10 0.5V5H14.5" stroke="#2563eb" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><text x="4.5" y="13.2" font-family="JetBrains Mono, monospace" font-size="7.5" font-weight="800" fill="#1d4ed8">R</text></svg>',
        f'  <span class="sr-tab-filename">{"desafio.R" if is_ch else "script.R"}</span>',
        '  <span class="sr-tab-close" aria-hidden="true">×</span>',
        '</div>',
        '<div class="sr-editor-header-actions">',
        '  <span class="sr-shortcut-badge" data-tour="run"><svg class="sr-kbd-icon" aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1.5" y="3.5" width="13" height="9" rx="2"/><path d="M4 6.5h.01M6.5 6.5h.01M9 6.5h.01M11.5 6.5h.01M4 9.5h.01M11.5 9.5h.01M6.5 9.5h3"/></svg><kbd>Ctrl + Enter</kbd> para ejecutar</span>',
        f'  <button class="sr-btn-reset" data-exercise-id="{ex_id}" title="Restaurar código inicial"><svg class="sr-btn-icon" aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 2.5v4h4"/><path d="M3.5 10a5 5 0 1 0 1.2-5.4L2.5 6.5"/></svg>Reiniciar</button>',
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
        f'<button class="sr-btn-submit{" sr-btn-submit--challenge" if is_ch else ""}" data-exercise-id="{ex_id}" data-tour="check">{"✓ Comprobar desafío" if is_ch else "✓ Comprobar respuesta"}</button>',
        f'<button class="sr-btn-run d-none" data-exercise-id="{ex_id}" aria-hidden="true" style="display:none !important;">Ejecutar</button>',
        "```",
        ":::",
        "",
        "::: {.sr-console-panel .sr-output-panel}",
        "",
        "::: {.sr-console-header .sr-output-header}",
        "```{=html}",
        f'<div class="sr-output-tabs" role="tablist" aria-label="Salida de R">',
        f'  <button type="button" class="sr-output-tab is-active" id="sr-tab-console-{ex_id}" role="tab" aria-selected="true" aria-controls="sr-pane-console-{ex_id}" data-tab="console" data-exercise-id="{ex_id}" tabindex="0">Consola R</button>',
        f'  <button type="button" class="sr-output-tab sr-output-tab-plot d-none" id="sr-tab-plot-{ex_id}" role="tab" aria-selected="false" aria-controls="sr-pane-plot-{ex_id}" data-tab="plot" data-exercise-id="{ex_id}" tabindex="-1">Gráfico</button>',
        f'</div>',
        f'<div class="sr-output-actions">',
        f'  <div class="sr-console-actions" id="sr-console-actions-{ex_id}">',
        f'    <button type="button" class="sr-btn-clear-console" data-exercise-id="{ex_id}" title="Limpiar consola">Limpiar</button>',
        f'  </div>',
        f'  <div class="sr-plot-actions d-none" id="sr-plot-actions-{ex_id}">',
        f'    <div class="sr-plot-pager d-none" id="sr-plot-pager-{ex_id}" role="group" aria-label="Navegación de gráficos">',
        f'      <button type="button" class="sr-plot-nav-btn sr-plot-prev" data-exercise-id="{ex_id}" aria-label="Gráfico anterior" title="Gráfico anterior" disabled>‹</button>',
        f'      <span class="sr-plot-counter" id="sr-plot-counter-{ex_id}">1 / 1</span>',
        f'      <button type="button" class="sr-plot-nav-btn sr-plot-next" data-exercise-id="{ex_id}" aria-label="Siguiente gráfico" title="Siguiente gráfico" disabled>›</button>',
        f'    </div>',
        f'    <button type="button" class="sr-btn-expand-plot" data-exercise-id="{ex_id}" title="Ampliar gráfico" aria-label="Ampliar gráfico">⛶ Ampliar</button>',
        f'  </div>',
        f'</div>',
        "```",
        ":::",  # close sr-console-header
        "",
        "::: {.sr-output-body}",
        "```{=html}",
        f'<div id="sr-pane-console-{ex_id}" class="sr-console-transcript sr-output-pane is-active" role="tabpanel" aria-labelledby="sr-tab-console-{ex_id}" data-exercise-id="{ex_id}"></div>',
        f'<div id="sr-pane-plot-{ex_id}" class="sr-plot-pane sr-output-pane d-none" role="tabpanel" aria-labelledby="sr-tab-plot-{ex_id}" data-exercise-id="{ex_id}" hidden>',
        f'  <div class="sr-plot-container" role="img" aria-label="Gráfico generado por R">',
        f'    <div class="sr-plot-stage" id="sr-plot-stage-{ex_id}"></div>',
        f'  </div>',
        f'</div>',
        "```",
        ":::",  # close sr-output-body
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


def generate_course_config(root_dir: Path, published_through: int, exercises: list[dict[str, Any]]) -> None:
    """Generate js/platform/course-config.js based on course.yml publication state."""
    course_yml = root_dir / "content" / "courses" / "intro-r" / "course.yml"
    total_modules = 13
    total_exercises = 88
    published_module_slugs = []
    all_module_slugs = []

    if course_yml.exists():
        try:
            cdata = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
            if isinstance(cdata, dict):
                total_modules = cdata.get("total_modules", 13)
                total_exercises = cdata.get("total_exercises", 88)
                modules_list = cdata.get("modules", [])
                for mod in modules_list:
                    if isinstance(mod, dict):
                        mod_id = mod.get("id")
                        all_module_slugs.append(mod_id)
                        if mod.get("order", 99) <= published_through:
                            published_module_slugs.append(mod_id)
        except Exception:
            pass

    if not all_module_slugs:
        all_module_slugs = [
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores",
            "03-hacer-preguntas-a-los-datos",
            "04-entender-una-base-de-datos",
            "05-seleccionar-y-filtrar-datos",
            "06-trabajar-cuando-faltan-datos",
            "07-describir-categorias",
            "08-describir-cantidades",
            "09-ver-relaciones-entre-dos-cantidades",
            "10-elegir-y-evaluar-una-correlacion",
            "11-trabajar-con-varias-correlaciones",
            "12-relacionar-categorias",
            "13-de-la-pregunta-al-analisis"
        ]

    if not published_module_slugs:
        published_module_slugs = all_module_slugs[:published_through]

    published_exercises = [ex for ex in exercises if ex.get("_module_order", 99) <= published_through]
    published_exercise_count = len(published_exercises)
    last_published_exercise_id = published_exercises[-1]["id"] if published_exercises else "intro-r-05-008"
    last_course_exercise_id = exercises[-1]["id"] if exercises else "intro-r-13-005"

    slugs_js = json.dumps(published_module_slugs, indent=6)
    all_slugs_js = json.dumps(all_module_slugs, indent=6)

    js_code = f"""/**
 * Social R - Central Course Publication Configuration
 * Defines publication state, published exercise boundaries, and module access control.
 * M01–M05: published (production baseline).
 * M06–M13: standby (editorial state kept intact, enabled exclusively in local preview mode).
 * Generated automatically from content/courses/intro-r/course.yml
 */
(function () {{
  "use strict";

  const courseConfig = {{
    courseId: "intro-r",
    totalModules: {total_modules},
    totalExercises: {total_exercises},
    publishedThrough: {published_through},
    publishedModuleCount: {len(published_module_slugs)},
    publishedExerciseCount: {published_exercise_count},
    lastPublishedExerciseId: "{last_published_exercise_id}",
    lastCourseExerciseId: "{last_course_exercise_id}",
    publishedModuleSlugs: {slugs_js},
    allModuleSlugs: {all_slugs_js},

    // Editorial status checks (Strictly reflect course.yml metadata)
    isModulePublished(moduleIdOrOrder) {{
      if (typeof moduleIdOrOrder === "number") {{
        return moduleIdOrOrder >= 1 && moduleIdOrOrder <= this.publishedThrough;
      }}
      if (typeof moduleIdOrOrder === "string") {{
        const m = moduleIdOrOrder.match(/^intro-r-(\\d+)-/);
        if (m) {{
          const modNum = parseInt(m[1], 10);
          return modNum >= 1 && modNum <= this.publishedThrough;
        }}
        return this.publishedModuleSlugs.includes(moduleIdOrOrder);
      }}
      return false;
    }},

    isExercisePublished(exerciseId) {{
      if (!exerciseId || typeof exerciseId !== "string") return false;
      const m = exerciseId.match(/^intro-r-(\\d+)-/);
      if (!m) return false;
      const modNum = parseInt(m[1], 10);
      return modNum >= 1 && modNum <= this.publishedThrough;
    }},

    isStandbyExercise(exerciseId) {{
      if (!exerciseId || typeof exerciseId !== "string") return false;
      const m = exerciseId.match(/^intro-r-(\\d+)-/);
      if (!m) return false;
      const modNum = parseInt(m[1], 10);
      return modNum > this.publishedThrough && modNum <= this.totalModules;
    }},

    isStandbyModule(moduleIdOrOrder) {{
      if (typeof moduleIdOrOrder === "number") {{
        return moduleIdOrOrder > this.publishedThrough && moduleIdOrOrder <= this.totalModules;
      }}
      if (typeof moduleIdOrOrder === "string") {{
        const m = moduleIdOrOrder.match(/^intro-r-(\\d+)-/);
        if (m) {{
          const modNum = parseInt(m[1], 10);
          return modNum > this.publishedThrough && modNum <= this.totalModules;
        }}
        const idx = this.allModuleSlugs.indexOf(moduleIdOrOrder);
        return idx >= this.publishedThrough && idx < this.totalModules;
      }}
      return false;
    }},

    // Central local preview detection (localhost / 127.0.0.1)
    isLocalPreview() {{
      if (typeof window !== "undefined" && window.__FORCE_PRODUCTION_MODE__) {{
        return false;
      }}
      if (typeof window === "undefined" || !window.location) return false;
      const hostname = window.location.hostname;
      return hostname === "localhost" || hostname === "127.0.0.1";
    }},

    // Availability layer for QA / local preview overrides
    // In production: availability == publication (M01-M05, 36 exercises)
    // In local preview: availability == published + standby (M01-M13, 88 exercises)
    isModuleAvailable(moduleIdOrOrder) {{
      if (this.isModulePublished(moduleIdOrOrder)) return true;
      if (this.isLocalPreview()) {{
        return this.isStandbyModule(moduleIdOrOrder);
      }}
      return false;
    }},

    isExerciseAvailable(exerciseId) {{
      if (this.isExercisePublished(exerciseId)) return true;
      if (this.isLocalPreview()) {{
        return this.isStandbyExercise(exerciseId);
      }}
      return false;
    }},

    getAvailableModuleIds() {{
      return this.isLocalPreview() ? [...this.allModuleSlugs] : [...this.publishedModuleSlugs];
    }},

    getAvailableExerciseCount() {{
      return this.isLocalPreview() ? this.totalExercises : this.publishedExerciseCount;
    }},

    getAvailableModuleCount() {{
      return this.isLocalPreview() ? this.totalModules : this.publishedModuleCount;
    }},

    getLastAvailableExerciseId() {{
      return this.isLocalPreview() ? this.lastCourseExerciseId : this.lastPublishedExerciseId;
    }},

    getPublishedModuleIds() {{
      return [...this.publishedModuleSlugs];
    }},

    getLastPublishedExerciseId() {{
      return this.lastPublishedExerciseId;
    }}
  }};

  window.SocialR = window.SocialR || {{}};
  window.SocialR.courseConfig = courseConfig;
}})();
"""
    dest_file = root_dir / "js" / "platform" / "course-config.js"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text(js_code, encoding="utf-8")

    docs_dest = root_dir / "docs" / "js" / "platform" / "course-config.js"
    docs_dest.parent.mkdir(parents=True, exist_ok=True)
    docs_dest.write_text(js_code, encoding="utf-8")
    print(f"[OK] Generated course-config.js (publishedThrough: {published_through}, exercises: {published_exercise_count})")


def build_document(
    exercises: list[dict[str, Any]],
    challenges: list[dict[str, Any]] | None = None,
    modules_metadata: dict[str, dict[str, Any]] | None = None,
    published_through: int | None = None,
) -> str:
    """Build the complete full-screen Quarto live-html document using Pandoc semantic fenced divs."""
    total_count = len(exercises)
    first_title = exercises[0]["title"] if exercises else "Social R"
    first_mod_title = exercises[0].get("_module_title", "Módulo 1: Tus primeros minutos con R") if exercises else "Módulo 1"
    first_mod_short = exercises[0].get("_module_short_title", "Módulo 1") if exercises else "Módulo 1"
    first_mod_total = exercises[0].get("_module_total", 8) if exercises else 8

    pub_threshold = published_through if published_through is not None else 5

    if modules_metadata is None:
        modules_metadata = {}
        for ex in exercises:
            mid = ex.get("_module_id", "")
            if mid and mid not in modules_metadata:
                order = ex.get("_module_order", 1)
                status = "published" if order <= pub_threshold else "standby"
                modules_metadata[mid] = {
                    "id": mid,
                    "title": ex.get("_module_title", f"Módulo {mid}"),
                    "short_title": ex.get("_module_short_title", f"Módulo {mid}"),
                    "order": order,
                    "status": status,
                    "learning_outcomes": ex.get("_module_outcomes", []),
                    "module_completion": {
                        "title": ex.get("_module_comp_title", "Ahora puedes:"),
                        "outcomes": ex.get("_module_outcomes", []),
                    },
                    "total_exercises": ex.get("_module_total", 8),
                }

    if challenges:
        for ch in challenges:
            mid = ch.get("_module_id", "")
            if mid in modules_metadata:
                modules_metadata[mid]["challenge"] = {
                    "id": ch["id"],
                    "title": ch["title"],
                }

    modules_json_str = json.dumps(modules_metadata, ensure_ascii=False)

    header = [
        "---",
        'title: "Social R | Curso interactivo"',
        'pagetitle: "Social R | Curso interactivo"',
        'title-prefix: ""',
        'description: "Aprende R desde cero con ejercicios y datos de ciencias sociales directamente en el navegador."',
        'lang: es',
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
        '      <link rel="stylesheet" href="css/tour.css?v=1.0">',
        '      <link rel="stylesheet" href="css/course-reset.css?v=1.0">',
        '      <link rel="icon" type="image/svg+xml" href="assets/favicon/favicon.svg">',
        '      <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon/favicon-32x32.png">',
        '      <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon/favicon-16x16.png">',
        '      <link rel="apple-touch-icon" sizes="180x180" href="assets/favicon/apple-touch-icon.png">',
        '      <link rel="shortcut icon" href="assets/favicon/favicon.ico">',
        '      <link rel="manifest" href="assets/favicon/site.webmanifest">',
        '      <meta name="theme-color" content="#0B0F19">',
        "include-after-body:",
        "  - text: |",
        '      <script src="js/platform/event-bus.js"></script>',
        '      <script src="js/platform/course-config.js"></script>',
        '      <script src="js/platform/progress-store.js"></script>',
        '      <script src="js/platform/course-reset.js"></script>',
        '      <script src="js/platform/graphics.js"></script>',
        '      <script src="js/app/navigation.js?v=0.4.1"></script>',
        '      <script src="js/app/shell.js?v=0.4.1"></script>',
        '      <script src="js/app/splitters.js"></script>',
        '      <script src="js/app/workspace.js"></script>',
        '      <script src="js/platform/quarto-live-adapter.js"></script>',
        '      <script src="js/app/tour.js?v=1.0"></script>',
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
        '    <a href="index.html" class="sr-logo" title="Volver al inicio">Social R</a>',
        '    <span class="sr-breadcrumb-sep">/</span>',
        '    <span class="sr-breadcrumb">Introducción a R</span>',
        '    <span class="sr-breadcrumb-sep">/</span>',
        f'    <span class="sr-breadcrumb-module">{first_mod_title}</span>',
        '  </div>',
        '<div class="sr-topbar-center" data-tour="exercise-navigation">',
        '  <button id="sr-btn-prev" class="sr-nav-btn" disabled title="Ejercicio anterior en este módulo">← Anterior</button>',
        '  <button id="sr-outline-trigger" class="sr-outline-trigger" title="Ver esquema del curso">',
        f'    <span id="sr-topbar-mod-pill" class="sr-topbar-mod-pill">Módulo 1</span>',
        '    <span class="sr-topbar-sep-bar" aria-hidden="true">|</span>',
        f'    <span id="sr-topbar-counter" class="sr-topbar-counter">1/{first_mod_total} ·</span>',
        f'    <span id="sr-topbar-title" class="sr-topbar-title">{first_title}</span>',
        '    <svg class="sr-chevron-icon" aria-hidden="true" focusable="false" width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4.5l3 3 3-3"/></svg>',
        '  </button>',
        '  <button id="sr-btn-next" class="sr-nav-btn" title="Siguiente ejercicio">Siguiente →</button>',
        '</div>',
        '  <div class="sr-topbar-right">',
        '    <div id="sr-webr-status" class="sr-webr-status" data-tour="r-status" aria-live="polite">',
        '      <span class="sr-status-dot"></span>',
        '      <span id="sr-webr-status-text">Iniciando R...</span>',
        '    </div>',
        '    <button id="sr-tour-btn" class="sr-tour-btn" title="Cómo usar Social R" aria-label="Cómo usar Social R">',
        '      <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">',
        '        <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>',
        '        <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>',
        '      </svg>',
        '    </button>',
        '  </div>',
        '</header>',
        '<div id="sr-drawer-backdrop" class="sr-drawer-backdrop">',
        '  <div class="sr-drawer" data-tour="course-map">',
        '    <div class="sr-drawer-header">',
        '      <h3 class="sr-drawer-title">Esquema del curso</h3>',
        '      <button id="sr-drawer-close" class="sr-drawer-close" aria-label="Cerrar esquema">×</button>',
        '    </div>',
        '    <div class="sr-drawer-body">',
        '      <div id="sr-drawer-list" class="sr-drawer-list"></div>',
        '    </div>',
        '    <div class="sr-drawer-footer">',
        '      <button id="sr-drawer-reset-btn" class="sr-drawer-reset-btn" type="button" aria-label="Reiniciar progreso del curso">',
        '        <svg width="13" height="13" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">',
        '          <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>',
        '          <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>',
        '        </svg>',
        '        <span>Reiniciar progreso del curso</span>',
        '      </button>',
        '    </div>',
        '  </div>',
        '</div>',
        '<div id="sr-celebration-backdrop" class="sr-celebration-backdrop" aria-hidden="true" style="display: none;">',
        '  <div class="sr-celebration-card" role="dialog" aria-modal="true" aria-labelledby="sr-cel-title">',
        '    <button id="sr-celebration-close" class="sr-celebration-close" aria-label="Cerrar celebración">×</button>',
        '    <div class="sr-celebration-glow"></div>',
        '    <div class="sr-celebration-icon-box">',
        '      <svg class="sr-celebration-check" aria-hidden="true" focusable="false" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">',
        '        <path d="M4 12l5 5L20 6"/>',
        '      </svg>',
        '    </div>',
        '    <div class="sr-celebration-badge">¡Módulo completado!</div>',
        '    <h2 id="sr-cel-title" class="sr-celebration-title">Tus primeros minutos con R</h2>',
        '    <p id="sr-cel-subtitle" class="sr-celebration-subtitle">Has terminado los 8 ejercicios de este módulo.</p>',
        '    <div class="sr-celebration-outcomes">',
        '      <div class="sr-outcomes-heading">Ahora puedes:</div>',
        '      <ul id="sr-cel-outcomes-list" class="sr-outcomes-list"></ul>',
        '    </div>',
        '    <div id="sr-cel-next-section" class="sr-celebration-next-section">',
        '      <div id="sr-cel-next-label" class="sr-next-step-label">Siguiente paso sugerido:</div>',
        '      <div id="sr-cel-next-title" class="sr-next-step-title">Módulo 2 · Trabajar con varios valores</div>',
        '      <button id="sr-cel-continue-btn" class="sr-btn-cel-continue">',
        '        <span id="sr-cel-btn-text">Continuar al Módulo 2</span>',
        '        <svg class="sr-arrow-icon" aria-hidden="true" focusable="false" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
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
    if challenges:
        for c_idx, ch in enumerate(challenges):
            exercise_blocks.append(render_exercise(ch, total_count + c_idx, total_count, is_challenge=True))

    footer = [
        "",
        "::: {.sr-drag-overlay}",
        ":::",
        "",
        ":::",  # close sr-workspace
        "",
        "```{=html}",
        '<footer class="sr-bottombar" data-tour="progress">',
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
        '<div id="sr-plot-modal" class="sr-plot-modal d-none" role="dialog" aria-modal="true" aria-label="Vista ampliada del gráfico">',
        '  <div class="sr-plot-modal-backdrop"></div>',
        '  <div class="sr-plot-modal-content">',
        '    <div class="sr-plot-modal-header">',
        '      <span class="sr-plot-modal-title">Gráfico R (Vista ampliada)</span>',
        '      <button type="button" class="sr-plot-modal-close" aria-label="Cerrar vista ampliada">✕</button>',
        '    </div>',
        '    <div class="sr-plot-modal-body">',
        '      <div class="sr-plot-modal-stage"></div>',
        '    </div>',
        '  </div>',
        '</div>',
        "```",
        "",
        ":::",  # close social-r-root
        "",
    ]

    return "\n".join(header + exercise_blocks + footer)


def bundle_css(root_dir: Path) -> None:
    """Bundle all modular CSS stylesheets into a single self-contained social-r.css."""
    css_dir = root_dir / "css"
    docs_css_dir = root_dir / "docs" / "css"
    docs_css_dir.mkdir(parents=True, exist_ok=True)

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
        "tour.css",
        "course-reset.css",
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
    (docs_css_dir / "social-r.css").write_text(full_css, encoding="utf-8")
    for fname in ordered_files:
        fpath = css_dir / fname
        if fpath.exists():
            (docs_css_dir / fname).write_text(fpath.read_text(encoding="utf-8"), encoding="utf-8")
    
    # Also copy landing.css standalone stylesheet
    landing_css = css_dir / "landing.css"
    if landing_css.exists():
        (docs_css_dir / "landing.css").write_text(landing_css.read_text(encoding="utf-8"), encoding="utf-8")
    
    # Also sync JS scripts across modular subdirectories
    for sub in ["app", "platform", "landing", "vendor"]:
        src_sub = root_dir / "js" / sub
        if src_sub.exists():
            dest_root = root_dir / "docs" / "js" / sub
            dest_root.mkdir(parents=True, exist_ok=True)
            for js_file in src_sub.glob("*.*"):
                (dest_root / js_file.name).write_bytes(js_file.read_bytes())

    # Sync root js files (e.g. social-r.js)
    for js_file in (root_dir / "js").glob("*.js"):
        dest_root = root_dir / "docs" / "js"
        dest_root.mkdir(parents=True, exist_ok=True)
        (dest_root / js_file.name).write_bytes(js_file.read_bytes())

    print(f"[OK] Bundled {len(ordered_files)} CSS files into social-r.css ({len(full_css)} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Social R Exercise Generator & Validator v0.4.0")
    parser.add_argument("--content", default="content", help="Directory with exercise YAML files")
    parser.add_argument("--schema", default="content/exercise.schema.json", help="JSON schema path")
    parser.add_argument("--output", default="curso.qmd", help="Output QMD file")
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

    print(f"Loading challenges from {content_dir} ...")
    try:
        challenges = load_challenges(content_dir, schema_path)
    except Exception as err:
        print(f"\n[ERROR] Challenge loading / validation failed:\n{err}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] Validated {len(challenges)} challenges successfully.")
    for ch in challenges:
        print(
            f"  [Challenge] {ch['id']}: '{ch['title']}' "
            f"({len(ch.get('checks', []))} checks, {len(ch.get('hints', []))} hints)"
        )

    if args.validate:
        print("\nValidation completed successfully.")
        return

    # Determine publication threshold from course.yml
    published_through = 5
    course_yml = content_dir / "courses" / "intro-r" / "course.yml"
    if course_yml.exists():
        try:
            cdata = yaml.safe_load(course_yml.read_text(encoding="utf-8"))
            if isinstance(cdata, dict) and "published_through" in cdata:
                published_through = int(cdata["published_through"])
        except Exception:
            pass

    # Bundle CSS and sync JS assets
    bundle_css(root)

    # Sync and generate course-config.js
    generate_course_config(root, published_through, exercises)

    # Compile curso.qmd
    qmd_content = build_document(exercises, challenges=challenges, published_through=published_through)
    output_path.write_text(qmd_content, encoding="utf-8")
    print(f"\n[OK] Generated {output_path} ({len(qmd_content.splitlines())} lines, published_through: M{published_through:02d})")


if __name__ == "__main__":
    main()

