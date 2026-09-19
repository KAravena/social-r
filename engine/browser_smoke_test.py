#!/usr/bin/env python3
"""End-to-end browser smoke test for Social R using system Chromium / Edge."""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


async def run_smoke_test(url="http://127.0.0.1:3617/"):
    exe_path = None
    for p in EDGE_PATHS:
        if Path(p).exists():
            exe_path = p
            break

    print(f"[TEST] Using browser executable: {exe_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=exe_path,
            headless=True,
            args=["--no-sandbox", "--disable-gpu"],
        )

        # Test at standard desktop resolution
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: print(f"  [BROWSER CONSOLE {msg.type}] {msg.text}") if msg.type in ["error", "warning"] else None)

        print(f"[TEST] Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # 1. Verify TopBar and webR status
        topbar_title = await page.inner_text(".sr-breadcrumb-module")
        print(f"[TEST] TopBar Module: '{topbar_title}'")
        assert "Tus primeros minutos con R" in topbar_title or "Primeros pasos" in topbar_title

        print("[TEST] Waiting for webR initialization (status dot)...")
        await page.wait_for_selector("#sr-webr-status.is-ready", timeout=120000)
        status_text = await page.inner_text("#sr-webr-status-text")
        print(f"[TEST] WebR status: '{status_text}'")
        assert "R listo" in status_text
        # 2. Verify Left Pedagogical Panel (3 sections: Ejercicio, Instrucciones, Ayuda)
        section_title = await page.inner_text(".is-active-exercise .sr-section-exercise .sr-section-title")
        section_badge = await page.inner_text(".is-active-exercise .sr-section-exercise .sr-section-badge")
        title = await page.inner_text(".is-active-exercise h3.sr-exercise-title")
        print(f"[TEST] Section 1: Title='{section_title}', Badge='{section_badge}', Exercise='{title}'")
        assert "Ejercicio" in section_title
        assert "1 de 8" in section_badge
        assert "Tu primera instrucción en R" in title

        has_instr = await page.query_selector(".is-active-exercise .sr-section-instructions")
        has_help = await page.query_selector(".is-active-exercise .sr-section-help")
        assert has_instr is not None, "Missing sr-section-instructions"
        assert has_help is not None, "Missing sr-section-help"

        # Verify SVG icons presence
        has_sec_icons = await page.query_selector_all(".is-active-exercise .sr-sec-icon")
        assert len(has_sec_icons) >= 3, f"Expected at least 3 section icons, found {len(has_sec_icons)}"
        
        has_target_icon = await page.query_selector(".is-active-exercise .sr-target-icon")
        assert has_target_icon is not None, "Missing target icon in objective block"

        has_r_file_icon = await page.query_selector(".is-active-exercise .sr-r-file-icon")
        assert has_r_file_icon is not None, "Missing R script file icon in tab"

        # Verify no visible source HTML leaks or grader leaks
        body_text = await page.inner_text("body")
        assert "<div" not in body_text, "Found literal '<div' in page body!"
        assert ".checker_args" not in body_text, "Found internal '.checker_args' in page body!"
        assert "feedback <- list" not in body_text, "Found internal grader code in page body!"
        print("[TEST] DOM text is clean: No HTML tags, no .checker_args, no grader code leaks.")

        # Verify initial console state is clean and empty (no prefilled prompt)
        initial_console = await page.inner_text(".is-active-exercise .sr-console-panel")
        print(f"[TEST] Initial Console content (must not have prefilled code): '{initial_console.strip()}'")
        assert ">" not in initial_console, f"Console must not have prefilled command prompt on load, got '{initial_console}'"

        # Verify Absence of 'Ver solución'
        has_sol_btn = await page.query_selector(".is-active-exercise .sr-solution-toggle-btn")
        assert has_sol_btn is None, "'Ver solución' button must not exist in DOM"

        # Verify Left Panel Section Header Width & Full-Bleed Layout
        panel_box = await (await page.query_selector(".is-active-exercise .sr-lesson-panel")).bounding_box()
        header1_box = await (await page.query_selector(".is-active-exercise .sr-section-exercise .sr-section-header")).bounding_box()
        header2_box = await (await page.query_selector(".is-active-exercise .sr-section-instructions .sr-section-header")).bounding_box()
        header3_box = await (await page.query_selector(".is-active-exercise .sr-section-help .sr-section-header")).bounding_box()

        left_gap = header1_box["x"] - panel_box["x"]
        right_gap = (panel_box["x"] + panel_box["width"]) - (header1_box["x"] + header1_box["width"])

        print(f"[TEST] Panel width: {panel_box['width']:.1f}px, Header1 width: {header1_box['width']:.1f}px (Left gap: {left_gap:.1f}px, Right gap: {right_gap:.1f}px)")
        assert abs(header1_box["width"] - panel_box["width"]) < 2.0, f"Section header must span full width of lesson panel, got header={header1_box['width']}px, panel={panel_box['width']}px"
        assert left_gap < 2.0 and right_gap < 2.0, f"Section header must be full-bleed edge-to-edge, got left_gap={left_gap}px, right_gap={right_gap}px"

        # Confirm all 3 section headers have identical width and height
        assert abs(header1_box["width"] - header2_box["width"]) < 1.0, "Header 1 and Header 2 width must be identical"
        assert abs(header1_box["width"] - header3_box["width"]) < 1.0, "Header 1 and Header 3 width must be identical"
        assert abs(header1_box["height"] - header2_box["height"]) < 1.0, "Header 1 and Header 2 height must be identical"
        assert abs(header1_box["height"] - header3_box["height"]) < 1.0, "Header 1 and Header 3 height must be identical"

        # Confirm content inside section-body has controlled interior reading gutter (~16-24px)
        title_box = await (await page.query_selector(".is-active-exercise h3.sr-exercise-title")).bounding_box()
        text_pad_left = title_box["x"] - panel_box["x"]
        print(f"[TEST] Text reading gutter: {text_pad_left:.1f}px")
        assert 14.0 <= text_pad_left <= 26.0, f"Text reading gutter should be ~16-24px, got {text_pad_left}px"

        # 3. Verify Typography (Inter & JetBrains Mono)
        body_font = await page.evaluate("getComputedStyle(document.body).fontFamily")
        print(f"[TEST] Body Font Family: '{body_font}'")
        assert "Inter" in body_font or "sans-serif" in body_font

        cm_editors = await page.query_selector_all(".is-active-exercise .cm-editor")
        print(f"[TEST] Active exercise CodeMirror count: {len(cm_editors)}")
        assert len(cm_editors) == 1, f"Expected exactly 1 CodeMirror editor, found {len(cm_editors)}"

        editor_font = await page.evaluate("getComputedStyle(document.querySelector('.is-active-exercise .cm-editor')).fontFamily")
        print(f"[TEST] Editor Font Family: '{editor_font}'")
        assert "JetBrains Mono" in editor_font or "monospace" in editor_font

        # Test focus on editor does NOT produce dotted outline
        await page.click(".is-active-exercise .cm-content")
        focus_outline = await page.evaluate("getComputedStyle(document.querySelector('.is-active-exercise .cm-editor')).outlineStyle")
        print(f"[TEST] Editor focus outline style: '{focus_outline}'")
        assert focus_outline != "dotted", f"Editor focus outline must not be dotted, got '{focus_outline}'"

        # 4. Verify Absence of Tabs & Presence of Unified Consola R Panel
        tab_element = await page.query_selector(".is-active-exercise .sr-output-tab")
        assert tab_element is None, "Tabs (Resultado / Consola R) must not exist"

        console_header = await page.inner_text(".is-active-exercise .sr-console-title")
        print(f"[TEST] Console Header Title: '{console_header}'")
        assert "CONSOLA R" in console_header.upper()

        # 5. Verify Workspace Proportions (Editor ~2/3, Console ~1/3)
        editor_box = await (await page.query_selector(".is-active-exercise .sr-editor-body")).bounding_box()
        console_box = await (await page.query_selector(".is-active-exercise .sr-console-panel")).bounding_box()
        print(f"[TEST] Heights: Editor = {editor_box['height']:.1f}px, Console = {console_box['height']:.1f}px")
        assert editor_box["height"] > console_box["height"], f"Editor ({editor_box['height']}px) must be taller than Console ({console_box['height']}px)"

        # 6. Verify 'Comprobar respuesta' button is compact (not full width) and right-aligned
        submit_btn = await page.query_selector(".is-active-exercise .sr-btn-submit")
        box = await submit_btn.bounding_box()
        print(f"[TEST] Submit button bounding box: width={box['width']:.1f}px, height={box['height']:.1f}px")
        assert box["width"] < 300, f"Submit button is too wide ({box['width']}px), expected compact button < 300px"

        # 7. Test Single Console Transcript & Double Execution of 18 + 12
        print("[TEST] Testing single console transcript with double execution of 18 + 12...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("18 + 12")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2500)

        # Run second time
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2500)

        state2 = await page.evaluate('''() => {
            const transcript = document.querySelector(".is-active-exercise .sr-console-transcript");
            const entries = Array.from(transcript.querySelectorAll(".sr-console-entry")).map(e => e.innerText.trim());
            return {
                entriesCount: entries.length,
                entries: entries,
                fullText: transcript.innerText.trim()
            };
        }''')
        print(f"[TEST] Transcript entries count after 2 runs: {state2['entriesCount']}")
        for idx, e in enumerate(state2["entries"]):
            print(f"  [TEST] Entry {idx + 1}: {repr(e)}")
        assert state2["entriesCount"] == 2, f"Expected exactly 2 entries in transcript, got {state2['entriesCount']}"
        assert "> 18 + 12" in state2["entries"][0] and "[1] 30" in state2["entries"][0]
        assert "> 18 + 12" in state2["entries"][1] and "[1] 30" in state2["entries"][1]

        # 7.1 Verify Exactly 1 Scroll Container inside Consola R
        scroll_info = await page.evaluate('''() => {
            const panel = document.querySelector(".is-active-exercise .sr-console-panel");
            const allElements = Array.from(panel.querySelectorAll("*"));
            const scrollContainers = allElements.filter(el => {
                const style = getComputedStyle(el);
                return style.overflowY === "auto" || style.overflowY === "scroll";
            }).map(el => ({
                tag: el.tagName,
                class: el.className,
                overflowY: getComputedStyle(el).overflowY
            }));
            return {
                panelOverflow: getComputedStyle(panel).overflowY,
                scrollContainers: scrollContainers
            };
        }''')
        print(f"[TEST] Console Panel overflowY: '{scroll_info['panelOverflow']}', Scrollable containers count: {len(scroll_info['scrollContainers'])}")
        assert scroll_info["panelOverflow"] == "hidden", "Console panel itself must have overflow-y: hidden"
        assert len(scroll_info["scrollContainers"]) == 1, f"Expected exactly 1 scroll container inside console, got {len(scroll_info['scrollContainers'])}"
        assert "sr-console-transcript" in scroll_info["scrollContainers"][0]["class"]

        # 7.2 Test Auto-scroll and Scroll Up History
        print("[TEST] Testing auto-scroll with multiple executions...")
        for i in range(6):
            await page.evaluate(f'''() => {{
                const cm = document.querySelector(".is-active-exercise .cm-content");
                if (cm && cm.cmView && cm.cmView.view) {{
                    const view = cm.cmView.view;
                    view.dispatch({{
                        changes: {{ from: 0, to: view.state.doc.length, insert: "10 + {i}" }}
                    }});
                }}
            }}''')
            await page.click(".is-active-exercise .cm-content")
            await page.keyboard.press("Control+Enter")
            await page.wait_for_timeout(600)

        autoscroll_check = await page.evaluate('''() => {
            const transcript = document.querySelector(".is-active-exercise .sr-console-transcript");
            const diff = transcript.scrollHeight - (transcript.scrollTop + transcript.clientHeight);
            return {
                scrollTop: transcript.scrollTop,
                clientHeight: transcript.clientHeight,
                scrollHeight: transcript.scrollHeight,
                diff: diff,
                entriesCount: transcript.querySelectorAll(".sr-console-entry").length
            };
        }''')
        print(f"[TEST] Auto-scroll state (Entries: {autoscroll_check['entriesCount']}): scrollH={autoscroll_check['scrollHeight']}, clientH={autoscroll_check['clientHeight']}, diff={autoscroll_check['diff']}px")
        assert autoscroll_check["scrollHeight"] > autoscroll_check["clientHeight"], "Transcript must have scrollable history"
        assert autoscroll_check["diff"] <= 5.0, f"Auto-scroll must be at bottom, diff={autoscroll_check['diff']}px"

        # Test scroll up to view past history
        await page.evaluate('document.querySelector(".is-active-exercise .sr-console-transcript").scrollTop = 0')
        await page.wait_for_timeout(200)
        top_pos = await page.evaluate('document.querySelector(".is-active-exercise .sr-console-transcript").scrollTop')
        assert top_pos == 0, "User must be able to scroll up to view earlier history"

        # 7.3 Test Limpiar Button
        print("[TEST] Testing Limpiar console button...")
        await page.click(".is-active-exercise .sr-btn-clear-console")
        await page.wait_for_timeout(400)
        clean_check = await page.evaluate('''() => {
            const transcript = document.querySelector(".is-active-exercise .sr-console-transcript");
            return {
                text: transcript ? transcript.innerText.trim() : null,
                entriesCount: transcript ? transcript.querySelectorAll(".sr-console-entry").length : 0
            };
        }''')
        print(f"[TEST] Console after Limpiar: entries={clean_check['entriesCount']}, text='{clean_check['text']}'")
        assert clean_check["text"] == "", "Transcript must be empty after Limpiar"
        assert clean_check["entriesCount"] == 0

        # 7.4 Test R Error handling inside Console: 18 + a with command prompt (> 18 + a)
        print("[TEST] Testing error execution (18 + a) inside Consola R...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("18 + a")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2500)

        err_metrics = await page.evaluate('''() => {
            const entry = document.querySelector(".is-active-exercise .sr-console-entry:last-child");
            if (!entry) return null;
            const prompt = entry.querySelector(".sr-console-prompt");
            const err = entry.querySelector(".sr-console-error, .cell-output-stderr");
            const entryRect = entry.getBoundingClientRect();
            const promptRect = prompt ? prompt.getBoundingClientRect() : null;
            const errRect = err ? err.getBoundingClientRect() : null;

            return {
                entryHeight: entryRect.height,
                promptBottom: promptRect ? promptRect.bottom : null,
                errorTop: errRect ? errRect.top : null,
                verticalGap: (promptRect && errRect) ? (errRect.top - promptRect.bottom) : null,
                text: entry.innerText.trim()
            };
        }''')
        print(f"[TEST] Error entry metrics: height={err_metrics['entryHeight']:.1f}px, gap={err_metrics['verticalGap']}px, text='{err_metrics['text']}'")
        assert err_metrics is not None, "Error entry must exist in DOM"
        assert "18 + a" in err_metrics["text"], f"Console must contain executed code '> 18 + a', got '{err_metrics['text']}'"
        assert "Error: non-numeric argument to binary operator" in err_metrics["text"] or "non-numeric" in err_metrics["text"]
        assert "R Error in" not in err_metrics["text"], "Callout duplicate header 'R Error in...' must not appear in console transcript"
        assert err_metrics["entryHeight"] < 80.0, f"Error entry must be compact (< 80px), got {err_metrics['entryHeight']}px"
        assert err_metrics["verticalGap"] is not None and err_metrics["verticalGap"] < 30.0, f"Vertical gap between prompt and error must be < 30px, got {err_metrics['verticalGap']}px"

        # 7.5 Test Comment Stripping & Pure Command Prompt on Execution
        print("[TEST] Testing comment stripping in console prompt...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("# Comentario inicial\nedad_test <- 21.4")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2000)

        console_text = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Console after script with comment: {console_text.strip()}")
        assert "# Comentario" not in console_text, "Full-line comment must NOT appear in console transcript"
        assert "> edad_test <- 21.4" in console_text, "Command must appear with '>' prompt"
        assert "+ edad_test" not in console_text, "Command must NOT appear with '+' continuation prompt"

        # 7.6 Test Multiple Independent Expressions in Console
        print("[TEST] Testing multiple independent expressions in console (1 press per expression)...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("# Variables\nx_val <- 10\ny_val <- 20\nx_val + y_val")
        
        # Cursor on line 1 (# Variables) -> 1st press executes x_val <- 10
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ selection: { anchor: 0, head: 0 } });
                view.focus();
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        # 2nd press executes y_val <- 20
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        # 3rd press executes x_val + y_val
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1500)

        console_text = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Console after multiple expressions:\n{console_text.strip()}")
        assert "> x_val <- 10" in console_text
        assert "> y_val <- 20" in console_text
        assert "> x_val + y_val" in console_text
        assert "[1] 30" in console_text

        # 7.7 Test True Multi-line Syntactic Continuation Expression
        print("[TEST] Testing true multi-line continuation expression...")
        await page.evaluate("""() => {
            const cm = document.querySelector('.is-active-exercise .cm-content');
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: { from: 0, to: view.state.doc.length, insert: "mean(\\n  c(10, 20, 30)\\n)" },
                    selection: { anchor: 0, head: 0 }
                });
                view.focus();
            }
        }""")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2500)

        console_text = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Console after multi-line continuation:\n{console_text.strip()}")
        assert "> mean(" in console_text
        assert "+   c(10, 20, 30)" in console_text or "+  c(10, 20, 30)" in console_text
        assert "+ )" in console_text
        assert "[1] 20" in console_text

        # 8. Test Exercise 0 with correct value: 18 + 12 with command prompt (> 18 + 12)
        print("[TEST] Testing correct execution on Exercise 0 (18 + 12)...")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "18 + 12" } });
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2500)

        output_text = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Output after Ctrl+Enter: {output_text.strip()}")
        assert "18 + 12" in output_text, f"Console must contain executed code '> 18 + 12', got '{output_text}'"
        assert "30" in output_text, f"Expected 30 in output, got '{output_text}'"

        # 9. Test Submission & Enhanced Success State Card
        print("[TEST] Clicking Comprobar respuesta...")
        await page.wait_for_timeout(1000)
        await page.click(".is-active-exercise .sr-btn-submit")
        try:
            await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-success", timeout=15000)
        except Exception as e:
            fb = await page.inner_text(".is-active-exercise .sr-feedback-card") if await page.query_selector(".is-active-exercise .sr-feedback-card") else "No feedback card found"
            print(f"[TEST DEBUG] Feedback card text: '{fb}'")
            raise e

        fb_card = await page.query_selector(".is-active-exercise .sr-feedback-card.is-success-enhanced")
        assert fb_card is not None, "Success card must have .is-success-enhanced class"

        fb_badge = await page.query_selector(".is-active-exercise .sr-feedback-icon-badge.is-success.sr-success-badge-animated")
        assert fb_badge is not None, "Missing animated success icon badge"

        level_up_tag = await page.query_selector(".is-active-exercise .sr-success-level-up")
        assert level_up_tag is not None, "Missing level-up tag in success header"

        progress_capsule = await page.query_selector(".is-active-exercise .sr-success-progress-capsule")
        assert progress_capsule is not None, "Missing progression capsule in success card"

        step_badge_text = await page.inner_text(".is-active-exercise .sr-success-step-badge")
        print(f"[TEST] Success step badge text: '{step_badge_text}'")
        assert "Ejercicio 1 de 8 completado" in step_badge_text

        pct_badge_text = await page.inner_text(".is-active-exercise .sr-success-pct-badge")
        print(f"[TEST] Success percentage badge text: '{pct_badge_text}'")
        assert "13% del módulo" in pct_badge_text

        next_preview = await page.inner_text(".is-active-exercise .sr-success-next-row")
        print(f"[TEST] Success next preview text: '{next_preview}'")
        assert "SIGUIENTE" in next_preview.upper() and "CÁLCULO" in next_preview.upper()

        fb_title = await page.inner_text(".is-active-exercise .sr-feedback-title")
        fb_msg = await page.inner_text(".is-active-exercise .sr-feedback-body")
        print(f"[TEST] Feedback badge found, title: '{fb_title}', Message: '{fb_msg}'")
        assert "Muy bien" in fb_title

        # 10. Test Prominent Unlocked Continue Button
        continue_btns = await page.query_selector_all(".is-active-exercise .sr-btn-feedback-continue")
        visible_continues = [btn for btn in continue_btns if await btn.is_visible()]
        print(f"[TEST] Visible Continue buttons in active exercise: {len(visible_continues)}")
        assert len(visible_continues) == 1, f"Expected exactly 1 visible Continue button, found {len(visible_continues)}"
        
        unlocked_btn = await page.query_selector(".is-active-exercise .sr-btn-feedback-continue.sr-btn-continue-unlocked")
        assert unlocked_btn is not None, "Continue button must have .sr-btn-continue-unlocked class"

        print("[TEST] Clicking Continuar...")
        await page.click(".is-active-exercise .sr-btn-feedback-continue")
        await page.wait_for_timeout(600)

        active_ex_id = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] New active exercise: '{active_ex_id}'")
        assert active_ex_id == "intro-r-01-002"

        eyebrow_1 = await page.inner_text(".is-active-exercise .sr-section-exercise .sr-section-badge")
        print(f"[TEST] Exercise 2 Badge: '{eyebrow_1}'")
        assert "2 de 8" in eyebrow_1

        # 11. Test Exercise 2 with incorrect value (Amber feedback)
        print("[TEST] Testing incorrect answer on Exercise 2 (18 + 10 = 28 instead of 33)...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("18 + 10")
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2000)

        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)
        warn_title = await page.inner_text(".is-active-exercise .sr-feedback-title")
        warn_msg = await page.inner_text(".is-active-exercise .sr-feedback-body")
        print(f"[TEST] Warning feedback title: '{warn_title}', Message: '{warn_msg}'")
        assert "Casi" in warn_title or "Revisa" in warn_title

        # 12. Test Progressive Scaffolding Hint System (1 by 1 revelation)
        print("[TEST] Testing progressive hint revelation system...")
        hint_btn = await page.query_selector(".is-active-exercise .sr-hint-toggle-btn")
        hint_btn_text_0 = await hint_btn.inner_text()
        print(f"[TEST] State 0 - Hint button: '{hint_btn_text_0.strip()}'")
        assert "Ver pista" in hint_btn_text_0

        # Click 1 -> Reveal Hint 1 (only Hint 1 visible)
        await hint_btn.click()
        await page.wait_for_timeout(300)
        h1_vis = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        hint_btn_text_1 = await hint_btn.inner_text()
        print(f"[TEST] State 1 - Hint 1 visible: {h1_vis}, Hint 2 visible: {h2_vis}, Button: '{hint_btn_text_1.strip()}'")
        assert h1_vis, "Hint 1 must be visible after 1st click"
        assert not h2_vis, "Hint 2 must NOT be visible after 1st click"
        assert "Ver otra pista" in hint_btn_text_1

        # Click 2 -> Reveal Hint 2 (both Hint 1 and Hint 2 visible, button says Ocultar pistas)
        await hint_btn.click()
        await page.wait_for_timeout(300)
        h1_vis_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_2 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        hint_btn_text_2 = await hint_btn.inner_text()
        print(f"[TEST] State 2 - Hint 1 visible: {h1_vis_2}, Hint 2 visible: {h2_vis_2}, Button: '{hint_btn_text_2.strip()}'")
        assert h1_vis_2, "Hint 1 must remain visible after 2nd click"
        assert h2_vis_2, "Hint 2 must be visible after 2nd click"
        assert "Ocultar pistas" in hint_btn_text_2 or "Ocultar pista" in hint_btn_text_2

        # Click 3 -> Collapse / Hide all hints -> back to State 0
        await hint_btn.click()
        await page.wait_for_timeout(300)
        h1_vis_0 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='1']")
        h2_vis_0 = await page.is_visible(".is-active-exercise .sr-hint-card[data-hint-index='2']")
        hint_btn_text_reset = await hint_btn.inner_text()
        print(f"[TEST] State 0 (reset) - Hint 1: {h1_vis_0}, Hint 2: {h2_vis_0}, Button: '{hint_btn_text_reset.strip()}'")
        assert not h1_vis_0, "Hint 1 must be hidden after reset"
        assert not h2_vis_0, "Hint 2 must be hidden after reset"
        assert "Ver pista" in hint_btn_text_reset

        # 13. Test Reset button
        print("[TEST] Testing Reiniciar button...")
        await page.click(".is-active-exercise .sr-btn-reset")
        await page.wait_for_timeout(500)
        reset_code = await page.inner_text(".is-active-exercise .cm-content")
        print(f"[TEST] Editor content after reset: '{reset_code.strip()}'")
        assert "18 + 12" in reset_code

        # 14. Complete Exercise 2 correctly: 18 + 15
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                const line2Pos = view.state.doc.line(2).from;
                view.dispatch({
                    changes: { from: 0, to: view.state.doc.length, insert: "# Total de respuestas\\n18 + 15" },
                    selection: { anchor: line2Pos, head: line2Pos }
                });
                view.focus();
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2000)
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-success", timeout=15000)
        await page.click(".is-active-exercise .sr-btn-feedback-continue")
        await page.wait_for_timeout(600)

        # Exercise 3 (intro-r-01-003) - Guardar información
        ex3_id = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Exercise 3 active: '{ex3_id}'")
        assert ex3_id == "intro-r-01-003"
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: { from: 0, to: view.state.doc.length, insert: "respuestas <- 33\\nrespuestas" }
                });
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(2000)
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-success", timeout=15000)
        print("[TEST] Exercise 3 (Guardar información) passed successfully!")

        # Exercise 4 (intro-r-01-004) - Crea tu primer objeto (Pruebas A, B, C, D, E)
        await page.click(".is-active-exercise .sr-btn-feedback-continue")
        await page.wait_for_timeout(600)
        ex4_id = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Exercise 4 active: '{ex4_id}'")
        assert ex4_id == "intro-r-01-004"

        # Prueba A: Solo asignación (respuestas_antropologia <- 15) -> NO completado
        print("[TEST] Exercise 4 - Prueba A: Only assignment -> Warning")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 15" } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)
        fb_text_a = await page.inner_text(".is-active-exercise .sr-feedback-card")
        print(f"[TEST] Feedback Prueba A: '{fb_text_a}'")
        assert "escribe sus nombres en líneas separadas" in fb_text_a

        # Prueba B: Asignación + solo respuestas_sociologia -> NO completado
        print("[TEST] Exercise 4 - Prueba B: Only respuestas_sociologia queried -> Warning")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 15\\nrespuestas_sociologia" } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)
        fb_text_b = await page.inner_text(".is-active-exercise .sr-feedback-card")
        print(f"[TEST] Feedback Prueba B: '{fb_text_b}'")
        assert "respuestas_antropologia" in fb_text_b

        # Prueba C: Asignación + solo respuestas_antropologia -> NO completado
        print("[TEST] Exercise 4 - Prueba C: Only respuestas_antropologia queried -> Warning")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 15\\nrespuestas_antropologia" } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)
        fb_text_c = await page.inner_text(".is-active-exercise .sr-feedback-card")
        print(f"[TEST] Feedback Prueba C: '{fb_text_c}'")
        assert "respuestas_sociologia" in fb_text_c

        # Prueba D: Asignación texto "15" + ambas consultas -> NO completado
        print("[TEST] Exercise 4 - Prueba D: String '15' assignment -> Warning")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: 'respuestas_sociologia <- 18\\nrespuestas_antropologia <- "15"\\nrespuestas_sociologia\\nrespuestas_antropologia' } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)
        fb_text_d = await page.inner_text(".is-active-exercise .sr-feedback-card")
        print(f"[TEST] Feedback Prueba D: '{fb_text_d}'")
        assert "texto" in fb_text_d

        # Prueba E: Asignación correcta + ambas consultas -> COMPLETADO
        print("[TEST] Exercise 4 - Prueba E: Correct solution -> Success")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 15\\nrespuestas_sociologia\\nrespuestas_antropologia" } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-success", timeout=15000)
        fb_text_e = await page.inner_text(".is-active-exercise .sr-feedback-card")
        print(f"[TEST] Feedback Prueba E: '{fb_text_e}'")
        assert "Creaste tu primer objeto" in fb_text_e
        print("[TEST] Exercise 4 (Crea tu primer objeto) passed all 5 edge cases successfully!")

        # 16. Test Ctrl + Enter Single R Expression Execution (User Prompt Requirements 21 & 22)
        print("[TEST] Testing single R expression execution per Ctrl + Enter press...")
        await page.click(".is-active-exercise .sr-btn-clear-console")
        await page.wait_for_timeout(300)

        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: {
                        from: 0,
                        to: view.state.doc.length,
                        insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 12\\ntotal <- respuestas_sociologia + respuestas_antropologia"
                    },
                    selection: { anchor: 0, head: 0 }
                });
                view.focus();
            }
        }''')

        # 1st Ctrl + Enter on Line 1 (respuestas_sociologia <- 18)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        transcript_1st = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 1st Ctrl+Enter:\n{transcript_1st}")
        assert "respuestas_sociologia <- 18" in transcript_1st, "1st execution must contain 'respuestas_sociologia <- 18'"
        assert "respuestas_antropologia <- 12" not in transcript_1st, "1st execution MUST NOT contain 'respuestas_antropologia <- 12'"

        pos_after_1 = await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            const view = cm.cmView.view;
            const sel = view.state.selection.main;
            const line = view.state.doc.lineAt(sel.head);
            return { lineNum: line.number, lineText: line.text };
        }''')
        print(f"[TEST] Cursor after 1st Ctrl+Enter: Line {pos_after_1['lineNum']} ('{pos_after_1['lineText']}')")
        assert pos_after_1["lineNum"] == 2, f"Cursor must be at line 2 after 1st press, got line {pos_after_1['lineNum']}"

        # 2nd Ctrl + Enter on Line 2 (respuestas_antropologia <- 12)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        transcript_2nd = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 2nd Ctrl+Enter:\n{transcript_2nd}")
        assert "respuestas_antropologia <- 12" in transcript_2nd, "2nd execution must contain 'respuestas_antropologia <- 12'"

        pos_after_2 = await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            const view = cm.cmView.view;
            const sel = view.state.selection.main;
            const line = view.state.doc.lineAt(sel.head);
            return { lineNum: line.number, lineText: line.text };
        }''')
        print(f"[TEST] Cursor after 2nd Ctrl+Enter: Line {pos_after_2['lineNum']} ('{pos_after_2['lineText']}')")
        assert pos_after_2["lineNum"] == 3, f"Cursor must be at line 3 after 2nd press, got line {pos_after_2['lineNum']}"

        # 3rd Ctrl + Enter on Line 3 (total <- respuestas_sociologia + respuestas_antropologia)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        transcript_3rd = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 3rd Ctrl+Enter:\n{transcript_3rd}")
        assert "total <- respuestas_sociologia" in transcript_3rd, "3rd execution must contain 'total <- respuestas_sociologia'"

        # 16.1 Test Exact User Prompt 4-step Assignment & Query transcript output
        print("[TEST] Testing exact assignment vs query transcript output...")
        await page.click(".is-active-exercise .sr-btn-clear-console")
        await page.wait_for_timeout(300)

        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: {
                        from: 0,
                        to: view.state.doc.length,
                        insert: "respuestas_sociologia <- 18\\nrespuestas_antropologia <- 15\\nrespuestas_sociologia\\nrespuestas_antropologia"
                    },
                    selection: { anchor: 0, head: 0 }
                });
                view.focus();
            }
        }''')

        # Press 1: respuestas_sociologia <- 18 (assignment -> NO output)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)
        tr1 = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 1st press:\n{tr1.strip()}")
        assert "> respuestas_sociologia <- 18" in tr1
        assert "[1] 18" not in tr1, "Assignment MUST NOT print invisible value '[1] 18'"
        assert "respuestas_antropologia" not in tr1

        # Press 2: respuestas_antropologia <- 15 (assignment -> NO output)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)
        tr2 = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 2nd press:\n{tr2.strip()}")
        assert "> respuestas_antropologia <- 15" in tr2
        assert "[1] 15" not in tr2, "Assignment MUST NOT print invisible value '[1] 15'"

        # Press 3: respuestas_sociologia (query -> prints [1] 18)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)
        tr3 = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 3rd press:\n{tr3.strip()}")
        assert "> respuestas_sociologia" in tr3 and "[1] 18" in tr3

        # Press 4: respuestas_antropologia (query -> prints [1] 15)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)
        tr4 = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after 4th press:\n{tr4.strip()}")
        assert "> respuestas_antropologia" in tr4 and "[1] 15" in tr4
        print("[TEST] 4-step assignment vs query transcript verification PASSED 100%!")

        # 16b. Test Multiline Function Call (User Prompt Requirement 23)
        print("[TEST] Testing multiline function call execution...")
        await page.click(".is-active-exercise .sr-btn-clear-console")
        await page.wait_for_timeout(300)

        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({
                    changes: {
                        from: 0,
                        to: view.state.doc.length,
                        insert: "promedio <- mean(\\n  c(18, 12, 20)\\n)\\nresultado <- promedio * 2"
                    },
                    selection: { anchor: 0, head: 0 }
                });
                view.focus();
            }
        }''')

        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        transcript_ml = await page.inner_text(".is-active-exercise .sr-console-transcript")
        print(f"[TEST] Transcript after multiline Ctrl+Enter:\n{transcript_ml}")
        assert "promedio <- mean" in transcript_ml, "Multiline function call must execute complete"
        assert "resultado <- promedio" not in transcript_ml, "Second expression 'resultado <- promedio * 2' MUST NOT execute on 1st press"

        pos_ml = await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            const view = cm.cmView.view;
            const sel = view.state.selection.main;
            const line = view.state.doc.lineAt(sel.head);
            return { lineNum: line.number, lineText: line.text };
        }''')
        print(f"[TEST] Cursor after multiline Ctrl+Enter: Line {pos_ml['lineNum']} ('{pos_ml['lineText']}')")
        assert pos_ml["lineNum"] == 4, f"Cursor must advance past multiline function to line 4, got line {pos_ml['lineNum']}"

        # 17. Test Ctrl + Enter with Selection (Test 20)
        print("[TEST] Testing Ctrl + Enter with code selection...")
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                const line1End = view.state.doc.line(2).to;
                view.dispatch({ selection: { anchor: 0, head: line1End } });
                view.focus();
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1500)

        pos_after_sel = await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            const view = cm.cmView.view;
            const sel = view.state.selection.main;
            const line = view.state.doc.lineAt(sel.head);
            return { lineNum: line.number, empty: sel.empty };
        }''')
        print(f"[TEST] Cursor after selection execution: Line {pos_after_sel['lineNum']} (selection empty={pos_after_sel['empty']})")
        assert pos_after_sel["lineNum"] == 3, f"Cursor should advance past selection to line 3, got line {pos_after_sel['lineNum']}"

        # 18. Test Ctrl + Enter with Comment Lines (Test 21)
        print("[TEST] Testing Ctrl + Enter skipping comment lines...")
        await page.click(".is-active-exercise .cm-content")
        await page.keyboard.press("Control+A")
        await page.keyboard.press("Backspace")
        await page.keyboard.type("# Comentario 1\nx <- 10\n# Comentario 2\ny <- 20")

        # Place cursor on line 1 (# Comentario 1)
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ selection: { anchor: 0, head: 0 } });
                view.focus();
            }
        }''')

        # 1st Ctrl + Enter on comment line 1 -> executes x <- 10 on line 2, skips comment line 3, lands on line 4 (y <- 20)
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1000)

        pos_comment_1 = await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            const view = cm.cmView.view;
            const sel = view.state.selection.main;
            const line = view.state.doc.lineAt(sel.head);
            return { lineNum: line.number, lineText: line.text };
        }''')
        print(f"[TEST] Cursor after executing from comment line 1 -> Line {pos_comment_1['lineNum']} ('{pos_comment_1['lineText']}')")
        assert pos_comment_1["lineNum"] == 4, f"Ctrl+Enter should execute line 2, skip comment line 3 and land on line 4, got line {pos_comment_1['lineNum']}"

        # 19. Visual Selection Contrast Test (Test 22)
        print("[TEST] Testing visual selection contrast in CodeMirror...")
        selection_bg = await page.evaluate('''() => {
            const tokenStyle = getComputedStyle(document.documentElement).getPropertyValue("--sr-selection-bg").trim();
            return tokenStyle;
        }''')
        print(f"[TEST] Selection background CSS token value: '{selection_bg}'")
        assert selection_bg != "", "Selection background CSS token --sr-selection-bg must be defined"
        assert selection_bg == "#c7d2fe" or "rgba" in selection_bg or "#" in selection_bg

        # 21. Test Progress Persistence Across Page Reloads (User Request Tests 28, 29, 30, 31, 32, 33)
        print("[TEST] Testing LocalProgressStore persistence across reload...")
        # Reset progress first to test clean slate reload persistence
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_selector(".is-active-exercise", timeout=10000)
        await page.wait_for_selector("#sr-webr-status.is-ready", timeout=120000)

        # Complete Exercise 1 correctly
        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "18 + 12" } });
            }
        }''')
        await page.keyboard.press("Control+Enter")
        await page.wait_for_timeout(1500)
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-success", timeout=15000)
        await page.click(".is-active-exercise .sr-btn-feedback-continue")
        await page.wait_for_timeout(600)

        active_ex_before_reload = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Active exercise before reload: '{active_ex_before_reload}'")
        assert active_ex_before_reload == "intro-r-01-002"

        # Reload page and verify active exercise and stepper are restored
        print("[TEST] Reloading page to test progress restoration...")
        await page.reload(wait_until="networkidle")
        await page.wait_for_selector(".is-active-exercise", timeout=15000)

        active_ex_after_reload = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Active exercise after reload: '{active_ex_after_reload}'")
        assert active_ex_after_reload == "intro-r-01-002", f"Page reload should restore active exercise 'intro-r-01-002', got '{active_ex_after_reload}'"

        pct_after_reload = await page.inner_text("#sr-progress-pct")
        print(f"[TEST] Progress percentage after reload: '{pct_after_reload}'")
        assert "del curso" in pct_after_reload or "del módulo" in pct_after_reload

        ex1_step_text = await page.evaluate('''() => {
            const nodes = document.querySelectorAll("#sr-bottom-module-track .sr-bottom-module-step, #sr-stepper .sr-step-node");
            return nodes.length > 0 ? nodes[0].innerText.trim() : null;
        }''')
        print(f"[TEST] Stepper node 1 text after reload: '{ex1_step_text}'")
        assert ex1_step_text == "✓", f"Completed exercise 1 must retain '✓' mark after reload, got '{ex1_step_text}'"

        # 22. Test Re-executing completed exercise with wrong code does NOT downgrade completion
        print("[TEST] Testing re-submitting incorrect code on completed exercise...")
        await page.click("#sr-btn-prev")
        await page.wait_for_timeout(500)

        await page.evaluate('''() => {
            const cm = document.querySelector(".is-active-exercise .cm-content");
            if (cm && cm.cmView && cm.cmView.view) {
                const view = cm.cmView.view;
                view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: "999 + 999" } });
            }
        }''')
        await page.click(".is-active-exercise .sr-btn-submit")
        await page.wait_for_selector(".is-active-exercise .sr-feedback-card.is-warning", timeout=15000)

        ex1_step_after_wrong = await page.evaluate('''() => {
            const nodes = document.querySelectorAll("#sr-bottom-module-track .sr-bottom-module-step, #sr-stepper .sr-step-node");
            return nodes.length > 0 ? nodes[0].innerText.trim() : null;
        }''')
        print(f"[TEST] Stepper node 1 text after wrong code submission: '{ex1_step_after_wrong}'")
        assert ex1_step_after_wrong == "✓", "Re-submitting wrong code MUST NOT erase completion status"

        # 23. Test Corrupted LocalStorage Recovery Fallback
        print("[TEST] Testing corrupted localStorage recovery fallback...")
        await page.evaluate('localStorage.setItem("social-r:progress:intro-r:01-primeros-pasos", "{corrupted json syntax...")')
        await page.reload(wait_until="networkidle")
        await page.wait_for_selector(".is-active-exercise", timeout=10000)
        corrupted_active_ex = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Active exercise after corrupted localStorage: '{corrupted_active_ex}'")
        assert corrupted_active_ex == "intro-r-01-001", "App must safely recover from corrupted JSON to exercise 1"

        # 24. Test Non-existent currentExerciseId Fallback
        print("[TEST] Testing non-existent currentExerciseId fallback...")
        await page.evaluate('''() => {
            localStorage.setItem("social-r:progress:intro-r:01-primeros-pasos", JSON.stringify({
                version: 1,
                currentExerciseId: "exercise-that-does-not-exist",
                completedExercises: []
            }));
        }''')
        await page.reload(wait_until="networkidle")
        await page.wait_for_selector(".is-active-exercise", timeout=10000)
        invalid_active_ex = await page.get_attribute(".social-r-exercise.is-active-exercise", "data-exercise-id")
        print(f"[TEST] Active exercise after invalid currentExerciseId: '{invalid_active_ex}'")
        assert invalid_active_ex == "intro-r-01-001", "App must fall back safely when currentExerciseId is invalid"

        # Reset progress for clean state
        await page.evaluate("window.SocialR.resetProgress()")

        # 25. Test Responsive Viewports (1366x768, 1920x1080)
        for w, h in [(1366, 768), (1920, 1080)]:
            await page.set_viewport_size({"width": w, "height": h})
            await page.wait_for_timeout(300)
            panel_vis = await page.is_visible(".is-active-exercise .sr-lesson-panel")
            coding_vis = await page.is_visible(".is-active-exercise .sr-coding-panel")
            assert panel_vis and coding_vis, f"Layout failed at {w}x{h}"
            print(f"[TEST] Responsive layout check passed at {w}x{h}")

        print("\n" + "=" * 60)
        print("[ALL TESTS PASSED] 100% Real Browser End-to-End Verification SUCCESSFUL!")
        print("=" * 60)

        await browser.close()


if __name__ == "__main__":
    test_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4464/"
    asyncio.run(run_smoke_test(test_url))

