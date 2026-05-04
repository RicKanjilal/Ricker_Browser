"""
Theme + style constants for the entire app.

Keeping all styling here means changing the look-and-feel is a one-file edit
instead of hunting through every widget class. Both themes follow a similar
palette: a deep base, a slightly lifted surface, and a single accent color.
"""

# ============================================================
# DESIGN TOKENS
# ============================================================
DARK = {
    "bg":          "#0a0b0f",     # deepest base, the window background
    "surface":     "#13151b",     # toolbars, tab bar, slightly raised
    "surface_hi":  "#1c1e26",     # buttons, cards, hovered states
    "border":      "#262830",     # subtle dividers
    "text":        "#e6e8ed",     # primary text
    "text_dim":    "#8b8f99",     # secondary text, placeholders
    "accent":      "#7c5cff",     # purple-blue, our brand color
    "accent_dim":  "#5847cc",     # darker variant for hover
    "danger":      "#ff5c8a",     # close buttons, errors
}

LIGHT = {
    "bg":          "#fafbfc",
    "surface":     "#ffffff",
    "surface_hi":  "#f0f2f5",
    "border":      "#e1e4e8",
    "text":        "#1a1d24",
    "text_dim":    "#6a7280",
    "accent":      "#5b3dd6",
    "accent_dim":  "#7c5cff",
    "danger":      "#e53e6b",
}

# ============================================================
# FONT
# ============================================================
# Use system font stack, looks native everywhere
FONT_STACK = (
    '-apple-system, BlinkMacSystemFont, "Inter", '
    '"Segoe UI", Roboto, Helvetica, Arial, sans-serif'
)
MONO_STACK = (
    '"SF Mono", "Menlo", "Cascadia Code", "Roboto Mono", '
    'Consolas, monospace'
)


# ============================================================
# QSS BUILDER
# ============================================================
def build_stylesheet(palette: dict) -> str:
    """
    Generate the Qt stylesheet from a palette dict.

    Qt doesn't support CSS custom properties, so we string-format the
    colors into the QSS at runtime. The structure mirrors a modern
    web app: rounded corners, subtle borders, hover states with smooth
    color transitions (where Qt allows them).
    """
    return f"""
    /* ============================================================
       BASE WINDOW
       ============================================================ */
    QMainWindow {{
        background-color: {palette["bg"]};
    }}

    QWidget {{
        background-color: {palette["bg"]};
        color: {palette["text"]};
        font-family: {FONT_STACK};
        font-size: 13px;
    }}

    /* ============================================================
       TAB BAR. Modern rounded tabs
       ============================================================ */
    QTabWidget::pane {{
        border: none;
        background-color: {palette["bg"]};
        margin-top: 0px;
    }}

    QTabBar {{
        background-color: {palette["surface"]};
        border-bottom: 1px solid {palette["border"]};
        qproperty-drawBase: 0;
    }}

    QTabBar::tab {{
        background-color: transparent;
        color: {palette["text_dim"]};
        padding: 10px 18px;
        margin: 4px 2px 0px 2px;
        border-radius: 8px 8px 0px 0px;
        min-width: 120px;
        max-width: 240px;
        font-weight: 500;
    }}

    QTabBar::tab:selected {{
        background-color: {palette["bg"]};
        color: {palette["text"]};
        border-bottom: 2px solid {palette["accent"]};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {palette["surface_hi"]};
        color: {palette["text"]};
    }}

    QTabBar::close-button {{
        image: none;
        background-color: transparent;
        border-radius: 4px;
        margin: 4px;
        width: 16px;
        height: 16px;
    }}

    QTabBar::close-button:hover {{
        background-color: {palette["danger"]};
    }}

    /* ============================================================
       TOOLBAR. Flat, modern
       ============================================================ */
    QToolBar {{
        background-color: {palette["surface"]};
        border: none;
        border-bottom: 1px solid {palette["border"]};
        padding: 6px 8px;
        spacing: 6px;
    }}

    QToolBar QToolButton {{
        background-color: transparent;
        border: none;
        border-radius: 6px;
        padding: 6px 10px;
        color: {palette["text_dim"]};
        font-size: 14px;
        font-weight: 500;
    }}

    QToolBar QToolButton:hover {{
        background-color: {palette["surface_hi"]};
        color: {palette["text"]};
    }}

    QToolBar QToolButton:pressed {{
        background-color: {palette["accent"]};
        color: white;
    }}

    /* ============================================================
       URL BAR
       ============================================================ */
    QLineEdit {{
        background-color: {palette["surface_hi"]};
        border: 1px solid {palette["border"]};
        border-radius: 8px;
        padding: 8px 14px;
        color: {palette["text"]};
        selection-background-color: {palette["accent"]};
        font-size: 13px;
    }}

    QLineEdit:focus {{
        border: 1px solid {palette["accent"]};
        background-color: {palette["bg"]};
    }}

    QLineEdit::placeholder {{
        color: {palette["text_dim"]};
    }}

    /* ============================================================
       MENUS
       ============================================================ */
    QMenuBar {{
        background-color: {palette["surface"]};
        color: {palette["text"]};
        border-bottom: 1px solid {palette["border"]};
        padding: 4px 8px;
    }}

    QMenuBar::item {{
        background-color: transparent;
        padding: 6px 12px;
        border-radius: 6px;
    }}

    QMenuBar::item:selected {{
        background-color: {palette["surface_hi"]};
    }}

    QMenu {{
        background-color: {palette["surface"]};
        color: {palette["text"]};
        border: 1px solid {palette["border"]};
        border-radius: 8px;
        padding: 6px;
    }}

    QMenu::item {{
        padding: 8px 24px 8px 16px;
        border-radius: 6px;
        margin: 2px;
    }}

    QMenu::item:selected {{
        background-color: {palette["accent"]};
        color: white;
    }}

    QMenu::separator {{
        height: 1px;
        background-color: {palette["border"]};
        margin: 4px 8px;
    }}

    /* ============================================================
       STATUS BAR
       ============================================================ */
    QStatusBar {{
        background-color: {palette["surface"]};
        color: {palette["text_dim"]};
        border-top: 1px solid {palette["border"]};
        padding: 4px 12px;
        font-size: 12px;
    }}

    /* ============================================================
       SCROLLBARS
       ============================================================ */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 10px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background-color: {palette["border"]};
        border-radius: 5px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {palette["text_dim"]};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: transparent;
    }}
    """
