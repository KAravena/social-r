#!/usr/bin/env python3
"""Audit Engine for Social R Activities (Modules 06 to 13, and course-wide).

Performs clean-session cold-start, checker parsing, canonical execution,
result evaluation, and negative testing using the local R runtime.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.generator.build import load_exercises, load_challenges, grader_code

RSCRIPT = shutil.which("Rscript")
if not RSCRIPT:
    default_r = Path(r"C:\Program Files\R\R-4.6.1\bin\Rscript.exe")
    if default_r.exists():
        RSCRIPT = str(default_r)


R_RUNNER_TEMPLATE = r"""
options(warn = 1, encoding = "UTF-8")
args <- commandArgs(trailingOnly = TRUE)
json_file <- args[1]
runner_env <- new.env()
runner_env$out_file <- args[2]
runner_env$payload <- jsonlite::fromJSON(json_file, simplifyVector = FALSE)
runner_env$results <- list()
baseline_search <- search()

for (i in seq_along(runner_env$payload)) {
  # Strict reset of attached packages and global environment
  current_pkgs <- setdiff(search(), baseline_search)
  for (pkg in current_pkgs) {
    tryCatch(detach(pkg, character.only = TRUE, unload = TRUE, force = TRUE), error = function(e) NULL)
  }
  rm(list = setdiff(ls(globalenv(), all.names = TRUE), c("runner_env", "baseline_search", "i")), envir = globalenv())

  act <- runner_env$payload[[i]]
  act_id <- act$id
  setup_code <- act$setup_code
  solution_code <- act$solution_code
  checker_code <- act$checker_code
  starter_code <- act$starter_code

  res <- list(
    id = act_id,
    module = act$module,
    is_challenge = act$is_challenge,
    cold_start_pass = FALSE,
    cold_start_error = NULL,
    checker_parse_pass = FALSE,
    checker_parse_error = NULL,
    canonical_exec_pass = FALSE,
    canonical_exec_error = NULL,
    canonical_checker_pass = FALSE,
    canonical_checker_message = NULL,
    wrong_answer_pass = FALSE,
    wrong_answer_message = NULL,
    starter_wrong_pass = FALSE,
    starter_wrong_message = NULL
  )

  # 1. Parse checker
  chk_parse <- tryCatch({
    parse(text = checker_code)
    TRUE
  }, error = function(e) {
    conditionMessage(e)
  })

  if (isTRUE(chk_parse)) {
    res$checker_parse_pass <- TRUE
  } else {
    res$checker_parse_pass <- FALSE
    res$checker_parse_error <- as.character(chk_parse)
  }

  # 2. Cold-start setup in isolated environment
  setup_env <- new.env(parent = globalenv())
  setup_res <- tryCatch({
    if (!is.null(setup_code) && nchar(trimws(setup_code)) > 0) {
      eval(parse(text = setup_code), envir = setup_env)
    }
    TRUE
  }, error = function(e) {
    conditionMessage(e)
  })

  if (isTRUE(setup_res)) {
    res$cold_start_pass <- TRUE
  } else {
    res$cold_start_pass <- FALSE
    res$cold_start_error <- as.character(setup_res)
  }

  # 3. Canonical execution and checker evaluation
  if (isTRUE(res$cold_start_pass) && isTRUE(res$checker_parse_pass)) {
    exec_env <- new.env(parent = globalenv())
    if (!is.null(setup_code) && nchar(trimws(setup_code)) > 0) {
      eval(parse(text = setup_code), envir = exec_env)
    }

    # Run canonical solution
    sol_res <- tryCatch({
      user_exprs <- parse(text = solution_code)
      last_val <- NULL
      for (e_idx in seq_along(user_exprs)) {
        last_val <- eval(user_exprs[[e_idx]], envir = exec_env)
      }
      assign(".result", last_val, envir = exec_env)
      assign(".last_value", last_val, envir = exec_env)
      list(ok = TRUE, last_val = last_val)
    }, error = function(e) {
      list(ok = FALSE, error = conditionMessage(e))
    })

    if (isTRUE(sol_res$ok)) {
      res$canonical_exec_pass <- TRUE

      # Evaluate checker on canonical solution
      chk_eval_res <- tryCatch({
        chk_env <- new.env(parent = exec_env)
        assign(".envir_result", exec_env, envir = chk_env)
        assign(".target_env", exec_env, envir = chk_env)
        assign(".user_code", solution_code, envir = chk_env)
        assign(".checker_args", list(user_code = solution_code), envir = chk_env)
        fb <- eval(parse(text = checker_code), envir = chk_env)
        fb
      }, error = function(e) {
        list(correct = FALSE, message = paste("Checker crash:", conditionMessage(e)))
      })

      if (is.list(chk_eval_res) && isTRUE(chk_eval_res$correct)) {
        res$canonical_checker_pass <- TRUE
        res$canonical_checker_message <- chk_eval_res$message
      } else {
        res$canonical_checker_pass <- FALSE
        res$canonical_checker_message <- if (is.list(chk_eval_res)) chk_eval_res$message else as.character(chk_eval_res)
      }
    } else {
      res$canonical_exec_pass <- FALSE
      res$canonical_exec_error <- sol_res$error
    }

    # 4. Starter code test: should FAIL (student has not solved it yet)
    st_env <- new.env(parent = globalenv())
    if (!is.null(setup_code) && nchar(trimws(setup_code)) > 0) {
      eval(parse(text = setup_code), envir = st_env)
    }
    st_code <- if (!is.null(starter_code)) starter_code else ""
    tryCatch({
      st_exprs <- parse(text = st_code)
      st_last <- NULL
      for (ste in seq_along(st_exprs)) {
        st_last <- eval(st_exprs[[ste]], envir = st_env)
      }
      assign(".result", st_last, envir = st_env)
      assign(".last_value", st_last, envir = st_env)
    }, error = function(e) NULL)

    st_chk_res <- tryCatch({
      st_chk_env <- new.env(parent = st_env)
      assign(".envir_result", st_env, envir = st_chk_env)
      assign(".target_env", st_env, envir = st_chk_env)
      assign(".user_code", st_code, envir = st_chk_env)
      assign(".checker_args", list(user_code = st_code), envir = st_chk_env)
      eval(parse(text = checker_code), envir = st_chk_env)
    }, error = function(e) {
      list(correct = FALSE, crash = TRUE, message = conditionMessage(e))
    })

    if (is.list(st_chk_res) && isTRUE(st_chk_res$correct)) {
      res$starter_false_pass <- TRUE
      res$starter_feedback <- st_chk_res$message
    } else {
      res$starter_false_pass <- FALSE
      res$starter_feedback <- if (is.list(st_chk_res)) st_chk_res$message else as.character(st_chk_res)
    }

    # 5. Dummy wrong answer test (should fail cleanly without crash)
    wrong_env <- new.env(parent = globalenv())
    if (!is.null(setup_code) && nchar(trimws(setup_code)) > 0) {
      eval(parse(text = setup_code), envir = wrong_env)
    }
    wrong_code <- "dummy_incorrect_code <- 99999\n99999"
    tryCatch({
      w_exprs <- parse(text = wrong_code)
      w_last <- NULL
      for (we in seq_along(w_exprs)) {
        w_last <- eval(w_exprs[[we]], envir = wrong_env)
      }
      assign(".result", w_last, envir = wrong_env)
      assign(".last_value", w_last, envir = wrong_env)
    }, error = function(e) NULL)

    wrong_chk_res <- tryCatch({
      w_chk_env <- new.env(parent = wrong_env)
      assign(".envir_result", wrong_env, envir = w_chk_env)
      assign(".target_env", wrong_env, envir = w_chk_env)
      assign(".user_code", wrong_code, envir = w_chk_env)
      assign(".checker_args", list(user_code = wrong_code), envir = w_chk_env)
      eval(parse(text = checker_code), envir = w_chk_env)
    }, error = function(e) {
      list(correct = FALSE, crash = TRUE, message = conditionMessage(e))
    })

    if (is.list(wrong_chk_res) && !isTRUE(wrong_chk_res$correct) && !isTRUE(wrong_chk_res$crash)) {
      res$wrong_answer_pass <- TRUE
      res$wrong_answer_message <- wrong_chk_res$message
    } else {
      res$wrong_answer_pass <- FALSE
      res$wrong_answer_message <- if (is.list(wrong_chk_res)) paste(wrong_chk_res$message, if (isTRUE(wrong_chk_res$crash)) "[CRASH]" else "[FALSE PASS]") else as.character(wrong_chk_res)
    }
  }

  runner_env$results[[act_id]] <- res
}

jsonlite::write_json(runner_env$results, runner_env$out_file, auto_unbox = TRUE, pretty = TRUE)
"""


def load_all_activities(modules: list[int] | None = None) -> list[dict[str, Any]]:
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

    if modules is not None:
        target_mod_prefixes = [f"intro-r-{m:02d}-" for m in modules]
        all_acts = [a for a in all_acts if any(a["id"].startswith(p) for p in target_mod_prefixes)]

    return all_acts


def run_r_audit(activities: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not RSCRIPT:
        raise RuntimeError(f"Rscript not found. Looked for {RSCRIPT}")

    # Prepare payload
    payload = []
    for act in activities:
        payload.append({
            "id": act["id"],
            "module": act.get("module") or act.get("_module_id") or "",
            "is_challenge": act.get("is_challenge", False),
            "setup_code": act.get("setup_code", ""),
            "solution_code": act.get("solution_code", ""),
            "checker_code": act.get("checker_code", ""),
            "starter_code": act.get("starter_code", ""),
        })

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as pf:
        json.dump(payload, pf, ensure_ascii=False)
        payload_path = pf.name

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as rf:
        out_path = rf.name

    with tempfile.NamedTemporaryFile("w", suffix=".R", encoding="utf-8", delete=False) as sf:
        sf.write(R_RUNNER_TEMPLATE)
        script_path = sf.name

    try:
        proc = subprocess.run(
            [RSCRIPT, "--vanilla", script_path, payload_path, out_path],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if proc.returncode != 0:
            print("R runner stderr:", proc.stderr)
            print("R runner stdout:", proc.stdout)
            raise RuntimeError(f"R runner exited with code {proc.returncode}: {proc.stderr}")

        with open(out_path, "r", encoding="utf-8") as f:
            return json.load(f)
    finally:
        for p in (payload_path, out_path, script_path):
            try:
                os.remove(p)
            except OSError:
                pass


if __name__ == "__main__":
    target_modules = list(range(6, 14))
    print(f"Loading activities for modules {target_modules}...")
    acts = load_all_activities(target_modules)
    print(f"Found {len(acts)} activities ({sum(1 for a in acts if not a['is_challenge'])} regular, {sum(1 for a in acts if a['is_challenge'])} challenges).")
    print("Executing R audit suite...")
    results = run_r_audit(acts)

    cold_fails = [r for r in results.values() if not r["cold_start_pass"]]
    parse_fails = [r for r in results.values() if not r["checker_parse_pass"]]
    canon_exec_fails = [r for r in results.values() if not r["canonical_exec_pass"]]
    canon_chk_fails = [r for r in results.values() if not r["canonical_checker_pass"]]
    wrong_fails = [r for r in results.values() if not r["wrong_answer_pass"]]
    starter_false_passes = [r for r in results.values() if r.get("starter_false_pass")]

    print("\n" + "=" * 60)
    print(f"AUDIT RESULTS SUMMARY (Modules 06-13, {len(acts)} activities):")
    print(f"  Cold-start PASS: {len(acts) - len(cold_fails)} / {len(acts)}")
    print(f"  Checker parse PASS: {len(acts) - len(parse_fails)} / {len(acts)}")
    print(f"  Canonical execution PASS: {len(acts) - len(canon_exec_fails)} / {len(acts)}")
    print(f"  Canonical checker PASS: {len(acts) - len(canon_chk_fails)} / {len(acts)}")
    print(f"  Dummy wrong answer rejected: {len(acts) - len(wrong_fails)} / {len(acts)}")
    print(f"  Starter code correctly rejected: {len(acts) - len(starter_false_passes)} / {len(acts)}")
    print("=" * 60)

    if cold_fails:
        print("\n[!] Cold-start failures:")
        for cf in cold_fails:
            print(f"  - {cf['id']}: {cf['cold_start_error']}")

    if parse_fails:
        print("\n[!] Checker parse errors:")
        for pf in parse_fails:
            print(f"  - {pf['id']}: {pf['checker_parse_error']}")

    if canon_exec_fails:
        print("\n[!] Canonical execution failures:")
        for cef in canon_exec_fails:
            print(f"  - {cef['id']}: {cef['canonical_exec_error']}")

    if canon_chk_fails:
        print("\n[!] Canonical checker FAILURES (Critical):")
        for ccf in canon_chk_fails:
            print(f"  - {ccf['id']}: {ccf['canonical_checker_message']}")

    if starter_false_passes:
        print("\n[!] Starter code FALSE PASSES (Checker accepts starter code without doing the task):")
        for sfp in starter_false_passes:
            print(f"  - {sfp['id']}: {sfp.get('starter_feedback')}")

    if wrong_fails:
        print("\n[!] Negative test unexpected results on dummy wrong input:")
        for wf in wrong_fails:
            print(f"  - {wf['id']}: {wf['wrong_answer_message']}")
