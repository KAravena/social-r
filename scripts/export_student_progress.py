#!/usr/bin/env python3
"""
Social R — Teacher Progress Export Utility
Connects to Supabase using the service role key and extracts student progress
from the 'teacher_progress_summary' view into a clean CSV for teaching follow-up.

Usage:
  python scripts/export_student_progress.py [--course intro-r] [--output exports/progress.csv] [--section 1]
"""

import argparse
import csv
import datetime
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Safe encoding configuration for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.rut_utils import format_rut, compute_rut_lookup, normalize_rut
from scripts.import_roster import parse_roster_csv


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


def make_request(url: str, service_key: str):
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else []
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code} Error: {err_body}") from e


def export_progress(course_id: str, output_path: Path, section_filter: str = None, roster_path: Path = None, secret: str = None, include_test: bool = False):
    print("=" * 60)
    print("SOCIAL R — EXPORTACIÓN DOCENTE DE PROGRESO DE ESTUDIANTES")
    print("=" * 60)
    print(f"Curso:      {course_id}")
    if section_filter:
        print(f"Sección:    {section_filter}")
    print(f"Destino:    {output_path}")
    print(f"Incluir TEST: {'SÍ' if include_test else 'NO (por defecto)'}")
    print("-" * 60)

    # 1. Check credentials (Modern Supabase 2026: SUPABASE_SECRET_KEY; legacy fallback isolated)
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    service_key = (os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")).strip()

    if not supabase_url or not service_key:
        print("\nError: Faltan variables de entorno requeridas:", file=sys.stderr)
        if not supabase_url:
            print("  - SUPABASE_URL", file=sys.stderr)
        if not service_key:
            print("  - SUPABASE_SECRET_KEY", file=sys.stderr)
        print("Por favor configura tu archivo .env o variables de entorno.", file=sys.stderr)
        sys.exit(1)

    # 2. Local roster reconciliation for zero-trust privacy
    rut_secret = (secret or os.environ.get("RUT_SECRET_KEY") or os.environ.get("RUT_LOOKUP_SECRET", "")).strip()
    lookup_to_rut = {}
    name_to_rut = {}

    roster_file = roster_path
    if not roster_file:
        cand = ROOT_DIR / "data" / "roster.csv"
        if cand.exists():
            roster_file = cand

    if roster_file and roster_file.exists():
        try:
            roster_records, _ = parse_roster_csv(roster_file)
            if rut_secret:
                lookup_to_rut = {
                    compute_rut_lookup(r["rut_normalized"], rut_secret): format_rut(r["rut_normalized"])
                    for r in roster_records
                }
            name_to_rut = {
                (r["display_name"].strip().lower(), r["section"].strip()): format_rut(r["rut_normalized"])
                for r in roster_records
            }
            print(f"[OK] Nómina local vinculada: {roster_file} ({len(roster_records)} estudiantes).")
            if not rut_secret:
                print("  (Aviso: Sin RUT_SECRET_KEY, reconciliando por Nombre + Sección)")
        except Exception as e:
            print(f"Aviso: No se pudo leer nómina local ({e}). Se usarán RUTs enmascarados.")
    else:
        print("Aviso: No se especificó nómina local. Se exportará con RUT enmascarado para preservar privacidad.")

    # 3. Query view teacher_progress_summary
    query_params = [f"course_id=eq.{course_id}"]
    if section_filter:
        query_params.append(f"section=eq.{section_filter}")
    query_params.append("order=section.asc,display_name.asc")

    url = f"{supabase_url}/rest/v1/teacher_progress_summary?{'&'.join(query_params)}"

    print("Consultando resumen de progreso en Supabase...")
    try:
        status, records = make_request(url, service_key)
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}", file=sys.stderr)
        sys.exit(1)

    total_db_records = len(records)
    # Exclude TEST, TEST-PILOT, TEST-ADMIN by default unless explicitly included or filtered
    if not include_test and not (section_filter and section_filter.upper().startswith("TEST")):
        records = [r for r in records if not str(r.get("section", "")).upper().startswith("TEST")]
        excluded_test_count = total_db_records - len(records)
        if excluded_test_count > 0:
            print(f"  (Aviso: {excluded_test_count} registros de secciones TEST* excluidos del reporte académico. Usa --include-test para verlos.)")

    print(f"Estudiantes a exportar: {len(records)} (de {total_db_records} totales en BD)")

    # 4. Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 5. Write CSV
    headers = [
        "RUT",
        "Nombre",
        "Sección",
        "Ejercicios completados",
        "% Ejercicios",
        "Desafíos acreditados",
        "Módulos acreditados",
        "Primer acceso",
        "Última actividad",
    ]

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for r in records:
            lookup_val = r.get("rut_lookup")
            display_name = r.get("display_name", "")
            section = r.get("section", "")

            # Reconcile full RUT locally if roster available, else masked RUT
            if lookup_val and lookup_val in lookup_to_rut:
                resolved_rut = lookup_to_rut[lookup_val]
            elif (display_name.strip().lower(), section.strip()) in name_to_rut:
                resolved_rut = name_to_rut[(display_name.strip().lower(), section.strip())]
            else:
                resolved_rut = r.get("rut_masked") or "••.•••.•••-•"

            first_login = r.get("first_login")
            last_activity = r.get("last_activity")

            # Format ISO timestamps nicely if present
            first_login_str = first_login[:19].replace("T", " ") if first_login else "Sin acceso"
            last_activity_str = last_activity[:19].replace("T", " ") if last_activity else "Sin actividad"

            writer.writerow([
                resolved_rut,
                display_name,
                section,
                r.get("completed_exercises", 0),
                f"{r.get('exercise_percent', 0.0)}%",
                r.get("passed_challenges", 0),
                r.get("accredited_modules", 0),
                first_login_str,
                last_activity_str,
            ])

    print(f"\n[OK] Archivo CSV generado con éxito en: {output_path}")


def main():
    load_env_file(ROOT_DIR / ".env")
    load_env_file(ROOT_DIR / ".env.local")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    default_output = ROOT_DIR / "exports" / f"progress_{today_str}.csv"

    parser = argparse.ArgumentParser(description="Exportar reporte docente de progreso estudiantil.")
    parser.add_argument("--course", "-c", type=str, default="intro-r", help="ID del curso (intro-r).")
    parser.add_argument("--output", "-o", type=Path, default=default_output, help="Ruta de salida del archivo CSV.")
    parser.add_argument("--section", "-s", type=str, default=None, help="Filtrar por sección específica.")
    parser.add_argument("--roster", "-r", type=Path, default=None, help="Ruta al archivo CSV de nómina local para des-anonimizar.")
    parser.add_argument("--secret", "-k", type=str, default=None, help="Clave secreta RUT_SECRET_KEY.")
    parser.add_argument("--include-test", action="store_true", help="Incluir cuentas de prueba y administración (secciones que inician con TEST).")

    args = parser.parse_args()
    export_progress(args.course, args.output, args.section, args.roster, args.secret, args.include_test)


if __name__ == "__main__":
    main()
