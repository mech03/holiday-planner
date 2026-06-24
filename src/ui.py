from __future__ import annotations
import streamlit as st

_CSS = """
<style>
/* Tighten top padding */
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; }

/* Metric values */
[data-testid="stMetricValue"] { font-size: 1.75rem; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase; }

/* Section dividers */
hr { border-top: 1px solid #D4E4F0; margin: 1.4rem 0; }

/* Alert / callout boxes */
[data-testid="stAlert"] { border-radius: 8px; }

/* Download / action buttons */
.stDownloadButton > button {
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: 0.02em;
}

/* Sidebar sliders — label spacing */
[data-testid="stSidebar"] label { font-size: 0.9rem; }

/* Dataframe header */
[data-testid="stDataFrame"] thead th {
    background-color: #EAF1F8;
    font-weight: 700;
}
</style>
"""


def apply_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
