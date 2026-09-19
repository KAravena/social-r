#!/usr/bin/env python3
"""Comprehensive Dynamic UI & Visual Verification for Social R:
1. Course Outline Drawer
2. Module Completed Celebration Modal & Icons
3. No literal 'svg' in DOM
4. Scoped SVG sizing (no oversized checks)
5. BottomBar across Module 1, 2, 3
6. Navigation transitions without reload
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def run_comprehensive_tests():
    print(f"Starting Comprehensive Dynamic UI Verification on {BASE_URL} ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        console_errors = []
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        await page.goto(f"{BASE_URL}?qa-clean=1", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # -------------------------------------------------------------
        # TEST 1: No literal 'svg' text in document body
        # -------------------------------------------------------------
        print("\n--- TEST 1: Assert No Literal 'svg' Text in Document ---")
        svg_matches = await page.evaluate("""() => {
            const matches = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let n;
            while (n = walker.nextNode()) {
                const txt = n.textContent.trim();
                // Check if any standalone text says 'svg' or '<svg'
                if (txt === 'svg' || txt.toLowerCase() === 'svg' || txt.startsWith('<svg')) {
                    matches.push({
                        text: txt,
                        parent: n.parentElement ? `${n.parentElement.tagName}.${n.parentElement.className}` : 'root'
                    });
                }
            }
            return matches;
        }""")
        print(f"  Matches for literal 'svg' text: {svg_matches}")
        assert len(svg_matches) == 0, f"Found literal 'svg' text in DOM: {svg_matches}"

        # -------------------------------------------------------------
        # TEST 2: Course Outline Drawer Visual & Layout
        # -------------------------------------------------------------
        print("\n--- TEST 2: Course Outline Drawer Layout & Styling ---")
        await page.click("#sr-outline-trigger")
        await page.wait_for_timeout(500)

        drawer = await page.query_selector(".sr-drawer")
        drawer_box = await drawer.bounding_box()
        print(f"  Drawer Bounding Box: {drawer_box}")
        assert 340 <= drawer_box["width"] <= 450, f"Drawer width should be ~380px, got {drawer_box['width']}"
        assert drawer_box["x"] >= 0, "Drawer must be visible on screen when opened"

        headers = await page.query_selector_all(".sr-drawer-module-header")
        items = await page.query_selector_all(".sr-drawer-item")
        print(f"  Drawer Module Headers: {len(headers)}, Exercise Items: {len(items)}")
        assert len(headers) == 3, f"Expected 3 module headers, got {len(headers)}"
        assert len(items) == 25, f"Expected 25 exercise items, got {len(items)}"

        await page.screenshot(path="tests/screenshots/audit_A_course_outline_open.png")
        print("  [Screenshot A saved: Course Outline]")

        await page.click("#sr-drawer-close")
        await page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # TEST 3: BottomBar in Module 1, Module 2, Module 3
        # -------------------------------------------------------------
        print("\n--- TEST 3: BottomBar Single-Row & Circular Stepper Across Modules ---")
        # 3.1 Module 1 (8 exercises)
        bb = await page.query_selector(".sr-bottombar")
        bb_box = await bb.bounding_box()
        m1_steps = await page.query_selector_all(".sr-bottom-module-step")
        m1_counter = (await page.text_content("#sr-bottombar-counter")).strip()
        print(f"  M1: Height={bb_box['height']}px, Counter='{m1_counter}', Steps={len(m1_steps)}")
        assert 40.0 <= bb_box["height"] <= 48.0
        assert "Módulo 1" in m1_counter and "1 de 8" in m1_counter
        assert len(m1_steps) == 8
        await bb.screenshot(path="tests/screenshots/audit_B_bottombar_m1.png")
        print("  [Screenshot B saved: BottomBar M1]")

        # 3.2 Navigate to Module 2 Exercise 1 (globalIndex 8)
        print("\n  [Navigating to Module 2]")
        await page.evaluate("window.SocialR.navigation.setActiveIndex(8)")
        await page.wait_for_timeout(400)
        m2_steps = await page.query_selector_all(".sr-bottom-module-step")
        m2_counter = (await page.text_content("#sr-bottombar-counter")).strip()
        print(f"  M2: Counter='{m2_counter}', Steps={len(m2_steps)}")
        assert "Módulo 2" in m2_counter and "1 de 9" in m2_counter
        assert len(m2_steps) == 9
        await bb.screenshot(path="tests/screenshots/audit_C_bottombar_m2.png")
        print("  [Screenshot C saved: BottomBar M2]")

        # 3.3 Navigate to Module 3 Exercise 1 (globalIndex 17)
        print("\n  [Navigating to Module 3]")
        await page.evaluate("window.SocialR.navigation.setActiveIndex(17)")
        await page.wait_for_timeout(400)
        m3_steps = await page.query_selector_all(".sr-bottom-module-step")
        m3_counter = (await page.text_content("#sr-bottombar-counter")).strip()
        print(f"  M3: Counter='{m3_counter}', Steps={len(m3_steps)}")
        assert "Módulo 3" in m3_counter and "1 de 8" in m3_counter
        assert len(m3_steps) == 8
        await bb.screenshot(path="tests/screenshots/audit_D_bottombar_m3.png")
        print("  [Screenshot D saved: BottomBar M3]")

        # -------------------------------------------------------------
        # TEST 4: Module Completed Celebration Modal
        # -------------------------------------------------------------
        print("\n--- TEST 4: Module Completed Modal & Scoped SVG Check ---")
        # Go back to Module 1 Exercise 8 (last in M1)
        await page.evaluate("window.SocialR.navigation.setActiveIndex(7)")
        await page.wait_for_timeout(300)

        # Trigger showCelebration for Module 1
        await page.evaluate("window.SocialR.navigation.showCelebration('primeros-pasos')")
        await page.wait_for_timeout(500)

        cel_card = await page.query_selector(".sr-celebration-card")
        cel_box = await cel_card.bounding_box()
        print(f"  Celebration Card Bounding Box: {cel_box}")
        assert 450 <= cel_box["width"] <= 600, f"Celebration card width should be 500-600px, got {cel_box['width']}"

        # Check celebration icon bounds
        icon_box = await page.query_selector(".sr-celebration-icon-box")
        svg_check = await page.query_selector(".sr-celebration-check")
        icon_box_rect = await icon_box.bounding_box()
        svg_rect = await svg_check.bounding_box()

        print(f"  Icon Container Box: {icon_box_rect}")
        print(f"  SVG Check Dimensions: {svg_rect}")

        assert icon_box_rect["width"] <= 64 and icon_box_rect["height"] <= 64, f"Icon container too large: {icon_box_rect}"
        assert svg_rect["width"] <= 36 and svg_rect["height"] <= 36, f"SVG check is giant! Got: {svg_rect}"

        # Verify Outcomes list
        outcomes = await page.query_selector_all(".sr-outcome-item")
        print(f"  Outcomes count: {len(outcomes)}")
        assert len(outcomes) >= 4, f"Expected at least 4 learning outcomes, got {len(outcomes)}"

        # Verify CTA button
        cta_btn = await page.query_selector("#sr-cel-continue-btn")
        cta_text = (await cta_btn.text_content()).strip()
        print(f"  CTA Button Text: '{cta_text}'")
        assert "Módulo 2" in cta_text

        await page.screenshot(path="tests/screenshots/audit_E_celebration_modal.png")
        print("  [Screenshot E saved: Celebration Modal]")

        # Click CTA to start Module 2
        print("\n  [Clicking 'Comenzar Módulo 2' inside Modal]")
        await cta_btn.click()
        await page.wait_for_timeout(500)

        # Verify active exercise is now Module 2 Exercise 1 (globalIndex 8)
        new_counter = (await page.text_content("#sr-topbar-counter")).strip()
        new_bottom = (await page.text_content("#sr-bottombar-counter")).strip()
        print(f"  After Modal CTA: TopBar='{new_counter}', BottomBar='{new_bottom}'")
        assert "1/9" in new_counter
        assert "Módulo 2 · 1 de 9" in new_bottom

        await page.screenshot(path="tests/screenshots/audit_F_module2_after_modal.png")
        print("  [Screenshot F saved: Workspace in Module 2 after modal transition]")

        await browser.close()
        print("\n[SUCCESS] Comprehensive Dynamic UI Verification Passed 100%!")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
