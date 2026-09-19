#!/usr/bin/env python3
"""Social R v0.3.2 End-to-End Test Suite - 3-Channel Isolation & Console Fidelity."""
import json
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_e2e():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    results = []
    out_file = Path(__file__).resolve().parents[1] / "docs" / "test_results_v032.json"

    def record(name, status, detail=""):
        res = {"step": name, "passed": bool(status), "detail": str(detail)}
        results.append(res)
        out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"[{'PASS' if status else 'FAIL'}] {name}: {detail}", flush=True)

    try:
        url = "http://127.0.0.1:4200/"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        # Clear progress store
        driver.execute_script("""(() => {
          window.SocialR.progress.clearAll();
          if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false);
        })()""")
        time.sleep(0.5)

        # 1. webR Status
        status_text = driver.execute_script("return (() => (document.getElementById('sr-webr-status-text') || {}).textContent || '')()")
        record("webR Status is R listo", "R listo" in status_text, status_text)

        # 2. Exploratory Run with 18 + 11
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 11";
        })()""")
        
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        console_text = driver.execute_script("return (() => (document.getElementById('sr-console-body') || {}).textContent || '')()")
        record("Run 18 + 11 produces [1] 29 in console", "[1] 29" in console_text, console_text[-60:])

        # Strict Editor Output Isolation Assertions
        editor_text = driver.execute_script("return (() => (document.querySelector('.social-r-exercise[data-exercise-id=\"intro-r-01-000\"] .sr-editor-body') || {}).innerText || '')()")
        record("Editor DOES NOT contain [1] 29 output", "[1] 29" not in editor_text, "Editor text clean")
        record("Editor DOES NOT contain grading feedback", "Correcto" not in editor_text and "Revisa" not in editor_text, "Editor feedback clean")

        # 3. Authentic R Assignment Fidelity (numero_estudiantes <- 120 outputs nothing extra)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "numero_estudiantes <- 120";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        console_text_assign = driver.execute_script("return (() => (document.getElementById('sr-console-body') || {}).textContent || '')()")
        record("Assignment run shows prompt > numero_estudiantes <- 120", "> numero_estudiantes <- 120" in console_text_assign, console_text_assign[-80:])
        record("Assignment run DOES NOT print fake [1] 120", "[1] 120" not in console_text_assign, "Authentic R behavior respected")

        # Now evaluate variable
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "numero_estudiantes";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        console_text_var = driver.execute_script("return (() => (document.getElementById('sr-console-body') || {}).textContent || '')()")
        record("Evaluating variable produces [1] 120 in console", "[1] 120" in console_text_var, console_text_var[-60:])

        # 4. Error Handling in Console
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "objeto_inexistente";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        console_text3 = driver.execute_script("return (() => (document.getElementById('sr-console-body') || {}).textContent || '')()")
        record("Run handles R runtime error in console without crash", "objeto_inexistente" in console_text3 and "not found" in console_text3, console_text3[-80:])

        # 5. Evaluative Submit (18 + 11) -> Left Panel Feedback Card
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 11";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        fb_cls0 = driver.execute_script("return (() => (document.getElementById('sr-feedback-card-intro-r-01-000') || {}).className || '')()")
        fb_txt0 = driver.execute_script("return (() => (document.getElementById('sr-feedback-card-intro-r-01-000') || {}).textContent || '')()")
        record("Submit 18 + 11 produces warning feedback in left panel", "is-warning" in fb_cls0 and "30" in fb_txt0, fb_txt0)

        # 6. Evaluative Submit (18 + 12) -> Success Feedback
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 12";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)

        fb_cls0_ok = driver.execute_script("return (() => (document.getElementById('sr-feedback-card-intro-r-01-000') || {}).className || '')()")
        record("Submit 18 + 12 produces success feedback in left panel", "is-success" in fb_cls0_ok, fb_cls0_ok)

        pct0 = driver.execute_script("return (() => (document.getElementById('sr-progress-pct') || {}).textContent || '')()")
        record("Ex0 completion updates progress to 25% completado", "25%" in pct0, pct0)

        # 7. Navigation & Progressive Hints Ex 1
        driver.execute_script("(() => { window.SocialR.navigation.next(); })()")
        time.sleep(0.3)
        cur_id1 = driver.execute_script("return (() => window.SocialR.navigation.getCurrentExercise().id)()")
        record("Navigate to Exercise 1", cur_id1 == "intro-r-01-001", cur_id1)

        # Complete Ex 1
        driver.execute_script("""(() => {
          const ex1 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const cmContent = ex1.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "25 + 17";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-001');
        })()""")
        time.sleep(0.8)

        pct1 = driver.execute_script("return (() => (document.getElementById('sr-progress-pct') || {}).textContent || '')()")
        record("Ex1 completion updates progress to 50% completado", "50%" in pct1, pct1)

        # 8. Exercise 2: Object Creation
        driver.execute_script("(() => { window.SocialR.navigation.next(); })()")
        time.sleep(0.3)

        driver.execute_script("""(() => {
          const ex2 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-002"]');
          const cmContent = ex2.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "numero_estudiantes <- 120";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-002');
        })()""")
        time.sleep(0.8)

        pct2 = driver.execute_script("return (() => (document.getElementById('sr-progress-pct') || {}).textContent || '')()")
        record("Ex2 completion updates progress to 75% completado", "75%" in pct2, pct2)

        # 9. Exercise 3: Types Diagnostic & Completion
        driver.execute_script("(() => { window.SocialR.navigation.next(); })()")
        time.sleep(0.3)

        driver.execute_script("""(() => {
          const ex3 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-003"]');
          const cmContent = ex3.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "edad_promedio <- 21.4";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-003');
        })()""")
        time.sleep(0.8)

        pct3 = driver.execute_script("return (() => (document.getElementById('sr-progress-pct') || {}).textContent || '')()")
        record("Ex3 completion updates progress to 100% completado", "100%" in pct3, pct3)

        # 10. Persistence across F5 Reload
        driver.get(url)
        time.sleep(2.0)

        all_p = driver.execute_script("return (() => window.SocialR.progress.getAll())()")
        all_completed = all(all_p.get(f"intro-r-01-00{i}", {}).get("status") == "completed" for i in range(4))
        record("Persistence across page refresh (all 4 completed)", all_completed, str(all_p))

        pct_reload = driver.execute_script("return (() => (document.getElementById('sr-progress-pct') || {}).textContent || '')()")
        record("Overall course progress shows 100% post-reload", "100%" in pct_reload, pct_reload)

    finally:
        driver.quit()

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    print(f"\nSummary: {passed_count}/{total_count} assertions passed.", flush=True)
    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    run_e2e()
