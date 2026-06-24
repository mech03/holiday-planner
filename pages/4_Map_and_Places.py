"""Map & Places page — interactive map + amenity heatmap.

Reads ``places.csv`` (nearby restaurants, bars, clubs, attractions, places to stay) and
plots them on a folium map with a density heatmap, plus a filterable top-rated list.
"""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_places, load_recommendations, PLACE_TYPE_LABELS

st.set_page_config(page_title="Map & Places · Holiday Planner", page_icon="🗺️", layout="wide")

CATEGORY_COLOURS = {
    "Restaurants": "red", "Bars": "purple", "Night clubs": "darkblue",
    "Attractions": "green", "Places to stay": "orange",
}


@st.cache_data
def _places():
    return load_places()


@st.cache_data
def _rec():
    return load_recommendations()


places, rec = _places(), _rec()
st.title("🗺️ Map & places")
st.write("Explore the nightlife, food and attractions around each destination.")

# ---- filters ----
dest = st.selectbox("Destination", sorted(places["destination"].unique()))
cats = st.multiselect("Show", list(PLACE_TYPE_LABELS.values()),
                      default=["Restaurants", "Bars", "Night clubs", "Attractions"])
min_rating = st.slider("Minimum rating", 0.0, 5.0, 4.0, 0.1)
show_heat = st.checkbox("Show density heatmap", value=True)

f = places[(places["destination"] == dest)
           & (places["category"].isin(cats))
           & (places["rating"].fillna(0) >= min_rating)].copy()

# headline counts from the recommendation table
row = rec[rec["destination"] == dest]
if not row.empty:
    r = row.iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Bars", int(r["bars_count"]))
    m2.metric("Night clubs", int(r["nightclubs_count"]))
    m3.metric("Restaurants", int(r["restaurants_count"]))
    m4.metric("Attractions", int(r["attractions_count"]))

if f.empty:
    st.warning("No places match the filters — lower the minimum rating or add categories.")
    st.stop()

# ---- map ----
try:
    import folium
    from folium.plugins import HeatMap
    from streamlit_folium import st_folium

    centre = [f["latitude"].mean(), f["longitude"].mean()]
    m = folium.Map(location=centre, zoom_start=13, tiles="cartodbpositron")
    if show_heat:
        HeatMap(f[["latitude", "longitude"]].values.tolist(), radius=18, blur=14).add_to(m)
    for p in f.itertuples():
        colour = CATEGORY_COLOURS.get(p.category, "gray")
        popup = (f"<b>{p.place_name}</b><br>{p.category} · {p.price_label}"
                 f"<br>★ {p.rating} ({int(p.user_rating_count) if p.user_rating_count==p.user_rating_count else 0})"
                 f"<br><a href='{p.google_maps_url}' target='_blank'>Open in Google Maps</a>")
        folium.CircleMarker([p.latitude, p.longitude], radius=5, color=colour, fill=True,
                            fill_opacity=0.85, popup=folium.Popup(popup, max_width=260),
                            tooltip=p.place_name).add_to(m)
    st_folium(m, height=480, use_container_width=True)
except Exception:
    st.map(f.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]])

# ---- legend + top-rated list ----
st.caption("Marker colours — " + " · ".join(f"{k}: {v}" for k, v in CATEGORY_COLOURS.items()))
st.subheader("Top-rated places")
top = (f.sort_values(["rating", "user_rating_count"], ascending=False)
         .head(15)[["place_name", "category", "price_label", "rating",
                    "user_rating_count", "google_maps_url"]]
         .rename(columns={"place_name": "Place", "category": "Type", "price_label": "Price",
                          "rating": "★", "user_rating_count": "Reviews",
                          "google_maps_url": "Map link"}))
st.dataframe(top, use_container_width=True, hide_index=True,
             column_config={"Map link": st.column_config.LinkColumn("Map link", display_text="Open ↗")})
