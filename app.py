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
    "Meksyk vs Polska": {"date": "2026-06-11", "home": "Meksyk", "away": "Polska"},
    "USA vs Walia": {"date": "2026-06-12", "home": "USA", "away": "Walia"},
    "Argentyna vs Arabia": {"date": "2026-06-12", "home": "Argentyna", "away": "Arabia"},
    "Francja vs Dania": {"date": "2026-06-13", "home": "Francja", "away": "Dania"},
    "Hiszpania vs Portugalia": {"date": "2026-06-14", "home": "Hiszpania", "away": "Portugalia"}
}

def load_data():
    try:
        response = requests.get(URL, headers={"X-Master-Key": API_KEY})
        return response.json()["record"]
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

# --- AUTOMATYKA DAT ---
# Pobieramy dzisiejszą datę w formacie tekstowym, np. "2026-06-11"
dzisiejsza_data = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 *Dzisiejsza data w systemie: **{dzisiejsza_data}***")

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- ZAKŁADKA 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    st.info("💡 Poniżej widzisz tylko mecze na dziś i kolejne dni. Minione spotkania znikają automatycznie!")
    
    user_name = st.text_input("Kim jesteś? (Wpisz swoje imię):").strip()
    if user_name:
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            # Warunek: Pokaż mecz TYLKO jeśli jego data jest dzisiejsza lub w przyszłości
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
            st.success("Turniej się zakończył! Brak meczów do typowania.")

# --- ZAKŁADKA 2: TABELA ---
with tab2:
    st.header("📊 Tabela Rodzinna")
    leaderboard = {}
    for user, bets in data["bets"].items():
        pts = sum(calculate_points(b[0], b[1], data["results"].get(m, [None])[0], data["results"].get(m, [None, None])[1]) for m, b in bets.items() if m in data["results"])
        leaderboard[user] = pts
        
    for idx, (player, pts) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True), 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🏃"
        st.markdown(f"#### {medal} {idx}. **{player}** — `{pts} pkt`")

# --- ZAKŁADKA 3: ADMIN ---
with tab3:
    st.header("⚙️ Wpisz wyniki (Admin)")
    st.info("💡 Tutaj widzisz tylko mecze dzisiejsze oraz te, które już się zakończyły, abyś mógł wpisać wyniki.")
    
    if st.text_input("Hasło:", type="password") == "rodzina2026":
        for match_id, match_info in MATCHES.items():
            # Warunek: Pokaż mecz TYLKO jeśli jego data to dziś lub minęła
            if match_info["date"] <= dzisiejsza_data:
                st.markdown(f"### 📅 {match_info['date']} | {match_id}")
                current_res = data["results"].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Wynik {match_info['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Wynik {match_info['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
                data["results"][match_id] = [res_h, res_a]
                
        if st.button("Aktualizuj oficjalne wyniki 📣"):
            save_data(data)
            st.success("Oficjalne wyniki zapisane! Tabela została automatycznie przeliczona.")
