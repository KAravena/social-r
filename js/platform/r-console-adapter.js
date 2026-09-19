/**
 * Social R Platform - R Console Adapter v0.3.5
 * Manages presentation and routing of real R outputs (stdout, stderr, errors, warnings, messages)
 * to the R Console panel in an RStudio/Positron inspired light theme.
 */
class RConsoleAdapter {
  constructor(consoleBodyId = "sr-console-body") {
    this.consoleBodyId = consoleBodyId;
    this.isFirstOutput = true;
  }

  getConsoleBody() {
    return document.getElementById(this.consoleBodyId);
  }

  clearVisualHistory() {
    const body = this.getConsoleBody();
    if (body) {
      body.innerHTML = "";
    }
  }

  scrollToBottom() {
    const body = this.getConsoleBody();
    if (body) {
      body.scrollTop = body.scrollHeight;
    }
  }

  prepareConsole() {
    const body = this.getConsoleBody();
    if (body && this.isFirstOutput) {
      const promptEl = body.querySelector(".sr-console-prompt");
      if (promptEl) {
        promptEl.remove();
      }
      this.isFirstOutput = false;
    }
  }

  appendCommand(code) {
    if (!code) return;
    this.prepareConsole();
    const body = this.getConsoleBody();
    if (!body) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry sr-console-entry-command";

    const codeLines = code.trim().split("\n");
    const formattedCode = codeLines.map((l, i) => (i === 0 ? `> ${l}` : `+ ${l}`)).join("\n");

    entry.innerHTML = `<pre class="sr-console-command"><code>${this.escapeHtml(formattedCode)}</code></pre>`;
    body.appendChild(entry);
    this.scrollToBottom();
  }

  appendOutput(text) {
    if (!text || !text.trim()) return;
    this.prepareConsole();
    const body = this.getConsoleBody();
    if (!body) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry sr-console-entry-output";

    entry.innerHTML = `<pre class="sr-console-output"><code>${this.escapeHtml(text.trim())}</code></pre>`;
    body.appendChild(entry);
    this.scrollToBottom();
  }

  appendError(text) {
    if (!text || !text.trim()) return;
    this.prepareConsole();
    const body = this.getConsoleBody();
    if (!body) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry sr-console-entry-error";

    entry.innerHTML = `<pre class="sr-console-error"><code>${this.escapeHtml(text.trim())}</code></pre>`;
    body.appendChild(entry);
    this.scrollToBottom();
  }

  appendWarning(text) {
    if (!text || !text.trim()) return;
    this.prepareConsole();
    const body = this.getConsoleBody();
    if (!body) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry sr-console-entry-warning";

    entry.innerHTML = `<pre class="sr-console-warning"><code>${this.escapeHtml(text.trim())}</code></pre>`;
    body.appendChild(entry);
    this.scrollToBottom();
  }

  appendMessage(text) {
    if (!text || !text.trim()) return;
    this.prepareConsole();
    const body = this.getConsoleBody();
    if (!body) return;

    const entry = document.createElement("div");
    entry.className = "sr-console-entry sr-console-entry-message";

    entry.innerHTML = `<pre class="sr-console-message"><code>${this.escapeHtml(text.trim())}</code></pre>`;
    body.appendChild(entry);
    this.scrollToBottom();
  }

  processResult(code, stdout, stderr) {
    this.appendCommand(code);

    if (stderr && stderr.trim()) {
      const errStr = stderr.trim();
      if (errStr.toLowerCase().includes("warning")) {
        this.appendWarning(errStr);
      } else if (errStr.toLowerCase().includes("message") || errStr.includes("test-message")) {
        this.appendMessage(errStr);
      } else {
        this.appendError(errStr);
      }
    }

    if (stdout && stdout.trim()) {
      const outStr = stdout.trim();
      if (outStr.startsWith("Warning message:") || outStr.includes("Warning:")) {
        this.appendWarning(outStr);
      } else {
        this.appendOutput(outStr);
      }
    }
  }

  escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}

window.RConsoleAdapter = RConsoleAdapter;
