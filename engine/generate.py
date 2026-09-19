#!/usr/bin/env python3
"""Convenience entrypoint delegating to engine.generator.build."""
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from engine.generator.build import main, load_exercises, grader_code, render_exercise, render_hint, build_document, r_literal

if __name__ == "__main__":
    main()
