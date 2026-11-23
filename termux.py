#!/usr/bin/env python3
"""DeveloperHCR HCRAPP Termux launcher.

termux.py is the ONLY main launcher for the Termux/local version.
It shows the startup interface and initializes the localhost-only local service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional


APP_NAME = "DeveloperHCR HCRAPP Termux Launcher"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3383
DEFAULT_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent


def get_xdg_config_base() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return Path(base) if base else (Path.home() / ".config")


def get_xdg_state_base() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    return Path(base) if base else (Path.home() / ".local" / "state")


def get_termux_config_path() -> Path:
    return get_xdg_config_base() / "developerhcr" / "hcrapp_termux_setup.json"


def get_local_dir() -> Path:
    p = get_xdg_config_base() / "developerhcr" / "hcrapp_local"
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_local_admin_path() -> Path:
    return get_local_dir() / "admin.json"


def get_local_state_dir() -> Path:
    p = get_xdg_state_base() / "developerhcr" / "hcrapp_local"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _safe_write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def _load_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _stdout_supports_unicode() -> bool:
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        "DeveloperHCR™".encode(enc)
        return True
    except Exception:
        return False


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


class UI:
    def __init__(self) -> None:
        self.tm = "™" if _stdout_supports_unicode() else "(TM)"
        self.color = _supports_color()
        self.width = max(40, min(shutil.get_terminal_size((80, 24)).columns, 92))

    def _ansi(self, code: str, text: str) -> str:
        if not self.color:
            return text
        return f"\033[{code}m{text}\033[0m"

    def bold(self, t: str) -> str:
        return self._ansi("1", t)

    def cyan(self, t: str) -> str:
        return self._ansi("36", t)

    def dim(self, t: str) -> str:
        return self._ansi("2", t)

    @staticmethod
    def _vlen(text: str) -> int:
        return len(re.sub(r"\033\[[0-9;]*m", "", text))

    def center(self, text: str) -> str:
        pad = max(0, (self.width - self._vlen(text)) // 2)
        return (" " * pad) + text

    def line(self, text: str = "", center: bool = False) -> None:
        print(self.center(text) if center else text)

    def blank(self, n: int = 1) -> None:
        for _ in range(n):
            print()


def load_termux_config() -> Dict[str, Any]:
    cfg = _load_json(get_termux_config_path(), {})
    if not isinstance(cfg, dict):
        cfg = {}
    cfg.setdefault("name", "USER")
    cfg.setdefault("first_time_completed", False)
    cfg.setdefault("admin_password_configurable", True)
    return cfg


def save_termux_config(cfg: Dict[str, Any]) -> None:
    _safe_write_json(get_termux_config_path(), cfg)


def ensure_local_admin_config() -> None:
    """Ensure local admin config exists (password configurable, not required by default)."""
    path = get_local_admin_path()
    data = _load_json(path, None)
    if isinstance(data, dict) and "password_required" in data:
        return
    # Migrate/initialize: no hard-coded production password. Default = not required.
    if isinstance(data, dict) and data.get("password_hash") and data.get("salt"):
        # Preserve existing configured password state.
        data.setdefault("password_required", True)
        data.setdefault("updated_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        _safe_write_json(path, data)
        return
    init = {
        "password_required": False,
        "salt": "",
        "password_hash": "",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Admin password is configurable. Set it from Local Setup if needed.",
    }
    _safe_write_json(path, init)


def is_port_open(host: str, port: int, timeout: float = 0.4) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def find_local_service_script() -> Path:
    return get_repo_root() / "pages" / "notinwebsite" / "local.py"


def start_local_service(port: int = DEFAULT_PORT) -> Dict[str, Any]:
    script = find_local_service_script()
    if not script.exists():
        return {"ok": False, "message": f"Local service script not found: {script}"}
    if is_port_open(DEFAULT_HOST, port):
        return {"ok": True, "message": "Local service already running", "already_running": True}

    log_path = get_local_state_dir() / "launcher.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        log_f = open(log_path, "a", encoding="utf-8")
    except Exception:
        log_f = subprocess.DEVNULL

    cmd = [sys.executable, str(script), "--host", DEFAULT_HOST, "--port", str(port)]
    kwargs: Dict[str, Any] = {
        "stdout": log_f if log_f is not subprocess.DEVNULL else subprocess.DEVNULL,
        "stderr": subprocess.STDOUT if log_f is not subprocess.DEVNULL else subprocess.DEVNULL,
        "cwd": str(get_repo_root()),
        "close_fds": True,
    }
    if os.name == "nt":
        kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    else:
        kwargs["start_new_session"] = True

    try:
        proc = subprocess.Popen(cmd, **kwargs)
        for _ in range(24):
            if is_port_open(DEFAULT_HOST, port):
                return {"ok": True, "message": "Local service started", "pid": proc.pid, "already_running": False}
            if proc.poll() is not None:
                return {"ok": False, "message": f"Local service exited early (code {proc.returncode}). Check {log_path}"}
            time.sleep(0.15)
        if is_port_open(DEFAULT_HOST, port):
            return {"ok": True, "message": "Local service started", "pid": proc.pid, "already_running": False}
        return {"ok": False, "message": f"Local service did not become ready on {DEFAULT_HOST}:{port}. Check {log_path}"}
    except Exception as e:
        return {"ok": False, "message": f"Failed to start local service: {e}"}


def render_interface(ui: UI, name: str, service_status: str, port: int = DEFAULT_PORT) -> None:
    url = f"http://{DEFAULT_HOST}:{port}"
    title = f"DeveloperHCR{ui.tm}"
    rows = [
        ui.bold(ui.cyan(title)),
        ui.bold("First Time Setup"),
        "",
        f"Name: {name}",
        "Password: NOT REQUIRED / configurable",
        "",
        f"Local Server: {url}",
        "Admin: Protected",
        "",
        f"Service: {service_status}",
    ]
    ui.blank(1)
    content_width = max(ui._vlen(r) for r in rows if r)
    pad = max(0, (ui.width - content_width) // 2)
    indent = " " * pad
    for r in rows:
        if r == "":
            ui.blank(1)
        else:
            print(indent + r)
    ui.blank(1)
    ui.line(ui.dim("Local service: pages/notinwebsite/local.py (localhost only)"), center=True)
    ui.line(ui.dim("Public GitHub Pages provides interface/links only and does not execute Python."), center=True)
    ui.blank(1)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="DeveloperHCR Termux launcher (local service initializer)")
    p.add_argument("--show", action="store_true", help="Show interface/status without starting service")
    p.add_argument("--setup", action="store_true", help="Run/setup and initialize local service")
    p.add_argument("--no-start", action="store_true", help="Do not start local service")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Local service port (default: 3383)")
    p.add_argument("--name", default=None, help="Set display name for setup")
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    port = int(args.port or DEFAULT_PORT)
    ui = UI()
    cfg = load_termux_config()
    if args.name:
        cfg["name"] = (args.name or "USER").strip() or "USER"
    if not cfg.get("name"):
        cfg["name"] = "USER"

    ensure_local_admin_config()

    service_result = {"ok": True, "message": "not started (--show/--no-start)"}
    should_start = (not args.show) and (not args.no_start)
    if should_start:
        service_result = start_local_service(port=port)

    running = is_port_open(DEFAULT_HOST, port)
    if service_result.get("already_running"):
        status_text = "already running"
    elif should_start and service_result.get("ok"):
        status_text = service_result.get("message", "running" if running else "started")
    elif should_start and not service_result.get("ok"):
        status_text = f"error: {service_result.get('message', 'unknown')}"
    else:
        status_text = "running" if running else "not running"

    render_interface(ui, name=str(cfg.get("name") or "USER"), service_status=status_text, port=port)

    cfg["first_time_completed"] = True
    cfg["last_local_url"] = f"http://{DEFAULT_HOST}:{port}"
    cfg["last_service_status"] = status_text
    save_termux_config(cfg)

    if should_start and not service_result.get("ok"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
