"""Recommendation page — set your priorities, get the best country & place to stay.

Uses the data team's component scores (weather / nightlife / amenities / cost) and the
user's preference weights to re-rank destinations, then highlights the top country and a
recommended place to stay.
"""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_recommendations, rerank, recommend_text, SCORE_COMPONENTS

st.set_page_config(page_title="Recommendation · Holiday Planner", page_icon="🏆", layout="wide")


@st.cache_data
def _rec():
    return load_recommendations()


rec = _rec()
st.title("🏆 Your recommendation")
st.write("Tell us what matters most for *your* trip — the ranking updates instantly.")

# ---- preference sliders -> weights ----
st.sidebar.header("What matters to you?")
weights = {
    "weather_score": st.sidebar.slider("Great weather", 0.0, 1.0, 0.30, 0.05),
    "nightlife_score": st.sidebar.slider("Nightlife", 0.0, 1.0, 0.30, 0.05),
    "amenity_score": st.sidebar.slider("Restaurants & attractions", 0.0, 1.0, 0.20, 0.05),
    "cost_score": st.sidebar.slider("Low cost / value", 0.0, 1.0, 0.20, 0.05),
}
if sum(weights.values()) == 0:
    st.warning("Move at least one slider above zero to get a recommendation.")
    st.stop()

ranked = rerank(rec, weights)
top = ranked.iloc[0]

# ---- headline ----
st.success("✅ " + recommend_text(top))
c1, c2, c3 = st.columns(3)
c1.metric("Best country", str(top["country"]))
c2.metric("Match score", f"{top['user_score']:.0f}/100")
c3.metric("Est. trip cost", f"£{top['estimated_trip_cost']:.0f}")

# ---- ranking chart ----
st.subheader("Ranked destinations (your priorities)")
st.bar_chart(ranked.set_index("destination")["user_score"])

left, right = st.columns([1, 1])
with left:
    st.subheader("Why it wins — score breakdown")
    comp = top[list(SCORE_COMPONENTS)].rename(SCORE_COMPONENTS)
    st.bar_chart(comp)
with right:
    st.subheader("Where to stay")
    st.markdown(f"**{top['selected_accommodation_name']}**")
    bits = []
    if "selected_accommodation_type" in top and str(top["selected_accommodation_type"]) != "nan":
        bits.append(str(top["selected_accommodation_type"]))
    if not (top.get("selected_accommodation_nightly_price") != top.get("selected_accommodation_nightly_price")):
        bits.append(f"£{top['selected_accommodation_nightly_price']:.0f}/night")
    if not (top.get("selected_accommodation_rating") != top.get("selected_accommodation_rating")):
        bits.append(f"★ {top['selected_accommodation_rating']:.1f}")
    st.write(" · ".join(bits) if bits else "—")
    link = str(top.get("selected_accommodation_link", ""))
    if link and link.lower() != "nan":
        st.markdown(f"[View accommodation ↗]({link})")

# ---- full table + download ----
st.subheader("Full ranking")
cols = ["destination", "country", "user_score", "final_recommendation_score",
        "avg_temp_c", "selected_flight_price", "estimated_trip_cost"] + list(SCORE_COMPONENTS)
st.dataframe(ranked[cols].round(1), use_container_width=True, hide_index=True)
st.download_button("⬇️ Download ranking (CSV)", ranked.to_csv(index=False).encode(),
                   "my_holiday_recommendations.csv")
