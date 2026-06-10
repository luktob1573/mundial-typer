import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

# --- KONFIGURACJA CHMURY (JSONBin.io) ---
# Wklej swoje klucze pomiędzy cudzysłowy poniżej:
BIN_ID = "6a280281da38895dfe9ff2d4"
API_KEY = "$2a$10$uxF0zHyUt65VVUdDqrOA/uCLX1CqedIR3aQhj56qJ9pgSAnMzFyZm"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

# --- LISTA GRACZY ---
GRACZE = ["Wybierz swoje imię...", "Łukasz", "Natalia", "Lena", "Babcia", "Dziadek", "Gość"]

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
        if "long_term" not in record: record["long_term"] = {}
        if "winner_result" not in record: record["winner_result"] = ""
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

page_bg_img = """
<style>
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
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("⚽ Rodzinny Typer Mundialowy")

# --- CZAS W POLSCE ---
czas_polska = datetime.utcnow() + timedelta(hours=2)
dzisiaj_obj = czas_polska.date()
jutro_obj = dzisiaj_obj + timedelta(days=1)

st.write(f"📅 *Mecze dostępne na: **{dzisiaj_obj.strftime('%d.%m')}** oraz **{jutro_obj.strftime('%d.%m')}***")

tab1, tab2, tab3 = st.tabs(["🎯 Typuj", "🏆 Tabela", "⚙️ Admin"])

# --- TAB 1: TYPOWANIE ---
with tab1:
    st.header("Oddaj swoje typy")
    user_name = st.selectbox("Kim jesteś?", GRACZE)
    
    if user_name != "Wybierz swoje imię...":
        if user_name not in data["bets"]: data["bets"][user_name] = {}
        
        # --- TYP DŁUGOTERMINOWY ---
        st.markdown("---")
        st.subheader("🏆 Twój Mistrz Świata")
        start_turnieju = datetime(2026, 6, 11, 21, 0)
        lista_panstw = sorted(list(FLAGS.keys()))
        
        if czas_polska < start_turnieju:
            st.info("⏰ Masz czas do 11 czerwca do 21:00 na wytypowanie Mistrza Świata (+8 pkt na koniec!)")
            obecny_typ = data["long_term"].get(user_name, "Wybierz państwo...")
            idx = lista_panstw.index(obecny_typ) if obecny_typ in lista_panstw else 0
            wybrane_panstwo = st.selectbox("Kto wygra Mundial?", ["Wybierz państwo..."] + lista_panstw, index=idx, key=f"lt_{user_name}")
            if wybrane_panstwo != "Wybierz państwo...":
                data["long_term"][user_name] = wybrane_panstwo
        else:
            wybrany = data["long_term"].get(user_name, "Brak typu")
            st.warning(f"🔒 Typowanie zamknięte. Twój wybór to: **{wybrany}**")
            
        st.markdown("---")
        st.subheader("⚽ Bieżące mecze")
        
        licznik_meczow = 0
        for match_id, match_info in MATCHES.items():
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            match_datetime_obj = datetime.strptime(f"{match_info['date']} {match_info['time']}", "%Y-%m-%d %H:%M")
            
            if dzisiaj_obj <= match_date_obj <= jutro_obj:
                licznik_meczow += 1
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} ⏰ {match_info['time']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                current_bet = data["bets"][user_name].get(match_id, [0, 0])
                
                if czas_polska < match_datetime_obj:
                    col1, col2 = st.columns(2)
                    with col1: score_home = st.number_input(f"Gole {match_info['home']}", 0, 20, int(current_bet[0]), key=f"bh_{match_id}_{user_name}")
                    with col2: score_away = st.number_input(f"Gole {match_info['away']}", 0, 20, int(current_bet[1]), key=f"ba_{match_id}_{user_name}")
                    data["bets"][user_name][match_id] = [score_home, score_away]
                else:
                    # --- OPCJA 4: PODGLĄD TYPÓW NA ŻYWO ---
                    st.error("⏳ Mecz już się rozpoczął. Edycja zablokowana.")
                    st.markdown("**Typy rodziny na ten mecz:**")
                    for gracz, gracz_bets in data.get("bets", {}).items():
                        if match_id in gracz_bets:
                            g_bet = gracz_bets[match_id]
                            st.write(f"👤 **{gracz}**: `{int(g_bet[0])} : {int(g_bet[1])}`")
                
        if licznik_meczow > 0 and czas_polska < start_turnieju or any(datetime.strptime(f"{m['date']} {m['time']}", "%Y-%m-%d %H:%M") > czas_polska for m in MATCHES.values() if datetime.strptime(m["date"], "%Y-%m-%d").date() in [dzisiaj_obj, jutro_obj]):
            if st.button("Zapisz zmiany 💾"):
                save_data(data)
                st.success("Wszystko zapisane!")

# --- TAB 2: TABELA I STATYSTYKI ---
with tab2:
    st.header("🏆 Tabela Rodzinna")
    
    bets_data = data.get("bets", {})
    results_data = data.get("results", {})
    long_term_data = data.get("long_term", {})
    winner_result = data.get("winner_result", "")
    
    leaderboard = {}
    punkty_dzis = {}
    
    for user in bets_data.keys():
        leaderboard[user] = 0
        punkty_dzis[user] = 0
        
    # Liczenie punktów bieżących i dzisiejszych
    for user, user_bets in bets_data.items():
        total_pts = 0
        for match_id, bet in user_bets.items():
            if match_id in results_data:
                res = results_data[match_id]
                pts = calculate_points(bet[0], bet[1], res[0], res[1])
                total_pts += pts
                if MATCHES[match_id]["date"] == dzisiaj_obj.strftime("%Y-%m-%d"):
                    punkty_dzis[user] += pts
        
        # Dodanie bonusu +8 za długoterminowy typ
        if winner_result and long_term_data.get(user) == winner_result:
            total_pts += 8
            
        leaderboard[user] = total_pts
        
    # Wyświetlanie tabeli głównej
    for idx, (player, pts) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True), 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🏃"
        lt_info = f" (Typ: {long_term_data.get(player, 'brak')})" if long_term_data.get(player) else ""
        st.markdown(f"#### {medal} {idx}. **{player}** — `{pts} pkt` *{lt_info}*")
        
    # --- OPCJA 3: WYKRES FORMY ---
    sorted_match_ids = sorted(MATCHES.keys(), key=lambda m: f"{MATCHES[m]['date']} {MATCHES[m]['time']}")
    history_points = {"Mecz": ["Start"]}
    for user in bets_data.keys():
        history_points[user] = [0]
        
    for m_id in sorted_match_ids:
        if m_id in results_data:
            res = results_data[m_id]
            history_points["Mecz"].append(m_id.split(" vs ")[0] + "-" + m_id.split(" vs ")[1])
            for user in bets_data.keys():
                user_bets = bets_data[user]
                last_pts = history_points[user][-1]
                if m_id in user_bets:
                    pts_gained = calculate_points(user_bets[m_id][0], user_bets[m_id][1], res[0], res[1])
                    history_points[user].append(last_pts + pts_gained)
                else:
                    history_points[user].append(last_pts)
                    
    if len(history_points["Mecz"]) > 1:
        st.markdown("---")
        st.subheader("📈 Wykres Formy (Progresja Punktów)")
        df_chart = pd.DataFrame(history_points).set_index("Mecz")
        st.line_chart(df_chart)

    # --- OPCJA 1: TABLICA CHWAŁY I SZYDERSTWA ---
    if any(punkty_dzis.values()):
        st.markdown("---")
        st.subheader("🎭 Tablica Chwały i Szyderstwa (Wyniki z dziś)")
        max_pt = max(punkty_dzis.values())
        min_pt = min(punkty_dzis.values())
        
        najlepsi = [u for u, p in punkty_dzis.items() if p == max_pt and p > 0]
        najgorsi = [u for u, p in punkty_dzis.items() if p == min_pt]
        
        if najlepsi:
            st.success(f"🧠 **Znawca Kolejki (Dziś):** {', '.join(najlepsi)} (+{max_pt} pkt!)")
        if najgorsi and min_pt == 0:
            st.error(f"🪑 **Kanapowy Selekcjoner (Dziś - 0 pkt):** {', '.join(najgorsi)}")

# --- TAB 3: ADMIN ---
with tab3:
    st.header("⚙️ Panel Administratora")
    if st.text_input("Hasło:", type="password") == "rodzina2026":
        
        st.subheader("🏆 Wynik Długoterminowy (Na koniec turnieju)")
        obecny_mistrz = data.get("winner_result", "")
        idx_m = lista_panstw.index(obecny_mistrz) if obecny_mistrz in lista_panstw else 0
        oficjalny_mistrz = st.selectbox("Kto oficjalnie wygrał Mundial?", ["Turniej w trakcie..."] + lista_panstw, index=idx_m)
        data["winner_result"] = oficjalny_mistrz if oficjalny_mistrz != "Turniej w trakcie..." else ""
        
        st.subheader("⚽ Wpisz wyniki meczów")
        for match_id, match_info in MATCHES.items():
            match_date_obj = datetime.strptime(match_info["date"], "%Y-%m-%d").date()
            if match_date_obj <= dzisiaj_obj:
                flaga_h = FLAGS.get(match_info['home'], "🏳️")
                flaga_a = FLAGS.get(match_info['away'], "🏳️")
                
                st.markdown(f"### 📅 {match_info['date']} | {flaga_h} {match_info['home']} vs {match_info['away']} {flaga_a}")
                current_res = data["results"].get(match_id, [0, 0])
                col1, col2 = st.columns(2)
                with col1: res_h = st.number_input(f"Wynik {match_info['home']}", 0, 20, int(current_res[0]), key=f"rh_{match_id}")
                with col2: res_a = st.number_input(f"Wynik {match_info['away']}", 0, 20, int(current_res[1]), key=f"ra_{match_id}")
                data["results"][match_id] = [res_h, res_a]
                
        if st.button("Aktualizuj dane i wyniki 📣"):
            save_data(data)
            st.success("Dane zaktualizowane!")
            
        # --- GENERATOR PRZYPOMNIEŃ WHATSAPP (MECZE NA JUTRO) ---
        st.markdown("---")
        st.subheader("📱 Przypomnienie WhatsApp (Mecze na Jutro)")
        jutrzejsze_mecze = []
        for m_id, info in MATCHES.items():
            if datetime.strptime(info["date"], "%Y-%m-%d").date() == jutro_obj:
                jutrzejsze_mecze.append(f"🔸 {info['home']} vs {info['away']} (⏰ {info['time']})")
                
        if jutrzejsze_mecze:
            LINK_DO_APLIKACJI = "https://rodzinka.streamlit.app/" 
            tekst_wa = "⚽ Hej rodzinko! Można już typować JUTRZEJSZE mecze na Mundialu! Zobaczcie, co gramy jutro:\n\n"
            tekst_wa += "\n".join(jutrzejsze_mecze)
            tekst_wa += f"\n\nWarto obstawić już dzisiaj wieczorem, żeby nie przegapić porannych spotkań! ⏳\nLink do naszej apki: {LINK_DO_APLIKACJI}"
            
            import urllib.parse
            gotowy_link = f"https://wa.me/?text={urllib.parse.quote(tekst_wa)}"
            st.code(tekst_wa, language="text")
            st.markdown(f'<a href="{gotowy_link}" target="_blank"><button style="background-color:#25D366;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;font-weight:bold;width:100%;">Wyślij na WhatsApp 💬</button></a>', unsafe_allow_html=True)
        else:
            st.success("Jutro nie ma meczów.")
            
       # --- DWUETAPOWA STREFA AWARYJNA ---
        st.markdown("---")
        st.subheader("🚨 Strefa Awaryjna")
        st.error("Uwaga! Ta operacja jest nieodwracalna. Całkowicie usunie wszystkie typy domowników oraz wpisane wyniki.")
        
        # Etap 1: Pole potwierdzenia (Checkbox)
        zabezpieczenie = st.checkbox("Rozumiem konsekwencje. Odblokuj przycisk resetu.")
        
        # Etap 2: Właściwy przycisk (pojawia się tylko, gdy pole wyżej jest zaznaczone)
        if zabezpieczenie:
            if st.button("🔴 OSTATECZNIE WYZERUJ CAŁY TURNIEJ 🔴"):
                save_data({"results": {}, "bets": {}, "long_term": {}, "winner_result": ""})
                st.success("Wszystko zostało bezpowrotnie wyczyszczone. Tabela jest znów pusta!")
                st.rerun()
