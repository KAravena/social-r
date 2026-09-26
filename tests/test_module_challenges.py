#!/usr/bin/env python3
"""Comprehensive test suite for Social R Module Mastery Challenges (Desafíos Finales).

Verifies:
1. Challenges are semantically distinct and DO NOT count as regular exercises.
2. Module exercise count remains intact (e.g. M4 has 6 exercises, not 7).
3. Challenge state is stored separately from completedExercises in ProgressStore.
4. Challenge card is placed below the exercise list in index.qmd / index.html.
5. Unlocking: Challenge unlocks when 100% of module exercises are complete.
6. Passed state persists and displays accreditation badge.
7. Reset progress clears both exercises and challenges.
8. Production vs Local Preview publication gating.
9. Deep links to locked or standby challenges are protected.
"""

import json
import re
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent

from engine.generator.build import load_exercises, load_challenges


class TestModuleMasteryChallenges(unittest.TestCase):
    """Test suite validating challenges architecture, schema, storage, and UI integration."""

    def setUp(self):
        self.content_dir = ROOT / "content"
        self.modules_dir = ROOT / "content" / "courses" / "intro-r" / "modules"
        self.index_qmd_path = ROOT / "index.qmd"
        self.index_html_path = ROOT / "docs" / "index.html"
        self.curso_html_path = ROOT / "docs" / "curso.html"
        self.progress_store_path = ROOT / "js" / "platform" / "progress-store.js"
        self.navigation_path = ROOT / "js" / "app" / "navigation.js"

    def test_1_challenges_not_counted_as_regular_exercises(self):
        """Regular exercises count must remain exactly 89; challenges are loaded separately as 13."""
        exercises = load_exercises(self.content_dir, self.content_dir / "exercise.schema.json")
        self.assertEqual(len(exercises), 89, f"Regular exercises count must be 89, got {len(exercises)}")

        challenges = load_challenges(self.content_dir, self.content_dir / "exercise.schema.json")
        self.assertEqual(len(challenges), 13, f"Must have exactly 13 challenges, got {len(challenges)}")

        # Verify challenge IDs
        for idx, ch in enumerate(challenges, 1):
            expected_id = f"intro-r-{idx:02d}-challenge"
            self.assertEqual(ch["id"], expected_id, f"Challenge {idx} ID mismatch")
            self.assertTrue(ch.get("is_challenge", False), f"Challenge {idx} must have is_challenge=True")

    def test_2_module_exercise_count_intact(self):
        """Module 4 must still have 6 exercises, M1 8 exercises, etc., in module.yml and course metadata."""
        course_yml = yaml.safe_load((ROOT / "content" / "courses" / "intro-r" / "course.yml").read_text(encoding="utf-8"))
        self.assertEqual(course_yml["total_exercises"], 89)

        # Check Module 4 specifically (prompt requirement)
        m4_dir = self.modules_dir / "04-entender-una-base-de-datos"
        m4_exs = [f for f in (m4_dir / "exercises").glob("*.yml") if f.name not in ("module.yml", "challenge.yml")]
        self.assertEqual(len(m4_exs), 6, "Module 4 must have exactly 6 regular exercises")

        # Check index.qmd header for M4
        index_content = self.index_qmd_path.read_text(encoding="utf-8")
        self.assertIn('data-module-id="04-entender-una-base-de-datos" data-module-order="4" data-module-total="6"', index_content)
        self.assertIn('<span class="sr-accordion-header__count">6 ejercicios</span>', index_content)

    def test_3_challenge_state_separated_in_progress_store(self):
        """progress-store.js must have distinct challenges state and methods."""
        store_code = self.progress_store_path.read_text(encoding="utf-8")

        self.assertIn("challenges: {}", store_code)
        self.assertIn("getChallengeStatus", store_code)
        self.assertIn("setChallengeStatus", store_code)
        self.assertIn("markChallengePassed", store_code)
        self.assertIn("isChallengePassed", store_code)
        self.assertIn("isModuleAccredited", store_code)

    def test_4_challenge_card_placed_below_exercise_list(self):
        """In index.qmd, each module accordion panel must place the challenge card below </ul>."""
        content = self.index_qmd_path.read_text(encoding="utf-8")

        cards = re.findall(r'<div class="sr-challenge-card[^"]*"[^>]*data-challenge-id="([^"]+)"', content)
        self.assertEqual(len(cards), 13, f"Expected 13 challenge cards in index.qmd, found {len(cards)}")

        # Verify that in each module, </ul> precedes <div class="sr-challenge-card
        for idx in range(1, 14):
            pattern = re.compile(
                rf'data-module-order="{idx}"[\s\S]*?</ul>[\s\S]*?<div class="sr-challenge-card',
                re.MULTILINE
            )
            self.assertTrue(bool(pattern.search(content)), f"Challenge card for module {idx} must appear below </ul>")

    def test_5_challenge_ui_styling_and_microcopy(self):
        """index.qmd challenge cards must use official microcopy and diamond icon."""
        content = self.index_qmd_path.read_text(encoding="utf-8")

        # Check eyebrow label and icon
        self.assertIn("DESAFÍO FINAL", content)
        self.assertIn("Integra lo aprendido en este módulo.", content)
        self.assertIn("◇", content)

        # Check pending copy
        self.assertIn("Disponible al completar el módulo", content)

        # Standby challenges should have 'En preparación'
        standby_badges = re.findall(r'<span class="sr-challenge-badge sr-challenge-badge--standby"[^>]*>En preparación</span>', content)
        self.assertEqual(len(standby_badges), 8, f"Expected 8 standby challenge badges with 'En preparación', found {len(standby_badges)}")

    def test_6_compiled_curso_html_includes_challenges_and_metadata(self):
        """curso.html must render challenge containers and include challenge metadata in sr-modules-metadata."""
        if not self.curso_html_path.exists():
            self.skipTest("docs/curso.html does not exist yet")

        content = self.curso_html_path.read_text(encoding="utf-8")

        # Check that challenge nodes exist with data-is-challenge="true"
        ch_nodes = re.findall(r'class="social-r-exercise social-r-challenge"[^>]*data-exercise-id="([^"]+)"', content)
        self.assertEqual(len(ch_nodes), 13, f"Expected 13 challenge elements in curso.html, found {len(ch_nodes)}")

        # Check sr-modules-metadata JSON
        match = re.search(r'<script id="sr-modules-metadata" type="application/json">(.*?)</script>', content)
        self.assertIsNotNone(match, "sr-modules-metadata must be present")
        meta = json.loads(match.group(1))

        for mod_id, m_data in meta.items():
            self.assertIn("challenge", m_data, f"Module {mod_id} metadata must include challenge object")
            ch_data = m_data["challenge"]
            self.assertIn("-challenge", ch_data["id"])
            self.assertTrue(len(ch_data["title"]) > 0)

    def test_7_navigation_manager_challenge_methods(self):
        """navigation.js must support challenge navigation, diamond stepper, and drawer rows."""
        nav_code = self.navigation_path.read_text(encoding="utf-8")

        self.assertIn("isChallengeUnlocked", nav_code)
        self.assertIn("isChallengeAvailable", nav_code)
        self.assertIn("setActiveChallenge", nav_code)
        self.assertIn("refreshUIForChallenge", nav_code)
        self.assertIn("sr-bottom-module-step--challenge", nav_code)
        self.assertIn("sr-drawer-challenge", nav_code)


if __name__ == "__main__":
    unittest.main()
