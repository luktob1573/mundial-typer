import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import json
import urllib.parse
import base64
from io import BytesIO
from PIL import Image

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
BIN_ID = "6a280281da38895dfe9ff2d4"
API_KEY = "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

# --- FUNKCJE DANYCH ---
def load_data_from_jsonbin():
    try:
        response = requests.get(URL, headers={"X-Master-Key": API_KEY})
        record = response.json().get("record", {})
        # Inicjalizacja struktury jeśli pusta
        for key in ["bets", "results", "long_term", "jokers", "avatars"]:
            if key not in record: record[key] = {}
        if "winner_result" not in record: record["winner_result"] = ""
        return record
    except:
        return {"results": {}, "bets": {}, "long_term": {}, "winner_result": "", "jokers": {}, "avatars": {}}

def save_data_to_jsonbin(data):
    requests.put(URL, json=data, headers=HEADERS)

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_avatar_source(name):
    data = load_data_from_jsonbin()
    avatars = data.get('avatars', {})
    if name in avatars:
        return f"data:image/png;base64,{avatars[name]}"
    # Fallback na DiceBear
    prefix = "female" if name in ZENSKIE_IMIONA else "male"
    return f"https://api.dicebear.com/8.x/notionists/svg?seed={urllib.parse.quote(name)}&gender={prefix}"

# --- LISTA GRACZY I MECZE ---
GRACZE = ["Wybierz swoje imię...", "Łukasz T", "Natalia", "Łukasz Z", "Babcia Ania", "Dziadek Adam", "Karolina", "Ala", "Asia", "Babcia Asia", "Dziadek Piotrek", "Wiki", "Wojtas",]
ZENSKIE_IMIONA = ["Natalia", "Babcia Ania", "Karolina", "Ala", "Asia", "Babcia Asia", "Wiki"]
FLAGS = {"Meksyk": "🇲🇽", "RPA": "🇿🇦", "Kanada": "🇨🇦", "Maroko": "🇲🇦", "Francja": "🇫🇷", "Brazylia": "🇧🇷", "Norwegia": "🇳🇴", "Anglia": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Portugalia": "🇵🇹", "Hiszpania": "🇪🇸", "USA": "🇺🇸", "Belgia": "🇧🇪", "Argentyna": "🇦🇷", "Egipt": "🇪🇬", "Szwajcaria": "🇨🇭", "Kolumbia": "🇨🇴", "Paragwaj": "🇵🇾"}
MATCHES = {
    "Kanada vs Maroko": {"date": "2026-07-04", "time": "19:00", "home": "Kanada", "away": "Maroko"},
    "Paragwaj vs Francja": {"date": "2026-07-04", "time": "23:00", "home": "Paragwaj", "away": "Francja"},
    "Brazylia vs Norwegia": {"date": "2026-07-05", "time": "22:00", "home": "Brazylia", "away": "Norwegia"},
    "Meksyk vs Anglia": {"date": "2026-07-06", "time": "02:00", "home": "Meksyk", "away": "Anglia"},
    "Portugalia vs Hiszpania": {"date": "2026-07-06", "time": "21:00", "home": "Portugalia", "away": "Hiszpania"},
    "USA vs Belgia": {"date": "2026-07-07", "time": "02:00", "home": "USA", "away": "Belgia"},
    "Argentyna vs Egipt": {"date": "2026-07-07", "time": "18:00", "home": "Argentyna", "away": "Egipt"},
    "Szwajcaria vs Kolumbia": {"date": "2026-07-07", "time": "22:00", "home": "Szwajcaria", "away": "Kolumbia"}
}

# --- LOGIKA APLIKACJI ---
st.set_page_config(page_title="Rodzinny Typer", page_icon="⚽", layout="centered")
data = load_data_from_jsonbin()
czas_polska = datetime.utcnow() + timedelta(hours=2)

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

with tab1:
    user_name = st.selectbox("Kim jesteś?", GRACZE)
    if user_name != "Wybierz swoje imię...":
        st.write(f"Witaj {user_name}!")
        # ... tutaj wstaw swoją logikę typowania z poprzedniego kodu ...

with tab2:
    st.header("🏆 Podium")
    # Zakładając, że masz posortowaną listę:
    # sorted_leaderboard = [...] 
    # Użycie awatarów:
    # <img src="{get_avatar_source(p1)}" ...>
    st.markdown("---")
    st.subheader("📸 Ustaw swój Awatar")
    user_name_avatar = st.selectbox("Wybierz swoje imię:", GRACZE, key="avatar_select")
    uploaded_file = st.file_uploader("Wgraj zdjęcie (kwadratowe):", type=["jpg", "png"])
    if uploaded_file and st.button("Zapisz Awatar"):
        img = Image.open(uploaded_file).convert("RGB").resize((200, 200))
        data = load_data_from_jsonbin()
        data['avatars'][user_name_avatar] = image_to_base64(img)
        save_data_to_jsonbin(data)
        st.success("Zapisano!")
        st.rerun()

with tab3:
    st.header("⚙️ Admin")
    # ... tutaj wstaw swoją logikę Admina ...
