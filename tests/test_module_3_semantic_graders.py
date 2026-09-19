#!/usr/bin/env python3
"""Comprehensive Semantic Grader Verification for Module 3 (Social R v0.4 Canonical Locked).

Executes the exact generated R grader code against user submissions using Rscript:
1. Validates success on canonical solutions for all 7 canonical exercises.
2. Validates diagnostic warnings on empty submissions.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RSCRIPT = r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe"

from engine.generator.build import load_exercises, grader_code


def evaluate_r_submission(ex: dict, user_code: str) -> dict:
    """Execute user_code in a clean R environment, then run ex grader_code, returning feedback dict."""
    grader = grader_code(ex)

    # Wrap inside an R evaluation script
    r_test_script = f"""
.envir_result <- new.env(parent = globalenv())
.checker_args <- list(user_code = {json.dumps(user_code)})

# Execute setup code if present
setup_code <- {json.dumps(ex.get("setup_code", ""))}
if (nchar(trimws(setup_code)) > 0) {{
  eval(parse(text = setup_code), envir = .envir_result)
}}

# Execute user code in .envir_result
.user_exprs <- tryCatch(parse(text = {json.dumps(user_code)}), error = function(e) e)
.res_val <- NULL
if (inherits(.user_exprs, "error")) {{
  .res_val <- NULL
}} else {{
  for (i in seq_along(.user_exprs)) {{
    .res_val <- eval(.user_exprs[[i]], envir = .envir_result)
  }}
}}
assign(".result", .res_val, envir = .envir_result)
assign(".last_value", .res_val, envir = .envir_result)

# Run grader
{grader}

# Serialize feedback to JSON
cat("\\n---FEEDBACK_JSON---\\n")
msg_clean <- if (!is.null(feedback$message)) as.character(feedback$message) else ""
msg_clean <- gsub("\\\\", "\\\\\\\\", msg_clean, fixed = TRUE)
msg_clean <- gsub('"', '\\\\"', msg_clean, fixed = TRUE)
msg_clean <- gsub("\r?\n", "\\\\n", msg_clean)
typ_clean <- if (!is.null(feedback$type)) as.character(feedback$type) else "info"
corr_clean <- if (!is.null(feedback$correct) && isTRUE(feedback$correct)) "true" else "false"
cat(paste0('{{"correct": ', corr_clean, ', "type": "', typ_clean, '", "message": "', msg_clean, '"}}'))
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".R", encoding="utf-8", delete=False) as f:
        f.write(r_test_script)
        temp_path = f.name

    try:
        cmd = [RSCRIPT, "--encoding=UTF-8", "--vanilla", temp_path]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if "---FEEDBACK_JSON---" not in proc.stdout:
            raise RuntimeError(f"Rscript failed: {proc.stderr}\nOutput: {proc.stdout}")

        json_str = proc.stdout.split("---FEEDBACK_JSON---")[1].strip()
        try:
            return json.loads(json_str)
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON '{json_str}'\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}") from e
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


class Module3SemanticGraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = ROOT / "content" / "exercise.schema.json"
        content_dir = ROOT / "content"
        cls.exercises = load_exercises(content_dir, schema_path)
        cls.m3_map = {x["id"]: x for x in cls.exercises if x["_module_id"] == "03-hacer-preguntas-a-los-datos"}

    def test_module_3_has_exactly_7_exercises(self):
        self.assertEqual(len(self.m3_map), 7, f"Expected 7 exercises in Module 3, found {len(self.m3_map)}")

    def test_e1_canonical_solution(self):
        ex = self.m3_map["intro-r-03-001"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e2_canonical_solution(self):
        ex = self.m3_map["intro-r-03-002"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e3_canonical_solution(self):
        ex = self.m3_map["intro-r-03-003"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e4_canonical_solution(self):
        ex = self.m3_map["intro-r-03-004"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e5_canonical_solution(self):
        ex = self.m3_map["intro-r-03-005"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e6_canonical_solution(self):
        ex = self.m3_map["intro-r-03-006"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e7_canonical_solution(self):
        ex = self.m3_map["intro-r-03-007"]
        fb = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(fb["correct"])
        self.assertEqual(fb["type"], "success")

    def test_e1_empty_diagnostic(self):
        ex = self.m3_map["intro-r-03-001"]
        fb = evaluate_r_submission(ex, "")
        self.assertFalse(fb["correct"])
        self.assertIn(fb["type"], ["info", "warning"])


if __name__ == "__main__":
    unittest.main()
