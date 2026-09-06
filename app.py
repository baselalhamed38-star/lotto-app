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
    st.info("نظام ذكي متكامل لتحليل السحوبات التاريخية وتوليد التوقعات لعام 2026 بأحدث التقنيات.")

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
        "hist_btn_title": "🔍 تحليل الأرشيف التاريخي وتوليد توقعات 2026",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام 2026 (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام 2026 (البرج الفلكي)",
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
        "hist_btn_title": "🔍 Analyze Historical Archive & Generate 2026 Predictions",
        "birth_title": "📅 Independent Birthdate Window",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate 2026 Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate 2026 Numbers (Zodiac)",
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
        "hist_btn_title": "🔍 Historisches Archiv analysieren & 2026 Prognosen generieren",
        "birth_title": "📅 Unabhängiges Geburtsdatum-Fenster",
        "birth_select": "Geburtsdatum wählen:",
        "birth_btn": "🎲 2026 Zahlen generieren (Geburtsdatum)",
        "zodiac_title": "🌟 Unabhängiges Sternzeichen-Fenster",
        "zodiac_select": "Sternzeichen wählen:",
        "zodiac_btn": "🎲 2026 Zahlen generieren (Sternzeichen)",
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
        if game_type == "lotto" and ("lotto" in f.lower() and "euro" not in f.lower()):
            matched_files.append(f)
        elif game_type == "euro" and ("euro" in f.lower() or "ej" in f.lower()):
            matched_files.append(f)
            
    if not matched_files:
        matched_files = all_files
        
    all_draws = []
    for file_name in matched_files:
        try:
            if file_name.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(file_name)
                for sheet_name in xls.sheet_names:
                    df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                    if not df_sheet.empty:
                        df_sheet['Source_Info'] = f"File: {file_name} ➔ [Sheet: {sheet_name}]"
                        all_draws.append(df_sheet)
            elif file_name.endswith('.csv'):
                df_csv = pd.read_csv(file_name, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty:
                    df_csv['Source_Info'] = f"File: {file_name}"
                    all_draws.append(df_csv)
        except Exception as e:
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
    numeric_vals = df.select_dtypes(include=[np.number])
    matrix_sum = int(numeric_vals.sum().sum()) if not numeric_vals.empty else 12345
    
    # بطاقة إحصائية جذابة
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
    
    # ----------------- 2. زر تحليل السحوبات التاريخية لتوليد التوقعات -----------------
    st.markdown(f"### {t['hist_btn_title']}")
    hist_counter_key = f"counter_hist_{game_name}"
    if hist_counter_key not in st.session_state:
        st.session_state[hist_counter_key] = 0
        
    if st.button(t["hist_btn_title"], key=f"btn_hist_{game_name}"):
        st.session_state[hist_counter_key] += 1
        
    if st.session_state[hist_counter_key] > 0:
        seed_hist = total_rows + matrix_sum + (st.session_state[hist_counter_key] * 444) + int(datetime.now().strftime("%f"))
        np.random.seed(seed_hist)
        
        st.success(f"✨ Prediction #{st.session_state[hist_counter_key]} (Historical Analysis):")
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
    
    # ----------------- 3. نافذة تاريخ الميلاد المستقلة -----------------
    st.markdown(f"### {t['birth_title']}")
    birth_date = st.date_input(t["birth_select"], value=datetime(1990, 1, 1), key=f"b_date_{game_name}")
    
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state:
        st.session_state[birth_counter_key] = 0
        
    if st.button(t["birth_btn"], key=f"btn_birth_{game_name}"):
        st.session_state[birth_counter_key] += 1
        
    if st.session_state[birth_counter_key] > 0:
        seed_birth = total_rows + matrix_sum + birth_date.toordinal() + (st.session_state[birth_counter_key] * 99)
        np.random.seed(seed_birth)
        
        st.success(f"✨ Birthdate Prediction #{st.session_state[birth_counter_key]}:")
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
    zodiac = st.selectbox(t["zodiac_select"], 
                          ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", 
                           "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", 
                           "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"], key=f"z_select_{game_name}")
    
    zodiac_counter_key = f"counter_zodiac_{game_name}"
    if zodiac_counter_key not in st.session_state:
        st.session_state[zodiac_counter_key] = 0
        
    if st.button(t["zodiac_btn"], key=f"btn_zodiac_{game_name}"):
        st.session_state[zodiac_counter_key] += 1
        
    if st.session_state[zodiac_counter_key] > 0:
        seed_zodiac = total_rows + matrix_sum + hash(zodiac) + (st.session_state[zodiac_counter_key] * 111)
        np.random.seed(seed_zodiac)
        
        st.success(f"✨ Zodiac Prediction #{st.session_state[zodiac_counter_key]} ({zodiac.split()[0]}):")
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
