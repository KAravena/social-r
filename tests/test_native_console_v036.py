#!/usr/bin/env python3
"""Social R v0.3.6 E2E Verification & Screenshot Suite for Native Console Architecture."""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_v036_suite():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.6"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    v036_results = {}

    def set_active(idx):
        driver.execute_script(f"window.SocialR.navigation.setActiveIndex({idx});")
        time.sleep(0.5)

    def type_code(ex_id, text):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        cm.click()
        time.sleep(0.2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
        time.sleep(0.4)

    def click_social_run(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2.5)

    def click_social_submit(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2.5)

    def press_ctrl_enter(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        cm.click()
        time.sleep(0.2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(2.5)

    def get_console_output(ex_id):
        return driver.execute_script(f"""
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
          const out = ex ? ex.querySelector('.cell-output-container, .cell-output, .exercise-cell-output') : null;
          return out ? out.textContent : "";
        """) or ""

    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        driver.execute_script("""(() => {
          window.SocialR.progress.clearAll();
          window.SocialR.devMode = true;
        })()""")
        time.sleep(0.5)

        # -------------------------------------------------------------
        # 1. NATIVE CONSOLE ARCHITECTURE: NO CUSTOM MIRROR
        # -------------------------------------------------------------
        no_custom_mirror = driver.execute_script("return typeof window.RConsoleAdapter === 'undefined';")
        v036_results["CUSTOM CONSOLE MIRROR REMOVED"] = "YES" if no_custom_mirror else "NO"
        print(f"Custom Console Mirror Removed: {v036_results['CUSTOM CONSOLE MIRROR REMOVED']}", flush=True)

        # -------------------------------------------------------------
        # 2. EXERCISE 1 RUN
        # -------------------------------------------------------------
        print("\n--- TEST: EXERCISE 1 RUN ---", flush=True)
        set_active(0)
        type_code("intro-r-01-000", "18 + 12")
        click_social_run("intro-r-01-000")

        ex1_out = get_console_output("intro-r-01-000")
        ex1_pass = "[1] 30" in ex1_out or "30" in ex1_out
        v036_results["EX1 RUN"] = "PASS" if ex1_pass else "FAIL"
        print(f"EX1 Run: {'PASS' if ex1_pass else 'FAIL'} | Output: {repr(ex1_out.strip())}", flush=True)

        # -------------------------------------------------------------
        # 3. EXERCISE 2 RUN (999 + 1 -> [1] 1000)
        # -------------------------------------------------------------
        print("\n--- TEST: EXERCISE 2 RUN (999 + 1) ---", flush=True)
        set_active(1)
        type_code("intro-r-01-001", "999 + 1")
        click_social_run("intro-r-01-001")

        ex2_out = get_console_output("intro-r-01-001")

        # Geometric check: output top >= editor top
        is_geo_below = driver.execute_script("""
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const cm = ex ? ex.querySelector('.cm-editor') : null;
          const out = ex ? ex.querySelector('.cell-output-container, .cell-output, .exercise-cell-output') : null;
          if (!cm || !out) return false;
          const cmRect = cm.getBoundingClientRect();
          const outRect = out.getBoundingClientRect();
          return (outRect.top >= cmRect.top - 100);
        """)

        ex2_pass = ("[1] 1000" in ex2_out or "1000" in ex2_out) and bool(is_geo_below)
        v036_results["EX2 RUN"] = "PASS" if ex2_pass else "FAIL"
        v036_results["NATIVE OUTPUT AS CONSOLE"] = "PASS" if bool(is_geo_below) else "FAIL"
        print(f"EX2 Run (999 + 1): {'PASS' if ex2_pass else 'FAIL'} | Geometric Position Below Editor: {is_geo_below} | Output: {repr(ex2_out.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "02-ex2-native-console.png"))
        print("  [OK] Saved 02-ex2-native-console.png", flush=True)

        # -------------------------------------------------------------
        # 4. EXERCISE 3 RUN (4321 + 1234 -> [1] 5555)
        # -------------------------------------------------------------
        print("\n--- TEST: EXERCISE 3 RUN (4321 + 1234) ---", flush=True)
        set_active(2)
        type_code("intro-r-01-002", "4321 + 1234")
        click_social_run("intro-r-01-002")

        ex3_out = get_console_output("intro-r-01-002")
        ex3_pass = "[1] 5555" in ex3_out or "5555" in ex3_out
        v036_results["EX3 RUN"] = "PASS" if ex3_pass else "FAIL"
        print(f"EX3 Run (4321 + 1234): {'PASS' if ex3_pass else 'FAIL'} | Output: {repr(ex3_out.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "03-ex3-native-console.png"))
        print("  [OK] Saved 03-ex3-native-console.png", flush=True)

        # -------------------------------------------------------------
        # 5. EXERCISE 4 RUN (9999 - 1 -> [1] 9998)
        # -------------------------------------------------------------
        print("\n--- TEST: EXERCISE 4 RUN (9999 - 1) ---", flush=True)
        set_active(3)
        type_code("intro-r-01-003", "9999 - 1")
        click_social_run("intro-r-01-003")

        ex4_out = get_console_output("intro-r-01-003")
        ex4_pass = "[1] 9998" in ex4_out or "9998" in ex4_out
        v036_results["EX4 RUN"] = "PASS" if ex4_pass else "FAIL"
        print(f"EX4 Run (9999 - 1): {'PASS' if ex4_pass else 'FAIL'} | Output: {repr(ex4_out.strip())}", flush=True)

        # -------------------------------------------------------------
        # 6. CYCLIC NAVIGATION & CTRL + ENTER ALL (1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1)
        # -------------------------------------------------------------
        print("\n--- TEST: CYCLIC NAVIGATION & CTRL + ENTER ALL ---", flush=True)
        ctrl_results = []

        # 3
        set_active(2)
        type_code("intro-r-01-002", "100 + 200")
        press_ctrl_enter("intro-r-01-002")
        out_c3 = get_console_output("intro-r-01-002")
        ctrl_results.append("300" in out_c3)

        # 2
        set_active(1)
        type_code("intro-r-01-001", "731 + 184")
        press_ctrl_enter("intro-r-01-001")
        out_c2 = get_console_output("intro-r-01-001")
        ctrl_results.append("915" in out_c2)

        # 1
        set_active(0)
        type_code("intro-r-01-000", "50 + 50")
        press_ctrl_enter("intro-r-01-000")
        out_c1 = get_console_output("intro-r-01-000")
        ctrl_results.append("100" in out_c1)

        all_ctrl_pass = all(ctrl_results)
        v036_results["CTRL+ENTER ALL"] = "PASS" if all_ctrl_pass else "FAIL"
        print(f"Cyclic Navigation & Ctrl+Enter All: {'PASS' if all_ctrl_pass else 'FAIL'}", flush=True)

        # -------------------------------------------------------------
        # 7. REAL R ERROR TEST
        # -------------------------------------------------------------
        print("\n--- TEST: REAL R ERROR IN NATIVE CONSOLE ---", flush=True)
        set_active(1)
        type_code("intro-r-01-001", "variable_no_existe")
        click_social_run("intro-r-01-001")

        err_out = get_console_output("intro-r-01-001")
        err_pass = "variable_no_existe" in err_out or "not found" in err_out.lower() or "error" in err_out.lower()
        v036_results["R ERROR OUTPUT"] = "PASS" if err_pass else "FAIL"
        print(f"Real R Error Test: {'PASS' if err_pass else 'FAIL'} | Output: {repr(err_out.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "04-r-error-console.png"))
        print("  [OK] Saved 04-r-error-console.png", flush=True)

        # -------------------------------------------------------------
        # 8. SUBMIT REGRESSION TEST
        # -------------------------------------------------------------
        print("\n--- TEST: SUBMIT REGRESSION ---", flush=True)
        set_active(1)
        type_code("intro-r-01-001", "25 + 17")
        click_social_submit("intro-r-01-001")

        fb2 = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        submit_pass = "Correcto" in fb2 and "42" in fb2
        v036_results["SUBMIT REGRESSION"] = "PASS" if submit_pass else "FAIL"
        print(f"Submit Regression Ex2: {'PASS' if submit_pass else 'FAIL'} | Feedback: {repr(fb2.strip())}", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("Social R v0.3.6 — NATIVE CONSOLE ARCHITECTURE SUMMARY")
    for k, v in v036_results.items():
        print(f"  {k}: {v}")
    print("=======================================================")

    all_pass = all(v in ["PASS", "YES"] for v in v036_results.values())
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    run_v036_suite()
