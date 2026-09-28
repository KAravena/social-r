import json
import re
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent


class TestFullPublication(unittest.TestCase):
    """Verifies that Social R full course publication publishes all 13 modules and 89 exercises,
    with 0 standby modules, displaying the complete curriculum with interactive links on the landing page."""

    def setUp(self):
        self.course_yml_path = ROOT / "content" / "courses" / "intro-r" / "course.yml"
        self.course_config_js_path = ROOT / "js" / "platform" / "course-config.js"
        self.modules_dir = ROOT / "content" / "courses" / "intro-r" / "modules"
        self.index_qmd_path = ROOT / "index.qmd"

        self.assertTrue(self.course_yml_path.exists(), "course.yml must exist")
        self.course_data = yaml.safe_load(self.course_yml_path.read_text(encoding="utf-8"))

    def test_course_yml_publication_thresholds(self):
        """course.yml must specify published_through: 13, 89 exercises, and last exercise intro-r-13-005."""
        c = self.course_data
        self.assertEqual(c.get("total_modules"), 13, "Total designed curriculum must be 13 modules")
        self.assertEqual(c.get("total_exercises"), 89, "Total designed exercises must be 89")
        self.assertEqual(c.get("published_through"), 13, "Publication threshold must be 13")
        self.assertEqual(c.get("published_module_count"), 13, "Published module count must be 13")
        self.assertEqual(c.get("published_exercise_count"), 89, "Published exercise count must be 89")
        self.assertEqual(c.get("last_published_exercise_id"), "intro-r-13-005")

        # Verify module statuses: all 13 published, 0 standby
        modules = c.get("modules", [])
        self.assertEqual(len(modules), 13)
        for mod in modules:
            order = mod.get("order")
            status = mod.get("status")
            self.assertEqual(status, "published", f"Module order {order} should be published")

    def test_course_config_js_consistency(self):
        """js/platform/course-config.js must match course.yml full publication state."""
        self.assertTrue(self.course_config_js_path.exists(), "course-config.js must exist")
        content = self.course_config_js_path.read_text(encoding="utf-8")

        self.assertIn("publishedThrough: 13", content)
        self.assertIn("publishedExerciseCount: 89", content)
        self.assertIn('lastPublishedExerciseId: "intro-r-13-005"', content)
        self.assertIn("totalModules: 13", content)
        self.assertIn("totalExercises: 89", content)
        self.assertIn("isModulePublished", content)
        self.assertIn("isExercisePublished", content)
        self.assertIn("isStandbyExercise", content)
        self.assertIn("isStandbyModule", content)
        self.assertIn("isLocalPreview", content)
        self.assertIn("isModuleAvailable", content)
        self.assertIn("isExerciseAvailable", content)
        self.assertIn("getAvailableExerciseCount", content)
        self.assertIn("getAvailableModuleCount", content)
        self.assertIn("getLastAvailableExerciseId", content)

    def test_all_modules_preserved_on_disk(self):
        """All 13 modules must remain 100% intact on disk in content/ and md_finales/."""
        # 1. Check content/courses/intro-r/modules/
        for m_num in range(1, 14):
            matches = list(self.modules_dir.glob(f"{m_num:02d}-*"))
            self.assertTrue(len(matches) > 0, f"Module directory for M{m_num:02d} must exist")
            mod_dir = matches[0]
            self.assertTrue((mod_dir / "module.yml").exists(), f"module.yml for M{m_num:02d} must exist")
            yaml_files = list(mod_dir.rglob("*.yml"))
            self.assertGreaterEqual(len(yaml_files), 6, f"M{m_num:02d} exercises must remain on disk")

        # 2. Check md_finales canonical markdown
        for m_num in range(1, 14):
            locked_md = ROOT / "md_finales" / f"social_r_modulo_{m_num:02d}_diseno_LOCKED.md"
            self.assertTrue(locked_md.exists(), f"Canonical locked MD for M{m_num:02d} must exist")
            self.assertGreater(locked_md.stat().st_size, 10000, f"Canonical locked MD for M{m_num:02d} must have content")

    def test_landing_recorrido_copy_and_accordion(self):
        """index.qmd must display all 13 modules as available with active links for all 89 exercises."""
        content = self.index_qmd_path.read_text(encoding="utf-8")

        # 1. All 13 modules must be present in the accordion
        for m_num in range(1, 14):
            self.assertIn(f'data-module-order="{m_num}"', content)

        # 2. No standby modules
        self.assertNotIn('data-module-status="standby"', content)
        self.assertNotIn('sr-accordion-item--standby', content)
        self.assertNotIn('sr-accordion-header--standby', content)

        # 3. No standby badges
        standby_module_badges = re.findall(r'<span class="sr-module-badge sr-module-badge--standby"', content)
        self.assertEqual(len(standby_module_badges), 0, f"No standby module badges expected, found {len(standby_module_badges)}")
        standby_challenge_badges = re.findall(r'<span class="sr-challenge-badge sr-challenge-badge--standby"', content)
        self.assertEqual(len(standby_challenge_badges), 0, f"No standby challenge badges expected, found {len(standby_challenge_badges)}")

        # 4. Exactly 89 links to exercises across all 13 modules
        published_links = re.findall(r'href="curso\.html#intro-r-(0[1-9]|1[0-3])-[^"]+"', content)
        self.assertEqual(len(published_links), 89, f"All 89 exercises must have links to curso.html, found {len(published_links)}")


if __name__ == "__main__":
    unittest.main()
