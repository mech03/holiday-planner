# 🌴 Holiday Planner — Adventurous Tropical Destination Recommender

> Find an adventurous tropical getaway near the nightlife. Holiday Planner blends live
> **weather**, **nightlife/amenity** and **cost** signals into a transparent, tunable
> *Adventure Score*, and presents the options on an interactive **map + heatmap**.

**Team:** Sam Willock · Amechi Obisesan · Fenner Backhouse
**Module:** Data Scientist Specialisation — Web Scraping & APIs capstone

---

## ✨ Features

- **Multiple destinations compared** on one transparent 0–100 score.
- **Google Places API** — nearby night clubs, bars and restaurants.
- **Google Geocoding API** — resolve user-entered destinations to coordinates.
- **Open-Meteo weather API** (keyless) — temperature, humidity, cloud, wind.
- **Web-scraping element** — indicative nightly accommodation prices (`requests` + `BeautifulSoup`).
- **SQLite caching** — billable API calls cached with a TTL (cost control + "database integration").
- **LLM-assisted recommendation** — natural-language "why this destination" blurb.
- **Interactive Streamlit app** — preference sliders, ranked table, bar chart, folium map + heatmap, CSV download.
- **Fully reproducible** — offline fallbacks mean it runs with zero keys; add keys for live data.

## 🏗️ Architecture

```
holiday-planner/
├── app.py                  # Streamlit app (the live demo)
├── src/                    # Modular, documented package
│   ├── config.py           # env-based settings & weights
│   ├── destinations.py     # candidate catalogue loader
│   ├── weather.py          # Open-Meteo client (+ fallback)
│   ├── places.py           # Google Places client (+ fallback)
│   ├── geocoding.py        # Google Geocoding client (+ fallback)
│   ├── scraping.py         # web-scraping price element (+ fallback)
│   ├── database.py         # SQLite cache layer + @cached decorator
│   ├── scoring.py          # transparent weighted Adventure Score
│   ├── llm.py              # LLM recommendation blurb (+ fallback)
│   └── pipeline.py         # one orchestrator used by app AND notebook
├── notebooks/
│   └── Holiday_Planner_Analysis.ipynb   # EDA, scoring, findings
├── data/destinations.csv   # editable seed catalogue
├── tests/test_scoring.py   # unit tests (pytest)
├── docs/                   # SoW, team structure, Trello board, plan, conclusions
├── presentation/           # 5-slide deck
├── requirements.txt · .env.example · .gitignore · LICENSE
```

The **same `src.pipeline`** powers both the app and the notebook, so analysis and product never drift.

## 🚀 Quick start

```bash
git clone <your-repo-url> holiday-planner && cd holiday-planner
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# optional: enable live data
cp .env.example .env        # then add your keys

streamlit run app.py
```

Open http://localhost:8501. **No keys needed to try it** — it runs on representative
fallback data and switches to live sources automatically when keys are present.

## ☁️ Deploy (live demo)

Push to GitHub and deploy free on **Streamlit Community Cloud**: point it at `app.py`
and add `GOOGLE_PLACES_API_KEY` / `LLM_API_KEY` as **Secrets**.

## 🔑 API keys

| Variable | Used for | Required? |
|----------|----------|-----------|
| `GOOGLE_PLACES_API_KEY` | nightlife/amenity counts | optional (fallback) |
| `GOOGLE_GEOCODING_API_KEY` | resolve custom places | optional (fallback) |
| `LLM_API_KEY` | recommendation blurb | optional (fallback) |

Keys are read from the environment / `.env`; **nothing secret is committed** (see `.gitignore`).

## 🧪 Tests

```bash
pytest -q
```

## 🧠 How the score works

`Adventure Score = 100 × Σ(weightᵢ × normalised signalᵢ)` over five signals: temperature
comfort, low cloud, calm wind, nightlife density and value. Weights are explicit and
tunable in the sidebar, so every recommendation is **explainable**.

## 📊 Data sources

- Weather: [Open-Meteo](https://open-meteo.com/) (no key)
- Amenities & geocoding: [Google Maps Platform](https://developers.google.com/maps)
- Prices: web-scraping stub (`requests` + `BeautifulSoup`)

## 📄 License

MIT — see [LICENSE](LICENSE).
