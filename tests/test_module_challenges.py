#!/usr/bin/env python3
"""Comprehensive test suite for Social R Module Mastery Challenges (Desafíos Finales)
and Accreditation Progression Gate Architecture.

Tests cover:
1. Challenges are semantically distinct and DO NOT count as regular exercises (89 exercises, 13 challenges).
2. Module exercise count remains intact (e.g. M4 has 6 exercises, not 7).
3. Challenge state is stored separately from completedExercises in ProgressStore.
4. Microcopy: eliminates "Disponible al completar el módulo"; shows "Demuestra lo que sabes y acredita el módulo."
5. Test Principal 1: New user (0/8 exercises) -> Challenge M1 is AVAILABLE.
6. Test Principal 2: PASS M1 challenge -> M2 is UNLOCKED; M1 exercises stay 0/8.
7. Test Principal 3: Complete 8/8 M1 without challenge -> M2 remains LOCKED; badge shows "Práctica completada".
8. Test Principal 4: FAIL challenge -> M2 remains LOCKED; M1 practice remains available.
9. Test Principal 5: PASS M1, M2, M3 challenges with 0 exercises -> M4 is UNLOCKED; exercises count remains 0.
10. Test Principal 6: PASS M5 in production -> M6 standby is NOT accessible.
11. Test Principal 7: PASS M5 in localhost -> M6 is accessible via Local Preview.
12. Test Principal 8: Deep link to current unlocked challenge is permitted (even with 0/N).
13. Test Principal 9: Deep link to locked next module is blocked.
14. Test Principal 10: Global reset clears challenge accreditation and re-locks progression.
"""

import asyncio
import http.server
import json
import re
import threading
import unittest
from pathlib import Path
import yaml
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent

from engine.generator.build import load_exercises, load_challenges


class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "docs"), **kwargs)

    def log_message(self, format, *args):
        pass


def make_progress_json(challenges=None, completed_exercises=None):
    """Helper creating schema v2 localStorage progress state."""
    state = {
        "version": 2,
        "contentVersion": "2026.03.1",
        "courseId": "intro-r",
        "activeModuleId": "01-empezar-a-pensar-con-r",
        "currentExerciseId": "intro-r-01-001",
        "modules": {},
        "challenges": {},
        "editorState": {},
        "lastActivity": "2026-09-26T12:00:00.000Z",
    }
    if challenges:
        for mod_id in challenges:
            state["challenges"][mod_id] = {"status": "passed", "passedAt": "2026-09-26T12:00:00.000Z"}
            if mod_id not in state["modules"]:
                state["modules"][mod_id] = {"id": mod_id, "completedExercises": [], "completed": False, "accredited": True}
            else:
                state["modules"][mod_id]["accredited"] = True

    if completed_exercises:
        for mod_id, ex_list in completed_exercises.items():
            if mod_id not in state["modules"]:
                state["modules"][mod_id] = {"id": mod_id, "completedExercises": ex_list, "completed": False, "accredited": False}
            else:
                state["modules"][mod_id]["completedExercises"] = ex_list

    return json.dumps(state)


class TestModuleMasteryChallengesStatic(unittest.TestCase):
    """Test suite validating challenges architecture, schema, storage, and UI templates."""

    def setUp(self):
        self.content_dir = ROOT / "content"
        self.modules_dir = ROOT / "content" / "courses" / "intro-r" / "modules"
        self.index_qmd_path = ROOT / "index.qmd"
        self.index_html_path = ROOT / "docs" / "index.html"
        self.curso_html_path = ROOT / "docs" / "curso.html"
        self.progress_store_path = ROOT / "js" / "platform" / "progress-store.js"
        self.navigation_path = ROOT / "js" / "app" / "navigation.js"
        self.course_config_path = ROOT / "js" / "platform" / "course-config.js"

    def test_1_challenges_not_counted_as_regular_exercises(self):
        """Regular exercises count must remain exactly 89; challenges are loaded separately as 13."""
        exercises = load_exercises(self.content_dir, self.content_dir / "exercise.schema.json")
        self.assertEqual(len(exercises), 89, f"Regular exercises count must be 89, got {len(exercises)}")

        challenges = load_challenges(self.content_dir, self.content_dir / "exercise.schema.json")
        self.assertEqual(len(challenges), 13, f"Must have exactly 13 challenges, got {len(challenges)}")

        for idx, ch in enumerate(challenges, 1):
            expected_id = f"intro-r-{idx:02d}-challenge"
            self.assertEqual(ch["id"], expected_id, f"Challenge {idx} ID mismatch")
            self.assertTrue(ch.get("is_challenge", False), f"Challenge {idx} must have is_challenge=True")

    def test_2_module_exercise_count_intact(self):
        """Module 4 must still have 6 exercises, M1 8 exercises, etc."""
        course_yml = yaml.safe_load((ROOT / "content" / "courses" / "intro-r" / "course.yml").read_text(encoding="utf-8"))
        self.assertEqual(course_yml["total_exercises"], 89)

        m4_dir = self.modules_dir / "04-entender-una-base-de-datos"
        m4_exs = [f for f in (m4_dir / "exercises").glob("*.yml") if f.name not in ("module.yml", "challenge.yml")]
        self.assertEqual(len(m4_exs), 6, "Module 4 must have exactly 6 regular exercises")

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

        for idx in range(1, 14):
            pattern = re.compile(
                rf'data-module-order="{idx}"[\s\S]*?</ul>[\s\S]*?<div class="sr-challenge-card',
                re.MULTILINE
            )
            self.assertTrue(bool(pattern.search(content)), f"Challenge card for module {idx} must appear below </ul>")

    def test_5_challenge_ui_styling_and_clean_microcopy(self):
        """Eliminate 'Disponible al completar el módulo'; use 'Demuestra lo que sabes y acredita el módulo.'"""
        content = self.index_qmd_path.read_text(encoding="utf-8")
        self.assertNotIn("Disponible al completar el módulo", content, "Old microcopy must be completely eliminated from index.qmd")
        self.assertIn("Demuestra lo que sabes y acredita el módulo.", content)
        self.assertIn("DESAFÍO FINAL", content)
        self.assertIn("◇", content)

    def test_6_central_course_config_progression_helpers(self):
        """course-config.js must contain single-source-of-truth progression helpers."""
        config_code = self.course_config_path.read_text(encoding="utf-8")
        self.assertIn("isModuleSatisfied", config_code)
        self.assertIn("isModuleUnlocked", config_code)
        self.assertIn("isChallengeUnlocked", config_code)
        self.assertIn("canNavigateToModule", config_code)
        self.assertIn("isExerciseUnlocked", config_code)


class TestModuleMasteryChallengesE2E(unittest.IsolatedAsyncioTestCase):
    """Playwright E2E and functional tests executing the 10 Principal Tests."""

    @classmethod
    def setUpClass(cls):
        cls.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DocsHTTPHandler)
        cls.port = cls.httpd.server_address[1]
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.index_url = f"{cls.base_url}/index.html"
        cls.curso_url = f"{cls.base_url}/curso.html"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    async def asyncSetUp(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(viewport={"width": 1280, "height": 800})

    async def asyncTearDown(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def test_principal_1_new_user_m1_challenge_available(self):
        """TEST PRINCIPAL 1:
        Nuevo usuario: M1 0/8 ejercicios. Challenge M1: AVAILABLE (button 'Comenzar desafío →').
        """
        page = await self.context.new_page()
        await page.goto(self.index_url)
        await page.evaluate("() => localStorage.clear()")
        await page.reload()

        m1_card = page.locator('.sr-accordion-item[data-module-id="01-empezar-a-pensar-con-r"] .sr-challenge-card')
        card_class = await m1_card.get_attribute("class")
        self.assertIn("is-available", card_class)

        btn = m1_card.locator(".sr-challenge-btn--available")
        self.assertTrue(await btn.is_visible())
        btn_text = await btn.inner_text()
        self.assertIn("Comenzar desafío", btn_text)

        # In curso.html, M1 challenge is unlocked from 0/8
        await page.goto(self.curso_url)
        is_ch1_unlocked = await page.evaluate(
            "() => window.SocialR.courseConfig.isChallengeUnlocked('01-empezar-a-pensar-con-r')"
        )
        self.assertTrue(is_ch1_unlocked)

    async def test_principal_2_pass_m1_challenge_unlocks_m2_with_zero_exercises(self):
        """TEST PRINCIPAL 2:
        PASS M1 challenge -> M2: UNLOCKED. Ejercicios M1: siguen 0/8 (no se inflan).
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(challenges=["01-empezar-a-pensar-con-r"])
        await page.goto(self.index_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        # Check exercise count remains 0 in hero and M1 badge
        hero_line = await page.locator("#sr-hero-progress-line").inner_text()
        self.assertIn("0/", hero_line)

        m1_badge = await page.locator('.sr-accordion-item[data-module-id="01-empezar-a-pensar-con-r"] .sr-module-badge').inner_text()
        self.assertIn("Acreditado", m1_badge)
        self.assertIn("0/8", m1_badge)

        # Check M2 is now UNLOCKED
        m2_card = page.locator('.sr-accordion-item[data-module-id="02-trabajar-con-varios-valores"] .sr-challenge-card')
        card_class = await m2_card.get_attribute("class")
        self.assertIn("is-available", card_class)

        # In curso.html
        await page.goto(self.curso_url)
        is_m2_unlocked = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('02-trabajar-con-varios-valores')"
        )
        self.assertTrue(is_m2_unlocked)

        # Exercises in M1 still completed = 0
        comp_count = await page.evaluate(
            "() => window.SocialR.progress.getModuleState('01-empezar-a-pensar-con-r').completedExercises.length"
        )
        self.assertEqual(comp_count, 0)

    async def test_principal_3_complete_practice_without_challenge_keeps_m2_locked(self):
        """TEST PRINCIPAL 3:
        Completar 8/8 M1. No hacer challenge. M2: LOCKED.
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(completed_exercises={
            "01-empezar-a-pensar-con-r": [
                "intro-r-01-001", "intro-r-01-002", "intro-r-01-003", "intro-r-01-004",
                "intro-r-01-005", "intro-r-01-006", "intro-r-01-007", "intro-r-01-008"
            ]
        })
        await page.goto(self.index_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        # M1 badge shows "Práctica completada"
        m1_badge = await page.locator('.sr-accordion-item[data-module-id="01-empezar-a-pensar-con-r"] .sr-module-badge').inner_text()
        self.assertIn("Práctica completada", m1_badge)

        # M2 remains LOCKED
        m2_card = page.locator('.sr-accordion-item[data-module-id="02-trabajar-con-varios-valores"] .sr-challenge-card')
        card_class = await m2_card.get_attribute("class")
        self.assertIn("is-module-locked", card_class)

        m2_badge_text = await m2_card.locator(".sr-challenge-badge").inner_text()
        self.assertIn("Disponible cuando acredites el módulo anterior", m2_badge_text)

        m2_hdr_badge = await page.locator('.sr-accordion-item[data-module-id="02-trabajar-con-varios-valores"] .sr-module-badge').inner_text()
        self.assertIn("Bloqueado", m2_hdr_badge)

        # In curso.html, M2 is locked
        await page.goto(self.curso_url)
        is_m2_unlocked = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('02-trabajar-con-varios-valores')"
        )
        self.assertFalse(is_m2_unlocked)

    async def test_principal_4_fail_challenge_keeps_m2_locked(self):
        """TEST PRINCIPAL 4:
        FAIL challenge. M2: LOCKED. M1 practice sigue disponible.
        """
        page = await self.context.new_page()
        fail_state = {
            "version": 2,
            "contentVersion": "2026.03.1",
            "courseId": "intro-r",
            "modules": {
                "01-empezar-a-pensar-con-r": {"id": "01-empezar-a-pensar-con-r", "completedExercises": [], "completed": False, "accredited": False}
            },
            "challenges": {
                "01-empezar-a-pensar-con-r": {"status": "in_progress", "attempts": 1}
            }
        }
        prog_json = json.dumps(fail_state)
        await page.goto(self.curso_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        # M2 is locked
        is_m2_unlocked = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('02-trabajar-con-varios-valores')"
        )
        self.assertFalse(is_m2_unlocked)

        # M1 practice is still available
        is_ex1_unlocked = await page.evaluate(
            "() => window.SocialR.navigation.isUnlocked(0)"
        )
        self.assertTrue(is_ex1_unlocked)

    async def test_principal_5_fast_track_challenges_unlocks_m4_zero_exercises(self):
        """TEST PRINCIPAL 5:
        PASS M1 challenge, PASS M2 challenge, PASS M3 challenge sin ejercicios.
        M4: UNLOCKED. Contador de ejercicios: 0 completados.
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(challenges=[
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores",
            "03-hacer-preguntas-a-los-datos"
        ])
        await page.goto(self.index_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        # Hero exercises counter is 0
        hero_line = await page.locator("#sr-hero-progress-line").inner_text()
        self.assertIn("0/", hero_line)

        # M4 is UNLOCKED
        m4_card = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-challenge-card')
        card_class = await m4_card.get_attribute("class")
        self.assertIn("is-available", card_class)

        # Expand M4 accordion to check button
        await page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header').click()
        btn = m4_card.locator(".sr-challenge-btn--available")
        self.assertTrue(await btn.is_visible())
        self.assertIn("Comenzar desafío", await btn.inner_text())

        # In curso.html, M4 is unlocked
        await page.goto(self.curso_url)
        is_m4_unlocked = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('04-entender-una-base-de-datos')"
        )
        self.assertTrue(is_m4_unlocked)

    async def test_principal_6_pass_m5_in_production_m6_standby_not_accessible(self):
        """TEST PRINCIPAL 6:
        PASS M5 en producción (simulated non-localhost). M6 standby: NO accesible.
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(challenges=[
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores",
            "03-hacer-preguntas-a-los-datos",
            "04-entender-una-base-de-datos",
            "05-seleccionar-y-filtrar-datos"
        ])
        await page.goto(self.curso_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        result = await page.evaluate("""() => {
            const config = window.SocialR.courseConfig;
            // Force production mode simulation
            const origPreview = config.isLocalPreview;
            config.isLocalPreview = () => false;

            const isM6Avail = config.isModuleAvailable("06-trabajar-cuando-faltan-datos");
            const canNavM6 = config.canNavigateToModule("06-trabajar-cuando-faltan-datos");
            const isM6Unlocked = config.isModuleUnlocked("06-trabajar-cuando-faltan-datos");

            // Restore
            config.isLocalPreview = origPreview;
            return { isM6Avail, canNavM6, isM6Unlocked };
        }""")
        self.assertFalse(result["isM6Avail"], "M6 must not be available in production mode")
        self.assertFalse(result["canNavM6"], "Cannot navigate to M6 in production mode")
        self.assertFalse(result["isM6Unlocked"], "M6 must not be unlocked in production mode")

    async def test_principal_7_pass_m5_in_localhost_m6_accessible_via_preview(self):
        """TEST PRINCIPAL 7:
        PASS M5 en localhost. M6: accesible mediante Local Preview.
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(challenges=[
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores",
            "03-hacer-preguntas-a-los-datos",
            "04-entender-una-base-de-datos",
            "05-seleccionar-y-filtrar-datos"
        ])
        await page.goto(self.curso_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        result = await page.evaluate("""() => {
            const config = window.SocialR.courseConfig;
            const isLocal = config.isLocalPreview();
            const isM6Avail = config.isModuleAvailable("06-trabajar-cuando-faltan-datos");
            const isM6Unlocked = config.isModuleUnlocked("06-trabajar-cuando-faltan-datos");
            const canNavM6 = config.canNavigateToModule("06-trabajar-cuando-faltan-datos");

            return { isLocal, isM6Avail, isM6Unlocked, canNavM6 };
        }""")
        self.assertTrue(result["isLocal"], "Host 127.0.0.1 must be recognized as local preview")
        self.assertTrue(result["isM6Avail"], "M6 is available under local preview")
        self.assertTrue(result["isM6Unlocked"], "M6 is unlocked after M5 challenge passed")
        self.assertTrue(result["canNavM6"], "Can navigate to M6 under local preview after M5 challenge passed")

    async def test_principal_8_deep_link_to_unlocked_challenge_permitted(self):
        """TEST PRINCIPAL 8:
        Deep link challenge actual: permitido si módulo desbloqueado (incluso con 0/N).
        """
        page = await self.context.new_page()
        await page.goto(f"{self.curso_url}#intro-r-01-challenge")
        await page.wait_for_timeout(400)

        is_viewing = await page.evaluate("() => window.SocialR.navigation.isViewingChallenge")
        active_ch_id = await page.evaluate("() => window.SocialR.navigation.activeChallenge ? window.SocialR.navigation.activeChallenge.id : null")
        self.assertTrue(is_viewing, "Must be viewing challenge")
        self.assertEqual(active_ch_id, "intro-r-01-challenge")

    async def test_principal_9_deep_link_to_locked_next_module_blocked(self):
        """TEST PRINCIPAL 9:
        Deep link siguiente módulo (ej. #intro-r-04-001 o #intro-r-04-challenge cuando M3 no está pasado):
        bloqueado si challenge anterior no aprobado.
        """
        page = await self.context.new_page()
        await page.goto(self.curso_url)
        await page.evaluate("() => localStorage.clear()")

        # Try deep link to M4 exercise directly
        await page.goto(f"{self.curso_url}#intro-r-04-001")
        await page.wait_for_timeout(400)

        cur_ex_id = await page.evaluate("() => window.SocialR.navigation.getCurrentExercise().id")
        self.assertNotEqual(cur_ex_id, "intro-r-04-001", "Access to locked M4 exercise must be blocked")

        # Try deep link to M4 challenge directly
        await page.goto(f"{self.curso_url}#intro-r-04-challenge")
        await page.wait_for_timeout(400)

        is_viewing = await page.evaluate("() => window.SocialR.navigation.isViewingChallenge")
        self.assertFalse(is_viewing, "Access to locked M4 challenge must be blocked")

    async def test_principal_10_global_reset_clears_accreditation_and_locks(self):
        """TEST PRINCIPAL 10:
        Reset global: elimina challenge accreditation y vuelve a bloquear progresión.
        """
        page = await self.context.new_page()
        prog_json = make_progress_json(challenges=[
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores"
        ])
        await page.goto(self.curso_url)
        await page.evaluate(f"() => localStorage.setItem('social-r:progress:intro-r', '{prog_json}')")
        await page.reload()

        # Verify M3 is unlocked
        is_m3_unlocked_before = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('03-hacer-preguntas-a-los-datos')"
        )
        self.assertTrue(is_m3_unlocked_before)

        # Trigger resetProgress
        await page.evaluate("() => window.SocialR.resetProgress()")

        # Verify M1 challenge is not passed, M2 and M3 are locked
        state = await page.evaluate("() => window.SocialR.progress.state")
        self.assertEqual(len(state.get("challenges", {})), 0)

        is_m2_unlocked_after = await page.evaluate(
            "() => window.SocialR.courseConfig.isModuleUnlocked('02-trabajar-con-varios-valores')"
        )
        self.assertFalse(is_m2_unlocked_after)


if __name__ == "__main__":
    unittest.main()
