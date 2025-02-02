import sys
import os
from threading import Thread
from flask import Flask, render_template
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTabWidget, QToolBar, QAction, QMenu, QColorDialog, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl

# Flask application setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')  # Ensure homepage.html exists in the templates folder


def run_flask():
    app.run(debug=True, use_reloader=False)  # Prevent Flask from running twice


# PyQt5 custom browser class
class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ricker")
        self.setGeometry(100, 100, 1200, 800)

        self.default_homepage = "http://127.0.0.1:5000/"
        self.theme = "light"  # Default theme: "light" or "dark"

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.select_browser_for_tab)
        self.tabs.currentChanged.connect(self.update_tab_title)

        # Add a "+" tab for creating new tabs
        self.tabs.addTab(QWidget(), "+")
        self.tabs.tabBarClicked.connect(self.handle_plus_tab)

        self.setCentralWidget(self.tabs)

        # Add the first tab
        self.add_new_tab(self.default_homepage, "Ricker")

        # Menu bar for customizations
        self.menu_bar = self.menuBar()
        self.setup_menu()

    def setup_menu(self):
        settings_menu = self.menu_bar.addMenu("Settings")

        # Theme customization
        theme_action = QAction("Change Theme", self)
        theme_action.triggered.connect(self.change_theme)
        settings_menu.addAction(theme_action)

        # Toolbar customization
        customize_toolbar_action = QAction("Customize Toolbar", self)
        customize_toolbar_action.triggered.connect(self.customize_toolbar)
        settings_menu.addAction(customize_toolbar_action)

        # Set Homepage
        set_homepage_action = QAction("Set Homepage", self)
        set_homepage_action.triggered.connect(self.set_homepage)
        settings_menu.addAction(set_homepage_action)

    def add_new_tab(self, url, title):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))

        # Toolbar with compact controls
        toolbar = QToolBar()
        toolbar.setMovable(False)

        back_action = QAction("<<", self)
        back_action.triggered.connect(browser.back)
        toolbar.addAction(back_action)

        forward_action = QAction(">>", self)
        forward_action.triggered.connect(browser.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("⟳", self)
        reload_action.triggered.connect(browser.reload)
        toolbar.addAction(reload_action)

        nav_bar = QLineEdit()
        nav_bar.setPlaceholderText("Enter URL...")
        nav_bar.returnPressed.connect(lambda: self.load_url(browser, nav_bar))
        toolbar.addWidget(nav_bar)

        # Layout for the tab
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(toolbar)
        tab_layout.addWidget(browser)

        # Set up the tab widget
        tab_widget = QWidget()
        tab_widget.setLayout(tab_layout)

        index = self.tabs.count() - 1
        self.tabs.insertTab(index, tab_widget, title)
        self.tabs.setCurrentIndex(index)

    def handle_plus_tab(self, index):
        # Check if "+" tab is clicked
        if index == self.tabs.count() - 1:
            self.add_new_tab(self.default_homepage, "New Tab")

    def select_browser_for_tab(self, index):
        if index != self.tabs.count() - 1:  # Ignore the "+" tab
            menu = QMenu(self)
            search_engines = {
                "Google": "https://www.google.com",
                "DuckDuckGo": "https://duckduckgo.com",
                "Bing": "https://www.bing.com",
                "Yahoo": "https://www.yahoo.com",
                "StartPage": "https://www.startpage.com",
                "Brave": "https://search.brave.com",
                "Yandex": "https://yandex.com",
                "Ecosia": "https://www.ecosia.org",
                "Qwant": "https://www.qwant.com",
                "Opera": "https://www.opera.com",
            }

            for engine, url in search_engines.items():
                action = QAction(engine, self)
                action.triggered.connect(lambda _, u=url, i=index: self.change_browser_for_tab(i, u, engine))
                menu.addAction(action)

            menu.exec_(self.mapToGlobal(self.tabs.tabBar().tabRect(index).center()))

    def change_browser_for_tab(self, index, url, engine_name):
        browser = self.tabs.widget(index).layout().itemAt(1).widget()
        browser.setUrl(QUrl(url))
        self.tabs.setTabText(index, engine_name)

    def load_url(self, browser, nav_bar):
        url = nav_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        browser.setUrl(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 2:  # Keep at least one tab + "+"
            self.tabs.removeTab(index)

    def update_tab_title(self, index):
        if index != self.tabs.count() - 1:  # Ignore the "+" tab
            self.setWindowTitle("Ricker")

    def change_theme(self):
        if self.theme == "light":
            self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
            self.theme = "dark"
        else:
            self.setStyleSheet("")
            self.theme = "light"

    def customize_toolbar(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    def set_homepage(self):
        homepage, _ = QFileDialog.getOpenFileName(self, "Select Homepage", "", "HTML Files (*.html);;All Files (*)")
        if homepage:
            self.default_homepage = homepage


def run_gui():
    app = QApplication(sys.argv)
    browser = CustomBrowser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Create separate threads for Flask and PyQt application
    flask_thread = Thread(target=run_flask)
    gui_thread = Thread(target=run_gui)

    # Start both threads
    flask_thread.start()
    gui_thread.start()

    # Wait for threads to finish
    flask_thread.join()
    gui_thread.join()
