import streamlit as st
import requests
from datetime import datetime

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
# Wklej swoje klucze pomiędzy cudzysłowy poniżej:
BIN_ID = "6a280281da38895dfe9ff2d4" 
API_KEY = "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm",
    "Content-Type": "application/json"
}

# --- BAZA MECZÓW Z DATAMI ---
# Ważne: Format daty musi wyglądać dokładnie tak: RRRR-MM-DD
MATCHES = {
    # Grupa A
    "Meksyk vs RPA": {"date": "2026-06-11", "home": "Meksyk", "away": "RPA"},
    "Korea Płd. vs Czechy": {"date": "2026-06-11", "home": "Korea Płd.", "away": "Czechy"},
    "Meksyk vs Korea Płd.": {"date": "2026-06-18", "home": "Meksyk", "away": "Korea Płd."},
    "Czechy vs RPA": {"date": "2026-06-18", "home": "Czechy", "away": "RPA"},
    "Czechy vs Meksyk": {"date": "2026-06-24", "home": "Czechy", "away": "Meksyk"},
    "RPA vs Korea Płd.": {"date": "2026-06-24", "home": "RPA", "away": "Korea Płd."},

    # Grupa B
    "Kanada vs Bośnia i Herc.": {"date": "2026-06-12", "home": "Kanada", "away": "Bośnia i Herc."},
    "Katar vs Szwajcaria": {"date": "2026-06-13", "home": "Katar", "away": "Szwajcaria"},
    "Kanada vs Katar": {"date": "2026-06-18", "home": "Kanada", "away": "Katar"},
    "Szwajcaria vs Bośnia i Herc.": {"date": "2026-06-18", "home": "Szwajcaria", "away": "Bośnia i Herc."},
    "Szwajcaria vs Kanada": {"date": "2026-06-24", "home": "Szwajcaria", "away": "Kanada"},
    "Bośnia i Herc. vs Katar": {"date": "2026-06-24", "home": "Bośnia i Herc.", "away": "Katar"},

    # Grupa C
    "Brazylia vs Maroko": {"date": "2026-06-13", "home": "Brazylia", "away": "Maroko"},
    "Haiti vs Szkocja": {"date": "2026-06-14", "home": "Haiti", "away": "Szkocja"},
    "Brazylia vs Haiti": {"date": "2026-06-19", "home": "Brazylia", "away": "Haiti"},
    "Szkocja vs Maroko": {"date": "2026-06-19", "home": "Szkocja", "away": "Maroko"},
    "Szkocja vs Brazylia": {"date": "2026-06-25", "home": "Szkocja", "away": "Brazylia"},
    "Maroko vs Haiti": {"date": "2026-06-25", "home": "Maroko", "away": "Haiti"},

    # Grupa D
    "USA vs Paragwaj": {"date": "2026-06-13", "home": "USA", "away": "Paragwaj"},
    "Australia vs Turcja": {"date": "2026-06-14", "home": "Australia", "away": "Turcja"},
    "USA vs Australia": {"date": "2026-06-19", "home": "USA", "away": "Australia"},
    "Turcja vs Paragwaj": {"date": "2026-06-19", "home": "Turcja", "away": "Paragwaj"},
    "Turcja vs USA": {"date": "2026-06-25", "home": "Turcja", "away": "USA"},
    "Paragwaj vs Australia": {"date": "2026-06-25", "home": "Paragwaj", "away": "Australia"},

    # Grupa E
    "Niemcy vs Curacao": {"date": "2026-06-14", "home": "Niemcy", "away": "Curacao"},
    "WKS vs Ekwador": {"date": "2026-06-15", "home": "WKS", "away": "Ekwador"},
    "Niemcy vs WKS": {"date": "2026-06-20", "home": "Niemcy", "away": "WKS"},
    "Ekwador vs Curacao": {"date": "2026-06-20", "home": "Ekwador", "away": "Curacao"},
    "Ekwador vs Niemcy": {"date": "2026-06-25", "home": "Ekwador", "away": "Niemcy"},
    "Curacao vs WKS": {"date": "2026-06-25", "home": "Curacao", "away": "WKS"},

    # Grupa F
    "Holandia vs Japonia": {"date": "2026-06-14", "home": "Holandia", "away": "Japonia"},
    "Szwecja vs Tunezja": {"date": "2026-06-15", "home": "Szwecja", "away": "Tunezja"},
    "Holandia vs Szwecja": {"date": "2026-06-20", "home": "Holandia", "away": "Szwecja"},
    "Tunezja vs Japonia": {"date": "2026-06-20", "home": "Tunezja", "away": "Japonia"},
    "Tunezja vs Holandia": {"date": "2026-06-26", "home": "Tunezja", "away": "Holandia"},
    "Japonia vs Szwecja": {"date": "2026-06-26", "home": "Japonia", "away": "Szwecja"},

    # Grupa G
    "Belgia vs Egipt": {"date": "2026-06-15", "home": "Belgia", "away": "Egipt"},
    "Iran vs Nowa Zelandia": {"date": "2026-06-16", "home": "Iran", "away": "Nowa Zelandia"},
    "Belgia vs Iran": {"date": "2026-06-21", "home": "Belgia", "away": "Iran"},
    "Nowa Zelandia vs Egipt": {"date": "2026-06-21", "home": "Nowa Zelandia", "away": "Egipt"},
    "Nowa Zelandia vs Belgia": {"date": "2026-06-26", "home": "Nowa Zelandia", "away": "Belgia"},
    "Egipt vs Iran": {"date": "2026-06-26", "home": "Egipt", "away": "Iran"},

    # Grupa H
    "Hiszpania vs Rep. Z. Przyl.": {"date": "2026-06-15", "home": "Hiszpania", "away": "Rep. Z. Przyl."},
    "Arabia Saud. vs Urugwaj": {"date": "2026-06-16", "home": "Arabia Saud.", "away": "Urugwaj"},
    "Hiszpania vs Arabia Saud.": {"date": "2026-06-21", "home": "Hiszpania", "away": "Arabia Saud."},
    "Urugwaj vs Rep. Z. Przyl.": {"date": "2026-06-21", "home": "Urugwaj", "away": "Rep. Z. Przyl."},
    "Urugwaj vs Hiszpania": {"date": "2026-06-27", "home": "Urugwaj", "away": "Hiszpania"},
    "Rep. Z. Przyl. vs Arabia Saud.": {"date": "2026-06-27", "home": "Rep. Z. Przyl.", "away": "Arabia Saud."},

    # Grupa I
    "Francja vs Senegal": {"date": "2026-06-16", "home": "Francja", "away": "Senegal"},
    "Irak vs Norwegia": {"date": "2026-06-17", "home": "Irak", "away": "Norwegia"},
    "Francja vs Irak": {"date": "2026-06-22", "home": "Francja", "away": "Irak"},
    "Norwegia vs Senegal": {"date": "2026-06-22", "home": "Norwegia", "away": "Senegal"},
    "Norwegia vs Francja": {"date": "2026-06-26", "home": "Norwegia", "away": "Francja"},
    "Senegal vs Irak": {"date": "2026-06-26", "home": "Senegal", "away": "Irak"},

    # Grupa J
    "Argentyna vs Algieria": {"date": "2026-06-17", "home": "Argentyna", "away": "Algieria"},
    "Austria vs Jordania": {"date": "2026-06-17", "home": "Austria", "away": "Jordania"},
    "Argentyna vs Austria": {"date": "2026-06-22", "home": "Argentyna", "away": "Austria"},
    "Jordania vs Algieria": {"date": "2026-06-22", "home": "Jordania", "away": "Algieria"},
    "Jordania vs Argentyna": {"date": "2026-06-27", "home": "Jordania", "away": "Argentyna"},
    "Algieria vs Austria": {"date": "2026-06-27", "home": "Algieria", "away": "Austria"},

    # Grupa K
    "Portugalia vs DR Konga": {"date": "2026-06-17", "home": "Portugalia", "away": "DR Konga"},
    "Uzbekistan vs Kolumbia": {"date": "2026-06-18", "home": "Uzbekistan", "away": "Kolumbia"},
    "Portugalia vs Uzbekistan": {"date": "2026-06-23", "home": "Portugalia", "away": "Uzbekistan"},
    "Kolumbia vs DR Konga": {"date": "2026-06-23", "home": "Kolumbia", "away": "DR Konga"},
    "Kolumbia vs Portugalia": {"date": "2026-06-28", "home": "Kolumbia", "away": "Portugalia"},
    "DR Konga vs Uzbekistan": {"date": "2026-06-28", "home": "DR Konga", "away": "Uzbekistan"},

    # Grupa L
    "Anglia vs Chorwacja": {"date": "2026-06-17", "home": "Anglia", "away": "Chorwacja"},
    "Ghana vs Panama": {"date": "2026-06-18", "home": "Ghana", "away": "Panama"},
    "Anglia vs Ghana": {"date": "2026-06-23", "home": "Anglia", "away": "Ghana"},
    "Panama vs Chorwacja": {"date": "2026-06-23", "home": "Panama", "away": "Chorwacja"},
    "Panama vs Anglia": {"date": "2026-06-28", "home": "Panama", "away": "Anglia"},
    "Chorwacja vs Ghana": {"date": "2026-06-28", "home": "Chorwacja", "away": "Ghana"}
}

def load_data():
    try:
        response = requests.get(URL, headers={"X-Master-Key": API_KEY})
        record = response.json().get("record", {})
        # BEZPIECZNIK: Upewniamy się, że struktura zawsze istnieje
        if "bets" not in record: record["bets"] = {}
        if "results" not in record: record["results"] = {}
        return record
    except Exception:
        return {"results": {}, "bets": {}}

def save_data(data):
    requests.put(URL, json=data, headers=HEADERS)

data = load_data()

def calculate_points(bet_home, bet_away, res_home, res_away):
    if res_home is None or res_away is None: return 0
    if bet_home == res_home and bet_away == res_away: return 3
    if (bet_home > bet_away and res_home > res_away) or \
       (bet_home < bet_away and res_home < res_away) or \
       (bet_home == bet_away and res_home == res_away): return 1
    return 0

st.set_page_config(page_title="Rodzinny Typer", page_icon="⚽", layout="centered")
st.title("⚽ Rodzinny Typer Mundialowy")

dzisiejsza_data = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 *Dzisiejsza data w systemie: **{dzisiejsza_data}***")

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- ZAKŁADKA 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    st.info("💡 Widzisz tylko mecze na dziś i kolejne dni.")
    
    user_name = st.text_input("Kim jesteś? (Wpisz swoje imię):").strip()
    if user_name:
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            if match_info["date"] >= dzisiejsza_data:
                licznik_meczow += 1
                st.markdown(f"### 📅 {match_info['date']} | {match_id}")
                current_bet = data["bets"][user_name].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: score_home = st.number_input(f"Gole {match_info['home']}", 0, 20, int(current_bet[0]), key=f"bh_{match_id}_{user_name}")
                with col2: score_away = st.number_input(f"Gole {match_info['away']}", 0, 20, int(current_bet[1]), key=f"ba_{match_id}_{user_name}")
                data["bets"][user_name][match_id] = [score_home, score_away]
                
        if licznik_meczow > 0:
            if st.button("Zapisz typy 💾"):
                save_data(data)
                st.success("Zapisano! Twoje typy są bezpieczne.")
        else:
            st.success("Brak meczów do typowania.")

# --- ZAKŁADKA 2: TABELA WYNIKÓW ---
with tab2:
    st.header("📊 Tabela Rodzinna")
    leaderboard = {}
    
    # Super-bezpieczne odczytywanie danych, które likwiduje KeyError
    bets_data = data.get("bets", {})
    results_data = data.get("results", {})
    
    for user, user_bets in bets_data.items():
        pts = 0
        for match_id, bet in user_bets.items():
            if match_id in results_data:
                res = results_data[match_id]
                if isinstance(res, list) and len(res) == 2 and isinstance(bet, list) and len(bet) == 2:
                    pts += calculate_points(bet[0], bet[1], res[0], res[1])
        leaderboard[user] = pts
        
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    if sorted_leaderboard:
        for idx, (player, pts) in enumerate(sorted_leaderboard, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🏃"
            st.markdown(f"#### {medal} {idx}. **{player}** — `{pts} pkt`")
    else:
        st.info("Brak punktów w tabeli. Oddajcie pierwsze typy!")

# --- ZAKŁADKA 3: PANEL ADMINA ---
with tab3:
    st.header("⚙️ Wpisz wyniki (Admin)")
    if st.text_input("Hasło:", type="password") == "rodzina2026":
        for match_id, match_info in MATCHES.items():
            if match_info["date"] <= dzisiejsza_data:
                st.markdown(f"### 📅 {match_info['date']} | {match_id}")
                current_res = data["results"].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Wynik {match_info['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Wynik {match_info['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
                data["results"][match_id] = [res_h, res_a]
                
        if st.button("Aktualizuj oficjalne wyniki 📣"):
            save_data(data)
            st.success("Oficjalne wyniki zapisane! Tabela została zaktualizowana.")
