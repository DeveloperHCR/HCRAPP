#!/usr/bin/env python3
"""DeveloperHCR local setup backend for http://localhost:3383."""

from __future__ import annotations

import argparse
import html
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

try:
    from . import connecte
except Exception:  # pragma: no cover - script execution fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import connecte  # type: ignore


LOGO_URL = "https://raw.githubusercontent.com/DeveloperHCR/HCRAPP/main/.backend/Main/data.png"
LOGO_PAGE_URL = "https://github.com/DeveloperHCR/HCRAPP/blob/main/.backend/Main/data.png"


def _page(title: str, body: str) -> bytes:
    doc = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{
      margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: linear-gradient(180deg, #f4fbff 0%, #ffffff 60%);
      color: #10233a;
    }}
    .wrap {{ max-width: 720px; margin: 0 auto; padding: 32px 20px 48px; }}
    .card {{
      background: #fff; border: 1px solid #d7e6f5; border-radius: 18px;
      box-shadow: 0 10px 30px rgba(16,35,58,0.08); padding: 24px;
    }}
    .logo {{ display: flex; justify-content: center; margin-bottom: 16px; }}
    .logo img {{ width: 140px; height: auto; border-radius: 16px; }}
    h1 {{ margin: 0 0 8px; text-align: center; font-size: 1.8rem; }}
    p.lead {{ margin: 0 0 20px; text-align: center; color: #35506f; }}
    form {{ display: grid; gap: 14px; margin-top: 8px; }}
    label {{ font-weight: 600; font-size: 0.95rem; }}
    input {{
      width: 100%; box-sizing: border-box; padding: 12px 14px; border-radius: 12px;
      border: 1px solid #bfd3e8; font-size: 1rem;
    }}
    button {{
      margin-top: 6px; padding: 12px 16px; border: 0; border-radius: 12px;
      background: #0891b2; color: #fff; font-weight: 700; font-size: 1rem; cursor: pointer;
    }}
    .note {{ margin-top: 16px; color: #45627f; font-size: 0.92rem; }}
    .ok {{ background: #ecfeff; border: 1px solid #a5f3fc; padding: 12px 14px; border-radius: 12px; }}
    .meta {{ margin-top: 18px; font-size: 0.9rem; color: #35506f; }}
    a {{ color: #0b6f86; }}
    code {{ background: #f1f7fb; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"card\">
      {body}
    </div>
  </div>
</body>
</html>"""
    return doc.encode("utf-8")


def render_setup_form(message: str = "", data: dict | None = None) -> bytes:
    data = data or connecte.load_setup_data()
    username = html.escape(str(data.get("username", "") or ""))
    password = html.escape(str(data.get("password", "") or ""))
    completed = bool(data.get("completed"))
    banner = f'<div class="ok">{html.escape(message)}</div>' if message else ""
    status = "Setup completed." if completed else "Fill username and password to complete setup."
    body = f"""
      <div class=\"logo\">
        <img src=\"{LOGO_URL}\" alt=\"DeveloperHCR logo\" />
      </div>
      <h1>DeveloperHCR™ Setup</h1>
      <p class=\"lead\">Open local setup at <code>{html.escape(connecte.DEFAULT_URL)}</code> and complete your details below.</p>
      {banner}
      <p><strong>Status:</strong> {html.escape(status)}</p>
      <form method=\"post\" action=\"/setup\">
        <div>
          <label for=\"username\">Username</label>
          <input id=\"username\" name=\"username\" type=\"text\" value=\"{username}\" placeholder=\"Enter username\" autocomplete=\"username\" />
        </div>
        <div>
          <label for=\"password\">Password</label>
          <input id=\"password\" name=\"password\" type=\"password\" value=\"{password}\" placeholder=\"Enter password\" autocomplete=\"current-password\" />
        </div>
        <button type=\"submit\">Save setup</button>
      </form>
      <p class=\"note\">Password is optional in terminal setup, but you can fill username and password here for local web setup.</p>
      <p class=\"meta\">Logo location: <a href=\"{LOGO_PAGE_URL}\">{html.escape(LOGO_PAGE_URL)}</a></p>
    """
    return _page("DeveloperHCR Setup", body)


def render_success(data: dict) -> bytes:
    username = html.escape(str(data.get("username", "") or "(not set)"))
    has_password = "set" if data.get("password") else "not set"
    body = f"""
      <div class=\"logo\">
        <img src=\"{LOGO_URL}\" alt=\"DeveloperHCR logo\" />
      </div>
      <h1>Setup Saved</h1>
      <div class=\"ok\">Your local setup details were saved successfully.</div>
      <div class=\"meta\">
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Password:</strong> {has_password}</p>
        <p><strong>URL:</strong> <code>{html.escape(connecte.DEFAULT_URL)}</code></p>
        <p><a href=\"/\">Back to setup</a></p>
      </div>
      <p class=\"meta\">Logo location: <a href=\"{LOGO_PAGE_URL}\">{html.escape(LOGO_PAGE_URL)}</a></p>
    """
    return _page("DeveloperHCR Setup Complete", body)


class SetupHandler(BaseHTTPRequestHandler):
    server_version = "DeveloperHCRSetup/1.0"

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/setup"):
            content = render_setup_form()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/setup":
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
        except Exception:
            length = 0
        raw = self.rfile.read(max(0, length)).decode("utf-8", errors="replace")
        form = parse_qs(raw, keep_blank_values=True)
        username = (form.get("username", [""])[0] or "").strip()
        password = form.get("password", [""])[0] or ""
        data = connecte.save_setup_data(username=username, password=password)
        content = render_success(data)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt: str, *args) -> None:  # quieter console
        sys.stdout.write("[setup] " + (fmt % args) + "\n")


def run_server(host: str = connecte.DEFAULT_HOST, port: int = connecte.DEFAULT_PORT) -> int:
    server = ThreadingHTTPServer((host, port), SetupHandler)
    print(f"DeveloperHCR local setup server running at {connecte.DEFAULT_URL}")
    print(f"Logo: {LOGO_PAGE_URL}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DeveloperHCR local setup backend server.")
    parser.add_argument("--host", default=connecte.DEFAULT_HOST, help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=connecte.DEFAULT_PORT, help="Port to bind (default: 3383)")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(run_server(host=args.host, port=args.port))
