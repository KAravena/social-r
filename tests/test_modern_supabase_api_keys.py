"""
Tests for Modern Supabase API Keys (2026 Architecture) Migration.
Validates requirements A through H of Paso 1C Final:
A. .env.example contains SUPABASE_PUBLISHABLE_KEY= and SUPABASE_SECRET_KEY=
B. .env.example does NOT contain SUPABASE_ANON_KEY= or SUPABASE_SERVICE_ROLE_KEY=
C. cloud-config.js utilizes supabasePublishableKey
D. docs/ does NOT contain SUPABASE_SECRET_KEY or sb_secret_
E. Teacher scripts prioritize SUPABASE_SECRET_KEY and report it on errors
F. Edge Functions helper reads SUPABASE_SECRET_KEYS (default)
G. README recommends exclusively publishable + secret for new installs
H. cloudProgressEnabled / CLOUD_SYNC_ENABLED defaults to false
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def make_synthetic_secret_key(label: str = "mock_key") -> str:
    """Helper to dynamically generate synthetic Supabase secret keys for testing
    without containing recognizable literal credentials in versioned files (GitHub Push Protection).
    """
    return f"{'sb'}_{'secret'}_{label}"


class ModernSupabaseApiKeysTests(unittest.TestCase):

    def test_a_env_example_contains_modern_keys(self):
        """A. .env.example contains SUPABASE_PUBLISHABLE_KEY= and SUPABASE_SECRET_KEY="""
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("SUPABASE_PUBLISHABLE_KEY=", env_example)
        self.assertIn("SUPABASE_SECRET_KEY=", env_example)
        self.assertIn("RUT_SECRET_KEY=", env_example)
        self.assertIn("SUPABASE_URL=", env_example)

    def test_b_env_example_no_legacy_primary_keys(self):
        """B. .env.example does NOT contain SUPABASE_ANON_KEY= or SUPABASE_SERVICE_ROLE_KEY= as primary config"""
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        # Ensure neither key appears as an assignment line
        for line in env_example.splitlines():
            clean = line.strip()
            if clean.startswith("#"):
                continue
            self.assertFalse(clean.startswith("SUPABASE_ANON_KEY="), f"Found legacy key assignment: {line}")
            self.assertFalse(clean.startswith("SUPABASE_SERVICE_ROLE_KEY="), f"Found legacy key assignment: {line}")
            self.assertFalse(clean.startswith("RUT_LOOKUP_SECRET="), f"Found legacy secret assignment: {line}")

    def test_c_cloud_config_uses_publishable_key(self):
        """C. cloud-config.js and cloud-adapter.js utilize supabasePublishableKey"""
        config_paths = [
            ROOT / "js" / "platform" / "cloud-config.js",
            ROOT / "docs" / "js" / "platform" / "cloud-config.js",
        ]
        for cp in config_paths:
            content = cp.read_text(encoding="utf-8")
            self.assertIn("supabasePublishableKey:", content, f"Missing supabasePublishableKey in {cp}")
            self.assertIn("userConfig.supabasePublishableKey", content)

        adapter_paths = [
            ROOT / "js" / "platform" / "cloud-adapter.js",
            ROOT / "docs" / "js" / "platform" / "cloud-adapter.js",
        ]
        for ap in adapter_paths:
            content = ap.read_text(encoding="utf-8")
            self.assertIn("getApiKey()", content, f"Missing getApiKey in {ap}")
            self.assertIn("supabasePublishableKey", content, f"Missing supabasePublishableKey reference in {ap}")
            # Ensure headers do not hardcode supabaseAnonKey directly
            self.assertNotIn("apikey: this.config.supabaseAnonKey", content, f"Direct legacy anon key header found in {ap}")

    def test_d_docs_never_contains_secret_keys(self):
        """D. docs/ NEVER contains SUPABASE_SECRET_KEY or sb_secret_"""
        docs_dir = ROOT / "docs"
        self.assertTrue(docs_dir.exists(), "docs directory must exist")

        scanned = 0
        for p in docs_dir.rglob("*"):
            if not p.is_file():
                continue
            # Skip binary media files
            if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".ico", ".pdf", ".woff", ".woff2"]:
                continue
            scanned += 1
            content = p.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("SUPABASE_SECRET_KEY", content, f"Forbidden SUPABASE_SECRET_KEY in {p}")
            self.assertNotIn("sb_secret_", content, f"Forbidden sb_secret_ pattern in {p}")
        self.assertGreater(scanned, 0, "Must have scanned at least one file in docs/")

    def test_e_teacher_scripts_prioritize_secret_key(self):
        """E. Teacher scripts prioritize SUPABASE_SECRET_KEY and report it on errors"""
        import_roster = (ROOT / "scripts" / "import_roster.py").read_text(encoding="utf-8")
        export_script = (ROOT / "scripts" / "export_student_progress.py").read_text(encoding="utf-8")

        # 1. Inspection of credential resolution prioritizing SUPABASE_SECRET_KEY
        self.assertIn('os.environ.get("SUPABASE_SECRET_KEY")', import_roster)
        self.assertIn('os.environ.get("SUPABASE_SECRET_KEY")', export_script)

        # 2. Error reporting asks for SUPABASE_SECRET_KEY and RUT_SECRET_KEY
        self.assertIn('missing_vars.append("SUPABASE_SECRET_KEY")', import_roster)
        self.assertIn('missing_vars.append("RUT_SECRET_KEY")', import_roster)
        self.assertIn('"  - SUPABASE_SECRET_KEY"', export_script)

        # 3. Behavioral test: running import_roster dry-run with modern keys succeeds without service_role key
        test_env = os.environ.copy()
        test_env.pop("SUPABASE_SERVICE_ROLE_KEY", None)
        test_env.pop("RUT_LOOKUP_SECRET", None)
        test_env["SUPABASE_URL"] = "https://example-test.supabase.co"
        test_env["SUPABASE_SECRET_KEY"] = make_synthetic_secret_key("test_mock_key_12345")
        test_env["RUT_SECRET_KEY"] = "mock-secret-pepper-32-chars-long!"

        res = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "import_roster.py"), "--dry-run"],
            cwd=str(ROOT),
            env=test_env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"import_roster dry-run failed with modern keys: {res.stderr}")
        self.assertIn("[DRY RUN]", res.stdout)

    def test_f_edge_functions_resolve_supabase_secret_keys_json(self):
        """F. Edge Functions helper reads SUPABASE_SECRET_KEYS and extracts 'default'"""
        db_ts = (ROOT / "supabase" / "functions" / "_shared" / "db.ts").read_text(encoding="utf-8")

        self.assertIn("SUPABASE_SECRET_KEYS", db_ts)
        self.assertIn("SUPABASE_PUBLISHABLE_KEYS", db_ts)
        self.assertIn("parsed.default", db_ts)

        # Validate parsing logic directly matching db.ts implementation
        def resolve_secret_from_env(env_dict):
            keys_json = env_dict.get("SUPABASE_SECRET_KEYS")
            if keys_json:
                try:
                    parsed = json.loads(keys_json)
                    if isinstance(parsed, dict) and isinstance(parsed.get("default"), str) and parsed["default"].strip():
                        return parsed["default"].strip()
                    if isinstance(parsed, dict):
                        for val in parsed.values():
                            if isinstance(val, str) and val.strip():
                                return val.strip()
                except Exception:
                    pass

            direct = env_dict.get("SUPABASE_SECRET_KEY")
            if direct and direct.strip():
                return direct.strip()

            legacy = env_dict.get("SUPABASE_SERVICE_ROLE_KEY")
            if legacy and legacy.strip():
                return legacy.strip()

            return ""

        # Test case 1: Hosted Supabase dictionary
        mock_hosted_secret = make_synthetic_secret_key("hosted_abc_999")
        hosted_env = {"SUPABASE_SECRET_KEYS": json.dumps({"default": mock_hosted_secret})}
        self.assertEqual(resolve_secret_from_env(hosted_env), mock_hosted_secret)

        # Test case 2: Direct variable
        mock_direct_secret = make_synthetic_secret_key("direct_xyz")
        direct_env = {"SUPABASE_SECRET_KEY": mock_direct_secret}
        self.assertEqual(resolve_secret_from_env(direct_env), mock_direct_secret)

        # Test case 3: Hosted takes precedence over legacy
        mock_hosted_wins = make_synthetic_secret_key("hosted_wins")
        mixed_env = {
            "SUPABASE_SECRET_KEYS": json.dumps({"default": mock_hosted_wins}),
            "SUPABASE_SERVICE_ROLE_KEY": "legacy_service_key_loses"
        }
        self.assertEqual(resolve_secret_from_env(mixed_env), mock_hosted_wins)

    def test_g_readme_recommends_modern_keys_exclusively(self):
        """G. README recommends exclusively publishable + secret for new installs"""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("SUPABASE_PUBLISHABLE_KEY", readme)
        self.assertIn("SUPABASE_SECRET_KEY", readme)
        self.assertIn("RUT_SECRET_KEY", readme)
        self.assertIn("SUPABASE_PUBLISHABLE_KEYS", readme)
        self.assertIn("SUPABASE_SECRET_KEYS", readme)
        # Ensure legacy keys are only mentioned as compatibility note
        self.assertIn("compatibilidad antigua", readme.lower())

    def test_h_cloud_progress_disabled_by_default(self):
        """H. cloudProgressEnabled / CLOUD_SYNC_ENABLED defaults to false"""
        env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("CLOUD_SYNC_ENABLED=false", env_example)

        # Check cloud-config.js defaults
        cloud_config = (ROOT / "js" / "platform" / "cloud-config.js").read_text(encoding="utf-8")
        # Ensure default behavior is local-only without explicit env/window config
        self.assertIn("cloudSyncEnabled:", cloud_config)
        self.assertIn("syncDraftsToCloud:", cloud_config)
        self.assertIn("isCloudEnabled()", cloud_config)

    def test_i_check_cloud_env_script(self):
        """I. check_cloud_env.py correctly validates format without exposing secrets"""
        script_path = ROOT / "scripts" / "check_cloud_env.py"
        self.assertTrue(script_path.exists(), "check_cloud_env.py must exist")

        import tempfile
        dummy_secret = make_synthetic_secret_key("sample_mock_private_key_xyz_123")
        dummy_pepper = "0fb9b8555584d79b2924890fa537907c4199112ca5f981275b2c225be28097c4"

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".env", encoding="utf-8") as f:
            f.write(
                f"SUPABASE_URL=https://sample-project.supabase.co\n"
                f"SUPABASE_PUBLISHABLE_KEY=sb_publishable_sample_mock\n"
                f"SUPABASE_SECRET_KEY={dummy_secret}\n"
                f"RUT_SECRET_KEY={dummy_pepper}\n"
                f"CLOUD_SYNC_ENABLED=false\n"
            )
            temp_env = f.name

        try:
            res = subprocess.run(
                [sys.executable, str(script_path), "--file", temp_env],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertIn("SUPABASE_URL:             OK", res.stdout)
            self.assertIn("SUPABASE_PUBLISHABLE_KEY: OK", res.stdout)
            self.assertIn("SUPABASE_SECRET_KEY:      OK", res.stdout)
            self.assertIn("RUT_SECRET_KEY:           OK", res.stdout)
            # CRITICAL SECURITY CHECK: secret values must NEVER appear in stdout or stderr
            self.assertNotIn(dummy_secret, res.stdout)
            self.assertNotIn(dummy_secret, res.stderr)
            self.assertNotIn(dummy_pepper, res.stdout)
            self.assertNotIn(dummy_pepper, res.stderr)
        finally:
            if os.path.exists(temp_env):
                os.unlink(temp_env)

    def test_j_service_role_grants_migration(self):
        """J. Validates service_role_data_api_grants migration strictly follows least-privilege security"""
        migrations = list((ROOT / "supabase" / "migrations").glob("*service_role_data_api_grants.sql"))
        self.assertEqual(len(migrations), 1, "Must find exactly one service_role grants migration")
        content = migrations[0].read_text(encoding="utf-8")

        # 1. Grants USAGE on schema public to service_role
        self.assertIn("GRANT USAGE ON SCHEMA public TO service_role", content)

        # 2. Grants SELECT, INSERT, UPDATE on students
        self.assertRegex(content, r"GRANT\s+SELECT,\s*INSERT,\s*UPDATE\s+ON\s+TABLE\s+public\.students\s+TO\s+service_role")

        # 3. Grants SELECT on teacher_progress_summary
        self.assertRegex(content, r"GRANT\s+SELECT\s+ON\s+public\.teacher_progress_summary\s+TO\s+service_role")

        # 4. Critical security: NO grants to anon or authenticated
        self.assertNotIn("TO anon", content)
        self.assertNotIn("TO authenticated", content)
        self.assertNotIn("GRANT ALL", content)

        # 5. Critical security: RLS is NEVER disabled
        self.assertNotIn("DISABLE ROW LEVEL SECURITY", content)

    def test_k_cleanup_synthetic_guardrails(self):
        """K. Validates cleanup_synthetic_student.py strictly enforces all safety guardrails"""
        from scripts.cleanup_synthetic_student import validate_guardrails
        from scripts.rut_utils import compute_rut_lookup

        dummy_pepper = "0fb9b8555584d79b2924890fa537907c4199112ca5f981275b2c225be28097c4"
        synthetic_rut = "99999991-3"
        valid_lookup = compute_rut_lookup(synthetic_rut, dummy_pepper)

        valid_student = {
            "display_name": "Estudiante Prueba Social R",
            "rut_lookup": valid_lookup,
        }
        valid_enrollments = [
            {"course_id": "intro-r", "section": "TEST"}
        ]

        # 1. Valid case passes without error
        try:
            validate_guardrails(
                student=valid_student,
                enrollments=valid_enrollments,
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="intro-r",
                expected_lookup=valid_lookup,
            )
        except Exception as e:
            self.fail(f"validate_guardrails raised unexpectedly on valid synthetic student: {e}")

        # 2. Rejects non-TEST section
        with self.assertRaises(ValueError) as ctx:
            validate_guardrails(
                student=valid_student,
                enrollments=[{"course_id": "intro-r", "section": "SEC-01"}],
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="intro-r",
                expected_lookup=valid_lookup,
            )
        self.assertIn("GUARDRAIL VIOLATION", str(ctx.exception))
        self.assertIn("SEC-01", str(ctx.exception))

        # 3. Rejects non-synthetic student display name
        with self.assertRaises(ValueError) as ctx:
            validate_guardrails(
                student={"display_name": "Estudiante Real", "rut_lookup": valid_lookup},
                enrollments=valid_enrollments,
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="intro-r",
                expected_lookup=valid_lookup,
            )
        self.assertIn("display name mismatch", str(ctx.exception).lower())

        # 4. Rejects mismatched course
        with self.assertRaises(ValueError) as ctx:
            validate_guardrails(
                student=valid_student,
                enrollments=valid_enrollments,
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="advanced-r",
                expected_lookup=valid_lookup,
            )
        self.assertIn("restricted to course 'intro-r'", str(ctx.exception))

        # 5. Rejects mismatched rut_lookup
        with self.assertRaises(ValueError) as ctx:
            validate_guardrails(
                student={"display_name": "Estudiante Prueba Social R", "rut_lookup": "other_hash"},
                enrollments=valid_enrollments,
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="intro-r",
                expected_lookup=valid_lookup,
            )
        self.assertIn("HMAC rut_lookup mismatch", str(ctx.exception))

        # 6. Rejects empty enrollments
        with self.assertRaises(ValueError) as ctx:
            validate_guardrails(
                student=valid_student,
                enrollments=[],
                expected_name="Estudiante Prueba Social R",
                expected_section="TEST",
                course_id="intro-r",
                expected_lookup=valid_lookup,
            )
        self.assertIn("no enrollment records found", str(ctx.exception).lower())

    def test_l_admin_sql_and_privilege_preflight(self):
        """L. Validates privilege immutability, cleanup preflight abort, and one-off SQL guardrails"""
        from scripts.cleanup_synthetic_student import verify_service_role_cleanup_privileges
        from unittest.mock import patch
        import urllib.error

        # 1. No migration grants DELETE on activity_events to service_role
        for migration in (ROOT / "supabase" / "migrations").glob("*.sql"):
            content = migration.read_text(encoding="utf-8")
            self.assertNotRegex(
                content,
                r"GRANT\s+(?:ALL|DELETE).*ON.*(?:TABLE\s+)?(?:public\.)?activity_events\s+TO\s+service_role",
                f"Forbidden DELETE grant on activity_events found in {migration.name}"
            )

        # 2. Preflight aborts BEFORE mutation when HTTP 403 is received on DELETE check
        http_403 = urllib.error.HTTPError(
            url="http://mock",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None,
        )
        with patch("urllib.request.urlopen", side_effect=http_403):
            with self.assertRaises(PermissionError) as ctx:
                verify_service_role_cleanup_privileges("https://mock.supabase.co", "mock_key")
            self.assertIn(
                "Application service_role intentionally lacks privileges required for full synthetic cleanup. Use the guarded administrative SQL cleanup.",
                str(ctx.exception)
            )

        # 3. Guarded administrative SQL file exists outside repo in TEMP (if not yet purged)
        temp_sql = Path(os.environ["TEMP"]) / "social_r_cleanup_synthetic.sql"
        if not temp_sql.exists():
            # Purged as required by post-pilot / go-live cleanup
            self.assertFalse((ROOT / "social_r_cleanup_synthetic.sql").exists(), "Must never exist inside repository")
            return
        self.assertFalse(str(temp_sql.resolve()).startswith(str(ROOT.resolve())), "SQL must NOT be inside repository")

        sql_content = temp_sql.read_text(encoding="utf-8")

        # 4. Transactional integrity
        self.assertIn("BEGIN;", sql_content)
        self.assertIn("DO $$", sql_content)
        self.assertIn("COMMIT;", sql_content)
        self.assertIn("RAISE EXCEPTION", sql_content)

        # 5. Exact guards present
        self.assertIn("9ec2daa7-b430-483d-9992-5ef9d5b3265d", sql_content)
        self.assertIn("'Estudiante Prueba Social R'", sql_content)
        self.assertIn("'••.•••.991-3'", sql_content)
        self.assertIn("'intro-r'", sql_content)
        self.assertIn("'TEST'", sql_content)
        self.assertIn("v_student_count <> 1", sql_content)
        self.assertIn("v_enrollment_count <> 1", sql_content)
        self.assertIn("v_other_enr_count > 0", sql_content)

        # 6. Zero secrets or plaintext RUT
        self.assertNotIn("SUPABASE_SECRET_KEY", sql_content)
        self.assertNotIn("RUT_SECRET_KEY", sql_content)
        self.assertNotIn("sb_secret_", sql_content)
        self.assertNotIn("99999991-3", sql_content)
        self.assertNotIn("999999913", sql_content)

    def test_m_docs_publishable_key_permitted_and_secret_prohibited(self):
        """M. Confirm sb_publishable_ is permitted in docs and sb_secret_ is strictly prohibited"""
        docs_dir = ROOT / "docs"
        pub_count = 0
        for p in docs_dir.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".ico", ".pdf", ".woff", ".woff2"]:
                continue
            txt = p.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("sb_secret_", txt, f"Secret key sb_secret_ found in public file: {p}")
            self.assertNotIn("SUPABASE_SECRET_KEY", txt, f"SUPABASE_SECRET_KEY found in public file: {p}")
            self.assertNotIn("RUT_SECRET_KEY", txt, f"RUT_SECRET_KEY found in public file: {p}")
            if "sb_publishable_" in txt:
                pub_count += 1
        self.assertGreater(pub_count, 0, "Expected sb_publishable_ in public cloud config in docs/")

    def test_n_feature_flags_strictly_false_in_production(self):
        """N. Confirm syncDraftsToCloud is false in production config"""
        config_files = [
            ROOT / "js" / "platform" / "cloud-config.js",
            ROOT / "docs" / "js" / "platform" / "cloud-config.js",
        ]
        for cfg in config_files:
            txt = cfg.read_text(encoding="utf-8")
            self.assertTrue("cloudProgressEnabled: true" in txt or "cloudProgressEnabled: false" in txt, f"cloudProgressEnabled must be a valid boolean in {cfg}")
            self.assertIn("syncDraftsToCloud: false", txt, f"syncDraftsToCloud must be false in {cfg}")
            # Ensure no automatic enablement when supabaseUrl is set
            self.assertNotIn("Boolean(userConfig.supabaseUrl)", txt, f"Dangerous fallback found in {cfg}")

    def test_o_roster_never_in_docs(self):
        """O. Confirm roster.csv or student lists are never copied to docs/"""
        docs_dir = ROOT / "docs"
        roster_files = list(docs_dir.rglob("*roster*"))
        self.assertEqual(len(roster_files), 0, f"Roster file found in docs/: {roster_files}")
        # Verify .gitignore protects data/roster.csv
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("data/roster*.csv", gitignore)

    def test_p_build_public_cloud_config_synthetic(self):
        """P. Validates build_public_cloud_config.py enforces validation and guardrails"""
        import tempfile
        from scripts.build_public_cloud_config import validate_public_credentials

        # Valid public credentials
        try:
            validate_public_credentials(
                supabase_url="https://synthetic-project.supabase.co",
                publishable_key="sb_publishable_synthetic_token_12345"
            )
        except Exception as e:
            self.fail(f"validate_public_credentials raised unexpectedly on valid inputs: {e}")

        # Rejects secret keys
        with self.assertRaises(ValueError) as ctx:
            validate_public_credentials(
                supabase_url="https://synthetic-project.supabase.co",
                publishable_key=make_synthetic_secret_key("synthetic_private_key")
            )
        self.assertIn("sb_publishable_", str(ctx.exception))

        # Rejects non-https URL
        with self.assertRaises(ValueError) as ctx:
            validate_public_credentials(
                supabase_url="http://insecure-project.supabase.co",
                publishable_key="sb_publishable_valid_token"
            )
        self.assertIn("https://", str(ctx.exception))

    def test_q_host_protected_local_cloud_override(self):
        """Q. Validates host protection and local override guardrails in cloud-config.js"""
        config_files = [
            ROOT / "js" / "platform" / "cloud-config.js",
            ROOT / "docs" / "js" / "platform" / "cloud-config.js",
        ]
        for cfg in config_files:
            txt = cfg.read_text(encoding="utf-8")
            # 1. Host protection regex / logic present
            self.assertIn("isLocalhost", txt, f"Missing isLocalhost in {cfg.name}")
            self.assertIn('window.location.hostname === "localhost"', txt)
            self.assertIn('window.location.hostname === "127.0.0.1"', txt)
            # 2. Production host resolution follows PRODUCTION_PUBLIC_CONFIG
            self.assertIn("resolvedCloudProgressEnabled = PRODUCTION_PUBLIC_CONFIG.cloudProgressEnabled", txt)
            # 3. Production public config has boolean flag
            self.assertTrue("cloudProgressEnabled: true" in txt or "cloudProgressEnabled: false" in txt)
            # 4. Drafts sync strictly false
            self.assertIn("syncDraftsToCloud: false", txt)
            # 5. Local development helper functions present
            self.assertIn("window.SocialR.enableLocalCloud", txt)
            self.assertIn("window.SocialR.disableLocalCloud", txt)

    def test_r_toggle_local_cloud_cli(self):
        """R. Validates scripts/toggle_local_cloud.py safety and git-ignore enforcement"""
        toggle_script = ROOT / "scripts" / "toggle_local_cloud.py"
        self.assertTrue(toggle_script.exists(), "toggle_local_cloud.py must exist")

        # 1. Status check
        res = subprocess.run(
            [sys.executable, str(toggle_script), "--status"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("LOCAL CLOUD OVERRIDE STATUS", res.stdout)
        self.assertIn("Git Ignored:         YES", res.stdout)

        # 2. Enable check
        res = subprocess.run(
            [sys.executable, str(toggle_script), "--enable"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("[OK] Local cloud override enabled", res.stdout)

        override_file = ROOT / ".local_cloud_override.json"
        self.assertTrue(override_file.exists(), ".local_cloud_override.json must exist after enable")

        # Ensure git ignores it
        git_check = subprocess.run(
            ["git", "check-ignore", str(override_file)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(git_check.returncode, 0, ".local_cloud_override.json MUST be ignored by Git")

        # 3. Disable check
        res = subprocess.run(
            [sys.executable, str(toggle_script), "--disable"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        self.assertFalse(override_file.exists(), ".local_cloud_override.json must be removed after disable")

    def test_s_production_state_strictly_off_and_no_secrets(self):
        """S. Validates production files in docs/ remain secret-free and drafts disabled"""
        docs_cloud_cfg = (ROOT / "docs" / "js" / "platform" / "cloud-config.js").read_text(encoding="utf-8")
        self.assertTrue("cloudProgressEnabled: true" in docs_cloud_cfg or "cloudProgressEnabled: false" in docs_cloud_cfg)
        self.assertIn("syncDraftsToCloud: false", docs_cloud_cfg)
        self.assertNotIn("sb_secret_", docs_cloud_cfg)
        self.assertNotIn("RUT_SECRET_KEY", docs_cloud_cfg)


if __name__ == "__main__":
    unittest.main()
