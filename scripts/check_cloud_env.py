#!/usr/bin/env python3
"""
Social R — Verificador Local Seguro de Variables de Entorno Cloud (.env)
Valida únicamente la presencia y formato estructural de las credenciales de Supabase.

REGLA DE SEGURIDAD ABSOLUTA:
NUNCA imprime ni exporta los valores de las claves. Solo reporta el estado (OK / MISSING / INVALID).
"""

import argparse
import sys
from pathlib import Path

# Configurar encoding UTF-8 seguro para consolas Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent


def parse_env_file(filepath: Path) -> dict:
    """Lee un archivo .env y extrae pares clave-valor sin procesar subshells."""
    env = {}
    if not filepath.exists():
        return env

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                # Quitar comillas si existen
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                env[key] = val
    return env


def check_env(env_path: Path = None) -> bool:
    target = env_path or (ROOT_DIR / ".env")
    print(f"Validando configuracion local en: {target.name}")
    print("-" * 60)

    if not target.exists():
        print(f"[ERROR] Archivo {target.name} no encontrado en {target.parent}.")
        print("Copia la plantilla con: cp .env.example .env")
        return False

    env = parse_env_file(target)
    all_ok = True

    # 1. SUPABASE_URL
    url = env.get("SUPABASE_URL", "")
    if not url:
        print("  SUPABASE_URL:             MISSING (vacia)")
        all_ok = False
    elif not url.startswith("https://") or ".supabase.co" not in url:
        print("  SUPABASE_URL:             INVALID (debe iniciar con 'https://' y contener '.supabase.co')")
        all_ok = False
    else:
        print("  SUPABASE_URL:             OK")

    # 2. SUPABASE_PUBLISHABLE_KEY
    pub_key = env.get("SUPABASE_PUBLISHABLE_KEY", "")
    if not pub_key:
        print("  SUPABASE_PUBLISHABLE_KEY: MISSING (vacia)")
        all_ok = False
    elif not pub_key.startswith("sb_publishable_"):
        print("  SUPABASE_PUBLISHABLE_KEY: INVALID (debe comenzar con 'sb_publishable_')")
        all_ok = False
    else:
        print("  SUPABASE_PUBLISHABLE_KEY: OK")

    # 3. SUPABASE_SECRET_KEY
    sec_key = env.get("SUPABASE_SECRET_KEY", "")
    if not sec_key:
        print("  SUPABASE_SECRET_KEY:      MISSING (vacia)")
        all_ok = False
    elif not sec_key.startswith("sb_secret_"):
        print("  SUPABASE_SECRET_KEY:      INVALID (debe comenzar con 'sb_secret_')")
        all_ok = False
    else:
        print("  SUPABASE_SECRET_KEY:      OK")

    # 4. RUT_SECRET_KEY
    rut_sec = env.get("RUT_SECRET_KEY", "")
    if not rut_sec:
        print("  RUT_SECRET_KEY:           MISSING (vacia)")
        all_ok = False
    elif len(rut_sec) < 32:
        print("  RUT_SECRET_KEY:           INVALID (minimo 32 caracteres requeridos)")
        all_ok = False
    else:
        print("  RUT_SECRET_KEY:           OK")

    # 5. Parametros de Curso y Feature Flag
    cloud_sync = env.get("CLOUD_SYNC_ENABLED", "").lower()
    if cloud_sync in ("false", "0", "no"):
        print("  CLOUD_SYNC_ENABLED:       OK (false - cloud apagado)")
    elif cloud_sync in ("true", "1", "yes"):
        print("  CLOUD_SYNC_ENABLED:       OK (true - cloud activado)")
    else:
        print("  CLOUD_SYNC_ENABLED:       MISSING / DEFAULT (false asumido)")

    drafts = env.get("SYNC_DRAFTS_TO_CLOUD", "false").lower()
    print(f"  SYNC_DRAFTS_TO_CLOUD:     OK ({drafts})")

    course_id = env.get("COURSE_ID", "intro-r")
    print(f"  COURSE_ID:                OK ({course_id})")

    print("-" * 60)

    if all_ok:
        print("[OK] Todas las credenciales requeridas estan presentes y con formato valido.")
        print("(Privacidad preservada: ningun valor sensible fue expuesto)")
        return True
    else:
        print("[AVISO] Faltan credenciales o tienen formato incompleto en tu archivo .env.")
        print("Por favor edita tu archivo .env local con tus valores de Supabase.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Verificador seguro de credenciales locales de Supabase.")
    parser.add_argument("--file", "-f", type=Path, default=None, help="Ruta alternativa al archivo .env.")
    args = parser.parse_args()

    success = check_env(args.file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
