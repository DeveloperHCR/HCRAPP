"""Connection and local setup data helpers for DeveloperHCR Termux setup."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


DEFAULT_PORT = 3383
DEFAULT_HOST = "127.0.0.1"
DEFAULT_URL = f"http://localhost:{DEFAULT_PORT}"


def get_repo_root() -> Path:
    # .backend/Main/Data/connecte.py -> repo root
    return Path(__file__).resolve().parents[3]


def get_data_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        root = Path(base)
    else:
        root = Path.home() / ".config"
    path = root / "developerhcr" / "hcrapp_web_setup"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_setup_data_path() -> Path:
    return get_data_dir() / "setup_data.json"


def load_setup_data() -> Dict[str, Any]:
    path = get_setup_data_path()
    if not path.exists():
        return {"username": "", "password": "", "completed": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("invalid data")
        return {
            "username": str(data.get("username", "") or ""),
            "password": str(data.get("password", "") or ""),
            "completed": bool(data.get("completed", False)),
        }
    except Exception:
        return {"username": "", "password": "", "completed": False}


def save_setup_data(username: str, password: str) -> Dict[str, Any]:
    data = {
        "username": (username or "").strip(),
        "password": password or "",
        "completed": True,
    }
    path = get_setup_data_path()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass
    return data


def status_text() -> str:
    data = load_setup_data()
    user = data.get("username") or "(not set)"
    pwd = "set" if data.get("password") else "not set"
    done = "yes" if data.get("completed") else "no"
    return f"completed={done}, username={user}, password={pwd}"
