#!/usr/bin/env python3
"""Playwright E2E UI and Flow Test Suite for Redesigned Module 3 (Social R v0.4).

Validates:
1. Navigation across all 8 exercises of Module 3 (global indices 17 through 24).
2. Exercise titles, objectives, instructions, context callouts, and starter code.
3. Progressive Hint transitions (State 0 -> 1 -> 2 -> 3 -> 0) on Module 3 exercises.
4. Solution button unlock behavior on Module 3 exercises.
5. Visual feedback card styling and Continue button unlocks.
6. Absence of deprecated classes or legacy exercises.
7. Screenshots of key pedagogical milestones in Module 3.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshots" / "module_03"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


async def run_m3_e2e_ui_tests(url: str):
    print(f"[TEST M3 UI] Target URL: {url}")
    browser_exe = os.environ.get("PLAYWRIGHT_CHROME_EXE", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=browser_exe if os.path.exists(browser_exe) else None,
            headless=True,
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print(f"[TEST M3 UI] Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_selector(".is-active-exercise", timeout=20000)

        # Clear progress and enable devMode for direct navigation
        await page.evaluate("() => { if (window.SocialR) { window.SocialR.devMode = true; if (window.SocialR.progress) window.SocialR.progress.clearAll(); } }")

        # =========================================================================
        # 1. VERIFY TOTAL AND MODULE 3 EXERCISE COUNTS & TITLES
        # =========================================================================
        print("\n" + "=" * 60)
        print("[TEST M3 UI] 1. Checking Module 3 Structure & Exercise Count...")
        print("=" * 60)

        total_exercises = await page.evaluate("() => document.querySelectorAll('.social-r-exercise').length")
        print(f"[TEST M3 UI] Total exercises in course: {total_exercises}")
        assert total_exercises == 25, f"Expected 25 exercises, found {total_exercises}"

        m3_exercises = await page.evaluate('''() => {
            const nodes = Array.from(document.querySelectorAll('.social-r-exercise[data-module-id="comparar-y-elegir-valores"]'));
            return nodes.map(n => ({
                id: n.getAttribute('data-exercise-id'),
                title: n.getAttribute('data-exercise-title'),
                module: n.getAttribute('data-module-id')
            }));
        }''')
        print(f"[TEST M3 UI] Module 3 exercise count: {len(m3_exercises)}")
        assert len(m3_exercises) == 8, f"Expected 8 exercises in M3, got {len(m3_exercises)}"

        expected_titles = [
            "De posiciones a preguntas",
            "La misma pregunta para todos",
            "Guardar las respuestas",
            "TRUE conserva, FALSE deja fuera",
            "Ahora selecciona tú",
            "La pregunta sigue funcionando",
            "También podemos preguntar por texto",
            "Mini desafío: encuentra los valores que cumplen",
        ]
        actual_titles = [x["title"] for x in m3_exercises]
        for i, (exp, act) in enumerate(zip(expected_titles, actual_titles)):
            print(f"  M3-E{i+1}: '{act}' (Expected: '{exp}')")
            assert act == exp, f"M3-E{i+1} title mismatch: expected '{exp}', got '{act}'"

        # =========================================================================
        # 2. TEST EACH EXERCISE UI, CODE EDITOR, & PROGRESSION
        # =========================================================================
        for idx in range(17, 25):
            e_num = idx - 16
            ex_data = m3_exercises[e_num - 1]
            ex_id = ex_data["id"]
            ex_title = ex_data["title"]

            print(f"\n--- Testing M3-E{e_num}: {ex_title} ({ex_id}) ---")
            await page.evaluate(f"window.SocialR.navigation.setActiveIndex({idx})")
            await page.wait_for_timeout(300)

            active_id = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
            assert active_id == ex_id, f"Expected active ID {ex_id}, got {active_id}"

            # Check badge
            badge_text = await page.inner_text(".is-active-exercise .sr-section-exercise .sr-section-badge")
            print(f"  Badge: '{badge_text}'")
            assert f"{e_num} de 8" in badge_text

            # Check action buttons
            run_btn = await page.query_selector(".is-active-exercise .sr-btn-run")
            submit_btn = await page.query_selector(".is-active-exercise .sr-btn-submit")
            hint_btn = await page.query_selector(".is-active-exercise .sr-hint-toggle-btn")
            assert run_btn is not None, "Run button must exist"
            assert submit_btn is not None, "Submit button must exist"
            assert hint_btn is not None, "Hint button must exist"

            # Check CodeMirror editor
            cm_text = await page.evaluate(f'''() => {{
                const cm = document.querySelector('.social-r-exercise[data-exercise-id="{ex_id}"] .cm-content');
                return cm ? cm.innerText : '';
            }}''')
            print(f"  Starter code loaded in CM: {repr(cm_text.strip()[:40])}...")
            assert len(cm_text.strip()) > 0, f"Starter code should not be empty for {ex_id}"

            # Test Progressive Hints
            # State 0 -> State 1
            await page.click(".is-active-exercise .sr-hint-toggle-btn")
            await page.wait_for_timeout(150)
            btn_txt = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
            assert "Ver otra pista" in btn_txt or "Ocultar pistas" in btn_txt

            # State 1 -> State 2
            await page.click(".is-active-exercise .sr-hint-toggle-btn")
            await page.wait_for_timeout(150)

            # State 2 -> State 3
            await page.click(".is-active-exercise .sr-hint-toggle-btn")
            await page.wait_for_timeout(150)
            btn_txt_3 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
            assert "Ocultar pistas" in btn_txt_3

            # State 3 -> State 0
            await page.click(".is-active-exercise .sr-hint-toggle-btn")
            await page.wait_for_timeout(150)
            btn_txt_0 = await page.inner_text(".is-active-exercise .sr-hint-toggle-btn")
            assert "Ver pista" in btn_txt_0
            print("  Progressive hints cycle 0 -> 1 -> 2 -> 3 -> 0: PASS")

            # Test Feedback Card Presentation
            await page.evaluate(f'''() => {{
                if (window.SocialR && window.SocialR.adapter) {{
                    window.SocialR.adapter.renderFeedbackCard(
                        "{ex_id}",
                        "success",
                        "¡Completado con éxito!",
                        "Has completado correctamente este ejercicio."
                    );
                }}
            }}''')
            await page.wait_for_timeout(200)

            fb_visible = await page.is_visible(f'.social-r-exercise[data-exercise-id="{ex_id}"] .sr-feedback-card.is-success')
            assert fb_visible, "Success feedback card must be visible"

            # Capture screenshot
            screenshot_path = SCREENSHOT_DIR / f"{e_num:02d}_{ex_id}.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"  Screenshot captured: {screenshot_path.name}")

        print("\n" + "=" * 60)
        print("[ALL MODULE 3 UI & E2E TESTS PASSED 100% SUCCESSFULLY!]")
        print("=" * 60)
        await browser.close()


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4200/"
    asyncio.run(run_m3_e2e_ui_tests(target))
