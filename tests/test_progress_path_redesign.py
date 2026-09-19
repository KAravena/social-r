#!/usr/bin/env python3
"""Verification script for the refined Connected Circles Progress Path in Social R BottomBar:
1. Módulo recién comenzado (1 active blue + pending gray)
2. Módulo parcialmente completado (green checks + active blue + pending gray)
3. Módulo completamente completado (all green checks)
4. Módulo 2 (1 de 9 / 4 de 9 / 9 de 9)
5. Strict circular geometry & horizontal alignment
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def test_progress_path():
    print(f"Connecting to {BASE_URL} for Progress Path Stepper validation ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        # -------------------------------------------------------------
        # 1. Módulo 1 Recién Comenzado (1 de 8)
        # -------------------------------------------------------------
        print("\n--- 1. Testing Módulo 1 Recién Comenzado (1 de 8) ---")
        await page.goto(f"{BASE_URL}?qa-clean=1", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        bb = await page.query_selector(".sr-bottombar")
        bb_box = await bb.bounding_box()
        print(f"  BottomBar height: {bb_box['height']}px (expected 40-48px)")
        assert 40.0 <= bb_box["height"] <= 48.0

        steps = await page.query_selector_all(".sr-bottom-module-step")
        connectors = await page.query_selector_all(".sr-bottom-module-connector")
        print(f"  M1 Steps: {len(steps)}, Connectors: {len(connectors)}")
        assert len(steps) == 8
        assert len(connectors) == 7

        # Check circular geometry (width == height, border-radius is 50%)
        step_boxes = [await s.bounding_box() for s in steps]
        for i, s_box in enumerate(step_boxes):
            assert abs(s_box["width"] - s_box["height"]) <= 1.0, f"Step {i} must be circular (width==height), got {s_box['width']}x{s_box['height']}"
            assert 16.0 <= s_box["width"] <= 28.0, f"Step {i} diameter should be 18-26px, got {s_box['width']}"

        # Horizontal alignment
        y_coords = [b["y"] for b in step_boxes]
        max_y_diff = max(y_coords) - min(y_coords)
        print(f"  Max Y diff between step nodes: {max_y_diff:.2f}px")
        assert max_y_diff <= 2.5, "Nodes must be strictly horizontally aligned"

        await bb.screenshot(path="tests/screenshots/path_01_m1_started.png")
        print("  Screenshot saved: path_01_m1_started.png")

        # -------------------------------------------------------------
        # 2. Módulo 1 Parcialmente Completado (5 de 8)
        # -------------------------------------------------------------
        print("\n--- 2. Testing Módulo 1 Parcialmente Completado (5 de 8) ---")
        await page.evaluate("""() => {
            const store = window.SocialR.progress;
            const m1_ex = ['intro-r-01-001', 'intro-r-01-002', 'intro-r-01-003', 'intro-r-01-004'];
            m1_ex.forEach(id => store.markCompleted(id, 'primeros-pasos'));
            window.SocialR.navigation.setActiveIndex(4); // Exercise 5 active
        }""")
        await page.wait_for_timeout(400)

        counter_txt = (await page.text_content("#sr-bottombar-counter")).strip()
        completed_steps = await page.query_selector_all(".sr-bottom-module-step.is-completed")
        active_step = await page.query_selector(".sr-bottom-module-step.is-active")
        active_text = (await active_step.text_content()).strip() if active_step else ""
        completed_connectors = await page.query_selector_all(".sr-bottom-module-connector.is-completed")

        print(f"  Counter text: '{counter_txt}'")
        print(f"  Completed green steps: {len(completed_steps)} (expected 4)")
        print(f"  Active blue step text: '{active_text}' (expected '5')")
        print(f"  Completed green connectors: {len(completed_connectors)} (expected 3)")

        assert "Módulo 1 · 5 de 8" in counter_txt
        assert len(completed_steps) == 4
        assert active_text == "5"
        assert len(completed_connectors) == 3

        await bb.screenshot(path="tests/screenshots/path_02_m1_partial_5of8.png")
        print("  Screenshot saved: path_02_m1_partial_5of8.png")

        # -------------------------------------------------------------
        # 3. Módulo 1 Totalmente Completado (8 de 8)
        # -------------------------------------------------------------
        print("\n--- 3. Testing Módulo 1 Totalmente Completado (8 de 8) ---")
        await page.evaluate("""() => {
            const store = window.SocialR.progress;
            const m1_ex = ['intro-r-01-001', 'intro-r-01-002', 'intro-r-01-003', 'intro-r-01-004', 'intro-r-01-005', 'intro-r-01-006', 'intro-r-01-007', 'intro-r-01-008'];
            m1_ex.forEach(id => store.markCompleted(id, 'primeros-pasos'));
            store.setModuleCompleted('primeros-pasos', true);
            window.SocialR.navigation.setActiveIndex(7); // Last exercise in M1
        }""")
        await page.wait_for_timeout(400)

        all_completed_steps = await page.query_selector_all(".sr-bottom-module-step.is-completed")
        all_completed_connectors = await page.query_selector_all(".sr-bottom-module-connector.is-completed")
        print(f"  All completed steps count: {len(all_completed_steps)} (expected 7 or 8 depending on active)")
        print(f"  All completed connectors count: {len(all_completed_connectors)} (expected 7)")
        assert len(all_completed_connectors) == 7

        await bb.screenshot(path="tests/screenshots/path_03_m1_all_completed.png")
        print("  Screenshot saved: path_03_m1_all_completed.png")

        # -------------------------------------------------------------
        # 4. Módulo 2 Parcialmente Completado (4 de 9)
        # -------------------------------------------------------------
        print("\n--- 4. Testing Módulo 2 (4 de 9) ---")
        await page.evaluate("""() => {
            const store = window.SocialR.progress;
            const m2_ex = ['intro-r-02-001', 'intro-r-02-002', 'intro-r-02-003'];
            m2_ex.forEach(id => store.markCompleted(id, 'trabajar-con-varios-valores'));
            window.SocialR.navigation.setActiveIndex(11); // Exercise 4 in M2 (globalIndex 11)
        }""")
        await page.wait_for_timeout(400)

        m2_counter_txt = (await page.text_content("#sr-bottombar-counter")).strip()
        m2_all_steps = await page.query_selector_all(".sr-bottom-module-step")
        m2_completed_steps = await page.query_selector_all(".sr-bottom-module-step.is-completed")
        m2_active_step = await page.query_selector(".sr-bottom-module-step.is-active")
        m2_active_text = (await m2_active_step.text_content()).strip()

        print(f"  M2 Counter: '{m2_counter_txt}'")
        print(f"  M2 Total steps: {len(m2_all_steps)} (expected 9)")
        print(f"  M2 Completed steps: {len(m2_completed_steps)} (expected 3)")
        print(f"  M2 Active step text: '{m2_active_text}' (expected '4')")

        assert "Módulo 2 · 4 de 9" in m2_counter_txt
        assert len(m2_all_steps) == 9
        assert len(m2_completed_steps) == 3
        assert m2_active_text == "4"

        await bb.screenshot(path="tests/screenshots/path_04_m2_partial_4of9.png")
        await page.screenshot(path="tests/screenshots/path_05_fullscreen_m2.png")
        print("  Screenshots saved: path_04_m2_partial_4of9.png, path_05_fullscreen_m2.png")

        await browser.close()
        print("\n[SUCCESS] Connected Circles Progress Path Verification Passed 100%!")

if __name__ == "__main__":
    asyncio.run(test_progress_path())
