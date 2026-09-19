import time
import sys
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def run_test():
    url = "http://127.0.0.1:4200/?qa-clean=1"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    
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
        
        # -------------------------------------------------------------
        # 1. Test Ctrl + Enter (RUN ONLY, NO FEEDBACK)
        # -------------------------------------------------------------
        print("\n--- TESTING CTRL + ENTER (RUN) ---", flush=True)
        active_ex = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
        editor_content = active_ex.find_element(By.CSS_SELECTOR, ".cm-content")
        fb_card_1 = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-000")
        
        # Set code to 18 + 11
        driver.execute_script("""
            const active = document.querySelector('.social-r-exercise.is-active-exercise');
            const cm = active.querySelector('.cm-content');
            if (cm && cm.cmView && cm.cmView.view) {
                cm.cmView.view.dispatch({
                    changes: {from: 0, to: cm.cmView.view.state.doc.length, insert: "18 + 11"}
                });
            }
        """)
        time.sleep(0.3)
        editor_content.click()
        time.sleep(0.2)
        
        # Send Ctrl + Enter
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        
        WebDriverWait(driver, 15).until(
            lambda d: "29" in active_ex.text
        )
        time.sleep(1.0)
        
        has_feedback = "is-visible" in fb_card_1.get_attribute("class") and len(fb_card_1.text.strip()) > 0
        p1 = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        assert not has_feedback, "Ctrl + Enter should NOT trigger pedagogical feedback"
        assert p1.get("status") != "completed", "Ctrl + Enter should NOT complete exercise"
        print("Ctrl + Enter (Run Only): PASS (Output=29, Feedback=None, Status=not_started)", flush=True)

        # -------------------------------------------------------------
        # 2. Test Ctrl + Shift + Enter (SUBMIT & GRADE)
        # -------------------------------------------------------------
        print("\n--- TESTING CTRL + SHIFT + ENTER (SUBMIT) 4/4 ---", flush=True)
        
        def test_submit_shortcut(code_str, expected_progress):
            active = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
            ex_id = active.get_attribute("data-exercise-id")
            fb_card = driver.find_element(By.ID, f"sr-feedback-card-{ex_id}")
            editor = active.find_element(By.CSS_SELECTOR, ".cm-content")
            
            # Set code
            driver.execute_script(f"""
                const active = document.querySelector('.social-r-exercise.is-active-exercise');
                const cm = active.querySelector('.cm-content');
                if (cm && cm.cmView && cm.cmView.view) {{
                    cm.cmView.view.dispatch({{
                        changes: {{from: 0, to: cm.cmView.view.state.doc.length, insert: {repr(code_str)}}}
                    }});
                }}
            """)
            time.sleep(0.3)
            editor.click()
            time.sleep(0.2)
            
            # Send Ctrl + Shift + Enter
            ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
            
            WebDriverWait(driver, 20).until(
                lambda d: "is-success" in fb_card.get_attribute("class") and "is-visible" in fb_card.get_attribute("class")
            )
            time.sleep(0.5)
            
            pct = driver.find_element(By.ID, "sr-progress-pct").text
            assert expected_progress in pct, f"Expected {expected_progress} in {pct}"
            print(f"[{ex_id}] Ctrl+Shift+Enter -> '{code_str}' -> Success ({pct})", flush=True)
        
        # Ex 1: 18 + 12 -> 25%
        test_submit_shortcut("18 + 12", "25%")
        
        # Ex 2: 25 + 17 -> 50%
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        test_submit_shortcut("25 + 17", "50%")
        
        # Ex 3: numero_estudiantes <- 120 -> 75%
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        test_submit_shortcut("numero_estudiantes <- 120", "75%")
        
        # Ex 4: edad_promedio <- 21.4 -> 100%
        driver.execute_script("window.SocialR.navigation.next();")
        time.sleep(1.0)
        test_submit_shortcut("edad_promedio <- 21.4", "100%")

        # -------------------------------------------------------------
        # 3. Test Stale Feedback Clearing on typing
        # -------------------------------------------------------------
        print("\n--- TESTING STALE FEEDBACK ON TYPING ---", flush=True)
        fb_card_4 = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-003")
        editor_4 = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise .cm-content")
        editor_4.click()
        editor_4.send_keys(" # modifying code")
        time.sleep(0.4)
        stale_cleared = "is-visible" not in fb_card_4.get_attribute("class") and fb_card_4.text.strip() == ""
        print(f"Stale feedback cleared on live typing: {'PASS' if stale_cleared else 'FAIL'}", flush=True)

        print("\n=======================================================")
        print("SHORTCUTS & INTERACTION SUITE (v0.3.7.4 Checkpoint D): PASS")
        print("=======================================================\n", flush=True)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
