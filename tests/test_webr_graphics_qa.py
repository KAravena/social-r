import asyncio
import os
import shutil
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = ROOT / "tests" / "screenshots" / "graphics"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("C:/Users/katin/.gemini/antigravity-ide/brain/789d2245-0c32-481a-8c13-c3a015b1d2e6")

async def run_graphics_qa():
    print("=== STARTING SOCIAL R WEBR GRAPHICS INTEGRATION QA ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1690, "height": 860})
        page = await context.new_page()

        print("1. Navigating to http://localhost:4200/curso.html ...")
        await page.goto("http://localhost:4200/curso.html", wait_until="networkidle")

        print("2. Waiting for WebR to be ready...")
        await page.wait_for_selector("#sr-webr-status.is-ready", timeout=60000)
        print("✓ WebR runtime is ready!")

        # -------------------------------------------------------------
        # TEST CASE 1: M8-E1 HISTOGRAM TEST (Mira la distribución)
        # -------------------------------------------------------------
        print("\n--- TEST CASE 1: M8-E1 (hist) ---")
        # Navigate to intro-r-08-001
        await page.evaluate("""() => {
            const nav = window.SocialR.navigation;
            const exIdx = nav.exercises.findIndex(e => e.id === "intro-r-08-001");
            nav.setActiveIndex(exIdx);
        }""")
        await page.wait_for_selector('.social-r-exercise[data-exercise-id="intro-r-08-001"].is-active-exercise', timeout=5000)
        
        # Verify initial tab state: only Consola R is visible, Gráfico is hidden
        tab_console = await page.query_selector('.social-r-exercise.is-active-exercise [data-tab="console"]')
        tab_plot = await page.query_selector('.social-r-exercise.is-active-exercise [data-tab="plot"]')
        assert tab_console is not None, "Consola R tab must exist"
        assert tab_plot is not None, "Gráfico tab element must exist"
        
        is_plot_tab_hidden = await tab_plot.evaluate("el => el.classList.contains('d-none')")
        assert is_plot_tab_hidden, "Gráfico tab must be initially hidden when no graphic exists"
        print("✓ Initial state verified: Gráfico tab is hidden before execution.")

        # Set code: hist(encuesta_social_demo$horas_estudio)
        hist_code = "hist(encuesta_social_demo$horas_estudio)"
        await page.evaluate(f"""() => {{
            window.SocialR.adapter.setCode("intro-r-08-001", "{hist_code}");
        }}""")

        # Execute code via adapter.runCode
        print(f"Executing: {hist_code} ...")
        await page.evaluate("""async () => {
            await window.SocialR.adapter.runCode("intro-r-08-001");
        }""")

        # Wait for plot tab to be active and visible
        await page.wait_for_selector('.social-r-exercise.is-active-exercise [data-tab="plot"]:not(.d-none).is-active', timeout=10000)
        await page.wait_for_selector('.social-r-exercise.is-active-exercise .sr-plot-stage img', timeout=10000)
        print("✓ Gráfico tab automatically revealed and activated!")

        # Verify image properties
        plot_img = await page.query_selector('.social-r-exercise.is-active-exercise .sr-plot-stage img')
        assert plot_img is not None, "Plot image must exist in stage"
        img_src = await plot_img.get_attribute("src")
        assert img_src and img_src.startswith("data:image/png;base64,"), "Plot image src must be valid base64 PNG"
        print(f"✓ Histogram image rendered with valid PNG data (length: {len(img_src)} chars)")

        # Verify console output survived: switch to Consola R tab
        print("Switching back to Consola R tab to verify console transcript...")
        await page.click('.social-r-exercise.is-active-exercise [data-tab="console"]')
        await page.wait_for_selector('.social-r-exercise.is-active-exercise .sr-console-transcript:not(.d-none)', timeout=5000)
        transcript_text = await page.evaluate("""() => {
            const transcript = document.querySelector('.social-r-exercise.is-active-exercise .sr-console-transcript');
            return transcript ? transcript.innerText : '';
        }""")
        assert "hist(encuesta_social_demo$horas_estudio)" in transcript_text, "Console must retain execution prompt"
        print("✓ Console transcript retained execution prompt!")

        # Switch back to Gráfico tab
        await page.click('.social-r-exercise.is-active-exercise [data-tab="plot"]')
        await page.wait_for_selector('.social-r-exercise.is-active-exercise .sr-plot-pane:not(.d-none)', timeout=5000)

        # Capture Desktop screenshot for M8-E1
        m8_screenshot_path = SCREENSHOT_DIR / "m08_e1_histogram_1690x860.png"
        await page.screenshot(path=str(m8_screenshot_path), full_page=False)
        print(f"✓ Saved M8-E1 screenshot: {m8_screenshot_path}")

        # Test expand modal on M8-E1
        print("Testing expand modal (⛶ Ampliar)...")
        await page.click('.social-r-exercise.is-active-exercise .sr-btn-expand-plot')
        await page.wait_for_selector('#sr-plot-modal:not(.d-none)', timeout=5000)
        modal_img = await page.query_selector('#sr-plot-modal .sr-plot-modal-stage img')
        assert modal_img is not None, "Expanded modal must contain plot image"
        print("✓ Modal opened with high-res plot.")

        # Close modal via Escape
        await page.keyboard.press("Escape")
        await page.wait_for_selector('#sr-plot-modal.d-none', timeout=5000)
        print("✓ Modal closed successfully via Escape.")

        # -------------------------------------------------------------
        # TEST CASE 2: M9-E2 SCATTERPLOT TEST (Cada persona se vuelve un punto)
        # -------------------------------------------------------------
        print("\n--- TEST CASE 2: M9-E2 (plot / scatterplot) ---")
        # Navigate to intro-r-09-002
        await page.evaluate("""() => {
            const nav = window.SocialR.navigation;
            const exIdx = nav.exercises.findIndex(e => e.id === "intro-r-09-002");
            nav.setActiveIndex(exIdx);
        }""")
        await page.wait_for_selector('.social-r-exercise[data-exercise-id="intro-r-09-002"].is-active-exercise', timeout=5000)

        # Verify that M8's plot DID NOT bleed into M9!
        tab_plot_m9 = await page.query_selector('.social-r-exercise.is-active-exercise [data-tab="plot"]')
        is_plot_tab_hidden_m9 = await tab_plot_m9.evaluate("el => el.classList.contains('d-none')")
        assert is_plot_tab_hidden_m9, "M9-E2 must initially have Gráfico tab hidden (no bleeding from M8)"
        print("✓ Exercise isolation confirmed: M8 histogram did not bleed into M9!")

        # Set code: plot(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)
        scatter_code = "plot(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)"
        await page.evaluate(f"""() => {{
            window.SocialR.adapter.setCode("intro-r-09-002", "{scatter_code}");
        }}""")

        print(f"Executing: {scatter_code} ...")
        await page.evaluate("""async () => {
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }""")

        # Wait for plot tab to be active and visible
        await page.wait_for_selector('.social-r-exercise.is-active-exercise [data-tab="plot"]:not(.d-none).is-active', timeout=10000)
        await page.wait_for_selector('.social-r-exercise.is-active-exercise .sr-plot-stage img', timeout=10000)
        print("✓ Scatterplot generated and Gráfico tab activated for M9-E2!")

        # Capture Desktop screenshot for M9-E2
        m9_screenshot_path = SCREENSHOT_DIR / "m09_e2_scatterplot_1690x860.png"
        await page.screenshot(path=str(m9_screenshot_path), full_page=False)
        print(f"✓ Saved M9-E2 screenshot: {m9_screenshot_path}")

        # -------------------------------------------------------------
        # TEST CASE 3: MULTIPLE PLOTS IN SAME RUN (Pager test)
        # -------------------------------------------------------------
        print("\n--- TEST CASE 3: MULTIPLE PLOTS (Pager test) ---")
        multi_code = "plot(1:10, 1:10); hist(c(1,2,2,3,3,3,4,4,5)); boxplot(c(2,4,6,8,10))"
        await page.evaluate(f"""async () => {{
            window.SocialR.adapter.setCode("intro-r-09-002", "{multi_code}");
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }}""")

        await page.wait_for_selector('.social-r-exercise.is-active-exercise .sr-plot-pager:not(.d-none)', timeout=10000)
        counter_text = await page.evaluate("""() => {
            const el = document.querySelector('.social-r-exercise.is-active-exercise .sr-plot-counter');
            return el ? el.textContent.trim() : '';
        }""")
        print(f"✓ Pager is visible for 3 plots! Counter shows: '{counter_text}'")
        assert counter_text == "3 / 3", f"Expected '3 / 3', got '{counter_text}'"

        # Click previous plot
        await page.click('.social-r-exercise.is-active-exercise .sr-plot-prev')
        counter_text_2 = await page.evaluate("""() => {
            return document.querySelector('.social-r-exercise.is-active-exercise .sr-plot-counter').textContent.trim();
        }""")
        assert counter_text_2 == "2 / 3", f"Expected '2 / 3' after prev click, got '{counter_text_2}'"
        print("✓ Pager navigated back to plot 2 / 3!")

        # -------------------------------------------------------------
        # TEST CASE 4: NON-GRAPHICAL CODE DOES NOT SHOW PLOT TAB
        # -------------------------------------------------------------
        print("\n--- TEST CASE 4: NON-GRAPHICAL CODE (table/summary) ---")
        # Run non-graphical code
        non_graph_code = "table(encuesta_social$carrera)"
        await page.evaluate(f"""async () => {{
            window.SocialR.adapter.setCode("intro-r-09-002", "{non_graph_code}");
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }}""")

        # Gráfico tab must now be hidden and Consola R active
        await page.wait_for_selector('.social-r-exercise.is-active-exercise [data-tab="console"].is-active', timeout=5000)
        is_plot_hidden_after_table = await page.evaluate("""() => {
            return document.querySelector('.social-r-exercise.is-active-exercise [data-tab="plot"]').classList.contains('d-none');
        }""")
        assert is_plot_hidden_after_table, "Non-graphical execution must hide Gráfico tab"
        print("✓ Non-graphical execution correctly kept view on Consola R and hid Gráfico tab!")

        # -------------------------------------------------------------
        # TEST CASE 5: ERROR HANDLING (R error does not generate fake plot)
        # -------------------------------------------------------------
        print("\n--- TEST CASE 5: R ERROR HANDLING ---")
        error_code = "hist(variable_inexistente_xyz_123)"
        await page.evaluate(f"""async () => {{
            window.SocialR.adapter.setCode("intro-r-09-002", "{error_code}");
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }}""")

        # Gráfico tab must remain hidden, console active with error
        await page.wait_for_selector('.social-r-exercise.is-active-exercise [data-tab="console"].is-active', timeout=5000)
        is_plot_hidden_after_error = await page.evaluate("""() => {
            return document.querySelector('.social-r-exercise.is-active-exercise [data-tab="plot"]').classList.contains('d-none');
        }""")
        assert is_plot_hidden_after_error, "R error must not create or show Gráfico tab"
        has_error_in_transcript = await page.evaluate("""() => {
            const transcript = document.querySelector('.social-r-exercise.is-active-exercise .sr-console-transcript');
            return transcript && transcript.querySelector('.sr-console-error') !== null;
        }""")
        assert has_error_in_transcript, "Console transcript must contain error block"
        print("✓ R error cleanly displayed in Consola R without showing fake plot tab!")

        # -------------------------------------------------------------
        # TEST CASE 6: REINICIAR (Reset button clears plot & console)
        # -------------------------------------------------------------
        print("\n--- TEST CASE 6: REINICIAR BUTTON ---")
        # Generate plot again first
        await page.evaluate("""async () => {
            window.SocialR.adapter.setCode("intro-r-09-002", "plot(1:5)");
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }""")
        await page.wait_for_selector('.social-r-exercise.is-active-exercise [data-tab="plot"]:not(.d-none).is-active', timeout=5000)

        # Click Reiniciar
        print("Clicking Reiniciar button...")
        await page.click('.social-r-exercise.is-active-exercise .sr-btn-reset')
        await page.wait_for_timeout(300)

        is_plot_hidden_after_reset = await page.evaluate("""() => {
            return document.querySelector('.social-r-exercise.is-active-exercise [data-tab="plot"]').classList.contains('d-none');
        }""")
        assert is_plot_hidden_after_reset, "Reiniciar must hide Gráfico tab"
        transcript_empty_after_reset = await page.evaluate("""() => {
            const transcript = document.querySelector('.social-r-exercise.is-active-exercise .sr-console-transcript');
            return !transcript || transcript.children.length === 0;
        }""")
        assert transcript_empty_after_reset, "Reiniciar must clear console transcript"
        print("✓ Reiniciar successfully cleared graphic, reset tabs to Consola R, and cleared transcript!")

        # -------------------------------------------------------------
        # TEST CASE 7: RESPONSIVE SCREENSHOT MATRIX
        # -------------------------------------------------------------
        print("\n--- TEST CASE 7: RESPONSIVE SCREENSHOT MATRIX ---")
        # Regenerate M8-E1 histogram
        await page.evaluate("""async () => {
            const nav = window.SocialR.navigation;
            const exIdx = nav.exercises.findIndex(e => e.id === "intro-r-08-001");
            nav.setActiveIndex(exIdx);
            window.SocialR.adapter.setCode("intro-r-08-001", "hist(encuesta_social_demo$horas_estudio)");
            await window.SocialR.adapter.runCode("intro-r-08-001");
        }""")
        await page.wait_for_selector('.social-r-exercise[data-exercise-id="intro-r-08-001"] .sr-plot-stage img', timeout=10000)

        viewports = [
            (1920, 1080),
            (1690, 860),
            (1440, 900),
            (1366, 768),
            (390, 844),
            (360, 800)
        ]

        for w, h in viewports:
            await page.set_viewport_size({"width": w, "height": h})
            await page.wait_for_timeout(300)
            ss_name = f"m08_e1_hist_{w}x{h}.png"
            ss_path = SCREENSHOT_DIR / ss_name
            await page.screenshot(path=str(ss_path), full_page=False)
            print(f"✓ Screenshot captured at {w}x{h}: {ss_path}")

        # Also capture M9 scatterplot at 1440x900 and 1366x768
        await page.evaluate("""async () => {
            const nav = window.SocialR.navigation;
            const exIdx = nav.exercises.findIndex(e => e.id === "intro-r-09-002");
            nav.setActiveIndex(exIdx);
            window.SocialR.adapter.setCode("intro-r-09-002", "plot(encuesta_social$horas_estudio, encuesta_social$puntaje_metodos)");
            await window.SocialR.adapter.runCode("intro-r-09-002");
        }""")
        await page.wait_for_selector('.social-r-exercise[data-exercise-id="intro-r-09-002"] .sr-plot-stage img', timeout=10000)

        for w, h in [(1440, 900), (1366, 768), (390, 844)]:
            await page.set_viewport_size({"width": w, "height": h})
            await page.wait_for_timeout(300)
            ss_name = f"m09_e2_scatter_{w}x{h}.png"
            ss_path = SCREENSHOT_DIR / ss_name
            await page.screenshot(path=str(ss_path), full_page=False)
            print(f"✓ Screenshot captured at {w}x{h}: {ss_path}")

        # Copy primary screenshots to ARTIFACT_DIR for user inspection
        if ARTIFACT_DIR.exists():
            for f in SCREENSHOT_DIR.glob("*.png"):
                dest = ARTIFACT_DIR / f.name
                shutil.copyfile(f, dest)
            print(f"✓ Copied screenshots to artifact directory: {ARTIFACT_DIR}")

        await browser.close()
        print("\n=== ALL WEBR GRAPHICS INTEGRATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    asyncio.run(run_graphics_qa())
