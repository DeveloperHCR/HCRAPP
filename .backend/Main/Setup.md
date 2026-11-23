# Local Setup (Termux)

`termux.py` is the main launcher for the Termux/local version.

- Start: `python3 termux.py`
- Local service: `pages/notinwebsite/local.py` (localhost only, default `http://127.0.0.1:3383`)
- Public GitHub Pages site does not execute Python; it only links to the local service where appropriate.
- Admin access is protected and validated server-side by the local service.
