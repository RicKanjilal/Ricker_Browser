"""
Background Flask server for the dashboard homepage.

Original code used a non-daemon thread that prevented clean shutdown.
This version:
  - Runs Flask in a daemon thread so it dies with the main process
  - Suppresses Flask's startup banner so the terminal stays clean
  - Picks a free port automatically if 5000 is taken
  - Exposes a one-line start_server() function for the main app
"""
import logging
import socket
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template


def _find_free_port(preferred: int = 5000) -> int:
    """
    Try the preferred port. If taken, ask the OS for any free port.

    Avoids the 'Address already in use' crash if the user has another
    Ricker instance running, or any service on 5000.
    """
    for port in (preferred, 5001, 5002, 5003):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    # Last resort: ask the OS for any free port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def create_app() -> Flask:
    """Build and return a configured Flask app."""
    # Resolve the templates / static folders relative to this file's parent
    here = Path(__file__).resolve().parent.parent
    templates = str(here / "homepage" / "templates")
    static = str(here / "homepage" / "static")

    app = Flask(
        __name__,
        template_folder=templates,
        static_folder=static,
    )

    # Quiet down werkzeug logging, which spams the terminal otherwise
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    @app.route("/")
    def home():
        return render_template("homepage.html")

    @app.route("/api/ping")
    def ping():
        """Health check used by the PyQt side to verify Flask is up."""
        return jsonify({"ok": True})

    return app


def start_server() -> int:
    """
    Spin up the Flask server in a background daemon thread.

    Returns the port it bound to. The port may differ from 5000 if
    another process holds that port.
    """
    port = _find_free_port()
    app = create_app()

    def _run():
        # use_reloader=False so we don't fork twice
        # debug=False so we don't dump tracebacks at users
        app.run(
            host="127.0.0.1",
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True,
        )

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return port
