#!/usr/bin/env python3
"""Social R v0.3.3 HOTFIX Full 16/16 E2E Test Suite & Evidence Screenshot Generator."""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_full_hotfix_suite():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.3-hotfix"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    matrix = {}

    def type_and_trigger(ex_id, code_text, mode="run_key"):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        cm.click()
        time.sleep(0.2)

        # Clear and type using real ActionChains
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(code_text).perform()
        time.sleep(0.3)

        if mode == "run_key":
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        elif mode == "submit_key":
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        elif mode == "run_btn":
            btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
            btn.click()
        elif mode == "submit_btn":
            btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
            btn.click()

        time.sleep(0.8)

    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        driver.execute_script("""(() => {
          window.SocialR.progress.clearAll();
          window.SocialR.devMode = true;
          if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false);
        })()""")
        time.sleep(0.5)

        # =============================================================
        # EXERCISE 1 (intro-r-01-000)
        # =============================================================
        print("\n=== Testing Exercise 1 ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.4)

        # 1A Run Btn
        type_and_trigger("intro-r-01-000", "18 + 12", "run_btn")
        c1a = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex1_run_btn = "> 18 + 12" in c1a and "[1] 30" in c1a

        # 1B Ctrl+Enter
        type_and_trigger("intro-r-01-000", "18 + 13", "run_key")
        c1b = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex1_ctrl_enter = "> 18 + 13" in c1b and "[1] 31" in c1b

        # Screenshot Ex1
        driver.save_screenshot(str(out_dir / "01-ex1-keyboard-run.png"))
        print("  [OK] Saved 01-ex1-keyboard-run.png", flush=True)

        # 1C Submit Btn
        type_and_trigger("intro-r-01-000", "18 + 11", "submit_btn")
        fb1c = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-000').textContent;")
        ex1_submit_btn = "Revisa tu respuesta" in fb1c

        # 1D Ctrl+Shift+Enter
        type_and_trigger("intro-r-01-000", "18 + 12", "submit_key")
        fb1d = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-000').textContent;")
        ex1_ctrl_shift_enter = "Correcto" in fb1d

        matrix["Exercise 1"] = {
            "Run Button": "PASS" if ex1_run_btn else "FAIL",
            "Ctrl+Enter": "PASS" if ex1_ctrl_enter else "FAIL",
            "Submit Button": "PASS" if ex1_submit_btn else "FAIL",
            "Ctrl+Shift+Enter": "PASS" if ex1_ctrl_shift_enter else "FAIL",
        }

        # =============================================================
        # EXERCISE 2 (intro-r-01-001)
        # =============================================================
        print("\n=== Testing Exercise 2 ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.4)

        # 2A Run Btn
        type_and_trigger("intro-r-01-001", "25 + 17", "run_btn")
        c2a = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_run_btn = "> 25 + 17" in c2a and "[1] 42" in c2a

        # 2B Ctrl+Enter with 999 + 1 (SPECIAL MANDATORY TEST)
        type_and_trigger("intro-r-01-001", "999 + 1", "run_key")
        c2b = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_ctrl_enter = "> 999 + 1" in c2b and "[1] 1000" in c2b
        print(f"  2B Ctrl+Enter (999 + 1): {ex2_ctrl_enter} | Output snippet: {c2b[-60:].strip()}", flush=True)

        # Screenshot Ex2 with 999 + 1 and [1] 1000 in console!
        driver.save_screenshot(str(out_dir / "02-ex2-keyboard-run-1000.png"))
        print("  [OK] Saved 02-ex2-keyboard-run-1000.png", flush=True)

        # 2C Submit Btn
        type_and_trigger("intro-r-01-001", "25 + 10", "submit_btn")
        fb2c = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        ex2_submit_btn = "Revisa tu respuesta" in fb2c

        # 2D Ctrl+Shift+Enter
        type_and_trigger("intro-r-01-001", "25 + 17", "submit_key")
        fb2d = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        ex2_ctrl_shift_enter = "Correcto" in fb2d

        matrix["Exercise 2"] = {
            "Run Button": "PASS" if ex2_run_btn else "FAIL",
            "Ctrl+Enter": "PASS" if ex2_ctrl_enter else "FAIL",
            "Submit Button": "PASS" if ex2_submit_btn else "FAIL",
            "Ctrl+Shift+Enter": "PASS" if ex2_ctrl_shift_enter else "FAIL",
        }

        # =============================================================
        # EXERCISE 3 (intro-r-01-002)
        # =============================================================
        print("\n=== Testing Exercise 3 ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.4)

        # 3A Run Btn
        type_and_trigger("intro-r-01-002", "100 + 20", "run_btn")
        c3a = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_run_btn = "> 100 + 20" in c3a and "[1] 120" in c3a

        # 3B Ctrl+Enter with assignment and value lookup
        type_and_trigger("intro-r-01-002", "numero_estudiantes <- 120", "run_key")
        type_and_trigger("intro-r-01-002", "numero_estudiantes", "run_key")
        c3b = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_ctrl_enter = "> numero_estudiantes" in c3b and "[1] 120" in c3b

        # Screenshot Ex3
        driver.save_screenshot(str(out_dir / "03-ex3-keyboard-run.png"))
        print("  [OK] Saved 03-ex3-keyboard-run.png", flush=True)

        # 3C Submit Btn
        type_and_trigger("intro-r-01-002", "numero_estudiantes <- 100", "submit_btn")
        fb3c = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-002').textContent;")
        ex3_submit_btn = "Revisa tu respuesta" in fb3c

        # 3D Ctrl+Shift+Enter
        type_and_trigger("intro-r-01-002", "numero_estudiantes <- 120", "submit_key")
        fb3d = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-002').textContent;")
        ex3_ctrl_shift_enter = "Correcto" in fb3d

        matrix["Exercise 3"] = {
            "Run Button": "PASS" if ex3_run_btn else "FAIL",
            "Ctrl+Enter": "PASS" if ex3_ctrl_enter else "FAIL",
            "Submit Button": "PASS" if ex3_submit_btn else "FAIL",
            "Ctrl+Shift+Enter": "PASS" if ex3_ctrl_shift_enter else "FAIL",
        }

        # =============================================================
        # EXERCISE 4 (intro-r-01-003)
        # =============================================================
        print("\n=== Testing Exercise 4 ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.4)

        # 4A Run Btn
        type_and_trigger("intro-r-01-003", "20.0 + 1.4", "run_btn")
        c4a = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex4_run_btn = "> 20.0 + 1.4" in c4a and "[1] 21.4" in c4a

        # 4B Ctrl+Enter with assignment and value lookup
        type_and_trigger("intro-r-01-003", "edad_promedio <- 21.4", "run_key")
        type_and_trigger("intro-r-01-003", "edad_promedio", "run_key")
        c4b = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex4_ctrl_enter = "> edad_promedio" in c4b and "[1] 21.4" in c4b

        # Screenshot Ex4
        driver.save_screenshot(str(out_dir / "04-ex4-keyboard-run.png"))
        print("  [OK] Saved 04-ex4-keyboard-run.png", flush=True)

        # 4C Submit Btn
        type_and_trigger("intro-r-01-003", 'edad_promedio <- "21.4"', "submit_btn")
        fb4c = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-003').textContent;")
        ex4_submit_btn = "Nota" in fb4c

        # 4D Ctrl+Shift+Enter
        type_and_trigger("intro-r-01-003", "edad_promedio <- 21.4", "submit_key")
        fb4d = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-003').textContent;")
        ex4_ctrl_shift_enter = "Correcto" in fb4d

        matrix["Exercise 4"] = {
            "Run Button": "PASS" if ex4_run_btn else "FAIL",
            "Ctrl+Enter": "PASS" if ex4_ctrl_enter else "FAIL",
            "Submit Button": "PASS" if ex4_submit_btn else "FAIL",
            "Ctrl+Shift+Enter": "PASS" if ex4_ctrl_shift_enter else "FAIL",
        }

        # =============================================================
        # CYCLIC NAVIGATION RE-TEST: 1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1
        # =============================================================
        print("\n=== Cyclic Navigation Re-Test ===", flush=True)
        for idx in [0, 1, 2, 3, 2, 1, 0]:
            driver.execute_script(f"window.SocialR.navigation.setActiveIndex({idx});")
            time.sleep(0.2)

        type_and_trigger("intro-r-01-000", "77 + 33", "run_key")
        c_retest = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        retest_ok = "> 77 + 33" in c_retest and "[1] 110" in c_retest
        print(f"Cyclic Navigation Re-Test: {'PASS' if retest_ok else 'FAIL'}", flush=True)

    finally:
        driver.quit()

    total_pass = sum(1 for ex in matrix.values() for v in ex.values() if v == "PASS")
    print(f"\n=======================================================")
    print(f"HOTFIX MATRIX RESULTS: {total_pass}/16 PASSED")
    print(json.dumps(matrix, indent=2))
    print(f"=======================================================")

    if total_pass < 16 or not retest_ok:
        sys.exit(1)


if __name__ == "__main__":
    run_full_hotfix_suite()
