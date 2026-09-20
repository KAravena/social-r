#!/usr/bin/env python3
"""E2E Test for Modular Progression, Independent Unlocking, and Celebration Modal in Social R."""

import asyncio
import json
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:4200"

async def run_tests():
    print(f"Connecting to {BASE_URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        # 1. Clean load with qa-clean
        await page.goto(f"{BASE_URL}?qa-clean=1")
        await page.wait_for_timeout(2000)

        print("[Test 1] Verify initial state: M1, M2, M3 first exercises unlocked")
        # Check that E1 of M1, E1 of M2, E1 of M3 are unlocked
        m1_e1_unlocked = await page.evaluate("window.SocialR.navigation.isUnlocked(0)") # intro-r-01-001
        m2_e1_unlocked = await page.evaluate("window.SocialR.navigation.isUnlocked(8)") # intro-r-02-001
        m3_e1_unlocked = await page.evaluate("window.SocialR.navigation.isUnlocked(17)") # intro-r-03-001

        print(f"  M1 E1 (idx 0) unlocked: {m1_e1_unlocked}")
        print(f"  M2 E1 (idx 8) unlocked: {m2_e1_unlocked}")
        print(f"  M3 E1 (idx 17) unlocked: {m3_e1_unlocked}")

        assert m1_e1_unlocked, "M1 E1 should be unlocked"
        assert m2_e1_unlocked, "M2 E1 should be unlocked independently"
        assert m3_e1_unlocked, "M3 E1 should be unlocked independently"

        # Check internal locking: M1 E2 and M2 E2 must be locked
        m1_e2_unlocked = await page.evaluate("window.SocialR.navigation.isUnlocked(1)")
        m2_e2_unlocked = await page.evaluate("window.SocialR.navigation.isUnlocked(9)")
        print(f"  M1 E2 (idx 1) unlocked (should be False): {m1_e2_unlocked}")
        print(f"  M2 E2 (idx 9) unlocked (should be False): {m2_e2_unlocked}")
        assert not m1_e2_unlocked, "M1 E2 should be locked initially"
        assert not m2_e2_unlocked, "M2 E2 should be locked initially"

        # Check TopBar and Prev button
        mod_pill = await page.text_content("#sr-topbar-mod-pill")
        topbar_counter = await page.text_content("#sr-topbar-counter")
        topbar_title = await page.text_content("#sr-topbar-title")
        prev_disabled = await page.is_disabled("#sr-btn-prev")
        print(f"  TopBar Pill: {mod_pill}")
        print(f"  TopBar Counter: {topbar_counter}")
        print(f"  TopBar Title: {topbar_title}")
        print(f"  Prev Button Disabled: {prev_disabled}")
        assert "Módulo 1" in mod_pill
        assert "1/8" in topbar_counter
        assert prev_disabled, "Prev button must be disabled on first exercise of module"

        # Check BottomBar single module stepper and mini pills
        mini_pills = await page.query_selector_all(".sr-mini-pill")
        stepper_nodes = await page.query_selector_all(".sr-step-node")
        print(f"  Mini course pills count: {len(mini_pills)}")
        print(f"  Module 1 stepper nodes count: {len(stepper_nodes)}")
        assert len(mini_pills) == 3, f"Expected 3 mini course pills, got {len(mini_pills)}"
        assert len(stepper_nodes) == 8, f"Expected 8 step nodes, got {len(stepper_nodes)}"

        bottom_counter = await page.text_content("#sr-bottombar-counter")
        print(f"  BottomBar counter: {bottom_counter}")
        assert "1 de 8" in bottom_counter

        # Take screenshot of Initial State
        os.makedirs("tests/screenshots", exist_ok=True)
        await page.screenshot(path="tests/screenshots/01_initial_modular_state.png")

        print("\n[Test 2] Jump directly to Module 2 Exercise 1 without solving Module 1")
        await page.evaluate("window.SocialR.navigation.setActiveIndex(8)")
        await page.wait_for_timeout(500)

        m2_pill = await page.text_content("#sr-topbar-mod-pill")
        m2_counter = await page.text_content("#sr-topbar-counter")
        m2_title = await page.text_content("#sr-topbar-title")
        m2_prev_disabled = await page.is_disabled("#sr-btn-prev")
        m2_bottom_counter = await page.text_content("#sr-bottombar-counter")

        print(f"  M2 TopBar Pill: {m2_pill}")
        print(f"  M2 TopBar Counter: {m2_counter}")
        print(f"  M2 TopBar Title: {m2_title}")
        print(f"  M2 Prev Disabled: {m2_prev_disabled}")
        print(f"  M2 BottomBar Counter: {m2_bottom_counter}")

        assert "Módulo 2" in m2_pill
        assert "1/9" in m2_counter
        assert m2_prev_disabled, "Prev button must be disabled on first exercise of Module 2"
        assert "1 de 9" in m2_bottom_counter
        await page.screenshot(path="tests/screenshots/02_module_2_direct_access.png")

        print("\n[Test 3] Jump to Module 3 Exercise 1 and check drawer")
        await page.evaluate("window.SocialR.navigation.setActiveIndex(17)")
        await page.wait_for_timeout(500)

        m3_pill = await page.text_content("#sr-topbar-mod-pill")
        m3_counter = await page.text_content("#sr-topbar-counter")
        m3_title = await page.text_content("#sr-topbar-title")
        print(f"  M3 TopBar Pill: {m3_pill}")
        print(f"  M3 TopBar Counter: {m3_counter}")
        print(f"  M3 TopBar Title: {m3_title}")
        assert "Módulo 3" in m3_pill
        assert "1/8" in m3_counter

        # Open Drawer
        await page.click("#sr-outline-trigger")
        await page.wait_for_timeout(300)
        drawer_headers = await page.query_selector_all(".sr-drawer-module-header")
        drawer_items = await page.query_selector_all(".sr-drawer-item")
        print(f"  Drawer module sections count: {len(drawer_headers)}")
        print(f"  Drawer exercise items count: {len(drawer_items)}")
        assert len(drawer_headers) == 3, f"Expected 3 drawer module sections, got {len(drawer_headers)}"
        assert len(drawer_items) == 25, f"Expected 25 drawer exercise items, got {len(drawer_items)}"
        await page.screenshot(path="tests/screenshots/03_drawer_modular_outline.png")

        # Close Drawer
        await page.click("#sr-drawer-close")
        await page.wait_for_timeout(200)

        print("\n[Test 4] Module Completion & Academic Celebration Modal")
        # Let's mark all exercises in Module 1 as completed to trigger celebration
        await page.evaluate("""() => {
            const m1_exercises = ['intro-r-01-001', 'intro-r-01-002', 'intro-r-01-003', 'intro-r-01-004', 'intro-r-01-005', 'intro-r-01-006', 'intro-r-01-007', 'intro-r-01-008'];
            m1_exercises.forEach(id => window.SocialR.progress.markCompleted(id, '01-empezar-a-pensar-con-r'));
            window.SocialR.navigation.setActiveIndex(7); // Last exercise in M1
            window.SocialR.navigation.showCelebration('01-empezar-a-pensar-con-r');
        }""")
        await page.wait_for_timeout(500)

        cel_is_open = await page.evaluate("document.getElementById('sr-celebration-backdrop').classList.contains('is-open')")
        cel_title = await page.text_content("#sr-cel-title")
        cel_subtitle = await page.text_content("#sr-cel-subtitle")
        cel_outcomes = await page.query_selector_all("#sr-cel-outcomes-list li")
        btn_text = await page.text_content("#sr-cel-btn-text")

        print(f"  Celebration Modal Open: {cel_is_open}")
        print(f"  Celebration Title: {cel_title}")
        print(f"  Celebration Subtitle: {cel_subtitle}")
        print(f"  Outcomes count: {len(cel_outcomes)}")
        print(f"  Continue Button Text: {btn_text}")

        assert cel_is_open, "Celebration backdrop should be visible"
        assert 2 <= len(cel_outcomes) <= 4, f"Should list between 2 and 4 learning outcomes, got {len(cel_outcomes)}"
        assert "Módulo 2" in btn_text, "CTA button should suggest continuing to Module 2"
        await page.screenshot(path="tests/screenshots/04_celebration_modal.png")

        print("\n[Test 5] Click continue button in celebration modal -> advances to Module 2")
        await page.click("#sr-cel-continue-btn")
        await page.wait_for_timeout(500)

        after_cel_pill = await page.text_content("#sr-topbar-mod-pill")
        after_cel_counter = await page.text_content("#sr-topbar-counter")
        after_cel_title = await page.text_content("#sr-topbar-title")
        print(f"  Current Pill after celebration continue: {after_cel_pill}")
        print(f"  Current Counter after celebration continue: {after_cel_counter}")
        print(f"  Current Title after celebration continue: {after_cel_title}")
        assert "Módulo 2" in after_cel_pill
        assert "1/9" in after_cel_counter

        print("\n[Test 6] Reload page and verify state persistence (Schema v2)")
        await page.reload()
        await page.wait_for_timeout(1000)

        reloaded_pill = await page.text_content("#sr-topbar-mod-pill")
        reloaded_counter = await page.text_content("#sr-topbar-counter")
        reloaded_title = await page.text_content("#sr-topbar-title")
        print(f"  Reloaded TopBar Pill: {reloaded_pill}")
        print(f"  Reloaded TopBar Counter: {reloaded_counter}")
        print(f"  Reloaded TopBar Title: {reloaded_title}")
        assert "Módulo 2" in reloaded_pill
        assert "1/9" in reloaded_counter
        await page.screenshot(path="tests/screenshots/05_reloaded_state_persistence.png")

        print("\n[PASS] All Modular Progression and Independent Unlocking E2E tests succeeded!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_tests())
