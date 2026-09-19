#!/usr/bin/env python3
"""Deep diagnostic script for Quarto Live, CodeMirror, webR, and grading."""
import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions


def run_diag():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)

    try:
        url = "http://127.0.0.1:4200/"
        print(f"Connecting to {url}...", flush=True)
        driver.get(url)

        # Wait for webR to finish loading packages
        print("Waiting for webR initialization...", flush=True)
        time.sleep(5.0)

        # 1. Inspect cards and parent values
        card_info = driver.execute_script("""
            const cards = Array.from(document.querySelectorAll('.card.exercise-editor'));
            return cards.map((c, i) => {
                const parent = c.parentElement;
                return {
                    index: i,
                    cardClass: c.className,
                    hasParentVal: !!(parent && parent.value),
                    parentValCode: parent && parent.value ? parent.value.code : null,
                    runBtn: !!c.querySelector('.exercise-editor-btn-run-code'),
                    startOverBtn: !!c.querySelector('.btn-exercise-editor.btn-outline-dark')
                };
            });
        """)
        print("\n=== CARD & PARENT VALUES ===", flush=True)
        print(json.dumps(card_info, indent=2), flush=True)

        # 2. Test clicking Quarto Live's native Run Code button
        print("\nTriggering native Run Code on Ex 0...", flush=True)
        driver.execute_script("""
            const card = document.querySelector('.card.exercise-editor');
            const runBtn = card ? card.querySelector('.exercise-editor-btn-run-code') : null;
            if (runBtn) {
                runBtn.click();
            }
        """)

        time.sleep(2.0)

        # 3. Inspect generated outputs and cell containers
        outputs = driver.execute_script("""
            const outEls = Array.from(document.querySelectorAll('.cell-output, .exercise-cell-output, .exercise-grade, .cell-output-container'));
            return outEls.map(el => ({
                tag: el.tagName,
                className: el.className,
                text: el.textContent.trim(),
                html: el.innerHTML.slice(0, 150)
            }));
        """)
        print("\n=== OUTPUTS AFTER NATIVE RUN ===", flush=True)
        print(json.dumps(outputs, indent=2), flush=True)

        # 4. Check how Social R's MutationObserver captures or processes outputs
        social_state = driver.execute_script("""
            const consoleBody = document.getElementById('sr-console-body');
            const feedbackCard = document.getElementById('sr-feedback-card-intro-r-01-000');
            const progress = window.SocialR ? window.SocialR.progress.get('intro-r-01-000') : null;
            return {
                consoleHtml: consoleBody ? consoleBody.innerHTML : null,
                consoleText: consoleBody ? consoleBody.textContent : null,
                feedbackClass: feedbackCard ? feedbackCard.className : null,
                feedbackHtml: feedbackCard ? feedbackCard.innerHTML : null,
                progress
            };
        """)
        print("\n=== SOCIAL R STATE AFTER RUN ===", flush=True)
        print(json.dumps(social_state, indent=2), flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    run_diag()
