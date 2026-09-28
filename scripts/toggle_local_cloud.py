#!/usr/bin/env python3
"""
Social R — Local Cloud Override CLI Tool (Paso 7B)
Manages the git-ignored local development override file `.local_cloud_override.json`.

CRITICAL SAFETY RULES:
- Only for development on localhost / 127.0.0.1 / ::1.
- Production configuration in docs/ and public git history is NEVER modified to true.
- `.local_cloud_override.json` MUST remain untracked by Git.
- `syncDraftsToCloud` MUST ALWAYS remain false.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Safe encoding configuration for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
OVERRIDE_FILE = ROOT_DIR / ".local_cloud_override.json"


def is_git_ignored(path: Path) -> bool:
    """Verifies that the target path is ignored by git."""
    try:
        res = subprocess.run(
            ["git", "check-ignore", str(path)],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
        )
        return res.returncode == 0
    except Exception:
        return False


def get_status() -> dict:
    """Returns the current state of local cloud override."""
    ignored = is_git_ignored(OVERRIDE_FILE)
    if not OVERRIDE_FILE.exists():
        return {
            "active": False,
            "file_exists": False,
            "git_ignored": ignored,
            "details": None,
        }
    try:
        data = json.loads(OVERRIDE_FILE.read_text(encoding="utf-8"))
        return {
            "active": bool(data.get("cloudProgressEnabled", False)),
            "file_exists": True,
            "git_ignored": ignored,
            "details": data,
        }
    except Exception as e:
        return {
            "active": False,
            "file_exists": True,
            "git_ignored": ignored,
            "error": str(e),
        }


def enable_override() -> bool:
    """Enables local development cloud override."""
    payload = {
        "cloudProgressEnabled": True,
        "cloudSyncEnabled": True,
        "syncDraftsToCloud": False,
        "restrictedTo": ["localhost", "127.0.0.1", "::1", "[::1]"],
        "note": "LOCAL DEV ONLY. Strictly ignored on non-localhost hosts such as karavena.github.io",
    }
    OVERRIDE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if not is_git_ignored(OVERRIDE_FILE):
        print(f"[WARN] {OVERRIDE_FILE.name} is NOT ignored by Git! Check .gitignore.", file=sys.stderr)
    print(f"[OK] Local cloud override enabled in {OVERRIDE_FILE.name}.")
    print("     Restricted to: localhost, 127.0.0.1, ::1")
    return True


def disable_override() -> bool:
    """Disables local development cloud override."""
    if OVERRIDE_FILE.exists():
        OVERRIDE_FILE.unlink()
        print(f"[OK] Local cloud override disabled. Removed {OVERRIDE_FILE.name}.")
    else:
        print("[OK] Local cloud override is already disabled.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Manage local development cloud override.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--enable", action="store_true", help="Enable local cloud override for localhost.")
    group.add_argument("--disable", action="store_true", help="Disable local cloud override.")
    group.add_argument("--status", action="store_true", help="Show current local cloud override status (default).")

    args = parser.parse_args()

    if args.enable:
        enable_override()
    elif args.disable:
        disable_override()
    else:
        status = get_status()
        print("=== LOCAL CLOUD OVERRIDE STATUS ===")
        print(f"Override Active:     {'YES' if status['active'] else 'NO'}")
        print(f"Override File:       {OVERRIDE_FILE.name} ({'EXISTS' if status['file_exists'] else 'NOT FOUND'})")
        print(f"Git Ignored:         {'YES' if status['git_ignored'] else 'NO'}")
        if status.get("details"):
            print(f"Allowed Hosts:       {status['details'].get('restrictedTo')}")
            print(f"cloudProgressEnabled: {status['details'].get('cloudProgressEnabled')}")
            print(f"syncDraftsToCloud:   {status['details'].get('syncDraftsToCloud')}")


if __name__ == "__main__":
    main()
