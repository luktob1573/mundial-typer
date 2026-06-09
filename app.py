inport srteamlit as st
import requests
from datetime import datetime,
BIN_ID = "6a280281da38895dfe9ff2d4"
API_KEY = "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

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

# --- BAZA MECZÓW Z DATAMI ---
MATCHES = {
     "cks vs real madryt": {"date": "2026-06-10", "home": "cks", "away": "real madryt"},
    "Meksyk vs RPA": {"date": "2026-06-11", "home": "Meksyk", "away": "RPA"},
    "Korea Płd. vs Czechy": {"date": "2026-06-11", "home": "Korea Płd.", "away": "Czechy"},
    "Meksyk vs Korea Płd.": {"date": "2026-06-18", "home": "Meksyk", "away": "Korea Płd."},
    "Czechy vs RPA": {"date": "2026-06-18", "home": "Czechy", "away": "RPA"},
    "Czechy vs Meksyk": {"date": "2026-06-24", "home": "Czechy", "away": "Meksyk"},
    "RPA vs Korea Płd.": {"date": "2026-06-24", "home": "RPA", "away": "Korea Płd."},
    "Kanada vs Bośnia i Herc.": {"date": "2026-06-12", "home": "Kanada", "away": "Bośnia i Herc."},
    "Katar vs Szwajcaria": {"date": "2026-06-13", "home": "Katar", "away": "Szwajcaria"},
    "Kanada vs Katar": {"date": "2026-06-18", "home": "Kanada", "away": "Katar"},
    "Szwajcaria vs Bośnia i Herc.": {"date": "2026-06-18", "home": "Szwajcaria", "away": "Bośnia i Herc."},
    "Szwajcaria vs Kanada": {"date": "2026-06-24", "home": "Szwajcaria", "away": "Kanada"},
    "Bośnia i Herc. vs Katar": {"date": "2026-06-24", "home": "Bośnia i Herc.", "away": "Katar"},
    "Brazylia vs Maroko": {"date": "2026-06-13", "home": "Brazylia", "away": "Maroko"},
    "Haiti vs Szkocja": {"date": "2026-06-14", "home": "Haiti", "away": "Szkocja"},
    "Brazylia vs Haiti": {"date": "2026-06-19", "home": "Brazylia", "away": "Haiti"},
    "Szkocja vs Maroko": {"date": "2026-06-19", "home": "Szkocja", "away": "Maroko"},
    "Szkocja vs Brazylia": {"date": "2026-06-25", "home": "Szkocja", "away": "Brazylia"},
    "Maroko vs Haiti": {"date": "2026-06-25", "home": "Maroko", "away": "Haiti"},
    "USA vs Paragwaj": {"date": "2026-06-13", "home": "USA", "away": "Paragwaj"},
    "Australia vs Turcja": {"date": "2026-06-14", "home": "Australia", "away": "Turcja"},
    "USA vs Australia": {"date": "2026-06-19", "home": "USA", "away": "Australia"},
    "Turcja vs Paragwaj": {"date": "2026-06-19", "home": "Turcja", "away": "Paragwaj"},
    "Turcja vs USA": {"date": "2026-06-25", "home": "Turcja", "away": "USA"},
    "Paragwaj vs Australia": {"date": "2026-06-25", "home": "Paragwaj", "away": "Australia"},
    "Niemcy vs Curacao": {"date": "2026-06-14", "home": "Niemcy", "away": "Curacao"},
    "WKS vs Ekwador": {"date": "2026-06-15", "home": "WKS", "away": "Ekwador"},
    "Niemcy vs WKS": {"date": "2026-06-20", "home": "Niemcy", "away": "WKS"},
    "Ekwador vs Curacao": {"date": "2026-06-20", "home": "Ekwador", "away": "Curacao"},
    "Ekwador vs Niemcy": {"date": "2026-06-25", "home": "Ekwador", "away": "Niemcy"},
    "Curacao vs WKS": {"date": "2026-06-25", "home": "Curacao", "away": "WKS"},
    "Holandia vs Japonia": {"date": "2026-06-14", "home": "Holandia", "away": "Japonia"},
    "Szwecja vs Tunezja": {"date": "2026-06-15", "home": "Szwecja", "away": "Tunezja"},
    "Holandia vs Szwecja": {"date": "2026-06-20", "home": "Holandia", "away": "Szwecja"},
    "Tunezja vs Japonia": {"date": "2026-06-20", "home": "Tunezja", "away": "Japonia"},
    "Tunezja vs Holandia": {"date": "2026-06-26", "home": "Tunezja", "away": "Holandia"},
    "Japonia vs Szwecja": {"date": "2026-06-26", "home": "Japonia", "away": "Szwecja"},
    "Belgia vs Egipt": {"date": "2026-06-15", "home": "Belgia", "away": "Egipt"},
    "Iran vs Nowa Zelandia": {"date": "2026-06-16", "home": "Iran", "away": "Nowa Zelandia"},
    "Belgia vs Iran": {"date": "2026-06-21", "home": "Belgia", "away": "Iran"},
    "Nowa Zelandia vs Egipt": {"date": "2026-06-21", "home": "Nowa Zelandia", "away": "Egipt"},
    "Nowa Zelandia vs Belgia": {"date": "2026-06-26", "home": "Nowa Zelandia", "away": "Belgia"},
    "Egipt vs Iran": {"date": "2026-06-26", "home": "Egipt", "away": "Iran"},
    "Hiszpania vs Rep. Z. Przyl.": {"date": "2026-06-15", "home": "Hiszpania", "away": "Rep. Z. Przyl."},
    "Arabia Saud. vs Urugwaj": {"date": "2026-06-16", "home": "Arabia Saud.", "away": "Urugwaj"},
    "Hiszpania vs Arabia Saud.": {"date": "2026-06-21", "home": "Hiszpania", "away": "Arabia Saud."},
    "Urugwaj vs Rep. Z. Przyl.": {"date": "2026-06-21", "home": "Urugwaj", "away": "Rep. Z. Przyl."},
    "Urugwaj vs Hiszpania": {"date": "2026-06-27", "home": "Urugwaj", "away": "Hiszpania"},
    "Rep. Z. Przyl. vs Arabia Saud.": {"date": "2026-06-27", "home": "Rep. Z. Przyl.", "away": "Arabia Saud."},
    "Francja vs Senegal": {"date": "2026-06-16", "home": "Francja", "away": "Senegal"},
    "Irak vs Norwegia": {"date": "2026-06-17", "home": "Irak", "away": "Norwegia"},
    "Francja vs Irak": {"date": "2026-06-22", "home": "Francja", "away": "Irak"},
    "Norwegia vs Senegal": {"date": "2026-06-22", "home": "Norwegia", "away": "Senegal"},
    "Norwegia vs Francja": {"date": "2026-06-26", "home": "Norwegia", "away": "Francja"},
    "Senegal vs Irak": {"date": "2026-06-26", "home": "Senegal", "away": "Irak"},
    "Argentyna vs Algieria": {"date": "2026-06-17", "home": "Argentyna", "away": "Algieria"},
    "Austria vs Jordania": {"date": "2026-06-17", "home": "Austria", "away": "Jordania"},
    "Argentyna vs Austria": {"date": "2026-06-22", "home": "Argentyna", "away": "Austria"},
    "Jordania vs Algieria": {"date": "2026-06-22", "home": "Jordania", "away": "Algieria"},
    "Jordania vs Argentyna": {"date": "2026-06-27", "home": "Jordania", "away": "Argentyna"},
    "Algieria vs Austria": {"date": "2026-06-27", "home": "Algieria", "away": "Austria"},
    "Portugalia vs DR Konga": {"date": "2026-06-17", "home": "Portugalia", "away": "DR Konga"},
    "Uzbekistan vs Kolumbia": {"date": "2026-06-18", "home": "Uzbekistan", "away": "Kolumbia"},
    "Portugalia vs Uzbekistan": {"date": "2026-06-23", "home": "Portugalia", "away": "Uzbekistan"},
    "Kolumbia vs DR Konga": {"date": "2026-06-23", "home": "Kolumbia", "away": "DR Konga"},
    "Kolumbia vs Portugalia": {"date": "2026-06-28", "home": "Kolumbia", "away": "Portugalia"},
    "DR Konga vs Uzbekistan": {"date": "2026-06-28", "home": "DR Konga", "away": "Uzbekistan"},
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

# --- OBLICZANIE DAT (Dziś i Jutro) ---
dzisiaj_obj = datetime.now().date()
jutro_obj = dzisiaj_obj + timedelta(days=1)

st.write(f"📅 *Mecze dostępne na: **{dzisiaj_obj.strftime('%d.%m')}** oraz **{jutro_obj.strftime('%d.%m')}***")

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- ZAKŁADKA 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    st.info("💡 Widzisz tutaj wyłącznie mecze, które odbywają się dzisiaj i jutro.")
    
    user_name = st.text_input("Kim jesteś? (Wpisz swoje imię):").strip()
    if user_name:
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            # Zmiana: Parowanie daty meczu
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            
            # Warunek: Pokaż tylko jeśli data meczu to dzisiaj LUB jutro
            if dzisiaj_obj <= match_date_obj <= jutro_obj:
                licznik_meczow += 1
                
                # Pobieranie flag
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                
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
            st.success("Aktualnie brak meczów do typowania na dziś i jutro!")

# --- ZAKŁADKA 2: TABELA WYNIKÓW ---
with tab2:
    st.header("📊 Tabela Rodzinna")
    leaderboard = {}
    
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
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            
            # W panelu admina pokazujemy mecze od dzisiaj w dół (minione)
            if match_date_obj <= dzisiaj_obj:
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                
                current_res = data["results"].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Wynik {match_info['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Wynik {match_info['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
                data["results"][match_id] = [res_h, res_a]
                
        if st.button("Aktualizuj oficjalne wyniki 📣"):
            save_data(data)
            st.success("Oficjalne wyniki zapisane! Tabela została zaktualizowana.")
