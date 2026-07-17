import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import json
import urllib.parse

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
BIN_ID = "6a280281da38895dfe9ff2d4"
API_KEY = "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# --- LISTA GRACZY ---
GRACZE = ["Wybierz swoje imię...", "Łukasz T", "Natalia", "Łukasz Z", "Babcia Ania", "Dziadek Adam", "Karolina", "Ala", "Asia", "Babcia Asia", "Dziadek Piotrek", "Wiki", "Wojtas",]
ZENSKIE_IMIONA = ["Natalia", "Babcia Ania", "Karolina", "Ala", "Asia", "Babcia Asia", "Wiki"]

# --- SŁOWNIK FLAG ---
FLAGS = {
    "Meksyk": "🇲🇽", "RPA": "🇿🇦", "Korea Płd.": "🇰🇷", "Czechy": "🇨🇿",
    "Kanada": "🇨🇦", "Bośnia i Herc.": "🇧🇦", "Katar": "🇶🇦", "Szwajcaria": "🇨🇭",
    "Brazylia": "🇧🇷", "Maroko": "🇲🇦", "Haiti": "🇭🇹", "Szkocja": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "USA": "🇺🇸", "Paragwaj": "🇵🇾", "Australia": "🇦🇺", "Turcja": "🇹🇷",
    "Niemcy": "🇩🇪", "Curacao": "🇨🇼", "WKS": "🇨🇮", "Ekwador": "🇪🇨",
    "Holandia": "🇳🇱", "Japonia": "🇯🇵", "Szwecja": "🇸🇪", "Tunezja": "🇹🇳",
    "Belgia": "🇧🇪", "Egipt": "🇪🇬", "Iran": "🇮🇷", "Nowa Zelandia": "🇳🇿",
    "Hiszpania": "🇪🇸", "Rep. Z. Przyl.": "🇨🇻", "Arabia Saud.": "🇸🇦", "Urugwaj": "🇺🇾",
    "Francja": "🇫🇷", "Senegal": "🇸🇳", "Irak": "🇮🇶", "Norwegia": "🇳🇴",
    "Argentyna": "🇦🇷", "Algieria": "🇩🇿", "Austria": "🇦🇹", "Jordania": "🇯🇴",
    "Portugalia": "🇵🇹", "DR Konga": "🇨🇩", "Uzbekistan": "🇺🇿", "Kolumbia": "🇨🇴",
    "Anglia": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Chorwacja": "🇭🇷", "Ghana": "🇬🇭", "Panama": "🇵🇦", "Polska": "🇵🇱"
}

lista_panstw = sorted(list(FLAGS.keys()))

# --- BAZA MECZÓW Z DATAMI I GODZINAMI ---
MATCHES = {
    # --- FAZA GRUPOWA (ZACHOWANA DLA HISTORII I WYKRESÓW) ---
    "Meksyk vs RPA": {"date": "2026-06-11", "time": "21:00", "home": "Meksyk", "away": "RPA"},
    "Korea Płd. vs Czechy": {"date": "2026-06-12", "time": "04:00", "home": "Korea Płd.", "away": "Czechy"},
    "Kanada vs Bośnia i Herc.": {"date": "2026-06-12", "time": "21:00", "home": "Kanada", "away": "Bośnia i Herc."},
    "USA vs Paragwaj": {"date": "2026-06-13", "time": "03:00", "home": "USA", "away": "Paragwaj"},
    "Katar vs Szwajcaria": {"date": "2026-06-13", "time": "21:00", "home": "Katar", "away": "Szwajcaria"},
    "Brazylia vs Maroko": {"date": "2026-06-14", "time": "00:00", "home": "Brazylia", "away": "Maroko"},
    "Haiti vs Szkocja": {"date": "2026-06-14", "time": "03:00", "home": "Haiti", "away": "Szkocja"},
    "Australia vs Turcja": {"date": "2026-06-14", "time": "06:00", "home": "Australia", "away": "Turcja"},
    "Niemcy vs Curacao": {"date": "2026-06-14", "time": "19:00", "home": "Niemcy", "away": "Curacao"},
    "Holandia vs Japonia": {"date": "2026-06-14", "time": "22:00", "home": "Holandia", "away": "Japonia"},
    "WKS vs Ekwador": {"date": "2026-06-15", "time": "01:00", "home": "WKS", "away": "Ekwador"},
    "Szwecja vs Tunezja": {"date": "2026-06-15", "time": "04:00", "home": "Szwecja", "away": "Tunezja"},
    "Hiszpania vs Rep. Z. Przyl.": {"date": "2026-06-15", "time": "18:00", "home": "Hiszpania", "away": "Rep. Z. Przyl."},
    "Belgia vs Egipt": {"date": "2026-06-15", "time": "21:00", "home": "Belgia", "away": "Egipt"},
    "Arabia Saud. vs Urugwaj": {"date": "2026-06-16", "time": "00:00", "home": "Arabia Saud.", "away": "Urugwaj"},
    "Iran vs Nowa Zelandia": {"date": "2026-06-16", "time": "03:00", "home": "Iran", "away": "Nowa Zelandia"},
    "Francja vs Senegal": {"date": "2026-06-16", "time": "21:00", "home": "Francja", "away": "Senegal"},
    "Irak vs Norwegia": {"date": "2026-06-17", "time": "00:00", "home": "Irak", "away": "Norwegia"},
    "Argentyna vs Algieria": {"date": "2026-06-17", "time": "03:00", "home": "Argentyna", "away": "Algieria"},
    "Austria vs Jordania": {"date": "2026-06-17", "time": "06:00", "home": "Austria", "away": "Jordania"},
    "Portugalia vs DR Konga": {"date": "2026-06-17", "time": "19:00", "home": "Portugalia", "away": "DR Konga"},
    "Anglia vs Chorwacja": {"date": "2026-06-17", "time": "22:00", "home": "Anglia", "away": "Chorwacja"},
    "Ghana vs Panama": {"date": "2026-06-18", "time": "01:00", "home": "Ghana", "away": "Panama"},
    "Uzbekistan vs Kolumbia": {"date": "2026-06-18", "time": "04:00", "home": "Uzbekistan", "away": "Kolumbia"},
    "Czechy vs RPA": {"date": "2026-06-18", "time": "18:00", "home": "Czechy", "away": "RPA"},
    "Szwajcaria vs Bośnia i Herc.": {"date": "2026-06-18", "time": "21:00", "home": "Szwajcaria", "away": "Bośnia i Herc."},
    "Kanada vs Katar": {"date": "2026-06-19", "time": "00:00", "home": "Kanada", "away": "Katar"},
    "Meksyk vs Korea Płd.": {"date": "2026-06-19", "time": "03:00", "home": "Meksyk", "away": "Korea Płd."},
    "USA vs Australia": {"date": "2026-06-19", "time": "21:00", "home": "USA", "away": "Australia"},
    "Szkocja vs Maroko": {"date": "2026-06-20", "time": "00:00", "home": "Szkocja", "away": "Maroko"},
    "Brazylia vs Haiti": {"date": "2026-06-20", "time": "03:00", "home": "Brazylia", "away": "Haiti"},
    "Turcja vs Paragwaj": {"date": "2026-06-20", "time": "06:00", "home": "Turcja", "away": "Paragwaj"},
    "Holandia vs Szwecja": {"date": "2026-06-20", "time": "19:00", "home": "Holandia", "away": "Szwecja"},
    "Niemcy vs WKS": {"date": "2026-06-20", "time": "22:00", "home": "Niemcy", "away": "WKS"},
    "Tunezja vs Japonia": {"date": "2026-06-21", "time": "00:00", "home": "Tunezja", "away": "Japonia"},
    "Ekwador vs Curacao": {"date": "2026-06-21", "time": "02:00", "home": "Ekwador", "away": "Curacao"},
    "Hiszpania vs Arabia Saud.": {"date": "2026-06-21", "time": "18:00", "home": "Hiszpania", "away": "Arabia Saud."},
    "Belgia vs Iran": {"date": "2026-06-21", "time": "21:00", "home": "Belgia", "away": "Iran"},
    "Urugwaj vs Rep. Z. Przyl.": {"date": "2026-06-22", "time": "00:00", "home": "Urugwaj", "away": "Rep. Z. Przyl."},
    "Nowa Zelandia vs Egipt": {"date": "2026-06-22", "time": "03:00", "home": "Nowa Zelandia", "away": "Egipt"},
    "Argentyna vs Austria": {"date": "2026-06-22", "time": "19:00", "home": "Argentyna", "away": "Austria"},
    "Francja vs Irak": {"date": "2026-06-22", "time": "23:00", "home": "Francja", "away": "Irak"},
    "Norwegia vs Senegal": {"date": "2026-06-23", "time": "02:00", "home": "Norwegia", "away": "Senegal"},
    "Jordania vs Algieria": {"date": "2026-06-23", "time": "05:00", "home": "Jordania", "away": "Algieria"},
    "Portugalia vs Uzbekistan": {"date": "2026-06-23", "time": "19:00", "home": "Portugalia", "away": "Uzbekistan"},
    "Anglia vs Ghana": {"date": "2026-06-23", "time": "22:00", "home": "Anglia", "away": "Ghana"},
    "Panama vs Chorwacja": {"date": "2026-06-24", "time": "01:00", "home": "Panama", "away": "Chorwacja"},
    "Kolumbia vs DR Konga": {"date": "2026-06-24", "time": "04:00", "home": "Kolumbia", "away": "DR Konga"},
    "Szwajcaria vs Kanada": {"date": "2026-06-24", "time": "21:00", "home": "Szwajcaria", "away": "Kanada"},
    "Bośnia i Herc. vs Katar": {"date": "2026-06-24", "time": "21:00", "home": "Bośnia i Herc.", "away": "Katar"},
    "Maroko vs Haiti": {"date": "2026-06-25", "time": "00:00", "home": "Maroko", "away": "Haiti"},
    "Szkocja vs Brazylia": {"date": "2026-06-25", "time": "00:00", "home": "Szkocja", "away": "Brazylia"},
    "RPA vs Korea Płd.": {"date": "2026-06-25", "time": "03:00", "home": "RPA", "away": "Korea Płd."},
    "Czechy vs Meksyk": {"date": "2026-06-25", "time": "03:00", "home": "Czechy", "away": "Meksyk"},
    "Curacao vs WKS": {"date": "2026-06-25", "time": "22:00", "home": "Curacao", "away": "WKS"},
    "Ekwador vs Niemcy": {"date": "2026-06-25", "time": "22:00", "home": "Ekwador", "away": "Niemcy"},
    "Japonia vs Szwecja": {"date": "2026-06-26", "time": "01:00", "home": "Japonia", "away": "Szwecja"},
    "Tunezja vs Holandia": {"date": "2026-06-26", "time": "01:00", "home": "Tunezja", "away": "Holandia"},
    "Paragwaj vs Australia": {"date": "2026-06-26", "time": "04:00", "home": "Paragwaj", "away": "Australia"},
    "Turcja vs USA": {"date": "2026-06-26", "time": "04:00", "home": "Turcja", "away": "USA"},
    "Norwegia vs Francja": {"date": "2026-06-26", "time": "21:00", "home": "Norwegia", "away": "Francja"},
    "Senegal vs Irak": {"date": "2026-06-26", "time": "21:00", "home": "Senegal", "away": "Irak"},
    "Rep. Z. Przyl. vs Arabia Saud.": {"date": "2026-06-27", "time": "02:00", "home": "Rep. Z. Przyl.", "away": "Arabia Saud."},
    "Urugwaj vs Hiszpania": {"date": "2026-06-27", "time": "02:00", "home": "Urugwaj", "away": "Hiszpania"},
    "Egipt vs Iran": {"date": "2026-06-27", "time": "05:00", "home": "Egipt", "away": "Iran"},
    "Nowa Zelandia vs Belgia": {"date": "2026-06-27", "time": "05:00", "home": "Nowa Zelandia", "away": "Belgia"},
    "Chorwacja vs Ghana": {"date": "2026-06-27", "time": "23:00", "home": "Chorwacja", "away": "Ghana"},
    "Panama vs Anglia": {"date": "2026-06-27", "time": "23:00", "home": "Panama", "away": "Anglia"},
    "Kolumbia vs Portugalia": {"date": "2026-06-28", "time": "01:30", "home": "Kolumbia", "away": "Portugalia"},
    "DR Konga vs Uzbekistan": {"date": "2026-06-28", "time": "01:30", "home": "DR Konga", "away": "Uzbekistan"},
    "Jordania vs Argentyna": {"date": "2026-06-28", "time": "04:00", "home": "Jordania", "away": "Argentyna"},
    "Algieria vs Austria": {"date": "2026-06-28", "time": "04:00", "home": "Algieria", "away": "Austria"},
    
    # --- NOWA FAZA 1/16 FINAŁU ---
    "RPA vs Kanada": {"date": "2026-06-28", "time": "21:00", "home": "RPA", "away": "Kanada"},
    "Brazylia vs Japonia": {"date": "2026-06-29", "time": "19:00", "home": "Brazylia", "away": "Japonia"},
    "Niemcy vs Paragwaj": {"date": "2026-06-29", "time": "22:30", "home": "Niemcy", "away": "Paragwaj"},
    "Holandia vs Maroko": {"date": "2026-06-30", "time": "03:00", "home": "Holandia", "away": "Maroko"},
    "WKS vs Norwegia": {"date": "2026-06-30", "time": "19:00", "home": "WKS", "away": "Norwegia"},
    "Francja vs Szwecja": {"date": "2026-06-30", "time": "23:00", "home": "Francja", "away": "Szwecja"},
    "Meksyk vs Ekwador": {"date": "2026-07-01", "time": "03:00", "home": "Meksyk", "away": "Ekwador"},
    "Anglia vs DR Konga": {"date": "2026-07-01", "time": "18:00", "home": "Anglia", "away": "DR Konga"},
    "Belgia vs Senegal": {"date": "2026-07-01", "time": "22:00", "home": "Belgia", "away": "Senegal"},
    "USA vs Bośnia i Herc.": {"date": "2026-07-02", "time": "02:00", "home": "USA", "away": "Bośnia i Herc."},
    "Hiszpania vs Austria": {"date": "2026-07-02", "time": "21:00", "home": "Hiszpania", "away": "Austria"},
    "Portugalia vs Chorwacja": {"date": "2026-07-03", "time": "01:00", "home": "Portugalia", "away": "Chorwacja"},
    "Szwajcaria vs Algieria": {"date": "2026-07-03", "time": "05:00", "home": "Szwajcaria", "away": "Algieria"},
    "Australia vs Egipt": {"date": "2026-07-03", "time": "20:00", "home": "Australia", "away": "Egipt"},
    "Argentyna vs Rep. Z. Przyl.": {"date": "2026-07-04", "time": "00:00", "home": "Argentyna", "away": "Rep. Z. Przyl."},
    "Kolumbia vs Ghana": {"date": "2026-07-04", "time": "03:30", "home": "Kolumbia", "away": "Ghana"},
    
    # --- ZAKTUALIZOWANA LISTA MECZÓW 1/8 FINAŁU ---
    "Kanada vs Maroko": {"date": "2026-07-04", "time": "19:00", "home": "Kanada", "away": "Maroko"},
    "Paragwaj vs Francja": {"date": "2026-07-04", "time": "23:00", "home": "Paragwaj", "away": "Francja"},
    "Brazylia vs Norwegia": {"date": "2026-07-05", "time": "22:00", "home": "Brazylia", "away": "Norwegia"},
    "Meksyk vs Anglia": {"date": "2026-07-06", "time": "02:00", "home": "Meksyk", "away": "Anglia"},
    "Portugalia vs Hiszpania": {"date": "2026-07-06", "time": "21:00", "home": "Portugalia", "away": "Hiszpania"},
    "USA vs Belgia": {"date": "2026-07-07", "time": "02:00", "home": "USA", "away": "Belgia"},
    "Argentyna vs Egipt": {"date": "2026-07-07", "time": "18:00", "home": "Argentyna", "away": "Egipt"},
    "Szwajcaria vs Kolumbia": {"date": "2026-07-07", "time": "22:00", "home": "Szwajcaria", "away": "Kolumbia"},
        # --- FAZA 1/4 FINAŁU (ĆWIERĆFINAŁY) ---
    "Ćwierćfinał 1": {"date": "2026-07-09", "time": "22:00", "home": "Francja", "away": "Maroko"},
    "Ćwierćfinał 2": {"date": "2026-07-10", "time": "21:00", "home": "Hiszpania", "away": "Belgia"},
    "Ćwierćfinał 3": {"date": "2026-07-11", "time": "23:00", "home": "Norwegia", "away": "Anglia"},
    "Ćwierćfinał 4": {"date": "2026-07-12", "time": "03:00", "home": "Argentyna", "away": "Szwajcaria"},
    # --- FAZA PÓŁFINAŁOWA ---
    "Półfinał 1": {"date": "2026-07-14", "time": "21:00", "home": "Francja", "away": "Hiszpania"},
    "Półfinał 2": {"date": "2026-07-15", "time": "21:00", "home": "Anglia", "away": "Argentyna"},

    # --- FINAŁY ---
    "Mecz o 3. miejsce": {"date": "2026-07-18", "time": "23:00", "home": "Francja", "away": "Anglia"},
    "Finał": {"date": "2026-07-19", "time": "21:00", "home": "Hiszpania", "away": "Argentyna"}

}

def load_data():
    try:
        response = requests.get(URL, headers={"X-Master-Key": API_KEY})
        record = response.json().get("record", {})
        if "bets" not in record: record["bets"] = {}
        if "results" not in record: record["results"] = {}
        if "long_term" not in record: record["long_term"] = {}
        if "winner_result" not in record: record["winner_result"] = ""
        if "jokers" not in record: record["jokers"] = {}
        return record
    except Exception:
        return {"results": {}, "bets": {}, "long_term": {}, "winner_result": "", "jokers": {}}

def save_data(data):
    requests.put(URL, json=data, headers=HEADERS)

data = load_data()

def calculate_points(bet_h, bet_a, res_h, res_a, bet_pen=False, res_pen=False):
    if res_h is None or res_a is None: return 0
    pts = 0
    if bet_h == res_h and bet_a == res_a:
        pts = 3
    elif (bet_h > bet_a and res_h > res_a) or (bet_h < bet_a and res_h < res_a) or (bet_h == bet_a and res_h == res_a):
        pts = 1
    # Ekstra punkt za rzuty karne (tylko gdy postawiono remis)
    if bet_pen and res_pen and bet_h == bet_a:
        pts += 1
    return pts

st.set_page_config(page_title="Rodzinny Typer", page_icon="⚽", layout="centered")

# --- ZMIANY WIZUALNE: CSS Z KARTAMI MECZOWYMI, PASKAMI I CZCIONKĄ ---
page_bg_img = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Oswald', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(15, 32, 39, 0.85), rgba(32, 58, 67, 0.85)), url("https://images.unsplash.com/photo-1518605368461-1ee1252271b1?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 5px;
}

/* KARTY MECZOWE */
.match-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    padding: 15px 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    transition: transform 0.2s;
}
.match-card:hover {
    transform: translateY(-2px);
    border-color: rgba(37, 211, 102, 0.5);
    box-shadow: 0 8px 32px 0 rgba(37, 211, 102, 0.2);
}
.match-header {
    text-align: center;
    color: #b0bec5;
    font-size: 14px;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 8px;
    margin-bottom: 12px;
}
.match-teams {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 24px;
    font-weight: 700;
}
.team { width: 40%; }
.team-left { text-align: right; }
.team-right { text-align: left; }
.vs {
    width: 20%;
    text-align: center;
    color: #ff4b4b;
    font-size: 20px;
    font-weight: 600;
}

/* NEONOWE PRZYCISKI */
.stButton > button {
    border-radius: 20px;
    text-transform: uppercase;
    font-weight: bold;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.3);
}
.stButton > button:hover {
    box-shadow: 0 0 15px rgba(37, 211, 102, 0.8);
    border-color: #25D366;
    color: #25D366;
}

/* PASKI POSTĘPU */
.stProgress > div > div > div > div {
    background-image: linear-gradient(to right, #00b4db, #0083b0);
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("⚽ Rodzinny Typer")

# --- CZAS W POLSCE ---
czas_polska = datetime.utcnow() + timedelta(hours=2)
dzisiaj_obj = czas_polska.date()
jutro_obj = dzisiaj_obj + timedelta(days=1)

st.write(f"<p style='text-align: center; color: #b0bec5;'>📅 Mecze dostępne na: <b>{dzisiaj_obj.strftime('%d.%m')}</b> oraz <b>{jutro_obj.strftime('%d.%m')}</b></p>", unsafe_allow_html=True)

# --- WSTĘPNE OBLICZENIE TABELI I ODZNAK ---
leaderboard_pre = {u: 0 for u in GRACZE[1:]}
user_badges = {u: [] for u in GRACZE[1:]}

for user in GRACZE[1:]:
    total_pts = 0
    zero_zero_count = 0
    draw_count = 0
    pechowiec = False
    
    user_bets = data.get("bets", {}).get(user, {})
    user_jokers = data.get("jokers", {}).get(user, [])
    
    for match_id, bet in user_bets.items():
        bet_h, bet_a = bet[0], bet[1]
        bet_pen = bet[2] if len(bet) > 2 else False
        
        if bet_h == 0 and bet_a == 0: zero_zero_count += 1
        if bet_h == bet_a: draw_count += 1
        
        if match_id in data.get("results", {}):
            res = data["results"][match_id]
            res_h, res_a = res[0], res[1]
            res_pen = res[2] if len(res) > 2 else False
            
            pts = calculate_points(bet_h, bet_a, res_h, res_a, bet_pen, res_pen)
            
            if match_id in user_jokers and pts == 0: pechowiec = True
            if match_id in user_jokers: pts *= 2
            total_pts += pts
            
    if pechowiec: user_badges[user].append("🤡")
    if draw_count >= 5: user_badges[user].append("🤝")
    if zero_zero_count >= 3: user_badges[user].append("🛡️")
            
    if data.get("winner_result") and data.get("long_term", {}).get(user) == data.get("winner_result"):
        total_pts += 8
    leaderboard_pre[user] = total_pts

sorted_leaderboard = sorted(leaderboard_pre.items(), key=lambda x: x[1], reverse=True)
max_points = sorted_leaderboard[0][1] if sorted_leaderboard else 1
if max_points == 0: max_points = 1  # Zabezpieczenie paska postępu przed błędem (dzielenie przez 0)

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- TAB 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    user_name = st.selectbox("Kim jesteś?", GRACZE)
    
    if user_name != "Wybierz swoje imię...":
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        if user_name not in data.get("jokers", {}): data.setdefault("jokers", {})[user_name] = []
        
        # --- MOTYWATOR ---
        st.markdown("---")
        if sorted_leaderboard:
            my_rank = next((i for i, v in enumerate(sorted_leaderboard) if v[0] == user_name), -1)
            my_pts = leaderboard_pre.get(user_name, 0)
            
            if my_rank == 0 and my_pts > 0:
                st.success(f"👑 **Cześć {user_name}!** Jesteś na szczycie z {my_pts} pkt! Uciekaj, bo gonią!")
            elif my_rank == 0 and my_pts == 0:
                st.success(f"👋 **Cześć {user_name}!** Turniej wystartował, walcz o pierwsze punkty!")
            elif my_rank > 0:
                leader_name, leader_pts = sorted_leaderboard[0]
                diff = leader_pts - my_pts
                if diff == 0:
    
