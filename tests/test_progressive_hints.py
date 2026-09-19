#!/usr/bin/env python3
"""Comprehensive Playwright E2E test suite for Progressive Scaffolding Hint System in Social R."""
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "tests" / "screenshots"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


async def run_progressive_hints_tests(url="http://127.0.0.1:4200/"):
    exe_path = None
    for p in EDGE_PATHS:
        if Path(p).exists():
            exe_path = p
            break

    print(f"[TEST] Using browser: {exe_path}")
    print(f"[TEST] Target URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=exe_path,
            headless=True,
            args=["--no-sandbox", "--disable-gpu"],
        )

        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print(f"[TEST] Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector(".is-active-exercise", timeout=20000)

        # Clear progress and enable dev mode for navigation
        await page.evaluate("() => { if (window.SocialR) { window.SocialR.devMode = true; if (window.SocialR.progress) window.SocialR.progress.clearAll(); } }")

        # =========================================================================
        # TEST SUITE 1: 3-Hint Exercise (intro-r-01-004) - Full 4-State Cycle & Screenshots
        # =========================================================================
        print("\n" + "=" * 60)
        print("[TEST SUITE 1] Testing 3-Hint Exercise (intro-r-01-004) full cycle...")
        print("=" * 60)

        # Navigate to Exercise 4 (index 3)
        await page.evaluate("() => { if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(3); }")
        await page.wait_for_timeout(500)

        ex4_id = await page.evaluate("() => document.querySelector('.is-active-exercise').getAttribute('data-exercise-id')")
        print(f"[TEST] Active Exercise ID: {ex4_id}")
        assert ex4_id == "intro-r-01-004", f"Expected intro-r-01-004, got {ex4_id}"

        # Check total hint cards rendered in DOM
        total_hints_ex4 = await page.evaluate("() => document.querySelectorAll('.is-active-exercise .sr-hint-card').length")
        print(f"[TEST] Total hint cards in DOM: {total_hints_ex4}")
        assert total_hints_ex4 == 3, f"Expected 3 hint cards, found {total_hints_ex4}"

        # --- STATE A: 0 Hints Visible ---
        print("\n--- STATE A: 0 Hints Visible ---")
        btn_text_0 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        aria_exp_0 = await page.get_attribute(".is-active-exercise .sr-hint-toggle-btn", "aria-expanded")
        h1_vis_0 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_0 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        h3_vis_0 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        print(f"State A -> Button: '{btn_text_0.strip()}', aria-expanded: {aria_exp_0}, Hints visible: H1={h1_vis_0}, H2={h2_vis_0}, H3={h3_vis_0}")
        assert "Ver pista" in btn_text_0
        assert aria_exp_0 == "false"
        assert not h1_vis_0 and not h2_vis_0 and not h3_vis_0

        # Capture Screenshot State A (0 hints)
        screenshot_a = ARTIFACT_DIR / "screenshot_hint_state_0.png"
        await page.screenshot(path=str(screenshot_a))
        print(f"[SCREENSHOT] Saved State A: {screenshot_a}")

        # --- STATE B: Click 1 -> 1 Hint Visible (Pista 1) ---
        print("\n--- STATE B: Click 1 -> Pista 1 Visible ---")
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(300)

        btn_text_1 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        aria_exp_1 = await page.get_attribute(".is-active-exercise .sr-hint-toggle-btn", "aria-expanded")
        h1_vis_1 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_1 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        h3_vis_1 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        h1_text = await page.inner_text(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        print(f"State B -> Button: '{btn_text_1.strip()}', aria-expanded: {aria_exp_1}, Hints visible: H1={h1_vis_1}, H2={h2_vis_1}, H3={h3_vis_1}")
        assert "Ver otra pista" in btn_text_1
        assert aria_exp_1 == "true"
        assert h1_vis_1, "Hint 1 must be visible"
        assert not h2_vis_1, "Hint 2 must NOT be visible"
        assert not h3_vis_1, "Hint 3 must NOT be visible"
        assert "Pista 1" in h1_text

        # Verify button is below Hint 1
        btn_pos_1 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-toggle-btn').getBoundingClientRect().top")
        h1_pos_1 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-card[data-hint-index=\"1\"]').getBoundingClientRect().bottom")
        print(f"State B -> Geometry: Hint 1 bottom = {h1_pos_1}px, Button top = {btn_pos_1}px")
        assert btn_pos_1 >= h1_pos_1 - 2, "Button must appear below Hint 1"

        # Capture Screenshot State B (1 hint)
        screenshot_b = ARTIFACT_DIR / "screenshot_hint_state_1.png"
        await page.screenshot(path=str(screenshot_b))
        print(f"[SCREENSHOT] Saved State B: {screenshot_b}")

        # --- STATE C: Click 2 -> 2 Hints Visible (Pista 1 + Pista 2) ---
        print("\n--- STATE C: Click 2 -> Pista 1 + Pista 2 Visible ---")
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(300)

        btn_text_2 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        aria_exp_2 = await page.get_attribute(".is-active-exercise .sr-hint-toggle-btn", "aria-expanded")
        h1_vis_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        h3_vis_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        h2_text = await page.inner_text(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        print(f"State C -> Button: '{btn_text_2.strip()}', aria-expanded: {aria_exp_2}, Hints visible: H1={h1_vis_2}, H2={h2_vis_2}, H3={h3_vis_2}")
        assert "Ver otra pista" in btn_text_2
        assert aria_exp_2 == "true"
        assert h1_vis_2 and h2_vis_2, "Hints 1 and 2 must be visible"
        assert not h3_vis_2, "Hint 3 must NOT be visible"
        assert "Pista 2" in h2_text

        # Verify button is below Hint 2
        btn_pos_2 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-toggle-btn').getBoundingClientRect().top")
        h2_pos_2 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-card[data-hint-index=\"2\"]').getBoundingClientRect().bottom")
        print(f"State C -> Geometry: Hint 2 bottom = {h2_pos_2}px, Button top = {btn_pos_2}px")
        assert btn_pos_2 >= h2_pos_2 - 2, "Button must appear below Hint 2"

        # Capture Screenshot State C (2 hints)
        screenshot_c = ARTIFACT_DIR / "screenshot_hint_state_2.png"
        await page.screenshot(path=str(screenshot_c))
        print(f"[SCREENSHOT] Saved State C: {screenshot_c}")

        # --- STATE D: Click 3 -> 3 Hints Visible (Pista 1 + Pista 2 + Pista 3) ---
        print("\n--- STATE D: Click 3 -> All 3 Hints Visible ---")
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(300)

        btn_text_3 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        aria_exp_3 = await page.get_attribute(".is-active-exercise .sr-hint-toggle-btn", "aria-expanded")
        h1_vis_3 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_3 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        h3_vis_3 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        h3_text = await page.inner_text(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        print(f"State D -> Button: '{btn_text_3.strip()}', aria-expanded: {aria_exp_3}, Hints visible: H1={h1_vis_3}, H2={h2_vis_3}, H3={h3_vis_3}")
        assert "Ocultar pistas" in btn_text_3 or "Ocultar pista" in btn_text_3
        assert aria_exp_3 == "true"
        assert h1_vis_3 and h2_vis_3 and h3_vis_3, "All 3 hints must be visible"
        assert "Pista 3" in h3_text
        assert "respuestas_antropologia" in h3_text, "Hint 3 code block must be visible and present"

        # Verify button is below Hint 3
        btn_pos_3 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-toggle-btn').getBoundingClientRect().top")
        h3_pos_3 = await page.evaluate("() => document.querySelector('.is-active-exercise .sr-hint-card[data-hint-index=\"3\"]').getBoundingClientRect().bottom")
        print(f"State D -> Geometry: Hint 3 bottom = {h3_pos_3}px, Button top = {btn_pos_3}px")
        assert btn_pos_3 >= h3_pos_3 - 2, "Button must appear below Hint 3"

        # Capture Screenshot State D (3 hints)
        screenshot_d = ARTIFACT_DIR / "screenshot_hint_state_3.png"
        await page.screenshot(path=str(screenshot_d))
        print(f"[SCREENSHOT] Saved State D: {screenshot_d}")

        # --- COLLAPSE: Click 4 -> Hide all hints ---
        print("\n--- COLLAPSE: Click 4 -> Hide all hints ---")
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(300)

        btn_text_final = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        aria_exp_final = await page.get_attribute(".is-active-exercise .sr-hint-toggle-btn", "aria-expanded")
        h1_vis_f = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_f = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        h3_vis_f = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='3']")
        print(f"Collapse -> Button: '{btn_text_final.strip()}', aria-expanded: {aria_exp_final}, Hints visible: H1={h1_vis_f}, H2={h2_vis_f}, H3={h3_vis_f}")
        assert "Ver pista" in btn_text_final
        assert aria_exp_final == "false"
        assert not h1_vis_f and not h2_vis_f and not h3_vis_f

        # =========================================================================
        # TEST SUITE 2: 2-Hint Exercise (intro-r-01-001) Progression
        # =========================================================================
        print("\n" + "=" * 60)
        print("[TEST SUITE 2] Testing 2-Hint Exercise (intro-r-01-001)...")
        print("=" * 60)

        # Navigate to Exercise 1 (index 0)
        await page.evaluate("() => { if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0); }")
        await page.wait_for_timeout(400)

        ex1_hints_count = await page.evaluate("() => document.querySelectorAll('.is-active-exercise .sr-hint-card').length")
        assert ex1_hints_count == 2, f"Expected 2 hints, found {ex1_hints_count}"

        # State 0
        btn_t0 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert "Ver pista" in btn_t0

        # Click 1 -> 1 visible, button says "Ver otra pista"
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(200)
        e1_h1 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        e1_h2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        btn_t1 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert e1_h1 and not e1_h2
        assert "Ver otra pista" in btn_t1

        # Click 2 -> 2 visible, button says "Ocultar pistas"
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(200)
        e1_h1_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        e1_h2_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        btn_t2 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert e1_h1_2 and e1_h2_2
        assert "Ocultar pistas" in btn_t2 or "Ocultar pista" in btn_t2

        # Click 3 -> reset
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(200)
        e1_h1_3 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        e1_h2_3 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        btn_t3 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert not e1_h1_3 and not e1_h2_3
        assert "Ver pista" in btn_t3

        # =========================================================================
        # TEST SUITE 3: Navigation Reset Isolation
        # =========================================================================
        print("\n" + "=" * 60)
        print("[TEST SUITE 3] Testing Navigation Hint Reset Isolation...")
        print("=" * 60)

        # Open 1 hint in Ex 1
        await page.click(".is-active-exercise .sr-hint-toggle-btn")
        await page.wait_for_timeout(200)
        assert await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")

        # Navigate to Exercise 2 (index 1)
        await page.evaluate("() => { if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(1); }")
        await page.wait_for_timeout(300)

        # Exercise 2 should have 0 hints visible
        ex2_h1 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        ex2_btn = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert not ex2_h1, "Exercise 2 must start with hints closed"
        assert "Ver pista" in ex2_btn

        # Navigate back to Exercise 1 (index 0)
        await page.evaluate("() => { if (window.SocialR && window.SocialR.navigation) window.SocialR.navigation.setActiveIndex(0); }")
        await page.wait_for_timeout(300)

        # Exercise 1 returned to should now have hints closed (fresh return)
        ex1_h1_ret = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        ex1_btn_ret = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
        assert not ex1_h1_ret, "Exercise 1 upon return must have hints closed"
        assert "Ver pista" in ex1_btn_ret

        # =========================================================================
        # TEST SUITE 4: ProgressStore & Grader Non-Contamination
        # =========================================================================
        print("\n" + "=" * 60)
        print("[TEST SUITE 4] Testing ProgressStore Non-Contamination...")
        print("=" * 60)

        progress_raw = await page.evaluate("() => window.SocialR.progress.get('intro-r-01-001')")
        print(f"[TEST] Ex 1 ProgressStore state: {progress_raw}")
        assert progress_raw.get("status") != "completed", "Opening hints must NEVER complete the exercise"

        print("\n" + "=" * 60)
        print("[ALL PROGRESSIVE HINT TESTS PASSED SUCCESSFULLY!]")
        print("=" * 60)

        await browser.close()


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4200/"
    asyncio.run(run_progressive_hints_tests(target_url))
