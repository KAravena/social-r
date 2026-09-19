#!/usr/bin/env python3
"""Integrated verification script for Social R v0.1."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("$", " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, text=True)
    if p.returncode != 0:
        print(f"FAILED: {' '.join(cmd)} exited with code {p.returncode}")
        sys.exit(p.returncode)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=== Social R v0.1: Verificacion Integral ===")
    # 1. Validate exercises schema
    run([sys.executable, "engine/generator/build.py", "--validate"])

    # 2. Generate index.qmd
    run([sys.executable, "engine/generator/build.py"])

    # 3. Run unit tests
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

    # 4. Check Quarto CLI
    if not shutil.which("quarto"):
        print("\nBLOCKED: Quarto CLI is not installed in this environment.")
        sys.exit(2)
    run(["quarto", "check"])

    # 5. Check Quarto Live extension
    ext = ROOT / "_extensions" / "r-wasm" / "live"
    if not ext.exists():
        print("\nBLOCKED: Quarto Live extension is missing in _extensions/r-wasm/live.")
        print("Run: quarto add r-wasm/quarto-live --no-prompt")
        sys.exit(3)

    # 6. Render Quarto site
    run(["quarto", "render"])

    # 7. Check rendered output
    output = ROOT / "_site" / "index.html"
    if not output.exists():
        print("Render succeeded but _site/index.html is missing", file=sys.stderr)
        sys.exit(4)

    html = output.read_text(encoding="utf-8", errors="ignore")
    required_ids = [
        "intro-r-01-001", "intro-r-01-002", "intro-r-01-003", "intro-r-01-004",
        "intro-r-01-005", "intro-r-01-006", "intro-r-01-007", "intro-r-01-008"
    ]
    for req in required_ids:
        if req not in html:
            print(f"Rendered HTML does not contain exercise ID: {req}", file=sys.stderr)
            sys.exit(5)

    print("\n[PASS] Validacion de fuentes, schema, generacion, tests y Quarto render completados con exito.")
    print("Para iniciar el servidor interactivo:")
    print("  quarto preview")


if __name__ == "__main__":
    main()
