"""
Single browser tab: webview + toolbar with nav controls + URL bar +
visible engine picker dropdown.

Each tab carries its own active search engine state so different tabs
can use different engines (e.g., one tab on Google, another on Kagi).
"""
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QAction,
    QLineEdit,
    QMenu,
    QPushButton,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

from app.engines import SEARCH_ENGINES, by_name


class BrowserTab(QWidget):
    """A single browsing tab with its own toolbar and webview."""

    def __init__(self, initial_url: str, parent=None):
        super().__init__(parent)

        self.current_engine = "Google"

        # ---------------- Web view ----------------
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(initial_url))
        self.webview.urlChanged.connect(self._on_url_changed)
        self.webview.titleChanged.connect(self._on_title_changed)
        self.webview.loadStarted.connect(self._on_load_started)
        self.webview.loadFinished.connect(self._on_load_finished)

        # ---------------- Toolbar ----------------
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(self.toolbar.iconSize())

        # Use unicode glyphs as icons. These render reliably across
        # platforms without bundling SVG/PNG assets.
        self.back_action = QAction("\u2190", self)        # ←
        self.back_action.setToolTip("Back")
        self.back_action.triggered.connect(self.webview.back)
        self.toolbar.addAction(self.back_action)

        self.forward_action = QAction("\u2192", self)     # →
        self.forward_action.setToolTip("Forward")
        self.forward_action.triggered.connect(self.webview.forward)
        self.toolbar.addAction(self.forward_action)

        self.reload_action = QAction("\u21bb", self)      # ↻
        self.reload_action.setToolTip("Reload")
        self.reload_action.triggered.connect(self.webview.reload)
        self.toolbar.addAction(self.reload_action)

        self.home_action = QAction("\u2302", self)        # ⌂
        self.home_action.setToolTip("Home")
        self.home_action.triggered.connect(self._go_home)
        self.toolbar.addAction(self.home_action)

        # ---------------- URL bar ----------------
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL")
        self.url_bar.returnPressed.connect(self._on_url_submitted)
        self.toolbar.addWidget(self.url_bar)

        # ---------------- Engine picker dropdown ----------------
        # This replaces the original double-click-to-switch which was
        # invisible to new users.
        self.engine_button = QPushButton(self.current_engine + " \u25BE")
        self.engine_button.setObjectName("engineButton")
        self.engine_button.setToolTip("Switch search engine")
        self.engine_button.clicked.connect(self._show_engine_menu)
        self.toolbar.addWidget(self.engine_button)

        # ---------------- Layout ----------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.webview)
        self.setLayout(layout)

        # Keep a stable reference to the home URL set at construction
        self._home_url = initial_url

    # ============================================================
    # ENGINE SWITCHING
    # ============================================================
    def _show_engine_menu(self) -> None:
        menu = QMenu(self)
        for engine in SEARCH_ENGINES:
            action = QAction(engine["name"], self)
            action.triggered.connect(
                lambda _, name=engine["name"]: self._switch_engine(name)
            )
            menu.addAction(action)

        # Position the menu directly under the engine button
        button = self.engine_button
        pos = button.mapToGlobal(button.rect().bottomLeft())
        menu.exec_(pos)

    def _switch_engine(self, name: str) -> None:
        self.current_engine = name
        self.engine_button.setText(f"{name} \u25BE")
        engine = by_name(name)
        self.webview.setUrl(QUrl(engine["home"]))

    # ============================================================
    # URL HANDLING
    # ============================================================
    def _on_url_submitted(self) -> None:
        text = self.url_bar.text().strip()
        if not text:
            return

        # If it looks like a URL, navigate directly
        if text.startswith(("http://", "https://")):
            self.webview.setUrl(QUrl(text))
        elif "." in text and " " not in text:
            self.webview.setUrl(QUrl("https://" + text))
        else:
            # Otherwise, search via the current engine
            engine = by_name(self.current_engine)
            search_url = engine["search"].format(q=text)
            self.webview.setUrl(QUrl(search_url))

    def _on_url_changed(self, url: QUrl) -> None:
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)

    def _on_title_changed(self, title: str) -> None:
        # Forwarded to the parent QTabWidget by the main window
        pass

    def _on_load_started(self) -> None:
        self.reload_action.setText("\u2715")  # ✕ to stop loading

    def _on_load_finished(self, ok: bool) -> None:
        self.reload_action.setText("\u21bb")  # ↻ back to reload

    def _go_home(self) -> None:
        self.webview.setUrl(QUrl(self._home_url))

    # ============================================================
    # PUBLIC HELPERS for the main window
    # ============================================================
    def page_title(self) -> str:
        return self.webview.title() or "New Tab"

    def page_url(self) -> str:
        return self.webview.url().toString()
