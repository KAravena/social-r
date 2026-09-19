#!/usr/bin/env python3
import json
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
    driver.get("http://127.0.0.1:4200/")
    time.sleep(4.0)

    res = driver.execute_script("""
        const card1 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"] .card.exercise-editor');
        const cmEl = card1 ? card1.querySelector('.cm-editor') : null;
        const cmContent = card1 ? card1.querySelector('.cm-content') : null;

        // CodeMirror 6 text extraction
        // cmContent.innerText in modern browsers gives line breaks accurately
        // Also check if we can get lines directly from .cm-line elements
        let lines = [];
        if (cmContent) {
            const lineEls = cmContent.querySelectorAll('.cm-line');
            lines = Array.from(lineEls).map(l => l.textContent);
        }

        return {
            cmContentInnerText: cmContent ? cmContent.innerText : null,
            lines: lines.join('\\n'),
            cardParentVal: card1 && card1.parentElement ? card1.parentElement.value : null
        };
    """)
    print("CodeMirror text:", json.dumps(res, indent=2))
finally:
    driver.quit()
