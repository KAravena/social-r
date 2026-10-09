#!/usr/bin/env python3
"""
Social R — Student Roster Import Utility
Reads a student roster CSV, validates Chilean RUTs with Modulo 11,
checks for duplicates, and upserts students and course enrollments
into Supabase using the service role key from environment variables.

Usage:
  python scripts/import_roster.py [--file path/to/roster.csv] [--course intro-r] [--dry-run]
"""

import argparse
import csv
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

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.rut_utils import (
    calculate_dv,
    clean_rut,
    compute_rut_lookup,
    format_rut,
    format_rut_masked,
    normalize_rut,
    validate_rut,
)


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


def make_request(url: str, method: str, service_key: str, data=None):
    """Executes an authenticated HTTP request against Supabase PostgREST API."""
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation,resolution=merge-duplicates",
    }
    encoded_data = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code} Error: {err_body}") from e


def parse_roster_csv(csv_path: Path):
    """Parses and validates roster CSV. Returns (valid_records, errors)."""
    valid_records = []
    seen_ruts = set()
    errors = []

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [c.lower().strip() for c in (reader.fieldnames or [])]

        rut_col = next((c for c in fieldnames if "rut" in c), None)
        name_col = next((c for c in fieldnames if "nom" in c or "name" in c), None)
        sec_col = next((c for c in fieldnames if "sec" in c), None)
        role_col = next((c for c in fieldnames if "rol" in c), None)

        if not rut_col or not name_col:
            raise ValueError("El CSV debe contener al menos las columnas 'rut' y 'nombre'.")

        f.seek(0)
        dict_reader = csv.DictReader(f)

        for line_num, row in enumerate(dict_reader, start=2):
            raw_rut = row.get(rut_col, "").strip()
            raw_name = row.get(name_col, "").strip()
            raw_section = row.get(sec_col, "1").strip() if sec_col else "1"
            raw_role = row.get(role_col, "").strip().lower() if role_col else ("admin" if "admin" in raw_section.lower() else "student")
            if raw_role not in ("student", "admin"):
                raw_role = "admin" if "admin" in raw_section.lower() else "student"

            if not raw_rut and not raw_name:
                continue

            if not validate_rut(raw_rut):
                masked_rut = format_rut_masked(raw_rut) if len(clean_rut(raw_rut)) >= 4 else "***"
                errors.append(f"Línea {line_num}: RUT o IPE inválido ({masked_rut}).")
                continue

            norm_rut = normalize_rut(raw_rut)
            if norm_rut in seen_ruts:
                masked_rut = format_rut_masked(raw_rut)
                errors.append(f"Línea {line_num}: RUT o IPE duplicado ({masked_rut}). Ya fue procesado.")
                continue

            seen_ruts.add(norm_rut)
            valid_records.append({
                "rut": norm_rut,
                "rut_normalized": norm_rut,
                "display_name": raw_name,
                "section": raw_section or "1",
                "role": raw_role,
            })

    return valid_records, errors


def import_roster(csv_path: Path, course_id: str, dry_run: bool = False, secret: str = None):
    print("=" * 60)
    print("SOCIAL R — IMPORTACIÓN DE NÓMINA DE ESTUDIANTES")
    print("=" * 60)
    print(f"Archivo CSV: {csv_path}")
    print(f"Curso:       {course_id}")
    print(f"Modo:        {'DRY-RUN (Simulación sin escribir)' if dry_run else 'PRODUCCIÓN'}")
    print("-" * 60)

    if not csv_path.exists():
        print(f"Error: El archivo '{csv_path}' no existe.", file=sys.stderr)
        sys.exit(1)

    try:
        valid_records, errors = parse_roster_csv(csv_path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Registros leídos:  {len(valid_records) + len(errors)}")
    print(f"Registros válidos: {len(valid_records)}")
    if errors:
        print(f"Errores encontrados ({len(errors)}):")
        for err in errors[:10]:
            print(f"  • {err}")
        if len(errors) > 10:
            print(f"  ... y {len(errors) - 10} errores adicionales.")

    if not valid_records:
        print("\nNo se encontraron registros válidos para importar.")
        sys.exit(1)

    rut_secret = (secret or os.environ.get("RUT_SECRET_KEY") or os.environ.get("RUT_LOOKUP_SECRET", "")).strip()

    if dry_run:
        dry_secret = rut_secret or "dry-run-secret"
        print("\n[DRY RUN] Validación completada. Ningún cambio fue escrito en la base de datos.")
        print("Muestra de registros preparados para inserción (privacidad preservada):")
        for idx, r in enumerate(valid_records[:5], start=1):
            masked = format_rut_masked(r['rut_normalized'])
            print(f"  • Estudiante {idx} | Sección: {r['section']} | Masked: {masked}")
        return

    # 2. Check credentials & secret (Modern Supabase 2026: SUPABASE_SECRET_KEY; legacy fallback isolated)
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    service_key = (os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")).strip()

    missing_vars = []
    if not supabase_url:
        missing_vars.append("SUPABASE_URL")
    if not service_key:
        missing_vars.append("SUPABASE_SECRET_KEY")
    if not rut_secret:
        missing_vars.append("RUT_SECRET_KEY")

    if missing_vars:
        print("\nError: Faltan variables de entorno requeridas:", file=sys.stderr)
        for var in missing_vars:
            print(f"  - {var}", file=sys.stderr)
        print("Por favor configura tu archivo .env o variables de entorno.", file=sys.stderr)
        sys.exit(1)

    # 3. Upsert students into Supabase (Plaintext RUT is NEVER sent or stored)
    print("\nConectando con Supabase para sincronizar estudiantes (rut_lookup + rut_masked)...")
    students_endpoint = f"{supabase_url}/rest/v1/students"
    enrollments_endpoint = f"{supabase_url}/rest/v1/enrollments"

    # Step A: Upsert students
    student_payload = [
        {
            "rut_lookup": compute_rut_lookup(r["rut_normalized"], rut_secret),
            "rut_masked": format_rut_masked(r["rut_normalized"]),
            "display_name": r["display_name"],
            "active": True,
            "updated_at": "now()",
        }
        for r in valid_records
    ]

    status, inserted_students = make_request(
        f"{students_endpoint}?on_conflict=rut_lookup",
        "POST",
        service_key,
        student_payload,
    )
    print(f"[OK] {len(inserted_students or [])} estudiantes registrados o actualizados.")

    # Step B: Map student_id and upsert enrollments
    # Fetch all students matching these lookups to obtain their UUIDs
    lookup_list = [f'"{compute_rut_lookup(r["rut_normalized"], rut_secret)}"' for r in valid_records]
    lookup_filter = ",".join(lookup_list)
    _, fetched_students = make_request(
        f"{students_endpoint}?rut_lookup=in.({lookup_filter})&select=student_id,rut_lookup",
        "GET",
        service_key,
    )

    lookup_to_id = {s["rut_lookup"]: s["student_id"] for s in (fetched_students or [])}

    enrollment_payload = []
    for r in valid_records:
        lookup_val = compute_rut_lookup(r["rut_normalized"], rut_secret)
        s_id = lookup_to_id.get(lookup_val)
        if s_id:
            enrollment_payload.append({
                "course_id": course_id,
                "student_id": s_id,
                "section": r["section"],
                "role": r.get("role", "student"),
                "active": True,
            })

    status, inserted_enrollments = make_request(
        f"{enrollments_endpoint}?on_conflict=course_id,student_id",
        "POST",
        service_key,
        enrollment_payload,
    )
    print(f"[OK] {len(inserted_enrollments or [])} matrículas asociadas al curso '{course_id}'.")
    print("\nProceso de importación de nómina completado con éxito.")


def main():
    # Load .env / .env.local if present
    load_env_file(ROOT_DIR / ".env")
    load_env_file(ROOT_DIR / ".env.local")

    default_csv = ROOT_DIR / "data" / "roster.csv"
    if not default_csv.exists():
        default_csv = ROOT_DIR / "data" / "roster.example.csv"

    parser = argparse.ArgumentParser(description="Importar nómina de estudiantes en Social R.")
    parser.add_argument("--file", "-f", type=Path, default=default_csv, help="Ruta al archivo CSV de nómina.")
    parser.add_argument("--course", "-c", type=str, default="intro-r", help="ID del curso (por defecto: intro-r).")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Simula la validación sin escribir en la BD.")
    parser.add_argument("--secret", "-s", type=str, default=None, help="Clave secreta RUT_SECRET_KEY.")

    args = parser.parse_args()
    import_roster(args.file, args.course, args.dry_run, args.secret)


if __name__ == "__main__":
    main()
