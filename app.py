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
    "Kolumbia vs Ghana": {"date": "2026-07-04", "time": "03:30", "home": "Kolumbia", "away": "Ghana"}
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
                    st.success(f"⚔️ **Cześć {user_name}!** Idziesz łeb w łeb z {leader_name}! Jeden dobry typ i odskakujesz!")
                else:
                    st.info(f"🚀 **Cześć {user_name}!** Masz {my_pts} pkt. Do lidera ({leader_name}) tracisz {diff} pkt.")

        # --- TYP DŁUGOTERMINOWY ---
        st.markdown("---")
        st.subheader("🏆 Mistrz Świata")
        start_turnieju = datetime(2026, 6, 11, 21, 0)
        
        if czas_polska < start_turnieju:
            st.info("⏰ Masz czas do 11 czerwca do 21:00 na wytypowanie.")
            obecny_typ = data["long_term"].get(user_name, "Wybierz państwo...")
            idx = lista_panstw.index(obecny_typ) if obecny_typ in lista_panstw else 0
            wybrane_panstwo = st.selectbox("Kto wygra Mundial?", ["Wybierz państwo..."] + lista_panstw, index=idx, key=f"lt_{user_name}")
            if wybrane_panstwo != "Wybierz państwo...":
                data["long_term"][user_name] = wybrane_panstwo
        else:
            wybrany = data["long_term"].get(user_name, "Brak typu")
            st.warning(f"🔒 Typowanie zamknięte. Twój wybór: **{wybrany}**")
            
        st.markdown("---")
        st.subheader("⚽ Bieżące mecze")
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            match_date_str = match_info["date"]
            match_date_obj = datetime.strptime(match_date_str, "%Y-%m-%d").date()
            match_datetime_obj = datetime.strptime(f"{match_date_str} {match_info['time']}", "%Y-%m-%d %H:%M")
            is_knockout = match_date_str >= "2026-06-28"
            
            if dzisiaj_obj <= match_date_obj <= jutro_obj:
                licznik_meczow += 1
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                # WYŚWIETLANIE JAKO PROFESJONALNA KARTA MECZOWA
                karta_html = f"""
                <div class="match-card">
                    <div class="match-header">📅 {match_info['date']} | ⏰ {match_info['time']}</div>
                    <div class="match-teams">
                        <div class="team team-left">{flaga_h} {match_info['home']}</div>
                        <div class="vs">VS</div>
                        <div class="team team-right">{match_info['away']} {flaga_a}</div>
                    </div>
                </div>
                """
                st.markdown(karta_html, unsafe_allow_html=True)
                
                current_bet = data["bets"][user_name].get(match_id, [0, 0, False])
                bet_h, bet_a = current_bet[0], current_bet[1]
                bet_pen = current_bet[2] if len(current_bet) > 2 else False
                
                if czas_polska < match_datetime_obj:
                    col1, col2 = st.columns(2)
                    with col1: score_home = st.number_input(f"Gole: {match_info['home']}", 0, 20, int(bet_h), key=f"bh_{match_id}_{user_name}")
                    with col2: score_away = st.number_input(f"Gole: {match_info['away']}", 0, 20, int(bet_a), key=f"ba_{match_id}_{user_name}")
                    
                    wants_penalties = False
                    if is_knockout:
                        wants_penalties = st.checkbox("🥅 Rzuty karne? (+1 pkt za trafienie z remisem)", value=bet_pen, key=f"pen_{match_id}_{user_name}")
                        if wants_penalties and score_home != score_away:
                            st.warning("⚠️ Punkty za karne otrzymasz TYLKO typując również remis.")
                    
                    data["bets"][user_name][match_id] = [score_home, score_away, wants_penalties]
                    
                    user_jokers = data["jokers"].get(user_name, [])
                    is_joker_active = match_id in user_jokers
                    jokers_used = len(user_jokers)
                    
                    if is_joker_active or jokers_used < 3:
                        zostalo = 3 - jokers_used if not is_joker_active else 3 - jokers_used + 1
                        joker_label = f"🃏 Użyj Jokera (Punkty x2! Zostało: {zostalo}/3)"
                        use_joker = st.checkbox(joker_label, value=is_joker_active, key=f"joker_{match_id}_{user_name}")
                        
                        if use_joker and not is_joker_active:
                            data["jokers"][user_name].append(match_id)
                        elif not use_joker and is_joker_active:
                            data["jokers"][user_name].remove(match_id)
                    else:
                        st.caption("🃏 Wykorzystałeś wszystkie 3 Jokery!")
                    st.markdown("<br>", unsafe_allow_html=True)
                        
                else:
                    if match_id in data.get("results", {}):
                        res = data["results"][match_id]
                        res_h, res_a = res[0], res[1]
                        res_pen = res[2] if len(res) > 2 else False
                        
                        wynik_str = f"🏁 WYNIK: {int(res_h)} : {int(res_a)}"
                        if res_pen: wynik_str += " (po karnych)"
                        st.success(wynik_str)
                    else:
                        st.error("⏳ Mecz w toku...")
                        
                    with st.expander("👀 Zobacz typy rodziny na ten mecz"):
                        for gracz in GRACZE[1:]:
                            gracz_bets = data.get("bets", {}).get(gracz, {})
                            if match_id in gracz_bets:
                                g_bet = gracz_bets[match_id]
                                g_bet_h, g_bet_a = g_bet[0], g_bet[1]
                                g_bet_pen = g_bet[2] if len(g_bet) > 2 else False
                                
                                ikonki = []
                                if match_id in data.get("jokers", {}).get(gracz, []): ikonki.append("🃏")
                                if g_bet_pen: ikonki.append("🥅")
                                ikonki_str = f" {' '.join(ikonki)}" if ikonki else ""
                                
                                st.write(f"👤 **{gracz}**: `{int(g_bet_h)} : {int(g_bet_a)}` {ikonki_str}")
                    st.markdown("<br>", unsafe_allow_html=True)
                
        if licznik_meczow > 0 and (czas_polska < start_turnieju or any(datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %H:%M") > czas_polska for m in MATCHES.values() if datetime.strptime(m["date"], "%Y-%m-%d").date() in [dzisiaj_obj, jutro_obj])):
            if st.button("Zapisz zmiany 💾", use_container_width=True):
                save_data(data)
                st.success("Wszystko zapisane!")

# --- TAB 2: TABELA I STATYSTYKI ---
with tab2:
    st.header("🏆 Tabela Rodzinna")
    
    # --- PODIUM ---
    if len(sorted_leaderboard) >= 3:
        p1, pts1 = sorted_leaderboard[0]
        p2, pts2 = sorted_leaderboard[1]
        p3, pts3 = sorted_leaderboard[2]
        
        seed1 = urllib.parse.quote(p1)
        seed2 = urllib.parse.quote(p2)
        seed3 = urllib.parse.quote(p3)

            # --- PODIUM ---
    if len(sorted_leaderboard) >= 3:
        p1, pts1 = sorted_leaderboard[0]
        p2, pts2 = sorted_leaderboard[1]
        p3, pts3 = sorted_leaderboard[2]
        
        # Logika płci (dodaj imiona żeńskie do tej listy)
        zenskie = ["Natalia", "Babcia Ania", "Karolina", "Ala", "Asia", "Babcia Asia", "Wiki"]
        
        def get_avatar_url(name):
            # Używamy różnych "seedów" dla kobiet i mężczyzn w stylu notionists
            prefix = "female" if name in zenske else "male"
            return f"https://api.dicebear.com/8.x/notionists/svg?seed={urllib.parse.quote(name)}&style=notionists&gender={prefix}"

        podium_html = f"""
        <div style="display: flex; justify-content: center; align-items: flex-end; gap: 20px; text-align: center; margin-bottom: 40px; margin-top: 20px;">
            <!-- Srebro -->
            <div style="margin-bottom: 10px;">
                <div style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #C0C0C0; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                    <img src="{get_avatar_url(p2)}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <p style="margin: 10px 0 0 0; font-size: 16px; color: #fff;"><b>🥈 {p2}</b></p>
                <p style="margin: 0; font-size: 14px; color: #ccc;">{pts2} pkt</p>
            </div>
            <!-- Złoto -->
            <div>
                <div style="width: 100px; height: 100px; border-radius: 50%; border: 4px solid #FFD700; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                    <img src="{get_avatar_url(p1)}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <p style="margin: 10px 0 0 0; font-size: 20px; color: #fff;"><b>🥇 {p1}</b></p>
                <p style="margin: 0; font-size: 16px; color: #FFD700;"><b>{pts1} pkt</b></p>
            </div>
            <!-- Brąz -->
            <div style="margin-bottom: 20px;">
                <div style="width: 70px; height: 70px; border-radius: 50%; border: 3px solid #CD7F32; background: #fff; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                    <img src="{get_avatar_url(p3)}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                <p style="margin: 10px 0 0 0; font-size: 15px; color: #fff;"><b>🥉 {p3}</b></p>
                <p style="margin: 0; font-size: 14px; color: #ccc;">{pts3} pkt</p>
            </div>
        </div>
        """
        st.markdown(podium_html, unsafe_allow_html=True)
        st.markdown("---")



        st.markdown(podium_html, unsafe_allow_html=True)
        st.markdown("---")
    
    punkty_dzis = {u: 0 for u in GRACZE[1:]}
    
    for user in GRACZE[1:]:
        user_bets = data.get("bets", {}).get(user, {})
        for match_id, bet in user_bets.items():
            if match_id in data.get("results", {}):
                bet_h, bet_a = bet[0], bet[1]
                bet_pen = bet[2] if len(bet) > 2 else False
                
                res = data["results"][match_id]
                res_h, res_a = res[0], res[1]
                res_pen = res[2] if len(res) > 2 else False
                
                pts = calculate_points(bet_h, bet_a, res_h, res_a, bet_pen, res_pen)
                if match_id in data.get("jokers", {}).get(user, []):
                    pts *= 2
                if MATCHES[match_id]["date"] == dzisiaj_obj.strftime("%Y-%m-%d"):
                    punkty_dzis[user] += pts
        
    for idx, (player, pts) in enumerate(sorted_leaderboard, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        lt_info = f" | 🏆 Typ: {data.get('long_term', {}).get(player, 'brak')}" if data.get("long_term", {}).get(player) else ""
        jokers_left = 3 - len(data.get("jokers", {}).get(player, []))
        odznaki = "".join(user_badges[player])
        
        # Pasek postępu pod każdym graczem
        postep = pts / max_points
        
        st.markdown(f"##### {medal} {player} {odznaki} ➔ {pts} pkt <span style='font-size: 13px; color: #aaa; font-weight: normal;'>(Jokery: {jokers_left}/3 {lt_info})</span>", unsafe_allow_html=True)
        st.progress(postep)
        
    with st.expander("ℹ️ Co oznaczają odznaki w tabeli?"):
        st.markdown("""
        * 🤡 **Pechowiec:** Użył Jokera, ale zgarnął okrągłe 0 pkt.
        * 🤝 **Król Remisów:** Wytypował min. 5 remisów w turnieju.
        * 🛡️ **Ekspert Defensywy:** Wytypował min. 3 razy wynik 0:0.
        """)
        
    # --- WYKRES FORMY ---
    sorted_match_ids = sorted(MATCHES.keys(), key=lambda m: f"{MATCHES[m]['date']} {MATCHES[m]['time']}")
    history_points = {"Mecz": ["Start"]}
    for user in GRACZE[1:]: history_points[user] = [0]
        
    for m_id in sorted_match_ids:
        if m_id in data.get("results", {}):
            res = data["results"][m_id]
            res_h, res_a, res_pen = res[0], res[1], res[2] if len(res) > 2 else False
            history_points["Mecz"].append(m_id.split(" vs ")[0] + "-" + m_id.split(" vs ")[1])
            
            for user in GRACZE[1:]:
                user_bets = data.get("bets", {}).get(user, {})
                last_pts = history_points[user][-1]
                if m_id in user_bets:
                    bet = user_bets[m_id]
                    bet_h, bet_a, bet_pen = bet[0], bet[1], bet[2] if len(bet) > 2 else False
                    pts_gained = calculate_points(bet_h, bet_a, res_h, res_a, bet_pen, res_pen)
                    if m_id in data.get("jokers", {}).get(user, []): pts_gained *= 2
                    history_points[user].append(last_pts + pts_gained)
                else:
                    history_points[user].append(last_pts)
                    
    if len(history_points["Mecz"]) > 1:
        st.markdown("---")
        st.subheader("📈 Wykres Formy")
        df_chart = pd.DataFrame(history_points).set_index("Mecz")
        st.line_chart(df_chart)

    if any(punkty_dzis.values()):
        st.markdown("---")
        st.subheader("🎭 Podsumowanie Dnia")
        max_pt = max(punkty_dzis.values())
        min_pt = min(punkty_dzis.values())
        najlepsi = [u for u, p in punkty_dzis.items() if p == max_pt and p > 0]
        najgorsi = [u for u, p in punkty_dzis.items() if p == min_pt]
        
        # ZMIENIONE NAZWY ZGODNIE Z PROŚBĄ:
        if najlepsi: st.success(f"🧠 **Znawca Kolejki:** {', '.join(najlepsi)} (+{max_pt} pkt!)")
        if najgorsi and min_pt == 0: st.error(f"🪑 **Kanapowy Selekcjoner (0 pkt):** {', '.join(najgorsi)}")

# --- TAB 3: ADMIN ---
with tab3:
    st.header("⚙️ Panel Administratora")
    if st.text_input("Hasło:", type="password") == "1111":
        
        st.subheader("🏆 Mistrz Świata (Oficjalnie)")
        obecny_mistrz = data.get("winner_result", "")
        idx_m = lista_panstw.index(obecny_mistrz) if obecny_mistrz in lista_panstw else 0
        oficjalny_mistrz = st.selectbox("Kto wygrał turniej?", ["Trwa..."] + lista_panstw, index=idx_m)
        data["winner_result"] = oficjalny_mistrz if oficjalny_mistrz != "Trwa..." else ""
        
        st.markdown("---")
        st.subheader("⚽ Wpisz wyniki meczów")
        
        mecze_do_wpisania = []
        mecze_wpisane = []
        
        for match_id, match_info in MATCHES.items():
            match_datetime_obj = datetime.strptime(f"{match_info['date']} {match_info['time']}", "%Y-%m-%d %H:%M")
            if czas_polska >= match_datetime_obj + timedelta(hours=2):
                if match_id in data.get("results", {}): mecze_wpisane.append(match_id)
                else: mecze_do_wpisania.append(match_id)
        
        nowe_wyniki = {}
        edytowane_wyniki = {}
        
        if mecze_do_wpisania:
            st.info("🔴 Oczekujące na wynik. Zaznacz 'Zatwierdź', aby zapisać.")
            for match_id in mecze_do_wpisania:
                match_info = MATCHES[match_id]
                is_knockout = match_info["date"] >= "2026-06-28"
                flaga_h, flaga_a = FLAGS.get(match_info['home'], "🏳️"), FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"**{flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}**")
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Gole: {match_info['home']}", 0, 20, 0, key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Gole: {match_info['away']}", 0, 20, 0, key=f"ra_{match_id}")
                
                was_penalty = False
                if is_knockout: was_penalty = st.checkbox("Mecz zakończył się rzutami karnymi?", key=f"adm_pen_{match_id}")
                
                if st.checkbox("Zatwierdź Wynik ✅", key=f"gotowe_{match_id}"):
                    nowe_wyniki[match_id] = [res_h, res_a, was_penalty]
                st.markdown("---")
        else:
            st.success("Wszystkie zakończone mecze mają wpisane wyniki!")

        if mecze_wpisane:
            with st.expander("✅ Wpisane mecze (Kliknij, aby edytować)"):
                for match_id in reversed(mecze_wpisane):
                    match_info = MATCHES[match_id]
                    c_res = data["results"][match_id]
                    c_res_pen = c_res[2] if len(c_res) > 2 else False
                    is_knockout = match_info["date"] >= "2026-06-28"
                    flaga_h, flaga_a = FLAGS.get(match_info['home'], "🏳️"), FLAGS.get(match_info['away'], "🏳️")
                    
                    st.markdown(f"**{flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}**")
                    col1, col2 = st.columns(2)
                    with col1: res_h = st.number_input(f"Gole: {match_info['home']}", 0, 20, int(c_res[0]), key=f"edit_h_{match_id}")
                    with col2: res_a = st.number_input(f"Gole: {match_info['away']}", 0, 20, int(c_res[1]), key=f"edit_a_{match_id}")
                    
                    was_penalty = c_res_pen
                    if is_knockout: was_penalty = st.checkbox("Rzuty karne?", value=c_res_pen, key=f"edit_pen_{match_id}")
                    edytowane_wyniki[match_id] = [res_h, res_a, was_penalty]

        if mecze_do_wpisania or mecze_wpisane:
            if st.button("Zapisz wyniki 📣", use_container_width=True):
                for m_id, res in nowe_wyniki.items(): data["results"][m_id] = res
                for m_id, res in edytowane_wyniki.items(): data["results"][m_id] = res
                save_data(data)
                st.success("Wyniki zaktualizowane!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("📱 Przypomnienie WhatsApp (Jutro)")
        jutrzejsze_mecze = [f"🔸 {info['home']} vs {info['away']} (⏰ {info['time']})" for m_id, info in MATCHES.items() if datetime.strptime(info["date"], "%Y-%m-%d").date() == jutro_obj]
                
        if jutrzejsze_mecze:
            LINK_DO_APLIKACJI = "https://rodzinka.streamlit.app/" 
            tekst_wa = "⚽ Hej rodzinko! Przypominam o typowaniu JUTRZEJSZYCH meczów! W fazie pucharowej łapiemy dodatkowe punkty za karne (pamiętajcie: karne wchodzą tylko z remisem!). 🥅 Zobaczcie co gramy:\n\n" + "\n".join(jutrzejsze_mecze) + f"\n\nNie przegapcie! ⏳\nLink do naszej apki: {LINK_DO_APLIKACJI}"
            gotowy_link = f"https://wa.me/?text={urllib.parse.quote(tekst_wa)}"
            st.code(tekst_wa, language="text")
            st.markdown(f'<a href="{gotowy_link}" target="_blank"><button style="background-color:#25D366;color:white;border:none;padding:10px 20px;border-radius:20px;cursor:pointer;font-weight:bold;width:100%;text-transform:uppercase;">Wyślij przypomnienie na WhatsApp 💬</button></a>', unsafe_allow_html=True)
        else:
            st.success("Jutro nie ma meczów.")
            
        st.markdown("---")
        st.subheader("💾 Backup / Awaryjne Kasowanie")
        st.download_button("Pobierz kopię JSON 📥", data=json.dumps(data, indent=4), file_name=f"backup_{dzisiaj_obj.strftime('%Y-%m-%d')}.json")
        if st.checkbox("Odblokuj reset turnieju"):
            if st.button("🔴 WYZERUJ WSZYSTKO 🔴"):
                save_data({"results": {}, "bets": {}, "long_term": {}, "winner_result": "", "jokers": {}})
                st.success("Zresetowano!")
                st.rerun()
