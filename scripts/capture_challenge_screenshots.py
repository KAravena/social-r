import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import shutil

ARTIFACT_DIR = Path(r"C:\Users\katin\.gemini\antigravity-ide\brain\c17fe665-3e0f-4cc5-a3c1-11fab00781dd")
SCRATCH_DIR = ARTIFACT_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://localhost:4200"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("1. Testing M4 Challenge - Pending state...")
        # State: 5 of 6 completed in M4
        pending_state = """
        (() => {
            const state = {
                version: 2,
                activeModuleId: "04-entender-una-base-de-datos",
                currentExerciseId: "intro-r-04-006",
                modules: {
                    "04-entender-una-base-de-datos": {
                        id: "04-entender-una-base-de-datos",
                        currentExerciseId: "intro-r-04-006",
                        completedExercises: [
                            "intro-r-04-001", "intro-r-04-002", "intro-r-04-003",
                            "intro-r-04-004", "intro-r-04-005"
                        ],
                        completed: false
                    }
                },
                challenges: {
                    "04-entender-una-base-de-datos": {
                        status: "pending",
                        passedAt: null
                    }
                }
            };
            localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
        })()
        """
        await page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await page.evaluate(pending_state)
        await page.reload(wait_until="networkidle")

        # Open M4 accordion
        m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
        await m4_header.scroll_into_view_if_needed()
        is_expanded = await m4_header.get_attribute("aria-expanded")
        if is_expanded != "true":
            await m4_header.click()
            await page.wait_for_timeout(300)

        # Capture M4 card in pending state
        m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
        m4_card = m4_item.locator('.sr-challenge-card')
        await m4_card.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)

        pending_path = SCRATCH_DIR / "m04_challenge_pending.png"
        await m4_item.screenshot(path=str(pending_path))
        shutil.copy(pending_path, ARTIFACT_DIR / "m04_challenge_pending.png")
        print("  -> Saved m04_challenge_pending.png")

        print("2. Testing M4 Challenge - Available state...")
        # State: 6 of 6 completed in M4
        available_state = """
        (() => {
            const state = {
                version: 2,
                activeModuleId: "04-entender-una-base-de-datos",
                currentExerciseId: "intro-r-04-006",
                modules: {
                    "04-entender-una-base-de-datos": {
                        id: "04-entender-una-base-de-datos",
                        currentExerciseId: "intro-r-04-006",
                        completedExercises: [
                            "intro-r-04-001", "intro-r-04-002", "intro-r-04-003",
                            "intro-r-04-004", "intro-r-04-005", "intro-r-04-006"
                        ],
                        completed: true
                    }
                },
                challenges: {
                    "04-entender-una-base-de-datos": {
                        status: "pending",
                        passedAt: null
                    }
                }
            };
            localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
        })()
        """
        await page.evaluate(available_state)
        await page.reload(wait_until="networkidle")

        m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
        await m4_header.scroll_into_view_if_needed()
        is_expanded = await m4_header.get_attribute("aria-expanded")
        if is_expanded != "true":
            await m4_header.click()
            await page.wait_for_timeout(300)

        m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
        await m4_item.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)

        available_path = SCRATCH_DIR / "m04_challenge_available.png"
        await m4_item.screenshot(path=str(available_path))
        shutil.copy(available_path, ARTIFACT_DIR / "m04_challenge_available.png")
        print("  -> Saved m04_challenge_available.png")

        print("3. Testing M4 Challenge - Accredited state...")
        # State: Challenge passed
        passed_state = """
        (() => {
            const state = {
                version: 2,
                activeModuleId: "04-entender-una-base-de-datos",
                currentExerciseId: "intro-r-04-006",
                modules: {
                    "04-entender-una-base-de-datos": {
                        id: "04-entender-una-base-de-datos",
                        currentExerciseId: "intro-r-04-006",
                        completedExercises: [
                            "intro-r-04-001", "intro-r-04-002", "intro-r-04-003",
                            "intro-r-04-004", "intro-r-04-005", "intro-r-04-006"
                        ],
                        completed: true,
                        accredited: true
                    }
                },
                challenges: {
                    "04-entender-una-base-de-datos": {
                        status: "passed",
                        passedAt: new Date().toISOString()
                    }
                }
            };
            localStorage.setItem("social-r:progress:intro-r", JSON.stringify(state));
        })()
        """
        await page.evaluate(passed_state)
        await page.reload(wait_until="networkidle")

        m4_header = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
        await m4_header.scroll_into_view_if_needed()
        is_expanded = await m4_header.get_attribute("aria-expanded")
        if is_expanded != "true":
            await m4_header.click()
            await page.wait_for_timeout(300)

        m4_item = page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
        await m4_item.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)

        accredited_path = SCRATCH_DIR / "m04_challenge_accredited.png"
        await m4_item.screenshot(path=str(accredited_path))
        shutil.copy(accredited_path, ARTIFACT_DIR / "m04_challenge_accredited.png")
        print("  -> Saved m04_challenge_accredited.png")

        print("4. Testing M6 Challenge - Standby state...")
        # M6 is standby/en preparación
        m6_header = page.locator('.sr-accordion-item[data-module-id="06-trabajar-cuando-faltan-datos"] .sr-accordion-header')
        await m6_header.scroll_into_view_if_needed()
        is_expanded = await m6_header.get_attribute("aria-expanded")
        if is_expanded != "true":
            await m6_header.click()
            await page.wait_for_timeout(300)

        m6_item = page.locator('.sr-accordion-item[data-module-id="06-trabajar-cuando-faltan-datos"]')
        await m6_item.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)

        m6_path = SCRATCH_DIR / "m06_challenge_standby.png"
        await m6_item.screenshot(path=str(m6_path))
        shutil.copy(m6_path, ARTIFACT_DIR / "m06_challenge_standby.png")
        print("  -> Saved m06_challenge_standby.png")

        print("5. Testing Mobile Viewport (390x844)...")
        mobile_context = await browser.new_context(viewport={"width": 390, "height": 844})
        mobile_page = await mobile_context.new_page()
        await mobile_page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        await mobile_page.evaluate(available_state)
        await mobile_page.reload(wait_until="networkidle")

        m4_mobile_header = mobile_page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"] .sr-accordion-header')
        await m4_mobile_header.scroll_into_view_if_needed()
        is_expanded = await m4_mobile_header.get_attribute("aria-expanded")
        if is_expanded != "true":
            await m4_mobile_header.click()
            await mobile_page.wait_for_timeout(300)

        m4_mobile_item = mobile_page.locator('.sr-accordion-item[data-module-id="04-entender-una-base-de-datos"]')
        await m4_mobile_item.scroll_into_view_if_needed()
        await mobile_page.wait_for_timeout(200)

        mobile_path = SCRATCH_DIR / "m04_challenge_mobile.png"
        await m4_mobile_item.screenshot(path=str(mobile_path))
        shutil.copy(mobile_path, ARTIFACT_DIR / "m04_challenge_mobile.png")
        print("  -> Saved m04_challenge_mobile.png")

        print("6. Testing Curso Challenge View (Deep link & stepper)...")
        # Navigate to curso.html#intro-r-04-challenge with M4 available
        curso_context = await browser.new_context(viewport={"width": 1440, "height": 900})
        curso_page = await curso_context.new_page()
        await curso_page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
        # Unlock M4
        await curso_page.evaluate(available_state)
        # Deep link to M4 challenge
        await curso_page.goto(f"{BASE_URL}/curso.html#intro-r-04-challenge", wait_until="networkidle")
        await curso_page.wait_for_timeout(1000)

        curso_path = SCRATCH_DIR / "curso_challenge_view.png"
        await curso_page.screenshot(path=str(curso_path))
        shutil.copy(curso_path, ARTIFACT_DIR / "curso_challenge_view.png")
        print("  -> Saved curso_challenge_view.png")

        await browser.close()
        print("All challenge screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(main())
