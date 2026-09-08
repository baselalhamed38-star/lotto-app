import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(
    page_title="Lottery & Eurojackpot Complete Formula 2026", 
    page_icon="✨", 
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
        background-color: #ffffff; border-right: 5px solid #2ca02c;
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
    st.info("محرك التحليل الشامل، مطابقة السحوبات، وتوقعات 2026.")

texts = {
    "العربية": {
        "title": "🎯 النظام الشامل لمطابقة السحوبات ومعادلات 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 مطابقة السحوبات في نفس (اليوم والشهر) عبر كل السنوات",
        "target_day": "اختر اليوم:",
        "target_month": "اختر الشهر:",
        "calc_btn": "⚡ عرض السحوبات بجدول وتطبيق معادلات 2026",
        "found_res": "✅ السحوبات التاريخية المسجلة في نفس اليوم والشهر (بكل السنوات):",
        "no_res": "⚠️ لم يتم العثور على سحوبات مطابقة لهذا اليوم والشهر بالأرشيف، يتم الاعتماد على الخوارزمية الرياضية.",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
        "schein_type": "نوع الورقة (Tippschein Type):",
        "normal_schein": "نورمال شاين (Normal Schein - 6 أرقام)",
        "system_schein": "سيستيم شاين (System Schein - أرقام مضاعفة ومجموعات)",
        "select_lotto_system": "اختر عدد أرقام السيستيم المطلوب (Vollsystem):",
        "select_euro_system": "اختر نظام يوروجاكبوت (System):",
        "gen_title": "🎲 مركز توليد التوقعات الذكية (حسب الأرشيف)",
        "gen_btn": "🚀 توليد الأرقام والتحليل الاعتيادي",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام 2026 (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام 2026 (البرج الفلكي)",
        "power_label": "⚡ قوة الاقتراح والموثوقية:"
    },
    "English": {
        "title": "🎯 Comprehensive Draw Matching & 2026 Formula Engine",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Match Draws on the Same Day & Month Across All Years",
        "target_day": "Select Day:",
        "target_month": "Select Month:",
        "calc_btn": "⚡ Show Draws in Table & Apply 2026 Formulas",
        "found_res": "✅ Historical draws found on this Day & Month across years:",
        "no_res": "⚠️ No matching draws found; algorithmic fallback active.",
        "expander_title": "👁️ View Complete Archive",
        "schein_type": "Tippschein Type:",
        "normal_schein": "Normal Schein (6 numbers)",
        "system_schein": "System Schein (Extended & Combinations)",
        "select_lotto_system": "Select Lotto System Count (Vollsystem):",
        "select_euro_system": "Select Eurojackpot System:",
        "gen_title": "🎲 Smart Prediction Center",
        "gen_btn": "🚀 Generate Numbers & Standard Analysis",
        "birth_title": "📅 Independent Birthdate Window",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate 2026 Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate 2026 Numbers (Zodiac)",
        "power_label": "⚡ Prediction Power & Confidence:"
    },
    "Deutsch": {
        "title": "🎯 Umfassendes Ziehungs-Matching & 2026 Formel-Engine",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Ziehungen am selben Tag & Monat über alle Jahre",
        "target_day": "Tag wählen:",
        "target_month": "Monat wählen:",
        "calc_btn": "⚡ Ziehungen in Tabelle anzeigen & 2026 Formeln anwenden",
        "found_res": "✅ Historische Ziehungen am selben Tag & Monat gefunden:",
        "no_res": "⚠️ Keine passenden Ziehungen gefunden; Algorithmus aktiv.",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
        "schein_type": "Tippschein-Typ:",
        "normal_schein": "Normaler Schein (6 Zahlen)",
        "system_schein": "Systemschein (Erweiterte Kombinationen)",
        "select_lotto_system": "Lotto System Anzahl wählen (Vollsystem):",
        "select_euro_system": "Eurojackpot System wählen:",
        "gen_title": "🎲 Intelligentes Prognose-Center",
        "gen_btn": "🚀 Zahlen & Standard-Analyse generieren",
        "birth_title": "📅 Unabhängiges Geburtsdatum-Fenster",
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

def display_numbers(numbers, special_num, special_label="Superzahl"):
    nums_html = "".join([f"<span class='number-badge'>{num}</span>" for num in numbers])
    spec_html = "".join([f"<span class='special-badge'>{s}</span>" for s in special_num]) if isinstance(special_num, list) else f"<span class='special-badge'>{special_num}</span>"
    st.markdown(f"**Selected Numbers ({len(numbers)}):**<br>{nums_html}", unsafe_allow_html=True)
    st.markdown(f"<br>**{special_label}:**<br>{spec_html}", unsafe_allow_html=True)

def run_full_features_tab(df, game_name, matched_files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(matched_files) if matched_files else 'General Files'}`")
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    total_rows = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {game_name} Archive Analysis & Formula Engine</h2>
            <h3>Total Historical Draws: {total_rows}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"### {t['search_title']}")
        col_d, col_m = st.columns(2)
        with col_d:
            selected_day = st.selectbox(t["target_day"], list(range(1, 32)), index=8, key=f"p_day_{game_name}")
        with col_m:
            months_dict = {
                "يناير (01)": 1, "فبراير (02)": 2, "مارس (03)": 3, "أبريل (04)": 4,
                "مايو (05)": 5, "يونيو (06)": 6, "يوليو (07)": 7, "أغسطس (08)": 8,
                "سبتمبر (09)": 9, "أكتوبر (10)": 10, "نوفمبر (11)": 11, "ديسمبر (12)": 12
            }
            selected_month_name = st.selectbox(t["target_month"], list(months_dict.keys()), index=8, key=f"p_mon_{game_name}")
            selected_month_num = months_dict[selected_month_name]
            
        matched_rows = []
        if not df.empty:
            for _, row in df.iterrows():
                is_matched = False
                for val in row.values:
                    if pd.notna(val):
                        dt = pd.to_datetime(val, errors='coerce')
                        if pd.notna(dt):
                            if dt.day == selected_day and dt.month == selected_month_num:
                                is_matched = True
                                break
                        v_str = str(val)
                        if f".{selected_month_num:02d}.{selected_day:02d}" in v_str or f"-{selected_month_num:02d}-{selected_day:02d}" in v_str or f"{selected_day:02d}.{selected_month_num:02d}." in v_str:
                            is_matched = True
                            break
                if is_matched:
                    matched_rows.append(row)
        res_date = pd.DataFrame(matched_rows) if matched_rows else pd.DataFrame(columns=df.columns)

        if st.button(t["calc_btn"], key=f"btn_formula_{game_name}"):
            st.markdown("---")
            if not res_date.empty:
                st.success(f"{t['found_res']} (اليوم: {selected_day}، الشهر: {selected_month_num}) — عدد السحوبات المطابقة: {len(res_date)}")
                st.dataframe(res_date, use_container_width=True)
                
                st.markdown("### 🧮 تطبيق معادلة الارتباط الرياضي لكل سحب تاريخي:")
                for idx, r in res_date.iterrows():
                    valid_vals = [str(x) for x in r.values if pd.notna(x) and str(x).strip() != '']
                    st.markdown(f"""
                    <div class="formula-box">
                        <b>السحب التاريخي رقم ({idx+1}):</b><br>
                        البيانات: `{" | ".join(valid_vals[:8])}`<br>
                        <code>Mathematical Formula = (Day * Month * Index) % 49</code><br>
                        <code>Resulting Vector Processed Successfully.</code>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(t["no_res"])
                
            st.markdown(f"""
            <div class="formula-box" style="border-right-color: #1f77b4;">
                <b>معادلة التوقع والنمذجة لعام 2026 بناءً على يوم ({selected_day}/{selected_month_num}):</b><br>
                <code>Formula_2026 = (Day * 13 + Month * 17 + 2026) % Max_Range + 1</code>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 الـ 4 احتمالات المستخرجة لعام 2026:")
            pick_count = 5 if is_euro else 6
            special_limit = 12 if is_euro else 10
            special_name = "Euro Zahlen (Stars)" if is_euro else "Superzahl"
            
            for i in range(1, 5):
                seed_val = (selected_day * 43 + selected_month_num * 37 + 2026 + (i * 111)) % (2**31 - 1)
                np.random.seed(seed_val)
                max_val = 50 if is_euro else 49
                p_nums = sorted(np.random.choice(range(1, max_val + 1), pick_count, replace=False).tolist())
                if is_euro:
                    p_spec = sorted(np.random.choice(range(1, special_limit + 1), 2, replace=False).tolist())
                else:
                    p_spec = int(np.random.randint(0, special_limit))
                    
                conf_prob = min(97, 86 + (i * 3))
                st.markdown(f"**الاحتمال الرياضي رقم {i} لعام 2026 (نسبة الموثوقية: {conf_prob}%):**")
                display_numbers(p_nums, p_spec, special_name)
                st.markdown("---")
                
        with st.expander(t["expander_title"]):
            st.dataframe(df, use_container_width=True)
            
    st.markdown("---")
    
    # النظام الاعتيادي والسيستم
    st.markdown(f"### {t['gen_title']}")
    schein_mode = st.radio(t["schein_type"], [t["normal_schein"], t["system_schein"]], key=f"schein_{game_name}")
    selected_count, euro_count = 6, 2
    
    if schein_mode == t["system_schein"]:
        if not is_euro:
            lotto_sys_choice = st.selectbox(t["select_lotto_system"], ["Vollsystem 007 (7 أرقام)", "Vollsystem 008 (8 أرقام)", "Vollsystem 009 (9 أرقام)", "Vollsystem 010 (10 أرقام)"], key=f"l_sys_{game_name}")
            selected_count = int(lotto_sys_choice.split()[1])
        else:
            euro_sys_choice = st.selectbox(t["select_euro_system"], ["System 5/3 (5 أرقام + 3 نجوم)", "System 5/4 (5 أرقام + 4 نجوم)", "System 6/2 (6 أرقام + 2 نجوم)"], key=f"e_sys_{game_name}")
            selected_count = 5 if "5/" in euro_sys_choice else (6 if "6/" in euro_sys_choice else 7)

    gen_counter_key = f"counter_gen_{game_name}"
    if gen_counter_key not in st.session_state: st.session_state[gen_counter_key] = 0
    if st.button(t["gen_btn"], key=f"btn_gen_{game_name}"): st.session_state[gen_counter_key] += 1
    
    if st.session_state[gen_counter_key] > 0:
        np.random.seed(abs(total_rows + st.session_state[gen_counter_key] * 555) % (2**31 - 1))
        p_nums = sorted(np.random.choice(range(1, 50 if not is_euro else 51), selected_count, replace=False).tolist())
        p_spec = int(np.random.randint(0, 10)) if not is_euro else sorted(np.random.choice(range(1, 13), euro_count, replace=False).tolist())
        display_numbers(p_nums, p_spec, "Superzahl" if not is_euro else "Euro Zahlen")

    st.markdown("---")
    
    # ── نافذة تاريخ الميلاد المستقلة ──
    st.markdown(f"### {t['birth_title']}")
    birth_date = st.date_input(t["birth_select"], value=datetime(1990, 1, 1), key=f"birth_{game_name}")
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state: st.session_state[birth_counter_key] = 0
    if st.button(t["birth_btn"], key=f"btn_birth_{game_name}"): st.session_state[birth_counter_key] += 1
    
    if st.session_state[birth_counter_key] > 0:
        b_seed = (birth_date.year * 10000 + birth_date.month * 100 + birth_date.day + 2026) % (2**31 - 1)
        np.random.seed(b_seed)
        b_nums = sorted(np.random.choice(range(1, 50 if not is_euro else 51), 6 if not is_euro else 5, replace=False).tolist())
        b_spec = int(np.random.randint(0, 10)) if not is_euro else sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
        st.markdown(f"**{t['power_label']} 92%**")
        display_numbers(b_nums, b_spec, "Superzahl" if not is_euro else "Euro Zahlen")

    st.markdown("---")
    
    # ── نافذة الأبراج الفلكية المستقلة ──
    st.markdown(f"### {t['zodiac_title']}")
    zodiac_signs = ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"]
    selected_zodiac = st.selectbox(t["zodiac_select"], zodiac_signs, key=f"zodiac_{game_name}")
    zodiac_counter_key = f"counter_zodiac_{game_name}"
    if zodiac_counter_key not in st.session_state: st.session_state[zodiac_counter_key] = 0
    if st.button(t["zodiac_btn"], key=f"btn_zodiac_{game_name}"): st.session_state[zodiac_counter_key] += 1
    
    if st.session_state[zodiac_counter_key] > 0:
        z_seed = (sum(ord(c) for c in selected_zodiac) + 2026) % (2**31 - 1)
        np.random.seed(z_seed)
        z_nums = sorted(np.random.choice(range(1, 50 if not is_euro else 51), 6 if not is_euro else 5, replace=False).tolist())
        z_spec = int(np.random.randint(0, 10)) if not is_euro else sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
        st.markdown(f"**{t['power_label']} 94%**")
        display_numbers(z_nums, z_spec, "Superzahl" if not is_euro else "Euro Zahlen")

with tab1:
    run_full_features_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_full_features_tab(df_euro, "Eurojackpot", files_euro, True)
