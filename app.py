"""
 መዝሙር Search — WikiMezmur Lyrics App
Powered by the WikiMezmur MediaWiki API (wikimezmur.org/api.php)
"""

import streamlit as st
import requests
import urllib.parse
import re
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=" መዝሙር Search",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

/* ── Root variables ── */
:root {
    --gold:    #c9982a;
    --gold-lt: #f0c96a;
    --ink:     #0d0d0d;
    --parchment: #fdf6e3;
    --sage:    #1a3a2a;
    --sage-lt: #2a5a3a;
    --cream:   #f5efe0;
    --muted:   #7a6a50;
    --card-bg: #fffdf5;
    --shadow:  0 4px 24px rgba(0,0,0,0.10);
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--parchment) !important;
    color: var(--ink);
    font-family: 'Cormorant Garamond', 'Noto Sans Ethiopic', serif;
}

/* Hide default Streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, var(--sage) 0%, #0a2018 60%, #142e1e 100%);
    border-radius: 18px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.25);
}
.hero::before {
    content: "𝄞";
    position: absolute;
    right: 3rem; top: 1rem;
    font-size: 11rem;
    color: rgba(201,152,42,0.10);
    line-height: 1;
    pointer-events: none;
}
.hero-amharic {
    font-family: 'Noto Sans Ethiopic', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--gold-lt);
    line-height: 1.2;
    margin: 0;
}
.hero-english {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.25rem;
    color: rgba(240,201,106,0.70);
    margin: 0.3rem 0 0.8rem;
}
.hero-tagline {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.55);
    font-family: 'Noto Sans Ethiopic', sans-serif;
    letter-spacing: 0.02em;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    background: var(--card-bg) !important;
    border: 2px solid var(--gold) !important;
    border-radius: 12px !important;
    font-size: 1.2rem !important;
    font-family: 'Noto Sans Ethiopic', 'Cormorant Garamond', serif !important;
    padding: 0.75rem 1.2rem !important;
    color: var(--ink) !important;
    box-shadow: 0 2px 12px rgba(201,152,42,0.15) !important;
    transition: box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    box-shadow: 0 4px 20px rgba(201,152,42,0.35) !important;
    outline: none !important;
}

/* ── Radio buttons (filter tabs) ── */
[data-testid="stRadio"] > div {
    flex-direction: row;
    gap: 0.75rem;
    flex-wrap: wrap;
}
[data-testid="stRadio"] > div > label {
    background: var(--card-bg);
    border: 1.5px solid var(--gold);
    border-radius: 50px;
    padding: 0.35rem 1.1rem;
    font-size: 0.95rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.18s ease;
    font-family: 'Noto Sans Ethiopic', sans-serif;
}
[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--gold) !important;
    color: var(--ink) !important;
    font-weight: 600;
    box-shadow: 0 2px 10px rgba(201,152,42,0.3);
}

/* ── Result cards ── */
.result-card {
    background: var(--card-bg);
    border: 1px solid rgba(201,152,42,0.25);
    border-left: 4px solid var(--gold);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}
.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(201,152,42,0.18);
    border-color: var(--gold);
}
.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--sage);
    font-family: 'Noto Sans Ethiopic', 'Cormorant Garamond', serif;
    margin-bottom: 0.2rem;
}
.card-snippet {
    font-size: 0.9rem;
    color: var(--muted);
    line-height: 1.55;
    font-family: 'Noto Sans Ethiopic', sans-serif;
}
.card-link {
    font-size: 0.78rem;
    color: var(--gold);
    margin-top: 0.4rem;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
}

/* ── Lyrics display ── */
.lyrics-container {
    background: var(--card-bg);
    border: 1px solid rgba(201,152,42,0.3);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    box-shadow: var(--shadow);
    font-family: 'Noto Sans Ethiopic', 'Cormorant Garamond', serif;
    font-size: 1.08rem;
    line-height: 1.9;
    white-space: pre-wrap;
    color: var(--ink);
}
.lyrics-title {
    font-family: 'Cormorant Garamond', 'Noto Sans Ethiopic', serif;
    font-size: 1.9rem;
    font-weight: 600;
    color: var(--sage);
    border-bottom: 2px solid var(--gold);
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
}
.lyrics-meta {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
    font-style: italic;
    font-family: 'Cormorant Garamond', serif;
}

/* ── Status / info pills ── */
.info-pill {
    display: inline-block;
    background: var(--sage);
    color: var(--gold-lt);
    border-radius: 50px;
    padding: 0.25rem 0.9rem;
    font-size: 0.82rem;
    font-family: 'Noto Sans Ethiopic', sans-serif;
    margin-bottom: 0.5rem;
}

/* ── Divider ── */
.gold-divider {
    border: none;
    border-top: 1.5px solid rgba(201,152,42,0.35);
    margin: 1.5rem 0;
}

/* ── Back button ── */
.stButton > button {
    background: var(--sage) !important;
    color: var(--gold-lt) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Noto Sans Ethiopic', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 1.3rem !important;
    transition: background 0.18s ease !important;
}
.stButton > button:hover {
    background: var(--sage-lt) !important;
    box-shadow: 0 4px 16px rgba(26,58,42,0.3) !important;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(201,152,42,0.2);
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
}

/* ── Responsive ── */
@media (max-width: 640px) {
    .hero { padding: 2rem 1.3rem 1.8rem; }
    .hero-amharic { font-size: 1.85rem; }
    .lyrics-container { padding: 1.2rem 1.2rem; font-size: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── WikiMezmur API ────────────────────────────────────────────────────────────
BASE_URL = "https://wikimezmur.org/api.php"
WIKI_BASE = "https://wikimezmur.org/am"

@st.cache_data(ttl=300, show_spinner=False)
def search_wiki(query: str, search_type: str = "all") -> list[dict]:
    """Full-text search via MediaWiki API. Returns list of result dicts."""
    if not query.strip():
        return []

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": "0",
        "srlimit": "30",
        "srprop": "snippet|titlesnippet|sectiontitle",
        "format": "json",
        "origin": "*",
    }

    # Narrow search by prefixing with singer name hint (best-effort)
    if search_type == "singer":
        params["srsearch"] = f"{query}"
        params["srwhat"] = "text"
    elif search_type == "title":
        params["srwhat"] = "title"
    else:
        params["srwhat"] = "text"

    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("query", {}).get("search", [])
    except Exception as e:
        st.error(f"API error: {e}")
        return []


@st.cache_data(ttl=600, show_spinner=False)
def get_page_content(title: str) -> dict:
    """Fetch wikitext + parsed HTML for a page."""
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
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))
        wikitext = (
            page.get("revisions", [{}])[0]
            .get("slots", {})
            .get("main", {})
            .get("*", "")
        )
        url = page.get("fullurl", f"{WIKI_BASE}/{urllib.parse.quote(title)}")
        return {"title": title, "wikitext": wikitext, "url": url}
    except Exception as e:
        return {"title": title, "wikitext": "", "url": "", "error": str(e)}


def clean_wikitext(text: str) -> str:
    """Strip wiki markup, leaving clean lyrics text."""
    # Remove templates {{...}}
    text = re.sub(r'\{\{[^{}]*\}\}', '', text)
    # Remove [[links]] but keep display text
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', text)
    # Remove external links [url text]
    text = re.sub(r'\[https?://\S+\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[https?://\S+\]', '', text)
    # Remove headers (=...=)
    text = re.sub(r'={2,}([^=]+)={2,}', r'\n\1\n', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove bold/italic wiki markup
    text = re.sub(r"'{2,}", '', text)
    # Collapse excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def clean_snippet(html: str) -> str:
    """Strip HTML from API snippet."""
    return re.sub(r'<[^>]+>', '', html)


@st.cache_data(ttl=600, show_spinner=False)
def get_recent_pages(limit: int = 20) -> list[dict]:
    """Fetch recently edited pages for the landing discover feed."""
    params = {
        "action": "query",
        "list": "recentchanges",
        "rcnamespace": "0",
        "rclimit": str(limit),
        "rcprop": "title|timestamp|comment",
        "rctype": "edit|new",
        "format": "json",
        "origin": "*",
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("query", {}).get("recentchanges", [])
    except Exception:
        return []


# ── Session state ─────────────────────────────────────────────────────────────
if "view_page" not in st.session_state:
    st.session_state.view_page = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_type" not in st.session_state:
    st.session_state.search_type = "all"


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-amharic">🎵  መዝሙር ፈልጉ</p>
    <p class="hero-english">Mezmur Lyrics Search</p>
    <p class="hero-tagline">ከ WikiMezmur — Free Amharic Gospel Song Database</p>
</div>
""", unsafe_allow_html=True)


# ── Lyrics view ───────────────────────────────────────────────────────────────
if st.session_state.view_page:
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("← ተመለስ / Back"):
            st.session_state.view_page = None
            st.rerun()

    with st.spinner("በመጫን ላይ… Loading lyrics…"):
        page_data = get_page_content(st.session_state.view_page)

    lyrics_clean = clean_wikitext(page_data.get("wikitext", ""))
    wiki_url = page_data.get("url", "")

    st.markdown(f'<div class="lyrics-title">{st.session_state.view_page}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="lyrics-meta">📖 <a href="{wiki_url}" target="_blank" style="color:var(--muted);font-size:0.78rem;text-decoration:none;">Content license: CC BY 4.0</a></div>',
        unsafe_allow_html=True
    )

    if lyrics_clean:
        st.markdown(f'<div class="lyrics-container">{lyrics_clean}</div>', unsafe_allow_html=True)
    else:
        st.info("ይህ ገጽ ምናልባት ሊጫን አልቻለም። / Could not load lyrics for this page.")
        st.markdown(f"[View original source ↗]({wiki_url})")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-footer">Lyrics data licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" style="color:var(--muted);">CC BY 4.0</a></div>',
        unsafe_allow_html=True
    )
    st.stop()


# ── Search UI ─────────────────────────────────────────────────────────────────
col_search, col_type = st.columns([3, 1])

with col_search:
    query = st.text_input(
        "",
        value=st.session_state.search_query,
        placeholder="🔍  Search in Amharic (አማርኛ) or English…",
        label_visibility="collapsed",
        key="query_input",
    )

with col_type:
    search_type = st.radio(
        "ፈልግ / Search by",
        ["ሁሉም / All", "ርዕስ / Title", "ዘፋኝ / Singer"],
        index=["all", "title", "singer"].index(st.session_state.search_type),
        label_visibility="collapsed",
    )

type_map = {"ሁሉም / All": "all", "ርዕስ / Title": "title", "ዘፋኝ / Singer": "singer"}
st.session_state.search_type = type_map[search_type]

if query != st.session_state.search_query:
    st.session_state.search_query = query

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


# ── Results / Discover ────────────────────────────────────────────────────────
if query.strip():
    with st.spinner("እየፈለጉ ነው… Searching WikiMezmur…"):
        results = search_wiki(query, st.session_state.search_type)

    if results:
        st.markdown(f'<span class="info-pill">✦ {len(results)} ውጤቶች / Results found</span>', unsafe_allow_html=True)
        for item in results:
            title = item.get("title", "")
            snippet_raw = item.get("snippet", "") or item.get("titlesnippet", "")
            snippet = clean_snippet(snippet_raw)
            page_url = f"{WIKI_BASE}/{urllib.parse.quote(title.replace(' ', '_'))}"

            card_html = f"""
            <div class="result-card">
                <div class="card-title">{title}</div>
                <div class="card-snippet">{snippet[:180]}{"…" if len(snippet) > 180 else ""}</div>
                <div class="card-link">wikimezmur.org ↗</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(f"📖 ግጥሙን ይመልከቱ / View Lyrics", key=f"btn_{title}"):
                    st.session_state.view_page = title
                    st.rerun()
            with col2:
                st.markdown(f'<a href="{page_url}" target="_blank" style="color:var(--gold);font-size:0.85rem;">↗ WikiMezmur</a>', unsafe_allow_html=True)
            st.markdown('<div style="height:0.3rem"></div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:var(--muted);">
            <div style="font-size:2.5rem;">🔍</div>
            <div style="font-size:1.1rem;margin-top:0.5rem;font-family:'Noto Sans Ethiopic',sans-serif;">
                ምንም ውጤት አልተገኘም / No results found
            </div>
            <div style="font-size:0.85rem;margin-top:0.3rem;">
                Try searching in Amharic or check the spelling
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # Discover feed — recently updated pages
    st.markdown('<span class="info-pill">✦ ቅርብ ጊዜ የተጨመሩ / Recently Added & Updated</span>', unsafe_allow_html=True)
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    with st.spinner("WikiMezmur በመጫን…"):
        recent = get_recent_pages(24)

    if recent:
        # Deduplicate by title
        seen = set()
        unique_recent = []
        for item in recent:
            t = item.get("title", "")
            if t not in seen:
                seen.add(t)
                unique_recent.append(item)

        cols = st.columns(2)
        for i, item in enumerate(unique_recent[:20]):
            title = item.get("title", "")
            ts = item.get("timestamp", "")[:10]
            page_url = f"{WIKI_BASE}/{urllib.parse.quote(title.replace(' ', '_'))}"

            with cols[i % 2]:
                card_html = f"""
                <div class="result-card" style="cursor:default;">
                    <div class="card-title">{title}</div>
                    <div class="card-snippet" style="font-size:0.78rem;">Updated: {ts}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📖 ግጥሙን ይመልከቱ", key=f"recent_{title}_{i}"):
                        st.session_state.view_page = title
                        st.rerun()
                with col_b:
                    st.markdown(f'<a href="{page_url}" target="_blank" style="color:var(--gold);font-size:0.82rem;">↗ Wiki</a>', unsafe_allow_html=True)
    else:
        st.info("Could not load recent pages. The data source may be temporarily unavailable.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Lyrics data licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" style="color:var(--muted);">CC BY 4.0</a>
    · Built with Streamlit · Refreshes every 5 minutes
</div>
""", unsafe_allow_html=True)
