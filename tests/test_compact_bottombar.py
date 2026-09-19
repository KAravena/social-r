#!/usr/bin/env python3
"""Validation script for the newly redesigned single-row compact connected circles BottomBar."""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def test_compact_bottombar():
    print(f"Connecting to {BASE_URL} for compact BottomBar validation ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for width, height in [(1920, 1080), (1366, 768)]:
            print(f"\n=======================================================")
            print(f"  TESTING VIEWPORT: {width} x {height}")
            print(f"=======================================================")
            page = await browser.new_page(viewport={"width": width, "height": height})

            await page.goto(f"{BASE_URL}?qa-clean=1", wait_until="networkidle")
            await page.wait_for_timeout(2000)

            # ---------------------------------------------------------
            # 1. Height & Layout Check
            # ---------------------------------------------------------
            bb = await page.query_selector(".sr-bottombar")
            bb_box = await bb.bounding_box()
            print(f"  BottomBar Bounding Box: {bb_box}")
            assert 38.0 <= bb_box["height"] <= 48.0, f"BottomBar height must be 40px-48px compact, got {bb_box['height']}px"

            # ---------------------------------------------------------
            # 2. Left Side Check (No M1/M2/M3 pills, only compact text)
            # ---------------------------------------------------------
            pills = await page.query_selector_all(".sr-bottombar .sr-mini-pill")
            print(f"  Pills in BottomBar: {len(pills)} (must be 0)")
            assert len(pills) == 0, f"M1/M2/M3 pills must be completely eliminated from bottombar, found {len(pills)}"

            counter_el = await page.query_selector("#sr-bottombar-counter")
            counter_txt = (await counter_el.text_content()).strip()
            print(f"  Left Counter Text: '{counter_txt}'")
            assert "Módulo 1" in counter_txt and "1 de 8" in counter_txt

            # ---------------------------------------------------------
            # 3. Center Connected Circles Check
            # ---------------------------------------------------------
            track_el = await page.query_selector(".sr-bottom-module-track")
            track_box = await track_el.bounding_box()
            print(f"  Track Bounding Box: {track_box}")

            steps = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-step")
            connectors = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-connector")
            print(f"  Step circles count for M1: {len(steps)}, Connectors: {len(connectors)}")
            assert len(steps) == 8, f"Expected 8 step circles for Module 1, got {len(steps)}"
            assert len(connectors) == 7, f"Expected 7 connectors for Module 1, got {len(connectors)}"

            # Check circle node dimensions (16px x 16px)
            step_boxes = [await s.bounding_box() for s in steps]
            for i, box in enumerate(step_boxes):
                assert abs(box["width"] - 16.0) <= 4.0 and abs(box["height"] - 16.0) <= 4.0, f"Circle {i} size should be ~16px, got {box['width']}x{box['height']}"

            # Check horizontal alignment
            y_coords = [b["y"] for b in step_boxes]
            x_coords = [b["x"] for b in step_boxes]
            max_y_diff = max(y_coords) - min(y_coords)
            print(f"  Max Y diff between circles: {max_y_diff:.2f}px")
            assert max_y_diff < 2.0, f"Circles must be strictly horizontal! Got max Y diff = {max_y_diff}px"

            for i in range(len(x_coords) - 1):
                assert x_coords[i+1] > x_coords[i], f"Circle {i+1} is not to the right of circle {i}"

            # ---------------------------------------------------------
            # 4. Right Side Check (Discrete course progress)
            # ---------------------------------------------------------
            pct_el = await page.query_selector("#sr-progress-pct")
            pct_txt = (await pct_el.text_content()).strip()
            print(f"  Right Percentage Text: '{pct_txt}'")
            assert "del curso" in pct_txt

            # Take Screenshots
            await bb.screenshot(path=f"tests/screenshots/compact_bottombar_m1_{width}x{height}.png")
            await page.screenshot(path=f"tests/screenshots/compact_fullscreen_m1_{width}x{height}.png")
            print(f"  Screenshots saved for M1 at {width}x{height}")

            # ---------------------------------------------------------
            # 5. Switch to Module 2 (9 exercises)
            # ---------------------------------------------------------
            print("\n  [Switching to Module 2 via navigation]")
            await page.evaluate("window.SocialR.navigation.setActiveIndex(8)")
            await page.wait_for_timeout(500)

            m2_counter_txt = (await counter_el.text_content()).strip()
            m2_steps = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-step")
            print(f"  M2 Counter: '{m2_counter_txt}'")
            print(f"  M2 Steps count: {len(m2_steps)}")
            assert "Módulo 2" in m2_counter_txt and "1 de 9" in m2_counter_txt
            assert len(m2_steps) == 9, f"Expected 9 step circles for Module 2, got {len(m2_steps)}"

            # Mark 3 exercises completed in M2 to verify green circles
            await page.evaluate("""() => {
                const store = window.SocialR.progress;
                store.markCompleted('intro-r-02-001', '02-trabajar-con-varios-valores');
                store.markCompleted('intro-r-02-002', '02-trabajar-con-varios-valores');
                store.markCompleted('intro-r-02-003', '02-trabajar-con-varios-valores');
                window.SocialR.navigation.setActiveIndex(11); // Exercise 4 active
            }""")
            await page.wait_for_timeout(500)

            completed_steps = await page.query_selector_all(".sr-bottom-module-step.is-completed")
            active_step = await page.query_selector(".sr-bottom-module-step.is-active")
            print(f"  Completed circles: {len(completed_steps)}, Active step found: {active_step is not None}")
            assert len(completed_steps) == 3, f"Expected 3 completed green circles, got {len(completed_steps)}"

            await bb.screenshot(path=f"tests/screenshots/compact_bottombar_m2_progress_{width}x{height}.png")
            await page.screenshot(path=f"tests/screenshots/compact_fullscreen_m2_{width}x{height}.png")
            print(f"  Screenshots saved for M2 with progress at {width}x{height}")

            await page.close()

        await browser.close()
        print("\n[SUCCESS] Compact BottomBar Verification Passed 100%!")

if __name__ == "__main__":
    asyncio.run(test_compact_bottombar())
