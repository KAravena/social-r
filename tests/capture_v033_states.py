#!/usr/bin/env python3
"""Capture state screenshots for Social R v0.3.3 keyboard execution across all 4 exercises."""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def capture_v033():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.3"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    try:
        url = "http://127.0.0.1:4200/?dev=true"
        driver.get(url)
        time.sleep(3.0)

        def type_code(ex_id, text):
            ex_el = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            cm = ex_el.find_element(By.CSS_SELECTOR, '.cm-content')
            cm.click()
            time.sleep(0.1)
            cm.send_keys(Keys.CONTROL, 'a')
            cm.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)
            cm.send_keys(text)
            time.sleep(0.2)

        def press_ctrl_enter():
            driver.execute_script("""(() => {
              const target = document.activeElement || window;
              target.dispatchEvent(new KeyboardEvent('keydown', {
                key: 'Enter', code: 'Enter', keyCode: 13, which: 13, ctrlKey: true, bubbles: true, cancelable: true, composed: true
              }));
            })()""")

        # Ex1 (intro-r-01-000)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.4)
        type_code("intro-r-01-000", "18 + 12")
        press_ctrl_enter()
        time.sleep(0.8)
        driver.save_screenshot(str(out_dir / "exercise-1-console.png"))
        print("[OK] Saved exercise-1-console.png", flush=True)

        # Ex2 (intro-r-01-001)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.4)
        type_code("intro-r-01-001", "25 + 17")
        press_ctrl_enter()
        time.sleep(0.8)
        driver.save_screenshot(str(out_dir / "exercise-2-console.png"))
        print("[OK] Saved exercise-2-console.png", flush=True)

        # Ex3 (intro-r-01-002)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.4)
        type_code("intro-r-01-002", "numero_estudiantes <- 120")
        press_ctrl_enter()
        time.sleep(0.8)
        driver.save_screenshot(str(out_dir / "exercise-3-console.png"))
        print("[OK] Saved exercise-3-console.png", flush=True)

        # Ex4 (intro-r-01-003)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.4)
        type_code("intro-r-01-003", "edad_promedio <- 21.4")
        press_ctrl_enter()
        time.sleep(0.8)
        driver.save_screenshot(str(out_dir / "exercise-4-console.png"))
        print("[OK] Saved exercise-4-console.png", flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_v033()
