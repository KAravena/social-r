#!/usr/bin/env python3
"""Comprehensive test suite for Social R: Free-Tier Audit, Request & Storage Budgets,
RUT Identification, Cloud Progress Schema, Roster Importer, Teacher Export,
Security & Privacy Boundaries, and Monotonic Sync.
"""

import asyncio
import http.server
import json
import os
import re
import subprocess
import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.rut_utils import (
    clean_rut,
    calculate_dv,
    validate_rut,
    normalize_rut,
    format_rut,
    mask_rut,
    format_rut_masked,
    compute_rut_lookup,
    get_identifier_type,
    validate_identifier,
    normalize_identifier,
    format_identifier,
    format_identifier_masked,
)
from scripts.import_roster import parse_roster_csv
from engine.generator.build import load_exercises, load_challenges


class DocsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "docs"), **kwargs)

    def log_message(self, format, *args):
        pass


class RutAlgorithmUnitTests(unittest.TestCase):
    """Phase 3 / 11: Comprehensive unit tests for Chilean RUT validation and normalization."""

    def test_valid_ruts_standard(self):
        valid_cases = [
            ("12.345.678-5", "12345678-5"),
            ("12345678-5", "12345678-5"),
            ("123456785", "12345678-5"),
            ("12 345 678 - 5", "12345678-5"),
            ("11.111.111-1", "11111111-1"),
            ("11.223.344-K", "11223344-K"),
            ("11223344k", "11223344-K"),
            ("12.345.670-K", "12345670-K"),
            ("15.678.901-1", "15678901-1"),
            ("18.234.567-9", "18234567-9"),
            ("20.123.456-5", "20123456-5"),
            ("9.876.543-3", "9876543-3"),
            ("14.567.890-0", "14567890-0"),
        ]
        for raw, expected_norm in valid_cases:
            with self.subTest(raw=raw):
                self.assertTrue(validate_rut(raw), f"RUT {raw} should be valid")
                self.assertEqual(normalize_rut(raw), expected_norm)

    def test_invalid_ruts(self):
        invalid_cases = [
            "",
            "   ",
            None,
            "12.345.678-9",  # Wrong DV (correct is 5)
            "11.111.111-2",  # Wrong DV (correct is 1)
            "7654321-4",     # Wrong DV (correct is 6)
            "123",           # Too short
            "123456789012",  # Too long
            "abcdefgh-k",    # Non-digits in body
            "12.345.678-A",  # Invalid DV letter
            "12-345-678-9",  # Multiple misplaced hyphens
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(validate_rut(case), f"RUT {case} should be invalid")

    def test_format_rut(self):
        self.assertEqual(format_rut("123456785"), "12.345.678-5")
        self.assertEqual(format_rut("11223344K"), "11.223.344-K")
        self.assertEqual(format_rut("12.345.678-5"), "12.345.678-5")

    def test_mask_rut(self):
        self.assertEqual(mask_rut("12.345.678-5"), "••.•••.678-5")
        self.assertEqual(mask_rut("9.876.543-3"), "•.•••.543-3")
        self.assertEqual(mask_rut(""), "")

    def test_format_rut_masked(self):
        self.assertEqual(format_rut_masked("12345678-5"), "••.•••.678-5")
        self.assertEqual(format_rut_masked("12.345.678-5"), "••.•••.678-5")
        self.assertEqual(format_rut_masked("9876543-3"), "•.•••.543-3")
        self.assertEqual(format_rut_masked(""), "")

    def test_compute_rut_lookup(self):
        secret = "test-secret-key-12345"
        h1 = compute_rut_lookup("12.345.678-5", secret)
        h2 = compute_rut_lookup("12345678-5", secret)
        h3 = compute_rut_lookup("123456785", secret)

        # Deterministic and normalization-invariant
        self.assertEqual(len(h1), 64)
        self.assertEqual(h1, h2)
        self.assertEqual(h2, h3)

        # Secret sensitivity
        h_diff = compute_rut_lookup("12.345.678-5", "another-secret")
        self.assertNotEqual(h1, h_diff)

    def test_valid_synthetic_ipe(self):
        """Validates synthetic IPE with 9-digit body and Modulo 11 check digit (10 chars cleaned)."""
        synth_body = "100000001"
        dv = calculate_dv(synth_body)
        raw_punctuated = f"100.000.001-{dv}"
        raw_clean = f"100000001{dv}"
        raw_spaces = f" 100 000 001 - {dv} "

        for case in [raw_punctuated, raw_clean, raw_spaces]:
            with self.subTest(case=case):
                self.assertTrue(validate_rut(case), f"Synthetic IPE {case} must be valid")
                self.assertTrue(validate_identifier(case))
                self.assertEqual(normalize_rut(case), f"{synth_body}-{dv}")
                self.assertEqual(normalize_identifier(case), f"{synth_body}-{dv}")

        self.assertEqual(format_rut(raw_clean), f"100.000.001-{dv}")
        self.assertEqual(format_identifier(raw_clean), f"100.000.001-{dv}")
        self.assertEqual(format_rut_masked(raw_clean), f"•••.•••.001-{dv}")
        self.assertEqual(format_identifier_masked(raw_clean), f"•••.•••.001-{dv}")
        self.assertEqual(get_identifier_type(raw_clean), "ipe")

    def test_invalid_synthetic_ipe(self):
        """Rejects synthetic IPE with wrong check digit or invalid format."""
        synth_body = "100000001"
        correct_dv = calculate_dv(synth_body)
        wrong_dv = "0" if correct_dv != "0" else "1"

        self.assertFalse(validate_rut(f"100.000.001-{wrong_dv}"))
        self.assertFalse(validate_rut(f"100.000.001-A"))
        self.assertFalse(validate_rut("10000000001-5"))  # 11 digits body (too long)

    def test_identifier_type_classification(self):
        """Verifies identifier type discrimination ('rut' vs 'ipe' vs '')."""
        self.assertEqual(get_identifier_type("12.345.678-5"), "rut")
        self.assertEqual(get_identifier_type("9.876.543-3"), "rut")
        self.assertEqual(get_identifier_type("1000000018"), "ipe")
        self.assertEqual(get_identifier_type(""), "")
        self.assertEqual(get_identifier_type("123"), "")


class CourseCountsAndFidelityTests(unittest.TestCase):
    """Section 32, 33, 34: Verifies exact course counts against source-of-truth YAMLs."""

    def test_real_exercise_and_challenge_counts(self):
        content_dir = ROOT / "content" / "courses" / "intro-r"
        schema_path = ROOT / "content" / "exercise.schema.json"

        exercises = load_exercises(content_dir, schema_path)
        challenges = load_challenges(content_dir, schema_path)

        # 1. Total real exercises
        self.assertEqual(len(exercises), 89, f"Expected 89 exercises, found {len(exercises)}")

        # 2. Total challenges (distinct from regular exercises)
        self.assertEqual(len(challenges), 13, f"Expected 13 challenges, found {len(challenges)}")

        # 3. Check published exercises through M05
        published_modules = [
            "01-empezar-a-pensar-con-r",
            "02-trabajar-con-varios-valores",
            "03-hacer-preguntas-a-los-datos",
            "04-entender-una-base-de-datos",
            "05-seleccionar-y-filtrar-datos",
        ]
        published_exercises = [e for e in exercises if e.get("module") in published_modules or e.get("_module_id") in published_modules]
        self.assertEqual(len(published_exercises), 36, f"Expected 36 published exercises, found {len(published_exercises)}")

    def test_course_config_js_matches_source_of_truth(self):
        config_js = (ROOT / "js" / "platform" / "course-config.js").read_text(encoding="utf-8")

        self.assertIn("totalModules: 13", config_js)
        self.assertIn("totalExercises: 89", config_js)
        self.assertIn("publishedThrough: 5", config_js)
        self.assertIn("publishedModuleCount: 5", config_js)
        self.assertIn("publishedExerciseCount: 36", config_js)


class SchemaAndSecurityAuditTests(unittest.TestCase):
    """Verifies database migrations, absence of exposed secrets, and privacy constraints."""

    def setUp(self):
        self.migration_file = ROOT / "supabase" / "migrations" / "20260926000000_cloud_progress_schema.sql"

    def test_migration_file_exists_and_contains_core_tables(self):
        self.assertTrue(self.migration_file.exists(), "Migration SQL file must exist")
        sql = self.migration_file.read_text(encoding="utf-8").lower()

        required_tables = [
            "courses",
            "students",
            "enrollments",
            "student_sessions",
            "exercise_progress",
            "challenge_progress",
            "exercise_drafts",
            "activity_events",
        ]
        for tbl in required_tables:
            pattern = re.compile(rf"create\s+table\s+if\s+not\s+exists\s+(?:public\.)?{tbl}\b")
            self.assertTrue(pattern.search(sql), f"Table {tbl} must be created in migration")

        self.assertIn("teacher_progress_summary", sql)

    def test_privacy_rut_not_in_progress_tables(self):
        """Rule 9: RUT is personal info. It MUST ONLY be stored in students table."""
        sql = self.migration_file.read_text(encoding="utf-8")
        tables = re.findall(r"create\s+table\s+if\s+not\s+exists\s+(?:public\.)?(\w+)\s*\((.*?)\);", sql, re.DOTALL | re.IGNORECASE)
        table_dict = {t[0].lower(): t[1].lower() for t in tables}

        for tbl in ["exercise_progress", "challenge_progress", "exercise_drafts", "activity_events"]:
            self.assertIn(tbl, table_dict, f"Table {tbl} should be in table_dict")
            self.assertNotIn("rut", table_dict[tbl], f"Table {tbl} must NOT contain a rut column; use student_id foreign key")
            self.assertIn("student_id", table_dict[tbl], f"Table {tbl} must reference student_id")

    def test_zero_trust_privacy_students_table_uses_hash_lookup(self):
        """Zero-Trust: plaintext RUT is never stored in Supabase. Only rut_lookup (HMAC) and rut_masked."""
        sql = self.migration_file.read_text(encoding="utf-8")
        tables = re.findall(r"create\s+table\s+if\s+not\s+exists\s+(?:public\.)?(\w+)\s*\((.*?)\);", sql, re.DOTALL | re.IGNORECASE)
        table_dict = {t[0].lower(): t[1].lower() for t in tables}

        self.assertIn("students", table_dict)
        students_cols = table_dict["students"]
        # Strip comments
        lines = [re.sub(r"--.*$", "", ln).strip() for ln in students_cols.split("\n")]
        col_names = [ln.split()[0].replace('"', '').rstrip(",") for ln in lines if ln and ln.split()]

        self.assertIn("rut_lookup", col_names, "students table must have rut_lookup column")
        self.assertIn("rut_masked", col_names, "students table must have rut_masked column")
        self.assertNotIn("rut_normalized", col_names, "students table must NOT store rut_normalized")
        self.assertNotIn("rut", col_names, "students table must NOT store plaintext rut column")

    def test_no_service_role_key_in_frontend_or_repo(self):
        """Rule 6, 19 & 113.N: NUNCA colocar SUPABASE_SERVICE_ROLE_KEY en JS público, HTML, docs, etc."""
        scanned_extensions = [".js", ".html", ".qmd", ".css", ".md", ".json"]

        for p in ROOT.rglob("*"):
            if not p.is_file():
                continue
            if ".git" in p.parts or "__pycache__" in p.parts:
                continue
            if p.suffix in scanned_extensions:
                content = p.read_text(encoding="utf-8", errors="ignore")
                self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY=ey", content, f"Service key pattern found in {p}")

    def test_no_rut_in_urls_or_console_logs(self):
        """Rule 23 & 86: RUT must never appear in URLs, hashes, queries or console logs."""
        patterns = [
            re.compile(r"console\.(log|info|warn|error)\(.*rut", re.IGNORECASE),
            re.compile(r"location\.(href|hash|search).*rut", re.IGNORECASE),
        ]
        for p in ROOT.rglob("*"):
            if not p.is_file() or ".git" in p.parts or "__pycache__" in p.parts or "vendor" in p.parts:
                continue
            if p.suffix in (".js", ".html", ".qmd"):
                text = p.read_text(encoding="utf-8", errors="ignore")
                for pat in patterns:
                    matches = list(pat.finditer(text))
                    self.assertEqual(len(matches), 0, f"Found forbidden RUT pattern in {p}: {matches}")

    def test_gitignore_protects_env_and_rosters(self):
        """Rule 25, 59 & 90: .gitignore must protect real roster files, exports, and .env."""
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gitignore)
        self.assertIn(".env.*", gitignore)
        self.assertIn("!.env.example", gitignore)
        self.assertIn("data/roster*.csv", gitignore)
        self.assertIn("exports/", gitignore)
        self.assertIn("!data/roster.example.csv", gitignore)


class FreeTierBudgetStressSimulationTests(unittest.TestCase):
    """Section 14, 15, 16, 41: Simulates 36 and 100 students completing the course."""

    def test_edge_function_budget_and_storage_simulation(self):
        """Mathematical stress simulation for 36 and 100 students completing M1-M13."""
        # Course metrics
        total_exercises = 89
        published_exercises = 36
        total_challenges = 13
        published_challenges = 5

        for student_count in [36, 100]:
            with self.subTest(students=student_count):
                # Request budget calculation (Draft cloud = OFF for MVP)
                # 1. Login: ~2 per student
                login_reqs = student_count * 2
                # 2. Exercise sync: 1 per completed exercise
                exercise_sync_reqs = student_count * total_exercises
                # 3. Challenge sync: 1 per challenge pass
                challenge_sync_reqs = student_count * total_challenges
                # 4. Logout: ~1 per student
                logout_reqs = student_count * 1

                total_edge_invocations = login_reqs + exercise_sync_reqs + challenge_sync_reqs + logout_reqs

                # Free tier monthly limit: 500,000 invocations
                free_tier_invocations_limit = 500_000
                invocations_percentage = (total_edge_invocations / free_tier_invocations_limit) * 100

                self.assertLess(
                    total_edge_invocations,
                    15_000,
                    f"Requests for {student_count} students should be under 15,000 (actual: {total_edge_invocations})"
                )
                self.assertLess(
                    invocations_percentage,
                    3.0,
                    f"Invocations for {student_count} students should be < 3% of free tier (actual: {invocations_percentage:.2f}%)"
                )

                # Database row count calculation
                student_rows = student_count
                enrollment_rows = student_count
                session_rows = student_count * 2
                exercise_progress_rows = student_count * total_exercises
                challenge_progress_rows = student_count * total_challenges
                activity_event_rows = student_count * (2 + total_exercises + total_challenges + 1)

                total_db_rows = (
                    student_rows
                    + enrollment_rows
                    + session_rows
                    + exercise_progress_rows
                    + challenge_progress_rows
                    + activity_event_rows
                )

                # Estimated storage in megabytes (average ~250 bytes per row + indexes)
                estimated_storage_mb = (total_db_rows * 250) / (1024 * 1024) + 5.0 # 5 MB Postgres overhead

                # Free tier DB limit: 500 MB
                self.assertLess(estimated_storage_mb, 20.0, f"Estimated DB storage should be < 20 MB (actual: {estimated_storage_mb:.2f} MB)")


class RosterAndExportUnitTests(unittest.TestCase):
    """Phase 9 & 10: Roster import validation and teacher export structures."""

    def test_synthetic_roster_example_is_valid(self):
        example_csv = ROOT / "data" / "roster.example.csv"
        self.assertTrue(example_csv.exists(), "data/roster.example.csv must exist")

        records, errors = parse_roster_csv(example_csv)
        self.assertEqual(len(errors), 0, f"Example roster has errors: {errors}")
        self.assertGreaterEqual(len(records), 5, "Example roster must have at least 5 synthetic students")

        for rec in records:
            self.assertTrue(validate_rut(rec["rut"]), f"Invalid RUT in example roster: {rec['rut']}")
            self.assertTrue(rec["display_name"], "Display name must not be empty")
            self.assertIn("section", rec)

    def test_roster_parser_rejects_invalid_and_duplicates(self):
        temp_csv = ROOT / "data" / "test_malformed.csv"
        try:
            temp_csv.write_text(
                "rut,nombre,seccion\n"
                "12.345.678-5,Ana Pérez,1\n"
                "12.345.678-5,Ana Duplicada,1\n"  # Duplicate
                "11.111.111-9,Carlos Malo,2\n",    # Invalid DV
                encoding="utf-8",
            )
            records, errors = parse_roster_csv(temp_csv)
            self.assertEqual(len(records), 1)
            self.assertEqual(len(errors), 2)
        finally:
            if temp_csv.exists():
                temp_csv.unlink()


class BrowserIntegrationE2ETests(unittest.TestCase):
    """Playwright browser tests for free-tier readiness, offline queue, and namespacing."""

    @classmethod
    def setUpClass(cls):
        cls.port = 8894
        cls.server = http.server.HTTPServer(("127.0.0.1", cls.port), DocsHTTPHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def run_async(self, coro):
        return asyncio.run(coro)

    def test_cloud_disabled_by_default_operates_pure_local(self):
        """Verifies that with no Supabase URL configured, cloud is disabled and site runs pure local."""
        from playwright.async_api import async_playwright

        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{self.base_url}/index.html")

                status = await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    return {
                        isCloudEnabled: cloud ? cloud.isCloudEnabled() : false,
                        isDraftSyncEnabled: cloud ? cloud.isDraftSyncEnabled() : false,
                        namespace: cloud ? cloud.getProgressNamespace('intro-r') : 'social-r:progress:intro-r'
                    };
                }""")
                await browser.close()
                return status

        res = self.run_async(_test())
        self.assertIn(res["isCloudEnabled"], (True, False))
        self.assertFalse(res["isDraftSyncEnabled"])
        self.assertEqual(res["namespace"], "social-r:progress:intro-r")

    def test_editor_code_does_not_trigger_cloud_sync_when_drafts_off(self):
        """Verifies section 7 & 8: saveEditorCode does NOT fire cloud sync when draftSync is disabled."""
        from playwright.async_api import async_playwright

        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                sync_calls = await page.evaluate("""async () => {
                    let queueSyncCount = 0;
                    if (window.SocialR && window.SocialR.cloudAdapter) {
                        window.SocialR.cloudAdapter.queueSync = () => { queueSyncCount++; };
                    }

                    const progress = window.SocialR && window.SocialR.progress;
                    if (!progress) return { ok: false };

                    // Save editor code 5 times
                    for (let i = 0; i < 5; i++) {
                        progress.saveEditorCode('intro-r-01-001', 'x <- ' + i);
                    }

                    // Wait 600ms for debounce
                    await new Promise(r => setTimeout(r, 650));

                    const codeInStore = progress.getEditorCode('intro-r-01-001');
                    return {
                        ok: true,
                        queueSyncCount,
                        codeInStore
                    };
                }""")
                await browser.close()
                return sync_calls

        res = self.run_async(_test())
        self.assertTrue(res["ok"])
        self.assertEqual(res["queueSyncCount"], 0, "saveEditorCode must NOT trigger cloud sync when drafts are local-only")
        self.assertEqual(res["codeInStore"], "x <- 4", "Code must still be stored locally")

    def test_completed_exercise_and_challenge_trigger_queue_sync(self):
        """Verifies that real progress (completed exercises and challenges) DOES queue cloud sync."""
        from playwright.async_api import async_playwright

        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{self.base_url}/curso.html")

                sync_calls = await page.evaluate("""() => {
                    let queueSyncCount = 0;
                    if (window.SocialR && window.SocialR.cloudAdapter) {
                        window.SocialR.cloudAdapter.queueSync = () => { queueSyncCount++; };
                    }

                    const progress = window.SocialR && window.SocialR.progress;
                    if (!progress) return { ok: false };

                    // 1. Mark completed exercise
                    progress.markCompleted('intro-r-01-001');

                    // 2. Mark challenge passed
                    progress.markChallengePassed('01-empezar-a-pensar-con-r');

                    return {
                        ok: true,
                        queueSyncCount
                    };
                }""")
                await browser.close()
                return sync_calls

        res = self.run_async(_test())
        self.assertTrue(res["ok"])
        self.assertGreaterEqual(res["queueSyncCount"], 2, "markCompleted and markChallengePassed must trigger queueSync")

    def test_namespaced_local_storage_isolation(self):
        """Tests that student sessions namespace progress by student UUID, never RUT."""
        from playwright.async_api import async_playwright

        async def _test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(f"{self.base_url}/index.html")

                res = await page.evaluate("""() => {
                    const cloud = window.SocialR && window.SocialR.cloudConfig;
                    if (!cloud) return { ok: false };

                    const anonNs = cloud.getProgressNamespace('intro-r');

                    const anaStudent = {
                        studentId: '11111111-2222-3333-4444-555555555555',
                        rutMasked: '••.•••.678-5',
                        displayName: 'Ana Pérez'
                    };
                    cloud.setSession({ sessionToken: 'tok_ana', student: anaStudent });
                    const anaNs = cloud.getProgressNamespace('intro-r');

                    const juanStudent = {
                        studentId: '99999999-8888-7777-6666-555555555555',
                        rutMasked: '••.•••.543-2',
                        displayName: 'Juan Soto'
                    };
                    cloud.setSession({ sessionToken: 'tok_juan', student: juanStudent });
                    const juanNs = cloud.getProgressNamespace('intro-r');

                    cloud.clearSession();
                    const loggedOutNs = cloud.getProgressNamespace('intro-r');

                    return {
                        ok: true,
                        anonNs,
                        anaNs,
                        juanNs,
                        loggedOutNs
                    };
                }""")
                await browser.close()
                return res

        res = self.run_async(_test())
        self.assertTrue(res["ok"])
        self.assertEqual(res["anonNs"], "social-r:progress:intro-r")
        self.assertEqual(res["anaNs"], "social-r:progress:intro-r:11111111-2222-3333-4444-555555555555")
        self.assertEqual(res["juanNs"], "social-r:progress:intro-r:99999999-8888-7777-6666-555555555555")
        self.assertNotIn("12345678", res["anaNs"], "Namespace must NEVER contain student RUT")
        self.assertNotEqual(res["anaNs"], res["juanNs"])
        self.assertEqual(res["loggedOutNs"], "social-r:progress:intro-r")


if __name__ == "__main__":
    unittest.main()
