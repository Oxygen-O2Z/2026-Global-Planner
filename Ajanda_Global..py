import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# --- 1. Dil Sözlüğü (Translations) ---
LANGUAGES = {
    "Türkçe (TR)": {
        "title": "📔 2026 Mobil Ajanda",
        "tab1": "📅 Günlük Akış",
        "tab2": "🎯 Aylık Hedefler",
        "tab3": "📊 Analiz",
        "how_feel": "Bugün Nasıl Hissediyorsun?",
        "date_sel": "Tarih Seç:",
        "mood_sel": "Modunu Seç:",
        "note_title": "Günün Notu",
        "note_ph": "Bugün neler oldu? Yarına notun ne?",
        "save_btn": "💾 Günlüğü Kaydet",
        "save_success": "Günlük başarıyla kaydedildi!",
        "month_sel": "Ay Seçiniz:",
        "goal_header": "Hedefleri",
        "new_goal": "Yeni Hedef Ekle",
        "add_btn": "Ekle",
        "no_goal": "Bu ay için henüz hedef yok.",
        "progress": "Tamamlanma Oranı:",
        "analysis_header": "📊 Duygu Durumu Özeti",
        "last_30": "Son 30 günün özeti:",
        "no_data": "Henüz veri girişi yapılmamış.",
        "months": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"],
        "moods": ["Harika 🤩", "İyi 🙂", "Nötr 😐", "Yorgun 😴", "Üzgün 😔", "Stresli 😫"]
    },
    "English (EN)": {
        "title": "📔 2026 Pocket Planner",
        "tab1": "📅 Daily Flow",
        "tab2": "🎯 Monthly Goals",
        "tab3": "📊 Analysis",
        "how_feel": "How do you feel today?",
        "date_sel": "Select Date:",
        "mood_sel": "Select Mood:",
        "note_title": "Daily Note",
        "note_ph": "What happened today? Notes for tomorrow?",
        "save_btn": "💾 Save Entry",
        "save_success": "Entry saved successfully!",
        "month_sel": "Select Month:",
        "goal_header": "Goals for",
        "new_goal": "Add New Goal",
        "add_btn": "Add",
        "no_goal": "No goals set for this month yet.",
        "progress": "Completion Rate:",
        "analysis_header": "📊 Mood Summary",
        "last_30": "Summary of last 30 days:",
        "no_data": "No data entered yet.",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "moods": ["Great 🤩", "Good 🙂", "Neutral 😐", "Tired 😴", "Sad 😔", "Stressed 😫"]
    },
    "Deutsch (DE)": {
        "title": "📔 2026 Taschenplaner",
        "tab1": "📅 Täglicher Ablauf",
        "tab2": "🎯 Monatsziele",
        "tab3": "📊 Analyse",
        "how_feel": "Wie fühlst du dich heute?",
        "date_sel": "Datum wählen:",
        "mood_sel": "Stimmung wählen:",
        "note_title": "Tagesnotiz",
        "note_ph": "Was ist heute passiert?",
        "save_btn": "💾 Speichern",
        "save_success": "Erfolgreich gespeichert!",
        "month_sel": "Monat wählen:",
        "goal_header": "Ziele für",
        "new_goal": "Neues Ziel hinzufügen",
        "add_btn": "Hinzufügen",
        "no_goal": "Noch keine Ziele für diesen Monat.",
        "progress": "Abschlussquote:",
        "analysis_header": "📊 Stimmungsübersicht",
        "last_30": "Zusammenfassung der letzten 30 Tage:",
        "no_data": "Noch keine Daten eingegeben.",
        "months": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
        "moods": ["Super 🤩", "Gut 🙂", "Neutral 😐", "Müde 😴", "Traurig 😔", "Gestresst 😫"]
    },
    "Français (FR)": {
        "title": "📔 Agenda 2026",
        "tab1": "📅 Flux Quotidien",
        "tab2": "🎯 Objectifs Mensuels",
        "tab3": "📊 Analyse",
        "how_feel": "Comment vous sentez-vous ?",
        "date_sel": "Choisir une date :",
        "mood_sel": "Humeur :",
        "note_title": "Note du jour",
        "note_ph": "Que s'est-il passé aujourd'hui ?",
        "save_btn": "💾 Enregistrer",
        "save_success": "Enregistré avec succès !",
        "month_sel": "Choisir le mois :",
        "goal_header": "Objectifs de",
        "new_goal": "Ajouter un objectif",
        "add_btn": "Ajouter",
        "no_goal": "Pas encore d'objectifs.",
        "progress": "Taux d'achèvement :",
        "analysis_header": "📊 Résumé de l'humeur",
        "last_30": "Résumé des 30 derniers jours :",
        "no_data": "Aucune donnée saisie.",
        "months": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        "moods": ["Génial 🤩", "Bien 🙂", "Neutre 😐", "Fatigué 😴", "Triste 😔", "Stressé 😫"]
    },
    "Español (ES)": {
        "title": "📔 Agenda 2026",
        "tab1": "📅 Flujo Diario",
        "tab2": "🎯 Objetivos Mensuales",
        "tab3": "📊 Análisis",
        "how_feel": "¿Cómo te sientes hoy?",
        "date_sel": "Seleccionar fecha:",
        "mood_sel": "Seleccionar estado de ánimo:",
        "note_title": "Nota del día",
        "note_ph": "¿Qué pasó hoy?",
        "save_btn": "💾 Guardar",
        "save_success": "¡Guardado con éxito!",
        "month_sel": "Seleccionar mes:",
        "goal_header": "Objetivos de",
        "new_goal": "Añadir nuevo objetivo",
        "add_btn": "Añadir",
        "no_goal": "Aún no hay objetivos.",
        "progress": "Tasa de finalización:",
        "analysis_header": "📊 Resumen de estado de ánimo",
        "last_30": "Resumen de los últimos 30 días:",
        "no_data": "Aún no hay datos.",
        "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        "moods": ["Genial 🤩", "Bien 🙂", "Neutral 😐", "Cansado 😴", "Triste 😔", "Estresado 😫"]
    }
}

# --- Veritabanı ---
def init_db():
    conn = sqlite3.connect('2026_ajanda_global.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hedefler (id INTEGER PRIMARY KEY, ay TEXT, hedef TEXT, durum INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS gunluk (tarih TEXT PRIMARY KEY, mood TEXT, notlar TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('2026_ajanda_global.db')

# --- Sayfa Ayarları ---
st.set_page_config(page_title="2026 Planner", page_icon="🌍", layout="centered")
init_db()

# --- Dil Seçimi (Sidebar) ---
with st.sidebar:
    st.header("Language / Dil")
    selected_lang_key = st.selectbox("Select Language", list(LANGUAGES.keys()))
    L = LANGUAGES[selected_lang_key] # Seçilen dilin sözlüğünü 'L' değişkenine ata

st.title(L["title"])

tab1, tab2, tab3 = st.tabs([L["tab1"], L["tab2"], L["tab3"]])

# ================= TAB 1: GÜNLÜK =================
with tab1:
    st.header(L["how_feel"])
    secilen_tarih = st.date_input(L["date_sel"], date.today())
    tarih_str = secilen_tarih.strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM gunluk WHERE tarih=?", (tarih_str,))
    kayit = c.fetchone()
    conn.close()
    
    # Mood listesini seçilen dile göre al
    mood_listesi = L["moods"]
    # Veritabanından gelen mood'un indexini bul (Eğer dil değişirse index kayabilir, basit çözüm olarak varsayılanı kullanıyoruz)
    saved_mood = kayit[1] if kayit else mood_listesi[2]
    # Eğer veritabanındaki mood listede yoksa (dil değiştiği için), nötr seç
    current_index = mood_listesi.index(saved_mood) if saved_mood in mood_listesi else 2
    
    yeni_mood = st.selectbox(L["mood_sel"], mood_listesi, index=current_index)
    
    st.subheader(L["note_title"])
    mevcut_not = kayit[2] if kayit else ""
    yeni_not = st.text_area(L["note_ph"], value=mevcut_not, height=150)
    
    if st.button(L["save_btn"], use_container_width=True):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO gunluk (tarih, mood, notlar) VALUES (?, ?, ?)", (tarih_str, yeni_mood, yeni_not))
        conn.commit()
        conn.close()
        st.success(L["save_success"])

# ================= TAB 2: HEDEFLER =================
with tab2:
    aylar_listesi = L["months"]
    # Ay ismini İngilizce veritabanında tutmak yerine index kullanmak daha global olur ama basitlik için metin tutuyoruz.
    secilen_ay_index = st.selectbox(L["month_sel"], range(len(aylar_listesi)), format_func=lambda x: aylar_listesi[x])
    secilen_ay_adi = aylar_listesi[secilen_ay_index]
    
    st.subheader(f"{L['goal_header']} {secilen_ay_adi}")
    
    with st.form("hedef_form", clear_on_submit=True):
        yeni_hedef_txt = st.text_input(L["new_goal"])
        if st.form_submit_button(L["add_btn"]):
            if yeni_hedef_txt:
                conn = get_db_connection()
                c = conn.cursor()
                # Ayı 'index' olarak kaydediyoruz (0=Ocak, 1=Şubat) böylece dil değişse de veri bozulmaz
                c.execute("INSERT INTO hedefler (ay, hedef, durum) VALUES (?, ?, ?)", (str(secilen_ay_index), yeni_hedef_txt, 0))
                conn.commit()
                conn.close()
                st.rerun()

    conn = get_db_connection()
    # Veriyi çekerken ay indexine göre çekiyoruz
    df_hedefler = pd.read_sql_query(f"SELECT * FROM hedefler WHERE ay = '{secilen_ay_index}'", conn)
    conn.close()

    if not df_hedefler.empty:
        for index, row in df_hedefler.iterrows():
            col_chk, col_txt, col_del = st.columns([1, 6, 1])
            is_checked = col_chk.checkbox("", value=bool(row['durum']), key=f"chk_{row['id']}")
            if is_checked != bool(row['durum']):
                conn = get_db_connection()
                conn.execute("UPDATE hedefler SET durum = ? WHERE id = ?", (int(is_checked), row['id']))
                conn.commit()
                conn.close()
                st.rerun()
            
            if is_checked: col_txt.markdown(f"~~{row['hedef']}~~")
            else: col_txt.write(row['hedef'])
            
            if col_del.button("🗑️", key=f"del_{row['id']}"):
                conn = get_db_connection()
                conn.execute("DELETE FROM hedefler WHERE id = ?", (row['id'],))
                conn.commit()
                conn.close()
                st.rerun()
        
        # İlerleme
        biten = len(df_hedefler[df_hedefler['durum'] == 1])
        oran = biten / len(df_hedefler)
        st.progress(oran)
        st.caption(f"{L['progress']} %{int(oran*100)}")
    else:
        st.info(L["no_goal"])

# ================= TAB 3: ANALİZ =================
with tab3:
    st.header(L["analysis_header"])
    conn = get_db_connection()
    df_gunluk = pd.read_sql_query("SELECT * FROM gunluk ORDER BY tarih DESC LIMIT 30", conn)
    conn.close()
    
    if not df_gunluk.empty:
        st.write(L["last_30"])
        st.bar_chart(df_gunluk['mood'].value_counts())
    else:
        st.warning(L["no_data"])