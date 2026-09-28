#!/usr/bin/env python3
"""
Social R — End-to-End Cloud Progress Smoke Test Tool
Tests the complete remote student flow against Supabase Edge Functions
using ONLY client-side permissions (Publishable Key + Bearer Token).

CRITICAL SECURITY RULES:
- Never prints full RUT, session tokens, or API keys.
- Never uses SUPABASE_SECRET_KEY for student simulation.
- Outputs discrete status lines: STEP: PASS / FAIL.
"""

import argparse
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

# Canonical Course Identifiers for Module 1
TEST_COURSE_ID = "intro-r"
TEST_EXERCISE_ID = "intro-r-01-001"
TEST_MODULE_ID = "01-empezar-a-pensar-con-r"
TEST_CHALLENGE_ID = "intro-r-01-challenge"


def load_env(env_path: Path) -> dict:
    """Loads environment variables without subshell evaluation."""
    env = {}
    if not env_path.exists():
        return env
    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env


def http_request(url: str, method: str, headers: dict, body: dict = None) -> tuple[int, dict]:
    """Performs an HTTP request and returns (status_code, json_body)."""
    encoded_body = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=encoded_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return resp.status, json.loads(data) if data else {}
    except urllib.error.HTTPError as e:
        err_data = e.read().decode("utf-8")
        parsed = {}
        try:
            parsed = json.loads(err_data)
        except Exception:
            parsed = {"raw": err_data}
        return e.code, parsed


def run_smoke_test(rut: str, course_id: str = TEST_COURSE_ID) -> bool:
    env = load_env(ROOT_DIR / ".env")
    supabase_url = (env.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL", "")).rstrip("/")
    publishable_key = (env.get("SUPABASE_PUBLISHABLE_KEY") or os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")).strip()

    print("=" * 60)
    print("SOCIAL R — CLOUD PROGRESS SMOKE TEST")
    print("=" * 60)
    print(f"Curso:             {course_id}")
    print(f"Ejercicio M01:     {TEST_EXERCISE_ID}")
    print(f"Desafio M01:       {TEST_CHALLENGE_ID}")
    print(f"RUT de prueba:     [MASKED]")
    print("-" * 60)

    if not supabase_url or not publishable_key:
        print("[FAIL] Error: SUPABASE_URL o SUPABASE_PUBLISHABLE_KEY faltan en .env.", file=sys.stderr)
        return False

    base_url = f"{supabase_url}/functions/v1"
    session_token = None
    all_passed = True

    # --------------------------------------------------------------------------
    # 1. student-login
    # --------------------------------------------------------------------------
    print("1. Invocando student-login...", end=" ", flush=True)
    login_url = f"{base_url}/student-login"
    login_headers = {
        "Content-Type": "application/json",
        "apikey": publishable_key,
    }
    status, login_res = http_request(
        login_url,
        "POST",
        login_headers,
        {"rut": rut, "courseId": course_id},
    )

    if status == 200 and "sessionToken" in login_res:
        session_token = login_res["sessionToken"]
        student = login_res.get("student", {})
        display_name = student.get("displayName", "Desconocido")
        masked_rut = student.get("rutMasked", "[MASKED]")
        print(f"[PASS] (Estudiante: {display_name} | {masked_rut})")
    else:
        print(f"[FAIL] (HTTP {status}: {login_res.get('message', login_res.get('error', 'Error'))})")
        return False

    # --------------------------------------------------------------------------
    # 2. Verificar sesion emitida
    # --------------------------------------------------------------------------
    print("2. Verificando estructura de sesion...", end=" ", flush=True)
    if session_token and len(session_token) > 20 and login_res.get("expiresAt"):
        print("[PASS] (Token opaco emitido con expiracion futura)")
    else:
        print("[FAIL] (Token invalido o estructura incorrecta)")
        return False

    auth_headers = {
        "Authorization": f"Bearer {session_token}",
        "apikey": publishable_key,
    }

    # --------------------------------------------------------------------------
    # 3 & 4. student-progress-get (inicialmente vacio)
    # --------------------------------------------------------------------------
    print("3. Recuperando progreso inicial (debe estar vacio)...", end=" ", flush=True)
    get_url = f"{base_url}/student-progress-get?courseId={course_id}"
    status, get_res = http_request(get_url, "GET", auth_headers)

    if status == 200:
        completed = get_res.get("completedExercises", [])
        challenges = get_res.get("challenges", {})
        if len(completed) == 0 and len(challenges) == 0:
            print("[PASS] (Progreso remoto limpio)")
        else:
            print(f"[AVISO] Progreso previo detectado ({len(completed)} ejercicios). Se restablecera.")
    else:
        print(f"[FAIL] (HTTP {status})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 5. student-progress-sync (1 ejercicio de practica)
    # --------------------------------------------------------------------------
    print(f"4. Sincronizando ejercicio de practica '{TEST_EXERCISE_ID}'...", end=" ", flush=True)
    sync_url = f"{base_url}/student-progress-sync"
    sync_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_token}",
        "apikey": publishable_key,
    }
    sync_payload = {
        "courseId": course_id,
        "completedExercises": [TEST_EXERCISE_ID],
    }
    status, sync_res = http_request(sync_url, "POST", sync_headers, sync_payload)

    if status == 200 and sync_res.get("success"):
        print("[PASS]")
    else:
        print(f"[FAIL] (HTTP {status})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 6. student-progress-get (verificar persistencia de ejercicio)
    # --------------------------------------------------------------------------
    print(f"5. Verificando persistencia de '{TEST_EXERCISE_ID}'...", end=" ", flush=True)
    status, get_res = http_request(get_url, "GET", auth_headers)
    completed = get_res.get("completedExercises", []) if status == 200 else []

    if status == 200 and TEST_EXERCISE_ID in completed:
        print("[PASS]")
    else:
        print(f"[FAIL] (Ejercicio no encontrado en progreso remoto: {completed})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 7. student-progress-sync (1 desafio modular)
    # --------------------------------------------------------------------------
    print(f"6. Sincronizando desafio '{TEST_CHALLENGE_ID}' como passed...", end=" ", flush=True)
    ch_payload = {
        "courseId": course_id,
        "challenges": {
            TEST_MODULE_ID: {
                "status": "passed",
                "challengeId": TEST_CHALLENGE_ID,
            }
        },
    }
    status, sync_res = http_request(sync_url, "POST", sync_headers, ch_payload)

    if status == 200 and sync_res.get("success"):
        print("[PASS]")
    else:
        print(f"[FAIL] (HTTP {status})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 8. student-progress-get (verificar independencia ejercicio vs desafio)
    # --------------------------------------------------------------------------
    print("7. Verificando independencia de ejercicio y desafio...", end=" ", flush=True)
    status, get_res = http_request(get_url, "GET", auth_headers)
    completed = get_res.get("completedExercises", []) if status == 200 else []
    challenges = get_res.get("challenges", {}) if status == 200 else {}
    ch_state = challenges.get(TEST_MODULE_ID, {}).get("status")

    if status == 200 and TEST_EXERCISE_ID in completed and ch_state == "passed":
        print("[PASS] (Ambos hechos persisten de forma independiente)")
    else:
        print(f"[FAIL] (Inconsistencia: completed={completed}, challenge={ch_state})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 9. student-reset (reinicio del progreso en la nube)
    # --------------------------------------------------------------------------
    print("8. Ejecutando student-reset...", end=" ", flush=True)
    reset_url = f"{base_url}/student-reset"
    reset_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_token}",
        "apikey": publishable_key,
    }
    status, reset_res = http_request(reset_url, "POST", reset_headers, {"courseId": course_id})

    if status == 200 and reset_res.get("success"):
        print("[PASS]")
    else:
        print(f"[FAIL] (HTTP {status})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 10. student-progress-get (verificar progreso vacio post-reset)
    # --------------------------------------------------------------------------
    print("9. Verificando progreso post-reset (debe estar vacio)...", end=" ", flush=True)
    status, get_res = http_request(get_url, "GET", auth_headers)
    completed = get_res.get("completedExercises", []) if status == 200 else [1]
    challenges = get_res.get("challenges", {}) if status == 200 else {1: 1}

    if status == 200 and len(completed) == 0 and len(challenges) == 0:
        print("[PASS] (Progreso completamente limpio)")
    else:
        print(f"[FAIL] (Progreso remanente tras reset: {completed}, {challenges})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 11. student-logout (cierre de sesion)
    # --------------------------------------------------------------------------
    print("10. Ejecutando student-logout...", end=" ", flush=True)
    logout_url = f"{base_url}/student-logout"
    status, logout_res = http_request(logout_url, "POST", auth_headers)

    if status == 200 and logout_res.get("success"):
        print("[PASS]")
    else:
        print(f"[FAIL] (HTTP {status})")
        all_passed = False

    # --------------------------------------------------------------------------
    # 12. Verificar rechazo de sesion revocada (401)
    # --------------------------------------------------------------------------
    print("11. Verificando rechazo con sesion revocada (401 esperado)...", end=" ", flush=True)
    status, revoked_res = http_request(get_url, "GET", auth_headers)

    if status == 401:
        print("[PASS] (Sesion revocada correctamente rechazada por Edge Function)")
    else:
        print(f"[FAIL] (Se esperaba HTTP 401 pero se obtuvo HTTP {status})")
        all_passed = False

    print("-" * 60)
    if all_passed:
        print("[EXITO] Todos los pasos del smoke test remoto pasaron satisfactoriamente.")
        return True
    else:
        print("[ERROR] Uno o mas pasos del smoke test fallaron.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Smoke test end-to-end seguro de Cloud Progress.")
    parser.add_argument("--rut", "-r", type=str, default=None, help="RUT del estudiante sintetico a probar.")
    parser.add_argument("--file", "-f", type=Path, default=None, help="Archivo CSV con el RUT de prueba.")
    parser.add_argument("--course", "-c", type=str, default=TEST_COURSE_ID, help="ID del curso (intro-r).")
    parser.add_argument("--dry-run-check", action="store_true", help="Valida sintaxis y entorno sin conectar a la red.")

    args = parser.parse_args()

    if args.dry_run_check:
        env = load_env(ROOT_DIR / ".env")
        has_url = bool(env.get("SUPABASE_URL"))
        has_pub = bool(env.get("SUPABASE_PUBLISHABLE_KEY"))
        print("[OK] scripts/smoke_test_cloud.py: Sintaxis valida y configuracion local lista.")
        print(f"  SUPABASE_URL presente:             {'YES' if has_url else 'NO'}")
        print(f"  SUPABASE_PUBLISHABLE_KEY presente: {'YES' if has_pub else 'NO'}")
        print(f"  Modulo 1 Ejercicio Canónico:       {TEST_EXERCISE_ID}")
        print(f"  Modulo 1 Desafio Canónico:         {TEST_CHALLENGE_ID}")
        sys.exit(0)

    target_rut = args.rut or os.environ.get("SYNTHETIC_RUT")

    if not target_rut and args.file and args.file.exists():
        import csv
        with open(args.file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            first_row = next(reader, None)
            if first_row:
                rut_col = next((c for c in first_row if "rut" in c.lower()), None)
                if rut_col:
                    target_rut = first_row[rut_col]

    if not target_rut:
        print("Error: Proporciona el RUT sintetico mediante --rut, --file o variable SYNTHETIC_RUT.", file=sys.stderr)
        print("Usa --dry-run-check para validar la herramienta sin invocar la red.", file=sys.stderr)
        sys.exit(1)

    success = run_smoke_test(target_rut, args.course)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
