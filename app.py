import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import random

st.set_page_config(
    page_title="True Date Formula Engine 2026", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #ffffff;
        border-radius: 10px 10px 0px 0px; padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important; color: white !important; font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .formula-box {
        background-color: #ffffff; border-right: 5px solid #1f77b4;
        padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px; font-family: monospace;
    }
    .stButton>button {
        width: 100%; border-radius: 10px; font-weight: bold; height: 45px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .number-badge {
        display: inline-block; background-color: #1f77b4; color: white;
        font-size: 16px; font-weight: bold; padding: 6px 12px; margin: 3px;
        border-radius: 50px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .special-badge {
        display: inline-block; background-color: #ff4b4b; color: white;
        font-size: 16px; font-weight: bold; padding: 6px 14px; margin: 3px;
        border-radius: 50px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌐 Language / اللغات / Sprache")
    lang_choice = st.selectbox("اختر اللغة / Choose Language:", ["العربية", "English", "Deutsch"])
    st.markdown("---")
    st.info("محرك الأرقام الثابت المستند إلى المفتاح الزمني للتاريخ.")

texts = {
    "العربية": {
        "title": "🎯 محرك توليد الأرقام المربوط بالتاريخ 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 مطابقة السحوبات التاريخية في الأرشيف",
        "target_day": "اختر اليوم:",
        "target_month": "اختر الشهر:",
        "search_btn": "⚡ عرض السحوبات المطابقة",
        "found_res": "✅ السحوبات التاريخية المطابقة في الأرشيف:",
        "no_res": "⚠️ لم يتم العثور على سحوبات مطابقة لهذا اليوم والشهر في الجدول.",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
        "schein_type": "نوع الورقة (Tippschein Type):",
        "normal_schein": "نورمال شاين (Normal Schein - 6 أرقام)",
        "system_schein": "سيستيم شاين (System Schein - أرقام مضاعفة ومجموعات)",
        "select_lotto_system": "اختر عدد أرقام السيستيم المطلوب (Vollsystem):",
        "gen_title": "📅 قسم التوقعات والأربع احتمالات المتجددة لسنة 2026",
        "gen_btn": "🚀 توليد 4 احتمالات جديدة",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام (البرج الفلكي)",
    },
    "English": {
        "title": "🎯 Date-Linked Lottery Engine 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Match Historical Draws in Archive",
        "target_day": "Select Day:",
        "target_month": "Select Month:",
        "search_btn": "⚡ Show Matched Draws",
        "found_res": "✅ Matched Historical Draws in Archive:",
        "no_res": "⚠️ No matching draws found.",
        "expander_title": "👁️ View Complete Archive",
        "schein_type": "Tippschein Type:",
        "normal_schein": "Normal Schein (6 numbers)",
        "system_schein": "System Schein (Extended & Combinations)",
        "select_lotto_system": "Select Lotto System Count (Vollsystem):",
        "gen_title": "📅 2026 Date-Seed 4 New Possibilities Center",
        "gen_btn": "🚀 Generate 4 New Possibilities",
        "birth_title": "📅 Independent Birthdate Window",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate Numbers (Zodiac)",
    },
    "Deutsch": {
        "title": "🎯 Datumsbasierte Lotto-Engine 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Historische Ziehungen im Archiv matchen",
        "target_day": "Tag wählen:",
        "target_month": "Monat wählen:",
        "search_btn": "⚡ Passende Ziehungen anzeigen",
        "found_res": "✅ Passende historische Ziehungen:",
        "no_res": "⚠️ Keine passenden Ziehungen gefunden.",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
        "schein_type": "Tippschein-Typ:",
        "normal_schein": "Normaler Schein (6 Zahlen)",
        "system_schein": "Systemschein",
        "select_lotto_system": "Lotto System Anzahl wählen (Vollsystem):",
        "gen_title": "📅 2026 Prognose-Center (Neue Möglichkeiten)",
        "gen_btn": "🚀 4 neue Möglichkeiten generieren",
        "birth_title": "📅 Unabhängiges Geburtsdatum-Fenster",
        "birth_select": "Geburtsdatum wählen:",
        "birth_btn": "🎲 Zahlen generieren (Geburtsdatum)",
        "zodiac_title": "🌟 Unabhängiges Sternzeichen-Fenster",
        "zodiac_select": "Sternzeichen wählen:",
        "zodiac_btn": "🎲 Zahlen generieren (Sternzeichen)",
    }
}

t = texts[lang_choice]

st.markdown(f"<h1 style='text-align: center; color: #1f77b4;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data(show_spinner=False)
def load_game_files(game_type):
    all_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls', '.csv'))]
    matched_files = [f for f in all_files if game_type in f.lower()]
    if not matched_files: matched_files = all_files
        
    all_draws = []
    for file_name in matched_files:
        try:
            if file_name.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(file_name)
                for sheet_name in xls.sheet_names:
                    df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                    if not df_sheet.empty: all_draws.append(df_sheet)
            elif file_name.endswith('.csv'):
                df_csv = pd.read_csv(file_name, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty: all_draws.append(df_csv)
        except:
            pass
    return pd.concat(all_draws, ignore_index=True) if all_draws else pd.DataFrame(), matched_files

df_lotto, files_lotto = load_game_files("lotto")
df_euro, files_euro = load_game_files("euro")

tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

def display_numbers(numbers, special_num, special_label="Superzahl (0-9)"):
    nums_html = "".join([f"<span class='number-badge'>{num}</span>" for num in numbers])
    spec_html = f"<span class='special-badge'>{special_num}</span>"
    st.markdown(f"**الأرقام الناتجة ({len(numbers)}):**<br>{nums_html}", unsafe_allow_html=True)
    st.markdown(f"<br>**{special_label}:** {spec_html}", unsafe_allow_html=True)

def generate_date_seed_numbers(year, month, day, count=6, max_val=49):
    seed_val = (year * 10000) + (month * 100) + day
    np.random.seed(seed_val % (2**31 - 1))
    nums = sorted(np.random.choice(range(1, max_val + 1), count, replace=False).tolist())
    spec_val = (year + month + day) % (12 if max_val == 50 else 10)
    return nums, spec_val, seed_val

def run_full_features_tab(df, game_name, matched_files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(matched_files) if matched_files else 'General Files'}`")
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    total_rows = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {game_name} Archive & Engine</h2>
            <h3>Total Records: {total_rows}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"### {t['search_title']}")
        col_d, col_m = st.columns(2)
        with col_d:
            selected_day = st.selectbox(t["target_day"], list(range(1, 32)), index=8, key=f"s_day_{game_name}")
        with col_m:
            months_dict = {
                "يناير (01)": 1, "فبراير (02)": 2, "مارس (03)": 3, "أبريل (04)": 4,
                "مايو (05)": 5, "يونيو (06)": 6, "يوليو (07)": 7, "أغسطس (08)": 8,
                "سبتمبر (09)": 9, "أكتوبر (10)": 10, "نوفمبر (11)": 11, "ديسمبر (12)": 12
            }
            selected_month_name = st.selectbox(t["target_month"], list(months_dict.keys()), index=8, key=f"s_mon_{game_name}")
            selected_month_num = months_dict[selected_month_name]
            
        matched_rows = []
        if not df.empty:
            for idx, row in df.iterrows():
                is_matched = False
                for val in row.values:
                    if pd.notna(val):
                        v_str = str(val).strip()
                        if (f"{selected_day:02d}.{selected_month_num:02d}." in v_str or 
                            f"{selected_day}.{selected_month_num}." in v_str):
                            is_matched = True
                            break
                        dt = pd.to_datetime(val, errors='coerce', dayfirst=True)
                        if pd.notna(dt) and dt.year > 1980 and dt.day == selected_day and dt.month == selected_month_num:
                            is_matched = True
                            break
                if is_matched:
                    matched_rows.append((idx, row))

        if st.button(t["search_btn"], key=f"btn_search_{game_name}
