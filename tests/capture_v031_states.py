#!/usr/bin/env python3
"""Capture multi-resolution and state-progression screenshots for Social R v0.3.1."""
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions


def capture_all():
    out_dir = Path(__file__).resolve().parents[1] / "docs" / "screenshots" / "v0.3.1"
    out_dir.mkdir(parents=True, exist_ok=True)

    url = "http://127.0.0.1:4200/"

    # Helper function for fresh browser
    def get_driver(width, height):
        options = EdgeOptions()
        options.page_load_strategy = "eager"
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument(f"--window-size={width},{height}")
        d = webdriver.Edge(options=options)
        d.get(url)
        time.sleep(3.0)
        return d

    # 1. Multi-resolution captures
    resolutions = [
        ("social-r-1366x768.png", 1366, 768),
        ("social-r-1440x900.png", 1440, 900),
        ("social-r-1920x1080.png", 1920, 1080),
    ]

    for fname, w, h in resolutions:
        driver = get_driver(w, h)
        try:
            driver.execute_script("(() => { window.SocialR.progress.clearAll(); if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false); })()")
            time.sleep(0.5)
            path = out_dir / fname
            driver.save_screenshot(str(path))
            print(f"[OK] Saved resolution screenshot: {fname} ({w}x{h})", flush=True)
        finally:
            driver.quit()

    # 2. State Progression captures at 1440x900
    driver = get_driver(1440, 900)
    try:
        driver.execute_script("(() => { window.SocialR.progress.clearAll(); if (window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0, false); })()")
        time.sleep(0.5)

        # 01-inicial.png
        p01 = out_dir / "01-inicial.png"
        driver.save_screenshot(str(p01))
        print(f"[OK] Saved state screenshot: 01-inicial.png", flush=True)

        # 02-run-output.png (Run code)
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.run('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p02 = out_dir / "02-run-output.png"
        driver.save_screenshot(str(p02))
        print(f"[OK] Saved state screenshot: 02-run-output.png", flush=True)

        # 03-feedback-incorrecto.png (Submit incorrect)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 11";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submit('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p03 = out_dir / "03-feedback-incorrecto.png"
        driver.save_screenshot(str(p03))
        print(f"[OK] Saved state screenshot: 03-feedback-incorrecto.png", flush=True)

        # 04-feedback-correcto.png (Submit correct)
        driver.execute_script("""(() => {
          const ex0 = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-01-000"]');
          const cmContent = ex0.querySelector('.cm-content');
          if (cmContent) cmContent.innerText = "18 + 12";
        })()""")
        driver.execute_script("""(async () => {
          await window.SocialR.adapter.submit('intro-r-01-000');
        })()""")
        time.sleep(0.8)
        p04 = out_dir / "04-feedback-correcto.png"
        driver.save_screenshot(str(p04))
        print(f"[OK] Saved state screenshot: 04-feedback-correcto.png", flush=True)

        # 05-course-outline.png (Open drawer)
        driver.execute_script("""(() => {
          const backdrop = document.getElementById('sr-drawer-backdrop');
          if (backdrop) backdrop.classList.add('is-open');
        })()""")
        time.sleep(0.4)
        p05 = out_dir / "05-course-outline.png"
        driver.save_screenshot(str(p05))
        print(f"[OK] Saved state screenshot: 05-course-outline.png", flush=True)

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_all()
