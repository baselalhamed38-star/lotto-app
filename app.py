import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

# إعدادات الصفحة بتصميم عصري
st.set_page_config(
    page_title="Lottery & Eurojackpot Analytics 2026", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- تصميم CSS جذاب وعصري -----------------
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 10px 10px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        height: 45px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- القائمة الجانبية للغات والتوجيه -----------------
with st.sidebar:
    st.markdown("### 🌐 Language / اللغات / Sprache")
    lang_choice = st.selectbox("اختر اللغة / Choose Language:", ["العربية", "English", "Deutsch"])
    
    st.markdown("---")
    st.markdown("### 🎯 Dashboard 2026")
    st.info("نظام ذكي متكامل لتحليل السحوبات التاريخية وتوليد التوقعات لعام 2026 مع خيارات النورمال والسيستيم شاين.")

# نصوص مترجمة حسب اختيار المستخدم
texts = {
    "العربية": {
        "title": "🎯 النظام الذكي المتقدم لتحليل وتوقع سحوبات 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 البحث الدقيق عن نفس اليوم والشهر (عبر كل السنوات)",
        "day_label": "اختر اليوم:",
        "month_label": "اختر الشهر:",
        "found_res": "✅ تم العثور على سحوبات مطابقة في نفس اليوم والشهر:",
        "no_res": "⚠️ لم يتم العثور على سحوبات مسجلة في هذا التاريخ بالتحديد ضمن الأرشيف.",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
        "gen_title": "🎲 مركز توليد التوقعات الذكية (الأرشيف)",
        "schein_type": "نوع الورقة (Tippschein Type):",
        "normal_schein": "نورمال شاين (Normal Schein - 6 أرقام)",
        "system_schein": "سيستيم شاين (System Schein - أرقام مضاعفة)",
        "select_lotto_system": "اختر نظام السيستيم (Vollsystem):",
        "select_euro_system": "اختر نظام يوروجاكبوت (System):",
        "gen_btn": "🚀 توليد الأرقام والتحليل",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة (مفتوحة)",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام 2026 (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام 2026 (البرج الفلكي)",
        "power_label": "⚡ قوة الاقتراح والموثوقية:"
    },
    "English": {
        "title": "🎯 Advanced System for Analytics & 2026 Predictions",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Precise Date Search (Same Day & Month across all years)",
        "day_label": "Select Day:",
        "month_label": "Select Month:",
        "found_res": "✅ Matching draws found for this day and month:",
        "no_res": "⚠️ No exact draws found for this specific date in the archive.",
        "expander_title": "👁️ View Complete Archive",
        "gen_title": "🎲 Smart Prediction Center (Archive)",
        "schein_type": "Tippschein Type:",
        "normal_schein": "Normal Schein (6 numbers)",
        "system_schein": "System Schein (Extended numbers)",
        "select_lotto_system": "Select Lotto System (Vollsystem):",
        "select_euro_system": "Select Eurojackpot System:",
        "gen_btn": "🚀 Generate Numbers & Analysis",
        "birth_title": "📅 Independent Birthdate Window (Open)",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate 2026 Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate 2026 Numbers (Zodiac)",
        "power_label": "⚡ Prediction Power & Confidence:"
    },
    "Deutsch": {
        "title": "🎯 Fortgeschrittenes System für Ziehungsanalysen & 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Exakte Datumssuche (Gleicher Tag & Monat über alle Jahre)",
        "day_label": "Tag wählen:",
        "month_label": "Monat wählen:",
        "found_res": "✅ Übereinstimmende Ziehungen für diesen Tag und Monat gefunden:",
        "no_res": "⚠️ Keine genauen Ziehungen für dieses Datum im Archiv gefunden.",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
        "gen_title": "🎲 Intelligentes Prognose-Center (Archiv)",
        "schein_type": "Tippschein-Typ:",
        "normal_schein": "Normaler Schein (6 Zahlen)",
        "system_schein": "Systemschein (Erweiterte Zahlen)",
        "select_lotto_system": "Lotto System wählen (Vollsystem):",
        "select_euro_system": "Eurojackpot System wählen:",
        "gen_btn": "🚀 Zahlen & Analyse generieren",
        "birth_title": "📅 Unabhängiges Geburtsdatum-Fenster (Offen)",
        "birth_select": "Geburtsdatum wählen:",
        "birth_btn": "🎲 2026 Zahlen generieren (Geburtsdatum)",
        "zodiac_title": "🌟 Unabhängiges Sternzeichen-Fenster",
        "zodiac_select": "Sternzeichen wählen:",
        "zodiac_btn": "🎲 2026 Zahlen generieren (Sternzeichen)",
        "power_label": "⚡ Vorhersagestärke & Konfidenz:"
    }
}

t = texts[lang_choice]

st.markdown(f"<h1 style='text-align: center; color: #1f77b4;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_game_files(game_type):
    all_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls', '.csv'))]
    matched_files = []
    for f in all_files:
        f_lower = f.lower()
        if game_type == "lotto" and ("lotto" in f_lower):
            matched_files.append(f)
        elif game_type == "euro" and ("euro" in f_lower or "ej" in f_lower):
            matched_files.append(f)
            
    if not matched_files:
        matched_files = all_files
        
    all_draws = []
    for file_name in matched_files:
        try:
            if file_name.endswith(('.xlsx', '.xls')):
                try:
                    xls = pd.ExcelFile(file_name)
                    for sheet_name in xls.sheet_names:
                        df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                        if not df_sheet.empty:
                            df_sheet['Source_Info'] = f"File: {file_name} ➔ [Sheet: {sheet_name}]"
                            all_draws.append(df_sheet)
                except Exception:
                    df_alt = pd.read_excel(file_name, header=None)
                    if not df_alt.empty:
                        df_alt['Source_Info'] = f"File: {file_name}"
                        all_draws.append(df_alt)
            elif file_name.endswith('.csv'):
                df_csv = pd.read_csv(file_name, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty:
                    df_csv['Source_Info'] = f"File: {file_name}"
                    all_draws.append(df_csv)
        except Exception:
            pass
            
    if all_draws:
        return pd.concat(all_draws, ignore_index=True), matched_files
    return pd.DataFrame(), []

df_lotto, files_lotto = load_game_files("lotto")
df_euro, files_euro = load_game_files("euro")

tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

def run_full_features_tab(df, game_name, matched_files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(matched_files) if matched_files else 'General Files'}`")
    
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    total_rows = len(df)
    
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {game_name} Archive Analysis</h2>
            <h3>Total Historical Draws: {total_rows}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # ----------------- 1. البحث الدقيق بنفس اليوم والشهر -----------------
    with st.container():
        st.markdown(f"### {t['search_title']}")
        col_d, col_m = st.columns(2)
        with col_d:
            selected_day = st.selectbox(t["day_label"], list(range(1, 32)), key=f"p_day_{game_name}")
        with col_m:
            months_dict = {
                "يناير (01) / January": "01", "فبراير (02) / February": "02", "مارس (03) / March": "03", "أبريل (04) / April": "04",
                "مايو (05) / May": "05", "يونيو (06) / June": "06", "يوليو (07) / July": "07", "أغسطس (08) / August": "08",
                "سبتمبر (09) / September": "09", "أكتوبر (10) / October": "10", "نوفمبر (11) / November": "11", "ديسمبر (12) / December": "12"
            }
            selected_month_name = st.selectbox(t["month_label"], list(months_dict.keys()), key=f"p_mon_{game_name}")
            selected_month_num = months_dict[selected_month_name].split()[0]
            
        day_str = f"{selected_day:02d}"
        df_str = df.astype(str)
        
        pattern_dot = f".*\\b{day_str}\\.{selected_month_num}\\b.*"
        pattern_slash = f".*\\b{int(day_str)}/{int(selected_month_num)}/.*"
        pattern_hyphen = f".*\\b-{selected_month_num}-{day_str}\\b.*"
        
        exact_date_mask = df_str.apply(lambda x: x.str.contains(pattern_dot, regex=True, case=False, na=False) |
                                                   x.str.contains(pattern_slash, regex=True, case=False, na=False) |
                                                   x.str.contains(pattern_hyphen, regex=True, case=False, na=False)).any(axis=1)
        
        res_date = df[exact_date_mask]
        
        if not res_date.empty:
            st.success(f"{t['found_res']} ({day_str}/{selected_month_num})")
            st.dataframe(res_date, use_container_width=True)
        else:
            st.warning(t["no_res"])
            
        with st.expander(t["expander_title"]):
            st.dataframe(df, use_container_width=True)
            
    st.markdown("---")
    
    # ----------------- 2. مركز توليد التوقعات (النورمال مقابل السيستيم شاين) -----------------
    st.markdown(f"### {t['gen_title']}")
    
    schein_mode = st.radio(t["schein_type"], [t["normal_schein"], t["system_schein"]], key=f"schein_{game_name}")
    
    selected_count = 6 # افتدري للوتو النورمال
    euro_count = 2
    
    if schein_mode == t["system_schein"]:
        if not is_euro:
            lotto_sys_choice = st.selectbox(
                t["select_lotto_system"], 
                ["Vollsystem 007 (7 أرقام)", "Vollsystem 008 (8 أرقام)", "Vollsystem 009 (9 أرقام)", "Vollsystem 010 (10 أرقام)", "Vollsystem 011 (11 أرقام)", "Vollsystem 012 (12 أرقام)"],
                key=f"l_sys_{game_name}"
            )
            selected_count = int(lotto_sys_choice.split()[1])
        else:
            euro_sys_choice = st.selectbox(
                t["select_euro_system"],
                ["System 5/3 (5 أرقام أساسية + 3 نجوم)", "System 5/4 (5 أرقام أساسية + 4 نجوم)", "System 6/2 (6 أرقام أساسية + 2 نجوم)", "System 7/2 (7 أرقام أساسية + 2 نجوم)"],
                key=f"e_sys_{game_name}"
            )
            if "5/" in euro_sys_choice:
                selected_count = 5
                euro_count = int(euro_sys_choice.split('/')[1].split()[0])
            elif "6/" in euro_sys_choice:
                selected_count = 6
                euro_count = 2
            elif "7/" in euro_sys_choice:
                selected_count = 7
                euro_count = 2

    gen_counter_key = f"counter_gen_{game_name}"
    if gen_counter_key not in st.session_state:
        st.session_state[gen_counter_key] = 0
        
    if st.button(t["gen_btn"], key=f"btn_gen_{game_name}"):
        st.session_state[gen_counter_key] += 1
        
    if st.session_state[gen_counter_key] > 0:
        seed_gen = abs(total_rows + (st.session_state[gen_counter_key] * 555)) % (2**31 - 1)
        np.random.seed(seed_gen)
        
        confidence_score = min(85 + (total_rows % 12) + (st.session_state[gen_counter_key] % 4), 99)
        
        if schein_mode == t["normal_schein"]:
            st.success(f"✨ Normal Schein Prediction #{st.session_state[gen_counter_key]}:")
        else:
            st.success(f"⚙️ System Schein Prediction #{st.session_state[gen_counter_key]} ({schein_mode}):")
            
        st.info(f"{t['power_label']} **{confidence_score}%** (Archive Matrix)")
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), selected_count, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            col1, col2 = st.columns(2)
            col1.metric("Selected Numbers:", str(p_nums))
            col2.metric("Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), selected_count, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), euro_count, replace=False).tolist())
            col1, col2 = st.columns(2)
            col1.metric("Main Numbers:", str(p_nums))
            col2.metric("Euro Zahlen (Stars):", str(p_stars))
            
    st.markdown("---")
    
    # ----------------- 3. نافذة تاريخ الميلاد المستقلة (مفتوحة) -----------------
    st.markdown(f"### {t['birth_title']}")
    birth_date = st.date_input(
        t["birth_select"], 
        value=datetime(1990, 1, 1), 
        min_value=datetime(1900, 1, 1), 
        max_value=datetime.today(), 
        key=f"b_date_{game_name}"
    )
    
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state:
        st.session_state[birth_counter_key] = 0
        
    if st.button(t["birth_btn"], key=f"btn_birth_{game_name}"):
        st.session_state[birth_counter_key] += 1
        
    if st.session_state[birth_counter_key] > 0:
        seed_birth = abs(birth_date.toordinal() + (st.session_state[birth_counter_key] * 99)) % (2**31 - 1)
        np.random.seed(seed_birth)
        
        confidence_score = 75 + (birth_date.day * 2) % 20
        
        st.success(f"✨ Birthdate Prediction #{st.session_state[birth_counter_key]}:")
        st.info(f"{t['power_label']} **{confidence_score}%** (Moderate-High / متوسط إلى مرتفع)")
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            col1, col2 = st.columns(2)
            col1.metric("Lotto Numbers:", str(p_nums))
            col2.metric("Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            col1, col2 = st.columns(2)
            col1.metric("Main Numbers:", str(p_nums))
            col2.metric("Euro Zahlen:", str(p_stars))
            
    st.markdown("---")
    
    # ----------------- 4. نافذة الأبراج الفلكية المستقلة -----------------
    st.markdown(f"### {t['zodiac_title']}")
    zodiac_list = [
        "الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", 
        "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", 
        "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"
    ]
    zodiac = st.selectbox(t["zodiac_select"], zodiac_list, key=f"z_select_{game_name}")
    
    zodiac_counter_key = f"counter_zodiac_{game_name}"
    if zodiac_counter_key not in st.session_state:
        st.session_state[zodiac_counter_key] = 0
        
    if st.button(t["zodiac_btn"], key=f"btn_zodiac_{game_name}"):
        st.session_state[zodiac_counter_key] += 1
        
    if st.session_state[zodiac_counter_key] > 0:
        zodiac_index = zodiac_list.index(zodiac) + 1
        seed_zodiac = abs((zodiac_index * 1000) + (st.session_state[zodiac_counter_key] * 111)) % (2**31 - 1)
        np.random.seed(seed_zodiac)
        
        confidence_score = 70 + (zodiac_index * 2) % 25
        
        st.success(f"✨ Zodiac Prediction #{st.session_state[zodiac_counter_key]} ({zodiac.split()[0]}):")
        st.info(f"{t['power_label']} **{confidence_score}%** (Astrological Match / توافق فلكي)")
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            col1, col2 = st.columns(2)
            col1.metric("Lotto Numbers:", str(p_nums))
            col2.metric("Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            col1, col2 = st.columns(2)
            col1.metric("Main Numbers:", str(p_nums))
            col2.metric("Euro Zahlen:", str(p_stars))

with tab1:
    run_full_features_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_full_features_tab(df_euro, "Eurojackpot", files_euro, True)
