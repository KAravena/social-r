#!/usr/bin/env python3
"""Regression and semantic validation tests for M05-E08 and all generated R checkers."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Locate Rscript
RSCRIPT = shutil.which("Rscript")
if not RSCRIPT:
    default_r = Path(r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe")
    if default_r.exists():
        RSCRIPT = str(default_r)

from engine.generator.build import load_exercises, load_challenges, grader_code


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


def evaluate_r_submission(ex: dict, user_code: str) -> dict:
    """Execute user_code in a clean R environment, then run ex grader_code, returning feedback dict."""
    if not RSCRIPT:
        raise unittest.SkipTest("Rscript executable not found")

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


class M05E08ValidatorRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = ROOT / "content" / "exercise.schema.json"
        content_dir = ROOT / "content"
        cls.exercises = load_exercises(content_dir, schema_path)
        cls.challenges = load_challenges(content_dir, schema_path)
        cls.ex_map = {x["id"]: x for x in cls.exercises}
        cls.ex_05_08 = cls.ex_map["intro-r-05-008"]

    def test_m05_e08_validator_parses(self):
        """Verify M05-E08 generated R checker parses without unrecognized escape or syntax error."""
        code = grader_code(self.ex_05_08)
        ok, err = parse_r_code(code)
        self.assertTrue(ok, f"M05-E08 validator failed to parse: {err}")
        # Ensure no unescaped regex escapes like single \s, \d, \w, \(
        unescaped_s = re.search(r"(?<!\\)\\s", code)
        self.assertIsNone(unescaped_s, "Generated R code must not contain unescaped \\s")

    def test_m05_e08_correct_solution_passes(self):
        """Verify canonical solution for M05-E08 passes grading."""
        code = 'datos_preparados <- encuesta_jovenes |>\n  filter(estudia == "Sí") |>\n  select(edad, comuna)'
        fb = evaluate_r_submission(self.ex_05_08, code)
        self.assertTrue(fb.get("correct"), f"Canonical solution failed: {fb}")
        self.assertEqual(fb.get("type"), "success")

    def test_m05_e08_spacing_variations_pass(self):
        """Verify formatting variations (spaces, newlines, pipe spacing) pass grading."""
        variations = [
            'datos_preparados <- encuesta_jovenes |> filter(estudia == "Sí") |> select(edad, comuna)',
            'datos_preparados <- encuesta_jovenes |>\n    filter(estudia == "Sí") |>\n    select(edad, comuna)',
            'datos_preparados   <-   encuesta_jovenes |> filter ( estudia == "Sí" ) |> select ( edad , comuna )',
        ]
        for var_code in variations:
            fb = evaluate_r_submission(self.ex_05_08, var_code)
            self.assertTrue(fb.get("correct"), f"Variation failed: {var_code}\nFeedback: {fb}")

    def test_m05_e08_wrong_solution_fails(self):
        """Verify wrong solutions fail cleanly with pedagogically appropriate guidance."""
        # A. Missing filter (keeps all 8 rows)
        wrong_filter = 'datos_preparados <- encuesta_jovenes |>\n  select(edad, comuna)'
        fb_a = evaluate_r_submission(self.ex_05_08, wrong_filter)
        self.assertFalse(fb_a.get("correct"))
        self.assertIn("filtrar", fb_a.get("message", "").lower())

        # B. Missing select (only filter)
        wrong_select = 'datos_preparados <- encuesta_jovenes |>\n  filter(estudia == "Sí")'
        fb_b = evaluate_r_submission(self.ex_05_08, wrong_select)
        self.assertFalse(fb_b.get("correct"))

        # C. Storing into wrong object name
        wrong_obj = 'otro_nombre <- encuesta_jovenes |>\n  filter(estudia == "Sí") |>\n  select(edad, comuna)'
        fb_c = evaluate_r_submission(self.ex_05_08, wrong_obj)
        self.assertFalse(fb_c.get("correct"))
        self.assertIn("datos_preparados", fb_c.get("message", ""))

        # D. Invalid R syntax
        invalid_r = 'datos_preparados <- encuesta_jovenes |> filter('
        fb_d = evaluate_r_submission(self.ex_05_08, invalid_r)
        self.assertFalse(fb_d.get("correct"))

    def test_other_affected_validators_parse(self):
        """Verify intro-r-10-008 and intro-r-13-005 generated R checkers parse cleanly."""
        for ex_id in ["intro-r-10-008", "intro-r-13-005"]:
            ex = self.ex_map[ex_id]
            code = grader_code(ex)
            ok, err = parse_r_code(code)
            self.assertTrue(ok, f"{ex_id} validator failed to parse: {err}")

    def test_all_generated_r_validators_parse(self):
        """Global scan: verify all 89 exercises and 13 challenges generate parseable R checkers in batch."""
        if not RSCRIPT:
            raise unittest.SkipTest("Rscript executable not found")

        all_items = self.exercises + self.challenges
        temp_dir = Path(tempfile.mkdtemp(prefix="social_r_checkers_"))

        try:
            for item in all_items:
                code = grader_code(item)
                f_path = temp_dir / f"{item['id']}.R"
                f_path.write_text(code, encoding="utf-8")

            runner_code = f"""
files <- list.files("{temp_dir.as_posix()}", pattern = "\\\\.R$", full.names = TRUE)
errors <- character()
for (f in files) {{
  id <- sub("\\\\.R$", "", basename(f))
  code_lines <- readLines(f, warn = FALSE, encoding = "UTF-8")
  code_text <- paste(code_lines, collapse = "\\n")
  res <- tryCatch(parse(text = code_text), error = function(e) conditionMessage(e))
  if (is.character(res)) {{
    errors <- c(errors, paste0(id, ": ", res))
  }}
}}
if (length(errors) > 0) {{
  cat("ERRORS:\\n", paste(errors, collapse = "\\n"), "\\n")
}} else {{
  cat("ALL_OK: ", length(files), "\\n")
}}
"""
            runner_file = temp_dir / "runner.R"
            runner_file.write_text(runner_code, encoding="utf-8")

            proc = subprocess.run([RSCRIPT, "--vanilla", str(runner_file)], capture_output=True, text=True, encoding="utf-8")
            out = proc.stdout.strip()
            self.assertIn("ALL_OK", out, f"Parse errors in batch scan:\n{out}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
