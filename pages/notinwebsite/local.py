#!/usr/bin/env python3
"""DeveloperHCR local service for Termux/HCRAPP.

Runs a localhost-only admin/setup dashboard for DeveloperHCR HCRAPP.
Default bind: 127.0.0.1:3383

Security notes:
- Administrative endpoints are intended for localhost use only.
- Admin authentication is validated server-side.
- Secrets/config are stored in local user config/state paths, not in README/public site.
- No production password is hard-coded in source.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import platform
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse


APP_NAME = "DeveloperHCR Local Service"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3383
DEFAULT_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
SESSION_COOKIE = "hcrapp_admin_session"
SESSION_TTL_SECONDS = 60 * 60 * 8  # 8 hours
MAX_LOG_LINES = 500


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_repo_root() -> Path:
    # pages/notinwebsite/local.py -> repo root
    return Path(__file__).resolve().parents[2]


def get_xdg_config_base() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return Path(base) if base else (Path.home() / ".config")


def get_xdg_state_base() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    return Path(base) if base else (Path.home() / ".local" / "state")


def get_local_dir() -> Path:
    path = get_xdg_config_base() / "developerhcr" / "hcrapp_local"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_state_dir() -> Path:
    path = get_xdg_state_base() / "developerhcr" / "hcrapp_local"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_path() -> Path:
    return get_local_dir() / "config.json"


def get_admin_path() -> Path:
    return get_local_dir() / "admin.json"


def get_plugins_path() -> Path:
    return get_local_dir() / "plugins.json"


def get_log_path() -> Path:
    return get_state_dir() / "local.log"


def get_pid_path() -> Path:
    return get_state_dir() / "local.pid"


def get_backup_dir() -> Path:
    path = get_state_dir() / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path


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


def append_log(level: str, message: str) -> None:
    try:
        line = f"{utc_now_iso()} [{level.upper()}] {message}\n"
        log_path = get_log_path()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def read_log_lines(limit: int = 200) -> List[str]:
    try:
        if not get_log_path().exists():
            return []
        lines = get_log_path().read_text(encoding="utf-8", errors="replace").splitlines()
        return lines[-max(1, min(limit, MAX_LOG_LINES)) :]
    except Exception:
        return []


def default_config() -> Dict[str, Any]:
    return {
        "version": 1,
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
        "theme": "dark",
        "auto_start": False,
        "log_level": "info",
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "features": {
            "health_checks": True,
            "file_browser": True,
            "plugin_manager": True,
        },
    }


def load_config() -> Dict[str, Any]:
    cfg = _load_json(get_config_path(), None)
    if not isinstance(cfg, dict):
        cfg = default_config()
        _safe_write_json(get_config_path(), cfg)
        return cfg
    d = default_config()
    for k, v in d.items():
        if k not in cfg:
            cfg[k] = v
    if not isinstance(cfg.get("features"), dict):
        cfg["features"] = d["features"]
    return cfg


def save_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    cfg = dict(cfg)
    cfg["updated_at"] = utc_now_iso()
    _safe_write_json(get_config_path(), cfg)
    return cfg


def _hash_password(password: str, salt_hex: str) -> str:
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return dk.hex()


def _normalize_admin_data(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        data = {}
    # Migrate legacy bootstrap-derived local auth state: no hardcoded/bootstrap password by default.
    # This removes old bootstrap password hashes stored locally by previous versions.
    if str(data.get("source") or "") == "bootstrap" and os.environ.get("HCRAPP_ADMIN_PASSWORD") in (None, ""):
        data = {
            "password_required": False,
            "salt": "",
            "password_hash": "",
            "created_at": str(data.get("created_at") or utc_now_iso()),
            "updated_at": utc_now_iso(),
            "note": "Admin password is configurable. Set it from Local Setup if needed.",
        }
        return data
    # Support env override marker in runtime only; stored config stays local.
    if "password_required" not in data:
        data["password_required"] = bool(data.get("password_hash") and data.get("salt"))
    data.setdefault("salt", "")
    data.setdefault("password_hash", "")
    data.setdefault("created_at", utc_now_iso())
    data.setdefault("updated_at", utc_now_iso())
    if not bool(data.get("password_required")) and os.environ.get("HCRAPP_ADMIN_PASSWORD") in (None, ""):
        data["salt"] = ""
        data["password_hash"] = ""
    return data


def load_or_init_admin() -> Dict[str, Any]:
    data = _load_json(get_admin_path(), None)
    if not isinstance(data, dict):
        data = {
            "password_required": False,
            "salt": "",
            "password_hash": "",
            "created_at": utc_now_iso(),
            "updated_at": utc_now_iso(),
            "note": "Admin password is configurable. Set it from Local Setup if needed.",
        }
        _safe_write_json(get_admin_path(), data)
        append_log("info", "Initialized local admin configuration (password not required)")
        return data
    norm = _normalize_admin_data(data)
    if norm != data:
        _safe_write_json(get_admin_path(), norm)
    return norm


def _env_password_override() -> Optional[str]:
    env_pw = os.environ.get("HCRAPP_ADMIN_PASSWORD")
    if env_pw is None:
        return None
    if env_pw == "":
        return None
    return env_pw


def admin_password_required() -> bool:
    if _env_password_override() is not None:
        return True
    data = load_or_init_admin()
    return bool(data.get("password_required"))


def verify_admin_password(password: str) -> bool:
    env_pw = _env_password_override()
    if env_pw is not None:
        return hmac.compare_digest(password, env_pw)
    data = load_or_init_admin()
    if not bool(data.get("password_required")):
        return True  # not required/configurable (localhost-only). User may leave blank.
    salt = str(data.get("salt") or "")
    ph = str(data.get("password_hash") or "")
    if not salt or not ph:
        return False
    try:
        return hmac.compare_digest(_hash_password(password, salt), ph)
    except Exception:
        return False


def set_admin_password(new_password: str) -> Dict[str, Any]:
    """Set or disable admin password (configurable). Empty disables requirement."""
    if _env_password_override() is not None:
        return {"ok": False, "error": "Admin password is controlled by HCRAPP_ADMIN_PASSWORD environment variable."}
    if new_password is None:
        new_password = ""
    new_password = str(new_password)
    if new_password == "":
        data = {
            "password_required": False,
            "salt": "",
            "password_hash": "",
            "created_at": (load_or_init_admin().get("created_at") or utc_now_iso()),
            "updated_at": utc_now_iso(),
            "note": "Admin password is configurable. Set it from Local Setup if needed.",
        }
        _safe_write_json(get_admin_path(), data)
        append_log("info", "Admin password requirement disabled (configurable)")
        return {"ok": True, "password_required": False}
    salt = secrets.token_hex(16)
    data = {
        "password_required": True,
        "salt": salt,
        "password_hash": _hash_password(new_password, salt),
        "created_at": (load_or_init_admin().get("created_at") or utc_now_iso()),
        "updated_at": utc_now_iso(),
    }
    _safe_write_json(get_admin_path(), data)
    append_log("info", "Admin password updated (configurable)")
    return {"ok": True, "password_required": True}


def default_plugins() -> List[Dict[str, Any]]:
    return [
        {"id": "health-check", "name": "Health Check", "enabled": True, "description": "Local service and dependency health checks."},
        {"id": "log-analyzer", "name": "Log Analyzer", "enabled": True, "description": "Summarize recent local logs and warnings."},
        {"id": "backup-manager", "name": "Backup Manager", "enabled": True, "description": "Create and restore local configuration backups."},
        {"id": "file-browser", "name": "Local File Browser", "enabled": True, "description": "Browse repository files from localhost dashboard."},
        {"id": "port-checker", "name": "Port/Status Checker", "enabled": True, "description": "Inspect localhost port and service status."},
        {"id": "integrity-checker", "name": "File Integrity Checker", "enabled": True, "description": "Compute hashes for local files."},
        {"id": "config-validator", "name": "Configuration Validator", "enabled": True, "description": "Validate local configuration and paths."},
        {"id": "process-viewer", "name": "Process Viewer", "enabled": True, "description": "View process and runtime information."},
        {"id": "network-status", "name": "Network Status Viewer", "enabled": True, "description": "Inspect local interface/network counters."},
        {"id": "theme-settings", "name": "Theme Settings", "enabled": True, "description": "Manage dashboard theme preference."},
    ]


def load_plugins() -> List[Dict[str, Any]]:
    data = _load_json(get_plugins_path(), None)
    if isinstance(data, list) and data:
        # merge any new defaults by id
        existing = {str(p.get("id")): p for p in data if isinstance(p, dict) and p.get("id")}
        merged = []
        for d in default_plugins():
            if d["id"] in existing:
                item = dict(d)
                item.update({k: existing[d["id"]].get(k, v) for k, v in d.items()})
                item["enabled"] = bool(existing[d["id"]].get("enabled", d["enabled"]))
                merged.append(item)
            else:
                merged.append(d)
        # keep unknown custom plugins
        default_ids = {d["id"] for d in default_plugins()}
        for p in data:
            if isinstance(p, dict) and p.get("id") and str(p.get("id")) not in default_ids:
                merged.append(p)
        return merged
    plugins = default_plugins()
    _safe_write_json(get_plugins_path(), plugins)
    return plugins


def save_plugins(plugins: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    _safe_write_json(get_plugins_path(), plugins)
    return plugins


@dataclass
class Session:
    token: str
    created_at: float
    expires_at: float


class SessionStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sessions: Dict[str, Session] = {}

    def create(self) -> Session:
        now = time.time()
        sess = Session(token=secrets.token_urlsafe(32), created_at=now, expires_at=now + SESSION_TTL_SECONDS)
        with self._lock:
            self._cleanup_locked(now)
            self._sessions[sess.token] = sess
        return sess

    def get(self, token: str) -> Optional[Session]:
        now = time.time()
        with self._lock:
            self._cleanup_locked(now)
            sess = self._sessions.get(token)
            if not sess:
                return None
            if sess.expires_at <= now:
                self._sessions.pop(token, None)
                return None
            return sess

    def delete(self, token: str) -> None:
        with self._lock:
            self._sessions.pop(token, None)

    def _cleanup_locked(self, now: float) -> None:
        expired = [k for k, v in self._sessions.items() if v.expires_at <= now]
        for k in expired:
            self._sessions.pop(k, None)


SESSIONS = SessionStore()
SERVER_START_TIME = time.time()


def _read_cpu_usage_percent(sample_interval: float = 0.1) -> Optional[float]:
    try:
        def read_stat() -> Tuple[int, int]:
            with open("/proc/stat", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("cpu "):
                        parts = [int(x) for x in line.split()[1:]]
                        idle = parts[3] + (parts[4] if len(parts) > 4 else 0)
                        total = sum(parts)
                        return idle, total
            return 0, 0
        idle1, total1 = read_stat()
        time.sleep(sample_interval)
        idle2, total2 = read_stat()
        totald = total2 - total1
        idled = idle2 - idle1
        if totald <= 0:
            return None
        usage = (1.0 - (idled / totald)) * 100.0
        return max(0.0, min(100.0, usage))
    except Exception:
        return None


def _read_mem_info() -> Dict[str, Any]:
    info: Dict[str, Any] = {"total_bytes": None, "available_bytes": None, "used_bytes": None, "percent": None}
    try:
        mem = {}
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    mem[k.strip()] = v.strip()
        def kb(key: str) -> Optional[int]:
            raw = mem.get(key)
            if not raw:
                return None
            parts = raw.split()
            if not parts:
                return None
            try:
                return int(parts[0]) * 1024
            except Exception:
                return None
        total = kb("MemTotal")
        avail = kb("MemAvailable") or kb("MemFree")
        if total is not None and avail is not None:
            used = max(0, total - avail)
            info.update({
                "total_bytes": total,
                "available_bytes": avail,
                "used_bytes": used,
                "percent": round((used / total) * 100.0, 2) if total else None,
            })
    except Exception:
        pass
    return info


def _read_storage_info(path: Path) -> Dict[str, Any]:
    try:
        usage = shutil.disk_usage(str(path))
        used = usage.used
        total = usage.total
        return {
            "path": str(path),
            "total_bytes": total,
            "used_bytes": used,
            "free_bytes": usage.free,
            "percent": round((used / total) * 100.0, 2) if total else None,
        }
    except Exception:
        return {"path": str(path), "total_bytes": None, "used_bytes": None, "free_bytes": None, "percent": None}


def _read_network_info() -> Dict[str, Any]:
    data: Dict[str, Any] = {"interfaces": [], "hostname": socket.gethostname()}
    try:
        with open("/proc/net/dev", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        for line in lines[2:]:
            if ":" not in line:
                continue
            iface, rest = line.split(":", 1)
            cols = rest.split()
            if len(cols) < 16:
                continue
            data["interfaces"].append({
                "name": iface.strip(),
                "rx_bytes": int(cols[0]),
                "rx_packets": int(cols[1]),
                "tx_bytes": int(cols[8]),
                "tx_packets": int(cols[9]),
            })
    except Exception:
        pass
    return data


def _process_info() -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "executable": sys.executable,
    }
    try:
        load1, load5, load15 = os.getloadavg()
        info["loadavg"] = {"1m": load1, "5m": load5, "15m": load15}
    except Exception:
        info["loadavg"] = None
    try:
        info["cwd"] = os.getcwd()
    except Exception:
        info["cwd"] = None
    return info


def _check_port(host: str, port: int) -> Dict[str, Any]:
    result = {"host": host, "port": port, "open": False, "error": None}
    try:
        with socket.create_connection((host, port), timeout=0.5):
            result["open"] = True
    except Exception as e:
        result["error"] = str(e)
    return result


def _run_safe_command(cmd: List[str], timeout: float = 2.0) -> Dict[str, Any]:
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": cp.returncode == 0, "returncode": cp.returncode, "stdout": cp.stdout[-4000:], "stderr": cp.stderr[-2000:]}
    except Exception as e:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(e)}


def get_status_payload(include_cpu_sample: bool = True) -> Dict[str, Any]:
    cfg = load_config()
    repo = get_repo_root()
    cpu = _read_cpu_usage_percent() if include_cpu_sample else None
    mem = _read_mem_info()
    disk = _read_storage_info(repo)
    net = _read_network_info()
    proc = _process_info()
    uptime = max(0, int(time.time() - SERVER_START_TIME))
    payload = {
        "app": APP_NAME,
        "status": "running",
        "local_url": f"http://{cfg.get('host', DEFAULT_HOST)}:{int(cfg.get('port', DEFAULT_PORT))}",
        "bind_host": cfg.get("host", DEFAULT_HOST),
        "port": int(cfg.get("port", DEFAULT_PORT)),
        "uptime_seconds": uptime,
        "server_time": utc_now_iso(),
        "cpu_percent": cpu,
        "memory": mem,
        "storage": disk,
        "network": net,
        "process": proc,
        "paths": {
            "repo_root": str(repo),
            "config": str(get_config_path()),
            "admin_config": str(get_admin_path()),
            "log": str(get_log_path()),
            "pid": str(get_pid_path()),
            "backup_dir": str(get_backup_dir()),
            "plugins": str(get_plugins_path()),
            "state_dir": str(get_state_dir()),
            "local_config_dir": str(get_local_dir()),
        },
        "health": {
            "config_readable": get_config_path().exists(),
            "admin_configured": get_admin_path().exists(),
            "log_writable_parent": get_log_path().parent.exists(),
        },
        "admin": {
            "password_required": admin_password_required(),
        },
    }
    return payload


def _runtime_report() -> Dict[str, Any]:
    cfg = load_config()
    return {
        "ok": True,
        "python": {
            "version": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
        },
        "paths": {
            "repo_root": str(get_repo_root()),
            "config": str(get_config_path()),
            "admin": str(get_admin_path()),
            "plugins": str(get_plugins_path()),
            "log": str(get_log_path()),
            "pid": str(get_pid_path()),
            "state_dir": str(get_state_dir()),
            "local_dir": str(get_local_dir()),
            "backup_dir": str(get_backup_dir()),
        },
        "config_summary": {
            "host": cfg.get("host"),
            "port": cfg.get("port"),
            "theme": cfg.get("theme"),
            "log_level": cfg.get("log_level"),
            "auto_start": cfg.get("auto_start"),
        },
        "time": utc_now_iso(),
    }


def _sessions_info() -> Dict[str, Any]:
    now = time.time()
    with SESSIONS._lock:
        active = [s for s in SESSIONS._sessions.values() if s.expires_at > now]
        expires = [int(s.expires_at - now) for s in active]
    return {
        "ok": True,
        "active_sessions": len(active),
        "soonest_expiry_seconds": min(expires) if expires else None,
        "latest_expiry_seconds": max(expires) if expires else None,
        "session_ttl_seconds": SESSION_TTL_SECONDS,
        "time": utc_now_iso(),
    }


def _endpoint_inventory() -> Dict[str, Any]:
    return {
        "ok": True,
        "public": ["/", "/admin", "/api/public/info", "/api/auth/session", "/api/auth/login", "/api/auth/logout"],
        "protected_get": ["/api/status", "/api/config", "/api/logs", "/api/plugins", "/api/backup/list", "/api/files", "/api/health"],
        "protected_post": [
            "/api/config", "/api/admin/password", "/api/action", "/api/plugins", "/api/backup/create", "/api/backup/restore",
            "/api/tools/dependency_check", "/api/tools/permission_check", "/api/tools/port_check", "/api/tools/network_status",
            "/api/tools/process_info", "/api/tools/config_validate", "/api/tools/integrity_check", "/api/tools/log_analyze",
            "/api/tools/runtime_report", "/api/tools/sessions_info", "/api/tools/endpoint_inventory", "/api/tools/readiness_check",
            "/api/tools/git_status", "/api/tools/path_report", "/api/tools/auth_log_summary", "/api/tools/config_snapshot",
            "/api/tools/diagnostics_bundle", "/api/tools/log_rotate", "/api/tools/self_test",
        ],
        "localhost_only": True,
    }


def _readiness_check() -> Dict[str, Any]:
    cfg = load_config()
    checks = {
        "service_script_exists": (get_repo_root() / "pages" / "notinwebsite" / "local.py").exists(),
        "termux_launcher_exists": (get_repo_root() / "termux.py").exists(),
        "config_readable": isinstance(cfg, dict),
        "admin_config_exists": get_admin_path().exists(),
        "log_parent_exists": get_log_path().parent.exists(),
        "backup_dir_exists": get_backup_dir().exists(),
        "localhost_bind": (cfg.get("host") == DEFAULT_HOST),
        "valid_port": isinstance(cfg.get("port"), int) and 1 <= int(cfg.get("port", 0)) <= 65535,
    }
    return {"ok": all(checks.values()), "checks": checks, "local_url": f"http://{DEFAULT_HOST}:{int(cfg.get('port', DEFAULT_PORT))}", "time": utc_now_iso()}


def _git_status_summary() -> Dict[str, Any]:
    repo = get_repo_root()
    if not (repo / ".git").exists():
        return {"ok": False, "error": "Not a git repository"}
    branch = _run_safe_command(["git", "-C", str(repo), "--no-pager", "rev-parse", "--abbrev-ref", "HEAD"], timeout=2.0)
    head = _run_safe_command(["git", "-C", str(repo), "--no-pager", "log", "-1", "--oneline"], timeout=2.0)
    status = _run_safe_command(["git", "-C", str(repo), "--no-pager", "status", "--short"], timeout=3.0)
    lines = [ln for ln in (status.get("stdout") or "").splitlines() if ln.strip()]
    return {
        "ok": bool(branch.get("ok") or head.get("ok")),
        "branch": (branch.get("stdout") or "").strip() or None,
        "head": (head.get("stdout") or "").strip() or None,
        "changed_entries": len(lines),
        "changes_preview": lines[:40],
        "read_only": True,
    }


def _path_report() -> Dict[str, Any]:
    targets = [
        ("repo_root", get_repo_root()),
        ("local_dir", get_local_dir()),
        ("state_dir", get_state_dir()),
        ("backup_dir", get_backup_dir()),
    ]
    rows = []
    for label, p in targets:
        info = {"label": label, "path": str(p), "exists": p.exists()}
        try:
            if p.exists():
                info["is_dir"] = p.is_dir()
                info["is_file"] = p.is_file()
                info["writable"] = os.access(p, os.W_OK)
                if p.is_dir():
                    # Shallow size/count for safety/performance.
                    total = 0
                    count = 0
                    for child in p.rglob("*"):
                        if child.is_file():
                            count += 1
                            try:
                                total += child.stat().st_size
                            except Exception:
                                pass
                            if count >= 2000:
                                break
                    info["approx_file_count"] = count
                    info["approx_size_bytes"] = total
        except Exception as e:
            info["error"] = str(e)
        rows.append(info)
    return {"ok": True, "paths": rows, "time": utc_now_iso()}


def _auth_log_summary() -> Dict[str, Any]:
    lines = read_log_lines(500)
    events = {"login_success": 0, "login_failed": 0, "logout": 0, "unauthorized": 0}
    recent = []
    for line in lines:
        low = line.lower()
        matched = None
        if "admin login successful" in low:
            events["login_success"] += 1; matched = "login_success"
        elif "admin login failed" in low:
            events["login_failed"] += 1; matched = "login_failed"
        elif "admin logout" in low:
            events["logout"] += 1; matched = "logout"
        elif "unauthorized" in low:
            events["unauthorized"] += 1; matched = "unauthorized"
        if matched:
            recent.append(line)
    return {"ok": True, "events": events, "recent": recent[-20:], "time": utc_now_iso()}


def _config_snapshot() -> Dict[str, Any]:
    cfg = load_config()
    plugins = load_plugins()
    raw = json.dumps({"config": cfg, "plugins": plugins}, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return {
        "ok": True,
        "config": cfg,
        "plugins_count": len(plugins),
        "enabled_plugins": [p.get("id") for p in plugins if isinstance(p, dict) and p.get("enabled")],
        "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
        "admin_password_required": admin_password_required(),
        "time": utc_now_iso(),
    }


def _diagnostics_bundle() -> Dict[str, Any]:
    return {
        "ok": True,
        "time": utc_now_iso(),
        "status": get_status_payload(include_cpu_sample=False),
        "health": _health_check(),
        "config_validation": _config_validation(),
        "dependency_check": _dependency_check(),
        "permission_check": _permission_check(),
        "runtime_report": _runtime_report(),
        "sessions_info": _sessions_info(),
        "readiness_check": _readiness_check(),
        "log_analysis": _analyze_logs(),
        "auth_log_summary": _auth_log_summary(),
        "path_report": _path_report(),
        "git_status": _git_status_summary(),
    }


def _rotate_log() -> Dict[str, Any]:
    log_path = get_log_path()
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        rotated = None
        if log_path.exists() and log_path.stat().st_size > 0:
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            rotated = log_path.with_name(f"local.log.{ts}")
            shutil.copy2(log_path, rotated)
            log_path.write_text("", encoding="utf-8")
            append_log("info", f"Rotated local log to {rotated.name}")
        else:
            log_path.write_text("", encoding="utf-8")
        return {"ok": True, "rotated_to": str(rotated) if rotated else None, "active_log": str(log_path)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _self_test() -> Dict[str, Any]:
    tests = {}
    tests["runtime_report"] = bool(_runtime_report().get("ok"))
    tests["sessions_info"] = bool(_sessions_info().get("ok"))
    tests["readiness_check"] = bool(_readiness_check().get("checks"))
    tests["config_validation"] = "ok" in _config_validation()
    tests["dependency_check"] = "ok" in _dependency_check()
    tests["permission_check"] = "ok" in _permission_check()
    tests["log_analysis"] = "ok" in _analyze_logs()
    tests["path_report"] = bool(_path_report().get("ok"))
    tests["endpoint_inventory"] = bool(_endpoint_inventory().get("ok"))
    tests["health_check"] = "ok" in _health_check()
    return {"ok": all(tests.values()), "tests": tests, "passed": sum(1 for v in tests.values() if v), "total": len(tests), "time": utc_now_iso()}


def _json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _read_request_json(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0") or "0")
    except Exception:
        length = 0
    raw = handler.rfile.read(max(0, length)) if length > 0 else b""
    if not raw:
        return {}
    try:
        data = json.loads(raw.decode("utf-8", errors="replace"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _parse_cookie_token(handler: BaseHTTPRequestHandler) -> Optional[str]:
    raw = handler.headers.get("Cookie")
    if not raw:
        return None
    try:
        c = SimpleCookie()
        c.load(raw)
        morsel = c.get(SESSION_COOKIE)
        if not morsel:
            return None
        token = morsel.value.strip()
        return token or None
    except Exception:
        return None


def _get_session(handler: BaseHTTPRequestHandler) -> Optional[Session]:
    token = _parse_cookie_token(handler)
    if not token:
        return None
    return SESSIONS.get(token)


def _require_admin(handler: BaseHTTPRequestHandler) -> Optional[Session]:
    return _get_session(handler)


def _safe_repo_path(rel: str) -> Optional[Path]:
    rel = (rel or "").strip().lstrip("/")
    root = get_repo_root().resolve()
    target = (root / rel).resolve() if rel else root
    try:
        target.relative_to(root)
    except Exception:
        return None
    return target


def _list_directory(rel: str = "") -> Dict[str, Any]:
    target = _safe_repo_path(rel)
    root = get_repo_root().resolve()
    if target is None:
        return {"ok": False, "error": "Invalid path"}
    if not target.exists():
        return {"ok": False, "error": "Path not found"}
    if not target.is_dir():
        return {"ok": False, "error": "Path is not a directory"}
    entries = []
    try:
        for child in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))[:300]:
            try:
                stat = child.stat()
                entries.append({
                    "name": child.name,
                    "path": str(child.relative_to(root)),
                    "type": "dir" if child.is_dir() else "file",
                    "size": stat.st_size if child.is_file() else None,
                    "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
                })
            except Exception:
                entries.append({"name": child.name, "path": str(child.relative_to(root)), "type": "dir" if child.is_dir() else "file"})
    except Exception as e:
        return {"ok": False, "error": str(e)}
    rel_path = str(target.relative_to(root)) if target != root else ""
    parent = str(target.parent.relative_to(root)) if target != root else None
    return {"ok": True, "path": rel_path, "parent": parent, "entries": entries}


def _hash_file(rel: str) -> Dict[str, Any]:
    target = _safe_repo_path(rel)
    if target is None or not target.exists() or not target.is_file():
        return {"ok": False, "error": "File not found"}
    try:
        h = hashlib.sha256()
        with target.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return {"ok": True, "path": rel, "sha256": h.hexdigest(), "size": target.stat().st_size}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _backup_state() -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = get_backup_dir() / ts
    backup_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for p in [get_config_path(), get_admin_path(), get_plugins_path()]:
        if p.exists():
            dest = backup_dir / p.name
            shutil.copy2(p, dest)
            copied.append(dest.name)
    manifest = {"created_at": utc_now_iso(), "files": copied}
    _safe_write_json(backup_dir / "manifest.json", manifest)
    append_log("info", f"Created backup {backup_dir.name} ({len(copied)} files)")
    return {"ok": True, "backup_id": backup_dir.name, "files": copied}


def _list_backups() -> List[Dict[str, Any]]:
    items = []
    base = get_backup_dir()
    if not base.exists():
        return items
    for child in sorted(base.iterdir(), reverse=True):
        if not child.is_dir():
            continue
        manifest = _load_json(child / "manifest.json", {})
        files = manifest.get("files") if isinstance(manifest, dict) else []
        items.append({
            "id": child.name,
            "created_at": manifest.get("created_at") if isinstance(manifest, dict) else None,
            "files": files if isinstance(files, list) else [],
        })
    return items[:50]


def _restore_backup(backup_id: str) -> Dict[str, Any]:
    safe_id = "".join(ch for ch in (backup_id or "") if ch.isalnum() or ch in ("T", "Z", "-", "_"))
    if not safe_id:
        return {"ok": False, "error": "Invalid backup id"}
    src = get_backup_dir() / safe_id
    if not src.exists() or not src.is_dir():
        return {"ok": False, "error": "Backup not found"}
    restored = []
    mapping = {
        "config.json": get_config_path(),
        "admin.json": get_admin_path(),
        "plugins.json": get_plugins_path(),
    }
    for name, dest in mapping.items():
        s = src / name
        if s.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, dest)
            restored.append(name)
    append_log("info", f"Restored backup {safe_id} ({len(restored)} files)")
    return {"ok": True, "backup_id": safe_id, "restored": restored}


def _analyze_logs() -> Dict[str, Any]:
    lines = read_log_lines(300)
    levels = {"INFO": 0, "WARN": 0, "WARNING": 0, "ERROR": 0}
    keywords = {"error": 0, "warn": 0, "fail": 0, "unauthorized": 0}
    for line in lines:
        upper = line.upper()
        for lvl in levels:
            if f"[{lvl}]" in upper:
                levels[lvl] += 1
        low = line.lower()
        for k in keywords:
            if k in low:
                keywords[k] += 1
    return {"ok": True, "total_lines": len(lines), "levels": levels, "keywords": keywords, "recent": lines[-20:]}


def _dependency_check() -> Dict[str, Any]:
    checks = {}
    for name in ["python3", "git", "curl", "bash"]:
        checks[name] = {"available": shutil.which(name) is not None, "path": shutil.which(name)}
    checks["python_version"] = {"available": True, "value": sys.version.split()[0]}
    checks["repo_service_script"] = {
        "available": (get_repo_root() / "pages" / "notinwebsite" / "local.py").exists(),
        "path": str(get_repo_root() / "pages" / "notinwebsite" / "local.py"),
    }
    return {"ok": True, "checks": checks}


def _permission_check() -> Dict[str, Any]:
    paths = [get_local_dir(), get_state_dir(), get_config_path(), get_admin_path(), get_plugins_path(), get_log_path(), get_pid_path(), get_backup_dir()]
    results = []
    for p in paths:
        exists = p.exists()
        mode = None
        if exists:
            try:
                mode = oct(p.stat().st_mode & 0o777)
            except Exception:
                mode = None
        results.append({
            "path": str(p),
            "exists": exists,
            "readable": os.access(p, os.R_OK) if exists else os.access(p.parent, os.R_OK),
            "writable": os.access(p, os.W_OK) if exists else os.access(p.parent, os.W_OK),
            "mode": mode,
        })
    return {"ok": True, "results": results}


def _config_validation() -> Dict[str, Any]:
    cfg = load_config()
    issues = []
    warnings = []
    host = str(cfg.get("host", DEFAULT_HOST))
    port = cfg.get("port", DEFAULT_PORT)
    if host not in ("127.0.0.1", "localhost", "::1"):
        issues.append("Host should be localhost-only (127.0.0.1) for admin safety.")
    try:
        port_i = int(port)
        if port_i < 1 or port_i > 65535:
            issues.append("Port must be between 1 and 65535.")
    except Exception:
        issues.append("Port must be an integer.")
    if str(cfg.get("theme", "dark")) not in ("dark", "light", "system"):
        warnings.append("Unknown theme value; dashboard will fallback to default styling.")
    if not get_admin_path().exists():
        warnings.append("Admin config not initialized yet.")
    return {"ok": len(issues) == 0, "issues": issues, "warnings": warnings, "config": cfg}


def _health_check() -> Dict[str, Any]:
    cfg = load_config()
    port = int(cfg.get("port", DEFAULT_PORT))
    port_check = _check_port("127.0.0.1", port)
    disk = _read_storage_info(get_repo_root())
    mem = _read_mem_info()
    checks = {
        "server_running": True,
        "localhost_port_probe": port_check,
        "config_valid": _config_validation(),
        "dependencies": _dependency_check(),
        "disk_ok": (disk.get("percent") is None or float(disk.get("percent")) < 95.0),
        "memory_ok": (mem.get("percent") is None or float(mem.get("percent")) < 98.0),
        "admin_configured": get_admin_path().exists(),
        "password_configurable": True,
    }
    ok = all([
        checks["server_running"],
        checks["config_valid"]["ok"],
        checks["disk_ok"],
        checks["memory_ok"],
    ])
    return {"ok": ok, "checks": checks, "time": utc_now_iso()}


def _dashboard_html() -> str:
    # Single-file localhost dashboard UI (served by local.py only).
    return r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DeveloperHCR Local Setup Dashboard</title>
<style>
:root{--bg:#07131f;--panel:#0f2233;--card:#12283b;--text:#eaf6ff;--muted:#9fb7c8;--primary:#67e8f9;--accent:#8b5cf6;--ok:#34d399;--warn:#f59e0b;--bad:#fb7185;--border:rgba(148,163,184,.22)}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(180deg,#07131f,#020b12);color:var(--text)}
.wrap{max-width:1200px;margin:0 auto;padding:20px}.hero{background:linear-gradient(135deg,rgba(103,232,249,.12),rgba(139,92,246,.12));border:1px solid var(--border);border-radius:18px;padding:18px 20px;margin-bottom:16px}
.hero h1{margin:0 0 6px;font-size:1.5rem}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px}.card h3{margin:0 0 8px;font-size:1rem}
.kv{font-size:.95rem;line-height:1.45}.k{color:var(--muted)}.row{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
button,.btn{appearance:none;border:1px solid var(--border);background:#173247;color:var(--text);padding:8px 12px;border-radius:10px;cursor:pointer;font-weight:600}
button:hover{border-color:var(--primary)}.primary{background:#0b6f86;border-color:#0b6f86}.danger{background:#7f1d1d;border-color:#7f1d1d}
input,select,textarea{width:100%;padding:8px 10px;border-radius:10px;border:1px solid var(--border);background:#0c1b29;color:var(--text)}
textarea{min-height:120px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}pre{white-space:pre-wrap;word-break:break-word;background:#081522;border:1px solid var(--border);border-radius:10px;padding:10px;max-height:260px;overflow:auto}
.section{margin-top:16px}.two{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media (max-width:900px){.two{grid-template-columns:1fr}}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.8rem;border:1px solid var(--border)}.ok{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}
table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid var(--border);text-align:left;font-size:.92rem;vertical-align:top}
.small{font-size:.85rem}.login{max-width:420px;margin:40px auto;background:var(--panel);border:1px solid var(--border);border-radius:16px;padding:18px}
hr{border:0;border-top:1px solid var(--border);margin:14px 0}
a{color:var(--primary)}
</style>
</head>
<body>
<div class="wrap" id="app">
  <div class="hero">
    <h1>DeveloperHCR™ Local Setup Dashboard</h1>
    <div class="muted">Localhost-only admin control panel for HCRAPP Termux/local service.</div>
    <div class="small muted" id="auth-state">Checking authentication...</div>
  </div>

  <div id="login-panel" class="login" style="display:none">
    <h2 style="margin-top:0">Admin Login</h2>
    <p class="muted">Enter the local admin password to open Local Setup. <span id="pw-hint"></span></p>
    <label for="pw">Password</label>
    <input id="pw" type="password" autocomplete="current-password" placeholder="Password (if configured)">
    <div class="row"><button class="primary" id="login-btn">Open Local Setup</button></div>
    <div id="login-msg" class="small muted"></div>
  </div>

  <div id="dash" style="display:none">
    <div class="row">
      <button class="primary" onclick="refreshAll()">Refresh</button>
      <button onclick="doAction('restart')">Restart</button>
      <button class="danger" onclick="doAction('stop')">Stop Server</button>
      <button onclick="logout()">Logout</button>
      <a class="btn" href="/" target="_self">Dashboard Home</a>
    </div>

    <div class="grid section" id="status-cards"></div>

    <div class="two section">
      <div class="card">
        <h3>Controls</h3>
        <div class="row">
          <button onclick="doAction('start')">Start</button>
          <button onclick="doAction('stop')" class="danger">Stop</button>
          <button onclick="doAction('restart')">Restart</button>
          <button onclick="runHealth()">Health Check</button>
          <button onclick="loadLogs()">Refresh Logs</button>
        </div>
        <div class="small muted">Start/Stop/Restart control the local service process (restart may require launcher/Termux to respawn depending on environment).</div>
        <pre id="action-out">No actions yet.</pre>
      </div>
      <div class="card">
        <h3>Configuration</h3>
        <label>Theme</label>
        <select id="cfg-theme"><option value="dark">dark</option><option value="light">light</option><option value="system">system</option></select>
        <label style="margin-top:8px;display:block">Log level</label>
        <select id="cfg-log"><option>info</option><option>debug</option><option>warn</option><option>error</option></select>
        <label style="margin-top:8px;display:block">Auto start (launcher hint)</label>
        <select id="cfg-autostart"><option value="false">false</option><option value="true">true</option></select>
        <div class="row"><button onclick="saveConfig()">Save Configuration</button><button onclick="validateConfig()">Validate</button></div>
        <pre id="cfg-out"></pre>
      </div>
    </div>

    <div class="two section">
      <div class="card">
        <h3>Logs</h3>
        <div class="row"><button onclick="loadLogs()">Refresh Logs</button><button onclick="analyzeLogs()">Analyze Logs</button></div>
        <pre id="logs">(loading)</pre>
      </div>
      <div class="card">
        <h3>Log Analyzer / Insights</h3>
        <pre id="logs-analysis"></pre>
      </div>
    </div>

    <div class="two section">
      <div class="card"><h3>Backup / Restore</h3><div class="row"><button onclick="createBackup()">Create Backup</button><button onclick="loadBackups()">Refresh Backups</button></div><pre id="backup-out"></pre></div>
      <div class="card"><h3>Plugin Manager</h3><div class="row"><button onclick="loadPlugins()">Refresh Plugins</button><button onclick="savePlugins()">Save Plugin States</button></div><div id="plugins"></div></div>
    </div>

    <div class="two section">
      <div class="card"><h3>Local File Browser</h3><div class="row"><button onclick="browse('')">Repo Root</button><button onclick="browse(currentPath)">Refresh</button></div><div class="small muted">Current: <span id="fb-path">(root)</span></div><pre id="fb-out"></pre></div>
      <div class="card"><h3>Developer / Security Tools</h3>
        <div class="row">
          <button onclick="tool('dependency_check')">Dependency Checker</button>
          <button onclick="tool('permission_check')">Permission Checker</button>
          <button onclick="tool('port_check')">Port/Status Checker</button>
          <button onclick="tool('network_status')">Network Status</button>
          <button onclick="tool('process_info')">Process Viewer</button>
          <button onclick="tool('health_check')">Service Health</button>
          <button onclick="tool('config_validate')">Config Validator</button>
        </div>
        <label class="small">File integrity (repo-relative path)</label>
        <input id="integrity-path" placeholder="e.g. termux.py">
        <div class="row"><button onclick="tool('integrity_check')">File Integrity Hash</button></div>
        <pre id="tool-out"></pre>
      </div>
    </div>

    <div class="two section">
      <div class="card"><h3>More Safe Utilities (Local-only)</h3>
        <div class="row">
          <button onclick="tool('runtime_report')">Runtime Report</button>
          <button onclick="tool('sessions_info')">Sessions Info</button>
          <button onclick="tool('endpoint_inventory')">Endpoint Inventory</button>
          <button onclick="tool('readiness_check')">Readiness Check</button>
          <button onclick="tool('git_status')">Git Status (Read-only)</button>
          <button onclick="tool('path_report')">Path/Storage Report</button>
          <button onclick="tool('auth_log_summary')">Auth/Log Summary</button>
          <button onclick="tool('config_snapshot')">Config Snapshot</button>
          <button onclick="tool('diagnostics_bundle')">Diagnostics Bundle</button>
          <button onclick="tool('log_rotate')">Rotate/Trim Logs</button>
          <button onclick="tool('self_test')">Safe Self-Test</button>
        </div>
        <div class="small muted">Defensive local diagnostics and maintenance tools only. No hacking, bombing, or unauthorized-access tools.</div>
        <pre id="extra-tool-out"></pre>
      </div>
      <div class="card">
        <h3>Admin Security Settings</h3>
        <p class="small muted">Password is configurable and stored locally (hashed) by the localhost service. Leave new password empty to disable password requirement.</p>
        <div id="admin-pw-state" class="small muted"></div>
        <label style="margin-top:8px;display:block">Current password (if required)</label>
        <input id="admin-current-pw" type="password" autocomplete="current-password" placeholder="Current password">
        <label style="margin-top:8px;display:block">New password (empty to disable)</label>
        <input id="admin-new-pw" type="password" autocomplete="new-password" placeholder="New password">
        <div class="row"><button onclick="updateAdminPassword()">Save Admin Password Setting</button></div>
        <pre id="admin-pw-out"></pre>
      </div>
      <div class="card">
        <h3>Environment / Paths</h3>
        <div class="row"><button onclick="refreshStatus()">Refresh Status</button><button onclick="copyLocalUrl()">Copy Local URL</button></div>
        <pre id="env-out"></pre>
      </div>
    </div>

    <div class="section card">
      <h3>Additional Features</h3>
      <ul class="small muted">
        <li>Session timeout indicator and secure localhost-only auth cookie</li>
        <li>Configurable admin password (server-side, local hash storage)</li>
        <li>Live uptime and runtime environment details</li>
        <li>Configuration validation warnings/issues</li>
        <li>Log keyword summary and recent log tail</li>
        <li>Backup history listing and one-click restore</li>
        <li>Plugin enable/disable state persistence</li>
        <li>Repository file browser with metadata</li>
        <li>SHA-256 file integrity hashing for local files</li>
        <li>Port probe and localhost service checks</li>
        <li>Dependency, permission, network, and process diagnostics</li>
        <li>Theme preference saved in local configuration</li>
        <li>Quick local URL copy and environment path summary</li>
        <li>Health-check aggregation for service/readiness</li>
        <li>Runtime environment report (Python, platform, paths)</li>
        <li>Active admin session diagnostics and expiry info</li>
        <li>Local API endpoint inventory (read-only reference)</li>
        <li>Readiness checklist for launcher, config, and paths</li>
        <li>Read-only repository git status summary</li>
        <li>Key path/storage usage report for local directories</li>
        <li>Auth/log event summary (success/fail/logout/unauthorized)</li>
        <li>Configuration snapshot hash and plugin summary</li>
        <li>Exportable diagnostics bundle for local troubleshooting</li>
        <li>Safe log rotation/trim utility for local maintenance</li>
        <li>Local self-test of safe diagnostic checks</li>
      </ul>
    </div>
  </div>
</div>
<script>
let authed=false, currentPath='', pluginsCache=[], lastStatus=null;
async function api(path, opts={}){
  const res = await fetch(path, Object.assign({credentials:'same-origin', headers:{'Content-Type':'application/json'}}, opts));
  const ct = res.headers.get('content-type')||'';
  let data = null;
  if(ct.includes('application/json')) data = await res.json(); else data = await res.text();
  return {ok: res.ok, status: res.status, data};
}
function fmtBytes(n){ if(n==null||isNaN(n)) return 'n/a'; const u=['B','KB','MB','GB','TB']; let i=0,x=Number(n); while(x>=1024&&i<u.length-1){x/=1024;i++;} return x.toFixed(i?2:0)+' '+u[i]; }
function esc(s){ return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
async function checkAuth(){
  const r = await api('/api/auth/session');
  authed = !!(r.ok && r.data && r.data.authenticated);
  const req = (r.ok && r.data) ? r.data.password_required : null;
  const hint = document.getElementById('pw-hint');
  if(hint){ hint.textContent = (req === false) ? '(Password not required by default; configurable.)' : ''; }
  document.getElementById('login-panel').style.display = authed ? 'none':'block';
  document.getElementById('dash').style.display = authed ? 'block':'none';
  document.getElementById('auth-state').textContent = authed ? 'Authenticated (localhost admin session active)' : 'Not authenticated';
  const pwInput = document.getElementById('pw');
  if(pwInput){ pwInput.required = (req === true); }
  if(authed){ await refreshAll(); }
}
async function login(){
  const pw = document.getElementById('pw').value || '';
  const msg = document.getElementById('login-msg');
  msg.textContent = 'Authenticating...';
  const r = await api('/api/auth/login', {method:'POST', body: JSON.stringify({password: pw})});
  if(r.ok && r.data && r.data.ok){ msg.textContent='Authenticated.'; document.getElementById('pw').value=''; await checkAuth(); }
  else { msg.textContent = (r.data && r.data.error) ? r.data.error : 'Authentication failed.'; }
}
async function logout(){ await api('/api/auth/logout', {method:'POST', body:'{}'}); await checkAuth(); }
function card(title, body){ return `<div class="card"><h3>${esc(title)}</h3><div class="kv">${body}</div></div>`; }
async function refreshStatus(){
  const r = await api('/api/status');
  if(!r.ok){ document.getElementById('status-cards').innerHTML = card('Status','Failed to load status'); return; }
  const s = r.data; lastStatus = s;
  const cards = [];
  cards.push(card('Server Status', `<div><span class="k">Status:</span> <span class="ok">${esc(s.status||'unknown')}</span></div><div><span class="k">Local URL:</span> ${esc(s.local_url||'')}</div><div><span class="k">Host/Port:</span> ${esc(s.bind_host)}:${esc(s.port)}</div><div><span class="k">Uptime:</span> ${esc(s.uptime_seconds)}s</div>`));
  cards.push(card('CPU / RAM', `<div><span class="k">CPU:</span> ${s.cpu_percent==null?'n/a':esc(s.cpu_percent+'%')}</div><div><span class="k">RAM Used:</span> ${esc(fmtBytes(s.memory?.used_bytes))} / ${esc(fmtBytes(s.memory?.total_bytes))} (${s.memory?.percent==null?'n/a':esc(s.memory.percent+'%')})</div><div><span class="k">RAM Free:</span> ${esc(fmtBytes(s.memory?.available_bytes))}</div>`));
  cards.push(card('Storage', `<div><span class="k">Path:</span> ${esc(s.storage?.path||'')}</div><div><span class="k">Used:</span> ${esc(fmtBytes(s.storage?.used_bytes))} / ${esc(fmtBytes(s.storage?.total_bytes))} (${s.storage?.percent==null?'n/a':esc(s.storage.percent+'%')})</div><div><span class="k">Free:</span> ${esc(fmtBytes(s.storage?.free_bytes))}</div>`));
  cards.push(card('Network / Process', `<div><span class="k">Hostname:</span> ${esc(s.network?.hostname||'')}</div><div><span class="k">Interfaces:</span> ${esc((s.network?.interfaces||[]).length)}</div><div><span class="k">PID:</span> ${esc(s.process?.pid)}</div><div><span class="k">Python:</span> ${esc(s.process?.python||'')}</div><div><span class="k">Platform:</span> ${esc(s.process?.platform||'')}</div>`));
  document.getElementById('status-cards').innerHTML = cards.join('');
  document.getElementById('cfg-theme').value = (s.config_theme||'dark');
  document.getElementById('admin-pw-state').textContent = 'Password required: ' + String(!!(s.admin && s.admin.password_required));
  document.getElementById('env-out').textContent = JSON.stringify({paths: s.paths||{}, process: s.process||{}, local_url: s.local_url, server_time: s.server_time, uptime_seconds: s.uptime_seconds}, null, 2);
}
async function copyLocalUrl(){ try { const url = (lastStatus && lastStatus.local_url) || location.origin; await navigator.clipboard.writeText(url); document.getElementById('action-out').textContent = 'Copied Local URL: ' + url; } catch(e){ document.getElementById('action-out').textContent = 'Copy failed. Local URL: ' + ((lastStatus && lastStatus.local_url) || location.origin); } }
async function loadConfig(){
  const r = await api('/api/config');
  if(r.ok){ const c=r.data.config||{}; document.getElementById('cfg-theme').value=c.theme||'dark'; document.getElementById('cfg-log').value=c.log_level||'info'; document.getElementById('cfg-autostart').value=String(!!c.auto_start); document.getElementById('cfg-out').textContent=JSON.stringify(c,null,2); }
}
async function saveConfig(){
  const body = {theme: document.getElementById('cfg-theme').value, log_level: document.getElementById('cfg-log').value, auto_start: document.getElementById('cfg-autostart').value === 'true'};
  const r = await api('/api/config', {method:'POST', body: JSON.stringify(body)});
  document.getElementById('cfg-out').textContent = JSON.stringify(r.data,null,2);
}
async function validateConfig(){ const r = await api('/api/tools/config_validate', {method:'POST', body:'{}'}); document.getElementById('cfg-out').textContent = JSON.stringify(r.data,null,2); }
async function doAction(action){ const r = await api('/api/action', {method:'POST', body: JSON.stringify({action})}); document.getElementById('action-out').textContent = JSON.stringify(r.data,null,2); if(action!=='stop') setTimeout(refreshAll, 500); }
async function runHealth(){ const r = await api('/api/health'); document.getElementById('action-out').textContent = JSON.stringify(r.data,null,2); }
async function loadLogs(){ const r = await api('/api/logs?limit=200'); document.getElementById('logs').textContent = (r.ok && r.data && Array.isArray(r.data.lines)) ? r.data.lines.join('\n') : JSON.stringify(r.data,null,2); }
async function analyzeLogs(){ const r = await api('/api/tools/log_analyze', {method:'POST', body:'{}'}); document.getElementById('logs-analysis').textContent = JSON.stringify(r.data,null,2); }
async function createBackup(){ const r = await api('/api/backup/create', {method:'POST', body:'{}'}); document.getElementById('backup-out').textContent = JSON.stringify(r.data,null,2); await loadBackups(); }
async function loadBackups(){ const r = await api('/api/backup/list'); if(r.ok && r.data && Array.isArray(r.data.backups)){
  let html = '<table><tr><th>ID</th><th>Created</th><th>Files</th><th></th></tr>';
  for(const b of r.data.backups){ html += `<tr><td>${esc(b.id)}</td><td>${esc(b.created_at||'')}</td><td>${esc((b.files||[]).join(', '))}</td><td><button onclick="restoreBackup('${esc(b.id)}')">Restore</button></td></tr>`; }
  html += '</table>'; document.getElementById('backup-out').innerHTML = html;
 } else { document.getElementById('backup-out').textContent = JSON.stringify(r.data,null,2); }
}
async function restoreBackup(id){ const r = await api('/api/backup/restore', {method:'POST', body: JSON.stringify({id})}); document.getElementById('backup-out').textContent = JSON.stringify(r.data,null,2); await loadConfig(); await loadPlugins(); await refreshStatus(); }
async function loadPlugins(){ const r = await api('/api/plugins'); if(!(r.ok && r.data && Array.isArray(r.data.plugins))){ document.getElementById('plugins').textContent='Failed to load plugins'; return; } pluginsCache=r.data.plugins; renderPlugins(); }
function renderPlugins(){ const root=document.getElementById('plugins'); let html='<table><tr><th>Enabled</th><th>Plugin</th><th>Description</th></tr>'; for(const p of pluginsCache){ html+=`<tr><td><input type="checkbox" ${p.enabled?'checked':''} onchange="togglePlugin('${esc(p.id)}', this.checked)"></td><td>${esc(p.name||p.id)}</td><td class="small muted">${esc(p.description||'')}</td></tr>`; } html+='</table>'; root.innerHTML=html; }
function togglePlugin(id, enabled){ const p=pluginsCache.find(x=>x.id===id); if(p) p.enabled=enabled; }
async function savePlugins(){ const r = await api('/api/plugins', {method:'POST', body: JSON.stringify({plugins: pluginsCache})}); if(r.ok) pluginsCache=r.data.plugins||pluginsCache; document.getElementById('tool-out').textContent = JSON.stringify(r.data,null,2); }
async function browse(path){ currentPath=path||''; const r = await api('/api/files?path='+encodeURIComponent(currentPath)); document.getElementById('fb-path').textContent = currentPath || '(root)'; document.getElementById('fb-out').textContent = JSON.stringify(r.data,null,2); }
async function tool(name){ let body={}; if(name==='integrity_check'){ body.path=document.getElementById('integrity-path').value||''; }
  const map={
    dependency_check:'/api/tools/dependency_check',permission_check:'/api/tools/permission_check',port_check:'/api/tools/port_check',network_status:'/api/tools/network_status',process_info:'/api/tools/process_info',health_check:'/api/health',config_validate:'/api/tools/config_validate',integrity_check:'/api/tools/integrity_check',log_analyze:'/api/tools/log_analyze',
    runtime_report:'/api/tools/runtime_report',sessions_info:'/api/tools/sessions_info',endpoint_inventory:'/api/tools/endpoint_inventory',readiness_check:'/api/tools/readiness_check',git_status:'/api/tools/git_status',path_report:'/api/tools/path_report',auth_log_summary:'/api/tools/auth_log_summary',config_snapshot:'/api/tools/config_snapshot',diagnostics_bundle:'/api/tools/diagnostics_bundle',log_rotate:'/api/tools/log_rotate',self_test:'/api/tools/self_test'
  };
  const url = map[name]; if(!url) return;
  const method = (url==='/api/health') ? 'GET' : 'POST';
  const r = await api(url, {method, body: method==='GET'?undefined:JSON.stringify(body)});
  const outId = (name==='runtime_report'||name==='sessions_info'||name==='endpoint_inventory'||name==='readiness_check'||name==='git_status'||name==='path_report'||name==='auth_log_summary'||name==='config_snapshot'||name==='diagnostics_bundle'||name==='log_rotate'||name==='self_test') ? 'extra-tool-out' : 'tool-out';
  document.getElementById(outId).textContent = JSON.stringify(r.data,null,2);
  if(name==='log_rotate'){ await loadLogs(); await analyzeLogs(); }
}
async function updateAdminPassword(){
  const body = { current_password: document.getElementById('admin-current-pw').value || '', new_password: document.getElementById('admin-new-pw').value || '' };
  const r = await api('/api/admin/password', {method:'POST', body: JSON.stringify(body)});
  document.getElementById('admin-pw-out').textContent = JSON.stringify(r.data,null,2);
  document.getElementById('admin-current-pw').value='';
  document.getElementById('admin-new-pw').value='';
  await refreshStatus();
}
async function refreshAll(){ await Promise.all([refreshStatus(), loadConfig(), loadLogs(), loadBackups(), loadPlugins(), browse(currentPath), analyzeLogs()]); }
document.getElementById('login-btn').addEventListener('click', login);
document.getElementById('pw').addEventListener('keydown', (e)=>{ if(e.key==='Enter') login(); });
checkAuth();
</script>
</body>
</html>
'''


ONE_TIME_TOKENS: Dict[str, float] = {}
ONE_TIME_LOCK = threading.Lock()


def issue_one_time_token(ttl: int = 120) -> str:
    token = secrets.token_urlsafe(24)
    with ONE_TIME_LOCK:
        now = time.time()
        expired = [k for k, v in ONE_TIME_TOKENS.items() if v <= now]
        for k in expired:
            ONE_TIME_TOKENS.pop(k, None)
        ONE_TIME_TOKENS[token] = now + ttl
    return token


def consume_one_time_token(token: str) -> bool:
    if not token:
        return False
    with ONE_TIME_LOCK:
        now = time.time()
        exp = ONE_TIME_TOKENS.pop(token, None)
        return exp is not None and exp > now


class LocalHandler(BaseHTTPRequestHandler):
    server_version = "DeveloperHCRLocal/1.0"
    protocol_version = "HTTP/1.1"

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        try:
            u = urlparse(origin)
            host = (u.hostname or "").lower()
            scheme = (u.scheme or "").lower()
            if host in ("127.0.0.1", "localhost", "::1"):
                return True
            if host == "developerhcr.github.io" and scheme in ("https", "http"):
                return True
            if scheme == "file":
                return True
            return False
        except Exception:
            return False

    def _send_cors(self) -> None:
        origin = self.headers.get("Origin")
        if origin and self._origin_allowed():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")

    def _send(self, status: int, body: bytes, content_type: str = "text/plain; charset=utf-8", extra_headers: Optional[Dict[str, str]] = None) -> None:
        self.send_response(status)
        self._send_cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, status: int, payload: Any, extra_headers: Optional[Dict[str, str]] = None) -> None:
        self._send(status, _json_bytes(payload), "application/json; charset=utf-8", extra_headers=extra_headers)

    def _unauthorized(self, message: str = "Unauthorized") -> None:
        self._send_json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": message})

    def do_OPTIONS(self) -> None:  # noqa: N802
        if not self._origin_allowed():
            self._send(HTTPStatus.FORBIDDEN, b"forbidden")
            return
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/admin", "/setup", "/local-setup"):
            token = (qs.get("token") or [""])[0]
            if token and consume_one_time_token(token):
                sess = SESSIONS.create()
                append_log("info", "Admin session established via one-time token")
                cookie = f"{SESSION_COOKIE}={sess.token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={SESSION_TTL_SECONDS}"
                body = ("""<!doctype html><meta charset='utf-8'><title>Opening Local Setup...</title>
<script>location.replace('/admin');</script>""").encode('utf-8')
                return self._send(HTTPStatus.OK, body, "text/html; charset=utf-8", extra_headers={"Set-Cookie": cookie})
            return self._send(HTTPStatus.OK, _dashboard_html().encode("utf-8"), "text/html; charset=utf-8")

        if path == "/health":
            return self._send_json(HTTPStatus.OK, _health_check())

        if path == "/api/public/info":
            cfg = load_config()
            return self._send_json(HTTPStatus.OK, {
                "ok": True,
                "service": APP_NAME,
                "running": True,
                "localhost_only": True,
                "local_url": f"http://{cfg.get('host', DEFAULT_HOST)}:{int(cfg.get('port', DEFAULT_PORT))}",
                "admin_protected": True,
                "admin_password_required": admin_password_required(),
                "time": utc_now_iso(),
            })

        if path == "/api/auth/session":
            sess = _get_session(self)
            return self._send_json(HTTPStatus.OK, {
                "ok": True,
                "authenticated": bool(sess),
                "expires_at": int(sess.expires_at) if sess else None,
                "password_required": admin_password_required(),
            })

        # Auth-required APIs below
        if not _require_admin(self):
            return self._unauthorized()

        if path == "/api/status":
            cfg = load_config()
            payload = get_status_payload(include_cpu_sample=True)
            payload["config_theme"] = cfg.get("theme", "dark")
            return self._send_json(HTTPStatus.OK, payload)

        if path == "/api/config":
            return self._send_json(HTTPStatus.OK, {"ok": True, "config": load_config()})

        if path == "/api/logs":
            try:
                limit = int((qs.get("limit") or ["200"])[0])
            except Exception:
                limit = 200
            return self._send_json(HTTPStatus.OK, {"ok": True, "lines": read_log_lines(limit)})

        if path == "/api/plugins":
            return self._send_json(HTTPStatus.OK, {"ok": True, "plugins": load_plugins()})

        if path == "/api/backup/list":
            return self._send_json(HTTPStatus.OK, {"ok": True, "backups": _list_backups()})

        if path == "/api/files":
            rel = (qs.get("path") or [""])[0]
            return self._send_json(HTTPStatus.OK, _list_directory(rel))

        if path == "/api/health":
            return self._send_json(HTTPStatus.OK, _health_check())

        return self._send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        data = _read_request_json(self)

        if path == "/api/auth/login":
            password = str(data.get("password") or "")
            if not verify_admin_password(password):
                append_log("warn", "Admin login failed: invalid password")
                return self._send_json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "Incorrect password"})
            sess = SESSIONS.create()
            one_time = issue_one_time_token()
            append_log("info", "Admin login successful")
            cookie = (
                f"{SESSION_COOKIE}={sess.token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={SESSION_TTL_SECONDS}"
            )
            cfg = load_config()
            dash_url = f"http://{DEFAULT_HOST}:{int(cfg.get('port', DEFAULT_PORT))}/admin?token={one_time}"
            return self._send_json(HTTPStatus.OK, {
                "ok": True,
                "authenticated": True,
                "expires_at": int(sess.expires_at),
                "one_time_token": one_time,
                "dashboard_url": dash_url,
                "password_required": admin_password_required(),
            }, extra_headers={"Set-Cookie": cookie})

        if path == "/api/auth/logout":
            token = _parse_cookie_token(self)
            if token:
                SESSIONS.delete(token)
            append_log("info", "Admin logout")
            cookie = f"{SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"
            return self._send_json(HTTPStatus.OK, {"ok": True, "authenticated": False}, extra_headers={"Set-Cookie": cookie})

        # Auth-required endpoints
        if not _require_admin(self):
            return self._unauthorized()

        if path == "/api/config":
            cfg = load_config()
            for key in ("theme", "log_level", "auto_start"):
                if key in data:
                    cfg[key] = data[key]
            cfg["host"] = DEFAULT_HOST  # enforce localhost-only
            if "port" in data:
                try:
                    port_i = int(data["port"])
                    if 1 <= port_i <= 65535:
                        cfg["port"] = port_i
                except Exception:
                    pass
            cfg = save_config(cfg)
            append_log("info", "Configuration updated")
            return self._send_json(HTTPStatus.OK, {"ok": True, "config": cfg})

        if path == "/api/admin/password":
            current = str(data.get("current_password") or "")
            new_pw = str(data.get("new_password") or "")
            # Require current password when a password is currently required
            if admin_password_required():
                if not verify_admin_password(current):
                    return self._send_json(HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "Current password is incorrect"})
            result = set_admin_password(new_pw)
            status = HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST
            result["password_required"] = admin_password_required()
            return self._send_json(status, result)

        if path == "/api/action":
            action = str(data.get("action") or "").strip().lower()
            if action == "start":
                append_log("info", "Start requested (service already running)")
                return self._send_json(HTTPStatus.OK, {"ok": True, "action": action, "message": "Local service is running."})
            if action == "stop":
                append_log("info", "Stop requested via dashboard")
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return self._send_json(HTTPStatus.OK, {"ok": True, "action": action, "message": "Stopping local service..."})
            if action == "restart":
                append_log("info", "Restart requested via dashboard")
                try:
                    def _restart():
                        time.sleep(0.4)
                        try:
                            self.server.shutdown()
                        except Exception:
                            pass
                        time.sleep(0.2)
                        os.execv(sys.executable, [sys.executable] + sys.argv)
                    threading.Thread(target=_restart, daemon=True).start()
                    return self._send_json(HTTPStatus.OK, {"ok": True, "action": action, "message": "Restarting local service..."})
                except Exception as e:
                    return self._send_json(HTTPStatus.OK, {"ok": False, "action": action, "message": f"Restart failed: {e}. Restart via termux.py."})
            return self._send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "Unknown action"})

        if path == "/api/plugins":
            plugins = data.get("plugins")
            if isinstance(plugins, list):
                cleaned = []
                for p in plugins:
                    if not isinstance(p, dict):
                        continue
                    pid = str(p.get("id") or "").strip()
                    if not pid:
                        continue
                    cleaned.append({
                        "id": pid,
                        "name": str(p.get("name") or pid),
                        "enabled": bool(p.get("enabled", True)),
                        "description": str(p.get("description") or ""),
                    })
                save_plugins(cleaned)
                append_log("info", "Plugin settings updated")
                return self._send_json(HTTPStatus.OK, {"ok": True, "plugins": cleaned})
            return self._send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "Invalid plugins payload"})

        if path == "/api/backup/create":
            return self._send_json(HTTPStatus.OK, _backup_state())
        if path == "/api/backup/restore":
            return self._send_json(HTTPStatus.OK, _restore_backup(str(data.get("id") or "")))

        if path == "/api/tools/dependency_check":
            return self._send_json(HTTPStatus.OK, _dependency_check())
        if path == "/api/tools/permission_check":
            return self._send_json(HTTPStatus.OK, _permission_check())
        if path == "/api/tools/port_check":
            cfg = load_config()
            return self._send_json(HTTPStatus.OK, {"ok": True, "port_check": _check_port("127.0.0.1", int(cfg.get("port", DEFAULT_PORT))), "local_url": f"http://{DEFAULT_HOST}:{int(cfg.get('port', DEFAULT_PORT))}"})
        if path == "/api/tools/network_status":
            return self._send_json(HTTPStatus.OK, {"ok": True, "network": _read_network_info()})
        if path == "/api/tools/process_info":
            procs = _run_safe_command(["ps", "-eo", "pid,ppid,stat,comm"], timeout=2.0)
            return self._send_json(HTTPStatus.OK, {"ok": True, "process": _process_info(), "process_list": procs})
        if path == "/api/tools/config_validate":
            return self._send_json(HTTPStatus.OK, _config_validation())
        if path == "/api/tools/integrity_check":
            return self._send_json(HTTPStatus.OK, _hash_file(str(data.get("path") or "")))
        if path == "/api/tools/log_analyze":
            return self._send_json(HTTPStatus.OK, _analyze_logs())
        if path == "/api/tools/runtime_report":
            return self._send_json(HTTPStatus.OK, _runtime_report())
        if path == "/api/tools/sessions_info":
            return self._send_json(HTTPStatus.OK, _sessions_info())
        if path == "/api/tools/endpoint_inventory":
            return self._send_json(HTTPStatus.OK, _endpoint_inventory())
        if path == "/api/tools/readiness_check":
            return self._send_json(HTTPStatus.OK, _readiness_check())
        if path == "/api/tools/git_status":
            return self._send_json(HTTPStatus.OK, _git_status_summary())
        if path == "/api/tools/path_report":
            return self._send_json(HTTPStatus.OK, _path_report())
        if path == "/api/tools/auth_log_summary":
            return self._send_json(HTTPStatus.OK, _auth_log_summary())
        if path == "/api/tools/config_snapshot":
            return self._send_json(HTTPStatus.OK, _config_snapshot())
        if path == "/api/tools/diagnostics_bundle":
            return self._send_json(HTTPStatus.OK, _diagnostics_bundle())
        if path == "/api/tools/log_rotate":
            return self._send_json(HTTPStatus.OK, _rotate_log())
        if path == "/api/tools/self_test":
            return self._send_json(HTTPStatus.OK, _self_test())
        if path == "/api/health":
            return self._send_json(HTTPStatus.OK, _health_check())

        return self._send_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found"})

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        try:
            append_log("info", "http " + (fmt % args))
        except Exception:
            pass


def write_pid_file() -> None:
    try:
        get_pid_path().write_text(str(os.getpid()) + "\n", encoding="utf-8")
        try:
            os.chmod(get_pid_path(), 0o600)
        except Exception:
            pass
    except Exception:
        pass


def remove_pid_file() -> None:
    try:
        if get_pid_path().exists():
            get_pid_path().unlink()
    except Exception:
        pass


def run_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> int:
    host = DEFAULT_HOST  # enforce localhost-only by default
    load_or_init_admin()
    load_config()
    load_plugins()
    write_pid_file()
    append_log("info", f"Starting {APP_NAME} on http://{host}:{port}")
    server = ThreadingHTTPServer((host, port), LocalHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            server.server_close()
        except Exception:
            pass
        remove_pid_file()
        append_log("info", "Local service stopped")
    return 0


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run DeveloperHCR local service (localhost-only).")
    p.add_argument("--host", default=DEFAULT_HOST, help="Bind host (forced to 127.0.0.1 for safety)")
    p.add_argument("--port", type=int, default=DEFAULT_PORT, help="Bind port (default: 3383)")
    p.add_argument("--status", action="store_true", help="Print local service config/status paths and exit")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.status:
        cfg = load_config()
        load_or_init_admin()
        print(json.dumps({
            "service": APP_NAME,
            "local_url": f"http://{DEFAULT_HOST}:{int(cfg.get('port', DEFAULT_PORT))}",
            "localhost_only": True,
            "admin_password_required": admin_password_required(),
            "config": str(get_config_path()),
            "admin": str(get_admin_path()),
            "log": str(get_log_path()),
            "state_dir": str(get_state_dir()),
        }, indent=2))
        return 0
    port = int(args.port or DEFAULT_PORT)
    return run_server(host=DEFAULT_HOST, port=port)


if __name__ == "__main__":
    raise SystemExit(main())
