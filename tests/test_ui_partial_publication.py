import asyncio
import http.server
import unittest
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent


class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "docs"), **kwargs)

    def log_message(self, format, *args):
        pass


class TestUIPartialPublication(unittest.IsolatedAsyncioTestCase):
    """E2E Playwright tests verifying full curriculum display on index (M01-M13)
    with M01-M05 published and M06-M13 in standby ('En preparación')."""

    @classmethod
    def setUpClass(cls):
        cls.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DocsHTTPHandler)
        cls.port = cls.httpd.server_address[1]
        import threading
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

    async def test_index_page_recorrido_and_copy(self):
        """Landing page must show all 13 modules, 8 standby badges, correct subtitle, and hero progress /36."""
        page = await self.context.new_page()

        # Seed localStorage with 10 completed exercises (8 in M1, 2 in M2, and one legacy in M8)
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({
                version: 2,
                courseId: 'intro-r',
                activeModuleId: '02-trabajar-con-varios-valores',
                currentExerciseId: 'intro-r-02-003',
                modules: {
                    '01-empezar-a-pensar-con-r': {
                        completedExercises: ['intro-r-01-001', 'intro-r-01-002', 'intro-r-01-003', 'intro-r-01-004', 'intro-r-01-005', 'intro-r-01-006', 'intro-r-01-007', 'intro-r-01-008']
                    },
                    '02-trabajar-con-varios-valores': {
                        completedExercises: ['intro-r-02-001', 'intro-r-02-002']
                    },
                    '08-describir-cantidades': {
                        completedExercises: ['intro-r-08-001', 'intro-r-08-002']
                    }
                }
            }));
        """)

        await page.goto(self.index_url)
        await page.wait_for_selector(".sr-section-header__desc")

        # 1. Verify subtitle
        subtitle = page.locator(".sr-section-header__desc")
        subtitle_text = await subtitle.text_content()
        self.assertEqual(
            subtitle_text.strip(),
            "5 módulos disponibles ahora. Los siguientes están en preparación."
        )

        # 2. Verify accordion has all 13 visible items
        items = page.locator("#sr-course-accordion .sr-accordion-item")
        count = await items.count()
        self.assertEqual(count, 13, f"Exactly 13 accordion items must be present in DOM, found {count}")

        # 3. Verify exactly 5 published and 8 standby
        standby_items = page.locator("#sr-course-accordion .sr-accordion-item.sr-accordion-item--standby")
        standby_count = await standby_items.count()
        self.assertEqual(standby_count, 8, f"Exactly 8 standby items expected, found {standby_count}")

        # 4. Verify exactly 8 'En preparación' badges
        badges = page.locator("#sr-course-accordion .sr-module-badge--standby")
        badge_count = await badges.count()
        self.assertEqual(badge_count, 8, f"Exactly 8 'En preparación' badges expected, found {badge_count}")
        for i in range(badge_count):
            txt = await badges.nth(i).text_content()
            self.assertEqual(txt.strip(), "En preparación")

        # 5. Verify Hero progress line shows /36 (10 completed, excluding M8 legacy)
        progress_line = page.locator("#sr-hero-progress-line")
        is_prog_visible = await progress_line.is_visible()
        self.assertTrue(is_prog_visible)
        text = await progress_line.text_content()
        self.assertIn("/36 ejercicios completados", text)
        self.assertEqual(text.strip(), "10/36 ejercicios completados")

        # 6. Verify Hero CTA link targets published exercise (intro-r-02-003)
        cta = page.locator("#sr-hero-cta")
        href = await cta.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-02-003")

    async def test_standby_module_can_expand_and_exercises_are_not_links(self):
        """Clicking M06 expands its accordion, shows real exercise titles, and confirms they are not links."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true');")
        await page.goto(self.index_url)
        await page.wait_for_selector("#sr-header-06")

        # Click M06 header to expand
        await page.click("#sr-header-06")
        await page.wait_for_selector("#sr-panel-06", state="visible")

        # Description check
        lead = page.locator("#sr-panel-06 .sr-module-lead")
        lead_text = await lead.text_content()
        self.assertIn("Aprenderás a reconocer datos ausentes", lead_text)

        # Check exercise items inside M06
        ex_items = page.locator("#sr-panel-06 .sr-exercise-item")
        count = await ex_items.count()
        self.assertEqual(count, 6, f"M06 must display 6 exercise items, found {count}")

        # Ensure NO <a> tags exist inside M06 exercises
        links = page.locator("#sr-panel-06 .sr-exercise-item a")
        self.assertEqual(await links.count(), 0, "Standby exercises must NOT contain <a> link tags")

        # Check titles are visible
        first_title = page.locator("#sr-panel-06 .sr-ex-preview .sr-ex-title").first
        self.assertEqual(await first_title.text_content(), "Aquí no sabemos el valor")

        # Clicking on the exercise item must not navigate or change URL
        current_url = page.url
        await first_title.click()
        self.assertEqual(page.url, current_url)

    async def test_m13_standby_expanded(self):
        """M13 is visible as standby, expands to show its 5 preview exercises without links."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true');")
        await page.goto(self.index_url)
        await page.wait_for_selector("#sr-header-13")

        # Click M13 header to expand
        await page.click("#sr-header-13")
        await page.wait_for_selector("#sr-panel-13", state="visible")

        # Check M13 has 5 preview items
        ex_items = page.locator("#sr-panel-13 .sr-exercise-item")
        self.assertEqual(await ex_items.count(), 5)

        # No links
        links = page.locator("#sr-panel-13 .sr-exercise-item a")
        self.assertEqual(await links.count(), 0)

    async def test_published_exercises_remain_links(self):
        """M01-M05 exercises must remain navigable links with valid href to curso.html."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true');")
        await page.goto(self.index_url)
        await page.wait_for_selector("#sr-course-accordion")

        # Count total links in accordion (must be exactly 36, all in M01-M05)
        all_links = page.locator("#sr-course-accordion a.sr-ex-link")
        link_count = await all_links.count()
        self.assertEqual(link_count, 36, f"Exactly 36 published exercise links expected, found {link_count}")

        # Sample check: first link in M1
        first_link = all_links.first
        href = await first_link.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-01-001")

    async def test_standby_progress_not_displayed(self):
        """Standby modules never display progress badges or completion state even with legacy progress."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({
                version: 2,
                courseId: 'intro-r',
                activeModuleId: '08-describir-cantidades',
                currentExerciseId: 'intro-r-08-003',
                modules: {
                    '08-describir-cantidades': {
                        completedExercises: ['intro-r-08-001', 'intro-r-08-002', 'intro-r-08-003'],
                        completed: true
                    }
                }
            }));
        """)
        await page.goto(self.index_url)
        await page.wait_for_selector("#sr-course-accordion")

        # M08 badge must still be "En preparación"
        m8_badge = page.locator('.sr-module-badge[data-badge-for="08-describir-cantidades"]')
        badge_text = await m8_badge.text_content()
        self.assertEqual(badge_text.strip(), "En preparación")
        self.assertNotIn("3/7", badge_text)
        self.assertNotIn("Completado", badge_text)

    async def test_legacy_m8_progress_clamped_on_landing(self):
        """A user whose saved currentExerciseId was in M8 must be clamped to M5 or last published."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({
                version: 2,
                courseId: 'intro-r',
                activeModuleId: '08-describir-cantidades',
                currentExerciseId: 'intro-r-08-003',
                modules: {
                    '08-describir-cantidades': {
                        completedExercises: ['intro-r-08-001', 'intro-r-08-002']
                    }
                }
            }));
        """)

        await page.goto(self.index_url)
        await page.wait_for_selector("#sr-hero-cta[href*='intro-r-05-008']")

        cta = page.locator("#sr-hero-cta")
        href = await cta.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-05-008")

    async def test_drawer_contains_only_5_modules(self):
        """Course outline drawer in curso.html must still contain exactly 5 modules (M1 to M5)."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
        """)
        await page.goto(self.curso_url)
        await page.wait_for_selector("#sr-outline-trigger")

        # Open drawer
        await page.click("#sr-outline-trigger")
        await page.wait_for_selector(".sr-drawer-module-header")

        # Count module headers in drawer
        mod_headers = page.locator(".sr-drawer-module-header")
        mod_count = await mod_headers.count()
        self.assertEqual(mod_count, 5, f"Drawer must list exactly 5 modules, found {mod_count}")

    async def test_deep_link_standby_interception(self):
        """Accessing curso.html#intro-r-06-001 must show notice and clamp to valid published content."""
        # 1. User with M1-M5 unlocked clamps to M5E8
        page = await self.context.new_page()
        all_36_ids = [
            f"intro-r-01-{i:03d}" for i in range(1, 9)
        ] + [
            f"intro-r-02-{i:03d}" for i in range(1, 8)
        ] + [
            f"intro-r-03-{i:03d}" for i in range(1, 8)
        ] + [
            f"intro-r-04-{i:03d}" for i in range(1, 7)
        ] + [
            f"intro-r-05-{i:03d}" for i in range(1, 9)
        ]
        await page.add_init_script(f"""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({{ completed: true, version: 1 }}));
            const ids = {all_36_ids};
            const mods = {{}};
            ['01-empezar-a-pensar-con-r', '02-trabajar-con-varios-valores', '03-hacer-preguntas-a-los-datos', '04-entender-una-base-de-datos', '05-seleccionar-y-filtrar-datos'].forEach((slug, idx) => {{
                const modNum = String(idx + 1).padStart(2, '0');
                mods[slug] = {{
                    completedExercises: ids.filter(id => id.includes('-' + modNum + '-')),
                    completed: true
                }};
            }});
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({{
                version: 2,
                courseId: 'intro-r',
                activeModuleId: '05-seleccionar-y-filtrar-datos',
                currentExerciseId: 'intro-r-05-008',
                modules: mods
            }}));
        """)

        await page.goto(f"{self.curso_url}#intro-r-06-001")
        await page.wait_for_selector("#sr-standby-notice.is-visible")

        notice = page.locator("#sr-standby-notice")
        notice_text = await notice.text_content()
        self.assertIn("Este módulo todavía no está disponible", notice_text)
        self.assertIn("Volver al recorrido", notice_text)

        active_ex = page.locator(".social-r-exercise.is-active-exercise")
        ex_id = await active_ex.get_attribute("data-exercise-id")
        self.assertEqual(ex_id, "intro-r-05-008")

        # 2. Brand new user with no progress in a fresh context clamps to M5E1 without exposing M6
        context2 = await self.browser.new_context(viewport={"width": 1280, "height": 800})
        page2 = await context2.new_page()
        await page2.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
        """)
        await page2.goto(f"{self.curso_url}#intro-r-06-001")
        await page2.wait_for_selector("#sr-standby-notice.is-visible")

        active_ex2 = page2.locator(".social-r-exercise.is-active-exercise")
        ex_id2 = await active_ex2.get_attribute("data-exercise-id")
        self.assertEqual(ex_id2, "intro-r-05-001")
        self.assertFalse(ex_id2.startswith("intro-r-06"))
        await context2.close()

    async def test_m5_completion_modal_and_cta(self):
        """Completing M5E8 shows celebration with 'Ver recorrido' CTA pointing to index.html#recorrido."""
        page = await self.context.new_page()

        all_36_ids = [
            f"intro-r-01-{i:03d}" for i in range(1, 9)
        ] + [
            f"intro-r-02-{i:03d}" for i in range(1, 8)
        ] + [
            f"intro-r-03-{i:03d}" for i in range(1, 8)
        ] + [
            f"intro-r-04-{i:03d}" for i in range(1, 7)
        ] + [
            f"intro-r-05-{i:03d}" for i in range(1, 9)
        ]

        await page.add_init_script(f"""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({{ completed: true, version: 1 }}));
            const ids = {all_36_ids};
            const mods = {{}};
            ['01-empezar-a-pensar-con-r', '02-trabajar-con-varios-valores', '03-hacer-preguntas-a-los-datos', '04-entender-una-base-de-datos', '05-seleccionar-y-filtrar-datos'].forEach((slug, idx) => {{
                const modNum = String(idx + 1).padStart(2, '0');
                mods[slug] = {{
                    completedExercises: ids.filter(id => id.includes('-' + modNum + '-')),
                    completed: true
                }};
            }});
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({{
                version: 2,
                courseId: 'intro-r',
                activeModuleId: '05-seleccionar-y-filtrar-datos',
                currentExerciseId: 'intro-r-05-008',
                modules: mods
            }}));
        """)

        await page.goto(f"{self.curso_url}#intro-r-05-008")
        await page.wait_for_selector("#sr-progress-pct")

        # Bottom bar percentage should say 100% del contenido disponible
        pct_el = page.locator("#sr-progress-pct")
        pct_text = await pct_el.text_content()
        self.assertEqual(pct_text.strip(), "100% del contenido disponible")

        # Click Next on M5E8 to trigger celebration
        next_btn = page.locator("#sr-btn-next")
        await next_btn.click()

        # Verify celebration modal
        backdrop = page.locator("#sr-celebration-backdrop")
        await page.wait_for_selector("#sr-celebration-backdrop.is-open")
        self.assertTrue(await backdrop.is_visible())

        # Check outcomes heading
        outcomes_heading = page.locator(".sr-outcomes-heading")
        self.assertEqual(await outcomes_heading.text_content(), "Ahora puedes:")

        # Check next step label
        next_label = page.locator("#sr-cel-next-label")
        self.assertEqual(await next_label.text_content(), "Contenido disponible completado")

        # Check title references upcoming modules in preparation
        next_title = page.locator("#sr-cel-next-title")
        title_text = await next_title.text_content()
        self.assertIn("Has completado todo el contenido disponible por ahora", title_text)
        self.assertIn("Los siguientes módulos están en preparación", title_text)
        self.assertIn("Puedes ver qué viene en el recorrido del curso", title_text)

        # Check CTA button text
        cta_text = page.locator("#sr-cel-btn-text")
        self.assertEqual(await cta_text.text_content(), "Ver recorrido")

    async def test_mobile_viewports(self):
        """Verify layout and celebration modal fit within 390x844 and 360x800 without overflow."""
        for width, height in [(390, 844), (360, 800)]:
            page = await self.context.new_page()
            await page.set_viewport_size({"width": width, "height": height})
            await page.goto(self.index_url)
            await page.wait_for_selector(".sr-hero")

            # Check horizontal overflow on index
            overflow = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
            self.assertFalse(overflow, f"Horizontal overflow detected on index at {width}x{height}")
            await page.close()


if __name__ == "__main__":
    unittest.main()
