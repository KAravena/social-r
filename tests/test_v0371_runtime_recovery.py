import time
import os
import json
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SCREENSHOT_DIR = Path(r"c:\Users\katin\Projects\R - camp\R-proyect\social-r-architecture-phase1\social-r-work\social-r-architecture\docs\screenshots\v0.3.7.1")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def run_v0371_suite():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,1000")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    driver = webdriver.Edge(options=options)
    
    summary = {}
    
    try:
        url = "http://127.0.0.1:4200/?dev=true&qa-clean=1"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        
        # Save initial state screenshot
        driver.save_screenshot(str(SCREENSHOT_DIR / "01-runtime-initializing.png"))
        
        # GATE 1: R READY STATUS TRANSITION
        print("\n--- GATE 1: R READY STATUS TRANSITION ---", flush=True)
        start_time = time.time()
        ready_reached = False
        final_status = ""
        
        for _ in range(30):
            time.sleep(0.5)
            status_text = driver.execute_script("return (document.getElementById('sr-webr-status-text') || {}).innerText || '';")
            if status_text == "R listo":
                ready_reached = True
                final_status = status_text
                break
        
        driver.save_screenshot(str(SCREENSHOT_DIR / "02-runtime-ready.png"))
        
        if ready_reached:
            print(f"Gate 1 (R Ready Status): PASS | Text: '{final_status}' after {int(time.time() - start_time)}s", flush=True)
            summary["GATE 1 R READY"] = "PASS"
        else:
            print(f"Gate 1 (R Ready Status): FAIL | Text: '{status_text}'", flush=True)
            summary["GATE 1 R READY"] = "FAIL"
            
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

        def click_social_submit(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
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

        # GATE 2: EX1 NATIVE RUN
        print("\n--- GATE 2: EX1 NATIVE RUN ---", flush=True)
        set_active(0)
        click_native_run("intro-r-01-000")
        out1 = get_console_output("intro-r-01-000")
        driver.save_screenshot(str(SCREENSHOT_DIR / "03-native-run-ex1.png"))
        if "[1] 30" in out1:
            print(f"Gate 2 (Ex1 Native Run): PASS | Output: '{out1.strip()}'", flush=True)
            summary["GATE 2 EX1 NATIVE RUN"] = "PASS"
        else:
            print(f"Gate 2 (Ex1 Native Run): FAIL | Output: '{out1.strip()}'", flush=True)
            summary["GATE 2 EX1 NATIVE RUN"] = "FAIL"

        # GATE 3: EX2 NATIVE RUN
        print("\n--- GATE 3: EX2 NATIVE RUN ---", flush=True)
        set_active(1)
        set_code("intro-r-01-001", "25 + 17")
        click_native_run("intro-r-01-001")
        out2 = get_console_output("intro-r-01-001")
        driver.save_screenshot(str(SCREENSHOT_DIR / "04-native-run-ex2.png"))
        if "[1] 42" in out2:
            print(f"Gate 3 (Ex2 Native Run): PASS | Output: '{out2.strip()}'", flush=True)
            summary["GATE 3 EX2 NATIVE RUN"] = "PASS"
        else:
            print(f"Gate 3 (Ex2 Native Run): FAIL | Output: '{out2.strip()}'", flush=True)
            summary["GATE 3 EX2 NATIVE RUN"] = "FAIL"

        # GATE 4: EX2 SOCIAL R RUN
        print("\n--- GATE 4: EX2 SOCIAL R RUN ---", flush=True)
        set_code("intro-r-01-001", "999 + 1")
        click_social_run("intro-r-01-001")
        out3 = get_console_output("intro-r-01-001")
        driver.save_screenshot(str(SCREENSHOT_DIR / "05-social-run-ex2.png"))
        if "[1] 1000" in out3:
            print(f"Gate 4 (Ex2 Social R Run): PASS | Output: '{out3.strip()}'", flush=True)
            summary["GATE 4 EX2 SOCIAL R RUN"] = "PASS"
        else:
            print(f"Gate 4 (Ex2 Social R Run): FAIL | Output: '{out3.strip()}'", flush=True)
            summary["GATE 4 EX2 SOCIAL R RUN"] = "FAIL"

        # GATE 5: EX2 CTRL+ENTER
        print("\n--- GATE 5: EX2 CTRL+ENTER ---", flush=True)
        set_code("intro-r-01-001", "731 + 184")
        press_ctrl_enter("intro-r-01-001")
        out4 = get_console_output("intro-r-01-001")
        if "[1] 915" in out4:
            print(f"Gate 5 (Ex2 Ctrl+Enter): PASS | Output: '{out4.strip()}'", flush=True)
            summary["GATE 5 EX2 CTRL+ENTER"] = "PASS"
        else:
            print(f"Gate 5 (Ex2 Ctrl+Enter): FAIL | Output: '{out4.strip()}'", flush=True)
            summary["GATE 5 EX2 CTRL+ENTER"] = "FAIL"

        # GATE 6: EX2 SUBMIT
        print("\n--- GATE 6: EX2 SUBMIT ---", flush=True)
        set_code("intro-r-01-001", "25 + 17")
        click_social_submit("intro-r-01-001")
        card = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-001")
        fb_text = card.text
        driver.save_screenshot(str(SCREENSHOT_DIR / "06-submit-ex2.png"))
        if "Correcto" in fb_text:
            print(f"Gate 6 (Ex2 Submit): PASS | Feedback: '{fb_text.strip()}'", flush=True)
            summary["GATE 6 EX2 SUBMIT"] = "PASS"
        else:
            print(f"Gate 6 (Ex2 Submit): FAIL | Feedback: '{fb_text.strip()}'", flush=True)
            summary["GATE 6 EX2 SUBMIT"] = "FAIL"

        print("\n=======================================================", flush=True)
        print("Social R v0.3.7.1 — RUNTIME RECOVERY SUMMARY", flush=True)
        for k, v in summary.items():
            print(f"  {k}: {v}", flush=True)
        print("=======================================================", flush=True)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_v0371_suite()
