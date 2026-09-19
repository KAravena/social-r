#!/usr/bin/env python3
"""Social R v0.3.4 Gate Test: Native Quarto Live Run across Exercises 1, 2, 3, 4."""
import json
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_native_gate():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    native_results = {}

    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        driver.execute_script("window.SocialR.devMode = true;")

        def type_code(ex_id, text):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
            cm.click()
            time.sleep(0.2)
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
            time.sleep(0.3)

        def click_native_run(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            # Quarto Live native run button inside card-footer or btn-exercise-editor
            btn = ex.find_element(By.CSS_SELECTOR, ".btn-exercise-editor.btn-primary, button[title*='Run']")
            btn.click()
            time.sleep(1.0)

        # Ex 1 Native Run
        driver.execute_script("window.SocialR.navigation.setActiveIndex(0);")
        time.sleep(0.5)
        type_code("intro-r-01-000", "18 + 12")
        click_native_run("intro-r-01-000")
        ex1_el = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-000"]')
        out1 = ex1_el.find_element(By.CSS_SELECTOR, ".cell-output, .exercise-cell-output, .card-footer").text
        ex1_pass = "[1] 30" in out1 or "30" in out1
        native_results["Exercise 1"] = "PASS" if ex1_pass else "FAIL"
        print(f"Ex 1 Native Run: {native_results['Exercise 1']} | Output: {repr(out1.strip())}", flush=True)

        # Ex 2 Native Run (999 + 1)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.5)
        type_code("intro-r-01-001", "999 + 1")
        click_native_run("intro-r-01-001")
        ex2_el = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-001"]')
        out2 = ex2_el.find_element(By.CSS_SELECTOR, ".cell-output, .exercise-cell-output, .card-footer").text
        ex2_pass = "[1] 1000" in out2 or "1000" in out2
        native_results["Exercise 2"] = "PASS" if ex2_pass else "FAIL"
        print(f"Ex 2 Native Run (999 + 1): {native_results['Exercise 2']} | Output: {repr(out2.strip())}", flush=True)

        # Ex 3 Native Run (4321 + 1234)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.5)
        type_code("intro-r-01-002", "4321 + 1234")
        click_native_run("intro-r-01-002")
        ex3_el = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-002"]')
        out3 = ex3_el.find_element(By.CSS_SELECTOR, ".cell-output, .exercise-cell-output, .card-footer").text
        ex3_pass = "[1] 5555" in out3 or "5555" in out3
        native_results["Exercise 3"] = "PASS" if ex3_pass else "FAIL"
        print(f"Ex 3 Native Run (4321 + 1234): {native_results['Exercise 3']} | Output: {repr(out3.strip())}", flush=True)

        # Ex 4 Native Run (9999 - 1)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.5)
        type_code("intro-r-01-003", "9999 - 1")
        click_native_run("intro-r-01-003")
        ex4_el = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-003"]')
        out4 = ex4_el.find_element(By.CSS_SELECTOR, ".cell-output, .exercise-cell-output, .card-footer").text
        ex4_pass = "[1] 9998" in out4 or "9998" in out4
        native_results["Exercise 4"] = "PASS" if ex4_pass else "FAIL"
        print(f"Ex 4 Native Run (9999 - 1): {native_results['Exercise 4']} | Output: {repr(out4.strip())}", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("NATIVE QUARTO LIVE RUN GATE RESULTS:")
    print(json.dumps(native_results, indent=2))
    print("=======================================================")

    all_pass = all(v == "PASS" for v in native_results.values())
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    run_native_gate()
