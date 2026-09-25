#!/usr/bin/env python3
"""Automated QA and Visual Verification for Pedagogical Data Tables in Social R."""

import asyncio
import os
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200/curso.html"
SCREENSHOTS_DIR = Path("tests/screenshots/tables")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORTS = [
    {"name": "1690x860", "width": 1690, "height": 860},
    {"name": "1440x900", "width": 1440, "height": 900},
    {"name": "1366x768", "width": 1366, "height": 768},
    {"name": "390x844", "width": 390, "height": 844},
]

# Exercises that had the typo and general table exercises
TEST_EXERCISES = [
    ("intro-r-07-002", "Módulo 7 Ejercicio 2 (Caso obligatorio)"),
    ("intro-r-05-008", "Módulo 5 Ejercicio 8 (Checkpoint B)"),
    ("intro-r-08-001", "Módulo 8 Ejercicio 1 (Distribución)"),
    ("intro-r-04-003", "Módulo 4 Ejercicio 3 (Head)"),
]


async def run_tables_qa():
    print("=== Starting Pedagogical Tables Verification ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for vp in VIEWPORTS:
            print(f"\n--- Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
            context = await browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = await context.new_page()

            # Bypass tour and onboarding
            await page.add_init_script("""
                localStorage.setItem('social-r:tour-completed', 'true');
                localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            """)

            for ex_id, desc in TEST_EXERCISES:
                await page.goto(f"{BASE_URL}#{ex_id}")
                await page.wait_for_selector(f"#ex-{ex_id}.is-active-exercise", timeout=15000)
                await page.wait_for_timeout(500)

                ex_locator = page.locator(f"#ex-{ex_id}")

                # 1. Verify NO raw pipes or alignment dashes appear in text content
                panel_text = await ex_locator.locator(".sr-lesson-panel").text_content()
                assert "|:---" not in panel_text, f"[{ex_id}] Raw separator found in text!"
                assert "|:—" not in panel_text, f"[{ex_id}] Em-dash raw separator found in text!"
                assert "| id | edad" not in panel_text, f"[{ex_id}] Raw header text found!"

                # 2. Verify table exists inside .sr-data-table-wrap
                wrap = ex_locator.locator(".sr-data-table-wrap")
                wrap_count = await wrap.count()
                assert wrap_count >= 1, f"[{ex_id}] Expected at least 1 .sr-data-table-wrap, found {wrap_count}"

                table = wrap.locator("table")
                assert await table.count() >= 1, f"[{ex_id}] Table not found inside .sr-data-table-wrap"

                # 3. Verify semantic table elements
                headers = await table.locator("th").all_text_contents()
                headers_clean = [h.strip() for h in headers if h.strip()]
                print(f"  [{vp['name']}] {ex_id}: Table headers -> {headers_clean}")
                assert len(headers_clean) >= 3, f"[{ex_id}] Expected at least 3 headers, got {headers_clean}"

                # 4. Verify scope="col" on th
                th_elements = await table.locator("th").all()
                for th in th_elements:
                    scope = await th.get_attribute("scope")
                    assert scope == "col", f"[{ex_id}] th missing scope='col'"

                # 5. Check rows count
                rows = await table.locator("tbody tr").count()
                print(f"  [{vp['name']}] {ex_id}: Data rows -> {rows}")
                assert rows >= 4, f"[{ex_id}] Expected at least 4 rows, found {rows}"

                # 6. Check geometry and overflow
                # Wrap width should not exceed viewport
                wrap_box = await wrap.first.bounding_box()
                panel_box = await ex_locator.locator(".sr-lesson-panel").bounding_box()
                table_box = await table.first.bounding_box()

                assert wrap_box["width"] <= panel_box["width"] + 2, f"Wrap width ({wrap_box['width']}) overflows panel ({panel_box['width']})"

                # In desktop viewports (1440, 1690), the table fits without internal scroll
                if vp["width"] >= 1366 and ex_id == "intro-r-07-002":
                    table_fits = table_box["width"] <= wrap_box["width"] + 2
                    print(f"  [{vp['name']}] Table fits completely in container? {table_fits} (Table: {table_box['width']}px, Wrap: {wrap_box['width']}px)")
                    assert table_fits, f"Table should fit in wrap without horizontal scroll on desktop"

                # 7. Verify Task section heading is visible
                task_heading = ex_locator.locator("h4.sr-task-heading")
                assert await task_heading.is_visible(), f"[{ex_id}] Task heading must be visible"

                # Capture screenshot for M7-E2
                if ex_id == "intro-r-07-002":
                    screenshot_path = SCREENSHOTS_DIR / f"m07_e2_table_{vp['name']}.png"
                    await page.screenshot(path=str(screenshot_path))
                    print(f"  [Screenshot] Saved: {screenshot_path}")

            await context.close()

        await browser.close()
    print("\n=== All Pedagogical Table QA Checks PASSED Successfully! ===")


if __name__ == "__main__":
    asyncio.run(run_tables_qa())
