#!/usr/bin/env python3
"""QA and Visual Verification for Redesigned M06 in Social R."""

import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200/curso.html"
SCREENSHOTS_DIR = Path("tests/screenshots/m06")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORTS = [
    {"name": "1690x860", "width": 1690, "height": 860},
    {"name": "1440x900", "width": 1440, "height": 900},
    {"name": "1366x768", "width": 1366, "height": 768},
]

EXERCISES_TO_CAPTURE = [
    ("intro-r-06-001", "m06_e1_el_valor_que_no_esta"),
    ("intro-r-06-005", "m06_e5_casos_completos_e_incompletos"),
    ("intro-r-06-007", "m06_e7_checkpoint_b_decidir_frente_a_datos_ausentes"),
]


async def run_visual_and_functional_qa():
    print("=== Starting M06 QA and Visual Verification ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for vp in VIEWPORTS:
            print(f"\n--- Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
            context = await browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = await context.new_page()

            # Enable local preview bypass and dismiss tour
            await page.add_init_script("""
                localStorage.setItem('social-r:tour-completed', 'true');
                localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            """)

            # Navigate to first exercise in M06
            await page.goto(f"{BASE_URL}#intro-r-06-001")
            await page.wait_for_selector(".social-r-exercise.is-active-exercise", timeout=15000)
            await page.wait_for_timeout(1000)

            # Capture screenshots for the 3 target exercises
            for ex_id, slug in EXERCISES_TO_CAPTURE:
                # Navigate to exercise via hash
                await page.evaluate(f"window.location.hash = '{ex_id}'")
                await page.wait_for_timeout(800)

                # Ensure active exercise has data-exercise-id matching ex_id
                active_id = await page.evaluate("document.querySelector('.social-r-exercise.is-active-exercise')?.getAttribute('data-exercise-id')")
                print(f"  Active exercise: {active_id} (target: {ex_id})")

                # Verify lesson panel scroll state
                panel_scrollable = await page.evaluate("""() => {
                    const panel = document.querySelector('.social-r-exercise.is-active-exercise .sr-lesson-panel');
                    if (!panel) return false;
                    return panel.scrollHeight > panel.clientHeight;
                }""")
                print(f"  [{vp['name']}] Exercise {ex_id}: Lesson panel scrollable? {panel_scrollable}")

                # Save screenshot
                screenshot_path = SCREENSHOTS_DIR / f"{slug}_{vp['name']}.png"
                await page.screenshot(path=str(screenshot_path))
                print(f"  Saved screenshot: {screenshot_path}")

            await context.close()

        print("\n=== Testing Exercise Navigation and Traversal within M06 ===")
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
        """)
        await page.goto(f"{BASE_URL}#intro-r-06-001")
        await page.wait_for_selector(".social-r-exercise.is-active-exercise")

        # Check all 7 exercises exist in M06 in the DOM
        m6_exercises = await page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('.social-r-exercise[data-module-id="06-trabajar-cuando-faltan-datos"]'));
            return all.map(el => ({
                id: el.getAttribute('data-exercise-id'),
                title: el.querySelector('.sr-lesson-title')?.textContent?.trim()
            }));
        }""")
        print(f"Found {len(m6_exercises)} exercises in M06:")
        for idx, ex in enumerate(m6_exercises, 1):
            print(f"  {idx}. {ex['id']} - {ex['title']}")
        assert len(m6_exercises) == 7, f"Expected 7 exercises in M06, found {len(m6_exercises)}"

        # Check M06 stepper in bottombar
        step_nodes = await page.query_selector_all(".sr-bottom-module-step")
        print(f"Bottombar stepper nodes for M06: {len(step_nodes)}")
        assert len(step_nodes) == 7, f"Expected 7 step nodes in M06 stepper, found {len(step_nodes)}"

        await context.close()
        await browser.close()
    print("\n=== M06 QA and Visual Verification COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    asyncio.run(run_visual_and_functional_qa())
