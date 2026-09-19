#!/usr/bin/env python3
"""Social R v0.3.3 Comprehensive 4x4 Matrix E2E Test Suite.
Tests Run Button, Ctrl+Enter, Submit Button, and Ctrl+Shift+Enter across ALL 4 Exercises.
"""
import json
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_matrix_tests():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    matrix_results = {}
    out_file = Path(__file__).resolve().parents[1] / "docs" / "test_results_v033.json"

    def record_matrix(ex_num, run_btn, ctrl_enter, submit_btn, ctrl_shift_enter):
        matrix_results[f"Exercise {ex_num}"] = {
            "Run Button": "PASS" if run_btn else "FAIL",
            "Ctrl+Enter": "PASS" if ctrl_enter else "FAIL",
            "Submit Button": "PASS" if submit_btn else "FAIL",
            "Ctrl+Shift+Enter": "PASS" if ctrl_shift_enter else "FAIL",
        }
        out_file.write_text(json.dumps(matrix_results, indent=2), encoding="utf-8")

    def set_editor_text_via_typing(ex_id, text):
        ex_el = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm_content = ex_el.find_element(By.CSS_SELECTOR, '.cm-content')
        cm_content.click()
        time.sleep(0.1)
        cm_content.send_keys(Keys.CONTROL, 'a')
        cm_content.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
        cm_content.send_keys(text)
        time.sleep(0.2)

    def trigger_shortcut(mode="run"):
        if mode == "run":
            driver.execute_script("""(() => {
              const target = document.activeElement || window;
              const evt = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                ctrlKey: true,
                bubbles: true,
                cancelable: true,
                composed: true
              });
              target.dispatchEvent(evt);
            })()""")
        elif mode == "submit":
            driver.execute_script("""(() => {
              const target = document.activeElement || window;
              const evt = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                ctrlKey: true,
                shiftKey: true,
                bubbles: true,
                cancelable: true,
                composed: true
              });
              target.dispatchEvent(evt);
            })()""")

    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        # Clear progress and ensure devMode is active
        driver.execute_script("""(() => {
          window.SocialR.progress.clearAll();
          window.SocialR.devMode = true;
          if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false);
        })()""")
        time.sleep(0.5)

        # -------------------------------------------------------------
        # EXERCISE 1 (intro-r-01-000)
        # -------------------------------------------------------------
        print("\n=== Testing Exercise 1 (intro-r-01-000) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.5)

        # 1A. Run Button Ex1 (18 + 12)
        set_editor_text_via_typing("intro-r-01-000", "18 + 12")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const btn = ex.querySelector('.sr-btn-run');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex1_run_btn = "> 18 + 12" in c_txt and "[1] 30" in c_txt
        print(f"1A Run Btn: {ex1_run_btn} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 1B. Ctrl+Enter Ex1 (18 + 13)
        set_editor_text_via_typing("intro-r-01-000", "18 + 13")
        trigger_shortcut("run")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex1_ctrl_enter = "> 18 + 13" in c_txt and "[1] 31" in c_txt
        print(f"1B Ctrl+Enter: {ex1_ctrl_enter} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 1C. Submit Button Ex1 (18 + 11 -> warning)
        set_editor_text_via_typing("intro-r-01-000", "18 + 11")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const btn = ex.querySelector('.sr-btn-submit');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-000').textContent;")
        ex1_submit_btn = "Revisa tu respuesta" in fb_txt and "30" in fb_txt
        print(f"1C Submit Btn: {ex1_submit_btn} | Feedback snippet: {fb_txt.strip()}", flush=True)

        # 1D. Ctrl+Shift+Enter Ex1 (18 + 12 -> success)
        set_editor_text_via_typing("intro-r-01-000", "18 + 12")
        trigger_shortcut("submit")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-000').textContent;")
        ex1_ctrl_shift_enter = "Correcto" in fb_txt
        print(f"1D Ctrl+Shift+Enter: {ex1_ctrl_shift_enter} | Feedback snippet: {fb_txt.strip()}", flush=True)

        record_matrix(1, ex1_run_btn, ex1_ctrl_enter, ex1_submit_btn, ex1_ctrl_shift_enter)

        # -------------------------------------------------------------
        # EXERCISE 2 (intro-r-01-001)
        # -------------------------------------------------------------
        print("\n=== Testing Exercise 2 (intro-r-01-001) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.6)

        # 2A. Run Button Ex2 (25 + 17)
        set_editor_text_via_typing("intro-r-01-001", "25 + 17")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const btn = ex.querySelector('.sr-btn-run');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_run_btn = "> 25 + 17" in c_txt and "[1] 42" in c_txt
        print(f"2A Run Btn: {ex2_run_btn} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 2B. Ctrl+Enter Ex2 (25 + 20)
        set_editor_text_via_typing("intro-r-01-001", "25 + 20")
        trigger_shortcut("run")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_ctrl_enter = "> 25 + 20" in c_txt and "[1] 45" in c_txt
        print(f"2B Ctrl+Enter: {ex2_ctrl_enter} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 2C. Submit Button Ex2 (25 + 10 -> warning)
        set_editor_text_via_typing("intro-r-01-001", "25 + 10")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const btn = ex.querySelector('.sr-btn-submit');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        ex2_submit_btn = "Revisa tu respuesta" in fb_txt and "42" in fb_txt
        print(f"2C Submit Btn: {ex2_submit_btn} | Feedback snippet: {fb_txt.strip()}", flush=True)

        # 2D. Ctrl+Shift+Enter Ex2 (25 + 17 -> success)
        set_editor_text_via_typing("intro-r-01-001", "25 + 17")
        trigger_shortcut("submit")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        ex2_ctrl_shift_enter = "Correcto" in fb_txt
        print(f"2D Ctrl+Shift+Enter: {ex2_ctrl_shift_enter} | Feedback snippet: {fb_txt.strip()}", flush=True)

        record_matrix(2, ex2_run_btn, ex2_ctrl_enter, ex2_submit_btn, ex2_ctrl_shift_enter)

        # -------------------------------------------------------------
        # EXERCISE 3 (intro-r-01-002)
        # -------------------------------------------------------------
        print("\n=== Testing Exercise 3 (intro-r-01-002) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.6)

        # 3A. Run Button Ex3 (100 + 20)
        set_editor_text_via_typing("intro-r-01-002", "100 + 20")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-002"]');
          const btn = ex.querySelector('.sr-btn-run');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_run_btn = "> 100 + 20" in c_txt and "[1] 120" in c_txt
        print(f"3A Run Btn: {ex3_run_btn} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 3B. Ctrl+Enter Ex3 (100 + 25)
        set_editor_text_via_typing("intro-r-01-002", "100 + 25")
        trigger_shortcut("run")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_ctrl_enter = "> 100 + 25" in c_txt and "[1] 125" in c_txt
        print(f"3B Ctrl+Enter: {ex3_ctrl_enter} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 3C. Submit Button Ex3 (numero_estudiantes <- 100 -> warning)
        set_editor_text_via_typing("intro-r-01-002", "numero_estudiantes <- 100")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-002"]');
          const btn = ex.querySelector('.sr-btn-submit');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-002').textContent;")
        ex3_submit_btn = "Revisa tu respuesta" in fb_txt and "120" in fb_txt
        print(f"3C Submit Btn: {ex3_submit_btn} | Feedback snippet: {fb_txt.strip()}", flush=True)

        # 3D. Ctrl+Shift+Enter Ex3 (numero_estudiantes <- 120 -> success)
        set_editor_text_via_typing("intro-r-01-002", "numero_estudiantes <- 120")
        trigger_shortcut("submit")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-002').textContent;")
        ex3_ctrl_shift_enter = "Correcto" in fb_txt
        print(f"3D Ctrl+Shift+Enter: {ex3_ctrl_shift_enter} | Feedback snippet: {fb_txt.strip()}", flush=True)

        record_matrix(3, ex3_run_btn, ex3_ctrl_enter, ex3_submit_btn, ex3_ctrl_shift_enter)

        # -------------------------------------------------------------
        # EXERCISE 4 (intro-r-01-003)
        # -------------------------------------------------------------
        print("\n=== Testing Exercise 4 (intro-r-01-003) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.6)

        # 4A. Run Button Ex4 (20.0 + 1.4)
        set_editor_text_via_typing("intro-r-01-003", "20.0 + 1.4")
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-003"]');
          const btn = ex.querySelector('.sr-btn-run');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex4_run_btn = "> 20.0 + 1.4" in c_txt and "[1] 21.4" in c_txt
        print(f"4A Run Btn: {ex4_run_btn} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 4B. Ctrl+Enter Ex4 (20.0 + 2.4)
        set_editor_text_via_typing("intro-r-01-003", "20.0 + 2.4")
        trigger_shortcut("run")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex4_ctrl_enter = "> 20.0 + 2.4" in c_txt and "[1] 22.4" in c_txt
        print(f"4B Ctrl+Enter: {ex4_ctrl_enter} | Output snippet: {c_txt[-60:].strip()}", flush=True)

        # 4C. Submit Button Ex4 (edad_promedio <- "21.4" -> info diagnostic)
        set_editor_text_via_typing("intro-r-01-003", 'edad_promedio <- "21.4"')
        driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-003"]');
          const btn = ex.querySelector('.sr-btn-submit');
          if (btn) btn.click();
        })()""")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-003').textContent;")
        ex4_submit_btn = "Nota" in fb_txt and "comillas" in fb_txt
        print(f"4C Submit Btn: {ex4_submit_btn} | Feedback snippet: {fb_txt.strip()}", flush=True)

        # 4D. Ctrl+Shift+Enter Ex4 (edad_promedio <- 21.4 -> success)
        set_editor_text_via_typing("intro-r-01-003", "edad_promedio <- 21.4")
        trigger_shortcut("submit")
        time.sleep(0.8)
        fb_txt = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-003').textContent;")
        ex4_ctrl_shift_enter = "Correcto" in fb_txt
        print(f"4D Ctrl+Shift+Enter: {ex4_ctrl_shift_enter} | Feedback snippet: {fb_txt.strip()}", flush=True)

        record_matrix(4, ex4_run_btn, ex4_ctrl_enter, ex4_submit_btn, ex4_ctrl_shift_enter)

        # -------------------------------------------------------------
        # BACK AND FORTH NAVIGATION RE-TEST
        # -------------------------------------------------------------
        print("\n=== Back and Forth Navigation Re-Test ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.4)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.4)
        set_editor_text_via_typing("intro-r-01-000", "99 + 1")
        trigger_shortcut("run")
        time.sleep(0.8)
        c_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        nav_retest_ok = "> 99 + 1" in c_txt and "[1] 100" in c_txt
        print(f"Back and Forth Navigation Re-Test: {'PASS' if nav_retest_ok else 'FAIL'}", flush=True)

    finally:
        driver.quit()

    total_pass = sum(1 for ex in matrix_results.values() for v in ex.values() if v == "PASS")
    print(f"\n=======================================================")
    print(f"FINAL MATRIX RESULTS: {total_pass}/16 PASSED")
    print(json.dumps(matrix_results, indent=2))
    print(f"=======================================================")
    if total_pass < 16:
        sys.exit(1)


if __name__ == "__main__":
    run_matrix_tests()
