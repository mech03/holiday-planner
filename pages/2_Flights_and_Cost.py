"""Flights & Cost page — compare flight, accommodation and total trip costs."""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_recommendations
from src.ui import apply_styles

st.set_page_config(page_title="Flights & Cost · Holiday Planner", layout="wide")
apply_styles()


@st.cache_data
def _rec():
    return load_recommendations()


rec = _rec()
st.title("Flights and Cost")
st.write("See what each trip would actually cost, broken down by flights, accommodation and total spend.")

st.divider()

# ---- filters ----
c1, c2 = st.columns(2)
budget = c1.slider("Max total trip budget (£)", 0, int(rec["estimated_trip_cost"].max()) + 100,
                   int(rec["estimated_trip_cost"].max()) + 100, step=50)
max_stops = c2.select_slider("Max flight stops", options=sorted(rec["selected_flight_stops"].unique()),
                             value=int(rec["selected_flight_stops"].max()))

f = rec[(rec["estimated_trip_cost"] <= budget) & (rec["selected_flight_stops"] <= max_stops)]
if f.empty:
    st.warning("No destinations fit those filters. Try raising the budget or allowing more stops.")
    st.stop()

f = f.sort_values("estimated_trip_cost")
idx = f.set_index("destination")

st.divider()

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
    st.bar_chart(breakdown)
    st.caption("Bars stack to the estimated total trip cost.")

st.divider()

# ---- cheapest callout ----
cheapest = f.iloc[0]
st.success(
    f"Best value: **{cheapest['destination']}**, total around £{cheapest['estimated_trip_cost']:.0f} "
    f"(flights £{cheapest['selected_flight_price']:.0f} on {cheapest['selected_airline']}, "
    f"{int(cheapest['selected_flight_stops'])} stop(s))."
)

# ---- details table ----
st.subheader("Full details")
table = f[["destination", "selected_airline", "selected_flight_stops",
           "selected_flight_duration_minutes", "selected_flight_price",
           "selected_accommodation_name", "selected_accommodation_nightly_price",
           "selected_accommodation_rating", "estimated_trip_cost"]].copy()
table["selected_flight_duration_minutes"] = (table["selected_flight_duration_minutes"] / 60).round(1)
table = table.rename(columns={
    "destination": "Destination", "selected_airline": "Airline",
    "selected_flight_stops": "Stops", "selected_flight_duration_minutes": "Flight (hrs)",
    "selected_flight_price": "Flight (£)", "selected_accommodation_name": "Stay",
    "selected_accommodation_nightly_price": "Per night (£)", "selected_accommodation_rating": "Stay rating",
    "estimated_trip_cost": "Total (£)"})
st.dataframe(table, use_container_width=True, hide_index=True)
