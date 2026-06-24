"""Holiday Planner — Streamlit app (Welcome page).

Run:  streamlit run app.py

A holiday-recommendation app for adventurous tropical trips near the nightlife. It reads
the data team's pipeline outputs (weather forecasts, nearby places, flight/accommodation
costs and component scores) and turns them into an explorable, filterable experience:

    • Welcome           (this page)        — overview + headline pick + destination map
    • 🌦  Weather        (pages/1)          — filter destinations, weather graphs
    • ✈️  Flights & Cost (pages/2)          — flight/accommodation/trip-cost graphs
    • 🏆  Recommendation (pages/3)          — tell us your priorities → best country & place to stay
    • 🗺️  Map & Places   (pages/4)          — interactive map + amenity heatmap

Owner: Amechi Obisesan (web application & UI).
"""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_recommendations

st.set_page_config(page_title="Holiday Planner", page_icon="🌴", layout="wide")


@st.cache_data
def _rec():
    return load_recommendations()


rec = _rec()

# ---------------------------------------------------------------- hero
st.title("🌴 Holiday Planner")
st.subheader("Find an adventurous tropical escape — near the nightlife, within budget.")
st.write(
    "Out of vacation time and spoilt for choice? Holiday Planner compares warm, lively "
    "destinations on **weather**, **nightlife & amenities** and **cost**, then recommends "
    "where to go and where to stay. Use the pages in the sidebar to explore the data and "
    "get a recommendation tailored to what *you* care about."
)

# ---------------------------------------------------------------- headline pick
top = rec.sort_values("final_recommendation_score", ascending=False).iloc[0]
st.success(
    f"🏆 **Today's top pick: {top['destination']}** — score "
    f"{top['final_recommendation_score']:.0f}/100 · ~{top['avg_temp_c']:.0f}°C · "
    f"flights ~£{top['selected_flight_price']:.0f} · est. trip £{top['estimated_trip_cost']:.0f}"
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Destinations compared", len(rec))
c2.metric("Cheapest flight", f"£{rec['selected_flight_price'].min():.0f}")
c3.metric("Warmest", f"{rec['avg_temp_c'].max():.0f}°C")
c4.metric("Lowest trip cost", f"£{rec['estimated_trip_cost'].min():.0f}")

# ---------------------------------------------------------------- candidate map + how to use
left, right = st.columns([1, 1])
with left:
    st.markdown("#### Candidate destinations")
    st.map(rec.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]],
           size=40000, zoom=1)
with right:
    st.markdown("#### How to use")
    st.markdown(
        "1. **🌦 Weather** — pick destinations and see the forecast graphs.\n"
        "2. **✈️ Flights & Cost** — compare flight, stay and total trip costs.\n"
        "3. **🏆 Recommendation** — set your priorities and get the best country + place to stay.\n"
        "4. **🗺️ Map & Places** — explore restaurants, bars, clubs and attractions on a map + heatmap."
    )
    st.markdown("#### Forecast window")
    st.write(f"{rec['forecast_start_date'].iloc[0]} → {rec['forecast_end_date'].iloc[0]} "
             f"({int(rec['forecast_days'].iloc[0])} days)")

st.caption("Data: data team pipeline (Open-Meteo weather · Google Places · flight/accommodation "
           "scrape). App & UI: Amechi Obisesan · Holiday Planner capstone.")
