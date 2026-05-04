"""
Main Ricker browser window.

Manages tabs, the menu bar, theme switching, and clean shutdown.

Bugs fixed from the original Ricker_Browser:
  - "+" tab could become active and render nothing  -> uses tabBar corner widget instead
  - Closing last real tab left "+" tab active        -> always opens a new tab if last is closed
  - Theme stylesheet was overwritten by toolbar pick -> separate concerns: theme vs accent
  - Flask thread couldn't be shut down               -> daemon thread in flask_server.py
  - set_homepage forced local file picker            -> now accepts URL string via input dialog
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QInputDialog,
    QMainWindow,
    QPushButton,
    QShortcut,
    QStatusBar,
    QTabWidget,
)

from app.tab_widget import BrowserTab
from app.styles import DARK, LIGHT, build_stylesheet


class RickerBrowser(QMainWindow):
    """The main browser window holding a tab widget and menu bar."""

    def __init__(self, homepage_url: str):
        super().__init__()

        self.homepage_url = homepage_url
        self.theme_name = "dark"

        self.setWindowTitle("Ricker")
        self.setGeometry(100, 100, 1280, 820)
        self.setMinimumSize(800, 500)

        # ---------------- Tab widget ----------------
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # New-tab button as a tabbar corner widget, which is better UX than a "+" tab
        new_tab_button = QPushButton("+")
        new_tab_button.setToolTip("New tab (Ctrl+T)")
        new_tab_button.setFixedSize(32, 32)
        new_tab_button.setObjectName("newTabButton")
        new_tab_button.clicked.connect(self._open_new_tab)
        self.tabs.setCornerWidget(new_tab_button, Qt.TopRightCorner)

        self.setCentralWidget(self.tabs)

        # ---------------- Menu bar ----------------
        self._build_menus()

        # ---------------- Status bar ----------------
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # ---------------- Keyboard shortcuts ----------------
        self._setup_shortcuts()

        # ---------------- Theme ----------------
        self._apply_theme()

        # ---------------- First tab ----------------
        self._open_new_tab()

    # ============================================================
    # MENU
    # ============================================================
    def _build_menus(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        new_tab = QAction("New Tab", self)
        new_tab.setShortcut(QKeySequence("Ctrl+T"))
        new_tab.triggered.connect(self._open_new_tab)
        file_menu.addAction(new_tab)

        close_tab = QAction("Close Tab", self)
        close_tab.setShortcut(QKeySequence("Ctrl+W"))
        close_tab.triggered.connect(
            lambda: self._close_tab(self.tabs.currentIndex())
        )
        file_menu.addAction(close_tab)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        view_menu = menu_bar.addMenu("View")
        toggle_theme = QAction("Toggle Theme", self)
        toggle_theme.setShortcut(QKeySequence("Ctrl+Shift+T"))
        toggle_theme.triggered.connect(self._toggle_theme)
        view_menu.addAction(toggle_theme)

        settings_menu = menu_bar.addMenu("Settings")
        set_home = QAction("Set Homepage URL", self)
        set_home.triggered.connect(self._set_homepage)
        settings_menu.addAction(set_home)

    # ============================================================
    # KEYBOARD SHORTCUTS
    # ============================================================
    def _setup_shortcuts(self) -> None:
        # Cmd/Ctrl+L focuses the URL bar (browser-standard shortcut)
        QShortcut(QKeySequence("Ctrl+L"), self, self._focus_url_bar)
        QShortcut(QKeySequence("Ctrl+R"), self, self._reload_current_tab)

    def _focus_url_bar(self) -> None:
        tab = self.tabs.currentWidget()
        if isinstance(tab, BrowserTab):
            tab.url_bar.setFocus()
            tab.url_bar.selectAll()

    def _reload_current_tab(self) -> None:
        tab = self.tabs.currentWidget()
        if isinstance(tab, BrowserTab):
            tab.webview.reload()

    # ============================================================
    # TABS
    # ============================================================
    def _open_new_tab(self) -> None:
        tab = BrowserTab(self.homepage_url)
        tab.webview.titleChanged.connect(
            lambda title, t=tab: self._update_tab_title(t, title)
        )
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        # Focus the URL bar so users can type immediately
        tab.url_bar.setFocus()

    def _close_tab(self, index: int) -> None:
        if index < 0:
            return

        widget = self.tabs.widget(index)
        if widget is not None:
            widget.deleteLater()
        self.tabs.removeTab(index)

        # Always keep at least one tab open
        if self.tabs.count() == 0:
            self._open_new_tab()

    def _update_tab_title(self, tab: BrowserTab, title: str) -> None:
        index = self.tabs.indexOf(tab)
        if index >= 0:
            display = (title[:30] + "...") if len(title) > 30 else (title or "New Tab")
            self.tabs.setTabText(index, display)

    def _on_tab_changed(self, index: int) -> None:
        tab = self.tabs.widget(index)
        if isinstance(tab, BrowserTab):
            self.setWindowTitle(f"Ricker - {tab.page_title()}")
            self.status.showMessage(tab.page_url(), 5000)

    # ============================================================
    # THEME
    # ============================================================
    def _apply_theme(self) -> None:
        palette = DARK if self.theme_name == "dark" else LIGHT
        self.setStyleSheet(build_stylesheet(palette))

    def _toggle_theme(self) -> None:
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self._apply_theme()
        self.status.showMessage(f"Theme: {self.theme_name}", 2000)

    # ============================================================
    # SETTINGS
    # ============================================================
    def _set_homepage(self) -> None:
        url, ok = QInputDialog.getText(
            self,
            "Set Homepage",
            "Homepage URL:",
            text=self.homepage_url,
        )
        if ok and url:
            if not url.startswith(("http://", "https://", "file://")):
                url = "https://" + url
            self.homepage_url = url
            self.status.showMessage(f"Homepage set to {url}", 3000)
