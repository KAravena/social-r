#!/usr/bin/env python3
"""Social R v0.3.4 Full Verification Test Suite & Screenshot Generator."""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_v034_tests():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.4"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    summary = {}

    def type_code(ex_id, text):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        cm.click()
        time.sleep(0.2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
        time.sleep(0.3)

    def click_social_run(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        btn.click()
        time.sleep(1.0)

    def click_social_submit(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
        btn.click()
        time.sleep(1.2)

    def press_ctrl_enter():
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(1.0)

    def clear_console():
        driver.execute_script("if (window.SocialR.adapter) window.SocialR.adapter.clearConsole();")
        time.sleep(0.2)

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

        # -------------------------------------------------------------
        # 1. NATIVE QUARTO LIVE RUN GATE
        # -------------------------------------------------------------
        print("\n--- 1. NATIVE QUARTO LIVE RUN GATE ---", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.5)
        type_code("intro-r-01-001", "999 + 1")

        ex2_el = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-001"]')
        native_btn = ex2_el.find_element(By.CSS_SELECTOR, ".btn-exercise-editor.btn-primary, button[title*='Run']")
        native_btn.click()
        time.sleep(1.0)

        # Screenshot 01-native-run-ex2.png
        driver.save_screenshot(str(out_dir / "01-native-run-ex2.png"))
        print("  [OK] Saved 01-native-run-ex2.png", flush=True)

        native_out = ex2_el.find_element(By.CSS_SELECTOR, ".cell-output, .exercise-cell-output, .card-footer").text
        native_ok = "[1] 1000" in native_out or "1000" in native_out
        summary["NATIVE QUARTO LIVE RUN"] = "PASS" if native_ok else "FAIL"
        print(f"Native Quarto Live Run Ex2: {'PASS' if native_ok else 'FAIL'} | Output: {repr(native_out.strip())}", flush=True)

        # -------------------------------------------------------------
        # 2. SOCIAL R MOUSE RUN (999 + 1 -> [1] 1000)
        # -------------------------------------------------------------
        print("\n--- 2. SOCIAL R MOUSE RUN ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "999 + 1")
        click_social_run("intro-r-01-001")
        c2_mouse = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        mouse_run_ok = "> 999 + 1" in c2_mouse and "[1] 1000" in c2_mouse
        summary["SOCIAL R MOUSE RUN"] = "PASS" if mouse_run_ok else "FAIL"
        summary["MANUAL EX2 999+1 -> 1000"] = "PASS" if mouse_run_ok else "FAIL"
        print(f"Social R Mouse Run Ex2: {'PASS' if mouse_run_ok else 'FAIL'} | Console: {repr(c2_mouse[-80:].strip())}", flush=True)

        # Screenshot 02-social-run-ex2-1000.png
        driver.save_screenshot(str(out_dir / "02-social-run-ex2-1000.png"))
        print("  [OK] Saved 02-social-run-ex2-1000.png", flush=True)

        # -------------------------------------------------------------
        # 3. CTRL + ENTER RUN (731 + 184 -> [1] 915)
        # -------------------------------------------------------------
        print("\n--- 3. CTRL + ENTER RUN ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "731 + 184")
        press_ctrl_enter()
        c2_ctrl = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ctrl_run_ok = "> 731 + 184" in c2_ctrl and "[1] 915" in c2_ctrl
        summary["CTRL+ENTER RUN"] = "PASS" if ctrl_run_ok else "FAIL"
        summary["REAL R CONSOLE OUTPUT"] = "PASS" if ctrl_run_ok else "FAIL"
        print(f"Ctrl+Enter Run Ex2: {'PASS' if ctrl_run_ok else 'FAIL'} | Console: {repr(c2_ctrl[-80:].strip())}", flush=True)

        # Screenshot 03-ctrl-enter-ex2-915.png
        driver.save_screenshot(str(out_dir / "03-ctrl-enter-ex2-915.png"))
        print("  [OK] Saved 03-ctrl-enter-ex2-915.png", flush=True)

        # -------------------------------------------------------------
        # 4. EXERCISE 3 CTRL + ENTER (4321 + 1234 -> [1] 5555)
        # -------------------------------------------------------------
        print("\n--- 4. EXERCISE 3 CTRL + ENTER ---", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.5)
        clear_console()
        type_code("intro-r-01-002", "4321 + 1234")
        press_ctrl_enter()
        c3_ctrl = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_ok = "> 4321 + 1234" in c3_ctrl and "[1] 5555" in c3_ctrl
        print(f"Ex3 Ctrl+Enter (4321 + 1234): {'PASS' if ex3_ok else 'FAIL'} | Console: {repr(c3_ctrl[-80:].strip())}", flush=True)

        # Screenshot 04-ctrl-enter-ex3-5555.png
        driver.save_screenshot(str(out_dir / "04-ctrl-enter-ex3-5555.png"))
        print("  [OK] Saved 04-ctrl-enter-ex3-5555.png", flush=True)

        # -------------------------------------------------------------
        # 5. R ENVIRONMENT PERSISTENCE & ERRORS
        # -------------------------------------------------------------
        print("\n--- 5. R ENVIRONMENT PERSISTENCE & ERRORS ---", flush=True)
        clear_console()
        type_code("intro-r-01-002", "variable_inexistente")
        press_ctrl_enter()
        c_err = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        err_ok = "variable_inexistente" in c_err and "not found" in c_err.lower()
        print(f"Real R Error Test: {'PASS' if err_ok else 'FAIL'} | Console: {repr(c_err[-80:].strip())}", flush=True)

        # Screenshot 05-r-error-console.png
        driver.save_screenshot(str(out_dir / "05-r-error-console.png"))
        print("  [OK] Saved 05-r-error-console.png", flush=True)

        # Environment assignment test
        type_code("intro-r-01-002", "val_test <- 42")
        press_ctrl_enter()
        type_code("intro-r-01-002", "val_test")
        press_ctrl_enter()
        c_persist = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        persist_ok = "> val_test" in c_persist and "[1] 42" in c_persist
        summary["R ENVIRONMENT PERSISTENCE"] = "PASS" if persist_ok else "FAIL"
        print(f"R Environment Persistence Test: {'PASS' if persist_ok else 'FAIL'} | Console: {repr(c_persist[-80:].strip())}", flush=True)

        # -------------------------------------------------------------
        # 6. SUBMIT REGRESSION TEST
        # -------------------------------------------------------------
        print("\n--- 6. SUBMIT REGRESSION TEST ---", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.5)
        type_code("intro-r-01-001", "25 + 17")
        click_social_submit("intro-r-01-001")
        fb2 = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        submit_ok = "Correcto" in fb2 and "42" in fb2
        summary["SUBMIT REGRESSION"] = "PASS" if submit_ok else "FAIL"
        print(f"Submit Regression Ex2: {'PASS' if submit_ok else 'FAIL'} | Feedback: {repr(fb2.strip())}", flush=True)

        # Screenshot 06-submit-correct-feedback.png
        driver.save_screenshot(str(out_dir / "06-submit-correct-feedback.png"))
        print("  [OK] Saved 06-submit-correct-feedback.png", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("Social R v0.3.4 — FUNCTIONAL RECOVERY SUMMARY")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("=======================================================")

    all_pass = all(v == "PASS" for v in summary.values())
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    run_v034_tests()
