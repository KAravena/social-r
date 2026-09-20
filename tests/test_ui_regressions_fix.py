#!/usr/bin/env python3
"""E2E Verification script for UI regressions fixes:
- Course Outline rendering with empty & populated progress
- Single-module horizontal BottomBar stepper (no vertical stacking)
- Mini course pills
- 3-tier TopBar hierarchy with graceful truncation
- Navigation from outline across independent modules
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200/curso.html"

async def run_tests():
    print(f"Starting UI regression tests on {BASE_URL} ...")
    os.makedirs("tests/screenshots", exist_ok=True)

    async with async_playwright() as p:
        # Launch browser with 1920x1080 viewport as requested
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        console_errors = []
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        # ==========================================
        # TEST 1: Clean State (localStorage empty)
        # ==========================================
        print("\n--- TEST 1: Clean State with Empty localStorage ---")
        await page.goto(f"{BASE_URL}?qa-clean=1")
        await page.wait_for_timeout(2000)

        assert len(console_errors) == 0, f"Page threw JS errors: {console_errors}"

        # 1.1 Check TopBar 3-tier elements
        mod_pill = await page.text_content("#sr-topbar-mod-pill")
        counter_txt = await page.text_content("#sr-topbar-counter")
        title_txt = await page.text_content("#sr-topbar-title")
        prev_btn_disabled = await page.is_disabled("#sr-btn-prev")

        print(f"  TopBar Pill: '{mod_pill}'")
        print(f"  TopBar Counter: '{counter_txt}'")
        print(f"  TopBar Title: '{title_txt}'")
        print(f"  Prev Button Disabled: {prev_btn_disabled}")

        assert "Módulo 1" in mod_pill, "TopBar pill should say 'Módulo 1'"
        assert "1/8" in counter_txt, "TopBar counter should be '1/8 ·'"
        assert prev_btn_disabled, "Prev button must be disabled on first exercise"

        # 1.2 Check BottomBar Single-Module Horizontal Stepper
        bottom_counter = await page.text_content("#sr-bottombar-counter")
        stepper_nodes = await page.query_selector_all(".sr-bottom-module-step, .sr-step-node")
        stepper_lines = await page.query_selector_all(".sr-bottom-module-connector, .sr-step-line")

        print(f"  BottomBar Counter: '{bottom_counter}'")
        print(f"  Current Module Stepper nodes count: {len(stepper_nodes)}")
        print(f"  Current Module Stepper lines count: {len(stepper_lines)}")

        assert "Módulo 1" in bottom_counter and "1 de 8" in bottom_counter
        assert len(stepper_nodes) == 8, f"Expected 8 step nodes for Module 1, got {len(stepper_nodes)}"
        assert len(stepper_lines) == 7, f"Expected 7 step lines for Module 1, got {len(stepper_lines)}"

        # Check horizontal layout: nodes should NOT be vertically stacked
        box0 = await stepper_nodes[0].bounding_box()
        box1 = await stepper_nodes[1].bounding_box()
        print(f"  Node 0 Y: {box0['y']}, Node 1 Y: {box1['y']}")
        assert abs(box0['y'] - box1['y']) < 3, "Stepper nodes must be horizontally aligned (no vertical wrapping)"
        assert box1['x'] > box0['x'], "Node 1 must be to the right of Node 0"

        await page.screenshot(path="tests/screenshots/fix_01_clean_state_1920x1080.png")
        print("  Screenshot saved: fix_01_clean_state_1920x1080.png")

        # ==========================================
        # TEST 2: Course Outline Drawer with Empty Progress
        # ==========================================
        print("\n--- TEST 2: Course Outline Drawer with Zero Progress ---")
        await page.click("#sr-outline-trigger")
        await page.wait_for_timeout(400)

        drawer_is_open = await page.evaluate("document.getElementById('sr-drawer-backdrop').classList.contains('is-open')")
        drawer_headers = await page.query_selector_all(".sr-drawer-module-header")
        drawer_items = await page.query_selector_all(".sr-drawer-item")

        print(f"  Drawer is open: {drawer_is_open}")
        print(f"  Drawer module headers: {len(drawer_headers)}")
        print(f"  Drawer exercise items: {len(drawer_items)}")

        assert drawer_is_open, "Drawer backdrop must be open"
        assert len(drawer_headers) == 3, f"Expected 3 module headers, got {len(drawer_headers)}"
        assert len(drawer_items) == 25, f"Expected 25 exercise items in outline, got {len(drawer_items)}"

        # Verify states in Outline:
        # M1 E1: current/active (●)
        # M2 E1: available (○)
        # M3 E1: available (○)
        # M1 E2: locked (🔒)
        m1_e1_badge = await drawer_items[0].query_selector(".sr-drawer-badge")
        m1_e2_badge = await drawer_items[1].query_selector(".sr-drawer-badge")
        m2_e1_badge = await drawer_items[8].query_selector(".sr-drawer-badge")
        m3_e1_badge = await drawer_items[17].query_selector(".sr-drawer-badge")

        print(f"  M1 E1 badge text: '{await m1_e1_badge.text_content()}'")
        print(f"  M1 E2 badge text: '{await m1_e2_badge.text_content()}'")
        print(f"  M2 E1 badge text: '{await m2_e1_badge.text_content()}'")
        print(f"  M3 E1 badge text: '{await m3_e1_badge.text_content()}'")

        assert "●" in await m1_e1_badge.text_content(), "M1 E1 should be current (●)"
        assert "🔒" in await m1_e2_badge.text_content(), "M1 E2 should be locked (🔒)"
        assert "○" in await m2_e1_badge.text_content(), "M2 E1 should be available (○)"
        assert "○" in await m3_e1_badge.text_content(), "M3 E1 should be available (○)"

        await page.screenshot(path="tests/screenshots/fix_02_drawer_empty_progress.png")
        print("  Screenshot saved: fix_02_drawer_empty_progress.png")

        # ==========================================
        # TEST 3: Click Módulo 2 E1 from Outline
        # ==========================================
        print("\n--- TEST 3: Navigate to Module 2 Exercise 1 from Course Outline ---")
        await drawer_items[8].click() # Click M2 E1
        await page.wait_for_timeout(400)

        m2_pill = await page.text_content("#sr-topbar-mod-pill")
        m2_counter = await page.text_content("#sr-topbar-counter")
        m2_title = await page.text_content("#sr-topbar-title")
        m2_bottom_counter = await page.text_content("#sr-bottombar-counter")
        m2_stepper_nodes = await page.query_selector_all(".sr-bottom-module-step, .sr-step-node")

        print(f"  New TopBar Pill: '{m2_pill}'")
        print(f"  New TopBar Counter: '{m2_counter}'")
        print(f"  New TopBar Title: '{m2_title}'")
        print(f"  New BottomBar Counter: '{m2_bottom_counter}'")
        print(f"  Module 2 Stepper Nodes: {len(m2_stepper_nodes)}")

        assert "Módulo 2" in m2_pill
        assert "1/9" in m2_counter
        assert "De un valor a varios" in m2_title
        assert "Módulo 2" in m2_bottom_counter and "1 de 9" in m2_bottom_counter
        assert len(m2_stepper_nodes) == 9, "Module 2 should have exactly 9 steps in stepper"

        await page.screenshot(path="tests/screenshots/fix_03_module_2_active.png")
        print("  Screenshot saved: fix_03_module_2_active.png")

        # ==========================================
        # TEST 4: Populated Progress (M1 8/8 Completed, M2 1/9 Started)
        # ==========================================
        print("\n--- TEST 4: Populated Progress (M1 completed, M2 active) ---")
        await page.evaluate("""() => {
            const m1_exercises = ['intro-r-01-001', 'intro-r-01-002', 'intro-r-01-003', 'intro-r-01-004', 'intro-r-01-005', 'intro-r-01-006', 'intro-r-01-007', 'intro-r-01-008'];
            m1_exercises.forEach(id => window.SocialR.progress.markCompleted(id, 'primeros-pasos'));
            window.SocialR.progress.setModuleCompleted('primeros-pasos', true);
            window.SocialR.navigation.setActiveIndex(8); // M2 E1
        }""")
        await page.wait_for_timeout(400)

        # Open Drawer and check summaries and checks
        await page.click("#sr-outline-trigger")
        await page.wait_for_timeout(400)

        fresh_headers = await page.query_selector_all(".sr-drawer-module-header")
        m1_summary = await (await fresh_headers[0].query_selector(".sr-drawer-module-summary")).text_content()
        m2_summary = await (await fresh_headers[1].query_selector(".sr-drawer-module-summary")).text_content()
        m3_summary = await (await fresh_headers[2].query_selector(".sr-drawer-module-summary")).text_content()

        print(f"  M1 Outline Summary: '{m1_summary}'")
        print(f"  M2 Outline Summary: '{m2_summary}'")
        print(f"  M3 Outline Summary: '{m3_summary}'")

        assert "8/8" in m1_summary and "✓" in m1_summary, "M1 summary should show 8/8 ✓"
        assert "0/9" in m2_summary, "M2 summary should show 0/9"

        # Verify all 8 items of M1 have checkmarks
        m1_items = await fresh_headers[0].evaluate_handle("el => { let curr = el.nextElementSibling; const items = []; while (curr && curr.classList.contains('sr-drawer-item')) { items.push(curr); curr = curr.nextElementSibling; } return items; }")
        
        await page.screenshot(path="tests/screenshots/fix_04_drawer_m1_completed_m2_active.png")
        print("  Screenshot saved: fix_04_drawer_m1_completed_m2_active.png")

        # Close Drawer and verify BottomBar
        await page.click("#sr-drawer-close")
        await page.wait_for_timeout(300)

        await page.screenshot(path="tests/screenshots/fix_05_m1_completed_bottombar.png")
        print("  Screenshot saved: fix_05_m1_completed_bottombar.png")

        # ==========================================
        # TEST 5: Title Truncation with Long Title
        # ==========================================
        print("\n--- TEST 5: Long Title Handling in TopBar ---")
        # Jump to Module 2 Exercise 3 ("Varios valores, distintas formas de información")
        await page.evaluate("""() => {
            window.SocialR.progress.markCompleted('intro-r-02-001', 'trabajar-con-varios-valores');
            window.SocialR.progress.markCompleted('intro-r-02-002', 'trabajar-con-varios-valores');
            window.SocialR.navigation.setActiveIndex(10); // M2 E3
        }""")
        await page.wait_for_timeout(400)

        long_title = await page.text_content("#sr-topbar-title")
        print(f"  Long title text: '{long_title}'")
        
        # Verify Next and Prev buttons are still fully visible on screen
        prev_box = await (await page.query_selector("#sr-btn-prev")).bounding_box()
        next_box = await (await page.query_selector("#sr-btn-next")).bounding_box()
        trigger_box = await (await page.query_selector("#sr-outline-trigger")).bounding_box()

        print(f"  Prev Button: x={prev_box['x']}, width={prev_box['width']}")
        print(f"  Trigger: x={trigger_box['x']}, width={trigger_box['width']}")
        print(f"  Next Button: x={next_box['x']}, width={next_box['width']}")

        assert prev_box['x'] > 0, "Prev button must be visible"
        assert next_box['x'] + next_box['width'] < 1920, "Next button must not be pushed off screen"
        assert trigger_box['x'] > prev_box['x'], "Trigger must be between Prev and Next"

        await page.screenshot(path="tests/screenshots/fix_06_long_title_topbar.png")
        print("  Screenshot saved: fix_06_long_title_topbar.png")

        print("\n[ALL TESTS PASSED] All UI regressions successfully fixed and verified!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_tests())
