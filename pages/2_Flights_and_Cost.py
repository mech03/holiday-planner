"""Flights & Cost page — compare flight, accommodation and total trip costs.

Reads the recommendation table (``destination_recommendations.csv``) and renders cost
graphs plus a details table (airline, stops, duration, where to stay).
"""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_recommendations

st.set_page_config(page_title="Flights & Cost · Holiday Planner", page_icon="✈️", layout="wide")


@st.cache_data
def _rec():
    return load_recommendations()


rec = _rec()
st.title("✈️ Flights & cost")
st.write("Compare what each trip would cost — flights, accommodation and total.")

# ---- filters ----
c1, c2 = st.columns(2)
budget = c1.slider("Max total trip budget (£)", 0, int(rec["estimated_trip_cost"].max()) + 100,
                   int(rec["estimated_trip_cost"].max()) + 100, step=50)
max_stops = c2.select_slider("Max flight stops", options=sorted(rec["selected_flight_stops"].unique()),
                             value=int(rec["selected_flight_stops"].max()))

f = rec[(rec["estimated_trip_cost"] <= budget) & (rec["selected_flight_stops"] <= max_stops)]
if f.empty:
    st.warning("No destinations fit those filters — try raising the budget or stops.")
    st.stop()

f = f.sort_values("estimated_trip_cost")
idx = f.set_index("destination")

# ---- graphs ----
g1, g2 = st.columns(2)
with g1:
    st.subheader("Flight price (£)")
    st.bar_chart(idx["selected_flight_price"])
    st.subheader("Flight duration (hours)")
    st.bar_chart((idx["selected_flight_duration_minutes"] / 60).round(1))
with g2:
    st.subheader("Trip cost breakdown (£)")
    breakdown = idx[["selected_flight_price", "estimated_accommodation_cost"]].rename(
        columns={"selected_flight_price": "Flights", "estimated_accommodation_cost": "Accommodation"})
    st.bar_chart(breakdown)  # stacked = total trip cost
    st.caption("Bars stack to the estimated total trip cost.")

# ---- cheapest callout ----
cheapest = f.iloc[0]
st.success(f"💸 **Best value: {cheapest['destination']}** — total ~£{cheapest['estimated_trip_cost']:.0f} "
           f"(flights £{cheapest['selected_flight_price']:.0f} on {cheapest['selected_airline']}, "
           f"{int(cheapest['selected_flight_stops'])} stop(s)).")

# ---- details table ----
st.subheader("Details")
table = f[["destination", "selected_airline", "selected_flight_stops",
           "selected_flight_duration_minutes", "selected_flight_price",
           "selected_accommodation_name", "selected_accommodation_nightly_price",
           "selected_accommodation_rating", "estimated_trip_cost"]].copy()
table["selected_flight_duration_minutes"] = (table["selected_flight_duration_minutes"] / 60).round(1)
table = table.rename(columns={
    "destination": "Destination", "selected_airline": "Airline",
    "selected_flight_stops": "Stops", "selected_flight_duration_minutes": "Flight (hrs)",
    "selected_flight_price": "Flight £", "selected_accommodation_name": "Stay",
    "selected_accommodation_nightly_price": "£/night", "selected_accommodation_rating": "Stay rating",
    "estimated_trip_cost": "Total £"})
st.dataframe(table, use_container_width=True, hide_index=True)
