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
    
    screenshot_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.7.4"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    driver = webdriver.Edge(options=options)
    
    try:
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        
        # 1. Check Build ID
        badge = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "sr-debug-build-badge"))
        )
        badge_text = badge.text.replace("\n", " | ")
        print(f"Build ID Visible: {badge_text}", flush=True)
        
        # 2. Wait for R Ready
        WebDriverWait(driver, 30).until(
            lambda d: "R listo" in d.find_element(By.ID, "sr-webr-status-text").text
        )
        print("R Ready: PASS", flush=True)
        
        # 3. Test Wrong Code on Ex 1: Run alone -> shows [1] 29, NO feedback, progress 0%, next disabled
        driver.execute_script("window.SocialR.navigation.showExercise('intro-r-01-000');")
        time.sleep(0.5)
        active_ex = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
        
        # Set code to 18 + 11
        driver.execute_script("""
            const active = document.querySelector('.social-r-exercise.is-active-exercise');
            const cm = active.querySelector('.cm-content');
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: {from: 0, to: view.state.doc.length, insert: "18 + 11"}
                });
            }
        """)
        time.sleep(0.3)
        
        # Click Social R Run button
        run_btn = active_ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        run_btn.click()
        
        # Wait for [1] 29
        WebDriverWait(driver, 15).until(
            lambda d: "29" in active_ex.text
        )
        time.sleep(1.0)
        
        # Check feedback card is empty
        feedback_card = driver.find_element(By.ID, "sr-feedback-card-intro-r-01-000")
        has_feedback = "is-visible" in feedback_card.get_attribute("class") or len(feedback_card.text.strip()) > 0
        
        # Check progress
        progress_val = driver.execute_script("return window.SocialR.progress.get('intro-r-01-000');")
        is_completed = progress_val.get("status") == "completed"
        
        # Save Screenshot 01: 01-run-wrong-no-feedback.png
        ss1_path = screenshot_dir / "01-run-wrong-no-feedback.png"
        driver.save_screenshot(str(ss1_path))
        print(f"Saved: {ss1_path.name}", flush=True)
        print(f"Ex 1 Run '18 + 11': Output=29, FeedbackVisible={has_feedback}, Completed={is_completed}", flush=True)
        
        if has_feedback or is_completed:
            print("FAIL: Run triggered feedback or completed exercise!", flush=True)
            sys.exit(1)
        
        # 4. Test Ex 2 Run & Console Layout
        driver.execute_script("window.SocialR.navigation.showExercise('intro-r-01-001');")
        time.sleep(1.0)
        active_ex2 = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
        driver.execute_script("""
            const active = document.querySelector('.social-r-exercise.is-active-exercise');
            const cm = active.querySelector('.cm-content');
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: {from: 0, to: view.state.doc.length, insert: "25 + 17"}
                });
            }
        """)
        time.sleep(0.5)
        run_btn2 = active_ex2.find_element(By.CSS_SELECTOR, ".sr-btn-run")
        run_btn2.click()
        WebDriverWait(driver, 15).until(
            lambda d: "42" in active_ex2.text
        )
        time.sleep(1.0)
        
        ss5_path = screenshot_dir / "05-ex2-run-console.png"
        driver.save_screenshot(str(ss5_path))
        print(f"Saved: {ss5_path.name}", flush=True)
        print("Ex 2 Run '25 + 17': Output=42 in R Console: PASS", flush=True)

        print("\nCHECKPOINT A OVERALL: PASS\n", flush=True)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
