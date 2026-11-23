#!/usr/bin/env python3
"""DeveloperHCR Termux/Linux terminal helper.

Provides a professional first-time setup screen for Termux and standard Linux
terminals while keeping the script extensible for future setup actions.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import sys
import textwrap
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


APP_NAME = "DeveloperHCR HCRAPP Termux Setup"
DEFAULT_NAME = "USER"
DEFAULT_PORT = 3383
DEFAULT_URL = f"http://localhost:{DEFAULT_PORT}"
CONFIG_VERSION = 1


@dataclass
class SetupConfig:
    version: int = CONFIG_VERSION
    first_time_completed: bool = False
    name: str = DEFAULT_NAME
    username: str = ""
    password_set: bool = False
    # Password value is intentionally not stored by default in this repository
    # helper. Local optional auth can be extended by future setup flows.


def _stdout_supports_unicode() -> bool:
    enc = getattr(sys.stdout, "encoding", None) or ""
    try:
        "DeveloperHCR™".encode(enc or "utf-8")
        return True
    except Exception:
        return False


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _supports_unicode_box() -> bool:
    if not _stdout_supports_unicode():
        return False
    # Prefer simple ASCII on very limited environments; TERMUX_VERSION usually fine.
    return True


class UI:
    def __init__(self) -> None:
        self.term_width = shutil.get_terminal_size((80, 24)).columns
        self.max_width = max(40, min(self.term_width, 76))
        self.color = _supports_color()
        self.unicode = _supports_unicode_box()
        self.tm = "™" if _stdout_supports_unicode() else "(TM)"

    def refresh(self) -> None:
        self.term_width = shutil.get_terminal_size((80, 24)).columns
        self.max_width = max(40, min(self.term_width, 76))

    def _ansi(self, code: str, text: str) -> str:
        if not self.color:
            return text
        return f"\033[{code}m{text}\033[0m"

    def bold(self, text: str) -> str:
        return self._ansi("1", text)

    def dim(self, text: str) -> str:
        return self._ansi("2", text)

    def cyan(self, text: str) -> str:
        return self._ansi("36", text)

    def bright_cyan(self, text: str) -> str:
        return self._ansi("96", text)

    def green(self, text: str) -> str:
        return self._ansi("32", text)

    def yellow(self, text: str) -> str:
        return self._ansi("33", text)

    def magenta(self, text: str) -> str:
        return self._ansi("35", text)

    @staticmethod
    def _visible_len(text: str) -> int:
        return len(re.sub(r"\033\[[0-9;]*m", "", text))

    def center(self, text: str, width: Optional[int] = None) -> str:
        w = width or self.max_width
        pad = max(0, (w - self._visible_len(text)) // 2)
        return (" " * pad) + text

    def hr(self, char: Optional[str] = None) -> str:
        ch = char or ("─" if self.unicode else "-")
        return ch * self.max_width

    def line(self, text: str = "", center: bool = False) -> None:
        if center:
            print(self.center(text))
        else:
            print(text)

    def blank(self, n: int = 1) -> None:
        for _ in range(n):
            print()

    def banner_brand(self) -> List[str]:
        # Prominent, professional branding compatible with limited terminals.
        title = f"DeveloperHCR{self.tm}"
        if self.unicode and self.max_width >= 54:
            top = "╔" + "═" * (self.max_width - 2) + "╗"
            bottom = "╚" + "═" * (self.max_width - 2) + "╝"
            inner_pad = self.max_width - 2
            mid = "║" + title.center(inner_pad) + "║"
            return [
                self.bright_cyan(self.bold(top)),
                self.bright_cyan(self.bold(mid)),
                self.bright_cyan(self.bold(bottom)),
            ]
        # Fallback: strong centered line with separators.
        sep = "=" * min(len(title) + 8, self.max_width)
        return [
            self.bright_cyan(self.bold(self.center(sep))),
            self.bright_cyan(self.bold(self.center(title))),
            self.bright_cyan(self.bold(self.center(sep))),
        ]

    def banner_subtitle(self) -> str:
        subtitle = "First Time Setup"
        if self.unicode and self.max_width >= 40:
            decorated = f"── {subtitle} ──"
        else:
            decorated = f"-- {subtitle} --"
        return self.cyan(self.bold(self.center(decorated)))


def get_config_path() -> Path:
    # Works in Termux and standard Linux terminals.
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        base = Path(xdg)
    else:
        base = Path.home() / ".config"
    return base / "developerhcr" / "hcrapp_termux_setup.json"


def load_config(path: Path) -> SetupConfig:
    if not path.exists():
        return SetupConfig()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return SetupConfig()
        cfg = SetupConfig()
        cfg.version = int(data.get("version", CONFIG_VERSION) or CONFIG_VERSION)
        cfg.first_time_completed = bool(data.get("first_time_completed", False))
        name = data.get("name", DEFAULT_NAME)
        cfg.name = str(name).strip() or DEFAULT_NAME
        cfg.username = str(data.get("username", "") or "").strip()
        cfg.password_set = bool(data.get("password_set", False))
        return cfg
    except Exception:
        return SetupConfig()


def save_config(path: Path, cfg: SetupConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(cfg)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def format_kv(label: str, value: str, label_width: int = 24) -> str:
    # Keep layout clean; avoid excessive width.
    left = f"{label:<{label_width}}"
    return left + value


def render_setup_screen(ui: UI, cfg: SetupConfig) -> None:
    ui.refresh()
    ui.blank(1)
    for line in ui.banner_brand():
        print(line)
    ui.blank(1)
    print(ui.banner_subtitle())
    ui.blank(1)

    # Core setup information block.
    lines = [
        format_kv("Setup:", "-"),
        "",
        format_kv("Name:", f"{cfg.name or DEFAULT_NAME} (DEFAULT)        (Optional)"),
        "",
        format_kv("PASSWORD:", "NOT REQUIRED"),
        "",
        "Username:",
        "Password:",
        "",
        ui.green(DEFAULT_URL),
        "",
        ui.bold("To setup more..."),
    ]

    # Render block centered as a whole when possible for a balanced look.
    block_width = min(max((ui._visible_len(l) for l in lines if l), default=0), ui.max_width)
    left_pad = max(0, (ui.max_width - block_width) // 2)
    indent = " " * left_pad
    for l in lines:
        if l == "":
            print()
            continue
        print(indent + l)

    ui.blank(1)
    # Extra helpful section under "To setup more..." while keeping UI clean.
    tips = [
        "- Optional: configure username/password for local setup preferences.",
        "- URL shown above can be used by compatible local services/setup flows.",
        "- Re-run anytime with: python3 termux.py --setup",
    ]
    tip_indent = indent
    for t in tips:
        wrapped = textwrap.wrap(t, width=max(30, ui.max_width - left_pad)) or [t]
        for i, wline in enumerate(wrapped):
            prefix = "" if i == 0 else "  "
            print(tip_indent + ui.dim(prefix + wline))
    ui.blank(1)


def prompt_optional(label: str, default: str = "", secret: bool = False) -> Optional[str]:
    try:
        prompt = f"{label}" + (f" [{default}]" if default else "") + ": "
        if secret:
            value = getpass.getpass(prompt)
        else:
            value = input(prompt)
    except EOFError:
        return None
    except KeyboardInterrupt:
        print()
        return None
    value = (value or "").strip()
    if value == "" and default:
        return default
    return value


def interactive_setup(ui: UI, cfg: SetupConfig) -> SetupConfig:
    print(ui.dim(ui.center("Press Enter to accept defaults. Username/Password are optional.")))
    ui.blank(1)

    name = prompt_optional("Display Name (optional)", default=cfg.name or DEFAULT_NAME, secret=False)
    if name is not None and name.strip():
        cfg.name = name.strip()
    elif not (cfg.name or "").strip():
        cfg.name = DEFAULT_NAME

    username = prompt_optional("Username (optional)", default=cfg.username, secret=False)
    if username is not None:
        cfg.username = username.strip()

    # Password optional and not required. Use hidden input when available.
    try:
        pw_prompt = "Password (optional, hidden input)"
        password = getpass.getpass(f"{pw_prompt}: ")
    except EOFError:
        password = None
    except KeyboardInterrupt:
        print()
        password = None
    except Exception:
        password = prompt_optional("Password (optional)", default="", secret=False)

    if password is not None and password != "":
        # Do not persist raw password in this helper's config; mark as configured.
        cfg.password_set = True
    # If left blank, keep previous state as-is (do not force-clear).

    cfg.first_time_completed = True
    return cfg


def print_post_setup_summary(ui: UI, cfg: SetupConfig, config_path: Path) -> None:
    ui.blank(1)
    print(ui.green(ui.bold(ui.center("Setup complete."))))
    ui.blank(1)
    summary = [
        f"Name: {cfg.name or DEFAULT_NAME}",
        f"Username: {cfg.username or '(not set)'}",
        f"Password: {'Configured locally (optional)' if cfg.password_set else 'NOT REQUIRED / not set'}",
        f"Service URL: {DEFAULT_URL}",
        f"Config: {config_path}",
    ]
    for s in summary:
        print(ui.center(s))
    ui.blank(1)
    print(ui.center(ui.dim("Tip: run with --show to view setup status without prompts.")))


def show_status(ui: UI, cfg: SetupConfig, config_path: Path) -> None:
    render_setup_screen(ui, cfg)
    print(ui.center(ui.dim(f"First-time setup completed: {'yes' if cfg.first_time_completed else 'no'}")))
    print(ui.center(ui.dim(f"Local config: {config_path}")))


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DeveloperHCR first-time terminal setup for Termux/Linux."
    )
    parser.add_argument("--setup", action="store_true", help="Run interactive setup screen now.")
    parser.add_argument("--show", action="store_true", help="Show setup/status screen without prompts.")
    parser.add_argument(
        "--reset-setup",
        action="store_true",
        help="Mark first-time setup as incomplete so the setup screen runs on next start.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Do not prompt for input; display the setup screen/status only.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    ui = UI()
    config_path = get_config_path()
    cfg = load_config(config_path)

    if args.reset_setup:
        cfg.first_time_completed = False
        save_config(config_path, cfg)
        print(ui.yellow("First-time setup has been reset."))
        print(ui.dim(f"Config: {config_path}"))
        return 0

    should_run_setup = args.setup or (not cfg.first_time_completed)
    show_only = args.show or args.non_interactive or not sys.stdin.isatty()

    if should_run_setup:
        render_setup_screen(ui, cfg)
        if show_only:
            if not sys.stdin.isatty() and not args.show and not args.non_interactive:
                print(ui.dim(ui.center("Non-interactive terminal detected; prompts skipped.")))
            # Persist completion marker on first display in non-interactive mode only
            # when explicitly requested via setup flow would be surprising; keep state.
            return 0

        # Interactive first-time/setup flow.
        try:
            cfg = interactive_setup(ui, cfg)
            save_config(config_path, cfg)
            print_post_setup_summary(ui, cfg, config_path)
        except Exception as exc:
            print(ui.yellow(f"Setup encountered an issue: {exc}"))
            print(ui.dim("You can re-run with: python3 termux.py --setup"))
            return 1
        return 0

    # Existing setup present: keep behavior working and provide status view.
    if args.show:
        show_status(ui, cfg, config_path)
        return 0

    # Default run when setup already completed: show compact status and options.
    ui.blank(1)
    print(ui.bright_cyan(ui.bold(ui.center(f"DeveloperHCR{ui.tm}"))))
    print(ui.center(ui.dim("Terminal setup is ready.")))
    ui.blank(1)
    print(ui.center(f"Name: {cfg.name or DEFAULT_NAME}"))
    print(ui.center(f"URL: {DEFAULT_URL}"))
    ui.blank(1)
    print(ui.center(ui.dim("To setup more... run: python3 termux.py --setup")))
    print(ui.center(ui.dim("For status: python3 termux.py --show")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
