"""Holiday Planner - Streamlit application.

Run:  streamlit run app.py

Recommends and compares adventurous tropical destinations near nightlife by blending
weather, amenity and cost signals into a transparent Adventure Score, with an
interactive map + heatmap. Uses the modular `src` package; see README for details.
"""
from __future__ import annotations
import pandas as pd
import streamlit as st

from src.config import SETTINGS, DEFAULT_WEIGHTS
from src.pipeline import build_recommendations
from src.scoring import explain
from src.llm import recommend_blurb

st.set_page_config(page_title="Holiday Planner", page_icon="🌴", layout="wide")


@st.cache_data(show_spinner="Gathering weather, nightlife and price data…")
def _load(weights_tuple, ideal_temp, nights):
    weights = dict(weights_tuple)
    return build_recommendations(weights=weights, ideal_temp=ideal_temp, trip_nights=nights)


# ----------------------------------------------------------------- sidebar (preferences)
st.sidebar.title("🌴 Your trip")
st.sidebar.caption("Tune the priorities — the ranking updates live.")
nights = st.sidebar.number_input("Trip length (nights)", 3, 28, 7)
ideal_temp = st.sidebar.slider("Ideal max temperature (°C)", 25, 35, 30)
st.sidebar.subheader("What matters to you")
w_night = st.sidebar.slider("Nightlife", 0.0, 1.0, DEFAULT_WEIGHTS["nightlife"], 0.05)
w_value = st.sidebar.slider("Value for money", 0.0, 1.0, DEFAULT_WEIGHTS["value"], 0.05)
w_temp = st.sidebar.slider("Warm weather", 0.0, 1.0, DEFAULT_WEIGHTS["temp_comfort"], 0.05)
w_cloud = st.sidebar.slider("Clear skies", 0.0, 1.0, DEFAULT_WEIGHTS["low_cloud"], 0.05)
w_wind = st.sidebar.slider("Calm winds", 0.0, 1.0, DEFAULT_WEIGHTS["calm_wind"], 0.05)
weights = {"temp_comfort": w_temp, "low_cloud": w_cloud, "calm_wind": w_wind,
           "nightlife": w_night, "value": w_value}

with st.sidebar.expander("Data sources / status"):
    st.write(SETTINGS.status())
    st.caption("Weather: Open-Meteo (keyless). Amenities: Google Places (key). "
               "Prices: web-scraping stub. Cache: SQLite.")

# ----------------------------------------------------------------- main
st.title("Holiday Planner")
st.caption("Adventurous tropical destinations near the nightlife — scored, ranked and mapped.")

ranked = _load(tuple(sorted(weights.items())), ideal_temp, nights)
best = ranked.iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Top pick", f"{best.city}")
c2.metric("Adventure score", f"{best.adventure_score:.0f}/100")
c3.metric("Max temp", f"{best.temp_max:.0f}°C")
c4.metric("Total trip cost", f"£{int(best.total_cost)}")

st.success(recommend_blurb(ranked))

left, right = st.columns([1.15, 1])
with left:
    st.subheader("Ranking")
    show = ranked[["city", "country", "temp_max", "night_clubs", "bars",
                   "restaurants", "total_cost", "adventure_score"]].round(1)
    st.dataframe(show, use_container_width=True, hide_index=True)
    st.bar_chart(ranked.set_index("city")["adventure_score"])
    st.download_button("⬇️ Download recommendations (CSV)",
                       ranked.to_csv(index=False).encode(), "holiday_recommendations.csv")

with right:
    st.subheader("Map & heatmap")
    try:
        import folium
        from folium.plugins import HeatMap
        from streamlit_folium import st_folium
        m = folium.Map(location=[10, 20], zoom_start=2, tiles="cartodbpositron")
        HeatMap(ranked[["lat", "lon", "adventure_score"]].values.tolist(), radius=25).add_to(m)
        for r in ranked.itertuples():
            folium.CircleMarker(
                [r.lat, r.lon], radius=6, color="#065A82", fill=True, fill_opacity=0.9,
                popup=f"{r.city} — {r.adventure_score:.0f}/100",
                tooltip=f"{r.city} ({r.adventure_score:.0f})").add_to(m)
        st_folium(m, height=430, use_container_width=True)
    except Exception:
        st.map(ranked.rename(columns={"lat": "latitude", "lon": "longitude"})[["latitude", "longitude"]])

with st.expander("Why these rankings? (per-destination rationale)"):
    for r in ranked.head(5).itertuples():
        st.write("• " + explain(pd.Series(r._asdict())))

st.caption("Holiday Planner · Data Scientist Specialisation capstone · "
           "Sam Willock · Amechi Obisesan · Fenner Backhouse")
