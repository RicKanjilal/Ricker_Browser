"""
Search engine registry.

Centralizes the list so adding a new engine means changing one place,
not three. Each engine has a homepage URL and a query template that
takes a search term.
"""

SEARCH_ENGINES = [
    {
        "name": "Google",
        "home": "https://www.google.com",
        "search": "https://www.google.com/search?q={q}",
        "color": "#4285F4",
        "short": "G",
    },
    {
        "name": "DuckDuckGo",
        "home": "https://duckduckgo.com",
        "search": "https://duckduckgo.com/?q={q}",
        "color": "#DE5833",
        "short": "D",
    },
    {
        "name": "Bing",
        "home": "https://www.bing.com",
        "search": "https://www.bing.com/search?q={q}",
        "color": "#008373",
        "short": "B",
    },
    {
        "name": "Yahoo",
        "home": "https://www.yahoo.com",
        "search": "https://search.yahoo.com/search?p={q}",
        "color": "#5F01D1",
        "short": "Y",
    },
    {
        "name": "Brave",
        "home": "https://search.brave.com",
        "search": "https://search.brave.com/search?q={q}",
        "color": "#FB542B",
        "short": "B",
    },
    {
        "name": "Startpage",
        "home": "https://www.startpage.com",
        "search": "https://www.startpage.com/do/search?query={q}",
        "color": "#5C5DD8",
        "short": "S",
    },
    {
        "name": "Yandex",
        "home": "https://yandex.com",
        "search": "https://yandex.com/search/?text={q}",
        "color": "#FF0000",
        "short": "Y",
    },
    {
        "name": "Ecosia",
        "home": "https://www.ecosia.org",
        "search": "https://www.ecosia.org/search?q={q}",
        "color": "#36A974",
        "short": "E",
    },
    {
        "name": "Qwant",
        "home": "https://www.qwant.com",
        "search": "https://www.qwant.com/?q={q}",
        "color": "#5C97FF",
        "short": "Q",
    },
    {
        "name": "Kagi",
        "home": "https://kagi.com",
        "search": "https://kagi.com/search?q={q}",
        "color": "#FFB319",
        "short": "K",
    },
]


def by_name(name: str) -> dict:
    """Look up an engine by name. Returns Google as fallback."""
    for engine in SEARCH_ENGINES:
        if engine["name"] == name:
            return engine
    return SEARCH_ENGINES[0]
