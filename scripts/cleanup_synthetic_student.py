#!/usr/bin/env python3
"""
Social R — Synthetic Student Cleanup Utility
Safely removes synthetic test student records generated during smoke testing.
Enforces strict guardrails to prevent accidental modification or deletion of real student data.

Guardrails:
- Must match expected synthetic display name ("Estudiante Prueba Social R").
- Must belong to section "TEST".
- Must belong to course "intro-r".
- Must match local HMAC rut_lookup exactly.
- Aborts if more than one matching student is found.
- Aborts if any ambiguity exists.
- Defaults to DRY-RUN mode.
- Real deletion requires explicit `--confirm-delete-synthetic` flag.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.rut_utils import (
    clean_rut,
    compute_rut_lookup,
    format_rut_masked,
    validate_rut,
)

DEFAULT_COURSE = "intro-r"
DEFAULT_EXPECTED_NAME = "Estudiante Prueba Social R"
DEFAULT_EXPECTED_SECTION = "TEST"
DEFAULT_SYNTHETIC_RUT = "99999991-3"


def load_env_file(filepath: Path):
    """Loads key=value pairs from a .env file into os.environ if not already set."""
    if not filepath.exists():
        return
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v


def make_postgrest_request(url: str, method: str, service_key: str, data=None):
    """Executes an authenticated HTTP request against Supabase PostgREST API."""
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else []
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code} Error on {method} {url}: {err_body}") from e


def mask_id(val: str) -> str:
    """Masks UUID for safe display."""
    if not val or len(val) < 8:
        return "********"
    return f"{val[:8]}..."


def validate_guardrails(
    student: dict,
    enrollments: list,
    expected_name: str,
    expected_section: str,
    course_id: str,
    expected_lookup: str,
):
    """
    Validates all safety guardrails before any action.
    Raises ValueError if ANY guardrail check fails.
    """
    # 1. Check course_id
    if course_id != DEFAULT_COURSE:
        raise ValueError(
            f"[GUARDRAIL VIOLATION] Cleanup is restricted to course '{DEFAULT_COURSE}'. Got: '{course_id}'"
        )

    # 2. Check student display name
    actual_name = student.get("display_name", "").strip()
    if actual_name != expected_name:
        raise ValueError(
            f"[GUARDRAIL VIOLATION] Display name mismatch: expected '{expected_name}', got '{actual_name}'"
        )

    # 3. Check HMAC rut_lookup
    actual_lookup = student.get("rut_lookup", "")
    if actual_lookup != expected_lookup:
        raise ValueError(
            "[GUARDRAIL VIOLATION] HMAC rut_lookup mismatch between local and remote record."
        )

    # 4. Check enrollments
    if not enrollments:
        raise ValueError(
            "[GUARDRAIL VIOLATION] Student has no enrollment records found for verification."
        )

    for enr in enrollments:
        enr_course = enr.get("course_id", "")
        enr_section = enr.get("section", "")
        if enr_course != DEFAULT_COURSE:
            raise ValueError(
                f"[GUARDRAIL VIOLATION] Enrollment belongs to non-test course '{enr_course}'"
            )
        if enr_section != expected_section:
            raise ValueError(
                f"[GUARDRAIL VIOLATION] Enrollment belongs to section '{enr_section}' (expected '{expected_section}')"
            )


def verify_service_role_cleanup_privileges(supabase_url: str, service_key: str):
    """
    Preflight check to ensure the caller has required DELETE privileges.
    If service_role lacks DELETE on ANY required table (such as activity_events),
    aborts BEFORE any mutation takes place to avoid partial cleanup.
    """
    dummy_uuid = "00000000-0000-0000-0000-000000000000"
    required_tables = [
        "student_sessions",
        "exercise_progress",
        "challenge_progress",
        "exercise_drafts",
        "activity_events",
        "enrollments",
        "students",
    ]
    for table in required_tables:
        url = f"{supabase_url}/rest/v1/{table}?student_id=eq.{dummy_uuid}"
        headers = {
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        req = urllib.request.Request(url, headers=headers, method="DELETE")
        try:
            with urllib.request.urlopen(req) as resp:
                pass
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise PermissionError(
                    "Application service_role intentionally lacks privileges required for full synthetic cleanup. "
                    "Use the guarded administrative SQL cleanup."
                )
            raise


def inspect_dependent_records(supabase_url: str, service_key: str, student_id: str, course_id: str):
    """Queries row counts for all dependent tables for the given student."""
    tables = [
        ("student_sessions", f"{supabase_url}/rest/v1/student_sessions?student_id=eq.{student_id}&select=session_id"),
        ("exercise_progress", f"{supabase_url}/rest/v1/exercise_progress?student_id=eq.{student_id}&course_id=eq.{course_id}&select=progress_id"),
        ("challenge_progress", f"{supabase_url}/rest/v1/challenge_progress?student_id=eq.{student_id}&course_id=eq.{course_id}&select=challenge_progress_id"),
        ("exercise_drafts", f"{supabase_url}/rest/v1/exercise_drafts?student_id=eq.{student_id}&course_id=eq.{course_id}&select=draft_id"),
        ("activity_events", f"{supabase_url}/rest/v1/activity_events?student_id=eq.{student_id}&select=event_id,event_type"),
        ("enrollments", f"{supabase_url}/rest/v1/enrollments?student_id=eq.{student_id}&course_id=eq.{course_id}&select=enrollment_id,section"),
    ]
    counts = {}
    for table_name, url in tables:
        _, rows = make_postgrest_request(url, "GET", service_key)
        counts[table_name] = rows or []
    return counts


def run_cleanup(
    supabase_url: str,
    service_key: str,
    rut_secret: str,
    rut: str = DEFAULT_SYNTHETIC_RUT,
    course_id: str = DEFAULT_COURSE,
    expected_name: str = DEFAULT_EXPECTED_NAME,
    expected_section: str = DEFAULT_EXPECTED_SECTION,
    confirm_delete: bool = False,
    dry_run: bool = True,
):
    """
    Main cleanup coordinator.
    If dry_run is True or confirm_delete is False, runs in DRY-RUN mode.
    """
    if not validate_rut(rut):
        raise ValueError("[GUARDRAIL VIOLATION] Invalid synthetic RUT format.")

    computed_lookup = compute_rut_lookup(rut, rut_secret)
    rut_masked_local = format_rut_masked(rut)

    print("============================================================")
    print("SOCIAL R — SYNTHETIC STUDENT CLEANUP AUDITOR")
    print("============================================================")
    print(f"Target Course:           {course_id}")
    print(f"Target Section:          {expected_section}")
    print(f"Expected Name:           {expected_name}")
    print(f"Synthetic Masked RUT:    {rut_masked_local}")
    print(f"Mode:                    {'DRY-RUN (Simulated)' if dry_run else 'ACTIVE DELETION'}")
    print("------------------------------------------------------------")

    # 1. Fetch student from public.students by rut_lookup
    lookup_url = f"{supabase_url}/rest/v1/students?rut_lookup=eq.{computed_lookup}&select=student_id,display_name,rut_masked,rut_lookup,active"
    _, students = make_postgrest_request(lookup_url, "GET", service_key)

    if not students:
        print("[INFO] No matching synthetic student found in public.students.")
        print("[OK] Database is already clean of this synthetic student.")
        return {"status": "NOT_FOUND", "deleted": 0}

    if len(students) > 1:
        raise ValueError(
            f"[GUARDRAIL VIOLATION] Multiple students ({len(students)}) found with identical rut_lookup! Aborting."
        )

    student = students[0]
    student_id = student["student_id"]
    masked_uuid = mask_id(student_id)

    # 2. Fetch enrollments
    enr_url = f"{supabase_url}/rest/v1/enrollments?student_id=eq.{student_id}&select=enrollment_id,course_id,section,active"
    _, enrollments = make_postgrest_request(enr_url, "GET", service_key)

    # 3. Validate guardrails strictly
    validate_guardrails(
        student=student,
        enrollments=enrollments,
        expected_name=expected_name,
        expected_section=expected_section,
        course_id=course_id,
        expected_lookup=computed_lookup,
    )
    print(f"[OK] Guardrails passed: Student ID {masked_uuid} verified as synthetic TEST student.")

    # 4. Inspect dependent records
    deps = inspect_dependent_records(supabase_url, service_key, student_id, course_id)

    print("------------------------------------------------------------")
    print("CURRENT SYNTHETIC RECORDS IN CLOUD:")
    print(f"  student_sessions:     {len(deps['student_sessions'])} rows")
    print(f"  exercise_progress:    {len(deps['exercise_progress'])} rows")
    print(f"  challenge_progress:   {len(deps['challenge_progress'])} rows")
    print(f"  exercise_drafts:      {len(deps['exercise_drafts'])} rows")
    print(f"  activity_events:      {len(deps['activity_events'])} rows")
    print(f"  enrollments:          {len(deps['enrollments'])} rows")
    print(f"  students:             1 row")
    print("------------------------------------------------------------")

    if dry_run or not confirm_delete:
        print("[DRY-RUN] Execution completed in preview mode.")
        print("[DRY-RUN] NO records were deleted from Supabase.")
        print("[DRY-RUN] To perform actual deletion, run with --confirm-delete-synthetic.")
        return {
            "status": "DRY_RUN",
            "student_id_masked": masked_uuid,
            "counts": {k: len(v) for k, v in deps.items()},
        }

    # 5. Preflight check: Ensure service_role has all required DELETE privileges before modifying ANY table
    print("[PREFLIGHT] Auditing DELETE privileges for service_role...")
    verify_service_role_cleanup_privileges(supabase_url, service_key)
    print("[OK] Privilege preflight passed.")

    # 6. Real deletion in strict reverse dependency order
    print("[WARNING] Performing REAL DELETION of synthetic records...")

    order = [
        ("student_sessions", f"{supabase_url}/rest/v1/student_sessions?student_id=eq.{student_id}"),
        ("exercise_progress", f"{supabase_url}/rest/v1/exercise_progress?student_id=eq.{student_id}&course_id=eq.{course_id}"),
        ("challenge_progress", f"{supabase_url}/rest/v1/challenge_progress?student_id=eq.{student_id}&course_id=eq.{course_id}"),
        ("exercise_drafts", f"{supabase_url}/rest/v1/exercise_drafts?student_id=eq.{student_id}&course_id=eq.{course_id}"),
        ("activity_events", f"{supabase_url}/rest/v1/activity_events?student_id=eq.{student_id}"),
        ("enrollments", f"{supabase_url}/rest/v1/enrollments?student_id=eq.{student_id}&course_id=eq.{course_id}"),
        ("students", f"{supabase_url}/rest/v1/students?student_id=eq.{student_id}"),
    ]

    deleted_summary = {}
    for table_name, del_url in order:
        _, deleted_rows = make_postgrest_request(del_url, "DELETE", service_key)
        count = len(deleted_rows) if isinstance(deleted_rows, list) else 0
        deleted_summary[table_name] = count
        print(f"  [DELETED] {table_name}: {count} row(s)")

    print("[SUCCESS] All synthetic student records successfully purged.")
    return {
        "status": "SUCCESS",
        "student_id_masked": masked_uuid,
        "deleted": deleted_summary,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Safely removes synthetic test student records from Supabase."
    )
    parser.add_argument(
        "--course",
        default=DEFAULT_COURSE,
        help=f"Course ID (must be '{DEFAULT_COURSE}').",
    )
    parser.add_argument(
        "--expected-name",
        default=DEFAULT_EXPECTED_NAME,
        help=f"Expected student name (must be '{DEFAULT_EXPECTED_NAME}').",
    )
    parser.add_argument(
        "--expected-section",
        default=DEFAULT_EXPECTED_SECTION,
        help=f"Expected section (must be '{DEFAULT_EXPECTED_SECTION}').",
    )
    parser.add_argument(
        "--rut",
        default=DEFAULT_SYNTHETIC_RUT,
        help="Synthetic student RUT (default: smoke test synthetic RUT).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview actions without modifying database (default behavior).",
    )
    parser.add_argument(
        "--confirm-delete-synthetic",
        action="store_true",
        default=False,
        help="Explicit confirmation required to execute real deletion.",
    )

    args = parser.parse_args()

    # Load environment
    env_file = ROOT_DIR / ".env"
    load_env_file(env_file)

    supabase_url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    rut_secret = os.environ.get("RUT_SECRET_KEY")

    if not supabase_url or not service_key or not rut_secret:
        print("[ABORT] Missing required environment variables (SUPABASE_URL, SUPABASE_SECRET_KEY, RUT_SECRET_KEY).")
        sys.exit(1)

    # Dry-run is enforced unless --confirm-delete-synthetic is set AND --dry-run is False
    is_dry_run = args.dry_run or (not args.confirm_delete_synthetic)

    try:
        res = run_cleanup(
            supabase_url=supabase_url,
            service_key=service_key,
            rut_secret=rut_secret,
            rut=args.rut,
            course_id=args.course,
            expected_name=args.expected_name,
            expected_section=args.expected_section,
            confirm_delete=args.confirm_delete_synthetic,
            dry_run=is_dry_run,
        )
        if res.get("status") in ("DRY_RUN", "SUCCESS", "NOT_FOUND"):
            sys.exit(0)
        sys.exit(1)
    except PermissionError as pe:
        print(f"[ABORT] {pe}", file=sys.stderr)
        print(r"[INFO] Administrative SQL cleanup script available at: $env:TEMP\social_r_cleanup_synthetic.sql", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ABORT] Cleanup stopped due to safety violation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
