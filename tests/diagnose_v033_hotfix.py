#!/usr/bin/env python3
"""Social R v0.3.3 HOTFIX Diagnostic Script.
Simulates human interactions (click, typing, Ctrl+Enter) and reads all console logs.
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_diagnostics():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Edge(options=options)
    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        # Ensure devMode
        driver.execute_script("window.SocialR.devMode = true;")

        print("\n--- TEST 1: Exercise 1 (18 + 12) ---", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.5)

        # Focus Ex1 editor and press Ctrl+Enter via ActionChains (real keyboard simulation)
        ex1 = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-000"]')
        cm1 = ex1.find_element(By.CSS_SELECTOR, ".cm-content")
        cm1.click()
        time.sleep(0.2)

        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys("18 + 12").perform()
        time.sleep(0.3)

        # Press Ctrl+Enter
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(1.0)

        c_txt1 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        print(f"Ex1 Console Output: {repr(c_txt1[-80:].strip())}", flush=True)

        print("\n--- TEST 2: Exercise 2 (999 + 1) ---", flush=True)
        # Navigate to Exercise 2 without refresh
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.5)

        ex2 = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-001"]')
        cm2 = ex2.find_element(By.CSS_SELECTOR, ".cm-content")
        cm2.click()
        time.sleep(0.2)

        # Type 999 + 1
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys("999 + 1").perform()
        time.sleep(0.3)

        # Press Ctrl+Enter
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(1.0)

        c_txt2 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        print(f"Ex2 Console Output: {repr(c_txt2[-80:].strip())}", flush=True)

        # Print all browser console logs
        print("\n=== BROWSER CONSOLE LOGS ===", flush=True)
        logs = driver.get_log("browser")
        for log in logs:
          msg = log.get("message", "")
          if "SocialR" in msg or "KEYDOWN" in msg or "webR" in msg:
            print(f"  {msg}", flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    run_diagnostics()
