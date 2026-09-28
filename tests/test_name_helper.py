#!/usr/bin/env python3
"""Social R — Name Helper & Presentation Layer Synthetic Test Suite
Validates:
- Canonical getFirstName implementation in cloud-config.js and UI components
- Parsing rules:
  * Case A (institutional with comma): "Apellido1 Apellido2, Nombre1 Nombre2" -> "Nombre1"
  * Case B (conventional without comma): "Nombre1 Nombre2 Apellido1" -> "Nombre1"
  * Case C (extra whitespace): "  Apellido1 Apellido2,   Nombre1 Nombre2  " -> "Nombre1"
  * Case D (empty/null/undefined): fallback ("Estudiante") without errors
  * Unicode and accents preservation: "Álvarez, Íñigo" -> "Íñigo", "Ñuñoa, Matías" -> "Matías"
- E2E Login presentation with synthetic fixture ("Rojas Pérez, Camila Andrea"):
  * Greeting title: "¡Hola, Camila!"
  * Confirmation card: full registered display name preserved intact ("Rojas Pérez, Camila Andrea")
  * Home profile name: "Camila"
  * Home avatar initial: "C"
  * Topbar pill: "👤 Camila"
  * Drawer: full registered display name preserved intact ("Rojas Pérez, Camila Andrea")
"""

import asyncio
import http.server
import re
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'docs'), **kwargs)
    def log_message(self, format, *args):
        pass


class NameHelperSyntheticTests(unittest.TestCase):
    """Synthetic unit tests for the getFirstName helper."""

    @staticmethod
    def parse_first_name(display_name, fallback="Estudiante"):
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

    def test_synthetic_cases(self):
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
        for name_in, expected in cases:
            self.assertEqual(
                self.parse_first_name(name_in),
                expected,
                f"Failed for name: {name_in}"
            )

    def test_e2e_browser_fixture(self):
        """Runs browser evaluation of getFirstName and UI components with synthetic fixture."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest("playwright not installed in environment")

        httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), DocsHTTPHandler)
        port = httpd.server_address[1]
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        base_url = f'http://127.0.0.1:{port}'

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Test on index.html
                page.goto(f"{base_url}/index.html")
                page.wait_for_timeout(500)

                # 1. Direct evaluate of window.SocialR.getFirstName
                cases = [
                    ("Rojas Pérez, Camila Andrea", "Camila"),
                    ("Fuentes, Martín", "Martín"),
                    ("Daniela Soto Pérez", "Daniela"),
                    ("  Rojas Pérez,   Camila Andrea ", "Camila"),
                    ("Camila", "Camila"),
                    ("", "Estudiante"),
                    (None, "Estudiante"),
                    ("Álvarez, Íñigo", "Íñigo"),
                    ("Ñuñoa, Matías", "Matías"),
                ]
                for raw, expected in cases:
                    res = page.evaluate("(val) => window.SocialR.getFirstName(val)", raw)
                    self.assertEqual(res, expected, f"Browser evaluation failed for {raw}")

                # 2. Login modal confirmation step with synthetic fixture
                fixture = {
                    "displayName": "Rojas Pérez, Camila Andrea",
                    "rutMasked": "••.•••.123-4",
                    "studentId": "s-synthetic-001"
                }

                step2_res = page.evaluate("""(student) => {
                    const modal = window.SocialR.loginModal;
                    modal._renderStep2({ student: student });
                    const title = document.querySelector("#sr-login-title").textContent.trim();
                    const confirmName = document.querySelector(".sr-login-confirm-name").textContent.trim();
                    return { title, confirmName };
                }""", fixture)

                # Requirement B: Greeting uses first name
                self.assertEqual(step2_res["title"], "¡Hola, Camila!")
                # Requirement C: Confirmation card preserves full registered display name
                self.assertEqual(step2_res["confirmName"], "Rojas Pérez, Camila Andrea")

                # 3. Home profile and avatar
                home_res = page.evaluate("""(student) => {
                    const cloud = window.SocialR.cloudConfig;
                    cloud.setSession({
                        sessionToken: "dummy-token",
                        student: student
                    });
                    if (typeof window.SocialR.updateProfileControl === "function") {
                        window.SocialR.updateProfileControl();
                    }
                    const profileName = document.querySelector(".sr-home-profile-name") ? document.querySelector(".sr-home-profile-name").textContent.trim() : null;
                    const profileAvatar = document.querySelector(".sr-home-profile-avatar") ? document.querySelector(".sr-home-profile-avatar").textContent.trim() : null;
                    return { profileName, profileAvatar };
                }""", fixture)

                # Requirement D: Home profile name uses first name
                self.assertEqual(home_res["profileName"], "Camila")
                # Requirement E: Home avatar initial is C (first letter of first name)
                self.assertEqual(home_res["profileAvatar"], "C")

                # 4. Topbar and drawer on curso.html
                page.add_init_script("""
                    window.localStorage.setItem('social-r:auth:session', JSON.stringify({
                        sessionToken: 'dummy-token',
                        student: { displayName: 'Rojas Pérez, Camila Andrea', rutMasked: '••.•••.123-4' }
                    }));
                    window.localStorage.setItem('social-r:onboarding', JSON.stringify({ completed: true, version: 1 }));
                """)
                page.goto(f"{base_url}/curso.html")
                page.wait_for_timeout(800)

                curso_res = page.evaluate("""() => {
                    const topbarPill = document.querySelector('.sr-user-pill__name') ? document.querySelector('.sr-user-pill__name').textContent.trim() : null;
                    const drawerName = document.querySelector('.sr-drawer-user-name') ? document.querySelector('.sr-drawer-user-name').textContent.trim() : null;
                    return { topbarPill, drawerName };
                }""")

                # Topbar uses first name
                self.assertIn("Camila", curso_res["topbarPill"])
                self.assertNotIn("Rojas", curso_res["topbarPill"])
                # Drawer preserves full registered display name
                self.assertEqual(curso_res["drawerName"], "Rojas Pérez, Camila Andrea")

                browser.close()
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
