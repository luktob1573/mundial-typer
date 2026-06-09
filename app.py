import streamlit as st
import requests

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
# Te dane aplikacja sama bezpiecznie pobierze z "Advanced settings" w Streamlit Cloud
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/6a280281da38895dfe9ff2d4"
HEADERS = {
    "X-Master-Key": "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm",
    "Content-Type": "application/json"
}

# --- BAZA MECZÓW (Tutaj możesz wpisać realne mecze przed turniejem) ---
MATCHES = {
    "Mecz 1: Polska vs Argentyna": {"home": "Polska", "away": "Argentyna"},
    "Mecz 2: Brazylia vs Niemcy": {"home": "Brazylia", "away": "Niemcy"},
    "Mecz 3: Francja vs Włochy": {"home": "Francja", "away": "Włochy"}
}

# Funkcja do pobierania typów z internetowej bazy danych
def load_data():
    try:
        response = requests.get(URL, headers={"X-Master-Key": "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"})
        return response.json()["record"]
    except Exception:
        return {"results": {}, "bets": {}}

# Funkcja do zapisywania typów w internetowej bazie danych
def save_data(data):
    requests.put(URL, json=data, headers=HEADERS)

# Ładujemy aktualne dane na start aplikacji
data = load_data()

# Logika liczenia punktów (3 pkt za dokładny wynik, 1 pkt za trafienie zwycięzcy/remisu)
def calculate_points(bet_home, bet_away, res_home, res_away):
    if res_home is None or res_away is None: return 0
    if bet_home == res_home and bet_away == res_away: return 3
    if (bet_home > bet_away and res_home > res_away) or \
       (bet_home < bet_away and res_home < res_away) or \
       (bet_home == bet_away and res_home == res_away): return 1
    return 0

# Ustawienia wyglądu strony
st.set_page_config(page_title="Rodzinny Typer", page_icon="⚽", layout="centered")
st.title("⚽ Rodzinny Typer Mundialowy")

# Podział aplikacji na 3 zakładki
tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- ZAKŁADKA 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    user_name = st.text_input("Kim jesteś? (Wpisz swoje imię):").strip()
    if user_name:
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        for match_id, teams in MATCHES.items():
            st.markdown(f"### {match_id}")
            current_bet = data["bets"][user_name].get(match_id, [0, 0])
            col1, col2 = st.columns(2)
            with col1: score_home = st.number_input(f"Gole {teams['home']}", 0, 20, int(current_bet[0]), key=f"bh_{match_id}_{user_name}")
            with col2: score_away = st.number_input(f"Gole {teams['away']}", 0, 20, int(current_bet[1]), key=f"ba_{match_id}_{user_name}")
            data["bets"][user_name][match_id] = [score_home, score_away]
            
        if st.button("Zapisz typy 💾"):
            save_data(data)
            st.success("Zapisano! Twoje typy są bezpieczne. Możesz sprawdzić tabelę.")

# --- ZAKŁADKA 2: TABELA WYNIKÓW ---
with tab2:
    st.header("📊 Tabela Rodzinna")
    leaderboard = {}
    for user, bets in data["bets"].items():
        pts = sum(calculate_points(b[0], b[1], data["results"].get(m, [None])[0], data["results"].get(m, [None, None])[1]) for m, b in bets.items() if m in data["results"])
        leaderboard[user] = pts
        
    for idx, (player, pts) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True), 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🏃"
        st.markdown(f"#### {medal} {idx}. **{player}** — `{pts} pkt`")

# --- ZAKŁADKA 3: PANEL ADMINISTRATORA ---
with tab3:
    st.header("⚙️ Wpisz wyniki (Admin)")
    # Hasło chroniące przed przypadkową zmianą wyników przez innych domowników
    if st.text_input("Hasło:", type="password") == "rodzina2026":
        for match_id, teams in MATCHES.items():
            st.markdown(f"### {match_id}")
            current_res = data["results"].get(match_id, [0, 0])
            col1, col2 = st.columns(2)
            with col1: res_h = st.number_input(f"Wynik {teams['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
            with col2: res_a = st.number_input(f"Wynik {teams['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
            data["results"][match_id] = [res_h, res_a]
            
        if st.button("Aktualizuj oficjalne wyniki 📣"):
            save_data(data)
            st.success("Oficjalne wyniki zapisane! Tabela została automatycznie przeliczona.")
