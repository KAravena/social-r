#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

options = EdgeOptions()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1440,900")

driver = webdriver.Edge(options=options)
try:
    driver.get("http://127.0.0.1:4200/?dev=true")
    time.sleep(3.0)

    res = driver.execute_script("""(() => {
        const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-001"]');
        const card = ex.querySelector('.card.exercise-editor');
        const cmEditor = ex.querySelector('.cm-editor');
        const parent = card ? card.parentElement : null;
        
        const parentKeys = parent ? Object.keys(parent) : [];
        const cmKeys = cmEditor ? Object.keys(cmEditor) : [];

        let viewFound = false;
        if (cmEditor && cmEditor.cmView) viewFound = true;
        
        return {
            parentKeys,
            cmKeys,
            viewFound,
            hasValue: Boolean(parent && parent.value),
            valueKeys: (parent && parent.value) ? Object.keys(parent.value) : []
        };
    })()""")
    print("Inspection result:", res)
finally:
    driver.quit()
