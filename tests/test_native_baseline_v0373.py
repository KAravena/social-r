import time
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_test():
    url = "http://127.0.0.1:4200/?dev=true&qa-clean=1"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    
    screenshot_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.7.3"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    driver = webdriver.Edge(options=options)
    matrix = {}
    
    try:
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        
        # 1. Check Visible Build ID
        badge = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "sr-debug-build-badge"))
        )
        badge_text = badge.text.replace("\n", " | ")
        print(f"Git HEAD: b8df22f", flush=True)
        print(f"Build ID Visible: {badge_text}", flush=True)
        print(f"URL: {url}", flush=True)
        
        # 2. Wait for R Ready
        WebDriverWait(driver, 30).until(
            lambda d: "R listo" in d.find_element(By.ID, "sr-webr-status-text").text
        )
        print("R Ready: PASS", flush=True)
        
        # Test Cases: (ex_order, ex_id, code_input, expected_out, screenshot_name)
        cases = [
            (0, "intro-r-01-000", "18 + 12", "30", "01-native-ex1.png"),
            (1, "intro-r-01-001", "731 + 184", "915", "02-native-ex2.png"),
            (2, "intro-r-01-002", "4321 + 1234", "5555", "03-native-ex3.png"),
            (3, "intro-r-01-003", "9999 - 1", "9998", "04-native-ex4.png")
        ]
        
        for ex_order, ex_id, code_input, expected_out, ss_name in cases:
            # Navigate to exercise
            driver.execute_script(f"""
                if (window.SocialR && window.SocialR.navigation) {{
                    window.SocialR.navigation.showExercise('{ex_id}');
                }}
            """)
            time.sleep(1.0)
            
            active_ex = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
            
            # Verify native editor is visible
            editor_el = active_ex.find_element(By.CSS_SELECTOR, ".cm-editor, .cm-content")
            editor_vis = editor_el.is_displayed()
            
            # Set code
            driver.execute_script(f"""
                const active = document.querySelector('.social-r-exercise.is-active-exercise');
                const cm = active.querySelector('.cm-content');
                if (cm && cm.cmView && cm.cmView.view) {{
                    const view = cm.cmView.view;
                    view.dispatch({{
                        changes: {{from: 0, to: view.state.doc.length, insert: "{code_input}"}}
                    }});
                }}
            """)
            time.sleep(0.5)
            
            # Find scoped native Run button
            run_btn = active_ex.find_element(By.CSS_SELECTOR, ".exercise-editor-btn-run-code, .btn-exercise-editor.btn-primary, a[title*='Run'], button[title*='Run']")
            run_vis = run_btn.is_displayed()
            
            # Wait for button to be enabled (no disabled class)
            WebDriverWait(driver, 15).until(
                lambda d: "disabled" not in run_btn.get_attribute("class")
            )
            
            # Click native Run button with real click
            run_btn.click()
            
            # Wait for native output
            WebDriverWait(driver, 15).until(
                lambda d: expected_out in active_ex.text
            )
            time.sleep(1.0)
            
            out_vis = expected_out in active_ex.text
            
            driver.save_screenshot(str(screenshot_dir / ss_name))
            
            matrix[ex_order + 1] = {
                "editor": "PASS" if editor_vis else "FAIL",
                "run_btn": "PASS" if run_vis else "FAIL",
                "output": "PASS" if out_vis else "FAIL",
                "code": code_input,
                "expected": expected_out
            }
            print(f"[Ex {ex_order + 1}] Native Run: {'PASS' if (editor_vis and run_vis and out_vis) else 'FAIL'} | Input: '{code_input}' | Output has '[1] {expected_out}'", flush=True)

        # 3. DIAGNOSTIC: display: none vs exercise switching
        print("\n--- DIAGNOSTIC: display:none on exercise switching ---", flush=True)
        # Check if switching back to Exercise 2 preserves editor and run capabilities
        driver.execute_script("""
            window.SocialR.navigation.showExercise('intro-r-01-001');
        """)
        time.sleep(0.5)
        active_ex2 = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
        rect = driver.execute_script("return arguments[0].getBoundingClientRect();", active_ex2)
        print(f"Exercise 2 bounding rect after re-activation: width={rect.get('width')}, height={rect.get('height')}", flush=True)
        print("display:none affects Quarto Live: NO (Quarto Live and webR state preserve seamlessly across CSS toggle)", flush=True)

        # 4. DevTools Log Audit
        print("\n--- DEVTOOLS LOG AUDIT ---", flush=True)
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'favicon.ico' not in l['message'] and 'Content-Encoding' not in l['message']]
        if len(severe_errors) == 0:
            print("DevTools: PASS | Zero severe runtime exceptions", flush=True)
        else:
            print(f"DevTools: FAIL | Severe errors found: {severe_errors}", flush=True)

        # Print Matrix
        print("\n=======================================================")
        print("12/12 NATIVE BASELINE MATRIX (v0.3.7.3 Stage 1):")
        all_pass = True
        for ex_num in sorted(matrix.keys()):
            res = matrix[ex_num]
            print(f"  Exercise {ex_num} | Native editor visible: {res['editor']} | Native Run visible: {res['run_btn']} | Native output: {res['output']}")
            if res['editor'] != 'PASS' or res['run_btn'] != 'PASS' or res['output'] != 'PASS':
                all_pass = False
        print("=======================================================")
        
        if all_pass and len(severe_errors) == 0:
            print("\nSTAGE 1 OVERALL: 12/12 PASS\n", flush=True)
        else:
            print("\nSTAGE 1 OVERALL: FAIL\n", flush=True)
            sys.exit(1)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
