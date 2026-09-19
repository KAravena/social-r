#!/usr/bin/env python3
"""Capture visual snapshots of Social R at different resolutions using Selenium and Edge/Chrome."""
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "docs" / "screenshots" / "v0.3"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def get_driver():
    options = EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--hide-scrollbars")
    
    # Use system edge
    try:
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    except Exception as e:
        print(f"Fallback to direct webdriver.Edge(): {e}")
        driver = webdriver.Edge(options=options)
    return driver


def capture_all():
    resolutions = [
        (1366, 768, "social-r-v03-1366x768.png"),
        (1440, 900, "social-r-v03-1440x900.png"),
        (1920, 1080, "social-r-v03-1920x1080.png"),
    ]

    driver = get_driver()
    try:
        url = "http://localhost:4200/"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)  # Wait for webR initialization & DOM rendering

        for width, height, filename in resolutions:
            driver.set_window_size(width, height)
            time.sleep(1)
            filepath = SCREENSHOT_DIR / filename
            driver.save_screenshot(str(filepath))
            print(f"Saved snapshot: {filepath} ({width}x{height})")

    finally:
        driver.quit()


if __name__ == "__main__":
    capture_all()
