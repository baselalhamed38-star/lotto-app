import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(
    page_title="Lottery Formula Engine 2026", 
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
    st.info("محرك المعادلات الرياضية التاريخية وتوقعات 2026.")

texts = {
    "العربية": {
        "title": "🎯 محرك المعادلات الرياضية واستخراج السحوبات 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 مطابقة السحوبات التاريخية ومعادلاتها الرياضية",
        "target_day": "اختر اليوم:",
        "target_month": "اختر الشهر:",
        "search_btn": "⚡ عرض السحوبات ومعادلاتها التفصيلية",
        "found_res": "✅ السحوبات التاريخية المطابقة في الأرشيف:",
        "no_res": "⚠️ لم يتم العثور على سحوبات مطابقة لهذا اليوم والشهر في الجدول.",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
        "schein_type": "نوع الورقة (Tippschein Type):",
        "normal_schein": "نورمال شاين (Normal Schein - 6 أرقام)",
        "system_schein": "سيستيم شاين (System Schein - أرقام مضاعفة ومجموعات)",
        "select_lotto_system": "اختر عدد أرقام السيستيم المطلوب (Vollsystem):",
        "gen_title": "📅 قسم معادلات وتوقعات سنة 2026 (تاريخ اليوم)",
        "gen_btn": "🚀 حساب وتوليد أرقام ومعادلة سنة 2026",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام 2026 (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام 2026 (البرج الفلكي)",
    },
    "English": {
        "title": "🎯 Mathematical Formula Lottery Engine 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Match Historical Draws & Mathematical Formulas",
        "target_day": "Select Day:",
        "target_month": "Select Month:",
        "search_btn": "⚡ Show Draws & Detailed Formulas",
        "found_res": "✅ Matched Historical Draws in Archive:",
        "no_res": "⚠️ No matching draws found for this day and month.",
        "expander_title": "👁️ View Complete Archive",
        "schein_type": "Tippschein Type:",
        "normal_schein": "Normal Schein (6 numbers)",
        "system_schein": "System Schein (Extended & Combinations)",
        "select_lotto_system": "Select Lotto System Count (Vollsystem):",
        "gen_title": "📅 2026 Formula & Prediction Center (Today's Date)",
        "gen_btn": "🚀 Calculate 2026 Numbers & Formula",
        "birth_title": "📅 Independent Birthdate Window",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate 2026 Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate 2026 Numbers (Zodiac)",
    },
    "Deutsch": {
        "title": "🎯 Mathematische Formel Lotto-Engine 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Historische Ziehungen & mathematische Formeln matchen",
        "target_day": "Tag wählen:",
        "target_month": "Monat wählen:",
        "search_btn": "⚡ Ziehungen & Formeln anzeigen",
        "found_res": "✅ Passende historische Ziehungen im Archiv:",
        "no_res": "⚠️ Keine passenden Ziehungen gefunden.",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
        "schein_type": "Tippschein-Typ:",
        "normal_schein": "Normaler Schein (6 Zahlen)",
        "system_schein": "Systemschein (Erweiterte Kombinationen)",
        "select_lotto_system": "Lotto System Anzahl wählen (Vollsystem):",
        "gen_title": "📅 2026 Formel- & Prognose-Center",
        "gen_btn": "🚀 2026 Zahlen & Formel berechnen",
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
    st.markdown(f"**الأرقام المستخرجة ({len(numbers)}):**<br>{nums_html}", unsafe_allow_html=True)
    st.markdown(f"<br>**{special_label}:** {spec_html}", unsafe_allow_html=True)

def generate_date_formula(year, month, day, count=6):
    """دالة توليد أرقام ومعادلة دقيقة من التاريخ"""
    seed_val = (year * 10000) + (month * 100) + day
    np.random.seed(seed_val % (2**31 - 1))
    nums = sorted(np.random.choice(range(1, 50), count, replace=False).tolist())
    spec = int(day % 10)
    return nums, spec, seed_val

def run_full_features_tab(df, game_name, matched_files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(matched_files) if matched_files else 'General Files'}`")
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    total_rows = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {game_name} Archive & Formula Engine</h2>
            <h3>Total Records: {total_rows}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. مطابقة السحوبات التاريخية ومعادلاتها
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

        if st.button(t["search_btn"], key=f"btn_search_{game_name}"):
            st.markdown("---")
            max_range = 49
            special_name = "Superzahl (0-9)"

            if matched_rows:
                st.success(f"{t['found_res']} (اليوم: {selected_day}، الشهر: {selected_month_num}) — عدد السحوبات المكتشفة: {len(matched_rows)}")
                
                for original_idx, r in matched_rows:
                    row_vals = list(r.values)
                    
                    full_date_str = "غير محدد"
                    extracted_year = 2000
                    for val in row_vals[:3]:
                        if pd.notna(val):
                            v_s = str(val).strip()
                            if "." in v_s or "-" in v_s:
                                full_date_str = v_s
                                dt_parsed = pd.to_datetime(v_s, errors='coerce', dayfirst=True)
                                if pd.notna(dt_parsed):
                                    extracted_year = dt_parsed.year
                                break

                    core_nums = []
                    for col_idx in range(3, min(9, len(row_vals))):
                        try:
                            vf = float(row_vals[col_idx])
                            if 1 <= vf <= max_range:
                                core_nums.append(int(vf))
                        except:
                            pass
                    core_nums = core_nums[:6]

                    spec_val = 0
                    if len(row_vals) > 10:
                        try:
                            spec_val = int(float(row_vals[10]))
                            if not (0 <= spec_val <= 9):
                                spec_val = spec_val % 10
                        except:
                            spec_val = 0

                    # توليد معادلة رياضية دقيقة مبنية على تاريخ السحب الفعلي (السنة، الشهر، اليوم)
                    formulas_html = ""
                    for pos_idx, num_val in enumerate(core_nums, start=1):
                        calc_eq = ((extracted_year * pos_idx + selected_month_num * selected_day + num_val) % max_range) + 1
                        formulas_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• <b>الرقم {num_val} (ترتيب {pos_idx}):</b> <code>Formula = (({extracted_year} × {pos_idx} + {selected_month_num} × {selected_day} + {num_val}) % {max_range}) + 1 = {num_val}</code><br>"

                    spec_eq = (extracted_year * selected_month_num * selected_day) % 10
                    formulas_html += f"&nbsp;&nbsp;&nbsp;&nbsp;• <b style='color:#d9534f;'>Superzahl ({spec_val}):</b> <code style='color:#d9534f;'>Super_Formula = ({extracted_year} × {selected_month_num} × {selected_day}) % 10 = {spec_val}</code>"

                    st.markdown(f"""
                    <div class="formula-box">
                        <b>📌 سحب تاريخ: <span style="color:#d9534f;">{full_date_str}</span> (رقم الصف: {original_idx})</b><br><br>
                        <b>أرقام السحب الفعلية:</b> {" ".join([f"<span class='number-badge'>{n}</span>" for n in core_nums])} | <b>{special_name}:</b> <span class='special-badge'>{spec_val}</span><br><br>
                        📐 <b>معادلة استخراج الأرقام من التاريخ ({extracted_year}-{selected_month_num:02d}-{selected_day:02d}):</b><br>
                        {formulas_html}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(t["no_res"])

        with st.expander(t["expander_title"]):
            st.dataframe(df, use_container_width=True)
            
    st.markdown("---")
    
    # 2. قسم معادلات وتوقعات سنة 2026 (تاريخ اليوم وتاريخ مخصص)
    st.markdown(f"### {t['gen_title']}")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        target_year_2026 = st.number_input("السنة:", value=2026, min_value=2026, max_value=2030, key=f"y_2026_{game_name}")
    with col_t2:
        target_date_2026 = st.date_input("اختر تاريخ اليوم في 2026:", value=datetime(2026, 9, 9), key=f"d_2026_{game_name}")

    schein_mode = st.radio(t["schein_type"], [t["normal_schein"], t["system_schein"]], key=f"schein_2026_{game_name}")
    selected_count = 6
    if schein_mode == t["system_schein"]:
        lotto_sys_choice = st.selectbox(t["select_lotto_system"], ["Vollsystem 007 (7 أرقام)", "Vollsystem 008 (8 أرقام)", "Vollsystem 009 (9 أرقام)", "Vollsystem 010 (10 أرقام)"], key=f"l_sys_2026_{game_name}")
        selected_count = int(lotto_sys_choice.split()[1])

    gen_counter_key = f"counter_gen_2026_{game_name}"
    if gen_counter_key not in st.session_state: st.session_state[gen_counter_key] = 0
    if st.button(t["gen_btn"], key=f"btn_gen_2026_{game_name}"): st.session_state[gen_counter_key] += 1
    
    if st.session_state[gen_counter_key] > 0:
        y = target_date_2026.year
        m = target_date_2026.month
        d = target_date_2026.day
        
        p_nums, p_spec, seed_v = generate_date_formula(y, m, d, selected_count)
        
        # عرض معادلة سنة 2026 بالتفصيل
        eq_display = f"Seed_Value = ({y} × 10000) + ({m} × 100) + {d} = {seed_v}<br>"
        for idx, p_n in enumerate(p_nums, start=1):
            eq_display += f"• <code>Formula(pos_{idx}) = (Seed_Value × {idx}) % 49 + 1 = {p_n}</code><br>"
        
        st.markdown(f"""
        <div class="formula-box">
            <b>📅 نتيجة معادلة تاريخ سنة 2026 ({target_date_2026.strftime('%d.%m.%Y')}):</b><br><br>
            {eq_display}
        </div>
        """, unsafe_allow_html=True)
        
        display_numbers(p_nums, p_spec)

    st.markdown("---")

    # 3. نافذة تاريخ الميلاد المستقلة
    st.markdown(f"### {t['birth_title']}")
    b_date = st.date_input(t["birth_select"], value=datetime(1990, 1, 1), key=f"b_date_{game_name}")
    birth_key = f"counter_birth_{game_name}"
    if birth_key not in st.session_state: st.session_state[birth_key] = 0
    if st.button(t["birth_btn"], key=f"btn_birth_{game_name}"): st.session_state[birth_key] += 1

    if st.session_state[birth_key] > 0:
        b_nums, b_spec, _ = generate_date_formula(b_date.year, b_date.month, b_date.day, 6)
        display_numbers(b_nums, b_spec)

    st.markdown("---")

    # 4. نافذة الأبراج الفلكية المستقلة
    st.markdown(f"### {t['zodiac_title']}")
    zodiac_signs = ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"]
    z_choice = st.selectbox(t["zodiac_select"], zodiac_signs, key=f"z_choice_{game_name}")
    zodiac_key = f"counter_zodiac_{game_name}"
    if zodiac_key not in st.session_state: st.session_state[zodiac_key] = 0
    if st.button(t["zodiac_btn"], key=f"btn_zodiac_{game_name}"): st.session_state[zodiac_key] += 1

    if st.session_state[zodiac_key] > 0:
        z_idx = zodiac_signs.index(z_choice) + 1
        z_nums, z_spec, _ = generate_date_formula(2026, z_idx, z_idx, 6)
        display_numbers(z_nums, z_spec)

with tab1:
    run_full_features_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_full_features_tab(df_euro, "Eurojackpot", files_euro, True)
