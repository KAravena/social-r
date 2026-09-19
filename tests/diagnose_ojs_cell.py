#!/usr/bin/env python3
"""Diagnostic script for Quarto Live OJS cell bindings and execution triggers."""
import time
from selenium import webdriver
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

    res = driver.execute_script("""
      return (() => {
        const ex2 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
        const runBtn = ex2.querySelector('.btn-exercise-editor, .exercise-editor-btn-run-code, a[title*="Run"], button[title*="Run"]');
        
        // Inspect OJS connector & scope
        const scope = window._ojs && window._ojs.ojsConnector && window._ojs.ojsConnector.mainModule ? Array.from(window._ojs.ojsConnector.mainModule._scope.keys()) : [];
        
        // Inspect cell element properties
        const cell = ex2.querySelector('.exercise-cell, div[id^="webr-"]');
        const parent = cell ? cell.parentElement : null;
        
        return {
          btnTag: runBtn ? runBtn.tagName : null,
          btnClass: runBtn ? runBtn.className : null,
          btnText: runBtn ? runBtn.textContent : null,
          scopeKeys: scope.filter(k => k.includes("webr") || k.includes("intro")),
          cellId: cell ? cell.id : null,
          parentValueKeys: parent && parent.value ? Object.keys(parent.value) : []
        };
      })();
    """)
    print("\n--- OJS CELL DIAGNOSTIC ---")
    print(res)

finally:
    driver.quit()
