#!/usr/bin/env python3
"""Diagnostic script for Observable viewof editor variable update."""
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
      return (async () => {
        try {
          const mod = window._ojs.ojsConnector.mainModule;
          const varObj = mod._scope.get("viewof _webr_editor_3");
          const edContainer = varObj ? varObj._value : null;
          
          if (!edContainer) return { error: "varObj or _value not found" };

          edContainer.value.code = "999 + 1";
          edContainer.dispatchEvent(new CustomEvent("input", { detail: { commit: true }, bubbles: true }));

          await new Promise(r => setTimeout(r, 2500));
          const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
          const out = ex.querySelector('.cell-output, .exercise-cell-output');
          return {
            hasOut: !!out,
            outTag: out ? out.tagName : null,
            outCls: out ? out.className : null,
            outText: out ? out.textContent : null,
            outHtml: out ? out.innerHTML : null
          };
        } catch(e) {
          return { error: e.message || String(e) };
        }
      })();
    """)
    print("\n--- OBSERVABLE VIEWOF UPDATE RESULT ---")
    print(res)

finally:
    driver.quit()
