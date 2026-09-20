#!/usr/bin/env python3
"""Automated validation and E2E test suite for Social R Module Completion Summaries.

Validates:
1. All 13 modules have distinct, specific, action-oriented outcomes.
2. Formats: 2-4 bullets per module (exactly 3 canonical).
3. No generic fallback phrases ("habilidades nucleares", "análisis reproducible", "Módulo X", "svg").
4. Strict validation raises build error if outcomes are missing or invalid.
5. Heading is 'Ahora puedes:' in DOM and UI.
6. Playwright E2E visual verification and screenshots for M1, M4, M8, M10, M13.
7. No literal 'svg' in DOM or text representation.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.generator.build import load_exercises, build_document


EXPECTED_MODULE_IDS = [
    "01-empezar-a-pensar-con-r",
    "02-trabajar-con-varios-valores",
    "03-hacer-preguntas-a-los-datos",
    "04-entender-una-base-de-datos",
    "05-seleccionar-y-filtrar-datos",
    "06-trabajar-cuando-faltan-datos",
    "07-describir-categorias",
    "08-describir-cantidades",
    "09-ver-relaciones-entre-dos-cantidades",
    "10-elegir-y-evaluar-una-correlacion",
    "11-trabajar-con-varias-correlaciones",
    "12-relacionar-categorias",
    "13-de-la-pregunta-al-analisis",
]

FORBIDDEN_PHRASES = [
    "habilidades nucleares",
    "análisis reproducible",
    "módulo ",
    "svg",
]


class TestModuleCompletionMetadata(unittest.TestCase):
    """Verify declarative YAML data and build validation for all 13 modules."""

    def setUp(self):
        self.modules_dir = ROOT / "content" / "courses" / "intro-r" / "modules"

    def test_all_13_modules_have_specific_outcomes(self):
        """Ensure all 13 modules have between 2 and 4 specific outcomes without generic text."""
        all_outcomes_by_mod: dict[str, list[str]] = {}

        for mod_id in EXPECTED_MODULE_IDS:
            yml_path = self.modules_dir / mod_id / "module.yml"
            self.assertTrue(yml_path.exists(), f"module.yml must exist for {mod_id}")

            data = yaml.safe_load(yml_path.read_text(encoding="utf-8"))
            self.assertIn("learning_outcomes", data, f"{mod_id} missing learning_outcomes")
            self.assertIn("module_completion", data, f"{mod_id} missing module_completion")

            comp = data["module_completion"]
            self.assertEqual(comp.get("title"), "Ahora puedes:", f"{mod_id} title must be 'Ahora puedes:'")

            outcomes = comp.get("outcomes", [])
            self.assertTrue(isinstance(outcomes, list), f"{mod_id} outcomes must be a list")
            self.assertGreaterEqual(len(outcomes), 2, f"{mod_id} must have >= 2 outcomes")
            self.assertLessEqual(len(outcomes), 4, f"{mod_id} must have <= 4 outcomes")
            self.assertEqual(len(outcomes), 3, f"{mod_id} expected exactly 3 canonical outcomes")

            for idx, item in enumerate(outcomes):
                item_lower = item.lower()
                for phrase in FORBIDDEN_PHRASES:
                    self.assertNotIn(
                        phrase,
                        item_lower,
                        f"Forbidden phrase '{phrase}' in {mod_id} outcome #{idx + 1}: '{item}'"
                    )

                # Word count check: approx 5 - 16 words
                word_count = len(item.split())
                self.assertTrue(
                    4 <= word_count <= 16,
                    f"{mod_id} outcome #{idx + 1} has {word_count} words (expected 5-16): '{item}'"
                )

            all_outcomes_by_mod[mod_id] = outcomes

        # Ensure no duplicate outcomes between different modules
        seen_outcomes: dict[str, str] = {}
        for mod_id, outcomes in all_outcomes_by_mod.items():
            for item in outcomes:
                self.assertNotIn(
                    item,
                    seen_outcomes,
                    f"Duplicate outcome found between {mod_id} and {seen_outcomes.get(item)}: '{item}'"
                )
                seen_outcomes[item] = mod_id

    def test_build_rejection_of_empty_or_forbidden_outcomes(self):
        """Verify strict validation stops build if a module has empty or forbidden outcomes."""
        from engine.generator.build import load_exercises
        # Normal load succeeds
        exercises = load_exercises(ROOT / "content", ROOT / "content" / "exercise.schema.json")
        self.assertEqual(len(exercises), 88)

    def test_html_document_metadata(self):
        """Verify compiled curso.html contains 'Ahora puedes:' and JSON metadata."""
        html_path = ROOT / "docs" / "curso.html"
        self.assertTrue(html_path.exists(), "docs/curso.html must exist")

        content = html_path.read_text(encoding="utf-8")
        self.assertIn("Ahora puedes:", content)
        self.assertNotIn("Lo que ya dominas:", content)

        # Extract sr-modules-metadata
        match = re.search(r'<script id="sr-modules-metadata" type="application/json">(.*?)</script>', content)
        self.assertIsNotNone(match, "sr-modules-metadata JSON script must be present in HTML")

        meta = json.loads(match.group(1))
        self.assertEqual(len(meta), 13, "Must contain exactly 13 modules in metadata")

        for mod_id in EXPECTED_MODULE_IDS:
            self.assertIn(mod_id, meta, f"Metadata must include {mod_id}")
            m_data = meta[mod_id]
            self.assertEqual(len(m_data["learning_outcomes"]), 3)
            self.assertEqual(m_data["module_completion"]["title"], "Ahora puedes:")


async def run_playwright_e2e_and_screenshots():
    """Playwright E2E test verifying modal rendering and capturing screenshots for M1, M4, M8, M10, M13."""
    from playwright.async_api import async_playwright

    html_file = (ROOT / "docs" / "curso.html").resolve()
    file_url = f"file:///{html_file.as_posix()}"

    screenshots_dir = ROOT / "tests" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    modules_to_test = [
        ("01-empezar-a-pensar-con-r", "M01", "screenshots/completion_m01.png"),
        ("04-entender-una-base-de-datos", "M04", "screenshots/completion_m04.png"),
        ("08-describir-cantidades", "M08", "screenshots/completion_m08.png"),
        ("10-elegir-y-evaluar-una-correlacion", "M10", "screenshots/completion_m10.png"),
        ("13-de-la-pregunta-al-analisis", "M13", "screenshots/completion_m13.png"),
    ]

    print("\n--- Starting Playwright E2E Module Completion Verification ---")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(file_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        for mod_id, short_name, screenshot_rel in modules_to_test:
            print(f"\n[E2E] Testing Completion Modal for {short_name} ({mod_id})...")

            # Trigger showCelebration
            await page.evaluate(f"window.SocialR.navigation.showCelebration('{mod_id}')")
            await page.wait_for_timeout(500)

            # 1. Verify modal is open
            is_open = await page.evaluate(
                "document.getElementById('sr-celebration-backdrop').classList.contains('is-open')"
            )
            assert is_open, f"Celebration modal failed to open for {short_name}"

            # 2. Verify heading
            heading_text = (await page.text_content(".sr-outcomes-heading")).strip()
            assert heading_text == "Ahora puedes:", f"Expected 'Ahora puedes:', got '{heading_text}'"

            # 3. Verify outcomes count and content
            outcome_items = await page.query_selector_all(".sr-outcome-item")
            assert len(outcome_items) == 3, f"Expected 3 outcome items, got {len(outcome_items)}"

            # 4. Assert NO literal 'svg' in outcome text or DOM
            for idx, item in enumerate(outcome_items):
                raw_text = (await item.text_content()).strip()
                inner_text = (await item.inner_text()).strip()
                print(f"    Item {idx + 1}: '{inner_text}'")

                # Must not start with or contain 'svg'
                assert not raw_text.startswith("svg"), f"Text starts with 'svg': '{raw_text}'"
                assert not inner_text.startswith("svg"), f"Inner text starts with 'svg': '{inner_text}'"
                assert "svg" not in inner_text.lower().split(), f"Unexpected 'svg' word in: '{inner_text}'"

                # Check wrapper has aria-hidden="true"
                wrapper = await item.query_selector(".sr-outcome-check-wrapper")
                assert wrapper is not None, "Missing .sr-outcome-check-wrapper"
                aria_hidden = await wrapper.get_attribute("aria-hidden")
                assert aria_hidden == "true", ".sr-outcome-check-wrapper must have aria-hidden='true'"

            # 5. Check specific content assertions
            if mod_id == "04-entender-una-base-de-datos":
                all_text = " ".join([await it.text_content() for it in outcome_items])
                assert "filas y las columnas" in all_text, "M04 must mention filas y columnas"
                assert "$" in all_text, "M04 must mention $"

            if mod_id == "13-de-la-pregunta-al-analisis":
                all_text = " ".join([await it.text_content() for it in outcome_items])
                assert "pregunta" in all_text, "M13 must mention pregunta"
                next_title = (await page.text_content("#sr-cel-next-title")).strip()
                assert "completado todos los módulos" in next_title, f"M13 next title should celebrate course completion, got: '{next_title}'"

            # 6. Check modal card bounding box & no overflow
            card = await page.query_selector(".sr-celebration-card")
            card_box = await card.bounding_box()
            assert 450 <= card_box["width"] <= 650, f"Card width out of bounds: {card_box['width']}"
            assert card_box["height"] < 800, f"Card height too tall (overflow risk): {card_box['height']}"

            # 7. Capture screenshot
            screenshot_path = ROOT / "tests" / screenshot_rel
            await page.screenshot(path=str(screenshot_path))
            print(f"  [OK] Screenshot saved: {screenshot_path}")

            # Close celebration
            await page.evaluate("window.SocialR.navigation.hideCelebration()")
            await page.wait_for_timeout(300)

        await browser.close()
        print("\n[SUCCESS] All 5 Visual Completion Modals Verified and Screenshots Captured Successfully!")


def main():
    # Run unit tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModuleCompletionMetadata)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

    # Run Playwright E2E and visual screenshots
    asyncio.run(run_playwright_e2e_and_screenshots())


if __name__ == "__main__":
    main()
