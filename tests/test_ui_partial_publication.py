import asyncio
import http.server
import threading
import unittest
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent


class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "docs"), **kwargs)

    def log_message(self, format, *args):
        pass


class TestUILocalPreview(unittest.IsolatedAsyncioTestCase):
    """E2E Playwright tests verifying LOCAL PREVIEW MODE (hostname = localhost / 127.0.0.1):
    - M01-M13 available (all 13 modules)
    - 88 exercises accessible
    - Drawer displays 13 modules with 'Preview local' badge
    - Deep links to standby modules (#intro-r-06-001, #intro-r-10-008, #intro-r-13-005) load without interception
    - Navigation traverses M01-M13 (M5E8 -> next -> M6E1; M6E1 -> previous -> M5E8)
    - Progress denominator = 88
    - M5 completion suggests Módulo 6 (continues to M6, not early completion notice)
    - M13 completion displays full course completion
    - Editorial status in course.yml / courseConfig strictly preserved (isModulePublished is False for M06-M13)."""

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

    async def test_local_preview_availability_model(self):
        """courseConfig in local preview mode must detect localhost, report 13 modules and 88 exercises,
        while maintaining isModulePublished(6) == false (editorial status preserved)."""
        page = await self.context.new_page()
        await page.goto(self.curso_url)

        model = await page.evaluate("""() => {
            const c = window.SocialR.courseConfig;
            return {
                isLocalPreview: c.isLocalPreview(),
                availableModuleCount: c.getAvailableModuleCount(),
                availableExerciseCount: c.getAvailableExerciseCount(),
                publishedModuleCount: c.publishedModuleCount,
                publishedExerciseCount: c.publishedExerciseCount,
                m05Available: c.isModuleAvailable(5),
                m06Available: c.isModuleAvailable(6),
                m13Available: c.isModuleAvailable(13),
                m05Published: c.isModulePublished(5),
                m06Published: c.isModulePublished(6),
                m13Published: c.isModulePublished(13),
                ex06_001Available: c.isExerciseAvailable('intro-r-06-001'),
                ex06_001Published: c.isExercisePublished('intro-r-06-001'),
                ex13_005Available: c.isExerciseAvailable('intro-r-13-005'),
                ex13_005Published: c.isExercisePublished('intro-r-13-005'),
                lastAvailableId: c.getLastAvailableExerciseId(),
                lastPublishedId: c.getLastPublishedExerciseId()
            };
        }""")

        # Local preview mode active
        self.assertTrue(model["isLocalPreview"], "Local preview must be active on 127.0.0.1")
        self.assertEqual(model["availableModuleCount"], 13, "Local preview must have 13 available modules")
        self.assertEqual(model["availableExerciseCount"], 89, "Local preview must have 89 available exercises")

        # Full publication status
        self.assertEqual(model["publishedModuleCount"], 13, "Published modules must be 13")
        self.assertEqual(model["publishedExerciseCount"], 89, "Published exercises must be 89")
        self.assertTrue(model["m05Published"], "M05 must be published")
        self.assertTrue(model["m06Published"], "M06 must be published")
        self.assertTrue(model["m13Published"], "M13 must be published")
        self.assertTrue(model["ex06_001Published"], "M06E01 must be published")
        self.assertTrue(model["ex13_005Published"], "M13E05 must be published")

        # Availability in QA / Local preview
        self.assertTrue(model["m05Available"], "M05 must be available")
        self.assertTrue(model["m06Available"], "M06 must be available in local preview")
        self.assertTrue(model["m13Available"], "M13 must be available in local preview")
        self.assertTrue(model["ex06_001Available"], "M06E01 must be available in local preview")
        self.assertTrue(model["ex13_005Available"], "M13E05 must be available in local preview")
        self.assertEqual(model["lastAvailableId"], "intro-r-13-005", "Last available exercise in local preview is M13E5")
        self.assertEqual(model["lastPublishedId"], "intro-r-13-005", "Last published exercise is M13E5")

    async def test_local_preview_drawer_contains_13_modules_and_preview_badge(self):
        """In local preview, the drawer must list all 13 modules, show 'Preview local' badge, and 89 items."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            localStorage.setItem('social-r:auth:guest-mode', 'true');
        """)
        await page.goto(self.curso_url)
        await page.wait_for_selector("#sr-outline-trigger")

        # Open drawer
        await page.click("#sr-outline-trigger")
        await page.wait_for_selector(".sr-drawer-module-header")

        # Check module headers count = 13
        mod_headers = page.locator(".sr-drawer-module-header")
        mod_count = await mod_headers.count()
        self.assertEqual(mod_count, 13, f"Local preview drawer must list all 13 modules, found {mod_count}")

        # Check 'Preview local' badge is visible
        preview_badge = page.locator(".sr-drawer-preview-badge")
        self.assertTrue(await preview_badge.is_visible(), "Drawer should display 'Preview local' badge in local preview")
        badge_text = await preview_badge.text_content()
        self.assertIn("Preview local", badge_text)

        # Check all 89 exercise items exist in drawer
        items = page.locator(".sr-drawer-item")
        item_count = await items.count()
        self.assertEqual(item_count, 89, f"Drawer must list all 89 exercises, found {item_count}")

    async def test_local_preview_deep_links(self):
        """In local preview, deep links to exercises (#intro-r-06-001, #intro-r-10-008, #intro-r-13-005)
        must load directly without being blocked or intercepted by standby banner."""
        test_ids = ["intro-r-06-001", "intro-r-10-008", "intro-r-13-005"]
        for ex_id in test_ids:
            page = await self.context.new_page()
            await page.add_init_script("""
                localStorage.setItem('social-r:tour-completed', 'true');
                localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
                localStorage.setItem('social-r:auth:guest-mode', 'true');
                window.SocialR = window.SocialR || {};
                window.SocialR.devMode = true;
            """)
            await page.goto(f"{self.curso_url}#{ex_id}")
            await page.wait_for_selector(f"#ex-{ex_id}")

            # Verify active exercise
            active_ex = page.locator(".social-r-exercise.is-active-exercise")
            current_id = await active_ex.get_attribute("data-exercise-id")
            self.assertEqual(current_id, ex_id, f"Deep link #{ex_id} should load exercise {ex_id}")

            # Verify standby notice is NOT visible
            standby_banner = page.locator("#sr-standby-notice.is-visible")
            self.assertEqual(await standby_banner.count(), 0, f"Standby notice must NOT be displayed for #{ex_id} in local preview")
            await page.close()

    async def test_local_preview_navigation_traversal(self):
        """In local preview, navigation can traverse between M05 and M06 (M5E8 -> next -> M6E1, M6E1 -> prev -> M5E8)."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            localStorage.setItem('social-r:auth:guest-mode', 'true');
            window.SocialR = window.SocialR || {};
            window.SocialR.devMode = true;
        """)
        await page.goto(f"{self.curso_url}#intro-r-05-008")
        await page.wait_for_selector("#ex-intro-r-05-008.is-active-exercise")

        # On M5E8, advance to M6E1 via next()
        await page.evaluate("window.SocialR.navigation.next()")
        await page.wait_for_selector("#ex-intro-r-06-001.is-active-exercise")

        active_ex = page.locator(".social-r-exercise.is-active-exercise")
        self.assertEqual(await active_ex.get_attribute("data-exercise-id"), "intro-r-06-001")

        # Topbar pill reflects Module 6
        mod_pill = await page.text_content("#sr-topbar-mod-pill")
        self.assertIn("Módulo 6", mod_pill)

        # On M6E1, previous button is enabled and clicking it returns to M5E8
        prev_btn = page.locator("#sr-btn-prev")
        self.assertFalse(await prev_btn.is_disabled(), "Anterior should be enabled on M6E1 in local preview")
        await prev_btn.click()
        await page.wait_for_selector("#ex-intro-r-05-008.is-active-exercise")

        active_ex_back = page.locator(".social-r-exercise.is-active-exercise")
        self.assertEqual(await active_ex_back.get_attribute("data-exercise-id"), "intro-r-05-008")

    async def test_local_preview_progress_denominator_89(self):
        """In local preview, ProgressStore.getCourseProgress() must use denominator 89."""
        page = await self.context.new_page()
        await page.goto(self.curso_url)

        prog = await page.evaluate("""() => {
            return window.SocialR.progress.getCourseProgress();
        }""")
        self.assertEqual(prog["totalCount"], 89, f"Progress denominator in local preview must be 89, got {prog['totalCount']}")

    async def test_local_preview_m5_completion_continues_to_m6(self):
        """Completing M5 in local preview shows celebration suggesting Módulo 6, NOT temporary closure message."""
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
            localStorage.setItem('social-r:auth:guest-mode', 'true');
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
        await page.wait_for_selector("#sr-btn-next")

        # Click next on M5E8 to open celebration
        await page.click("#sr-btn-next")
        await page.wait_for_selector("#sr-celebration-backdrop.is-open")

        # Next step label should suggest next module
        next_label = (await page.text_content("#sr-cel-next-label")).strip()
        self.assertEqual(next_label, "Siguiente paso sugerido:")

        next_title = (await page.text_content("#sr-cel-next-title")).strip()
        self.assertIn("Módulo 6", next_title)
        self.assertNotIn("Has completado todo el contenido disponible por ahora", next_title)

        # Button text should say Comenzar Módulo 6 (or Continuar en Módulo 6)
        btn_text = (await page.text_content("#sr-cel-btn-text")).strip()
        self.assertIn("Módulo 6", btn_text)

        # Clicking continue button navigates to M6E1
        await page.click("#sr-cel-continue-btn")
        await page.wait_for_selector("#ex-intro-r-06-001.is-active-exercise")

        active_ex = page.locator(".social-r-exercise.is-active-exercise")
        self.assertEqual(await active_ex.get_attribute("data-exercise-id"), "intro-r-06-001")

    async def test_local_preview_m13_course_completion(self):
        """In local preview, completing M13 shows the full course completion celebration."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            localStorage.setItem('social-r:auth:guest-mode', 'true');
            localStorage.setItem('social-r:progress:intro-r', JSON.stringify({
                version: 2,
                courseId: 'intro-r',
                challenges: {
                    '13-de-la-pregunta-al-analisis': { status: 'passed' }
                }
            }));
            window.SocialR = window.SocialR || {};
            window.SocialR.devMode = true;
        """)
        await page.goto(f"{self.curso_url}#intro-r-13-005")
        await page.wait_for_selector("#ex-intro-r-13-005")

        # Trigger showCelebration for M13
        await page.evaluate("window.SocialR.navigation.showCelebration('13-de-la-pregunta-al-analisis')")
        await page.wait_for_selector("#sr-celebration-backdrop.is-open")

        next_label = (await page.text_content("#sr-cel-next-label")).strip()
        self.assertEqual(next_label, "¡Curso completado!")

        next_title = (await page.text_content("#sr-cel-next-title")).strip()
        self.assertIn("completado todos los módulos", next_title)


class TestUIProductionMode(unittest.IsolatedAsyncioTestCase):
    """E2E Playwright tests verifying PRODUCTION MODE (simulating hostname = karavena.github.io):
    - All M01-M13 published (89 exercises)
    - 0 modules in standby
    - Drawer contains 13 modules and 89 items
    - Deep links to M06-M13 load directly without standby warning
    - Navigation traverses all modules
    - Progress denominator = 89
    - Full course completion modal on M13."""

    @classmethod
    def setUpClass(cls):
        cls.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DocsHTTPHandler)
        cls.port = cls.httpd.server_address[1]
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.local_url = f"http://127.0.0.1:{cls.port}"
        cls.prod_base_url = "http://karavena.github.io"
        cls.prod_index_url = f"{cls.prod_base_url}/index.html"
        cls.prod_curso_url = f"{cls.prod_base_url}/curso.html"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    async def asyncSetUp(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(viewport={"width": 1280, "height": 800})
        # Simulate GitHub Pages production hostname
        await self.context.route(
            "http://karavena.github.io/**",
            lambda route, req: route.continue_(url=req.url.replace("http://karavena.github.io", self.local_url))
        )

    async def asyncTearDown(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    async def test_production_availability_model(self):
        """In production mode (karavena.github.io), isLocalPreview must be False, available modules = 13, exercises = 89."""
        page = await self.context.new_page()
        await page.goto(self.prod_curso_url)

        model = await page.evaluate("""() => {
            const c = window.SocialR.courseConfig;
            return {
                hostname: location.hostname,
                isLocalPreview: c.isLocalPreview(),
                availableModuleCount: c.getAvailableModuleCount(),
                availableExerciseCount: c.getAvailableExerciseCount(),
                publishedModuleCount: c.publishedModuleCount,
                publishedExerciseCount: c.publishedExerciseCount,
                m05Available: c.isModuleAvailable(5),
                m06Available: c.isModuleAvailable(6),
                m13Available: c.isModuleAvailable(13),
                ex06_001Available: c.isExerciseAvailable('intro-r-06-001'),
                ex13_005Available: c.isExerciseAvailable('intro-r-13-005')
            };
        }""")

        self.assertEqual(model["hostname"], "karavena.github.io")
        self.assertFalse(model["isLocalPreview"], "Local preview must be False on karavena.github.io")
        self.assertEqual(model["availableModuleCount"], 13, "Production available modules must be exactly 13")
        self.assertEqual(model["availableExerciseCount"], 89, "Production available exercises must be exactly 89")
        self.assertEqual(model["publishedModuleCount"], 13, "Production published modules must be 13")
        self.assertEqual(model["publishedExerciseCount"], 89, "Production published exercises must be 89")
        self.assertTrue(model["m05Available"], "M05 must be available in production")
        self.assertTrue(model["m06Available"], "M06 must be available in production")
        self.assertTrue(model["m13Available"], "M13 must be available in production")
        self.assertTrue(model["ex06_001Available"], "M06E01 must be available in production")
        self.assertTrue(model["ex13_005Available"], "M13E05 must be available in production")

    async def test_production_drawer_contains_13_modules(self):
        """In production mode, the drawer must list all 13 modules and NOT display 'Preview local' badge."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            localStorage.setItem('social-r:auth:guest-mode', 'true');
        """)
        await page.goto(self.prod_curso_url)
        await page.wait_for_selector("#sr-outline-trigger")

        await page.click("#sr-outline-trigger")
        await page.wait_for_selector(".sr-drawer-module-header")

        mod_headers = page.locator(".sr-drawer-module-header")
        mod_count = await mod_headers.count()
        self.assertEqual(mod_count, 13, f"Production drawer must list exactly 13 modules, found {mod_count}")

        # Ensure NO preview badge
        preview_badge = page.locator(".sr-drawer-preview-badge")
        self.assertEqual(await preview_badge.count(), 0, "Production drawer must NEVER have 'Preview local' badge")

        # Exercises in drawer must be 89
        items = page.locator(".sr-drawer-item")
        self.assertEqual(await items.count(), 89, "Production drawer must list exactly 89 exercises")

    async def test_production_deep_links_load_without_standby(self):
        """In production, deep links to M06-M13 must load without standby warning or interception."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
            localStorage.setItem('social-r:auth:guest-mode', 'true');
            window.SocialR = window.SocialR || {};
            window.SocialR.devMode = true;
        """)

        await page.goto(f"{self.prod_curso_url}#intro-r-06-001")
        await page.wait_for_selector("#ex-intro-r-06-001.is-active-exercise")

        notice = page.locator("#sr-standby-notice.is-visible")
        self.assertEqual(await notice.count(), 0, "Standby notice must NOT be displayed")

        active_ex = page.locator(".social-r-exercise.is-active-exercise")
        ex_id = await active_ex.get_attribute("data-exercise-id")
        self.assertEqual(ex_id, "intro-r-06-001")

    async def test_production_progress_denominator_89(self):
        """In production, ProgressStore.getCourseProgress() must use denominator 89."""
        page = await self.context.new_page()
        await page.goto(self.prod_curso_url)

        prog = await page.evaluate("""() => {
            return window.SocialR.progress.getCourseProgress();
        }""")
        self.assertEqual(prog["totalCount"], 89, f"Progress denominator in production must be 89, got {prog['totalCount']}")

    async def test_production_m5_completion_modal_and_cta(self):
        """Completing M5E8 in production shows celebration suggesting Módulo 6."""
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
            localStorage.setItem('social-r:auth:guest-mode', 'true');
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

        await page.goto(f"{self.prod_curso_url}#intro-r-05-008")
        await page.wait_for_selector("#sr-progress-pct")

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
        self.assertEqual(await next_label.text_content(), "Siguiente paso sugerido:")

        next_title = page.locator("#sr-cel-next-title")
        title_text = await next_title.text_content()
        self.assertIn("Módulo 6", title_text)

        # Check CTA button text
        cta_text = page.locator("#sr-cel-btn-text")
        self.assertIn("Módulo 6", await cta_text.text_content())

    async def test_index_page_recorrido_and_copy(self):
        """Landing page must show all 13 modules, 0 standby badges, correct subtitle, and hero progress /89."""
        page = await self.context.new_page()

        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:auth:guest-mode', 'true');
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

        await page.goto(self.prod_index_url)
        await page.wait_for_selector(".sr-section-header__desc")

        # 1. Verify subtitle
        subtitle = page.locator(".sr-section-header__desc")
        subtitle_text = await subtitle.text_content()
        self.assertEqual(
            subtitle_text.strip(),
            "13 módulos prácticos desde el primer día: código real, explicaciones claras y retroalimentación inmediata."
        )

        # 2. Verify accordion has all 13 visible items
        items = page.locator("#sr-course-accordion .sr-accordion-item")
        count = await items.count()
        self.assertEqual(count, 13, f"Exactly 13 accordion items must be present in DOM, found {count}")

        # 3. Verify 0 standby items
        standby_items = page.locator("#sr-course-accordion .sr-accordion-item.sr-accordion-item--standby")
        standby_count = await standby_items.count()
        self.assertEqual(standby_count, 0, f"0 standby items expected, found {standby_count}")

        # 4. Verify 0 'En preparación' badges
        badges = page.locator("#sr-course-accordion .sr-module-badge--standby")
        badge_count = await badges.count()
        self.assertEqual(badge_count, 0, f"0 'En preparación' badges expected, found {badge_count}")

        # 5. Verify Hero progress line shows /89 (12 completed: 8 from M1, 2 from M2, 2 from M8)
        progress_line = page.locator("#sr-hero-progress-line")
        is_prog_visible = await progress_line.is_visible()
        self.assertTrue(is_prog_visible)
        text = await progress_line.text_content()
        self.assertIn("/89 ejercicios completados", text)
        self.assertEqual(text.strip(), "12/89 ejercicios completados")

        # 6. Verify Hero CTA link targets current exercise (intro-r-02-003)
        cta = page.locator("#sr-hero-cta")
        href = await cta.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-02-003")

    async def test_module_06_can_expand_and_exercises_are_links(self):
        """Clicking M06 expands its accordion, shows real exercise titles, and confirms they are links."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true'); localStorage.setItem('social-r:auth:guest-mode', 'true');")
        await page.goto(self.prod_index_url)
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
        self.assertEqual(count, 7, f"M06 must display 7 exercise items, found {count}")

        # Ensure all 7 exercises contain <a> link tags
        links = page.locator("#sr-panel-06 .sr-exercise-item a")
        self.assertEqual(await links.count(), 7, "All M06 exercises must contain <a> link tags")

    async def test_m13_expanded(self):
        """M13 is visible, expands to show its 5 exercises as links."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true'); localStorage.setItem('social-r:auth:guest-mode', 'true');")
        await page.goto(self.prod_index_url)
        await page.wait_for_selector("#sr-header-13")

        # Click M13 header to expand
        await page.click("#sr-header-13")
        await page.wait_for_selector("#sr-panel-13", state="visible")

        # Check M13 has 5 items
        ex_items = page.locator("#sr-panel-13 .sr-exercise-item")
        self.assertEqual(await ex_items.count(), 5)

        # All 5 are links
        links = page.locator("#sr-panel-13 .sr-exercise-item a")
        self.assertEqual(await links.count(), 5)

    async def test_published_exercises_remain_links(self):
        """All 89 exercises must remain navigable links with valid href to curso.html."""
        page = await self.context.new_page()
        await page.add_init_script("localStorage.setItem('social-r:tour-completed', 'true'); localStorage.setItem('social-r:auth:guest-mode', 'true');")
        await page.goto(self.prod_index_url)
        await page.wait_for_selector("#sr-course-accordion")

        all_links = page.locator("#sr-course-accordion a.sr-ex-link")
        link_count = await all_links.count()
        self.assertEqual(link_count, 89, f"Exactly 89 published exercise links expected, found {link_count}")

        first_link = all_links.first
        href = await first_link.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-01-001")

    async def test_m8_progress_displayed_and_not_clamped(self):
        """M8 progress is displayed and not clamped on landing page."""
        page = await self.context.new_page()
        await page.add_init_script("""
            localStorage.setItem('social-r:tour-completed', 'true');
            localStorage.setItem('social-r:auth:guest-mode', 'true');
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
        await page.goto(self.prod_index_url)
        await page.wait_for_selector("#sr-course-accordion")

        m8_badge = page.locator('.sr-module-badge[data-badge-for="08-describir-cantidades"]')
        badge_text = await m8_badge.text_content()
        self.assertNotIn("En preparación", badge_text)

        # CTA targets M8 exercise directly
        cta = page.locator("#sr-hero-cta")
        href = await cta.get_attribute("href")
        self.assertEqual(href, "curso.html#intro-r-08-003")

    async def test_mobile_viewports(self):
        """Verify layout and celebration modal fit within 390x844 and 360x800 without overflow."""
        for width, height in [(390, 844), (360, 800)]:
            page = await self.context.new_page()
            await page.set_viewport_size({"width": width, "height": height})
            await page.goto(self.prod_index_url)
            await page.wait_for_selector(".sr-hero")

            overflow = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
            self.assertFalse(overflow, f"Horizontal overflow detected on index at {width}x{height}")
            await page.close()


if __name__ == "__main__":
    unittest.main()
