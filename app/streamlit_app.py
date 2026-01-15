"""
Streamlit app for predicting apartment prices in Warsaw.
"""
import time
from pathlib import Path

import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8008"
PREDICT_URL = f"{API_BASE}/model/predict"
OPTIONS_URL = f"{API_BASE}/model/options"

BASE_DIR = Path(__file__).resolve().parent
HEADER_IMAGE = (BASE_DIR.parent / "images" / "warsaw_image.jpg").resolve()


districts: list[str] = []
construction_statuses: list[str] = []
markets: list[str] = []

def load_options() -> tuple[list[str], list[str], list[str]]:
    """Load categorical feature options from the API."""
    try:
        resp = requests.get(OPTIONS_URL, timeout=3)
        if resp.ok:
            j = resp.json()
            return (
                j.get("districts") or [],
                j.get("construction_statuses") or [],
                j.get("markets") or [],
            )
    except requests.RequestException:
        st.error("Nie można załadować opcji z serwera.")
    return [], [], []

if "options_loaded" not in st.session_state:
    districts, construction_statuses, markets = load_options()
    st.session_state["districts"] = districts
    st.session_state["construction_statuses"] = construction_statuses
    st.session_state["markets"] = markets

st.title("Przewidywanie cen mieszkań w Warszawie")

if HEADER_IMAGE.exists():
    st.image(str(HEADER_IMAGE))

st.info("Wyniki nie są wiążące i służą wyłącznie celom informacyjnym.")

with st.form("predict_form"):
    c1, c2, c3 = st.columns(3)
    district = c1.selectbox("Dzielnica", districts)
    surface = c2.number_input(
        "Powierzchnia (m²)",
        min_value=14.0,
        max_value=102.0,
        value=60.5,
        format="%.2f")
    rooms_num = c3.number_input("Liczba pokoi", min_value=1, max_value=6, value=3, step=1)

    c4, c5, c6 = st.columns(3)
    construction_status = c4.selectbox("Stan wykończenia", construction_statuses)
    market = c5.selectbox("Rynek", markets)
    build_year = c6.number_input("Rok budowy", min_value=1900, max_value=2025, value=2005, step=1)

    c7, c8, c9 = st.columns(3)
    floor_no = c7.number_input("Piętro", min_value=0, max_value=50, value=2, step=1)
    building_floors_num = c8.number_input("Liczba pięter w budynku", min_value=1, max_value=50, value=5, step=1)
    transit_dur_m = c9.number_input("Czas komunikacją miejską do centrum warszawy (m)", min_value=4.9, max_value=230.0, value=5.0, format="%.1f")

    model_name_col, submit_col = st.columns([3, 1])
    submitted = submit_col.form_submit_button("Oblicz cenę")


if submitted:
    payload = {
        "district": district,
        "surface": float(surface),
        "rooms_num": int(rooms_num),
        "construction_status": construction_status,
        "market": market,
        "build_year": int(build_year),
        "floor_no": int(floor_no),
        "building_floors_num": int(building_floors_num),
        "transit_dur_m": float(transit_dur_m)
    }

    with st.spinner("Obliczanie..."):
        time.sleep(0.6)
        st.divider()
        try:
            resp = requests.post(PREDICT_URL, json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                price_raw = data.get("predicted_price")

                try:
                    price_val = float(price_raw)
                    formatted = f"{price_val:,.2f}"
                    formatted = formatted.replace(",", " ").replace(".", ",")  # "1 234 567,89"
                    st.text("Wynik:")
                    st.success(f"{formatted} PLN")

                except (TypeError, ValueError):
                    formatted = str(price_raw)
            else:
                st.error(f"Błąd serwera: {resp.status_code} - {resp.text}")
        except requests.RequestException as e:
            st.error(f"Błąd połączenia: {e}")
