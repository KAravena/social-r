class QuartoLiveAdapter {
  constructor() {
    this.visibleHintCounts = new Map();
    this.hintPointers = this.visibleHintCounts;
    this.hintOpenState = new Map();
    this._lastHintClickTime = 0;
    this._webRPromise = null;
    this.lastSubmittedCode = new Map();
    this.lastExecutedCode = new Map();
    this.submissionCounter = 0;
    this.evaluators = new Map();
  }

  formatExecutedCodeForConsole(code) {
    if (!code || typeof code !== "string") return "";

    const rawLines = code.split(/\r?\n/);
    // 1. Filter out whole-line comments when mixed with executable code
    let nonCommentLines = rawLines.filter((l) => !/^\s*#/.test(l));

    // 2. Trim leading and trailing blank lines
    while (nonCommentLines.length > 0 && nonCommentLines[0].trim() === "") {
      nonCommentLines.shift();
    }
    while (nonCommentLines.length > 0 && nonCommentLines[nonCommentLines.length - 1].trim() === "") {
      nonCommentLines.pop();
    }

    if (nonCommentLines.length === 0) {
      const trimmedRaw = rawLines.filter((l) => l.trim() !== "");
      if (trimmedRaw.length === 0) return "";
      return trimmedRaw.map((l, i) => (i === 0 ? `> ${l}` : `+ ${l}`)).join("\n");
    }

    const formattedLines = [];
    let bracketDepth = 0;
    let inString = null;
    let isEscaped = false;
    let prevEndsWithOperator = false;

    for (let i = 0; i < nonCommentLines.length; i++) {
      const line = nonCommentLines[i];
      if (line.trim() === "" && bracketDepth === 0 && !prevEndsWithOperator) {
        continue;
      }

      const isContinuation = bracketDepth > 0 || prevEndsWithOperator;
      const prompt = isContinuation ? "+ " : "> ";
      formattedLines.push(prompt + line);

      // Scan characters to track brackets, strings, and operators
      let strippedLine = "";
      for (let cIdx = 0; cIdx < line.length; cIdx++) {
        const ch = line[cIdx];
        if (isEscaped) {
          isEscaped = false;
          continue;
        }
        if (ch === "\\") {
          isEscaped = true;
          continue;
        }
        if (inString) {
          if (ch === inString) {
            inString = null;
          }
          continue;
        }
        if (ch === '"' || ch === "'") {
          inString = ch;
          continue;
        }
        if (ch === "#") {
          // Inline comment starts -> ignore rest of line for syntax analysis
          break;
        }
        strippedLine += ch;
        if (ch === "(" || ch === "[" || ch === "{") {
          bracketDepth++;
        } else if (ch === ")" || ch === "]" || ch === "}") {
          if (bracketDepth > 0) bracketDepth--;
        }
      }

      const trimmedStripped = strippedLine.trim();
      // Check if line ends with a dangling operator, pipe, comma, or assignment
      prevEndsWithOperator = /([+\-*/^=~<>&|,]|<-|%>%|\|>|::|:::|%[a-zA-Z0-9._]+%)\s*$/.test(trimmedStripped);
    }

    return formattedLines.join("\n");
  }

  formatPromptCode(code) {
    return this.formatExecutedCodeForConsole(code);
  }

  escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  getTranscriptElement(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    if (!container) return null;

    let transcript = container.querySelector(".sr-console-transcript");
    if (!transcript) {
      const panel = container.querySelector(".sr-console-panel");
      if (panel) {
        transcript = document.createElement("div");
        transcript.className = "sr-console-transcript";
        transcript.setAttribute("data-exercise-id", exerciseId);
        panel.appendChild(transcript);
      }
    }
    return transcript;
  }

  cleanOutputNodeForConsole(outputNode, entry) {
    if (!outputNode) return null;

    const fragment = document.createDocumentFragment();
    let hasContent = false;

    // Collect meaningful output children
    const items = outputNode.querySelectorAll(
      ".callout-important, .callout-danger, .callout-warning, .cell-output-stdout, .cell-output-stderr, canvas, img, svg, table"
    );

    if (items.length === 0) {
      const rawText = (outputNode.innerText !== undefined ? outputNode.innerText : outputNode.textContent).trim();
      if (rawText) {
        const outBody = document.createElement("div");
        outBody.className = "sr-console-output-body";
        const pre = document.createElement("pre");
        const code = document.createElement("code");
        code.textContent = rawText;
        pre.appendChild(code);
        outBody.appendChild(pre);
        return outBody;
      }
      return null;
    }

    items.forEach((item) => {
      // Avoid processing nested elements inside callouts twice
      if (item.parentElement && item.parentElement.closest(".callout-important, .callout-danger, .callout-warning")) {
        return;
      }

      if (item.matches(".callout-important, .callout-danger")) {
        entry.classList.add("is-error");
        const pre = item.querySelector(".callout-body pre, pre, code") || item;
        const text = (pre.innerText !== undefined ? pre.innerText : pre.textContent).trim();
        if (text) {
          const errDiv = document.createElement("div");
          errDiv.className = "sr-console-error";
          const preEl = document.createElement("pre");
          const codeEl = document.createElement("code");
          codeEl.textContent = text;
          preEl.appendChild(codeEl);
          errDiv.appendChild(preEl);
          fragment.appendChild(errDiv);
          hasContent = true;
        }
      } else if (item.matches(".callout-warning")) {
        entry.classList.add("is-warning");
        const pre = item.querySelector(".callout-body pre, pre, code") || item;
        const text = (pre.innerText !== undefined ? pre.innerText : pre.textContent).trim();
        if (text) {
          const warnDiv = document.createElement("div");
          warnDiv.className = "sr-console-warning";
          const preEl = document.createElement("pre");
          const codeEl = document.createElement("code");
          codeEl.textContent = text;
          preEl.appendChild(codeEl);
          warnDiv.appendChild(preEl);
          fragment.appendChild(warnDiv);
          hasContent = true;
        }
      } else if (item.matches(".cell-output-stdout, .cell-output-stderr")) {
        const pre = item.querySelector("pre, code") || item;
        const text = (pre.innerText !== undefined ? pre.innerText : pre.textContent).trimEnd();
        if (text && text.trim().length > 0) {
          const outBody = document.createElement("div");
          outBody.className = "sr-console-output-body";
          const preEl = document.createElement("pre");
          const codeEl = document.createElement("code");
          codeEl.textContent = text;
          preEl.appendChild(codeEl);
          outBody.appendChild(preEl);
          fragment.appendChild(outBody);
          hasContent = true;
        }
      } else if (item.matches("canvas, img, svg, table")) {
        const outBody = document.createElement("div");
        outBody.className = "sr-console-output-body";
        outBody.appendChild(item.cloneNode(true));
        fragment.appendChild(outBody);
        hasContent = true;
      }
    });

    if (!hasContent) return null;

    const wrapper = document.createElement("div");
    wrapper.className = "sr-console-result-wrapper";
    wrapper.appendChild(fragment);
    return wrapper;
  }

  appendTranscriptEntry(exerciseId, rawCode, outputNode = null) {
    const transcript = this.getTranscriptElement(exerciseId);
    if (!transcript) return;

    const formattedPrompt = this.formatExecutedCodeForConsole(rawCode);
    if (!formattedPrompt && !outputNode) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry";

    // 1. Command Prompt line (> code / + code)
    if (formattedPrompt) {
      const promptDiv = document.createElement("div");
      promptDiv.className = "sr-console-prompt";
      promptDiv.textContent = formattedPrompt;
      entry.appendChild(promptDiv);
    }

    // 2. Output result (stdout / stderr / error / figures)
    if (outputNode) {
      const resultElement = this.cleanOutputNodeForConsole(outputNode, entry);
      if (resultElement) {
        entry.appendChild(resultElement);
      }
    }

    transcript.appendChild(entry);

    // Auto-scroll transcript directly to bottom
    transcript.scrollTop = transcript.scrollHeight;
  }

  async getWebR() {
    if (this._webRPromise) return this._webRPromise;

    this._webRPromise = new Promise((resolve, reject) => {
      let attempts = 0;
      const maxAttempts = 100;

      const check = () => {
        attempts++;
        try {
          if (
            window._ojs &&
            window._ojs.ojsConnector &&
            window._ojs.ojsConnector.mainModule &&
            window._ojs.ojsConnector.mainModule._scope.has("webROjs")
          ) {
            const webROjs = window._ojs.ojsConnector.mainModule._scope.get("webROjs")._value;
            if (webROjs && webROjs.webRPromise) {
              webROjs.webRPromise.then(resolve).catch(reject);
              return;
            }
          }
        } catch (e) {}

        if (attempts >= maxAttempts) {
          reject(new Error("Timeout waiting for webR runtime initialization."));
        } else {
          setTimeout(check, 100);
        }
      };

      check();
    });

    return this._webRPromise;
  }

  async getEvaluator(exerciseId) {
    if (this.evaluators.has(exerciseId)) {
      return this.evaluators.get(exerciseId);
    }
    const webR = await this.getWebR();
    const { WebREvaluator } = window._exercise_ojs_runtime;
    const context = {
      code: "",
      options: {
        id: `webr-${exerciseId}-contents`,
        envir: `exercise-env-${exerciseId}`,
        exercise: exerciseId,
        warning: true,
        error: false,
        canvas: true,
        timelimit: 30
      }
    };
    const evaluator = new WebREvaluator(webR, context);
    this.evaluators.set(exerciseId, evaluator);
    return evaluator;
  }

  getExerciseContainer(exerciseId) {
    return document.querySelector(`.social-r-exercise[data-exercise-id="${exerciseId}"]`);
  }

  getEditorCard(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    return container ? container.querySelector(".sr-editor-body") || container : null;
  }

  getEditor(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    return container ? container.querySelector(".cm-editor") : null;
  }

  getEvaluationOutput(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    return container ? container.querySelector(".cell-output-container, .cell-output-stdout, .cell-output, .exercise-cell-output") : null;
  }

  getGradeFeedback(exerciseId) {
    return document.getElementById(`sr-feedback-card-${exerciseId}`);
  }

  run(exerciseId) {
    return this.runCode(exerciseId);
  }

  submit(exerciseId) {
    return this.submitCode(exerciseId);
  }

  getCode(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    if (!container) return "";

    // 1. State doc from CodeMirror 6 EditorView (.cm-content or .cm-editor)
    const cmContent = container.querySelector(".cm-content");
    if (cmContent && cmContent.cmView && cmContent.cmView.view) {
      return cmContent.cmView.view.state.doc.toString();
    }

    const cmEditor = container.querySelector(".cm-editor");
    if (cmEditor && cmEditor.cmView && cmEditor.cmView.view) {
      return cmEditor.cmView.view.state.doc.toString();
    }

    // 2. DOM text content from .cm-line
    if (cmContent) {
      const lines = Array.from(cmContent.querySelectorAll(".cm-line"));
      if (lines.length > 0) {
        const domCode = lines.map((l) => l.textContent).join("\n");
        if (domCode.trim()) {
          return domCode;
        }
      }
      if (cmContent.innerText !== undefined && cmContent.innerText.trim()) {
        return cmContent.innerText.replace(/\r\n/g, "\n");
      }
    }

    // 3. Quarto Live cell object value
    const cell = container.querySelector(".exercise-cell, .card, div[id^='webr-']");
    if (cell && cell.value && cell.value.code) {
      return cell.value.code;
    }

    return "";
  }

  getCMView(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    if (!container) return null;
    const cmContent = container.querySelector(".cm-content");
    if (cmContent && cmContent.cmView && cmContent.cmView.view) {
      return cmContent.cmView.view;
    }
    const cmEditor = container.querySelector(".cm-editor");
    if (cmEditor && cmEditor.cmView && cmEditor.cmView.view) {
      return cmEditor.cmView.view;
    }
    return null;
  }

  setCode(exerciseId, newCode) {
    const view = this.getCMView(exerciseId);
    if (view && view.state && view.state.doc) {
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: newCode }
      });
      return true;
    }
    return false;
  }

  invalidateFeedbackIfStale(exerciseId) {
    if (!exerciseId) return;
    const currentCode = this.getCode(exerciseId);
    const submittedCode = this.lastSubmittedCode.get(exerciseId);

    // If student has modified code since last submission, invalidate and hide stale feedback immediately!
    if (submittedCode !== undefined && currentCode !== submittedCode) {
      const card = this.getGradeFeedback(exerciseId);
      if (card) {
        card.className = "sr-feedback-card";
        card.innerHTML = "";
      }
    }
  }

  async runCode(exerciseId) {
    console.log("[SR Native] runCode for:", exerciseId);
    if (!exerciseId) return;

    const container = this.getExerciseContainer(exerciseId);
    if (!container) return;

    const exprInfo = this.getExpressionToRun(exerciseId);
    const codeToRun = exprInfo.code;
    if (!codeToRun || !codeToRun.trim()) {
      return;
    }

    this.lastExecutedCode.set(exerciseId, codeToRun);

    // 1. Advance cursor to position after executed expression and retain editor focus
    this.setCursorPosition(exerciseId, exprInfo.nextPos);

    // 2. Emit global event
    window.SocialR.events.emit("code_run", { exerciseId, code: codeToRun });

    // 3. Evaluate single atomic expression in WebR and render transcript immediately
    try {
      const evaluator = await this.getEvaluator(exerciseId);
      const evalResult = await evaluator.evaluate(codeToRun, "result");
      const htmlNode = evalResult ? await evaluator.asHtml(evalResult) : null;
      this.appendTranscriptEntry(exerciseId, codeToRun, htmlNode);
    } catch (err) {
      console.error("[SR Adapter ERR] runCode failed:", err);
      const errContainer = document.createElement("div");
      errContainer.className = "sr-console-error";
      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = err.message || String(err);
      pre.appendChild(code);
      errContainer.appendChild(pre);
      this.appendTranscriptEntry(exerciseId, codeToRun, errContainer);
    }
  }

  getCMView(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    if (!container) return null;

    const cmContent = container.querySelector(".cm-content");
    if (cmContent && cmContent.cmView && cmContent.cmView.view) {
      return cmContent.cmView.view;
    }

    const cmEditor = container.querySelector(".cm-editor");
    if (cmEditor && cmEditor.cmView && cmEditor.cmView.view) {
      return cmEditor.cmView.view;
    }

    return null;
  }

  findNextExecutablePos(doc, afterLineNum) {
    let searchNum = afterLineNum + 1;

    while (searchNum <= doc.lines) {
      const line = doc.line(searchNum);
      const text = line.text;

      const isExecutable = !/^\s*(#.*)?$/.test(text);
      if (isExecutable) {
        const match = text.match(/^\s*/);
        const indentLen = match ? match[0].length : 0;
        return line.from + indentLen;
      }

      searchNum++;
    }

    return doc.length;
  }

  findStatementStartLine(doc, fromLineNum) {
    let startLine = fromLineNum;
    while (startLine > 1) {
      const prevLine = doc.line(startLine - 1);
      const prevText = prevLine.text.replace(/#.*$/, "").trim();
      if (!prevText) {
        // Blank line separates statements unless open bracket exists across it
        let depth = 0;
        for (let l = 1; l < startLine; l++) {
          const t = doc.line(l).text.replace(/#.*$/, "");
          for (const ch of t) {
            if (ch === "(" || ch === "[" || ch === "{") depth++;
            else if (ch === ")" || ch === "]" || ch === "}") {
              if (depth > 0) depth--;
            }
          }
        }
        if (depth === 0) break;
      }

      const prevEndsWithOp = /([+\-*/^=~<>&|,]|<-|%>%|\|>|::|:::|%[a-zA-Z0-9._]+%)\s*$/.test(prevText);
      const currLine = doc.line(startLine);
      const currText = currLine.text.replace(/#.*$/, "").trim();
      const currStartsWithContinuation = /^(else\b|%>%|\|>|[+*/^&|])/.test(currText);

      let depth = 0;
      for (let l = 1; l < startLine; l++) {
        const t = doc.line(l).text.replace(/#.*$/, "");
        for (const ch of t) {
          if (ch === "(" || ch === "[" || ch === "{") depth++;
          else if (ch === ")" || ch === "]" || ch === "}") {
            if (depth > 0) depth--;
          }
        }
      }

      if (prevEndsWithOp || currStartsWithContinuation || depth > 0) {
        startLine--;
      } else {
        break;
      }
    }
    return startLine;
  }

  getExpressionToRun(exerciseId) {
    const view = this.getCMView(exerciseId);
    if (!view || !view.state || !view.state.doc) {
      const fallbackCode = this.getCode(exerciseId);
      return { code: fallbackCode, nextPos: 0 };
    }

    const state = view.state;
    const doc = state.doc;
    const sel = state.selection ? state.selection.main : null;

    // 1. Manual selection: run exact selected text block
    if (sel && !sel.empty) {
      const selectedCode = doc.sliceString(sel.from, sel.to);
      const maxPos = Math.max(sel.from, sel.to);
      const endLineNum = doc.lineAt(maxPos).number;
      const nextPos = this.findNextExecutablePos(doc, endLineNum);
      return { code: selectedCode, nextPos };
    }

    // 2. No manual selection: extract single complete R expression starting at cursor
    const currentPos = sel ? sel.head : 0;
    let curLineObj = doc.lineAt(Math.min(currentPos, doc.length));
    let curLineNum = curLineObj.number;

    // Skip leading comment-only or blank lines if cursor is currently on one
    while (curLineNum <= doc.lines && /^\s*(#.*)?$/.test(doc.line(curLineNum).text)) {
      curLineNum++;
    }

    if (curLineNum > doc.lines) {
      return { code: "", nextPos: doc.length };
    }

    // Scan backwards to find the top of the statement if cursor was on a continuation line
    const startLineNum = this.findStatementStartLine(doc, curLineNum);

    let lineNum = startLineNum;
    let bracketDepth = 0;
    let inString = null;
    let isEscaped = false;
    const linesContent = [];

    while (lineNum <= doc.lines) {
      const lineText = doc.line(lineNum).text;
      linesContent.push(lineText);

      for (let i = 0; i < lineText.length; i++) {
        const ch = lineText[i];
        if (isEscaped) {
          isEscaped = false;
          continue;
        }
        if (ch === "\\") {
          isEscaped = true;
          continue;
        }
        if (inString) {
          if (ch === inString) inString = null;
          continue;
        }
        if (ch === '"' || ch === "'") {
          inString = ch;
          continue;
        }
        if (ch === "#") {
          break;
        }
        if (ch === "(" || ch === "[" || ch === "{") {
          bracketDepth++;
        } else if (ch === ")" || ch === "]" || ch === "}") {
          if (bracketDepth > 0) bracketDepth--;
        }
      }

      const cleanText = lineText.replace(/#.*$/, "").trim();
      const endsWithOp = /([+\-*/^=~<>&|,]|<-|%>%|\|>|::|:::|%[a-zA-Z0-9._]+%)\s*$/.test(cleanText);
      const endsWithControl = /\b(else|function\s*\([^)]*\))\s*$/.test(cleanText);

      if (bracketDepth === 0 && inString === null && !endsWithOp && !endsWithControl) {
        // Look ahead to check if the next non-empty line is a syntactic continuation (e.g. else, pipe, operator)
        let peekLineNum = lineNum + 1;
        while (peekLineNum <= doc.lines && /^\s*(#.*)?$/.test(doc.line(peekLineNum).text)) {
          peekLineNum++;
        }
        let nextIsContinuation = false;
        if (peekLineNum <= doc.lines) {
          const peekText = doc.line(peekLineNum).text.replace(/#.*$/, "").trim();
          nextIsContinuation = /^(else\b|%>%|\|>|[+*/^&|])/.test(peekText);
        }

        if (!nextIsContinuation) {
          const code = linesContent.join("\n");
          const nextPos = this.findNextExecutablePos(doc, lineNum);
          return { code, nextPos };
        }
      }

      lineNum++;
    }

    const code = linesContent.join("\n");
    return { code, nextPos: doc.length };
  }

  setCursorPosition(exerciseId, targetPos) {
    const view = this.getCMView(exerciseId);
    if (!view || !view.state || !view.state.doc) return;

    const safePos = Math.min(Math.max(0, targetPos), view.state.doc.length);
    try {
      view.dispatch({
        selection: { anchor: safePos, head: safePos },
        scrollIntoView: true
      });
      view.focus();
    } catch (err) {
      console.error("[SR Adapter ERR] setCursorPosition failed:", err);
    }
  }

  submit(exerciseId) {
    return this.submitCode(exerciseId);
  }

  async submitCode(exerciseId) {
    console.log("[SR Native] submitCode for:", exerciseId);
    if (!exerciseId) return;

    const container = this.getExerciseContainer(exerciseId);
    if (!container) return;

    const code = this.getCode(exerciseId);
    if (!code || !code.trim()) {
      this.renderFeedbackCard(exerciseId, "warning", "Revisa tu respuesta", "Por favor escribe código antes de enviar.");
      return;
    }

    this.lastSubmittedCode.set(exerciseId, code);
    const submissionId = ++this.submissionCounter;

    const submitBtn = container.querySelector(".sr-btn-submit");
    if (submitBtn) submitBtn.disabled = true;

    window.SocialR.events.emit("exercise_submitted", { exerciseId, code });

    // 1. Sync code with Quarto Live cell object
    const cell = container.querySelector(".card.exercise-editor, .exercise-cell, div[id^='webr-']");
    if (cell) {
      if (cell.value) cell.value.code = code;
      cell.dispatchEvent(new CustomEvent("input", { detail: { commit: true, code }, bubbles: true, cancelable: true }));
      cell.dispatchEvent(new Event("input", { bubbles: true, cancelable: true }));
    }

    // 2. Grade code via WebREvaluator & WebRGrader (Diagnostics only, NO console echo)
    try {
      const webR = await this.getWebR();
      const { WebREvaluator, WebRGrader } = window._exercise_ojs_runtime;

      const context = {
        code: code,
        options: {
          id: `webr-${exerciseId}-contents`,
          envir: `exercise-env-${exerciseId}`,
          exercise: exerciseId,
          checker: true
        }
      };

      const evaluator = new WebREvaluator(webR, context);
      await evaluator.process({});
      const grader = new WebRGrader(evaluator);
      const feedbackEl = await grader.gradeExercise();

      if (submissionId !== this.submissionCounter) return;

      let isCorrect = false;
      let type = "info";
      let messageHtml = "";

      if (feedbackEl) {
        if (feedbackEl.classList.contains("alert-success")) {
          isCorrect = true;
          type = "success";
        } else if (feedbackEl.classList.contains("alert-warning")) {
          type = "warning";
        } else if (feedbackEl.classList.contains("alert-info")) {
          type = "info";
        } else if (feedbackEl.classList.contains("alert-danger")) {
          type = "error";
        }

        const fbMsg = feedbackEl.querySelector(".exercise-feedback");
        messageHtml = fbMsg ? fbMsg.innerHTML : feedbackEl.innerHTML;
      }

      if (messageHtml && messageHtml.trim() !== "NULL" && !messageHtml.includes("NULL")) {
        let title = isCorrect ? "✓ Muy bien" : (type === "warning" ? "Casi" : (type === "error" ? "Tu código no se puede ejecutar" : "Nota"));

        // Intercept syntax errors or QuartoLive parse check messages to ensure friendly Spanish
        if (messageHtml.includes("It looks like this might not be valid R code") ||
            messageHtml.includes("R cannot determine how to turn your text") ||
            messageHtml.includes("instrucción incompleta o mal escrita")) {
          title = "Tu código no se puede ejecutar";
          messageHtml = "R encontró una instrucción incompleta o mal escrita.<br>Revisa si falta algún valor, una coma, un paréntesis o una comilla.";
        }

        this.renderFeedbackCard(exerciseId, type, title, messageHtml, isCorrect);

        if (isCorrect) {
          window.SocialR.progress.save(exerciseId, { status: "completed" });
          window.SocialR.events.emit("exercise_completed", { exerciseId });
          if (window.SocialR.navigation && typeof window.SocialR.navigation.refreshUI === "function") {
            window.SocialR.navigation.refreshUI();
          }
        } else {
          const current = window.SocialR.progress.get(exerciseId);
          window.SocialR.progress.save(exerciseId, {
            status: "in_progress",
            attempts: (current.attempts || 0) + 1
          });
          if (window.SocialR.navigation && typeof window.SocialR.navigation.refreshUI === "function") {
            window.SocialR.navigation.refreshUI();
          }
        }
      }
    } catch (err) {
      console.error("[SR Adapter ERR] submitCode failed:", err);
      this.renderFeedbackCard(exerciseId, "error", "Tu código no se puede ejecutar", "R encontró una instrucción incompleta o mal escrita.<br>Revisa si falta algún valor, una coma, un paréntesis o una comilla.", false);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  formatInline(str) {
    if (!str) return "";

    // 1. Unescape accidental backslash escapes from Markdown tokens first
    let text = String(str).replace(/\\+([*_`>:\-\.#\(\)\[\]])/g, "$1");

    // 2. Extract existing inline HTML tags (e.g. <strong>, <em>, <code>) to protect them from double escaping
    const tagSpans = [];
    text = text.replace(/<\/?(?:strong|b|em|i|code|span)[^>]*>/gi, (match) => {
      const idx = tagSpans.length;
      tagSpans.push(match);
      return `___SR_TAG_${idx}___`;
    });

    // 3. Extract inline code blocks first to protect code contents from html escaping / formatting
    const codeSpans = [];
    let s = text.replace(/`([^`]+)`/g, (match, codeContent) => {
      // Escape HTML inside code block
      const safeCode = codeContent
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
      const idx = codeSpans.length;
      codeSpans.push(`<code class="sr-inline-code">${safeCode}</code>`);
      return `___SR_CODE_${idx}___`;
    });

    // 4. Escape HTML characters in remaining surrounding text (prevents XSS)
    s = s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");

    // 5. Bold: **text** (handles **Bien.** and all internal punctuation)
    s = s.replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>");

    // 6. Italic: *text* (not surrounded by asterisks) or _text_
    s = s.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");
    s = s.replace(/\b_([^_]+)_\b/g, "<em>$1</em>");

    // 7. Restore code spans
    for (let idx = 0; idx < codeSpans.length; idx++) {
      s = s.replace(`___SR_CODE_${idx}___`, codeSpans[idx]);
    }

    // 8. Restore preserved tag spans
    for (let idx = 0; idx < tagSpans.length; idx++) {
      s = s.replace(`___SR_TAG_${idx}___`, tagSpans[idx]);
    }

    return s;
  }

  parseMarkdownFeedback(rawText) {
    if (!rawText) return "";

    // Normalize line endings, strip wrapping paragraph/div tags, and decode common HTML entities
    let text = String(rawText)
      .replace(/<\/?(?:p|div)[^>]*>/gi, "\n")
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/&gt;/g, ">")
      .replace(/&lt;/g, "<")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&amp;/g, "&");

    // Clean up R output prefix like [1] if present
    text = text.replace(/^\[\d+\]\s*"?(.*?)"?$/gm, "$1");

    // Remove accidental backslash escapes from markdown characters
    text = text.replace(/\\+([*_`>:\-\.#\(\)\[\]])/g, "$1");

    // Split into lines
    const lines = text.split(/\r?\n/);
    const blocks = [];
    let currentQuote = [];
    let currentList = [];
    let currentListType = null;
    let currentParagraph = [];

    const flushParagraph = () => {
      if (currentParagraph.length > 0) {
        const pText = currentParagraph.join(" ").trim();
        if (pText) {
          blocks.push({ type: "p", text: pText });
        }
        currentParagraph = [];
      }
    };

    const flushQuote = () => {
      if (currentQuote.length > 0) {
        blocks.push({ type: "quote", lines: [...currentQuote] });
        currentQuote = [];
      }
    };

    const flushList = () => {
      if (currentList.length > 0 && currentListType) {
        blocks.push({ type: currentListType, items: [...currentList] });
        currentList = [];
        currentListType = null;
      }
    };

    const flushAll = () => {
      flushParagraph();
      flushQuote();
      flushList();
    };

    for (let i = 0; i < lines.length; i++) {
      const rawLine = lines[i].trim();
      if (!rawLine) {
        flushAll();
        continue;
      }

      // Blockquote: starts with '>' or escaped '\>'
      if (rawLine.startsWith(">") || rawLine.startsWith("\\>")) {
        flushParagraph();
        flushList();
        const qContent = rawLine.replace(/^\\?>\s*/, "").trim();
        currentQuote.push(qContent);
        continue;
      }

      // Unordered list: starts with '- ' or '* '
      const ulMatch = rawLine.match(/^[-*]\s+(.*)$/);
      if (ulMatch) {
        flushParagraph();
        flushQuote();
        if (currentListType !== "ul") {
          flushList();
          currentListType = "ul";
        }
        currentList.push(ulMatch[1].trim());
        continue;
      }

      // Ordered list: starts with '1. ', '2. ', etc.
      const olMatch = rawLine.match(/^\d+\.\s+(.*)$/);
      if (olMatch) {
        flushParagraph();
        flushQuote();
        if (currentListType !== "ol") {
          flushList();
          currentListType = "ol";
        }
        currentList.push(olMatch[1].trim());
        continue;
      }

      // Normal text line
      flushQuote();
      flushList();
      currentParagraph.push(rawLine);
    }
    flushAll();

    let html = "";
    for (const b of blocks) {
      if (b.type === "p") {
        html += `<p class="sr-feedback-p">${this.formatInline(b.text)}</p>`;
      } else if (b.type === "quote") {
        const qParas = [];
        let curQP = [];
        for (const ql of b.lines) {
          if (!ql) {
            if (curQP.length) { qParas.push(curQP.join(" ")); curQP = []; }
          } else {
            curQP.push(ql);
          }
        }
        if (curQP.length) qParas.push(curQP.join(" "));

        html += `<blockquote class="sr-feedback-quote">`;
        for (const qp of qParas) {
          html += `<p>${this.formatInline(qp)}</p>`;
        }
        html += `</blockquote>`;
      } else if (b.type === "ul") {
        html += `<ul class="sr-feedback-list">`;
        for (const it of b.items) {
          html += `<li>${this.formatInline(it)}</li>`;
        }
        html += `</ul>`;
      } else if (b.type === "ol") {
        html += `<ol class="sr-feedback-list">`;
        for (const it of b.items) {
          html += `<li>${this.formatInline(it)}</li>`;
        }
        html += `</ol>`;
      }
    }
    return html;
  }

  renderFeedbackCard(exerciseId, type, title, messageHtml, isCorrect = false) {
    const card = this.getGradeFeedback(exerciseId);
    if (!card) return;

    const formattedBody = this.parseMarkdownFeedback(messageHtml);
    let contentHtml = "";

    if (isCorrect) {
      const exInfo = (window.SocialR && window.SocialR.navigation && typeof window.SocialR.navigation.getExerciseInfo === "function")
        ? window.SocialR.navigation.getExerciseInfo(exerciseId)
        : null;

      const order = exInfo ? exInfo.order : 0;
      const modTotal = exInfo ? exInfo.moduleTotal : 8;
      const modOrder = exInfo ? exInfo.moduleOrder : 1;
      const nextTitle = exInfo ? exInfo.nextTitle : "";
      const isLastInModule = exInfo ? exInfo.isLastInModule : false;
      const isLastInCourse = exInfo ? exInfo.isLastInCourse : false;
      const progressPct = Math.round(((order + 1) / modTotal) * 100);

      const displayTitle = title && title.includes("Muy bien")
        ? "✓ Muy bien"
        : this.formatInline(title || "✓ Muy bien");

      contentHtml = `
        <div class="sr-feedback-header">
          <div class="sr-feedback-icon-badge is-success sr-success-badge-animated">
            <svg class="sr-check-svg" aria-hidden="true" focusable="false" role="img" width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <path class="sr-check-path" d="M4.5 10.5l3.5 3.5L15.5 6"/>
            </svg>
          </div>
          <div class="sr-feedback-header-content">
            <span class="sr-feedback-title">${displayTitle}</span>
            <span class="sr-success-level-up">Paso completado</span>
          </div>
        </div>

        <div class="sr-feedback-body">${formattedBody}</div>

        <div class="sr-success-progress-capsule" role="status" aria-label="Progreso del módulo">
          <div class="sr-success-progress-row">
            <div class="sr-success-step-badge">
              <svg class="sr-success-mini-icon" aria-hidden="true" focusable="false" role="img" width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm3.2 5.3-4 4a.8.8 0 0 1-1.1 0l-2-2a.8.8 0 1 1 1.1-1.1L6.6 8.7l3.5-3.5a.8.8 0 0 1 1.1 1.1z"/></svg>
              <span class="sr-success-step-label">Ejercicio ${order + 1} de ${modTotal} completado</span>
            </div>
            <div class="sr-success-pct-badge">
              <span class="sr-success-pct-label">${progressPct}% del módulo</span>
            </div>
          </div>
          ${nextTitle ? `
          <div class="sr-success-next-row">
            <span class="sr-next-label">Siguiente</span>
            <span class="sr-next-sep" aria-hidden="true">:</span>
            <span class="sr-next-title">${this.formatInline(nextTitle)}</span>
          </div>` : isLastInModule ? `
          <div class="sr-success-next-row is-module-end">
            <span class="sr-next-label">Módulo finalizado</span>
            <span class="sr-next-sep" aria-hidden="true">:</span>
            <span class="sr-next-title">¡Has completado los ${modTotal} ejercicios del Módulo ${modOrder}!</span>
          </div>` : ''}
        </div>

        <div class="sr-feedback-actions">
          ${isLastInModule ? `
            <button class="sr-btn-feedback-continue sr-btn-celebrate-module" data-exercise-id="${exerciseId}" data-module-id="${exInfo.moduleId}">
              <svg class="sr-trophy-icon" aria-hidden="true" focusable="false" role="img" width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M2.5.5A.5.5 0 0 1 3 1v1h10V1a.5.5 0 0 1 1 0v1.5a3.5 3.5 0 0 1-3.5 3.5H9.9a4.5 4.5 0 0 1-1.4 2.2V11h2a.5.5 0 0 1 0 1H5.5a.5.5 0 0 1 0-1h2V9.2A4.5 4.5 0 0 1 6.1 7H5.5A3.5 3.5 0 0 1 2 3.5V1a.5.5 0 0 1 .5-.5z"/></svg>
              <span>Ver resumen del Módulo ${modOrder} →</span>
            </button>` : `
            <button class="sr-btn-feedback-continue sr-btn-continue-unlocked" data-exercise-id="${exerciseId}">
              <span>Continuar</span>
              <svg class="sr-arrow-icon" aria-hidden="true" focusable="false" role="img" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 8h10M9 4l4 4-4 4"/>
              </svg>
            </button>`
          }
        </div>
      `;
    } else {
      let iconSvg = "";
      if (type === "warning") {
        iconSvg = `
          <div class="sr-feedback-icon-badge is-warning">
            <svg class="sr-warn-svg" aria-hidden="true" focusable="false" role="img" width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="10" cy="10" r="7.5"/>
              <line x1="10" y1="6.5" x2="10" y2="10.5"/>
              <circle cx="10" cy="14" r="0.75" fill="currentColor"/>
            </svg>
          </div>`;
      } else if (type === "error") {
        iconSvg = `
          <div class="sr-feedback-icon-badge is-error">
            <svg class="sr-warn-svg" aria-hidden="true" focusable="false" role="img" width="16" height="16" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="10" cy="10" r="7.5"/>
              <line x1="6.5" y1="6.5" x2="13.5" y2="13.5"/>
              <line x1="13.5" y1="6.5" x2="6.5" y2="13.5"/>
            </svg>
          </div>`;
      }

      contentHtml = `
        <div class="sr-feedback-header">
          ${iconSvg}
          <span class="sr-feedback-title">${this.formatInline(title)}</span>
        </div>
        <div class="sr-feedback-body">${formattedBody}</div>
      `;
    }

    card.className = `sr-feedback-card is-visible is-${type}${isCorrect ? " is-success-enhanced" : ""}`;
    card.innerHTML = contentHtml;
  }

  clearConsole(exerciseId) {
    if (!exerciseId) {
      const activeEx = document.querySelector(".social-r-exercise.is-active-exercise");
      exerciseId = activeEx ? activeEx.getAttribute("data-exercise-id") : null;
    }
    if (!exerciseId) return;

    this.lastExecutedCode.delete(exerciseId);

    const transcript = this.getTranscriptElement(exerciseId);
    if (transcript) {
      transcript.innerHTML = "";
    }

    const container = this.getExerciseContainer(exerciseId);
    if (container) {
      const outputs = container.querySelectorAll(".cell-output-container, .cell-output-stdout, .cell-output-stderr, .cell-output, .exercise-cell-output, .callout, .sr-console-prompt");
      outputs.forEach((el) => {
        if (!el.closest(".sr-console-transcript")) {
          el.innerHTML = "";
        }
      });
    }
  }

  reset(exerciseId) {
    this.lastExecutedCode.delete(exerciseId);
    this.lastSubmittedCode.delete(exerciseId);
    this.evaluators.delete(exerciseId);

    const card = this.getEditorCard(exerciseId);
    if (card) {
      const resetBtn = card.querySelector('.btn-exercise-editor.btn-outline-dark, a[aria-label="Start Over"], a[title*="Start Over"]');
      if (resetBtn) {
        resetBtn.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
      }
    }

    const feedbackCard = this.getGradeFeedback(exerciseId);
    if (feedbackCard) {
      feedbackCard.className = "sr-feedback-card";
      feedbackCard.innerHTML = "";
    }

    window.SocialR.events.emit("exercise_reset", { exerciseId });
  }

  getVisibleHintCount(exerciseId) {
    return this.visibleHintCounts.get(exerciseId) || 0;
  }

  toggleHint(exerciseId) {
    // Debounce rapid double-clicks within 60ms
    const now = Date.now();
    if (now - (this._lastHintClickTime || 0) < 60) return null;
    this._lastHintClickTime = now;

    const container = this.getExerciseContainer(exerciseId);
    if (!container) return null;

    const hints = Array.from(container.querySelectorAll(".sr-hint-card"));
    if (hints.length === 0) return null;

    const totalHints = hints.length;
    const currentCount = this.getVisibleHintCount(exerciseId);

    const hintBtn = container.querySelector(".sr-hint-toggle-btn");
    const btnText = hintBtn ? (hintBtn.querySelector(".sr-hint-btn-text") || hintBtn) : null;
    const hintsList = container.querySelector(".sr-hints-list");

    if (currentCount < totalHints) {
      // Reveal the next hint card
      const newCount = currentCount + 1;
      this.visibleHintCounts.set(exerciseId, newCount);
      this.hintOpenState.set(exerciseId, true);

      // Show the newly revealed hint card
      const targetHint = hints[newCount - 1];
      if (targetHint) {
        targetHint.removeAttribute("hidden");
        targetHint.classList.add("is-revealed");
      }

      if (hintsList) {
        hintsList.classList.add("has-revealed");
      }

      // Update button state and text
      if (hintBtn) {
        hintBtn.setAttribute("aria-expanded", "true");
      }
      if (btnText) {
        if (newCount < totalHints) {
          btnText.textContent = "Ver otra pista";
        } else {
          btnText.textContent = totalHints === 1 ? "Ocultar pista" : "Ocultar pistas";
        }
      }

      // Emit event for analytics / instrumentation
      if (window.SocialR && window.SocialR.events) {
        window.SocialR.events.emit("hint_opened", {
          exerciseId,
          hintIndex: newCount,
          totalHints,
        });
      }

      return { current: newCount, total: totalHints, hasMore: newCount < totalHints };
    } else {
      // All hints currently visible -> reset/hide all
      this.resetHints(exerciseId);
      return { current: 0, total: totalHints, hasMore: true };
    }
  }

  revealNextHint(exerciseId) {
    const container = this.getExerciseContainer(exerciseId);
    if (!container) return null;

    const hints = Array.from(container.querySelectorAll(".sr-hint-card"));
    if (hints.length === 0) return null;

    const totalHints = hints.length;
    const currentCount = this.getVisibleHintCount(exerciseId);

    if (currentCount < totalHints) {
      return this.toggleHint(exerciseId);
    }
    return { current: currentCount, total: totalHints, hasMore: false };
  }

  resetHints(exerciseId) {
    this.visibleHintCounts.set(exerciseId, 0);
    this.hintOpenState.set(exerciseId, false);

    const container = this.getExerciseContainer(exerciseId);
    if (!container) return;

    const hints = Array.from(container.querySelectorAll(".sr-hint-card"));
    hints.forEach((hint) => {
      hint.setAttribute("hidden", "");
      hint.classList.remove("is-revealed");
    });

    const hintsList = container.querySelector(".sr-hints-list");
    if (hintsList) {
      hintsList.classList.remove("has-revealed");
    }

    const hintBtn = container.querySelector(".sr-hint-toggle-btn");
    if (hintBtn) {
      hintBtn.setAttribute("aria-expanded", "false");
      const btnText = hintBtn.querySelector(".sr-hint-btn-text") || hintBtn;
      if (btnText) {
        btnText.textContent = "Ver pista";
      }
    }
  }

  resetHintsAll() {
    this.visibleHintCounts.clear();
    this.hintOpenState.clear();
    document.querySelectorAll(".social-r-exercise").forEach((ex) => {
      const exId = ex.getAttribute("data-exercise-id");
      if (exId) {
        this.resetHints(exId);
      }
    });
  }
}

window.QuartoLiveAdapter = QuartoLiveAdapter;

// Canonical Social R Markdown Renderer for all student-facing dynamic copy
window.SocialR = window.SocialR || {};
const _defaultAdapterInstance = new QuartoLiveAdapter();
window.SocialR.renderMarkdown = (text) => _defaultAdapterInstance.parseMarkdownFeedback(text);
window.SocialR.renderInlineMarkdown = (text) => _defaultAdapterInstance.formatInline(text);
