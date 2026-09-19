#!/usr/bin/env python3
"""Diagnostic script for Social R v0.3.3 keyboard shortcuts bug."""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions


def diagnose():
    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")

    driver = webdriver.Edge(options=options)
    try:
        url = "http://127.0.0.1:4200/"
        print(f"Loading {url}...", flush=True)
        driver.get(url)
        time.sleep(3.5)

        ex_ids = ["intro-r-01-000", "intro-r-01-001", "intro-r-01-002", "intro-r-01-003"]

        for idx, ex_id in enumerate(ex_ids):
            print(f"\n--- Testing Exercise {idx}: {ex_id} ---", flush=True)

            # Navigate to exercise
            driver.execute_script(f"window.SocialR.navigation.setActiveIndex({idx});")
            time.sleep(0.5)

            # Check DOM container & CodeMirror
            info = driver.execute_script(f"""(() => {{
                const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
                const cmContent = ex ? ex.querySelector('.cm-content') : null;
                const cmEditor = ex ? ex.querySelector('.cm-editor') : null;
                const activeNav = window.SocialR.navigation.getCurrentExercise();
                const activeId = window.SocialR.navigation.getActiveExerciseId ? window.SocialR.navigation.getActiveExerciseId() : (activeNav ? activeNav.id : null);
                
                return {{
                    exFound: Boolean(ex),
                    isActiveClass: ex ? ex.classList.contains('is-active-exercise') : false,
                    cmContentFound: Boolean(cmContent),
                    cmEditorFound: Boolean(cmEditor),
                    linesCount: cmContent ? cmContent.querySelectorAll('.cm-line').length : 0,
                    codeRead: window.SocialR.adapter.getCode('{ex_id}'),
                    activeId
                }};
            }})()""")
            print(f"Container info: {info}", flush=True)

            # Focus the cm-content element
            driver.execute_script(f"""(() => {{
                const ex = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"]');
                const cmContent = ex ? ex.querySelector('.cm-content') : null;
                if (cmContent) {{
                    cmContent.focus();
                }}
            }})()""")
            time.sleep(0.2)

            # Send Ctrl+Enter via Selenium ActionChains / SendKeys to activeElement
            try:
                active_el = driver.switch_to.active_element
                active_el.send_keys(Keys.CONTROL, Keys.ENTER)
                time.sleep(0.8)
            except Exception as err:
                print(f"Send keys error: {err}", flush=True)

            # Read console output
            console_txt = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
            print(f"Console Output after Ctrl+Enter:\n{console_txt.strip()[-150:]}", flush=True)

            # Test Run Button click for comparison
            driver.execute_script(f"""(() => {{
                const btn = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"] .sr-btn-run');
                if (btn) btn.click();
            }})()""")
            time.sleep(0.8)

            console_txt_after_btn = driver.execute_script("return document.getElementById('sr-console-body').textContent;")
            print(f"Console Output after Run Button Click:\n{console_txt_after_btn.strip()[-150:]}", flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    diagnose()
