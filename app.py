"""
መዝሙር Search App
"""

import streamlit as st
import requests
import urllib.parse
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="መዝሙር Search",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;600;700;900&family=Playfair+Display:ital,wght@0,700;0,900;1,400&display=swap');

:root {
    --purple:     #4a0e8f;
    --purple-mid: #6b21c8;
    --purple-lt:  #9b59e8;
    --gold:       #d4a017;
    --gold-lt:    #f5c842;
    --gold-pale:  #fef3c7;
    --bg:         #0e0618;
    --bg2:        #180d2e;
    --bg3:        #221040;
    --card:       #1e0f38;
    --card-hov:   #2a1650;
    --text:       #f0e6ff;
    --muted:      #9b8ab8;
    --white:      #ffffff;
    --shadow:     0 8px 32px rgba(74,14,143,0.35);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Noto Sans Ethiopic', sans-serif;
}
[data-testid="stAppViewContainer"] > div { background: transparent !important; }
[data-testid="block-container"] { padding-top: 1rem !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--purple-mid); border-radius: 3px; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #2d0a5a 0%, #1a0535 50%, #0e0618 100%);
    border: 1px solid rgba(212,160,23,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(74,14,143,0.5);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(107,33,200,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(212,160,23,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--gold-lt);
    font-family: 'Noto Sans Ethiopic', sans-serif;
    line-height: 1.1;
    margin: 0;
    text-shadow: 0 2px 20px rgba(245,200,66,0.4);
}
.hero-sub {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: var(--purple-lt);
    margin: 0.4rem 0 0.6rem;
}
.hero-desc {
    font-size: 0.88rem;
    color: var(--muted);
    font-family: 'Noto Sans Ethiopic', sans-serif;
}

/* ── Search input ── */
.stTextInput > div > div > input {
    background: var(--bg3) !important;
    border: 2px solid var(--purple-mid) !important;
    border-radius: 14px !important;
    font-size: 1.1rem !important;
    font-family: 'Noto Sans Ethiopic', sans-serif !important;
    padding: 0.7rem 1.2rem !important;
    color: var(--text) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(212,160,23,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Radio filter ── */
[data-testid="stRadio"] > div {
    flex-direction: row;
    gap: 0.6rem;
    flex-wrap: wrap;
}
[data-testid="stRadio"] > div > label {
    background: var(--bg3);
    border: 1.5px solid var(--purple-mid);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.88rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.18s ease;
    font-family: 'Noto Sans Ethiopic', sans-serif;
}
[data-testid="stRadio"] > div > label:has(input:checked) {
    background: linear-gradient(135deg, var(--purple-mid), var(--purple)) !important;
    color: var(--gold-lt) !important;
    border-color: var(--gold) !important;
    font-weight: 700;
    box-shadow: 0 2px 12px rgba(107,33,200,0.4);
}

/* ── Section pill ── */
.section-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, var(--purple), var(--purple-mid));
    color: var(--gold-lt);
    border-radius: 50px;
    padding: 0.3rem 1rem;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 1rem;
    border: 1px solid rgba(212,160,23,0.3);
}

/* ── Magazine grid cards ── */
.grid-wrap {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}
@media (max-width: 640px) {
    .grid-wrap { grid-template-columns: 1fr; }
    .hero-title { font-size: 1.9rem; }
}
.mag-card {
    background: var(--card);
    border: 1px solid rgba(107,33,200,0.3);
    border-radius: 16px;
    padding: 1.3rem 1.4rem 1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    cursor: pointer;
}
.mag-card::before {
    content: '🎵';
    position: absolute;
    top: -8px; right: 10px;
    font-size: 4rem;
    opacity: 0.06;
    pointer-events: none;
}
.mag-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow);
    border-color: var(--gold);
}
.mag-card-accent {
    height: 3px;
    background: linear-gradient(90deg, var(--purple-mid), var(--gold));
    border-radius: 2px;
    margin-bottom: 0.8rem;
}
.mag-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    font-family: 'Noto Sans Ethiopic', sans-serif;
    line-height: 1.35;
    margin-bottom: 0.35rem;
}
.mag-card-snippet {
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.5;
    font-family: 'Noto Sans Ethiopic', sans-serif;
}
.mag-card-date {
    font-size: 0.72rem;
    color: var(--purple-lt);
    margin-top: 0.5rem;
    font-style: italic;
}

/* ── View lyrics button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--purple-mid), var(--purple)) !important;
    color: var(--gold-lt) !important;
    border: 1px solid rgba(212,160,23,0.3) !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans Ethiopic', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.1rem !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--purple), var(--purple-mid)) !important;
    box-shadow: 0 4px 20px rgba(107,33,200,0.5) !important;
    border-color: var(--gold) !important;
}

/* ── Lyrics page ── */
.lyrics-header {
    background: linear-gradient(135deg, #2d0a5a, #1a0535);
    border: 1px solid rgba(212,160,23,0.25);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}
.lyrics-title {
    font-size: 2rem;
    font-weight: 900;
    color: var(--gold-lt);
    font-family: 'Noto Sans Ethiopic', sans-serif;
    margin-bottom: 0.3rem;
    text-shadow: 0 2px 16px rgba(245,200,66,0.3);
}
.lyrics-body {
    background: var(--card);
    border: 1px solid rgba(107,33,200,0.25);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    font-family: 'Noto Sans Ethiopic', sans-serif;
    font-size: 1.12rem;
    line-height: 2;
    color: var(--text);
    white-space: pre-wrap;
}
.lyrics-line-accent {
    display: inline-block;
    width: 40px;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--purple-lt));
    border-radius: 2px;
    margin-bottom: 1rem;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(107,33,200,0.25);
    margin: 1.2rem 0;
}

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--muted);
}
.no-results-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.no-results-text { font-size: 1.05rem; font-family: 'Noto Sans Ethiopic', sans-serif; }

/* ── Footer ── */
.app-footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(107,33,200,0.2);
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ── API helpers ───────────────────────────────────────────────────────────────
BASE_URL = "https://wikimezmur.org/api.php"

@st.cache_data(ttl=300, show_spinner=False)
def search_wiki(query: str, search_type: str = "all") -> list:
    if not query.strip():
        return []
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "0",
        "srlimit": "40",
        "srprop": "snippet|titlesnippet",
        "format": "json",
        "origin": "*",
        "srwhat": "title" if search_type == "title" else "text",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        results = r.json().get("query", {}).get("search", [])
        return [x for x in results if is_real_lyrics_page(x.get("title", ""))]
    except Exception as e:
        st.error(f"Search error: {e}")
        return []


@st.cache_data(ttl=600, show_spinner=False)
def get_category_pages(category: str = "Lyrics", limit: int = 50) -> list:
    """Fetch pages from a specific category — filters out spam."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": str(limit),
        "cmtype": "page",
        "cmprop": "title|timestamp",
        "format": "json",
        "origin": "*",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("query", {}).get("categorymembers", [])
    except Exception:
        return []


@st.cache_data(ttl=600, show_spinner=False)
def get_page_content(title: str) -> dict:
    params = {
        "action": "query",
        "titles": title,
        "prop": "revisions|info",
        "rvprop": "content",
        "rvslots": "main",
        "inprop": "url",
        "format": "json",
        "origin": "*",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        page = next(iter(pages.values()))
        wikitext = (
            page.get("revisions", [{}])[0]
            .get("slots", {}).get("main", {}).get("*", "")
        )
        url = page.get("fullurl", "")
        return {"title": title, "wikitext": wikitext, "url": url}
    except Exception as e:
        return {"title": title, "wikitext": "", "url": "", "error": str(e)}


def is_real_lyrics_page(title: str) -> bool:
    """Return False for obvious spam/non-lyrics pages."""
    spam_signals = [
        "html", ".com", ".net", ".org", "http", "consultant",
        "software", "students", "education", "insurance", "loan",
        "casino", "poker", "viagra", "pharmacy", "essay", "writing",
        "marketing", "seo", "backlink", "wordpress",
    ]
    t = title.lower()
    if any(s in t for s in spam_signals):
        return False
    if len(title) > 120:
        return False
    return True


def clean_wikitext(text: str) -> str:
    text = re.sub(r'\{\{[^{}]*\}\}', '', text)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', text)
    text = re.sub(r'\[https?://\S+\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[https?://\S+\]', '', text)
    text = re.sub(r'={2,}([^=]+)={2,}', r'\n\1\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r"'{2,}", '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def clean_snippet(html: str) -> str:
    return re.sub(r'<[^>]+>', '', html)


# ── Session state ─────────────────────────────────────────────────────────────
if "view_page" not in st.session_state:
    st.session_state.view_page = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_type" not in st.session_state:
    st.session_state.search_type = "all"


# ── Lyrics view ───────────────────────────────────────────────────────────────
if st.session_state.view_page:
    if st.button("← ተመለስ / Back"):
        st.session_state.view_page = None
        st.rerun()

    with st.spinner("ግጥሙን በመጫን ላይ…"):
        page_data = get_page_content(st.session_state.view_page)

    lyrics = clean_wikitext(page_data.get("wikitext", ""))

    st.markdown(f"""
    <div class="lyrics-header">
        <div class="lyrics-title">{st.session_state.view_page}</div>
        <div class="lyrics-line-accent"></div>
    </div>
    """, unsafe_allow_html=True)

    if lyrics:
        st.markdown(f'<div class="lyrics-body">{lyrics}</div>', unsafe_allow_html=True)
    else:
        st.warning("ግጥሙ ሊጫን አልቻለም። / Lyrics could not be loaded.")

    st.markdown('<div class="app-footer">Lyrics data licensed under CC BY 4.0</div>', unsafe_allow_html=True)
    st.stop()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🎵 መዝሙር Search</div>
    <div class="hero-sub">Amharic Gospel Lyrics</div>
    <div class="hero-desc">ፈልጉ — Search in Amharic or English</div>
</div>
""", unsafe_allow_html=True)


# ── Search bar ────────────────────────────────────────────────────────────────
col_s, col_t = st.columns([3, 1])
with col_s:
    query = st.text_input(
        "",
        value=st.session_state.search_query,
        placeholder="🔍  ፈልግ — Search songs or singers…",
        label_visibility="collapsed",
        key="query_input",
    )
with col_t:
    search_type = st.radio(
        "",
        ["ሁሉም / All", "ርዕስ / Title", "ዘማሪ / Singer"],
        index=["all", "title", "singer"].index(st.session_state.search_type),
        label_visibility="collapsed",
    )

type_map = {"ሁሉም / All": "all", "ርዕስ / Title": "title", "ዘማሪ / Singer": "singer"}
st.session_state.search_type = type_map[search_type]
st.session_state.search_query = query
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── Render grid of cards ──────────────────────────────────────────────────────
def render_grid(items: list, key_prefix: str):
    """Render items as a 2-column magazine grid."""
    # Split into pairs for 2-col layout
    for i in range(0, len(items), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(items):
                break
            item = items[idx]
            title = item.get("title", "")
            snippet = clean_snippet(item.get("snippet", "") or item.get("titlesnippet", ""))
            date = item.get("timestamp", "")[:10] if "timestamp" in item else ""

            with col:
                st.markdown(f"""
                <div class="mag-card">
                    <div class="mag-card-accent"></div>
                    <div class="mag-card-title">{title}</div>
                    <div class="mag-card-snippet">{snippet[:120]}{"…" if len(snippet) > 120 else ""}</div>
                    {"<div class='mag-card-date'>" + date + "</div>" if date else ""}
                </div>
                """, unsafe_allow_html=True)
                if st.button("📖 ግጥሙን ይመልከቱ", key=f"{key_prefix}_{title}_{idx}"):
                    st.session_state.view_page = title
                    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
if query.strip():
    with st.spinner("እየፈለጉ ነው…"):
        results = search_wiki(query, st.session_state.search_type)

    if results:
        st.markdown(f'<div class="section-pill">✦ {len(results)} ውጤቶች / Results</div>', unsafe_allow_html=True)
        render_grid(results, "search")
    else:
        st.markdown("""
        <div class="no-results">
            <div class="no-results-icon">🔍</div>
            <div class="no-results-text">ምንም ውጤት አልተገኘም / No results found</div>
            <div style="font-size:0.82rem;margin-top:0.3rem;color:#6b5a8a;">Try different keywords or search in Amharic</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Discover: pull from Lyrics category (no spam) ────────────────────────
    st.markdown('<div class="section-pill">✦ ቅርብ ጊዜ የተጨመሩ / Recently Added Lyrics</div>', unsafe_allow_html=True)

    with st.spinner("ዘፈኖችን በመጫን ላይ…"):
        pages = get_category_pages("Lyrics", limit=60)

    if not pages:
        # fallback: try recent changes filtered by our spam check
        with st.spinner("በሌላ መንገድ እየሞከርን…"):
            params = {
                "action": "query",
                "list": "recentchanges",
                "rcnamespace": "0",
                "rclimit": "50",
                "rcprop": "title|timestamp",
                "rctype": "edit|new",
                "format": "json",
                "origin": "*",
            }
            try:
                r = requests.get(BASE_URL, params=params, timeout=10)
                raw = r.json().get("query", {}).get("recentchanges", [])
                pages = [x for x in raw if is_real_lyrics_page(x.get("title", ""))]
            except Exception:
                pages = []

    if pages:
        # Deduplicate
        seen = set()
        unique = []
        for p in pages:
            t = p.get("title", "")
            if t not in seen:
                seen.add(t)
                unique.append(p)
        render_grid(unique[:40], "discover")
    else:
        st.info("ዘፈኖችን ማምጣት አልተቻለም። / Could not load songs. Please try searching above.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Lyrics data licensed under CC BY 4.0 · Built with Streamlit
</div>
""", unsafe_allow_html=True)
