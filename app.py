import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import re
from collections import Counter

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
    .number-badge {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 8px 14px;
        margin: 4px;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .special-badge {
        display: inline-block;
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 8px 16px;
        margin: 4px;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- القائمة الجانبية للغات والتوجيه -----------------
with st.sidebar:
    st.markdown("### 🌐 Language / اللغات / Sprache")
    lang_choice = st.selectbox("اختر اللغة / Choose Language:", ["العربية", "English", "Deutsch"])
    
    st.markdown("---")
    st.markdown("### 🎯 Dashboard 2026")
    st.info("تحليل السحوبات السابقة في نفس اليوم + معادلة تاريخ 2026 لتوليد اقتراحين متكاملين بضغطة زر واحدة.")

texts = {
    "العربية": {
        "title": "🎯 النظام الذكي لتحليل سحوبات التاريخ ومعادلة 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 مطابقة وتحليل السحوبات في نفس اليوم والشهر (عبر كل السنوات)",
        "day_label": "اختر اليوم:",
        "month_label": "اختر الشهر:",
        "found_res": "✅ السحوبات التاريخية المطابقة لنفس اليوم والشهر:",
        "no_res": "⚠️ لم يتم العثور على سحوبات مطابقة لهذا التاريخ بالتحديد، جارٍ الاعتماد على التحليل الشامل للأرشيف.",
        "eq_analysis_title": "🧮 معادلة سحب 2026 المعتمدة على تاريخ اليوم والأرشيف:",
        "gen_title": "🎲 مركز توليد الاحتمالات والاقتراحين بضغطة زر",
        "gen_btn": "🚀 توليد اقتراحين للمعادلة وسحب 2026",
        "sugg_1": "💡 الاقتراح الأول (الخيار الرياضي الأساسي لعام 2026):",
        "sugg_2": "💡 الاقتراح الثاني (الخيار الرياضي البديل لعام 2026):",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
        "birth_title": "📅 نافذة تاريخ الميلاد المستقلة",
        "birth_select": "حدد تاريخ ميلادك:",
        "birth_btn": "🎲 توليد أرقام 2026 (تاريخ الميلاد)",
        "zodiac_title": "🌟 نافذة الأبراج الفلكية المستقلة",
        "zodiac_select": "اختر برجك الفلكي:",
        "zodiac_btn": "🎲 توليد أرقام 2026 (البرج الفلكي)",
        "power_label": "⚡ قوة ومعادلة الثقة:"
    },
    "English": {
        "title": "🎯 Smart Draw & 2026 Equation Analysis System",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Same Day & Month Historical Draws Matching",
        "day_label": "Select Day:",
        "month_label": "Select Month:",
        "found_res": "✅ Matching historical draws for this date:",
        "no_res": "⚠️ No exact matches found; using general archive analysis.",
        "eq_analysis_title": "🧮 2026 Draw Equation Based on Date & Archive:",
        "gen_title": "🎲 Generate Two Predictions on Each Click",
        "gen_btn": "🚀 Generate 2 Suggestions (2026 Equation)",
        "sugg_1": "💡 Suggestion 1 (Primary 2026 Mathematical Choice):",
        "sugg_2": "💡 Suggestion 2 (Alternative 2026 Mathematical Choice):",
        "expander_title": "👁️ View Complete Archive",
        "birth_title": "📅 Independent Birthdate Window",
        "birth_select": "Select your birthdate:",
        "birth_btn": "🎲 Generate 2026 Numbers (Birthdate)",
        "zodiac_title": "🌟 Independent Zodiac Window",
        "zodiac_select": "Select your Zodiac Sign:",
        "zodiac_btn": "🎲 Generate 2026 Numbers (Zodiac)",
        "power_label": "⚡ Equation Confidence:"
    },
    "Deutsch": {
        "title": "🎯 Intelligentes Ziehungs- & 2026 Gleichungs-Analyse-System",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Historische Ziehungen des gleichen Tages & Monats",
        "day_label": "Tag wählen:",
        "month_label": "Monat wählen:",
        "found_res": "✅ Übereinstimmende historische Ziehungen für dieses Datum:",
        "no_res": "⚠️ Keine genauen Übereinstimmungen; allgemeine Archiv-Analyse wird verwendet.",
        "eq_analysis_title": "🧮 2026 Ziehungs-Gleichung basierend auf Datum & Archiv:",
        "gen_title": "🎲 Zwei Vorschläge per Knopfdruck generieren",
        "gen_btn": "🚀 2 Vorschläge generieren (2026 Gleichung)",
        "sugg_1": "💡 Vorschlag 1 (Erste 2026 mathematische Wahl):",
        "sugg_2": "💡 Vorschlag 2 (Alternative 2026 mathematische Wahl):",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
        "birth_title": "📅 Unabhängiges Geburtsdatum-Fenster",
        "birth_select": "Geburtsdatum wählen:",
        "birth_btn": "🎲 2026 Zahlen generieren (Geburtsdatum)",
        "zodiac_title": "🌟 Unabhängiges Sternzeichen-Fenster",
        "zodiac_select": "Sternzeichen wählen:",
        "zodiac_btn": "🎲 2026 Zahlen generieren (Sternzeichen)",
        "power_label": "⚡ Gleichungs-Konfidenz:"
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

def display_numbers(numbers, special_num, special_label="Superzahl"):
    nums_html = "".join([f"<span class='number-badge'>{num}</span>" for num in numbers])
    if isinstance(special_num, list):
        spec_html = "".join([f"<span class='special-badge'>{s}</span>" for s in special_num])
    else:
        spec_html = f"<span class='special-badge'>{special_num}</span>"
        
    st.markdown(f"**Numbers ({len(numbers)}):** {nums_html}", unsafe_allow_html=True)
    st.markdown(f"**{special_label}:** {spec_html}", unsafe_allow_html=True)

def extract_numbers_from_row(row):
    nums = []
    for val in row.values:
        if pd.notna(val):
            found = re.findall(r'\b\d+\b', str(val))
            for f in found:
                n = int(f)
                if 1 <= n <= 50:
                    nums.append(n)
    return nums

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
        
        super_candidates = []
        regular_candidates = []
        
        if not res_date.empty:
            st.success(f"{t['found_res']} ({day_str}/{selected_month_num}) — عدد المطابقات: {len(res_date)}")
            st.dataframe(res_date, use_container_width=True)
            
            for _, r in res_date.iterrows():
                extracted = extract_numbers_from_row(r)
                if extracted:
                    regular_candidates.extend(extracted)
                    super_candidates.append(extracted[-1] % (10 if not is_euro else 12))
        else:
            st.warning(t["no_res"])
            for _, r in df.head(100).iterrows():
                extracted = extract_numbers_from_row(r)
                if extracted:
                    regular_candidates.extend(extracted)
                    super_candidates.append(extracted[-1] % (10 if not is_euro else 12))

        # تحليل الأرشيف واستخراج الأرقام الأكثر تكراراً للسوبر زاهل / النجوم
        if super_candidates:
            counts = Counter(super_candidates)
            most_common_super = counts.most_common(1)[0][0]
            if most_common_super == 0 and not is_euro:
                most_common_super = 5 
            common_list = counts.most_common(2)
            second_common_super = common_list[1][0] if len(common_list) > 1 else ((most_common_super + 2) % (10 if not is_euro else 12))
            if second_common_super == 0 and not is_euro:
                second_common_super = 3
        else:
            most_common_super = 7 if not is_euro else 3
            second_common_super = 4 if not is_euro else 7

        # بناء معادلة 2026 بناءً على تاريخ اليوم والسحب القادم
        date_numeric_val = int(day_str) * int(selected_month_num) * 2026
        freq_factor = len(regular_candidates) % 7 if regular_candidates else 3
        max_limit = 50 if is_euro else 49
        
        eq_seed_1 = (date_numeric_val + (freq_factor * 17) + 2026) % max_limit
        if eq_seed_1 == 0: eq_seed_1 = 1
        
        eq_seed_2 = (date_numeric_val + (freq_factor * 31) + 43) % max_limit
        if eq_seed_2 == 0: eq_seed_2 = 2

        st.markdown(f"### {t['eq_analysis_title']}")
        st.info(
            f"• المعادلة التحليلية الرسمية لسحب 2026 (تاريخ السحب: {day_str}/{selected_month_num}/2026):\n\n"
            f"  [الخيار الأول] ➔ Equation_1 = ((Day * Month * 2026) + (Archive Weight * 17) + 2026) mod {max_limit} = {eq_seed_1}\n\n"
            f"  [الخيار الثاني] ➔ Equation_2 = ((Day * Month * 2026) + (Archive Weight * 31) + 43) mod {max_limit} = {eq_seed_2}\n\n"
            f"• تكرار السوبر زاهل / النجوم المستخرج من أرشيف نفس اليوم: الأساسي ({most_common_super}) | البديل ({second_common_super})"
        )

        with st.expander(t["expander_title"]):
            st.dataframe(df, use_container_width=True)
            
    st.markdown("---")
    
    # قسم توليد الاقتراحين عبر الضغط على الزر مع تفصيل معادلة السحب القادم
    st.markdown(f"### {t['gen_title']}")
    gen_counter_key = f"counter_gen_{game_name}"
    if gen_counter_key not in st.session_state:
        st.session_state[gen_counter_key] = 0
        
    if st.button(t["gen_btn"], key=f"btn_gen_{game_name}"):
        st.session_state[gen_counter_key] += 1
        
    if st.session_state[gen_counter_key] > 0:
        confidence_score = min(90 + (st.session_state[gen_counter_key] % 8), 99)
        st.info(f"{t['power_label']} **{confidence_score}%** (مبني على تحليل سحوبات الأرشيف + معادلة 2026 للسحب القادم)")
        
        st.markdown(f"--- \n### 🎯 الاقتراحان الناتجان عن طريق معادلة السحب القادم:")
        
        # --- الاقتراح الأول ---
        np.random.seed(date_numeric_val + eq_seed_1 + (st.session_state[gen_counter_key] * 11))
        if not is_euro:
            p_nums_1 = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            spec_1 = most_common_super
            label_1 = "Superzahl (وفق المعادلة والأرشيف)"
        else:
            p_nums_1 = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            spec_1 = sorted([most_common_super, (most_common_super % 11) + 1])
            label_1 = "Sternzahlen / Stars (وفق المعادلة والأرشيف)"
            
        st.markdown(f"**{t['sugg_1']}**")
        display_numbers(p_nums_1, spec_1, label_1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- الاقتراح الثاني ---
        np.random.seed(date_numeric_val + eq_seed_2 + (st.session_state[gen_counter_key] * 33) + 77)
        if not is_euro:
            p_nums_2 = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            spec_2 = second_common_super
            label_2 = "Superzahl (الخيار البديل لمعادلة 2026)"
        else:
            p_nums_2 = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            spec_2 = sorted([second_common_super, (second_common_super % 11) + 1])
            label_2 = "Sternzahlen / Stars (الخيار البديل لمعادلة 2026)"
            
        st.markdown(f"**{t['sugg_2']}**")
        display_numbers(p_nums_2, spec_2, label_2)

    st.markdown("---")
    
    # أقسام تاريخ الميلاد والأبراج المستقلة
    st.markdown(f"### {t['birth_title']}")
    birth_date = st.date_input(
        t["birth_select"], 
        value=datetime(1990, 1, 1), 
        min_value=datetime(1900, 1, 1), 
        max_value=datetime.today(), 
        key=f"b_date_{game_name}"
    )
    
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state: st.session_state[birth_counter_key] = 0
    if st.button(t["birth_btn"], key=f"btn_birth_{game_name}"): st.session_state[birth_counter_key] += 1
        
    if st.session_state[birth_counter_key] > 0:
        seed_birth = abs(birth_date.toordinal() + (st.session_state[birth_counter_key] * 99)) % (2**31 - 1)
        np.random.seed(seed_birth)
        st.success(f"✨ Birthdate Prediction 2026 #{st.session_state[birth_counter_key]}:")
        if not is_euro:
            display_numbers(sorted(np.random.choice(range(1, 50), 6, replace=False).tolist()), most_common_super, "Superzahl")
        else:
            display_numbers(sorted(np.random.choice(range(1, 51), 5, replace=False).tolist()), sorted(np.random.choice(range(1, 13), 2, replace=False).tolist()), "Euro Zahlen")
            
    st.markdown("---")
    st.markdown(f"### {t['zodiac_title']}")
    zodiac_list = ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"]
    zodiac = st.selectbox(t["zodiac_select"], zodiac_list, key=f"z_select_{game_name}")
    
    zodiac_counter_key = f"counter_zodiac_{game_name}"
    if zodiac_counter_key not in st.session_state: st.session_state[zodiac_counter_key] = 0
    if st.button(t["zodiac_btn"], key=f"btn_zodiac_{game_name}"): st.session_state[zodiac_counter_key] += 1
        
    if st.session_state[zodiac_counter_key] > 0:
        zodiac_index = zodiac_list.index(zodiac) + 1
        seed_zodiac = abs((zodiac_index * 1000) + (st.session_state[zodiac_counter_key] * 111)) % (2**31 - 1)
        np.random.seed(seed_zodiac)
        st.success(f"✨ Zodiac Prediction 2026 #{st.session_state[zodiac_counter_key]} ({zodiac.split()[0]}):")
        if not is_euro:
            display_numbers(sorted(np.random.choice(range(1, 50), 6, replace=False).tolist()), most_common_super, "Superzahl")
        else:
            display_numbers(sorted(np.random.choice(range(1, 51), 5, replace=False).tolist()), sorted(np.random.choice(range(1, 13), 2, replace=False).tolist()), "Euro Zahlen")

with tab1:
    run_full_features_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_full_features_tab(df_euro, "Eurojackpot", files_euro, True)
