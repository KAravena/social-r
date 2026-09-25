import json
import re
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent


class TestPartialPublication(unittest.TestCase):
    """Verifies that Social R partial publication adheres strictly to the configuration,
    preserving M06-M13 in standby while publishing M01-M05 and displaying full curriculum
    on the landing page with 'En preparación' previews."""

    def setUp(self):
        self.course_yml_path = ROOT / "content" / "courses" / "intro-r" / "course.yml"
        self.course_config_js_path = ROOT / "js" / "platform" / "course-config.js"
        self.modules_dir = ROOT / "content" / "courses" / "intro-r" / "modules"
        self.index_qmd_path = ROOT / "index.qmd"

        self.assertTrue(self.course_yml_path.exists(), "course.yml must exist")
        self.course_data = yaml.safe_load(self.course_yml_path.read_text(encoding="utf-8"))

    def test_course_yml_publication_thresholds(self):
        """course.yml must specify published_through: 5, 36 exercises, and last exercise intro-r-05-008."""
        c = self.course_data
        self.assertEqual(c.get("total_modules"), 13, "Total designed curriculum must be 13 modules")
        self.assertEqual(c.get("total_exercises"), 89, "Total designed exercises must be 89")
        self.assertEqual(c.get("published_through"), 5, "Publication threshold must be 5")
        self.assertEqual(c.get("published_module_count"), 5, "Published module count must be 5")
        self.assertEqual(c.get("published_exercise_count"), 36, "Published exercise count must be 36")
        self.assertEqual(c.get("last_published_exercise_id"), "intro-r-05-008")

        # Verify module statuses
        modules = c.get("modules", [])
        self.assertEqual(len(modules), 13)
        for mod in modules:
            order = mod.get("order")
            status = mod.get("status")
            if order <= 5:
                self.assertEqual(status, "published", f"Module order {order} should be published")
            else:
                self.assertEqual(status, "standby", f"Module order {order} should be standby")

    def test_course_config_js_consistency(self):
        """js/platform/course-config.js must match course.yml publication state."""
        self.assertTrue(self.course_config_js_path.exists(), "course-config.js must exist")
        content = self.course_config_js_path.read_text(encoding="utf-8")

        self.assertIn("publishedThrough: 5", content)
        self.assertIn("publishedExerciseCount: 36", content)
        self.assertIn('lastPublishedExerciseId: "intro-r-05-008"', content)
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

    def test_standby_modules_preserved_on_disk(self):
        """Modules 06 to 13 must remain 100% intact on disk in content/ and md_finales/."""
        # 1. Check content/courses/intro-r/modules/
        for m_num in range(6, 14):
            matches = list(self.modules_dir.glob(f"{m_num:02d}-*"))
            self.assertTrue(len(matches) > 0, f"Module directory for M{m_num:02d} must exist")
            mod_dir = matches[0]
            self.assertTrue((mod_dir / "module.yml").exists(), f"module.yml for M{m_num:02d} must exist")
            yaml_files = list(mod_dir.rglob("*.yml"))
            self.assertGreaterEqual(len(yaml_files), 6, f"M{m_num:02d} exercises must remain on disk")

        # 2. Check md_finales canonical markdown
        for m_num in range(6, 14):
            locked_md = ROOT / "md_finales" / f"social_r_modulo_{m_num:02d}_diseno_LOCKED.md"
            self.assertTrue(locked_md.exists(), f"Canonical locked MD for M{m_num:02d} must exist")
            self.assertGreater(locked_md.stat().st_size, 10000, f"Canonical locked MD for M{m_num:02d} must have content")

    def test_landing_recorrido_copy_and_accordion(self):
        """index.qmd must display the official copy, 13 modules (5 published, 8 standby), and 0 links to M06-M13."""
        content = self.index_qmd_path.read_text(encoding="utf-8")

        expected_subtitle = "5 módulos disponibles ahora. Los siguientes están en preparación."
        self.assertIn(expected_subtitle, content)

        # 1. All 13 modules must be present in the accordion
        for m_num in range(1, 14):
            self.assertIn(f'data-module-order="{m_num}"', content)

        # 2. Modules 6..13 must have data-module-status="standby"
        for m_num in range(6, 14):
            pattern = rf'data-module-order="{m_num}"[^>]*data-module-status="standby"|data-module-status="standby"[^>]*data-module-order="{m_num}"'
            self.assertTrue(bool(re.search(pattern, content)), f"Module order {m_num} must have data-module-status='standby'")

        # 3. Badges for standby must be 'En preparación'
        standby_badges = re.findall(r'En preparación', content)
        self.assertEqual(len(standby_badges), 8, f"Exactly 8 'En preparación' badges expected, found {len(standby_badges)}")

        # 4. Zero href links to M06-M13
        standby_links = re.findall(r'href="curso\.html#intro-r-(0[6-9]|1[0-3])-[^"]+"', content)
        self.assertEqual(len(standby_links), 0, f"Standby exercises must NOT have links to curso.html, found {len(standby_links)}")

        # 5. Exactly 36 links to M01-M05
        published_links = re.findall(r'href="curso\.html#intro-r-(0[1-5])-[^"]+"', content)
        self.assertEqual(len(published_links), 36, f"Published exercises must have exactly 36 links, found {len(published_links)}")


if __name__ == "__main__":
    unittest.main()
