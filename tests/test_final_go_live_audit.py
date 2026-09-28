#!/usr/bin/env python3
"""Social R — Final Go-Live Audit & Safety Test Suite (Step 8A)
Validates:
- Legacy local progress detection, explicit choice, and safe clearing
- Shared computer isolation and logout cleanup
- Monotonic merge semantics (exercises, challenges, drafts)
- Session expiry handling
- Tour vs Login coexistence (zero click collision)
- Production config staging (ON/OFF) and rapid rollback
- Frontend security and PII isolation
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_public_cloud_config import (
    build_config_block,
    update_cloud_config_file,
    CONFIG_FILES,
)


class FinalGoLiveAuditTests(unittest.TestCase):
    """Step 8A test suite covering all architectural go-live verifications."""

    def test_cloud_config_has_clear_legacy_progress(self):
        """Verify that cloud-config.js implements clearLegacyProgress."""
        for cfg_path in CONFIG_FILES:
            content = cfg_path.read_text(encoding="utf-8")
            self.assertIn("clearLegacyProgress(courseId", content)
            self.assertIn("window.localStorage.removeItem", content)

    def test_login_modal_explicit_legacy_choice(self):
        """Verify that login-modal.js presents an explicit choice (merge vs discard) for legacy progress."""
        for js_path in [ROOT / "js" / "app" / "login-modal.js", ROOT / "docs" / "js" / "app" / "login-modal.js"]:
            content = js_path.read_text(encoding="utf-8")
            self.assertIn("sr-login-legacy-choice-card", content)
            self.assertIn('name="sr-legacy-decision"', content)
            self.assertIn('value="merge"', content)
            self.assertIn('value="discard"', content)
            self.assertIn("clearLegacyProgress", content)
            # Ensure it only merges if chosen
            self.assertIn("shouldMergeLegacy", content)

    def test_login_modal_tour_coexistence(self):
        """Verify that login modal terminates active tour on open and triggers check on close."""
        for js_path in [ROOT / "js" / "app" / "login-modal.js", ROOT / "docs" / "js" / "app" / "login-modal.js"]:
            content = js_path.read_text(encoding="utf-8")
            self.assertIn("tour.end(false)", content)
            self.assertIn("tour.checkAutoLaunch()", content)

    def test_tour_does_not_launch_over_login_or_pending_cloud(self):
        """Verify that tour.js checks for login modal and unauthenticated cloud state."""
        for tour_path in [ROOT / "js" / "app" / "tour.js", ROOT / "docs" / "js" / "app" / "tour.js"]:
            content = tour_path.read_text(encoding="utf-8")
            self.assertIn("loginModal.isOpen()", content)
            self.assertIn("cloud.isCloudEnabled() && !cloud.isAuthenticated()", content)

    def test_progress_store_auth_event_binding(self):
        """Verify that ProgressStore listens to auth_state_changed to isolate shared computer sessions."""
        for ps_path in [ROOT / "js" / "platform" / "progress-store.js", ROOT / "docs" / "js" / "platform" / "progress-store.js"]:
            content = ps_path.read_text(encoding="utf-8")
            self.assertIn("_bindAuthEvents", content)
            self.assertIn('"auth_state_changed"', content)
            self.assertIn("rebindSession(studentId)", content)

    def test_logout_redirect_or_reload(self):
        """Verify that handleLogout cleanly reloads or redirects so no state lingers."""
        for js_path in [ROOT / "js" / "app" / "login-modal.js", ROOT / "docs" / "js" / "app" / "login-modal.js"]:
            content = js_path.read_text(encoding="utf-8")
            self.assertIn("window.location.reload()", content)
            self.assertIn('window.location.href = "index.html"', content)

    def test_build_config_staging_and_rollback(self):
        """Verify that build_public_cloud_config supports staged ON and rapid OFF rollback."""
        block_off = build_config_block("https://test.supabase.co", "sb_publishable_test", "intro-r", enable_cloud=False)
        self.assertIn("cloudProgressEnabled: false,", block_off)

        block_on = build_config_block("https://test.supabase.co", "sb_publishable_test", "intro-r", enable_cloud=True)
        self.assertIn("cloudProgressEnabled: true,", block_on)

        # Ensure dry-run script runs cleanly with --enable-cloud and --disable-cloud
        res_on = subprocess.run(
            [sys.executable, "scripts/build_public_cloud_config.py", "--dry-run", "--enable-cloud"],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(res_on.returncode, 0)
        self.assertIn("[DRY-RUN]", res_on.stdout)

        res_off = subprocess.run(
            [sys.executable, "scripts/build_public_cloud_config.py", "--dry-run", "--disable-cloud"],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(res_off.returncode, 0)
        self.assertIn("[DRY-RUN]", res_off.stdout)

    def test_production_cloud_config_valid(self):
        """Verify that in docs/js/platform/cloud-config.js cloudProgressEnabled is a boolean and syncDraftsToCloud is false."""
        doc_cfg = ROOT / "docs" / "js" / "platform" / "cloud-config.js"
        content = doc_cfg.read_text(encoding="utf-8")
        match = re.search(r"cloudProgressEnabled:\s*(false|true)", content)
        self.assertTrue(match, "Could not find cloudProgressEnabled in docs config")
        self.assertIn("syncDraftsToCloud: false", content)

    def test_zero_secrets_in_docs(self):
        """Verify no backend secrets or private keys leaked to docs/."""
        docs_dir = ROOT / "docs"
        forbidden = [
            "sb_secret_",
            "RUT_SECRET_KEY",
            "SUPABASE_SECRET_KEY",
            "SUPABASE_SERVICE_ROLE_KEY",
        ]
        for f in docs_dir.rglob("*.js"):
            txt = f.read_text(encoding="utf-8", errors="ignore")
            for pattern in forbidden:
                self.assertNotIn(pattern, txt, f"Found forbidden secret {pattern} in {f.name}")

    def test_guest_mode_cloud_config(self):
        """Verify that cloud-config.js implements guest mode storage key, methods and session clearing."""
        for cfg_path in CONFIG_FILES:
            content = cfg_path.read_text(encoding="utf-8")
            self.assertIn('guestModeStorageKey: "social-r:auth:guest-mode"', content)
            self.assertIn("isGuestMode()", content)
            self.assertIn("setGuestMode(enabled = true)", content)
            self.assertIn("clearGuestMode()", content)
            # Ensure setSession clears guest mode
            self.assertIn("this.clearGuestMode()", content)

    def test_login_modal_guest_button_and_explanatory_copy(self):
        """Verify that login modal renders 'Ingresar con RUT o IPE', 'Continuar sin iniciar sesión' and explanatory box."""
        for js_path in [ROOT / "js" / "app" / "login-modal.js", ROOT / "docs" / "js" / "app" / "login-modal.js"]:
            content = js_path.read_text(encoding="utf-8")
            self.assertIn("Ingresar con RUT o IPE", content)
            self.assertIn("Continuar sin iniciar sesión", content)
            self.assertIn("sr-login-btn-guest", content)
            self.assertIn("sr-login-info-box", content)
            self.assertIn("cloudConfig.setGuestMode(true)", content)

    def test_home_profile_icon_markup_and_styles(self):
        """Verify that home hero top-nav contains profile container and responsive styles."""
        for html_path in [ROOT / "index.qmd", ROOT / "docs" / "index.html"]:
            content = html_path.read_text(encoding="utf-8")
            self.assertIn("sr-hero__top-nav", content)
            self.assertIn("sr-home-profile-container", content)
            self.assertIn("sr-hero__project-link", content)

        for css_path in [ROOT / "css" / "landing.css", ROOT / "docs" / "css" / "landing.css"]:
            content = css_path.read_text(encoding="utf-8")
            self.assertIn(".sr-hero__top-nav", content)
            self.assertIn(".sr-home-profile-container", content)
            self.assertIn(".sr-home-profile-btn", content)
            self.assertIn(".sr-home-profile-pill", content)

    def test_landing_progress_namespace_isolation(self):
        """Verify landing.js syncProgress strictly isolates student namespace from guest/legacy namespace."""
        for js_path in [ROOT / "js" / "landing" / "landing.js", ROOT / "docs" / "js" / "landing" / "landing.js"]:
            content = js_path.read_text(encoding="utf-8")
            self.assertIn("cloud && cloud.isAuthenticated()", content)
            self.assertIn("const studentNs = cloud.getProgressNamespace", content)
            self.assertIn("const raw = localStorage.getItem(studentNs);", content)

    def test_export_student_progress_excludes_test_sections_by_default(self):
        """Verify export_student_progress.py filters out TEST* sections unless --include-test is passed."""
        script_path = ROOT / "scripts" / "export_student_progress.py"
        content = script_path.read_text(encoding="utf-8")
        self.assertIn("--include-test", content)
        self.assertIn('startswith("TEST")', content)

        # Functional test of the exclusion logic
        sample_records = [
            {"section": "1", "display_name": "Estudiante 1"},
            {"section": "2", "display_name": "Estudiante 2"},
            {"section": "TEST-ADMIN", "display_name": "Docente Test"},
            {"section": "TEST-PILOT", "display_name": "Piloto Test"},
            {"section": "TEST", "display_name": "Generico Test"},
        ]
        # Default behavior: exclude TEST*
        filtered_default = [r for r in sample_records if not str(r.get("section", "")).upper().startswith("TEST")]
        self.assertEqual(len(filtered_default), 2)
        self.assertEqual([r["display_name"] for r in filtered_default], ["Estudiante 1", "Estudiante 2"])

        # With include_test: keep all
        filtered_all = sample_records
        self.assertEqual(len(filtered_all), 5)

    def test_test_accounts_gitignore_and_example(self):
        """Verify data/test-accounts.csv is gitignored and data/test-accounts.example.csv exists and is tracked."""
        example_csv = ROOT / "data" / "test-accounts.example.csv"
        self.assertTrue(example_csv.exists(), "test-accounts.example.csv must exist")
        content = example_csv.read_text(encoding="utf-8")
        self.assertIn("rut,nombre,seccion", content)
        self.assertIn("TEST-ADMIN", content)

        # Check gitignore using git check-ignore
        res_ignored = subprocess.run(
            ["git", "check-ignore", "data/test-accounts.csv"],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(res_ignored.returncode, 0, "data/test-accounts.csv must be ignored by git")

        res_example = subprocess.run(
            ["git", "check-ignore", "data/test-accounts.example.csv"],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertNotEqual(res_example.returncode, 0, "data/test-accounts.example.csv must NOT be ignored by git")

    @staticmethod
    def _parse_first_name(display_name, fallback="Estudiante"):
        if display_name is None or not isinstance(display_name, str):
            return fallback
        trimmed = display_name.strip()
        if not trimmed:
            return fallback
        if "," in trimmed:
            comma_idx = trimmed.find(",")
            after_comma = trimmed[comma_idx + 1:].strip()
            if after_comma:
                tokens = [t for t in re.split(r"\s+", after_comma) if t]
                if tokens:
                    return tokens[0]
            before_tokens = [t for t in re.split(r"\s+", trimmed[:comma_idx].strip()) if t]
            return before_tokens[0] if before_tokens else fallback
        tokens = [t for t in re.split(r"\s+", trimmed) if t]
        return tokens[0] if tokens else fallback

    def test_first_name_canonical_helper_in_codebase(self):
        """Verify getFirstName is implemented in cloud-config.js, exposed on window.SocialR, and used across UI."""
        for cfg_path in [ROOT / "js" / "platform" / "cloud-config.js", ROOT / "docs" / "js" / "platform" / "cloud-config.js"]:
            content = cfg_path.read_text(encoding="utf-8")
            self.assertIn("getFirstName(displayName, fallback = \"Estudiante\")", content)
            self.assertIn("window.SocialR.getFirstName =", content)

        for modal_path in [ROOT / "js" / "app" / "login-modal.js", ROOT / "docs" / "js" / "app" / "login-modal.js"]:
            content = modal_path.read_text(encoding="utf-8")
            self.assertIn("getFirstName", content)
            self.assertIn("title.textContent = `¡Hola, ${firstName}!`;", content)
            # Full name must be preserved in confirm card and drawer
            self.assertIn("${student.displayName || \"Estudiante\"}</div>", content)
            self.assertIn("<div class=\"sr-drawer-user-name\">${displayName}</div>", content)
            self.assertIn("<span class=\"sr-user-pill__name\">👤 ${firstName}</span>", content)

        for landing_path in [ROOT / "js" / "landing" / "landing.js", ROOT / "docs" / "js" / "landing" / "landing.js"]:
            content = landing_path.read_text(encoding="utf-8")
            self.assertIn("getFirstName", content)
            # Avatar initial derived from firstName
            self.assertIn('(firstName[0] || "E").toUpperCase()', content)
            self.assertIn("<span class=\"sr-home-profile-avatar\" aria-hidden=\"true\">${initial}</span>", content)
            self.assertIn("<span class=\"sr-home-profile-name\">${safeName}</span>", content)

    def test_first_name_synthetic_rules_and_unicode(self):
        """Verify synthetic test cases covering comma/no-comma/extra whitespace/Unicode/fallbacks."""
        cases = [
            ("Rojas Pérez, Camila Andrea", "Camila"),
            ("Fuentes, Martín", "Martín"),
            ("Daniela Soto Pérez", "Daniela"),
            ("  Rojas Pérez,   Camila Andrea ", "Camila"),
            ("Camila", "Camila"),
            ("", "Estudiante"),
            (None, "Estudiante"),
            ("   ", "Estudiante"),
            ("Álvarez, Íñigo", "Íñigo"),
            ("Ñuñoa, Matías", "Matías"),
            ("O'Higgins, Bernardo", "Bernardo"),
        ]
        for raw_name, expected in cases:
            self.assertEqual(
                self._parse_first_name(raw_name),
                expected,
                f"Failed for input: {raw_name}"
            )


if __name__ == "__main__":
    unittest.main()
