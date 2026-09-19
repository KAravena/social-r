#!/usr/bin/env python3
"""Strict validation and measurement of the visible .sr-bottom-module-track component."""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def validate():
    print(f"Connecting to {BASE_URL} for strict visual & geometric validation ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for width, height in [(1920, 1080), (1366, 768)]:
            print(f"\n=======================================================")
            print(f"  TESTING VIEWPORT: {width} x {height}")
            print(f"=======================================================")
            page = await browser.new_page(viewport={"width": width, "height": height})

            # Hard load with qa-clean
            await page.goto(f"{BASE_URL}?qa-clean=1", wait_until="networkidle")
            await page.wait_for_timeout(2000)

            # -------------------------------------------------------------
            # Requirement 2 & 17: Count total and visible tracks
            # -------------------------------------------------------------
            track_counts = await page.evaluate("""() => {
                const tracks = Array.from(document.querySelectorAll('.sr-bottom-module-track'));
                const visible = tracks.filter(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
                });
                return {
                    total: tracks.length,
                    visible: visible.length
                };
            }""")
            print(f"Total .sr-bottom-module-track in DOM: {track_counts['total']}")
            print(f"Visible .sr-bottom-module-track in DOM: {track_counts['visible']}")
            assert track_counts["visible"] == 1, f"Expected exactly 1 visible track, got {track_counts['visible']}"

            # -------------------------------------------------------------
            # Requirement 4, 5, 6, 25: Computed CSS of visible track
            # -------------------------------------------------------------
            track_styles = await page.evaluate("""() => {
                const track = document.querySelector('.sr-bottom-module-track');
                const bb = document.querySelector('.sr-bottombar');
                const tStyle = window.getComputedStyle(track);
                const bStyle = window.getComputedStyle(bb);
                const tRect = track.getBoundingClientRect();
                const bRect = bb.getBoundingClientRect();
                return {
                    display: tStyle.display,
                    flexDirection: tStyle.flexDirection,
                    flexWrap: tStyle.flexWrap,
                    width: tStyle.width,
                    gridColumn: tStyle.gridColumn,
                    position: tStyle.position,
                    trackRect: { x: tRect.x, y: tRect.y, width: tRect.width, height: tRect.height },
                    bottombarRect: { x: bRect.x, y: bRect.y, width: bRect.width, height: bRect.height }
                };
            }""")
            print(f"\nVisible Track Computed Styles:")
            print(f"  display:        {track_styles['display']}")
            print(f"  flexDirection:  {track_styles['flexDirection']}")
            print(f"  flexWrap:       {track_styles['flexWrap']}")
            print(f"  gridColumn:     {track_styles['gridColumn']}")
            print(f"  position:       {track_styles['position']}")
            print(f"  track width:    {track_styles['trackRect']['width']}px (BottomBar width: {track_styles['bottombarRect']['width']}px)")

            assert track_styles["display"] == "flex", f"Track display must be 'flex', got {track_styles['display']}"
            assert track_styles["flexDirection"] == "row", f"Track flex-direction must be 'row', got {track_styles['flexDirection']}"
            assert track_styles["flexWrap"] == "nowrap", f"Track flex-wrap must be 'nowrap', got {track_styles['flexWrap']}"
            assert track_styles["trackRect"]["width"] >= 0.75 * track_styles["bottombarRect"]["width"], f"Track width must be >= 75% of bottombar"

            # -------------------------------------------------------------
            # Requirement 7, 16, 21: Coordinates of steps in Module 1
            # -------------------------------------------------------------
            steps_m1 = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-step")
            print(f"\nModule 1 step nodes count: {len(steps_m1)}")
            assert len(steps_m1) == 8, f"Expected 8 nodes for Module 1, got {len(steps_m1)}"

            boxes_m1 = [await s.bounding_box() for s in steps_m1]
            y_m1 = [b["y"] for b in boxes_m1]
            x_m1 = [b["x"] for b in boxes_m1]

            print(f"  First 3 nodes: x=[{x_m1[0]:.1f}, {x_m1[1]:.1f}, {x_m1[2]:.1f}], y=[{y_m1[0]:.1f}, {y_m1[1]:.1f}, {y_m1[2]:.1f}]")
            print(f"  Last 3 nodes:  x=[{x_m1[5]:.1f}, {x_m1[6]:.1f}, {x_m1[7]:.1f}], y=[{y_m1[5]:.1f}, {y_m1[6]:.1f}, {y_m1[7]:.1f}]")

            max_y_diff_m1 = max(y_m1) - min(y_m1)
            span_x_m1 = x_m1[-1] - x_m1[0]
            print(f"  Max Y difference: {max_y_diff_m1:.2f}px")
            print(f"  Horizontal span:  {span_x_m1:.2f}px (vs track width: {track_styles['trackRect']['width']}px)")

            assert max_y_diff_m1 < 4.0, f"Nodes are NOT horizontal! Max Y diff = {max_y_diff_m1}px"
            assert span_x_m1 > 0.65 * track_styles["trackRect"]["width"], "Nodes are clustered instead of spanning across the track"
            for i in range(len(x_m1) - 1):
                assert x_m1[i+1] > x_m1[i], f"Step {i+1} is not to the right of step {i}"

            # -------------------------------------------------------------
            # Requirement 8 & 9: Cropped BottomBar screenshot & full screenshot
            # -------------------------------------------------------------
            bb_element = await page.query_selector(".sr-bottombar")
            await bb_element.screenshot(path=f"tests/screenshots/cropped_bottombar_m1_{width}x{height}.png")
            await page.screenshot(path=f"tests/screenshots/fullscreen_m1_{width}x{height}.png")
            print(f"  Screenshots saved: cropped_bottombar_m1_{width}x{height}.png, fullscreen_m1_{width}x{height}.png")

            # -------------------------------------------------------------
            # Switch to Module 2 (9 exercises)
            # -------------------------------------------------------------
            print("\n--- Navigating to Module 2 ---")
            pills = await page.query_selector_all(".sr-mini-pill")
            await pills[1].click()
            await page.wait_for_timeout(500)

            steps_m2 = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-step")
            print(f"Module 2 step nodes count: {len(steps_m2)}")
            assert len(steps_m2) == 9, f"Expected 9 nodes for Module 2, got {len(steps_m2)}"

            boxes_m2 = [await s.bounding_box() for s in steps_m2]
            y_m2 = [b["y"] for b in boxes_m2]
            x_m2 = [b["x"] for b in boxes_m2]

            print(f"  First 3 nodes: x=[{x_m2[0]:.1f}, {x_m2[1]:.1f}, {x_m2[2]:.1f}], y=[{y_m2[0]:.1f}, {y_m2[1]:.1f}, {y_m2[2]:.1f}]")
            print(f"  Last 3 nodes:  x=[{x_m2[6]:.1f}, {x_m2[7]:.1f}, {x_m2[8]:.1f}], y=[{y_m2[6]:.1f}, {y_m2[7]:.1f}, {y_m2[8]:.1f}]")

            max_y_diff_m2 = max(y_m2) - min(y_m2)
            span_x_m2 = x_m2[-1] - x_m2[0]
            print(f"  M2 Max Y difference: {max_y_diff_m2:.2f}px")
            print(f"  M2 Horizontal span:  {span_x_m2:.2f}px")

            assert max_y_diff_m2 < 4.0, f"Module 2 nodes are NOT horizontal! Max Y diff = {max_y_diff_m2}px"
            assert span_x_m2 > 0.65 * track_styles["trackRect"]["width"], "Module 2 nodes do not span the track"

            await bb_element.screenshot(path=f"tests/screenshots/cropped_bottombar_m2_{width}x{height}.png")
            await page.screenshot(path=f"tests/screenshots/fullscreen_m2_{width}x{height}.png")
            print(f"  Screenshots saved: cropped_bottombar_m2_{width}x{height}.png, fullscreen_m2_{width}x{height}.png")

            # -------------------------------------------------------------
            # Switch to Module 3 (8 exercises)
            # -------------------------------------------------------------
            print("\n--- Navigating to Module 3 ---")
            fresh_pills = await page.query_selector_all(".sr-mini-pill")
            await fresh_pills[2].click()
            await page.wait_for_timeout(500)

            steps_m3 = await page.query_selector_all(".sr-bottom-module-track .sr-bottom-module-step")
            print(f"Module 3 step nodes count: {len(steps_m3)}")
            assert len(steps_m3) == 8, f"Expected 8 nodes for Module 3, got {len(steps_m3)}"

            await bb_element.screenshot(path=f"tests/screenshots/cropped_bottombar_m3_{width}x{height}.png")
            await page.screenshot(path=f"tests/screenshots/fullscreen_m3_{width}x{height}.png")

            await page.close()

        await browser.close()
        print("\n=======================================================")
        print("  ALL STRICT VISUAL & GEOMETRIC VALIDATIONS PASSED 100%!")
        print("=======================================================")

if __name__ == "__main__":
    asyncio.run(validate())
