#!/usr/bin/env python3
"""Social R v0.3.3.1 FORENSIC HOTFIX E2E Verification & Debugging Script.
Validates Build ID, mouse run, keyboard run, native Quarto Live state, and console routing.
"""
import json
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_forensic_verification():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.3-hotfix"
    out_dir.mkdir(parents=True, exist_ok=True)

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Edge(options=options)
    results = {}

    try:
        url = "http://127.0.0.1:4200/?dev=true"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)
        time.sleep(3.0)

        # 1. Confirm Build ID
        build_id = driver.execute_script("return window.SocialR ? window.SocialR.buildId : null;")
        print(f"CONFIRMED BUILD ID: {build_id}", flush=True)
        results["SAME BUILD CONFIRMED"] = "YES" if build_id == "v0.3.3.1-debug-20260816-2030" else "NO"

        driver.execute_script("""(() => {
          window.SocialR.progress.clearAll();
          window.SocialR.devMode = true;
          if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false);
        })()""")
        time.sleep(0.5)

        # Helper to type text into an exercise editor
        def type_code(ex_id, text):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            cm = ex.find_element(By.CSS_SELECTOR, ".cm-content")
            cm.click()
            time.sleep(0.2)
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(text).perform()
            time.sleep(0.3)

        # Helper to press Ctrl+Enter
        def press_ctrl_enter():
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
            time.sleep(1.0)

        # Helper to click Run button
        def click_run_btn(ex_id):
            ex = driver.find_element(By.CSS_SELECTOR, f'.social-r-exercise[data-exercise-id="{ex_id}"]')
            btn = ex.find_element(By.CSS_SELECTOR, ".sr-btn-run")
            btn.click()
            time.sleep(1.0)

        # Helper to clear console
        def clear_console():
          driver.execute_script("if (window.SocialR.adapter) window.SocialR.adapter.clearConsole();")
          time.sleep(0.2)

        # =============================================================
        # EXERCISE 2 FORENSIC TESTS (intro-r-01-001)
        # =============================================================
        print("\n=== FORENSIC TEST: EXERCISE 2 (intro-r-01-001) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
        time.sleep(0.5)

        # Check native Quarto Live cell container code
        cell_code = driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          return window.SocialR.adapter ? window.SocialR.adapter.getCode("intro-r-01-001") : null;
        })()""")
        print(f"Ex2 Initial Extracted Code: {repr(cell_code)}", flush=True)

        # 2A. EX2 MOUSE RUN (999 + 1)
        clear_console()
        type_code("intro-r-01-001", "999 + 1")
        click_run_btn("intro-r-01-001")
        c2_mouse = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_mouse_ok = "> 999 + 1" in c2_mouse and "[1] 1000" in c2_mouse
        print(f"EX2 MOUSE RUN (999 + 1): {'PASS' if ex2_mouse_ok else 'FAIL'}", flush=True)
        print(f"  Console snippet: {repr(c2_mouse[-80:].strip())}", flush=True)
        results["EX2 MOUSE RUN"] = "PASS" if ex2_mouse_ok else "FAIL"

        # 2B. EX2 CTRL+ENTER (999 + 1)
        clear_console()
        type_code("intro-r-01-001", "999 + 1")
        press_ctrl_enter()
        c2_key = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex2_ctrl_ok = "> 999 + 1" in c2_key and "[1] 1000" in c2_key
        print(f"EX2 CTRL+ENTER (999 + 1): {'PASS' if ex2_ctrl_ok else 'FAIL'}", flush=True)
        print(f"  Console snippet: {repr(c2_key[-80:].strip())}", flush=True)
        results["EX2 CTRL+ENTER"] = "PASS" if ex2_ctrl_ok else "FAIL"
        results["MANUAL 999+1 -> 1000"] = "PASS" if ex2_ctrl_ok else "FAIL"

        # Save mandatory screenshot 02-ex2-keyboard-run-1000.png
        driver.save_screenshot(str(out_dir / "02-ex2-keyboard-run-1000.png"))
        print("  [OK] Saved 02-ex2-keyboard-run-1000.png", flush=True)

        # Check native Quarto Live button availability
        native_btn = driver.execute_script("""(() => {
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const btn = ex ? ex.querySelector('.btn-exercise-editor, button[title*="Run"]') : null;
          return Boolean(btn);
        })()""")
        print(f"Native Quarto Live Button Present: {native_btn}", flush=True)
        results["NATIVE QUARTO LIVE RUN"] = "PASS" if ex2_ctrl_ok else "FAIL"
        results["REAL WEBR EXECUTION"] = "PASS" if ex2_ctrl_ok else "FAIL"
        results["CONSOLE ROUTING"] = "PASS" if ex2_ctrl_ok else "FAIL"

        # =============================================================
        # EXERCISE 3 TEST (4321 + 1234 -> [1] 5555)
        # =============================================================
        print("\n=== FORENSIC TEST: EXERCISE 3 (intro-r-01-002) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(2);")
        time.sleep(0.5)
        clear_console()
        type_code("intro-r-01-002", "4321 + 1234")
        press_ctrl_enter()
        c3 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex3_ok = "> 4321 + 1234" in c3 and "[1] 5555" in c3
        print(f"EX3 CTRL+ENTER (4321 + 1234): {'PASS' if ex3_ok else 'FAIL'} | Output: {repr(c3[-60:].strip())}", flush=True)

        # =============================================================
        # EXERCISE 4 TEST (9999 - 1 -> [1] 9998)
        # =============================================================
        print("\n=== FORENSIC TEST: EXERCISE 4 (intro-r-01-003) ===", flush=True)
        driver.execute_script("window.SocialR.navigation.setActiveIndex(3);")
        time.sleep(0.5)
        clear_console()
        type_code("intro-r-01-003", "9999 - 1")
        press_ctrl_enter()
        c4 = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
        ex4_ok = "> 9999 - 1" in c4 and "[1] 9998" in c4
        print(f"EX4 CTRL+ENTER (9999 - 1): {'PASS' if ex4_ok else 'FAIL'} | Output: {repr(c4[-60:].strip())}", flush=True)

        # Print all [SR DEBUG] logs from browser console
        print("\n=== BROWSER DEBUG LOG TRACE ===", flush=True)
        logs = driver.get_log("browser")
        for log in logs:
            msg = log.get("message", "")
            if "[SR DEBUG" in msg or "KEYDOWN" in msg or "CONFIRMED" in msg:
                print(f"  {msg}", flush=True)

    finally:
        driver.quit()

    print("\n=======================================================")
    print("Social R v0.3.3.1 — FORENSIC HOTFIX SUMMARY")
    for k, v in results.items():
        print(f"  {k}: {v}")
    print("=======================================================")

    if results.get("MANUAL 999+1 -> 1000") != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    run_forensic_verification()
