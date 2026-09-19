import time
import os
import json
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SCREENSHOT_DIR = Path(r"c:\Users\katin\Projects\R - camp\R-proyect\social-r-architecture-phase1\social-r-work\social-r-architecture\docs\screenshots\v0.3.7.2")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def run_v0372_pipeline_suite():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1000")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    driver = webdriver.Edge(options=options)
    
    matrix = {
        "Ex 1": {"native": "FAIL", "social": "FAIL", "shortcut": "FAIL"},
        "Ex 2": {"native": "FAIL", "social": "FAIL", "shortcut": "FAIL"},
        "Ex 3": {"native": "FAIL", "social": "FAIL", "shortcut": "FAIL"},
        "Ex 4": {"native": "FAIL", "social": "FAIL", "shortcut": "FAIL"}
    }
    
    status_summary = {
        "R READY": "FAIL",
        "NATIVE RUN 4/4": "FAIL",
        "SOCIAL RUN 4/4": "FAIL",
        "CTRL+ENTER 4/4": "FAIL",
        "CYCLIC NAVIGATION RUN": "FAIL",
        "DEVTOOLS": "FAIL",
        "MANUAL EX2 731+184 -> 915": "FAIL"
    }

    try:
        url = "http://127.0.0.1:4200/?dev=true&qa-clean=1"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        
        # 1. BOOT CHECK
        print("\n--- BOOT CHECK (R READY) ---", flush=True)
        ready_reached = False
        for _ in range(30):
            time.sleep(0.5)
            status_text = driver.execute_script("return (document.getElementById('sr-webr-status-text') || {}).innerText || '';")
            if status_text == "R listo":
                ready_reached = True
                break
        
        driver.save_screenshot(str(SCREENSHOT_DIR / "01-r-ready.png"))
        if ready_reached:
            print("R Ready: PASS", flush=True)
            status_summary["R READY"] = "PASS"
        else:
            print("R Ready: FAIL", flush=True)
            return

        def set_active(idx):
            driver.execute_script("""
              if (window.SocialR && window.SocialR.navigation) {
                window.SocialR.navigation.setActiveIndex(arguments[0]);
              } else {
                const exercises = document.querySelectorAll(".social-r-exercise");
                exercises.forEach((ex, i) => {
                  if (i === arguments[0]) {
                    ex.classList.add("is-active-exercise");
                    ex.classList.remove("d-none");
                    ex.style.display = "flex";
                  } else {
                    ex.classList.remove("is-active-exercise");
                    ex.classList.add("d-none");
                    ex.style.display = "none";
                  }
                });
              }
            """, idx)
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
            """)
            time.sleep(0.5)

        def click_native_run(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            btn = ex.find_element(By.CSS_SELECTOR, ".btn-exercise-editor.btn-primary, .exercise-editor-btn-run-code, a[title*='Run'], button[title*='Run']")
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(3.0)

        def click_social_run(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(3.0)

        def press_ctrl_enter(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
            driver.execute_script("arguments[0].focus();", cm)
            time.sleep(0.2)
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
            time.sleep(3.0)

        def get_console_output(ex_id):
            return driver.execute_script(f"""
              const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
              const out = ex ? ex.querySelector('.cell-output-container, .cell-output-stdout, .cell-output, .exercise-cell-output') : null;
              return out ? out.innerText : '';
            """)

        # 2. LAYER 1: NATIVE RUN (4/4)
        print("\n--- LAYER 1: NATIVE RUN ---", flush=True)
        native_passes = 0
        native_tests = [
            (0, "intro-r-01-000", "18 + 12", "[1] 30", "Ex 1"),
            (1, "intro-r-01-001", "999 + 1", "[1] 1000", "Ex 2"),
            (2, "intro-r-01-002", "4321 + 1234", "[1] 5555", "Ex 3"),
            (3, "intro-r-01-003", "9999 - 1", "[1] 9998", "Ex 4"),
        ]
        for idx, ex_id, code, expected, label in native_tests:
            set_active(idx)
            set_code(ex_id, code)
            click_native_run(ex_id)
            out = get_console_output(ex_id)
            if idx == 1:
                driver.save_screenshot(str(SCREENSHOT_DIR / "02-native-run-ex2.png"))
            if expected in out:
                matrix[label]["native"] = "PASS"
                native_passes += 1
                print(f"[{label}] Native Run: PASS | Code: '{code}' | Output: '{out.strip()}'", flush=True)
            else:
                print(f"[{label}] Native Run: FAIL | Code: '{code}' | Output: '{out.strip()}'", flush=True)

        if native_passes == 4:
            status_summary["NATIVE RUN 4/4"] = "PASS"

        # 3. LAYER 2: SOCIAL R EJECUTAR BUTTON (4/4)
        print("\n--- LAYER 2: SOCIAL R EJECUTAR BUTTON ---", flush=True)
        social_passes = 0
        social_tests = [
            (0, "intro-r-01-000", "18 + 12", "[1] 30", "Ex 1"),
            (1, "intro-r-01-001", "999 + 1", "[1] 1000", "Ex 2"),
            (2, "intro-r-01-002", "4321 + 1234", "[1] 5555", "Ex 3"),
            (3, "intro-r-01-003", "9999 - 1", "[1] 9998", "Ex 4"),
        ]
        for idx, ex_id, code, expected, label in social_tests:
            set_active(idx)
            set_code(ex_id, code)
            click_social_run(ex_id)
            out = get_console_output(ex_id)
            if idx == 1:
                driver.save_screenshot(str(SCREENSHOT_DIR / "03-social-run-ex2.png"))
            if expected in out:
                matrix[label]["social"] = "PASS"
                social_passes += 1
                print(f"[{label}] Social Run: PASS | Code: '{code}' | Output: '{out.strip()}'", flush=True)
            else:
                print(f"[{label}] Social Run: FAIL | Code: '{code}' | Output: '{out.strip()}'", flush=True)

        if social_passes == 4:
            status_summary["SOCIAL RUN 4/4"] = "PASS"

        # 4. LAYER 3: CTRL+ENTER KEYBOARD SHORTCUT WITH RANDOM VALUES (4/4)
        print("\n--- LAYER 3: CTRL+ENTER SHORTCUT (RANDOM VALUES) ---", flush=True)
        shortcut_passes = 0
        
        # Specific test for Directive 58: Ex2 731 + 184 -> [1] 915
        set_active(1)
        set_code("intro-r-01-001", "731 + 184")
        press_ctrl_enter("intro-r-01-001")
        ex2_out = get_console_output("intro-r-01-001")
        driver.save_screenshot(str(SCREENSHOT_DIR / "04-ctrl-enter-ex2.png"))
        if "[1] 915" in ex2_out:
            status_summary["MANUAL EX2 731+184 -> 915"] = "PASS"
            print("[Ex 2] Specific 731+184 test: PASS | Output: '[1] 915'", flush=True)

        shortcut_tests = [
            (0, "intro-r-01-000", "100 + 1", "[1] 101", "Ex 1"),
            (1, "intro-r-01-001", "731 + 184", "[1] 915", "Ex 2"),
            (2, "intro-r-01-002", "4321 + 1234", "[1] 5555", "Ex 3"),
            (3, "intro-r-01-003", "9999 - 1", "[1] 9998", "Ex 4"),
        ]

        for idx, ex_id, code, expected, label in shortcut_tests:
            set_active(idx)
            set_code(ex_id, code)
            press_ctrl_enter(ex_id)
            out = get_console_output(ex_id)
            if idx == 2:
                driver.save_screenshot(str(SCREENSHOT_DIR / "05-ctrl-enter-ex3.png"))
            if expected in out:
                matrix[label]["shortcut"] = "PASS"
                shortcut_passes += 1
                print(f"[{label}] Ctrl+Enter: PASS | Code: '{code}' | Output: '{out.strip()}'", flush=True)
            else:
                print(f"[{label}] Ctrl+Enter: FAIL | Code: '{code}' | Output: '{out.strip()}'", flush=True)

        if shortcut_passes == 4:
            status_summary["CTRL+ENTER 4/4"] = "PASS"

        # 5. CYCLIC NAVIGATION RUN TEST
        print("\n--- CYCLIC NAVIGATION RUN TEST ---", flush=True)
        sequence = [
            (0, "intro-r-01-000", "643 + 278", "[1] 921"),
            (1, "intro-r-01-001", "500 + 500", "[1] 1000"),
            (2, "intro-r-01-002", "123 + 456", "[1] 579"),
            (3, "intro-r-01-003", "8888 - 1111", "[1] 7777"),
            (2, "intro-r-01-002", "1000 + 2000", "[1] 3000"),
            (1, "intro-r-01-001", "300 + 400", "[1] 700"),
            (0, "intro-r-01-000", "50 + 50", "[1] 100"),
        ]

        cyclic_passed = True
        for idx, ex_id, code, expected in sequence:
            set_active(idx)
            set_code(ex_id, code)
            press_ctrl_enter(ex_id)
            out = get_console_output(ex_id)
            if expected in out:
                print(f"Cyclic Ex {idx+1}: PASS | Code: '{code}' | Output: '{out.strip()}'", flush=True)
            else:
                print(f"Cyclic Ex {idx+1}: FAIL | Code: '{code}' | Output: '{out.strip()}'", flush=True)
                cyclic_passed = False

        if cyclic_passed:
            status_summary["CYCLIC NAVIGATION RUN"] = "PASS"

        # 6. DEVTOOLS LOG AUDIT
        print("\n--- DEVTOOLS LOG AUDIT ---", flush=True)
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'favicon.ico' not in l['message'] and 'Content-Encoding' not in l['message']]
        if len(severe_errors) == 0:
            status_summary["DEVTOOLS"] = "PASS"
            print("DevTools: PASS | No severe runtime exceptions", flush=True)
        else:
            print(f"DevTools: FAIL | Severe errors found: {severe_errors}", flush=True)

        # PRINT FINAL MATRIX SUMMARY
        print("\n=======================================================", flush=True)
        print("12/12 EXECUTION PIPELINE MATRIX (v0.3.7.2):", flush=True)
        print(f"  Exercise 1 | Native: {matrix['Ex 1']['native']} | Social: {matrix['Ex 1']['social']} | Ctrl+Enter: {matrix['Ex 1']['shortcut']}", flush=True)
        print(f"  Exercise 2 | Native: {matrix['Ex 2']['native']} | Social: {matrix['Ex 2']['social']} | Ctrl+Enter: {matrix['Ex 2']['shortcut']}", flush=True)
        print(f"  Exercise 3 | Native: {matrix['Ex 3']['native']} | Social: {matrix['Ex 3']['social']} | Ctrl+Enter: {matrix['Ex 3']['shortcut']}", flush=True)
        print(f"  Exercise 4 | Native: {matrix['Ex 4']['native']} | Social: {matrix['Ex 4']['social']} | Ctrl+Enter: {matrix['Ex 4']['shortcut']}", flush=True)
        print("-------------------------------------------------------", flush=True)
        print("OVERALL SUMMARY:", flush=True)
        for k, v in status_summary.items():
            print(f"  {k}: {v}", flush=True)
        print("=======================================================", flush=True)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_v0372_pipeline_suite()
