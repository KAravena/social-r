#!/usr/bin/env python3
"""Diagnostic script for .cell-output-container text after native click."""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions

options = EdgeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Edge(options=options)
try:
    driver.get("http://127.0.0.1:4200/?dev=true")
    time.sleep(4.0)

    # 0. Set active index 1 (exercise 2)
    driver.execute_script("window.SocialR.navigation.setActiveIndex(1);")
    time.sleep(0.5)

    # 1. Type 999 + 1 in Ex2
    driver.execute_script("""
      const cm = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"] .cm-editor');
      if (cm && cm.cmView && cm.cmView.view) {
        cm.cmView.view.dispatch({ changes: { from: 0, to: cm.cmView.view.state.doc.length, insert: "999 + 1" } });
      }
    """)
    time.sleep(0.3)

    # 2. Click native Run Code button via JS click
    ex2 = driver.find_element(By.CSS_SELECTOR, '.social-r-exercise[data-exercise-id="intro-r-01-001"]')
    run_btn = ex2.find_element(By.CSS_SELECTOR, ".exercise-editor-btn-run-code, .btn-exercise-editor.btn-primary, a[title*='Run']")
    driver.execute_script("arguments[0].click();", run_btn)
    time.sleep(3.5)

    # 3. Check cell-output-container text
    out = driver.execute_script("""
      const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
      const container = ex.querySelector('.cell-output-container, .cell-output, .exercise-cell-output');
      return {
        hasContainer: !!container,
        containerCls: container ? container.className : null,
        text: container ? container.textContent : null,
        html: container ? container.innerHTML : null
      };
    """)
    print("\n--- NATIVE CELL OUTPUT CONTAINER RESULT ---")
    print(out)

finally:
    driver.quit()
