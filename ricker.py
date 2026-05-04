#!/usr/bin/env python3
"""
Ricker: a multi-search-engine desktop browser.

Run with:
    python ricker.py

What it does:
  - Spins up a Flask server on a free port (5000 by default)
  - Serves a dashboard homepage as the default new-tab page
  - Opens a PyQt5 window with browser tabs
  - Each tab can search via 10 different engines, switchable via dropdown

Architecture:
  - app/flask_server.py    -- background Flask thread (daemon)
  - app/browser_window.py  -- main QMainWindow with tab management
  - app/tab_widget.py      -- individual browser tab
  - app/engines.py         -- search engine registry
  - app/styles.py          -- centralized theme + stylesheet builder
  - homepage/              -- dashboard HTML/CSS/JS
"""
import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication

from app.browser_window import RickerBrowser
from app.flask_server import start_server


def main() -> int:
    # High-DPI rendering: critical for the modern look on retina/4K displays
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Start the Flask homepage server in the background
    port = start_server()
    homepage_url = f"http://127.0.0.1:{port}/"

    # Launch the Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Ricker")
    app.setOrganizationName("RicKanjilal")

    window = RickerBrowser(homepage_url)
    window.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
