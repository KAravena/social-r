#!/usr/bin/env python3
"""Social R v0.3.5 E2E Verification & Screenshot Suite for Real R Console."""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_v035_suite():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.5"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    v035_results = {}

    def type_code(ex_id, text):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        cm.click()
        time.sleep(0.2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
        time.sleep(0.3)

    def click_run(ex_id):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        btn.click()
        time.sleep(1.0)

    def click_submit(ex_id):
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
          if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(1, false);
        })()""")
        time.sleep(0.5)

        # 0. Save 01-console-empty.png
        driver.save_screenshot(str(out_dir / "01-console-empty.png"))
        print("  [OK] Saved 01-console-empty.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 1: Ex 2 (999 + 1) -> R Console has > 999 + 1 and [1] 1000
        # -------------------------------------------------------------
        print("\n--- E2E TEST 1: Mouse Run 999 + 1 ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "999 + 1")
        click_run("intro-r-01-001")

        console_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        top_native_visible = driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const out = ex.querySelector('.cell-output, .card-footer');
          if (!out) return false;
          const style = window.getComputedStyle(out);
          return style.display !== 'none' && style.visibility !== 'hidden';
        })()""")

        t1_ok = "> 999 + 1" in console_txt and "[1] 1000" in console_txt and not top_native_visible
        v035_results["REAL R OUTPUT -> CONSOLE"] = "PASS" if t1_ok else "FAIL"
        v035_results["TOP NATIVE OUTPUT HIDDEN"] = "PASS" if not top_native_visible else "FAIL"
        print(f"Test 1 Real Output in Console: {'PASS' if t1_ok else 'FAIL'} | Top Output Visible: {top_native_visible}", flush=True)

        # 02-run-25-17-console.png (Re-run 25 + 17 for explicit screenshot 02)
        type_code("intro-r-01-001", "25 + 17")
        click_run("intro-r-01-001")
        driver.save_screenshot(str(out_dir / "02-run-25-17-console.png"))
        print("  [OK] Saved 02-run-25-17-console.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 2: Ctrl+Enter Arithmetic (483 + 217) -> [1] 700
        # -------------------------------------------------------------
        print("\n--- E2E TEST 2: Ctrl+Enter Arithmetic ---", flush=True)
        type_code("intro-r-01-001", "483 + 217")
        press_ctrl_enter()

        c_hist = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t2_ok = "> 483 + 217" in c_hist and "[1] 700" in c_hist
        v035_results["CONSOLE HISTORY"] = "PASS" if t2_ok else "FAIL"
        print(f"Test 2 History & Ctrl+Enter: {'PASS' if t2_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "03-history-console.png"))
        print("  [OK] Saved 03-history-console.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 3: Assignments (social_r_test <- 12345 -> then query social_r_test)
        # -------------------------------------------------------------
        print("\n--- E2E TEST 3: Assignments & Environment ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "social_r_test <- 12345")
        click_run("intro-r-01-001")

        c_assign1 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        assign_no_extra_val = "[1] 12345" not in c_assign1

        type_code("intro-r-01-001", "social_r_test")
        click_run("intro-r-01-001")

        c_assign2 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t3_ok = assign_no_extra_val and "> social_r_test" in c_assign2 and "[1] 12345" in c_assign2
        v035_results["R ENVIRONMENT"] = "PASS" if t3_ok else "FAIL"
        print(f"Test 3 Assignment & Environment: {'PASS' if t3_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "04-assignment-console.png"))
        print("  [OK] Saved 04-assignment-console.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 4: Real R Errors (social_r_variable_that_does_not_exist)
        # -------------------------------------------------------------
        print("\n--- E2E TEST 4: Real R Errors ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "social_r_variable_that_does_not_exist")
        click_run("intro-r-01-001")

        c_err = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t4_ok = "social_r_variable_that_does_not_exist" in c_err and "not found" in c_err.lower()
        v035_results["R ERRORS"] = "PASS" if t4_ok else "FAIL"
        print(f"Test 4 Real R Error: {'PASS' if t4_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "05-r-error-console.png"))
        print("  [OK] Saved 05-r-error-console.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 5: R Warnings (sqrt(-1))
        # -------------------------------------------------------------
        print("\n--- E2E TEST 5: R Warnings ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "sqrt(-1)")
        click_run("intro-r-01-001")

        c_warn = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t5_ok = "NaN" in c_warn or "warning" in c_warn.lower()
        v035_results["R WARNINGS"] = "PASS" if t5_ok else "FAIL"
        print(f"Test 5 Real R Warning: {'PASS' if t5_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "06-warning-console.png"))
        print("  [OK] Saved 06-warning-console.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 6 & 7: message(), cat(), and Clear
        # -------------------------------------------------------------
        print("\n--- E2E TEST 6 & 7: message(), cat(), and Clear ---", flush=True)
        type_code("intro-r-01-001", 'message("test-message-social-r")')
        click_run("intro-r-01-001")
        type_code("intro-r-01-001", 'cat("test-cat-social-r\\n")')
        click_run("intro-r-01-001")

        c_out_mix = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t6_ok = "test-message-social-r" in c_out_mix and "test-cat-social-r" in c_out_mix
        print(f"Test 6 message() and cat(): {'PASS' if t6_ok else 'FAIL'}", flush=True)

        # Test Clear -> clears DOM, object social_r_test remains
        clear_console()
        c_cleared = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        type_code("intro-r-01-001", "social_r_test")
        click_run("intro-r-01-001")
        c_after_clear = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t7_ok = c_cleared.strip() == "" and "[1] 12345" in c_after_clear
        print(f"Test 7 Clear visual history: {'PASS' if t7_ok else 'FAIL'}", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 8: Collapse & Expand
        # -------------------------------------------------------------
        print("\n--- E2E TEST 8: Collapse & Expand ---", flush=True)
        driver.execute_script("document.getElementById('sr-btn-collapse-console').click();")
        time.sleep(0.3)
        driver.execute_script("document.getElementById('sr-btn-collapse-console').click();")
        time.sleep(0.3)
        c_collapsed_expanded = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t8_ok = "[1] 12345" in c_collapsed_expanded
        print(f"Test 8 Collapse & Expand: {'PASS' if t8_ok else 'FAIL'}", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 9: Submit Incorrect Answer (25 + 16)
        # -------------------------------------------------------------
        print("\n--- E2E TEST 9: Submit Incorrect ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "25 + 16")
        click_submit("intro-r-01-001")

        fb_inc = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        c_inc = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t9_ok = "Revisa tu respuesta" in fb_inc and "> 25 + 16" in c_inc and "[1] 41" in c_inc
        print(f"Test 9 Submit Incorrect: {'PASS' if t9_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "07-submit-incorrect.png"))
        print("  [OK] Saved 07-submit-incorrect.png", flush=True)

        # -------------------------------------------------------------
        # E2E TEST 10: Submit Correct Answer (25 + 17)
        # -------------------------------------------------------------
        print("\n--- E2E TEST 10: Submit Correct ---", flush=True)
        clear_console()
        type_code("intro-r-01-001", "25 + 17")
        click_submit("intro-r-01-001")

        fb_cor = driver.execute_script("return document.getElementById('sr-feedback-card-intro-r-01-001').textContent;")
        c_cor = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        t10_ok = "Correcto" in fb_cor and "> 25 + 17" in c_cor and "[1] 42" in c_cor
        v035_results["RUN VS SUBMIT SEPARATION"] = "PASS" if t9_ok and t10_ok else "FAIL"
        print(f"Test 10 Submit Correct: {'PASS' if t10_ok else 'FAIL'}", flush=True)

        driver.save_screenshot(str(out_dir / "08-submit-correct.png"))
        print("  [OK] Saved 08-submit-correct.png", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("Social R v0.3.5 — REAL R CONSOLE VERIFICATION SUMMARY")
    for k, v in v035_results.items():
        print(f"  {k}: {v}")
    print("=======================================================")

    all_pass = all(v == "PASS" for v in v035_results.values())
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    run_v035_suite()
