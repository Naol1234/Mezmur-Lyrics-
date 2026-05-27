# 🎵 መዝሙር Search — WikiMezmur Lyrics App

A clean, bilingual (Amharic + English) lyrics search app powered **live** from [WikiMezmur.org](https://wikimezmur.org) via its MediaWiki API. Any new song added to the wiki appears in the app automatically — no rebuilds needed.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🔍 Search | Full-text search in Amharic or English |
| 🎤 Filter by | All / Song Title / Singer |
| 📖 Lyrics view | Full lyrics stripped of wiki markup |
| ⏱ Live data | Cached 5 min; always fresh from WikiMezmur |
| 📱 Mobile-friendly | Responsive layout, large Ethiopic font |
| 🎨 Designed for | Ethiopian gospel / worship context |

---

## 🚀 Deploy to Streamlit Community Cloud (Free)

### 1. Push to GitHub

```bash
# Create a new repo on GitHub, then:
git init
git add .
git commit -m "Initial commit — Mezmur Search App"
git remote add origin https://github.com/YOUR_USERNAME/mezmur-search.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **"New app"**
3. Select your repo → branch `main` → file `app.py`
4. Click **Deploy** — done! You'll get a public URL like:
   `https://your-app-name.streamlit.app`

> No API keys needed. The WikiMezmur API is public.

---

## 🖥 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

---

## 🗂 Project Structure

```
mezmur-app/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── config.toml      # Theme + server config
└── README.md
```

---

## 🔌 How the Live Data Works

The app calls the **MediaWiki API** at `https://wikimezmur.org/api.php`:

| Action | API call |
|---|---|
| Search songs | `?action=query&list=search&srsearch=...` |
| Get lyrics | `?action=query&prop=revisions&titles=...` |
| Recent updates | `?action=query&list=recentchanges` |

Results are cached for **5 minutes** with `@st.cache_data(ttl=300)`. The "Recently Added" feed on the home screen shows pages edited on the wiki in real time.

---

## 🎨 Design

- **Palette**: Ethiopian parchment gold + forest sage green
- **Fonts**: Noto Sans Ethiopic (Amharic) + Cormorant Garamond (English)
- **Aesthetic**: Sacred manuscript meets modern card UI

---

## 📄 Content License

All lyrics content is from WikiMezmur.org and is available under [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
