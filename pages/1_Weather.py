"""Weather page — filter destinations and view forecast graphs.

Reads the daily forecast (``weather.csv``) and renders temperature, humidity, cloud and
wind graphs across the forecast window, plus a summary table.
"""
from __future__ import annotations
import streamlit as st

from src.data_loader import load_weather

st.set_page_config(page_title="Weather · Holiday Planner", page_icon="🌦", layout="wide")


@st.cache_data
def _weather():
    return load_weather()


wx = _weather()
st.title("🌦 Weather forecast")
st.write("Compare the forecast across destinations over the trip window.")

# ---- filters ----
all_dest = sorted(wx["destination"].unique())
chosen = st.multiselect("Destinations", all_dest, default=all_dest)
dmin, dmax = wx["forecast_date"].min().date(), wx["forecast_date"].max().date()
date_range = st.slider("Date range", min_value=dmin, max_value=dmax, value=(dmin, dmax))

f = wx[wx["destination"].isin(chosen)
       & (wx["forecast_date"].dt.date >= date_range[0])
       & (wx["forecast_date"].dt.date <= date_range[1])]

if f.empty:
    st.warning("No data for the current selection — pick at least one destination.")
    st.stop()


def _pivot(col):
    return f.pivot_table(index="forecast_date", columns="destination", values=col)


# ---- graphs ----
st.subheader("🌡 Maximum temperature (°C)")
st.line_chart(_pivot("forecast_max_temp_c"))

c1, c2 = st.columns(2)
with c1:
    st.subheader("Average temperature (°C)")
    st.line_chart(_pivot("forecast_avg_temp_c"))
    st.subheader("Humidity (%)")
    st.line_chart(_pivot("forecast_avg_humidity_pct"))
with c2:
    st.subheader("Cloudiness (%)")
    st.line_chart(_pivot("forecast_avg_cloudiness_pct"))
    st.subheader("Wind speed (m/s)")
    st.line_chart(_pivot("forecast_avg_wind_speed_mps"))

# ---- summary ----
st.subheader("Summary over the selected window")
summary = (f.groupby("destination")
             .agg(avg_max_temp=("forecast_max_temp_c", "mean"),
                  avg_temp=("forecast_avg_temp_c", "mean"),
                  avg_humidity=("forecast_avg_humidity_pct", "mean"),
                  avg_cloud=("forecast_avg_cloudiness_pct", "mean"),
                  avg_wind=("forecast_avg_wind_speed_mps", "mean"))
             .round(1).sort_values("avg_max_temp", ascending=False))
st.dataframe(summary, use_container_width=True)
warmest = summary.index[0]
st.info(f"☀️ Warmest in this window: **{warmest}** "
        f"({summary.loc[warmest, 'avg_max_temp']:.0f}°C average max).")
