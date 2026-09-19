#!/usr/bin/env python3
"""Social R - Canonical 13 Modules Importer & YAML Generator

Generates all 13 pedagogically audited modules (M01-M13, 88 exercises)
from the canonical locked Markdown specifications in md_finales/.
Produces valid declarative YAML files adhering to content/exercise.schema.json.
"""
from __future__ import annotations

import glob
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
LOCKED_DIR = ROOT / "md_finales"
CONTENT_DIR = ROOT / "content" / "courses" / "intro-r"
MODULES_DIR = CONTENT_DIR / "modules"


MODULE_SLUGS = {
    1: ("01-empezar-a-pensar-con-r", "Módulo 1: Empezar a pensar con R", "Módulo 1"),
    2: ("02-trabajar-con-varios-valores", "Módulo 2: Trabajar con varios valores", "Módulo 2"),
    3: ("03-hacer-preguntas-a-los-datos", "Módulo 3: Hacer preguntas a los datos", "Módulo 3"),
    4: ("04-entender-una-base-de-datos", "Módulo 4: Entender una base de datos", "Módulo 4"),
    5: ("05-seleccionar-y-filtrar-datos", "Módulo 5: Seleccionar y filtrar datos", "Módulo 5"),
    6: ("06-trabajar-cuando-faltan-datos", "Módulo 6: Trabajar cuando faltan datos", "Módulo 6"),
    7: ("07-describir-categorias", "Módulo 7: Describir categorías", "Módulo 7"),
    8: ("08-describir-cantidades", "Módulo 8: Describir cantidades", "Módulo 8"),
    9: ("09-ver-relaciones-entre-dos-cantidades", "Módulo 9: Ver relaciones entre dos cantidades", "Módulo 9"),
    10: ("10-elegir-y-evaluar-una-correlacion", "Módulo 10: Elegir y evaluar una correlación", "Módulo 10"),
    11: ("11-trabajar-con-varias-correlaciones", "Módulo 11: Trabajar con varias correlaciones", "Módulo 11"),
    12: ("12-relacionar-categorias", "Módulo 12: Relacionar categorías", "Módulo 12"),
    13: ("13-de-la-pregunta-al-analisis", "Módulo 13: De la pregunta al análisis", "Módulo 13"),
}


def clean_text(t: str) -> str:
    """Normalize text whitespace and strip leading/trailing spaces."""
    return re.sub(r"\r\n", "\n", t).strip()


def extract_code_block(text: str) -> str:
    """Extract code from ```r ... ``` or ``` ... ``` block, or return raw text."""
    m = re.search(r"```(?:r|text)?\s*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).rstrip()
    lines = [l for l in text.splitlines() if not l.startswith("#") and not l.startswith(">")]
    return "\n".join(lines).strip() if lines else text.strip()


def parse_module(filepath: Path) -> dict[str, Any]:
    content = filepath.read_text(encoding="utf-8")
    fname = filepath.name

    m_num_match = re.search(r"Módulo\s*(\d+)", content, re.I)
    m_num = int(m_num_match.group(1)) if m_num_match else 1

    h2 = re.search(r"^##\s*(.*?)$", content, re.M)
    title = h2.group(1).strip() if h2 else f"Módulo {m_num}"

    cap_d = re.search(r"### Capacidad después\s*\n(.*?)(?=\n###|\n#|\Z)", content, re.DOTALL)
    description = clean_text(cap_d.group(1)) if cap_d else ""

    hab_nuc = re.search(r"### Habilidades nucleares\s*\n(.*?)(?=\n###|\n#|\Z)", content, re.DOTALL)
    skills = []
    if hab_nuc:
        for line in hab_nuc.group(1).splitlines():
            line = line.strip()
            if line.startswith("- "):
                skills.append(line[2:].strip().rstrip(";."))

    raw_exs = re.split(r"\n##\s+(M\d+[-_]E\d+.*?)\n", content)
    exercises = []

    for i in range(1, len(raw_exs), 2):
        header = raw_exs[i].strip()
        body = raw_exs[i + 1]

        h_parts = re.split(r"\s*[—–-]\s*", header, maxsplit=1)
        code_id = h_parts[0].strip()
        ex_title = h_parts[1].strip() if len(h_parts) > 1 else header
        ex_num = len(exercises) + 1

        def get_sec(pat: str) -> str:
            m = re.search(pat, body, re.DOTALL)
            return clean_text(m.group(1)) if m else ""

        s1_role = get_sec(r"### 1\.\s*Rol[^\n]*\n(.*?)(?=\n###|\Z)")
        s3_cap_before = get_sec(r"### 3\.\s*Capacidad antes[^\n]*\n(.*?)(?=\n###|\Z)")
        s4_cap_after = get_sec(r"### 4\.\s*Capacidad después[^\n]*\n(.*?)(?=\n###|\Z)")
        s8_context = get_sec(r"### 8\.\s*Contexto sustantivo[^\n]*\n(.*?)(?=\n###|\Z)")
        s9_dataset = get_sec(r"### 9\.\s*Dataset[^\n]*\n(.*?)(?=\n###|\Z)")
        s10_text = get_sec(r"### 10\.\s*Texto para\s*(?:el\s*)?estudiante[^\n]*\n(.*?)(?=\n###|\Z)")
        s12_worked = get_sec(r"### 12\.\s*(?:Código trabajado|Representación)[^\n]*\n(.*?)(?=\n###|\Z)")
        s13_starter = get_sec(r"### 13\.\s*Starter[^\n]*\n(.*?)(?=\n###|\Z)")
        s14_action = get_sec(r"### 14\.\s*Acción esperada[^\n]*\n(.*?)(?=\n###|\Z)")
        s15_solution = get_sec(r"### 15\.\s*Solución canónica[^\n]*\n(.*?)(?=\n###|\Z)")
        s16_result = get_sec(r"### 16\.\s*Resultado esperado[^\n]*\n(.*?)(?=\n###|\Z)")
        s17_criteria = get_sec(r"### 17\.\s*Criterio[^\n]*\n(.*?)(?=\n###|\Z)")
        s19_error = get_sec(r"### 19\.\s*Error esperado[^\n]*\n(.*?)(?=\n###|\Z)")
        s20_feedback = get_sec(r"### 20\.\s*Feedback[^\n]*\n(.*?)(?=\n###|\Z)")
        s21_diag_feedback = get_sec(r"### 21\.\s*Feedback[^\n]*\n(.*?)(?=\n###|\Z)")
        s26_type = get_sec(r"### 26\.\s*Tipo de ejercicio[^\n]*\n(.*?)(?=\n###|\Z)")
        s33_notes = get_sec(r"### 33\.\s*Notas[^\n]*\n(.*?)(?=\n---|\n##|\Z)")

        hint_matches = re.finditer(r"### (?:2[2-9]|3[0-2])\.\s*Hint\s*(\d+)\s*\n(.*?)(?=\n###|\Z)", body, re.DOTALL)
        hints = []
        for hm in hint_matches:
            h_idx = int(hm.group(1))
            h_text = clean_text(hm.group(2))
            hints.append((h_idx, h_text))

        exercises.append({
            "code_id": code_id,
            "title": ex_title,
            "order": ex_num - 1,
            "s1_role": s1_role,
            "s3_cap_before": s3_cap_before,
            "s4_cap_after": s4_cap_after,
            "s8_context": s8_context,
            "s9_dataset": s9_dataset,
            "s10_text": s10_text,
            "s12_worked": s12_worked,
            "s13_starter": s13_starter,
            "s14_action": s14_action,
            "s15_solution": s15_solution,
            "s16_result": s16_result,
            "s17_criteria": s17_criteria,
            "s19_error": s19_error,
            "s20_feedback": s20_feedback,
            "s21_diag_feedback": s21_diag_feedback,
            "s26_type": s26_type,
            "s33_notes": s33_notes,
            "hints": hints,
        })

    return {
        "file": fname,
        "module_num": m_num,
        "title": title,
        "description": description,
        "skills": skills,
        "exercises": exercises,
    }

print("Loaded module generator functions.")
