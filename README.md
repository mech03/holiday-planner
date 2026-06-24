# 🌴 Holiday Planner — Adventurous Tropical Destination Recommender

> A Streamlit web app that helps you pick a warm, lively holiday near the nightlife.
> It compares destinations on **weather**, **nightlife & amenities** and **cost**, then
> recommends where to go and where to stay — with graphs, an interactive map and a heatmap.

**Team:** Sam Willock · Amechi Obisesan · Fenner Backhouse
**This repository (web app & UI):** Amechi Obisesan
**Module:** Data Scientist Specialisation — Web Scraping & APIs capstone

---

## ✨ What the app does (pages)

| Page | What you get |
|------|--------------|
| **Welcome** (`app.py`) | Overview, today's top pick, and a map of candidate destinations |
| **🌦 Weather** | Filter destinations & dates → temperature, humidity, cloud and wind **graphs** |
| **✈️ Flights & Cost** | Flight price, duration and **trip-cost breakdown** graphs + details table |
| **🏆 Recommendation** | Set your priorities → best **country** and a recommended **place to stay** |
| **🗺️ Map & Places** | Interactive **map + heatmap** of restaurants, bars, clubs and attractions |

## 🧱 How it fits together

This repo is the **web application** layer. It reads the **data team's pipeline outputs**
(CSV files in `data/`) and turns them into the experience above:

```
holiday-planner/
├── app.py                       # Welcome page (Streamlit entry point)
├── pages/                       # Streamlit multipage app
│   ├── 1_Weather.py
│   ├── 2_Flights_and_Cost.py
│   ├── 3_Recommendation.py
│   └── 4_Map_and_Places.py
├── src/
│   ├── __init__.py
│   └── data_loader.py           # loads the CSVs, re-ranks by user preferences
├── data/                        # data-team pipeline outputs
│   ├── destination_recommendations.csv   # main table: scores, flights, accommodation, cost
│   ├── weather.csv                        # daily weather forecast per destination
│   ├── places.csv                         # nearby places (map / heatmap)
│   └── destinations.csv                   # current-snapshot (secondary)
├── tests/test_data_loader.py    # unit tests (pytest)
├── docs/                        # SoW, team structure, Trello board, project plan
├── presentation/                # 5-slide deck
└── requirements.txt · .gitignore · LICENSE · GITHUB_SETUP.md
```

> **Separation of concerns.** The data team's pipeline (weather, Google Places, flight &
> accommodation scraping, scoring) produces the CSVs; this app focuses on a clean,
> insightful UI. To refresh the data, drop new CSVs of the same shape into `data/`.

## 🚀 Quick start

```bash
git clone <your-repo-url> holiday-planner && cd holiday-planner
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. No API keys are needed to run the app — it reads the CSVs in
`data/`.

## ☁️ Deploy (live demo)

Push to GitHub (see `GITHUB_SETUP.md`) and deploy free on **Streamlit Community Cloud**:
point it at `app.py`. Because the app is CSV-driven, the live demo works out of the box.

## 🧠 How the recommendation works

The data team provides 0–100 **component scores** (weather, nightlife, amenities, cost).
The Recommendation page lets you weight what *you* care about and recomputes a transparent
`user_score`, so the suggested country and place to stay reflect your priorities.

## 🧪 Tests

```bash
pytest -q
```

## 📄 License

MIT — see [LICENSE](LICENSE).
# holiday-planner
