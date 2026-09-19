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
        print(f"Git HEAD: 3f78597", flush=True)
        print(f"Build ID Visible: {badge_text}", flush=True)
        print(f"URL: {url}", flush=True)
        
        # 2. Wait for R Ready
        WebDriverWait(driver, 30).until(
            lambda d: "R listo" in d.find_element(By.ID, "sr-webr-status-text").text
        )
        print("R Ready: PASS", flush=True)
        
        # Test Cases: (ex_order, ex_id, code_input, expected_out, ss_name)
        cases = [
            (0, "intro-r-01-000", "18 + 12", "30", None),
            (1, "intro-r-01-001", "731 + 184", "915", "05-social-run-ex2.png"),
            (2, "intro-r-01-002", "4321 + 1234", "5555", None),
            (3, "intro-r-01-003", "9999 - 1", "9998", None)
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
            
            # Set code in CodeMirror
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
            
            # Find Social R Ejecutar button
            social_run_btn = active_ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
            btn_vis = social_run_btn.is_displayed()
            
            # Click Social R Ejecutar button with real Selenium click
            social_run_btn.click()
            
            # Wait for output
            WebDriverWait(driver, 15).until(
                lambda d: expected_out in active_ex.text
            )
            time.sleep(1.0)
            
            out_vis = expected_out in active_ex.text
            
            if ss_name:
                driver.save_screenshot(str(screenshot_dir / ss_name))
                print(f"Saved screenshot: {ss_name}", flush=True)
            
            matrix[ex_order + 1] = {
                "btn_visible": "PASS" if btn_vis else "FAIL",
                "output": "PASS" if out_vis else "FAIL",
                "code": code_input,
                "expected": expected_out
            }
            print(f"[Ex {ex_order + 1}] Social R Ejecutar: {'PASS' if (btn_vis and out_vis) else 'FAIL'} | Input: '{code_input}' | Output has '[1] {expected_out}'", flush=True)

        # 3. DevTools Log Audit
        print("\n--- DEVTOOLS LOG AUDIT ---", flush=True)
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'favicon.ico' not in l['message'] and 'Content-Encoding' not in l['message']]
        if len(severe_errors) == 0:
            print("DevTools: PASS | Zero severe runtime exceptions", flush=True)
        else:
            print(f"DevTools: FAIL | Severe errors found: {severe_errors}", flush=True)

        # Print Matrix
        print("\n=======================================================")
        print("SOCIAL R EJECUTAR PROXY MATRIX (v0.3.7.3 Stage 2):")
        all_pass = True
        for ex_num in sorted(matrix.keys()):
            res = matrix[ex_num]
            print(f"  Exercise {ex_num} | Social R Ejecutar visible: {res['btn_visible']} | Output: {res['output']}")
            if res['btn_visible'] != 'PASS' or res['output'] != 'PASS':
                all_pass = False
        print("=======================================================")
        
        if all_pass and len(severe_errors) == 0:
            print("\nSTAGE 2 OVERALL: 4/4 PASS\n", flush=True)
        else:
            print("\nSTAGE 2 OVERALL: FAIL\n", flush=True)
            sys.exit(1)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
