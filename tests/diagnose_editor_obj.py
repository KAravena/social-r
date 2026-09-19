#!/usr/bin/env python3
"""Diagnostic script for _webr_editor methods in Observable mainModule scope."""
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
        try {
          const mod = window._ojs.ojsConnector.mainModule;
          const edObj = mod._scope.get("_webr_editor_3")._value;
          const proto = edObj ? Object.getPrototypeOf(edObj) : null;
          const methods = proto ? Object.getOwnPropertyNames(proto) : [];
          const ownKeys = edObj ? Object.keys(edObj) : [];
          return {
            hasEd: !!edObj,
            ownKeys,
            methods,
            edObjType: edObj ? edObj.constructor.name : null
          };
        } catch(e) {
          return { error: e.message || String(e) };
        }
      })();
    """)
    print("\n--- WEBR EDITOR OBJECT METHODS ---")
    print(res)

finally:
    driver.quit()
