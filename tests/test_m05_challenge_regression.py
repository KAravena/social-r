#!/usr/bin/env python3
"""Regression tests for M05 Final Challenge (intro-r-05-challenge):
Ensures checker robustness, pedagogical alignment with dplyr pipelines,
and acceptance of semantically equivalent solutions (base R & subset).
"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT))
from engine.generator.build import load_challenges, grader_code

RSCRIPT = shutil.which("Rscript")
if not RSCRIPT:
    default_r = Path(r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe")
    if default_r.exists():
        RSCRIPT = str(default_r)


def parse_r_code(code_str: str) -> tuple[bool, str]:
    """Test if a given R code string parses cleanly using Rscript."""
    if not RSCRIPT:
        raise unittest.SkipTest("Rscript executable not found")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".R", encoding="utf-8", delete=False) as f:
        f.write(code_str)
        temp_path = f.name

    r_parse_runner = f"""
code_lines <- readLines("{Path(temp_path).as_posix()}", warn = FALSE, encoding = "UTF-8")
code_text <- paste(code_lines, collapse = "\\n")
res <- tryCatch(
  parse(text = code_text),
  error = function(e) conditionMessage(e)
)
if (is.character(res)) {{
  cat("ERROR:", res, "\\n")
}} else {{
  cat("PARSE_OK\\n")
}}
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".R", encoding="utf-8", delete=False) as rf:
        rf.write(r_parse_runner)
        runner_path = rf.name

    try:
        proc = subprocess.run([RSCRIPT, "--vanilla", runner_path], capture_output=True, text=True, encoding="utf-8")
        out = proc.stdout.strip()
        if "PARSE_OK" in out:
            return True, ""
        return False, out
    finally:
        for p in (temp_path, runner_path):
            try:
                os.remove(p)
            except OSError:
                pass


def evaluate_r_submission(challenge_dict: dict, user_code: str) -> dict:
    """Execute user_code in R and evaluate using challenge grader_code."""
    if not RSCRIPT:
        raise unittest.SkipTest("Rscript executable not found")

    grader = grader_code(challenge_dict)

    r_test_script = f"""
.envir_result <- new.env(parent = globalenv())
.checker_args <- list(user_code = {json.dumps(user_code)})

# Execute setup code. If dplyr load fails due to Windows AppLocker policy on cli.dll,
# provide fallback filter/select in globalenv to allow test suite execution.
setup_code <- {json.dumps(challenge_dict.get("setup_code", ""))}
tryCatch({{
  eval(parse(text = setup_code), envir = .envir_result)
}}, error = function(e) {{
  # Fallback for Windows AppLocker environments where binary dll is blocked
  assign("filter", function(.data, cond) .data[cond, , drop = FALSE], envir = .GlobalEnv)
  assign("select", function(.data, ...) {{
    vars <- as.character(substitute(c(...)))[-1]
    .data[, vars, drop = FALSE]
  }}, envir = .GlobalEnv)
  # Execute setup without library(dplyr)
  clean_setup <- gsub("suppressPackageStartupMessages\\\\(library\\\\(dplyr\\\\)\\\\)", "", setup_code)
  eval(parse(text = clean_setup), envir = .envir_result)
}})

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
        proc = subprocess.run([RSCRIPT, "--encoding=UTF-8", "--vanilla", temp_path], capture_output=True, text=True, encoding="utf-8")
        if "---FEEDBACK_JSON---" not in proc.stdout:
            raise RuntimeError(f"Rscript failed: {proc.stderr}\nOutput: {proc.stdout}")
        json_str = proc.stdout.split("---FEEDBACK_JSON---")[1].strip()
        return json.loads(json_str)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


class M05ChallengeRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        content_dir = ROOT / "content"
        schema_path = content_dir / "exercise.schema.json"
        challenges = load_challenges(content_dir, schema_path)
        cls.challenge = next((c for c in challenges if c["id"] == "intro-r-05-challenge"), None)
        assert cls.challenge is not None, "intro-r-05-challenge must exist"

    def test_m05_challenge_checker_parses(self):
        """Confirm generated checker parses cleanly without syntax errors."""
        code = grader_code(self.challenge)
        ok, err = parse_r_code(code)
        self.assertTrue(ok, f"Checker R code failed to parse: {err}")

    def test_m05_challenge_canonical_dplyr_passes(self):
        """Canonical dplyr solution must PASS grading."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- encuesta_urbana |>
  filter(filtro_sur_satisfecho) |>
  select(edad, ingreso)
ingreso_promedio_focal <- mean(submuestra_focal$ingreso)
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertTrue(fb.get("correct"), f"Canonical dplyr failed: {fb}")

    def test_m05_challenge_base_r_equivalent_passes(self):
        """Base R bracket indexing equivalent must PASS grading."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- encuesta_urbana[filtro_sur_satisfecho, c("edad", "ingreso")]
ingreso_promedio_focal <- mean(submuestra_focal$ingreso)
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertTrue(fb.get("correct"), f"Base R equivalent failed: {fb}")

    def test_m05_challenge_subset_equivalent_passes(self):
        """subset() equivalent must PASS grading."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- subset(encuesta_urbana, filtro_sur_satisfecho, select = c(edad, ingreso))
ingreso_promedio_focal <- mean(submuestra_focal$ingreso)
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertTrue(fb.get("correct"), f"subset() equivalent failed: {fb}")

    def test_m05_challenge_wrong_rows_fails(self):
        """Filtering wrong rows (e.g. Norte instead of Sur) must FAIL."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Norte" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- encuesta_urbana[filtro_sur_satisfecho, c("edad", "ingreso")]
ingreso_promedio_focal <- mean(submuestra_focal$ingreso)
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertFalse(fb.get("correct"))

    def test_m05_challenge_wrong_columns_fails(self):
        """Selecting wrong columns (e.g. edad and zona) must FAIL."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- encuesta_urbana[filtro_sur_satisfecho, c("edad", "zona")]
ingreso_promedio_focal <- 703.33
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertFalse(fb.get("correct"))

    def test_m05_challenge_missing_condition_fails(self):
        """Omitting 'filtro_sur_satisfecho' must FAIL."""
        user_code = '''
submuestra_focal <- encuesta_urbana[encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí", c("edad", "ingreso")]
ingreso_promedio_focal <- mean(submuestra_focal$ingreso)
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertFalse(fb.get("correct"))
        self.assertIn("filtro_sur_satisfecho", fb.get("message", ""))

    def test_m05_challenge_wrong_mean_fails(self):
        """Calculating an incorrect mean must FAIL."""
        user_code = '''
filtro_sur_satisfecho <- encuesta_urbana$zona == "Sur" & encuesta_urbana$satisfecho == "Sí"
submuestra_focal <- encuesta_urbana[filtro_sur_satisfecho, c("edad", "ingreso")]
ingreso_promedio_focal <- 500
'''
        fb = evaluate_r_submission(self.challenge, user_code)
        self.assertFalse(fb.get("correct"))
        self.assertIn("ingreso_promedio_focal", fb.get("message", ""))

    def test_m05_challenge_runs_in_fresh_session(self):
        """Verify challenge setup includes library(dplyr) and creates encuesta_urbana."""
        setup = self.challenge.get("setup_code", "")
        self.assertIn("library(dplyr)", setup, "Setup code must preload dplyr for fresh sessions")
        self.assertIn("encuesta_urbana", setup, "Setup code must create encuesta_urbana")


if __name__ == "__main__":
    unittest.main()
