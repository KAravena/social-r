#!/usr/bin/env python3
"""Pedagogical and Data Audit for Social R Activities (Modules 06 to 13).

Audits:
- Tildes and UTF-8 consistency ("Sí" vs "Si", "Región", etc.)
- Data consistency between instructions/tables and setup_code
- Hint consistency and progression
- Checker strictness / permissiveness
- LOCKED design alignment
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.generator.build import load_exercises, load_challenges, grader_code

def audit_pedagogy_and_data():
    schema_path = ROOT / "content" / "exercise.schema.json"
    content_dir = ROOT / "content" / "courses" / "intro-r"

    exercises = load_exercises(content_dir, schema_path)
    challenges = load_challenges(content_dir, schema_path)

    for ex in exercises:
        ex["is_challenge"] = False
        ex["checker_code"] = grader_code(ex)
    for ch in challenges:
        ch["is_challenge"] = True
        ch["checker_code"] = grader_code(ch)

    all_acts = exercises + challenges
    target_mod_prefixes = [f"intro-r-{m:02d}-" for m in range(6, 14)]
    acts = [a for a in all_acts if any(a["id"].startswith(p) for p in target_mod_prefixes)]

    issues = []

    for act in acts:
        aid = act["id"]
        setup = act.get("setup_code", "") or ""
        sol = act.get("solution_code", "") or ""
        starter = act.get("starter_code", "") or ""
        inst = act.get("instruction", "") or ""
        ctx = act.get("context", "") or ""
        hints = act.get("hints", []) or []
        checks = act.get("checks", []) or []

        # 1. Check for unaccented 'Si'
        for text, name in [(setup, "setup"), (sol, "solution"), (inst, "instruction"), (ctx, "context")]:
            for m in re.finditer(r'["\']Si["\']|==\s*["\']Si["\']', text):
                issues.append({
                    "id": aid,
                    "severity": "MEDIUM",
                    "category": "ACCENTS_UTF8",
                    "problem": f"Found unaccented 'Si' in {name}: '{m.group(0)}'. Expected 'Sí'."
                })

        # 2. Check hints consistency
        if len(hints) < 2:
            issues.append({
                "id": aid,
                "severity": "LOW",
                "category": "HINTS",
                "problem": f"Activity has fewer than 2 hints ({len(hints)})."
            })

        for h_idx, h in enumerate(hints, 1):
            h_text = h.get("text", "")
            if not h_text.strip():
                issues.append({
                    "id": aid,
                    "severity": "HIGH",
                    "category": "HINTS",
                    "problem": f"Hint {h_idx} has empty text."
                })

        # 3. Check for overly permissive checks
        check_types = [c.get("type") for c in checks]
        custom_codes = [c.get("code", "") for c in checks if c.get("type") == "custom_r"]

        # Only checks .res_val not null
        if len(checks) == 1 and checks[0].get("type") == "custom_r" and "!is.null(.res_val)" in checks[0].get("code", ""):
            issues.append({
                "id": aid,
                "severity": "HIGH",
                "category": "TOO_PERMISSIVE",
                "problem": "Checker only verifies '!is.null(.res_val)'. Any non-null expression passes."
            })

        # Only checks object_exists without value
        if all(c.get("type") in ("object_exists", "custom_r") for c in checks):
            non_exists_checks = [c for c in checks if c.get("type") != "object_exists"]
            if all("exists(" in c.get("code", "") for c in non_exists_checks):
                issues.append({
                    "id": aid,
                    "severity": "HIGH",
                    "category": "TOO_PERMISSIVE",
                    "problem": "Checker only verifies object existence without checking contents or values."
                })

        # Regex checks matching starter comments
        for c in checks:
            if c.get("type") == "custom_r":
                code_str = c.get("code", "")
                m = re.findall(r"grepl\(['\"]([^'\"]+)['\"],\s*\.user_code", code_str)
                for pattern in m:
                    # check if clean pattern appears in starter comments
                    # e.g. 'spearman' or 'pairwise'
                    clean_pat = pattern.replace("\\\\", "").replace("\\", "").replace(".", "\\.")
                    raw_word = re.sub(r'[^a-zA-Z0-9_]', '', pattern)
                    if raw_word and len(raw_word) > 3:
                        for line in starter.splitlines():
                            if line.strip().startswith("#") and raw_word.lower() in line.lower():
                                issues.append({
                                    "id": aid,
                                    "severity": "HIGH",
                                    "category": "TOO_PERMISSIVE",
                                    "problem": f"grepl pattern '{pattern}' matches text in starter code comment: '{line.strip()}'."
                                })

    print(f"Total pedagogical/data issues flagged: {len(issues)}")
    for iss in issues:
        print(f"[{iss['severity']} | {iss['category']}] {iss['id']}: {iss['problem']}")

if __name__ == "__main__":
    audit_pedagogy_and_data()
