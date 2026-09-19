#!/usr/bin/env python3
"""Capture state-progression screenshots for Social R v0.3.2 (Positron Light Theme)."""
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions


def capture_all():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.2"
    out_dir.mkdir(parents=True, exist_ok=True)

    url = "http://127.0.0.1:4200/"

    options = EdgeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1440,900")
    driver = webdriver.Edge(options=options)

    try:
        driver.get(url)
        time.sleep(3.0)
        driver.execute_script("(() => { window.SocialR.progress.clearAll(); if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false); })()")
        time.sleep(0.5)

        # 01-exercise-initial-light.png
        p01 = out_dir / "01-exercise-initial-light.png"
        driver.save_screenshot(str(p01))
        print(f"[OK] Saved: 01-exercise-initial-light.png", flush=True)

        # 02-run-console-output.png (Run 25 + 17)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "25 + 17";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p02 = out_dir / "02-run-console-output.png"
        driver.save_screenshot(str(p02))
        print(f"[OK] Saved: 02-run-console-output.png", flush=True)

        # 03-submit-incorrect.png (Submit 25 + 16)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "25 + 16";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p03 = out_dir / "03-submit-incorrect.png"
        driver.save_screenshot(str(p03))
        print(f"[OK] Saved: 03-submit-incorrect.png", flush=True)

        # 04-submit-correct.png (Submit 18 + 12)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 12";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submitCode('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p04 = out_dir / "04-submit-correct.png"
        driver.save_screenshot(str(p04))
        print(f"[OK] Saved: 04-submit-correct.png", flush=True)

        # 05-object-assignment.png (Exercise 2 numero_estudiantes <- 120)
        driver.execute_script("(() => { window.SocialR.navigation.setActiveIndex(2); })()")
        time.sleep(0.4)
        driver.execute_script("""(() => {
          const ex2 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-002"]');
          const cmContent = ex2.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "numero_estudiantes <- 120";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-002');
        })()""")
        time.sleep(0.8)
        p05 = out_dir / "05-object-assignment.png"
        driver.save_screenshot(str(p05))
        print(f"[OK] Saved: 05-object-assignment.png", flush=True)

        # 06-r-error.png (R Error objeto_inexistente)
        driver.execute_script("""(() => {
          const ex2 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-002"]');
          const cmContent = ex2.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "objeto_inexistente";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.runCode('intro-r-01-002');
        })()""")
        time.sleep(0.8)
        p06 = out_dir / "06-r-error.png"
        driver.save_screenshot(str(p06))
        print(f"[OK] Saved: 06-r-error.png", flush=True)

        # 07-course-outline.png (Open drawer)
        driver.execute_script("""(() => {
          const backdrop = document.getElementById('sr-drawer-backdrop');
          if (backdrop) backdrop.classList.add('is-open');
        })()""")
        time.sleep(0.4)
        p07 = out_dir / "07-course-outline.png"
        driver.save_screenshot(str(p07))
        print(f"[OK] Saved: 07-course-outline.png", flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_all()
