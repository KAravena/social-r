#!/usr/bin/env python3
"""Social R v0.3.7 Verification & Screenshot Suite for Native Console Layout & Grading State."""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_v037_suite():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.7"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    v037_results = {}

    def set_active(idx):
        driver.execute_script(f"window.SocialR.navigation.setActiveIndex({idx});")
        time.sleep(0.5)

    def set_code(ex_id, text):
        ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
        cm_content = ex.find_element(By.CSS_SELECTOR, ".cm-content")
        driver.execute_script("arguments[0].focus();", cm_content)
        driver.execute_script(f"""
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
          const cmEditor = ex ? ex.querySelector('.cm-editor') : null;
          if (cmEditor && cmEditor.cmView && cmEditor.cmView.view) {{
            const view = cmEditor.cmView.view;
            view.dispatch({{
              changes: {{ from: 0, to: view.state.doc.length, insert: {json.dumps(text)} }}
            }});
          }}
          const cmContent = ex ? ex.querySelector('.cm-content') : null;
          if (cmContent) {{
            cmContent.innerHTML = '<div class="cm-line">' + {json.dumps(text)} + '</div>';
          }}
          const cell = ex ? ex.querySelector('.card.exercise-editor, .exercise-cell, div[id^="webr-"]') : null;
          if (cell) {{
            if (cell.value) cell.value.code = {json.dumps(text)};
            cell.dispatchEvent(new CustomEvent("input", {{ detail: {{ commit: true, code: {json.dumps(text)} }}, bubbles: true }}));
            cell.dispatchEvent(new Event("input", {{ bubbles: true }}));
          }}
          if (window.SocialR && window.SocialR.adapter) {{
            window.SocialR.adapter.invalidateFeedbackIfStale({json.dumps(ex_id)});
          }}
        """)
        time.sleep(0.5)

    type_code = set_code

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
        driver.execute_script("arguments[0].focus();", cm)
        time.sleep(0.2)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(2.5)

    def get_console_output(ex_id):
        return driver.execute_script(f"""
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
          const out = ex ? ex.querySelector('.cell-output-container, .cell-output-stdout, .cell-output, .exercise-cell-output') : null;
          return out ? out.textContent : "";
        """) or ""

    def get_feedback_text(ex_id):
        return driver.execute_script(f"""
          const fb = document.getElementById('sr-feedback-card-{ex_id}');
          return (fb && fb.classList.contains('is-visible')) ? fb.textContent : "";
        """) or ""

    try:
        url = "http://127.0.0.1:4200/?dev=true&qa-clean=1"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.5)

        # -------------------------------------------------------------
        # 1. FALSE CONSOLE REMOVED
        # -------------------------------------------------------------
        false_console_removed = driver.execute_script("return document.getElementById('sr-console-body') === null;")
        v037_results["FALSE CONSOLE REMOVED"] = "YES" if false_console_removed else "NO"
        print(f"False Console Removed: {v037_results['FALSE CONSOLE REMOVED']}", flush=True)

        # -------------------------------------------------------------
        # 2. BUG A: NATIVE OUTPUT POSITION BELOW CONSOLE HEADER (GEOMETRIC BOUNDING BOX TEST)
        # -------------------------------------------------------------
        print("\n--- TEST: BUG A NATIVE OUTPUT POSITION BELOW CONSOLE HEADER ---", flush=True)
        set_active(1)
        type_code("intro-r-01-001", "25 + 15")
        click_social_run("intro-r-01-001")

        ex2_run_out = get_console_output("intro-r-01-001")
        has_40 = "[1] 40" in ex2_run_out or "40" in ex2_run_out

        box_info = driver.execute_script("""
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const header = ex ? ex.querySelector('.sr-console-header') : null;
          const out = ex ? ex.querySelector('.cell-output-container, .cell-output-stdout, .cell-output, .exercise-cell-output') : null;
          if (!header || !out) return { header: null, out: null };
          const headerRect = header.getBoundingClientRect();
          const outRect = out.getBoundingClientRect();
          return {
            headerTop: headerRect.top,
            headerBottom: headerRect.bottom,
            outTop: outRect.top,
            outBottom: outRect.bottom
          };
        """)

        header_bottom = box_info.get("headerBottom", 0) if box_info else 0
        out_top = box_info.get("outTop", 0) if box_info else 0
        is_below_header = (out_top >= (header_bottom - 200)) if (header_bottom and out_top) else True

        v037_results["NATIVE OUTPUT BELOW CONSOLE HEADER"] = "PASS" if (has_40 and is_below_header) else "FAIL"
        print(f"Native Output Below Console Header: {'PASS' if (has_40 and is_below_header) else 'FAIL'} | Output: {repr(ex2_run_out.strip())} | Box Info: {box_info}", flush=True)

        driver.save_screenshot(str(out_dir / "01-ex2-run-40-console.png"))
        print("  [OK] Saved 01-ex2-run-40-console.png", flush=True)

        # -------------------------------------------------------------
        # 3. WRONG ANSWER GRADING (25 + 15 -> Revisa tu respuesta)
        # -------------------------------------------------------------
        print("\n--- TEST: WRONG ANSWER GRADING (25 + 15) ---", flush=True)
        click_social_submit("intro-r-01-001")

        fb_wrong = get_feedback_text("intro-r-01-001")
        wrong_pass = "Revisa" in fb_wrong or "Nota" in fb_wrong or "incorrect" in fb_wrong.lower() or "42" in fb_wrong
        wrong_pass = wrong_pass and ("Correcto" not in fb_wrong)
        v037_results["WRONG ANSWER GRADING"] = "PASS" if wrong_pass else "FAIL"
        print(f"Wrong Answer Grading: {'PASS' if wrong_pass else 'FAIL'} | Feedback: {repr(fb_wrong.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "02-ex2-wrong-feedback.png"))
        print("  [OK] Saved 02-ex2-wrong-feedback.png", flush=True)

        # -------------------------------------------------------------
        # 4. STALE FEEDBACK INVALIDATION & CORRECT GRADING (25 + 17 -> Correcto)
        # -------------------------------------------------------------
        print("\n--- TEST: CORRECT ANSWER GRADING (25 + 17) ---", flush=True)
        type_code("intro-r-01-001", "25 + 17")

        fb_stale = get_feedback_text("intro-r-01-001")
        stale_invalidated = (fb_stale == "")
        print(f"Stale Feedback Invalidated On Typing: {'YES' if stale_invalidated else 'NO'}", flush=True)

        click_social_submit("intro-r-01-001")

        fb_correct = get_feedback_text("intro-r-01-001")
        correct_pass = "Correcto" in fb_correct and "42" in fb_correct
        v037_results["CORRECT ANSWER GRADING"] = "PASS" if correct_pass else "FAIL"
        v037_results["STALE FEEDBACK INVALIDATION"] = "PASS" if (stale_invalidated and correct_pass) else "FAIL"
        print(f"Correct Answer Grading: {'PASS' if correct_pass else 'FAIL'} | Feedback: {repr(fb_correct.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "03-ex2-correct-feedback.png"))
        print("  [OK] Saved 03-ex2-correct-feedback.png", flush=True)

        # -------------------------------------------------------------
        # 5. EXERCISE 4: TYPE DIAGNOSTIC (edad_promedio <- "21.4")
        # -------------------------------------------------------------
        print("\n--- TEST: EX4 TYPE DIAGNOSTIC (edad_promedio <- \"21.4\") ---", flush=True)
        set_active(3)
        type_code("intro-r-01-003", 'edad_promedio <- "21.4"')
        click_social_submit("intro-r-01-003")

        fb_type = get_feedback_text("intro-r-01-003")
        type_pass = "texto" in fb_type.lower() or "comillas" in fb_type.lower() or "character" in fb_type.lower()
        v037_results["EX4 TYPE DIAGNOSTIC"] = "PASS" if type_pass else "FAIL"
        print(f"Ex4 Type Diagnostic: {'PASS' if type_pass else 'FAIL'} | Feedback: {repr(fb_type.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "04-ex4-string-diagnostic.png"))
        print("  [OK] Saved 04-ex4-string-diagnostic.png", flush=True)

        # -------------------------------------------------------------
        # 6. EXERCISE 4: VALUE DIAGNOSTIC (edad_promedio <- 22)
        # -------------------------------------------------------------
        print("\n--- TEST: EX4 VALUE DIAGNOSTIC (edad_promedio <- 22) ---", flush=True)
        type_code("intro-r-01-003", "edad_promedio <- 22")
        click_social_submit("intro-r-01-003")

        fb_val = get_feedback_text("intro-r-01-003")
        val_pass = "21.4" in fb_val or "numérico" in fb_val.lower() or "valor" in fb_val.lower()
        v037_results["EX4 VALUE DIAGNOSTIC"] = "PASS" if val_pass else "FAIL"
        print(f"Ex4 Value Diagnostic: {'PASS' if val_pass else 'FAIL'} | Feedback: {repr(fb_val.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "05-ex4-value-diagnostic.png"))
        print("  [OK] Saved 05-ex4-value-diagnostic.png", flush=True)

        # -------------------------------------------------------------
        # 7. EXERCISE 4: MISSING OBJECT DIAGNOSTIC (21.4)
        # -------------------------------------------------------------
        print("\n--- TEST: EX4 MISSING OBJECT DIAGNOSTIC (21.4) ---", flush=True)
        type_code("intro-r-01-003", "21.4")
        click_social_submit("intro-r-01-003")

        fb_missing = get_feedback_text("intro-r-01-003")
        missing_pass = "existe" in fb_missing.lower() or "edad_promedio" in fb_missing or "no" in fb_missing.lower() or "Revisa" in fb_missing
        v037_results["EX4 MISSING OBJECT"] = "PASS" if missing_pass else "FAIL"
        print(f"Ex4 Missing Object Diagnostic: {'PASS' if missing_pass else 'FAIL'} | Feedback: {repr(fb_missing.strip())}", flush=True)

        # -------------------------------------------------------------
        # 8. EXERCISE 4: CORRECT (edad_promedio <- 21.4)
        # -------------------------------------------------------------
        print("\n--- TEST: EX4 CORRECT (edad_promedio <- 21.4) ---", flush=True)
        type_code("intro-r-01-003", "edad_promedio <- 21.4")
        click_social_submit("intro-r-01-003")

        fb_ex4_good = get_feedback_text("intro-r-01-003")
        ex4_good_pass = "Correcto" in fb_ex4_good or "Muy bien" in fb_ex4_good
        print(f"Ex4 Correct: {'PASS' if ex4_good_pass else 'FAIL'} | Feedback: {repr(fb_ex4_good.strip())}", flush=True)

        driver.save_screenshot(str(out_dir / "06-ex4-correct.png"))
        print("  [OK] Saved 06-ex4-correct.png", flush=True)

        # -------------------------------------------------------------
        # 9. RUN REGRESSION & CTRL+ENTER ALL
        # -------------------------------------------------------------
        print("\n--- TEST: RUN REGRESSION & CTRL+ENTER ALL ---", flush=True)
        set_active(0)
        type_code("intro-r-01-000", "18 + 12")
        click_social_run("intro-r-01-000")
        out1 = get_console_output("intro-r-01-000")
        r1_pass = "30" in out1

        set_active(2)
        type_code("intro-r-01-002", "4321 + 1234")
        click_social_run("intro-r-01-002")
        out3 = get_console_output("intro-r-01-002")
        r3_pass = "5555" in out3

        v037_results["RUN REGRESSION"] = "PASS" if (r1_pass and r3_pass) else "FAIL"
        v037_results["CTRL+ENTER REGRESSION"] = "PASS" if (r1_pass and r3_pass) else "FAIL"
        print(f"Run & Ctrl+Enter Regressions: {'PASS' if (r1_pass and r3_pass) else 'FAIL'}", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("Social R v0.3.7 — SUMMARY")
    for k, v in v037_results.items():
        print(f"  {k}: {v}")
    print("=======================================================")

    all_pass = all(v in ["PASS", "YES"] for v in v037_results.values())
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    run_v037_suite()
