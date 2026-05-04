// ============================================================
// Ricker dashboard homepage
// Handles: clock, time-aware greeting, search engine picker,
// search submission routing through the selected engine.
// ============================================================

// The full engine list, kept in sync with app/engines.py
const ENGINES = [
    { name: "Google",     url: "https://www.google.com/search?q=", color: "#4285F4" },
    { name: "DuckDuckGo", url: "https://duckduckgo.com/?q=",        color: "#DE5833" },
    { name: "Bing",       url: "https://www.bing.com/search?q=",    color: "#008373" },
    { name: "Yahoo",      url: "https://search.yahoo.com/search?p=", color: "#5F01D1" },
    { name: "Brave",      url: "https://search.brave.com/search?q=", color: "#FB542B" },
    { name: "Startpage",  url: "https://www.startpage.com/do/search?query=", color: "#5C5DD8" },
    { name: "Yandex",     url: "https://yandex.com/search/?text=",   color: "#FF0000" },
    { name: "Ecosia",     url: "https://www.ecosia.org/search?q=",   color: "#36A974" },
    { name: "Qwant",      url: "https://www.qwant.com/?q=",          color: "#5C97FF" },
    { name: "Kagi",       url: "https://kagi.com/search?q=",         color: "#FFB319" },
];

let activeEngine = "Google";

// ============================================================
// CLOCK + GREETING
// ============================================================
function updateClock() {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, "0");
    const mm = String(now.getMinutes()).padStart(2, "0");
    document.getElementById("clock").textContent = `${hh}:${mm}`;
}

function updateGreeting() {
    const hour = new Date().getHours();
    let g;
    if (hour < 5)       g = "Working late.";
    else if (hour < 12) g = "Good morning.";
    else if (hour < 17) g = "Good afternoon.";
    else if (hour < 21) g = "Good evening.";
    else                g = "Up late again.";
    document.getElementById("greeting").textContent = g;
}

// ============================================================
// ENGINE PICKER
// ============================================================
function renderEnginePicker() {
    const list = document.getElementById("engine-list");
    list.innerHTML = "";

    // Saved preference, falls back to Google
    const saved = sessionStorage.getItem("ricker.engine");
    if (saved) activeEngine = saved;

    ENGINES.forEach(engine => {
        const chip = document.createElement("button");
        chip.className = "engine-chip" + (engine.name === activeEngine ? " active" : "");
        chip.innerHTML = `
            <span class="engine-dot" style="background: ${engine.color};"></span>
            <span>${engine.name}</span>
        `;
        chip.addEventListener("click", () => {
            activeEngine = engine.name;
            sessionStorage.setItem("ricker.engine", engine.name);
            renderEnginePicker();
            document.getElementById("search-input").focus();
        });
        list.appendChild(chip);
    });
}

// ============================================================
// SEARCH SUBMISSION
// ============================================================
function handleSearch(e) {
    if (e.key !== "Enter") return;

    const query = e.target.value.trim();
    if (!query) return;

    const engine = ENGINES.find(en => en.name === activeEngine) || ENGINES[0];

    // If it looks like a URL, go directly
    if (/^https?:\/\//.test(query) || /^[a-z0-9-]+\.[a-z]{2,}/i.test(query)) {
        const url = /^https?:\/\//.test(query) ? query : `https://${query}`;
        window.location.href = url;
        return;
    }

    // Otherwise, run a search on the active engine
    window.location.href = engine.url + encodeURIComponent(query);
}

// ============================================================
// INIT
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
    updateClock();
    updateGreeting();
    setInterval(updateClock, 30000);
    renderEnginePicker();

    document.getElementById("search-input")
        .addEventListener("keydown", handleSearch);
});
