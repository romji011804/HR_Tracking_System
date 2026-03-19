"""
Application paths (Windows-friendly).

When packaged/installed, the app directory may be read-only (e.g. Program Files).
We store the SQLite DB and uploaded documents in a per-user writable directory.

Portable mode:
- Set environment variable MOA_SYSTEM_PORTABLE=1 to store data alongside the code.
"""

from __future__ import annotations

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent


def is_portable_mode() -> bool:
    return os.environ.get("MOA_SYSTEM_PORTABLE", "").strip() in {"1", "true", "True", "yes", "YES"}


def get_app_data_dir() -> Path:
    if is_portable_mode():
        return APP_DIR

    local_appdata = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
    if local_appdata:
        base = Path(local_appdata)
    else:
        base = Path.home() / "AppData" / "Local"

    # Keep name stable for migrations/backups
    return base / "PSU-MOA-LO-Tracking"


def ensure_data_dirs() -> dict[str, Path]:
    data_dir = get_app_data_dir()
    uploads_dir = data_dir / "uploads"
    lo_dir = uploads_dir / "lo"
    moa_dir = uploads_dir / "moa"

    data_dir.mkdir(parents=True, exist_ok=True)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    lo_dir.mkdir(parents=True, exist_ok=True)
    moa_dir.mkdir(parents=True, exist_ok=True)

    return {
        "data_dir": data_dir,
        "uploads_dir": uploads_dir,
        "lo_uploads_dir": lo_dir,
        "moa_uploads_dir": moa_dir,
    }


def get_db_path() -> Path:
    dirs = ensure_data_dirs()
    return dirs["data_dir"] / "moa_tracking.db"


def get_legacy_db_path() -> Path:
    # Older versions stored DB next to code.
    return APP_DIR / "moa_tracking.db"


def migrate_legacy_db_if_needed() -> None:
    """
    If a legacy DB exists next to the code but not in the new data dir, copy it over.
    """
    if is_portable_mode():
        return

    new_path = get_db_path()
    legacy_path = get_legacy_db_path()
    if new_path.exists() or not legacy_path.exists():
        return

    try:
        new_path.write_bytes(legacy_path.read_bytes())
    except Exception:
        # Best-effort migration; DB will be created fresh if this fails.
        pass

