import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import shutil
import http.server
import threading

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def log_message(self, format, *args):
        pass

ARTIFACT_DIR = Path(r"C:\Users\katin\.gemini\antigravity-ide\brain\c17fe665-3e0f-4cc5-a3c1-11fab00781dd")
SCRATCH_DIR = ARTIFACT_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), DocsHTTPHandler)
    port = httpd.server_address[1]
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://127.0.0.1:{port}"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1440, "height": 900})
            page = await context.new_page()

            # 1. State: M4 available from 0/6 exercises (New Philosophy)
            print("1. Testing M4 Challenge - Available from 0/6 exercises...")
            available_state = """
            (() => {
                const state = {
                    version: 2,
                    activeModuleId: "04-entender-una-base-de-datos",
                    currentExerciseId: "intro-r-04-001",
                    modules: {
                        "01-empezar-a-pensar-con-r": { id: "01-empezar-a-pensar-con-r", completedExercises: [], completed: false, accredited: true },
                        "02-trabajar-con-varios-valores": { id: "02-trabajar-con-varios-valores", completedExercises: [], completed: false, accredited: true },
                        "03-hacer-preguntas-a-los-datos": { id: "03-hacer-preguntas-a-los-datos", completedExercises: [], completed: false, accredited: true },
                        "04-entender-una-base-de-datos": {
                            id: "04-entender-una-base-de-datos",
                            currentExerciseId: "intro-r-04-001",
                            completedExercises: [],
                            completed: false,
                            accredited: false
                        }
                    },
                    challenges: {
                        "01-empezar-a-pensar-con-r": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "02-trabajar-con-varios-valores": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "03-hacer-preguntas-a-los-datos": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "04-entender-una-base-de-datos": { status: "available", passedAt: null }
                    }
                };
                localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
            })()
            """
            await page.goto(f"{base_url}/index.html", wait_until="networkidle")
            await page.evaluate(available_state)
            await page.reload(wait_until="networkidle")

            # Open M4 accordion
            m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
            await m4_header.scroll_into_view_if_needed()
            is_expanded = await m4_header.get_attribute("aria-expanded")
            if is_expanded != "true":
                await m4_header.click()
                await page.wait_for_timeout(300)

            m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
            await m4_item.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)

            available_path = SCRATCH_DIR / "m04_challenge_available.png"
            await m4_item.screenshot(path=str(available_path))
            shutil.copy(available_path, ARTIFACT_DIR / "m04_challenge_available.png")
            print("  -> Saved m04_challenge_available.png")

            # 2. State: 6 of 6 completed in M4, but challenge still pending (Práctica completada)
            print("2. Testing M4 Challenge - Practice completed (6/6 exercises, challenge pending)...")
            pending_state = """
            (() => {
                const state = {
                    version: 2,
                    activeModuleId: "04-entender-una-base-de-datos",
                    currentExerciseId: "intro-r-04-006",
                    modules: {
                        "01-empezar-a-pensar-con-r": { id: "01-empezar-a-pensar-con-r", completedExercises: [], completed: false, accredited: true },
                        "02-trabajar-con-varios-valores": { id: "02-trabajar-con-varios-valores", completedExercises: [], completed: false, accredited: true },
                        "03-hacer-preguntas-a-los-datos": { id: "03-hacer-preguntas-a-los-datos", completedExercises: [], completed: false, accredited: true },
                        "04-entender-una-base-de-datos": {
                            id: "04-entender-una-base-de-datos",
                            currentExerciseId: "intro-r-04-006",
                            completedExercises: [
                                "intro-r-04-001", "intro-r-04-002", "intro-r-04-003",
                                "intro-r-04-004", "intro-r-04-005", "intro-r-04-006"
                            ],
                            completed: true,
                            accredited: false
                        }
                    },
                    challenges: {
                        "01-empezar-a-pensar-con-r": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "02-trabajar-con-varios-valores": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "03-hacer-preguntas-a-los-datos": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "04-entender-una-base-de-datos": { status: "available", passedAt: null }
                    }
                };
                localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
            })()
            """
            await page.evaluate(pending_state)
            await page.reload(wait_until="networkidle")

            m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
            await m4_header.scroll_into_view_if_needed()
            is_expanded = await m4_header.get_attribute("aria-expanded")
            if is_expanded != "true":
                await m4_header.click()
                await page.wait_for_timeout(300)

            m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
            await m4_item.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)

            pending_path = SCRATCH_DIR / "m04_challenge_pending.png"
            await m4_item.screenshot(path=str(pending_path))
            shutil.copy(pending_path, ARTIFACT_DIR / "m04_challenge_pending.png")
            print("  -> Saved m04_challenge_pending.png")

            # 3. State: M4 Challenge Passed with 0/6 exercises (Accredited without practice)
            print("3. Testing M4 Challenge - Accredited state (0/6 exercises)...")
            accredited_state = """
            (() => {
                const state = {
                    version: 2,
                    activeModuleId: "04-entender-una-base-de-datos",
                    currentExerciseId: "intro-r-04-001",
                    modules: {
                        "01-empezar-a-pensar-con-r": { id: "01-empezar-a-pensar-con-r", completedExercises: [], completed: false, accredited: true },
                        "02-trabajar-con-varios-valores": { id: "02-trabajar-con-varios-valores", completedExercises: [], completed: false, accredited: true },
                        "03-hacer-preguntas-a-los-datos": { id: "03-hacer-preguntas-a-los-datos", completedExercises: [], completed: false, accredited: true },
                        "04-entender-una-base-de-datos": {
                            id: "04-entender-una-base-de-datos",
                            currentExerciseId: "intro-r-04-001",
                            completedExercises: [],
                            completed: false,
                            accredited: true
                        }
                    },
                    challenges: {
                        "01-empezar-a-pensar-con-r": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "02-trabajar-con-varios-valores": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "03-hacer-preguntas-a-los-datos": { status: "passed", passedAt: "2026-09-26T12:00:00.000Z" },
                        "04-entender-una-base-de-datos": {
                            status: "passed",
                            passedAt: "2026-09-26T12:00:00.000Z"
                        }
                    }
                };
                localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
            })()
            """
            await page.evaluate(accredited_state)
            await page.reload(wait_until="networkidle")

            m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
            await m4_header.scroll_into_view_if_needed()
            is_expanded = await m4_header.get_attribute("aria-expanded")
            if is_expanded != "true":
                await m4_header.click()
                await page.wait_for_timeout(300)

            m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
            await m4_item.scroll_into_view_if_needed()
            await page.wait_for_timeout(300)

            accredited_path = SCRATCH_DIR / "m04_challenge_accredited.png"
            await m4_item.screenshot(path=str(accredited_path))
            shutil.copy(accredited_path, ARTIFACT_DIR / "m04_challenge_accredited.png")
            print("  -> Saved m04_challenge_accredited.png")

            # 4. State: Module 6 Standby
            print("4. Testing M6 Standby state...")
            m6_item = page.locator('.sr-accordion-item[data-module-order="6"]')
            await m6_item.scroll_into_view_if_needed()
            m6_header = m6_item.locator('.sr-accordion-header')
            is_expanded = await m6_header.get_attribute("aria-expanded")
            if is_expanded != "true":
                await m6_header.click()
                await page.wait_for_timeout(300)

            await page.wait_for_timeout(300)
            standby_path = SCRATCH_DIR / "m06_challenge_standby.png"
            await m6_item.screenshot(path=str(standby_path))
            shutil.copy(standby_path, ARTIFACT_DIR / "m06_challenge_standby.png")
            print("  -> Saved m06_challenge_standby.png")

            # 5. Mobile view (390px)
            print("5. Testing mobile view...")
            await context.close()
            mobile_context = await browser.new_context(viewport={"width": 390, "height": 844})
            mobile_page = await mobile_context.new_page()
            await mobile_page.goto(f"{base_url}/index.html", wait_until="networkidle")
            await mobile_page.evaluate(available_state)
            await mobile_page.reload(wait_until="networkidle")

            m4_header = mobile_page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
            await m4_header.scroll_into_view_if_needed()
            is_expanded = await m4_header.get_attribute("aria-expanded")
            if is_expanded != "true":
                await m4_header.click()
                await mobile_page.wait_for_timeout(300)

            m4_card = mobile_page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-challenge-card')
            await m4_card.scroll_into_view_if_needed()
            await mobile_page.wait_for_timeout(300)

            mobile_path = SCRATCH_DIR / "m04_challenge_mobile.png"
            await m4_card.screenshot(path=str(mobile_path))
            shutil.copy(mobile_path, ARTIFACT_DIR / "m04_challenge_mobile.png")
            print("  -> Saved m04_challenge_mobile.png")
            await mobile_context.close()

            # 6. Curso Challenge View (Interactive)
            print("6. Testing Curso Challenge View...")
            desktop_context = await browser.new_context(viewport={"width": 1440, "height": 900})
            curso_page = await desktop_context.new_page()
            await curso_page.goto(f"{base_url}/index.html", wait_until="networkidle")
            await curso_page.evaluate(available_state)
            await curso_page.evaluate("""() => {
                localStorage.setItem("social-r:onboarding", JSON.stringify({ completed: true, version: 1 }));
            }""")
            await curso_page.goto(f"{base_url}/curso.html#intro-r-04-challenge", wait_until="networkidle")
            await curso_page.wait_for_timeout(2000)

            curso_path = SCRATCH_DIR / "curso_challenge_view.png"
            await curso_page.screenshot(path=str(curso_path))
            shutil.copy(curso_path, ARTIFACT_DIR / "curso_challenge_view.png")
            print("  -> Saved curso_challenge_view.png")
            await desktop_context.close()

            await browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

if __name__ == "__main__":
    asyncio.run(main())
