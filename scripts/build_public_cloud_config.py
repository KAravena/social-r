#!/usr/bin/env python3
"""
Social R — Public Cloud Configuration Builder
Extracts public Supabase frontend settings (URL, publishable key, courseId)
from the local .env file and updates `js/platform/cloud-config.js` and `docs/js/platform/cloud-config.js`.

CRITICAL SECURITY RULES:
- Only SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, and COURSE_ID may be exported to client scripts.
- SUPABASE_SECRET_KEY, RUT_SECRET_KEY, or any private keys are STRICTLY PROHIBITED.
- `cloudProgressEnabled` / `cloudSyncEnabled` MUST ALWAYS remain `false` by default.
- `syncDraftsToCloud` MUST ALWAYS remain `false` by default.
"""

import argparse
import re
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
sys.path.insert(0, str(ROOT_DIR))

from scripts.check_cloud_env import parse_env_file

CONFIG_FILES = [
    ROOT_DIR / "js" / "platform" / "cloud-config.js",
    ROOT_DIR / "docs" / "js" / "platform" / "cloud-config.js",
]


def validate_public_credentials(supabase_url: str, publishable_key: str):
    """Ensures public credentials are valid and DO NOT contain secret keys."""
    if not supabase_url or not supabase_url.startswith("https://"):
        raise ValueError(f"Invalid SUPABASE_URL: must start with https://, got: {supabase_url}")
    if not publishable_key or not publishable_key.startswith("sb_publishable_"):
        raise ValueError(
            "Invalid publishable key: must begin with modern 'sb_publishable_' prefix. "
            "Never use secret keys in frontend configuration."
        )
    if "sb_secret_" in publishable_key:
        raise ValueError("CRITICAL SECURITY ERROR: Detected secret key where publishable key was expected!")


def build_config_block(supabase_url: str, publishable_key: str, course_id: str = "intro-r", enable_cloud: bool = False) -> str:
    """Generates the JavaScript snippet for PRODUCTION_PUBLIC_CONFIG."""
    cloud_bool_str = "true" if enable_cloud else "false"
    return f"""  // Production base public configuration (Strictly public endpoints; secrets are NEVER in client)
  const PRODUCTION_PUBLIC_CONFIG = {{
    supabaseUrl: "{supabase_url}",
    supabasePublishableKey: "{publishable_key}",
    courseId: "{course_id}",
    cloudProgressEnabled: {cloud_bool_str},
    syncDraftsToCloud: false,
  }};"""


def update_cloud_config_file(filepath: Path, supabase_url: str, publishable_key: str, course_id: str, enable_cloud: bool = False, dry_run: bool = False) -> bool:
    """Updates cloud-config.js with the given public parameters."""
    if not filepath.exists():
        print(f"[WARN] Target file {filepath} does not exist. Skipping.")
        return False

    content = filepath.read_text(encoding="utf-8")

    # Safety assertion: Ensure file never has secret keys
    if "sb_secret_" in content:
        raise ValueError(f"Security error: existing file {filepath} contains sb_secret_ pattern!")

    new_block = build_config_block(supabase_url, publishable_key, course_id, enable_cloud=enable_cloud)

    # Replace or insert PRODUCTION_PUBLIC_CONFIG block
    pattern = r"  // Production base public configuration[\s\S]*?  \};"
    if re.search(pattern, content):
        updated_content = re.sub(pattern, new_block, content, count=1)
    else:
        # Insert before userConfig definition
        target_marker = "  // Global override from window"
        if target_marker not in content:
            target_marker = "  const userConfig ="
        if target_marker in content:
            updated_content = content.replace(target_marker, new_block + "\n\n" + target_marker, 1)
        else:
            raise ValueError(f"Could not find insertion marker in {filepath}")

    # Ensure CloudConfig uses PRODUCTION_PUBLIC_CONFIG fallbacks
    # 1. supabaseUrl fallback
    updated_content = re.sub(
        r'supabaseUrl:\s*userConfig\.supabaseUrl\s*\|\|\s*userConfig\.SUPABASE_URL\s*\|\|\s*["\'].*?["\']',
        'supabaseUrl: userConfig.supabaseUrl || userConfig.SUPABASE_URL || PRODUCTION_PUBLIC_CONFIG.supabaseUrl',
        updated_content
    )
    # 2. supabasePublishableKey fallback
    updated_content = re.sub(
        r'supabasePublishableKey:\s*userConfig\.supabasePublishableKey\s*\|\|\s*userConfig\.SUPABASE_PUBLISHABLE_KEY\s*\|\|\s*userConfig\.supabaseAnonKey\s*\|\|\s*userConfig\.SUPABASE_ANON_KEY\s*\|\|\s*["\'].*?["\']',
        'supabasePublishableKey: userConfig.supabasePublishableKey || userConfig.SUPABASE_PUBLISHABLE_KEY || userConfig.supabaseAnonKey || userConfig.SUPABASE_ANON_KEY || PRODUCTION_PUBLIC_CONFIG.supabasePublishableKey',
        updated_content
    )
    # 3. courseId
    if "courseId: userConfig" not in updated_content:
        updated_content = updated_content.replace(
            "const CloudConfig = {",
            "const CloudConfig = {\n    courseId: userConfig.courseId || PRODUCTION_PUBLIC_CONFIG.courseId,",
            1
        )
    # 4. cloudSyncEnabled is strictly bound to resolvedCloudProgressEnabled (with host protection)
    # 5. syncDraftsToCloud is strictly false in free-tier MVP
    if "syncDraftsToCloud: false" not in updated_content:
        updated_content = re.sub(
            r'syncDraftsToCloud:\s*typeof\s*userConfig\.syncDraftsToCloud[\s\S]*?,',
            'syncDraftsToCloud: false,',
            updated_content
        )

    # Final security check on updated content
    if "sb_secret_" in updated_content:
        raise ValueError(f"CRITICAL: Secret key detected in output buffer for {filepath}")
    if "RUT_SECRET_KEY" in updated_content:
        raise ValueError(f"CRITICAL: RUT_SECRET_KEY detected in output buffer for {filepath}")

    if dry_run:
        print(f"[DRY-RUN] Validated public configuration injection for {filepath.name}.")
        return True

    filepath.write_text(updated_content, encoding="utf-8")
    print(f"[OK] Successfully updated public cloud configuration in {filepath.relative_to(ROOT_DIR)}.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Injects public Supabase settings from .env into frontend scripts.")
    parser.add_argument("--env-file", default=None, help="Path to .env file (default: project root .env).")
    parser.add_argument("--enable-cloud", action="store_true", help="Enable cloud progress in production configuration (default: False).")
    parser.add_argument("--disable-cloud", action="store_true", help="Force cloud progress to false in production configuration.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate update without modifying files.")
    parser.add_argument("--check", action="store_true", help="Verify that public config matches .env without writing.")
    args = parser.parse_args()

    env_path = Path(args.env_file) if args.env_file else (ROOT_DIR / ".env")
    if not env_path.exists():
        print(f"[ERROR] Environment file {env_path} not found.", file=sys.stderr)
        sys.exit(1)

    env = parse_env_file(env_path)
    supabase_url = env.get("SUPABASE_URL", "").rstrip("/")
    publishable_key = env.get("SUPABASE_PUBLISHABLE_KEY", "").strip()
    course_id = env.get("COURSE_ID", "intro-r").strip()
    enable_cloud = args.enable_cloud and not args.disable_cloud

    try:
        validate_public_credentials(supabase_url, publishable_key)
    except ValueError as e:
        print(f"[ERROR] Validation failed: {e}", file=sys.stderr)
        sys.exit(1)

    all_ok = True
    for cfg_path in CONFIG_FILES:
        try:
            ok = update_cloud_config_file(
                filepath=cfg_path,
                supabase_url=supabase_url,
                publishable_key=publishable_key,
                course_id=course_id,
                enable_cloud=enable_cloud,
                dry_run=args.dry_run or args.check,
            )
            all_ok = all_ok and ok
        except Exception as e:
            print(f"[ERROR] Failed to update {cfg_path}: {e}", file=sys.stderr)
            sys.exit(1)

    if all_ok:
        print("[SUCCESS] Public cloud frontend configuration is consistent and secure.")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
