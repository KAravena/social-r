#!/usr/bin/env python3
"""Automated unit test suite for Social R generator and evaluation engine across all 13 modules."""
import subprocess
import sys
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.generator.build import (
    load_exercises,
    grader_code,
    render_exercise,
    render_hint,
    build_document,
    r_literal,
)


class SocialREngineTests(unittest.TestCase):
    def setUp(self):
        self.content_dir = ROOT / "content"
        self.schema_path = ROOT / "content" / "exercise.schema.json"
        self.exercises = load_exercises(self.content_dir, self.schema_path)

    def test_all_88_exercises_loaded_and_unique_ids(self):
        """Verify all 89 exercises across 13 modules are loaded with unique IDs and canonical order."""
        self.assertEqual(len(self.exercises), 89, f"Expected 89 exercises, found {len(self.exercises)}")
        ids = [x["id"] for x in self.exercises]
        self.assertEqual(len(set(ids)), 89, "All 89 exercise IDs must be strictly unique")

        # Verify module counts
        expected_counts = {
            "01-empezar-a-pensar-con-r": 8,
            "02-trabajar-con-varios-valores": 7,
            "03-hacer-preguntas-a-los-datos": 7,
            "04-entender-una-base-de-datos": 6,
            "05-seleccionar-y-filtrar-datos": 8,
            "06-trabajar-cuando-faltan-datos": 7,
            "07-describir-categorias": 6,
            "08-describir-cantidades": 7,
            "09-ver-relaciones-entre-dos-cantidades": 7,
            "10-elegir-y-evaluar-una-correlacion": 8,
            "11-trabajar-con-varias-correlaciones": 6,
            "12-relacionar-categorias": 7,
            "13-de-la-pregunta-al-analisis": 5,
        }

        actual_counts = {}
        for ex in self.exercises:
            mid = ex.get("_module_id")
            actual_counts[mid] = actual_counts.get(mid, 0) + 1

        self.assertEqual(actual_counts, expected_counts, f"Module exercise counts must match canonical locked counts: {expected_counts}")

    def test_pedagogical_metadata(self):
        """Verify that learning objectives (r, data, social) are present in all 88 exercises."""
        for ex in self.exercises:
            self.assertIn("learning_objectives", ex, f"Exercise {ex['id']} missing learning_objectives")
            objs = ex["learning_objectives"]
            self.assertIn("r", objs, f"Exercise {ex['id']} missing r objective")
            self.assertIn("data", objs, f"Exercise {ex['id']} missing data objective")
            self.assertIn("social", objs, f"Exercise {ex['id']} missing social objective")

    def test_progressive_hints_structure(self):
        """Verify all exercises have at least 1 hint and all hints have non-empty text."""
        for ex in self.exercises:
            hints = ex.get("hints", [])
            self.assertGreater(len(hints), 0, f"Exercise {ex['id']} must have at least 1 hint")
            for h in hints:
                self.assertTrue(h.get("text", "").strip(), f"Exercise {ex['id']} has empty hint text")

    def test_clean_titles(self):
        """Verify that no exercise titles retain prefixes like 'E1 —' or 'M1-E1 —'."""
        import re
        for ex in self.exercises:
            title = ex.get("title", "")
            self.assertFalse(bool(re.match(r"^(?:M\d+[-_])?E\d+\b", title)), f"Title '{title}' in {ex['id']} starts with exercise prefix")
            self.assertFalse("—" in title and any(p in title for p in ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"]),
                             f"Title '{title}' in {ex['id']} contains raw exercise prefix")

    def test_document_builder_quarto_live_all_exercises(self):
        """Verify generated document contains required Quarto Live directives and all 88 exercises."""
        qmd = build_document(self.exercises)
        self.assertIn("live-html:", qmd)
        self.assertIn("webr:", qmd)
        self.assertIn("persist: true", qmd)
        self.assertIn("js/social-r.js", qmd)
        self.assertIn("css/social-r.css", qmd)

        # Check all 88 exercises are embedded with fenced divs
        for ex in self.exercises:
            self.assertIn(f'#| exercise: {ex["id"]}', qmd)
            self.assertIn(f'#ex-{ex["id"]}', qmd)

    def test_single_editor_and_single_check_cell_per_exercise(self):
        """Verify exactly 1 student editor cell and 1 check: true cell per exercise for all 88 exercises."""
        qmd = build_document(self.exercises)
        blocks = qmd.split("```{webr}")
        student_counts = {}
        check_counts = {}

        for b in blocks[1:]:
            header = b.split("```")[0]
            for ex in self.exercises:
                ex_id = ex["id"]
                if f"exercise: {ex_id}" in header:
                    if "check: true" in header:
                        check_counts[ex_id] = check_counts.get(ex_id, 0) + 1
                    elif "setup: true" not in header:
                        student_counts[ex_id] = student_counts.get(ex_id, 0) + 1

        for ex in self.exercises:
            ex_id = ex["id"]
            self.assertEqual(student_counts.get(ex_id, 0), 1, f"Exercise {ex_id} must have exactly 1 student editor cell")
            self.assertEqual(check_counts.get(ex_id, 0), 1, f"Exercise {ex_id} must have exactly 1 check cell")

    def test_semantic_fenced_divs_no_raw_html_wrapping_chunks(self):
        """Verify QMD uses semantic fenced divs (:::) and no raw <div> tags wrap code chunks."""
        qmd = build_document(self.exercises)
        self.assertIn("::: {.sr-lesson-panel}", qmd)
        self.assertIn("::: {.sr-editor-body}", qmd)
        self.assertIn("::: {.sr-actions-bar}", qmd)
        self.assertNotIn('<div class="sr-lesson-content">', qmd)
        self.assertNotIn('<div class="sr-editor-body">', qmd)
        self.assertNotIn('<div class="sr-editor-panel">', qmd)
        self.assertNotIn('<div class="sr-coding-panel">', qmd)
        self.assertNotIn('<div class="sr-task-section">', qmd)


if __name__ == "__main__":
    unittest.main()
