import time
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def run_suite():
    url = "http://127.0.0.1:4200/?qa-clean=1"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    
    screenshot_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.7.5"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    driver = webdriver.Edge(options=options)
    
    try:
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        
        # 1. Wait for R Ready
        WebDriverWait(driver, 30).until(
            lambda d: "R listo" in d.find_element(By.ID, "sr-webr-status-text").text
        )
        print("R Ready: PASS", flush=True)
        time.sleep(1.0)
        
        active_ex = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
        run_btn = active_ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        submit_btn = active_ex.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
        fb_card_1 = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-000")
        
        def set_code(code_str):
            driver.execute_script(f"""
                const active = document.querySelector('.social-r-exercise.is-active-exercise');
                const cm = active.querySelector('.cm-content');
                if (cm && cm.cmView && cm.cmView.view) {{
                    cm.cmView.view.dispatch({{
                        changes: {{from: 0, to: cm.cmView.view.state.doc.length, insert: {repr(code_str)}}}
                    }});
                }}
            """)
            time.sleep(0.4)
            
        def get_console_text():
            return driver.execute_script("""
                const active = document.querySelector('.social-r-exercise.is-active-exercise');
                const outContainers = active.querySelectorAll('.cell-output-container, .cell-output-container-webr, .exercise-cell-output');
                return Array.from(outContainers).map(c => c.innerText).join('\\n');
            """)

        # -------------------------------------------------------------
        # TEST 1: Normal Result (18 + 25 -> 43)
        # -------------------------------------------------------------
        print("\n--- TEST 1: NORMAL RESULT (18 + 25) ---", flush=True)
        set_code("18 + 25")
        run_btn.click()
        WebDriverWait(driver, 15).until(lambda d: "43" in get_console_text())
        time.sleep(0.5)
        ss1 = screenshot_dir / "01-normal-result.png"
        driver.save_screenshot(str(ss1))
        print(f"Saved: {ss1.name} | Console: {repr(get_console_text().strip())}", flush=True)
        assert "43" in get_console_text()

        # -------------------------------------------------------------
        # TEST 2: Non-Existent Object Error
        # -------------------------------------------------------------
        print("\n--- TEST 2: NON-EXISTENT OBJECT ERROR ---", flush=True)
        obj_name = "social_r_objeto_que_no_existe_92831"
        set_code(obj_name)
        run_btn.click()
        WebDriverWait(driver, 15).until(
            lambda d: obj_name in get_console_text() and ("not found" in get_console_text() or "Error" in get_console_text())
        )
        time.sleep(0.5)
        ss2 = screenshot_dir / "02-object-error.png"
        driver.save_screenshot(str(ss2))
        print(f"Saved: {ss2.name} | Console: {repr(get_console_text().strip())}", flush=True)
        assert obj_name in get_console_text() and "not found" in get_console_text()

        # -------------------------------------------------------------
        # TEST 3: Syntax Error (18 +)
        # -------------------------------------------------------------
        print("\n--- TEST 3: SYNTAX ERROR (18 +) ---", flush=True)
        set_code("18 +")
        run_btn.click()
        WebDriverWait(driver, 15).until(
            lambda d: "Error" in get_console_text() and ("parse" in get_console_text() or "unexpected" in get_console_text())
        )
        time.sleep(0.5)
        ss3 = screenshot_dir / "03-syntax-error.png"
        driver.save_screenshot(str(ss3))
        print(f"Saved: {ss3.name} | Console: {repr(get_console_text().strip())}", flush=True)
        assert "Error" in get_console_text()

        # -------------------------------------------------------------
        # TEST 4: Warning (sqrt(-1))
        # -------------------------------------------------------------
        print("\n--- TEST 4: WARNING (sqrt(-1)) ---", flush=True)
        set_code("sqrt(-1)")
        run_btn.click()
        WebDriverWait(driver, 15).until(
            lambda d: "Warning" in get_console_text() and "NaN" in get_console_text()
        )
        time.sleep(0.5)
        ss4 = screenshot_dir / "04-warning.png"
        driver.save_screenshot(str(ss4))
        print(f"Saved: {ss4.name} | Console: {repr(get_console_text().strip())}", flush=True)
        assert "Warning" in get_console_text() and "NaN" in get_console_text()

        # -------------------------------------------------------------
        # TEST 5: Recovery After Errors (18 + 12 -> 30)
        # -------------------------------------------------------------
        print("\n--- TEST 5: RECOVERY AFTER ERRORS (18 + 12) ---", flush=True)
        set_code("18 + 12")
        run_btn.click()
        WebDriverWait(driver, 15).until(lambda d: "30" in get_console_text())
        time.sleep(0.5)
        ss5 = screenshot_dir / "05-recovery-after-error.png"
        driver.save_screenshot(str(ss5))
        print(f"Saved: {ss5.name} | Console: {repr(get_console_text().strip())}", flush=True)
        assert "30" in get_console_text()

        # -------------------------------------------------------------
        # TEST 6: Message and Cat Outputs
        # -------------------------------------------------------------
        print("\n--- TEST 6: MESSAGE & CAT OUTPUTS ---", flush=True)
        set_code('message("mensaje-social-r")')
        run_btn.click()
        WebDriverWait(driver, 15).until(lambda d: "mensaje-social-r" in get_console_text())
        print("Message output in Console: PASS", flush=True)
        
        set_code('cat("hola-social-r\\n")')
        run_btn.click()
        WebDriverWait(driver, 15).until(lambda d: "hola-social-r" in get_console_text())
        print("Cat stdout output in Console: PASS", flush=True)

        # -------------------------------------------------------------
        # TEST 7: Clean UI / No OJS Leaks
        # -------------------------------------------------------------
        print("\n--- TEST 7: CLEAN UI (NO OJS LEAKS) ---", flush=True)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "_webr_editor_" not in body_text, "Leak: _webr_editor_ visible in body text"
        assert "_webr_value_" not in body_text, "Leak: _webr_value_ visible in body text"
        assert "evaluator: Go" not in body_text, "Leak: evaluator: Go visible in body text"
        ss6 = screenshot_dir / "06-clean-ui-no-ojs.png"
        driver.save_screenshot(str(ss6))
        print(f"Saved: {ss6.name} | Clean UI Verified: PASS", flush=True)
        # -------------------------------------------------------------
        # TEST 8: Run vs Submit Regression
        # -------------------------------------------------------------
        print("\n--- TEST 8: RUN VS SUBMIT REGRESSION ---", flush=True)
        def submit_exercise(code_str, expected_type, expected_snippets=None):
            active = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
            ex_id = active.get_attribute("data-exercise-id")
            fb_card = driver.find_element(By.ID, f"sr-feedback-card-{ex_id}")
            btn = active.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
            
            driver.execute_script(f"""
                const active = document.querySelector('.social-r-exercise.is-active-exercise');
                const cm = active.querySelector('.cm-content');
                if (cm && cm.cmView && cm.cmView.view) {{
                    const view = cm.cmView.view;
                    view.dispatch({{
                        changes: {{from: 0, to: view.state.doc.length, insert: {repr(code_str)}}}
                    }});
                }}
            """)
            time.sleep(0.5)
            btn.click()
            time.sleep(2.5)
            
            card_class = fb_card.get_attribute("class")
            card_text = fb_card.text
            print(f"[{ex_id}] Code: '{code_str}' -> [{card_class}] '{card_text.replace(chr(10), ' ')}'", flush=True)
            
            assert f"is-{expected_type}" in card_class, f"Expected 'is-{expected_type}' in '{card_class}'"
            assert "is-visible" in card_class, f"Expected 'is-visible' in '{card_class}'"
            if expected_snippets:
                for snip in expected_snippets:
                    assert snip in card_text, f"Snippet '{snip}' not found in '{card_text}'"

        # 1. Run 18 + 11 -> output 29, no feedback, progress 0
        set_code("18 + 11")
        driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise .sr-btn-run").click()
        WebDriverWait(driver, 15).until(lambda d: "29" in get_console_text())
        time.sleep(0.5)
        has_fb = "is-visible" in fb_card_1.get_attribute("class") and len(fb_card_1.text.strip()) > 0
        p1 = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        assert not has_fb, "Run should NOT show feedback card"
        assert p1.get("status") != "completed", "Run should NOT complete exercise"
        print("Run '18 + 11': PASS (Output 29, No Feedback, Not Completed)", flush=True)
        
        # 2. Submit 18 + 11 -> warning
        submit_exercise("18 + 11", "warning", ["30"])
        
        # 3. Submit 18 + 12 -> success, progress 25%, next enabled
        submit_exercise("18 + 12", "success", ["30"])
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.getElementById('sr-btn-next').disabled === false")
        )
        pct = driver.find_element(By.ID, "sr-progress-pct").text
        next_btn = driver.find_element(By.ID, "sr-btn-next")
        assert "25%" in pct, f"Expected 25% in progress: {pct}"
        assert next_btn.get_attribute("disabled") is None, "Next button should be enabled after correct submit"
        print(f"Submit '18 + 12': PASS (Success Feedback, Progress: {pct}, Next Enabled)", flush=True)

        print("\n===============================================================")
        print("SOCIAL R v0.3.7.5 CONSOLE ERROR SEMANTICS: ALL TESTS PASS!")
        print("===============================================================\n", flush=True)

    finally:
        driver.quit()

if __name__ == "__main__":
    run_suite()

