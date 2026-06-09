import streamlit as st
import requests
from datetime import datetime, timedelta

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
# Wklej swoje klucze pomiędzy cudzysłowy poniżej:
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

# --- BAZA MECZÓW Z DATAMI I GODZINAMI (Czas Warszawski - TVP Sport) ---
MATCHES = {
    "CKS vs Real madrit": {"date": "2026-06-09", "time": "21:00", "home": "CKS", "away": "Real madrit"}, 
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
    "Algieria vs Austria": {"date": "2026-06-28", "time": "04:00", "home": "Algieria", "away": "Austria"}
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

# --- NOWOCZESNE TŁO I WYGLĄD (CSS) ---
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(rgba(15, 32, 39, 0.85), rgba(32, 58, 67, 0.85)), url("https://images.unsplash.com/photo-1518605368461-1ee1252271b1?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 5px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("⚽ Rodzinny Typer Mundialowy")

# --- OBLICZANIE CZASU DLA POLSKI ---
# Chmura domyślnie działa w czasie UTC. Zwiększamy o 2h, aby dopasować do polskiego czasu letniego.
czas_polska = datetime.utcnow() + timedelta(hours=2)
dzisiaj_obj = czas_polska.date()
jutro_obj = dzisiaj_obj + timedelta(days=1)

st.write(f"📅 *Mecze dostępne na: **{dzisiaj_obj.strftime('%d.%m')}** oraz **{jutro_obj.strftime('%d.%m')}***")

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

with tab1:
    st.header("Oddaj swoje typy")
    st.info("💡 Pamiętaj: typowanie jest zablokowane od momentu rozpoczęcia meczu!")
    
    user_name = st.text_input("Kim jesteś? (Wpisz swoje imię):").strip()
    if user_name:
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            # Łączymy datę i godzinę meczu do precyzyjnego porównania
            match_datetime_obj = datetime.strptime(f"{match_info['date']} {match_info['time']}", "%Y-%m-%d %H:%M")
            
            if dzisiaj_obj <= match_date_obj <= jutro_obj:
                licznik_meczow += 1
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} ⏰ {match_info['time']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                
                current_bet = data["bets"][user_name].get(match_id, [0, 0])
                
                # BLOKADA CZASOWA
                if czas_polska < match_datetime_obj:
                    col1, col2 = st.columns(2)
                    with col1: score_home = st.number_input(f"Gole {match_info['home']}", 0, 20, int(current_bet[0]), key=f"bh_{match_id}_{user_name}")
                    with col2: score_away = st.number_input(f"Gole {match_info['away']}", 0, 20, int(current_bet[1]), key=f"ba_{match_id}_{user_name}")
                    data["bets"][user_name][match_id] = [score_home, score_away]
                else:
                    st.error("⏳ Mecz już się rozpoczął (lub zakończył). Typowanie zablokowane.")
                    st.info(f"Twój zapisany typ to: **{int(current_bet[0])} : {int(current_bet[1])}**")
                
        if licznik_meczow > 0:
            if st.button("Zapisz typy 💾"):
                save_data(data)
                st.success("Zapisano! Twoje typy są bezpieczne.")
        else:
            st.success("Aktualnie brak meczów do typowania na dziś i jutro!")

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

with tab3:
    st.header("⚙️ Wpisz wyniki (Admin)")
    if st.text_input("Hasło:", type="password") == "rodzina2026":
        for match_id, match_info in MATCHES.items():
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            
            if match_date_obj <= dzisiaj_obj:
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} ⏰ {match_info['time']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                
                current_res = data["results"].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Wynik {match_info['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Wynik {match_info['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
                data["results"][match_id] = [res_h, res_a]
                
        if st.button("Aktualizuj oficjalne wyniki 📣"):
            save_data(data)
            st.success("Oficjalne wyniki zapisane! Tabela została zaktualizowana.")
            
        # --- DODATKOWY PRZYCISK RESETU ---
        st.markdown("---")
        st.subheader("🚨 Strefa Awaryjna")
        if st.button("WYZERUJ CAŁY TURNIEJ (Usuń typy i wyniki) 🧹"):
            czyste_dane = {"results": {}, "bets": {}}
            save_data(czyste_dane)
            st.warning("Wszystkie dane zostały wymazane! Tabela jest czysta.")
            st.rerun()
