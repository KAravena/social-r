#!/usr/bin/env python3
"""Comprehensive Semantic Grader Verification for Module 6 (Social R Redesigned).

Executes the exact generated R grader code against user submissions using Rscript:
1. Validates success on canonical solutions for all 7 exercises (M6-E1 to M6-E7).
2. Validates diagnostic warnings on empty starter submissions.
3. Validates specific diagnostic guidance on typical student errors and anti-patterns.
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
corr_clean <- if (isTRUE(feedback$correct)) "true" else "false"
cat(sprintf('{{"correct": %s, "type": "%s", "message": "%s"}}\\n', corr_clean, typ_clean, msg_clean))
"""

    with tempfile.NamedTemporaryFile("w", suffix=".R", delete=False, encoding="utf-8") as tf:
        tf.write(r_test_script)
        tf_path = tf.name

    try:
        proc = subprocess.run(
            [RSCRIPT, "--vanilla", tf_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
        stdout = proc.stdout
        if "---FEEDBACK_JSON---" not in stdout:
            raise RuntimeError(f"Rscript failed without JSON: {proc.stderr}\nStdout: {stdout}")
        json_part = stdout.split("---FEEDBACK_JSON---")[1].strip()
        return json.loads(json_part)
    finally:
        if os.path.exists(tf_path):
            os.remove(tf_path)


class Module6SemanticGraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        content_dir = ROOT / "content"
        schema_path = ROOT / "content" / "exercise.schema.json"
        all_exercises = load_exercises(content_dir, schema_path)
        cls.m6_exercises = {
            ex["id"]: ex
            for ex in all_exercises
            if ex.get("_module_id") == "06-trabajar-cuando-faltan-datos"
        }

    def test_module_6_has_exactly_7_exercises(self):
        self.assertEqual(len(self.m6_exercises), 7)
        expected_ids = [
            "intro-r-06-001",
            "intro-r-06-002",
            "intro-r-06-003",
            "intro-r-06-004",
            "intro-r-06-005",
            "intro-r-06-006",
            "intro-r-06-007",
        ]
        self.assertEqual(list(self.m6_exercises.keys()), expected_ids)

    # --- M6-E1: El valor que no está ---
    def test_e1_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-001"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E1 failed on canonical solution: {res}")
        self.assertIn("información no está disponible", res["message"])

    def test_e1_starter_code_fails(self):
        ex = self.m6_exercises["intro-r-06-001"]
        res = evaluate_r_submission(ex, ex["starter_code"])
        self.assertFalse(res["correct"], "Starter code should not pass")

    def test_e1_wrong_replacement_with_zero(self):
        ex = self.m6_exercises["intro-r-06-001"]
        bad_code = "c(4, 0, 0, 12, 0)"
        res = evaluate_r_submission(ex, bad_code)
        self.assertFalse(res["correct"])

    # --- M6-E2: ¿Dónde falta información? ---
    def test_e2_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-002"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E2 failed on canonical solution: {res}")
        self.assertIn("TRUE", res["message"])

    def test_e2_starter_code_fails(self):
        ex = self.m6_exercises["intro-r-06-002"]
        res = evaluate_r_submission(ex, ex["starter_code"])
        self.assertFalse(res["correct"], "Starter code should not pass")

    # --- M6-E3: ¿Cuántos faltan y cuántos quedan? ---
    def test_e3_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-003"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E3 failed on canonical solution: {res}")
        self.assertIn("N disponible", res["message"])

    def test_e3_missing_disponibles(self):
        ex = self.m6_exercises["intro-r-06-003"]
        code = "faltan <- sum(is.na(horas_cuidado))"
        res = evaluate_r_submission(ex, code)
        self.assertFalse(res["correct"])
        self.assertIn("disponibles", res["message"])

    # --- M6-E4: Calcular con los datos disponibles ---
    def test_e4_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-004"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E4 failed on canonical solution: {res}")
        self.assertIn("na.rm = TRUE", res["message"])

    def test_e4_calculation_without_na_rm(self):
        ex = self.m6_exercises["intro-r-06-004"]
        code = "sum(horas_cuidado)"
        res = evaluate_r_submission(ex, code)
        self.assertFalse(res["correct"])
        self.assertIn("na.rm = TRUE", res["message"])

    # --- M6-E5: Casos completos e incompletos ---
    def test_e5_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-005"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E5 failed on canonical solution: {res}")
        self.assertIn("complete.cases()", res["message"])

    def test_e5_hardcoded_number_rejected(self):
        ex = self.m6_exercises["intro-r-06-005"]
        code = """
filas_completas <- c(TRUE, FALSE, FALSE, TRUE, FALSE)
total_completos <- 2
"""
        res = evaluate_r_submission(ex, code)
        self.assertFalse(res["correct"])
        self.assertIn("complete.cases", res["message"])

    # --- M6-E6: Diagnosticar antes de analizar ---
    def test_e6_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-006"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E6 failed on canonical solution: {res}")
        self.assertIn("información completa", res["message"])

    def test_e6_without_filtering_trabaja(self):
        ex = self.m6_exercises["intro-r-06-006"]
        code = """
datos_trabajan <- select(filter(encuesta_social_demo, trabaja == "No"), edad, horas_cuidado)
sum(complete.cases(datos_trabajan))
"""
        res = evaluate_r_submission(ex, code)
        self.assertFalse(res["correct"])
        self.assertIn("trabajan", res["message"])

    # --- M6-E7: Checkpoint B: Decidir frente a datos ausentes ---
    def test_e7_canonical_solution(self):
        ex = self.m6_exercises["intro-r-06-007"]
        res = evaluate_r_submission(ex, ex["solution_code"])
        self.assertTrue(res["correct"], f"E7 failed on canonical solution: {res}")
        self.assertIn("Checkpoint B", res["message"])

    def test_e7_without_participacion_na_rm(self):
        ex = self.m6_exercises["intro-r-06-007"]
        code = """
n_ausentes <- sum(is.na(encuesta_vecinal$participacion))
n_disponibles <- sum(!is.na(encuesta_vecinal$participacion))
total_participacion <- sum(encuesta_vecinal$participacion)
"""
        res = evaluate_r_submission(ex, code)
        self.assertFalse(res["correct"])
        self.assertIn("na.rm = TRUE", res["message"])


if __name__ == "__main__":
    unittest.main()
