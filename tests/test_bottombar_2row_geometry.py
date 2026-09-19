#!/usr/bin/env python3
"""E2E Test to strictly verify the 2-row BottomBar geometry, horizontal alignment, and no-wrap behavior."""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def test_geometry():
    print(f"Connecting to {BASE_URL} for BottomBar 2-Row Geometry Verification ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for width, height in [(1920, 1080), (1366, 768)]:
            print(f"\n================ Testing at {width}x{height} ================")
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()

            await page.goto(f"{BASE_URL}?qa-clean=1")
            await page.wait_for_timeout(2000)

            # ---------------------------------------------
            # 1. Check BottomBar element dimensions
            # ---------------------------------------------
            bb = await page.query_selector(".sr-bottombar")
            bb_box = await bb.bounding_box()
            print(f"  BottomBar box: {bb_box}")
            assert bb_box["height"] >= 50 and bb_box["height"] <= 70, f"BottomBar height should be compact (50-70px), got {bb_box['height']}px"

            # ---------------------------------------------
            # 2. Check Row 1 (Meta Header)
            # ---------------------------------------------
            meta_el = await page.query_selector(".sr-bottombar-meta")
            counter_el = await page.query_selector("#sr-bottombar-counter")
            pills = await page.query_selector_all(".sr-mini-pill")
            pct_el = await page.query_selector("#sr-progress-pct")

            counter_txt = await counter_el.text_content()
            pct_txt = await pct_el.text_content()

            print(f"  Counter text: '{counter_txt}'")
            print(f"  Mini pills count: {len(pills)}")
            print(f"  Percentage text: '{pct_txt}'")

            assert "Módulo 1" in counter_txt and "1 de 8" in counter_txt
            assert len(pills) == 3, f"Expected 3 mini pills (M1, M2, M3), got {len(pills)}"
            assert "curso" in pct_txt

            # ---------------------------------------------
            # 3. Check Row 2 (Stepper full width and horizontal alignment)
            # ---------------------------------------------
            stepper = await page.query_selector(".sr-module-stepper")
            stepper_box = await stepper.bounding_box()
            print(f"  Stepper box: {stepper_box}")

            # Stepper should occupy virtually the full width of the container
            assert stepper_box["width"] >= bb_box["width"] * 0.85, f"Stepper width ({stepper_box['width']}) should occupy full width (>= 85% of {bb_box['width']})"

            nodes = await page.query_selector_all(".sr-step-node")
            print(f"  Step nodes count for Module 1: {len(nodes)}")
            assert len(nodes) == 8, f"Expected 8 nodes for Module 1, got {len(nodes)}"

            node_boxes = [await n.bounding_box() for n in nodes]
            y_coords = [b["y"] for b in node_boxes]
            x_coords = [b["x"] for b in node_boxes]

            y_diff = max(y_coords) - min(y_coords)
            print(f"  Max Y diff between nodes: {y_diff:.2f}px")
            assert y_diff < 2.0, f"All nodes must be strictly on the same horizontal line! (Max Y diff: {y_diff}px)"

            for i in range(len(x_coords) - 1):
                assert x_coords[i+1] > x_coords[i], f"Node {i+1} (x={x_coords[i+1]}) must be to the right of Node {i} (x={x_coords[i]})"

            await page.screenshot(path=f"tests/screenshots/bottombar_m1_{width}x{height}.png")
            print(f"  Screenshot saved: bottombar_m1_{width}x{height}.png")

            # ---------------------------------------------
            # 4. Switch to Module 2 (9 exercises) and verify
            # ---------------------------------------------
            print("\n  [Switching to Module 2]")
            await pills[1].click() # Click M2 mini pill
            await page.wait_for_timeout(500)

            m2_counter_txt = await counter_el.text_content()
            m2_nodes = await page.query_selector_all(".sr-step-node")
            print(f"  M2 Counter text: '{m2_counter_txt}'")
            print(f"  M2 Step nodes count: {len(m2_nodes)}")

            assert "Módulo 2" in m2_counter_txt and "1 de 9" in m2_counter_txt
            assert len(m2_nodes) == 9, f"Expected 9 nodes for Module 2, got {len(m2_nodes)}"

            m2_node_boxes = [await n.bounding_box() for n in m2_nodes]
            m2_y_coords = [b["y"] for b in m2_node_boxes]
            m2_x_coords = [b["x"] for b in m2_node_boxes]

            m2_y_diff = max(m2_y_coords) - min(m2_y_coords)
            print(f"  M2 Max Y diff: {m2_y_diff:.2f}px")
            assert m2_y_diff < 2.0, f"Module 2 nodes must be on the same horizontal line! (Max Y diff: {m2_y_diff}px)"

            for i in range(len(m2_x_coords) - 1):
                assert m2_x_coords[i+1] > m2_x_coords[i], f"M2 Node {i+1} must be to the right of Node {i}"

            await page.screenshot(path=f"tests/screenshots/bottombar_m2_{width}x{height}.png")
            print(f"  Screenshot saved: bottombar_m2_{width}x{height}.png")

            # ---------------------------------------------
            # 5. Switch to Module 3 (8 exercises) and verify
            # ---------------------------------------------
            print("\n  [Switching to Module 3]")
            fresh_pills = await page.query_selector_all(".sr-mini-pill")
            await fresh_pills[2].click() # Click M3 mini pill
            await page.wait_for_timeout(500)

            m3_counter_txt = await counter_el.text_content()
            m3_nodes = await page.query_selector_all(".sr-step-node")
            print(f"  M3 Counter text: '{m3_counter_txt}'")
            print(f"  M3 Step nodes count: {len(m3_nodes)}")

            assert "Módulo 3" in m3_counter_txt and "1 de 8" in m3_counter_txt
            assert len(m3_nodes) == 8, f"Expected 8 nodes for Module 3, got {len(m3_nodes)}"

            m3_node_boxes = [await n.bounding_box() for n in m3_nodes]
            m3_y_coords = [b["y"] for b in m3_node_boxes]
            m3_y_diff = max(m3_y_coords) - min(m3_y_coords)
            print(f"  M3 Max Y diff: {m3_y_diff:.2f}px")
            assert m3_y_diff < 2.0, f"Module 3 nodes must be on the same horizontal line! (Max Y diff: {m3_y_diff}px)"

            await page.screenshot(path=f"tests/screenshots/bottombar_m3_{width}x{height}.png")
            print(f"  Screenshot saved: bottombar_m3_{width}x{height}.png")

            await context.close()

        await browser.close()
        print("\n[SUCCESS] All BottomBar 2-Row Geometry and Alignment Tests Passed 100%!")

if __name__ == "__main__":
    asyncio.run(test_geometry())
