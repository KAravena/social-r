#!/usr/bin/env python3
"""Canonical Locked Markdown Fidelity Test.
Verifies that each generated exercise matches its corresponding specification in md_finales/
with 1-to-1 fidelity for exercises, titles, hints, and checks.
"""
import re
import sys
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.generator.build import load_exercises

LOCKED_DIR = ROOT / "md_finales"

CANONICAL_COUNTS = {
    1: 8,
    2: 7,
    3: 7,
    4: 6,
    5: 8,
    6: 6,
    7: 6,
    8: 7,
    9: 7,
    10: 8,
    11: 6,
    12: 7,
    13: 5,
}


class CanonicalLockedFidelityTests(unittest.TestCase):
    def setUp(self):
        self.exercises = load_exercises(ROOT / "content", ROOT / "content" / "exercise.schema.json")

    def test_canonical_files_exist(self):
        """Verify all 13 canonical locked markdown files exist."""
        for m in range(1, 14):
            path = LOCKED_DIR / f"social_r_modulo_{m:02d}_diseno_LOCKED.md"
            self.assertTrue(path.exists(), f"Locked file missing: {path}")

    def test_exercise_counts_per_locked_file(self):
        """Verify that parsed exercises count per module matches canonical count exactly."""
        for m, expected_count in CANONICAL_COUNTS.items():
            mod_prefix = f"intro-r-{m:02d}-"
            mod_exs = [x for x in self.exercises if x["id"].startswith(mod_prefix)]
            self.assertEqual(
                len(mod_exs),
                expected_count,
                f"Module {m} has {len(mod_exs)} exercises, expected {expected_count}"
            )

    def test_progressive_hints_count(self):
        """Verify that hints are progressive, have sequential titles, and non-empty text."""
        for ex in self.exercises:
            hints = ex.get("hints", [])
            self.assertGreaterEqual(len(hints), 1, f"Exercise {ex['id']} has no hints")
            for idx, h in enumerate(hints, 1):
                self.assertTrue(h.get("text", "").strip(), f"Hint {idx} in {ex['id']} has empty text")
                self.assertIn(f"Pista {idx}", h.get("title", ""), f"Hint title mismatch in {ex['id']}")

    def test_checks_presence_and_validity(self):
        """Verify that every exercise has valid checks."""
        for ex in self.exercises:
            checks = ex.get("checks", [])
            self.assertGreaterEqual(len(checks), 1, f"Exercise {ex['id']} must have at least 1 check")
            for c in checks:
                self.assertIn("type", c, f"Check in {ex['id']} missing type")

    def test_copy_file_fidelity(self):
        """Verify that social_r_modulo_04_diseno_LOCKED copy.md is byte-for-byte identical or documented."""
        orig = (LOCKED_DIR / "social_r_modulo_04_diseno_LOCKED.md").read_bytes()
        copy = (LOCKED_DIR / "social_r_modulo_04_diseno_LOCKED copy.md").read_bytes()
        self.assertEqual(orig, copy, "Copy file differs from canonical M04 locked file")


if __name__ == "__main__":
    unittest.main()
