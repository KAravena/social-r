import asyncio
from playwright.async_api import async_playwright

async def debug_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"[BROWSER {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))

        await page.goto("http://localhost:4200/curso.html", wait_until="networkidle")
        await page.wait_for_selector("#sr-webr-status.is-ready", timeout=60000)

        # Navigate to M8-E1
        await page.evaluate("""() => {
            const nav = window.SocialR.navigation;
            const exIdx = nav.exercises.findIndex(e => e.id === "intro-r-08-001");
            nav.setActiveIndex(exIdx);
        }""")

        await page.evaluate("""() => {
            window.SocialR.adapter.setCode("intro-r-08-001", "hist(encuesta_social_demo$horas_estudio)");
        }""")

        res = await page.evaluate("""async () => {
            console.log("Checking adapter...");
            console.log("Graphics manager:", window.SocialR.graphics);
            try {
                await window.SocialR.adapter.runCode("intro-r-08-001");
                console.log("runCode finished!");
            } catch (e) {
                console.error("runCode error:", e);
            }
            
            const ex = document.querySelector('.social-r-exercise[data-exercise-id="intro-r-08-001"]');
            const tabPlot = ex ? ex.querySelector('.sr-output-tab-plot') : null;
            const tabConsole = ex ? ex.querySelector('[data-tab="console"]') : null;
            const stage = ex ? ex.querySelector('.sr-plot-stage') : null;
            const transcript = ex ? ex.querySelector('.sr-console-transcript') : null;
            
            return {
                tabPlotClass: tabPlot ? tabPlot.className : null,
                tabConsoleClass: tabConsole ? tabConsole.className : null,
                stageHTML: stage ? stage.innerHTML : null,
                transcriptHTML: transcript ? transcript.innerHTML : null,
                plotsInManager: window.SocialR.graphics ? Array.from(window.SocialR.graphics.plotsByExercise.keys()) : null
            };
        }""")
        print("Debug result:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_test())
