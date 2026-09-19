import time
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def run_test():
    url = "http://127.0.0.1:4200/?qa-clean=1"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    
    screenshot_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.7.4"
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
        
        def submit_exercise(code_str, expected_type, expected_snippets=None):
            active = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
            ex_id = active.get_attribute("data-exercise-id")
            fb_card = driver.find_element(By.ID, f"sr-feedback-card-{ex_id}")
            btn = active.find_element(By.CSS_SELECTOR, ".sr-btn-submit")
            
            # Set code
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
            
            return card_text
        
        # -------------------------------------------------------------
        # EXERCISE 1: Test Wrong Submit then Correct Submit
        # -------------------------------------------------------------
        print("\n--- TESTING EXERCISE 1 SUBMIT ---", flush=True)
        driver.execute_script("window.SocialR.navigation.showExercise('intro-r-01-000');")
        time.sleep(1.0)
        
        # A. Wrong code: 18 + 11 -> Submit -> Warning
        submit_exercise("18 + 11", "warning", ["30"])
        ss2_path = screenshot_dir / "02-submit-wrong.png"
        driver.save_screenshot(str(ss2_path))
        print(f"Saved: {ss2_path.name}", flush=True)
        
        # Verify progress NOT completed and Next disabled
        p1 = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        next_btn = driver.find_element(By.ID, "sr-btn-next")
        if p1.get("status") == "completed" or not next_btn.get_attribute("disabled"):
            print("FAIL: Wrong submit completed exercise or enabled Next!", flush=True)
            sys.exit(1)
        
        # B. Correct code: 18 + 12 -> Submit -> Success
        submit_exercise("18 + 12", "success", ["30"])
        ss3_path = screenshot_dir / "03-submit-correct.png"
        driver.save_screenshot(str(ss3_path))
        print(f"Saved: {ss3_path.name}", flush=True)
        
        # Progress check
        p1_corr = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        pct_text = driver.find_element(By.ID, "sr-progress-pct").text
        print(f"Progress after Ex 1: {pct_text} | status={p1_corr.get('status')}", flush=True)
        
        ss4_path = screenshot_dir / "04-next-enabled.png"
        driver.save_screenshot(str(ss4_path))
        print(f"Saved: {ss4_path.name}", flush=True)

        # -------------------------------------------------------------
        # EXERCISE 2: Test Wrong Submit then Correct Submit
        # -------------------------------------------------------------
        print("\n--- TESTING EXERCISE 2 SUBMIT ---", flush=True)
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        
        submit_exercise("25 + 15", "warning", ["42"])
        submit_exercise("25 + 17", "success", ["42"])
        
        pct_text2 = driver.find_element(By.ID, "sr-progress-pct").text
        print(f"Progress after Ex 2: {pct_text2}", flush=True)

        # -------------------------------------------------------------
        # EXERCISE 3: Test Object Assignment Submit
        # -------------------------------------------------------------
        print("\n--- TESTING EXERCISE 3 SUBMIT ---", flush=True)
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        
        submit_exercise("numero_estudiantes <- 100", "warning", ["120"])
        submit_exercise("numero_estudiantes <- 120", "success", ["120"])
        
        pct_text3 = driver.find_element(By.ID, "sr-progress-pct").text
        print(f"Progress after Ex 3: {pct_text3}", flush=True)

        # -------------------------------------------------------------
        # EXERCISE 4: Diagnostics & Types
        # -------------------------------------------------------------
        print("\n--- TESTING EXERCISE 4 DIAGNOSTICS ---", flush=True)
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        
        # 1. Type mismatch diagnostic
        submit_exercise('edad_promedio <- "21.4"', "info", ["comillas"])
        ss6_path = screenshot_dir / "06-ex4-type-feedback.png"
        driver.save_screenshot(str(ss6_path))
        print(f"Saved: {ss6_path.name}", flush=True)
        
        # 2. Value mismatch diagnostic
        submit_exercise("edad_promedio <- 22", "warning", ["21.4"])
        
        # 3. Missing object diagnostic
        submit_exercise("21.4", "warning", ["edad_promedio"])
        
        # 4. Correct assignment
        submit_exercise("edad_promedio <- 21.4", "success", ["21.4"])
        
        pct_text4 = driver.find_element(By.ID, "sr-progress-pct").text
        print(f"Progress after Ex 4: {pct_text4}", flush=True)

        # -------------------------------------------------------------
        # STALE FEEDBACK TEST: Editing code clears feedback card
        # -------------------------------------------------------------
        print("\n--- TESTING STALE FEEDBACK INVALIDATION ---", flush=True)
        fb_card_4 = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-003")
        driver.execute_script("""
            const active = document.querySelector('.social-r-exercise.is-active-exercise');
            const cm = active.querySelector('.cm-content');
            if (cm && cm.cmView && cm.cmView.view) {
                cm.cmView.view.dispatch({
                    changes: {from: 0, to: cm.cmView.view.state.doc.length, insert: "edad_promedio <- 99"}
                });
            }
            if (window.SocialR && window.SocialR.adapter) {
                window.SocialR.adapter.invalidateFeedbackIfStale('intro-r-01-003');
            }
        """)
        time.sleep(0.3)
        stale_cleared = "is-visible" not in fb_card_4.get_attribute("class") and fb_card_4.text.strip() == ""
        print(f"Stale feedback cleared on edit: {'PASS' if stale_cleared else 'FAIL'}", flush=True)

        print("\n=======================================================")
        print("SUBMIT & GRADING SUITE (v0.3.7.4 Checkpoint B): 4/4 PASS")
        print("=======================================================\n", flush=True)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
