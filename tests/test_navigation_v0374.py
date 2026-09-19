import time
import sys
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
        
        prev_btn = driver.find_element(By.ID, "sr-btn-prev")
        next_btn = driver.find_element(By.ID, "sr-btn-next")
        title_el = driver.find_element(By.ID, "sr-topbar-exercise-title")
        
        # Ex 1 state
        assert "1/4" in title_el.text, f"Expected 1/4 in title: {title_el.text}"
        assert prev_btn.get_attribute("disabled") is not None, "Prev button should be disabled on Ex 1"
        assert next_btn.get_attribute("disabled") is not None, "Next button should be disabled before Ex 1 completion"
        print("Initial Ex 1 Navigation State: PASS (Prev=Disabled, Next=Disabled)", flush=True)
        
        def complete_active(code_str):
            active = driver.find_element(By.CSS_SELECTOR, ".social-r-exercise.is-active-exercise")
            ex_id = active.get_attribute("data-exercise-id")
            fb_card = driver.find_element(By.ID, f"sr-feedback-card-{ex_id}")
            
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
            active.find_element(By.CSS_SELECTOR, ".sr-btn-submit").click()
            
            WebDriverWait(driver, 20).until(
                lambda d: "is-success" in fb_card.get_attribute("class") and "is-visible" in fb_card.get_attribute("class")
            )
            time.sleep(0.5)
        
        # 1. Complete Ex 1
        complete_active("18 + 12")
        assert next_btn.get_attribute("disabled") is None, "Next button should be enabled after Ex 1 completion"
        continue_bottom = driver.find_element(By.ID, "sr-btn-continue-bottom")
        assert "is-visible" in continue_bottom.get_attribute("class"), "Continue button at bottom should be visible"
        print("Ex 1 Completed -> Next & Continue Enabled: PASS", flush=True)
        
        # 2. Navigate to Ex 2 via Next button click
        next_btn.click()
        time.sleep(1.0)
        assert "2/4" in title_el.text, f"Expected 2/4 in title: {title_el.text}"
        assert prev_btn.get_attribute("disabled") is None, "Prev button should be enabled on Ex 2"
        assert next_btn.get_attribute("disabled") is not None, "Next button should be disabled before Ex 2 completion"
        print("Navigated to Ex 2: PASS", flush=True)
        
        # 3. Complete Ex 2
        complete_active("25 + 17")
        assert next_btn.get_attribute("disabled") is None, "Next button should be enabled after Ex 2 completion"
        print("Ex 2 Completed -> Next Enabled: PASS", flush=True)
        
        # 4. Navigate to Ex 3 via Bottom Continue button click
        continue_bottom.click()
        time.sleep(1.0)
        assert "3/4" in title_el.text, f"Expected 3/4 in title: {title_el.text}"
        assert prev_btn.get_attribute("disabled") is None, "Prev button should be enabled on Ex 3"
        assert next_btn.get_attribute("disabled") is not None, "Next button should be disabled before Ex 3 completion"
        print("Navigated to Ex 3 via Continue Bottom: PASS", flush=True)
        
        # 5. Complete Ex 3
        complete_active("numero_estudiantes <- 120")
        assert next_btn.get_attribute("disabled") is None, "Next button should be enabled after Ex 3 completion"
        print("Ex 3 Completed -> Next Enabled: PASS", flush=True)
        
        # 6. Navigate to Ex 4
        next_btn.click()
        time.sleep(1.0)
        assert "4/4" in title_el.text, f"Expected 4/4 in title: {title_el.text}"
        assert next_btn.get_attribute("disabled") is not None, "Next button should be disabled on last exercise"
        print("Navigated to Ex 4: PASS", flush=True)
        
        # 7. Complete Ex 4
        complete_active("edad_promedio <- 21.4")
        pct_text = driver.find_element(By.ID, "sr-progress-pct").text
        assert "100%" in pct_text, f"Expected 100% progress: {pct_text}"
        print(f"Ex 4 Completed -> Final Progress: {pct_text}: PASS", flush=True)
        
        # 8. Test Stepper backward navigation to Ex 1
        steps = driver.find_elements(By.CSS_SELECTOR, ".sr-step-node")
        assert len(steps) == 4, f"Expected 4 step nodes, found {len(steps)}"
        steps[0].click()
        time.sleep(0.8)
        assert "1/4" in title_el.text, "Stepper should navigate back to Ex 1"
        print("Stepper click navigation: PASS", flush=True)

        print("\n=======================================================")
        print("NAVIGATION & PROGRESS SUITE (v0.3.7.4 Checkpoint C): 4/4 PASS")
        print("=======================================================\n", flush=True)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
