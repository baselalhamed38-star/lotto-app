import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(
    page_title="Lottery Exact Historical Engine", 
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
    .draw-box {
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
    st.info("محرك استخراج سحوبات التاريخ المطابقة لنفس اليوم والشهر.")

texts = {
    "العربية": {
        "title": "🎯 محرك استخراج السحوبات التاريخية حسب اليوم والشهر",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 مطابقة واستخراج سحوبات نفس اليوم والشهر عبر كل السنوات",
        "target_day": "اختر اليوم:",
        "target_month": "اختر الشهر:",
        "search_btn": "🔍 عرض كافة السحوبات التاريخية لهذا اليوم والشهر",
        "found_res": "✅ السحوبات التاريخية المطابقة في الأرشيف:",
        "no_res": "⚠️ لم يتم العثور على سحوبات مطابقة لهذا اليوم والشهر في الجدول.",
        "expander_title": "👁️ استعراض أرشيف السحوبات الكامل",
    },
    "English": {
        "title": "🎯 Historical Draws Extraction Engine by Day & Month",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Match & Extract Draws for Same Day & Month Across Years",
        "target_day": "Select Day:",
        "target_month": "Select Month:",
        "search_btn": "🔍 Show All Historical Draws for This Day & Month",
        "found_res": "✅ Matched Historical Draws in Archive:",
        "no_res": "⚠️ No matching draws found for this day and month in the table.",
        "expander_title": "👁️ View Complete Archive",
    },
    "Deutsch": {
        "title": "🎯 Historische Ziehungs-Extraktions-Engine nach Tag & Monat",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Zugehörige Dateien:",
        "search_title": "📅 Ziehungen für denselben Tag & Monat über alle Jahre matchen",
        "target_day": "Tag wählen:",
        "target_month": "Monat wählen:",
        "search_btn": "🔍 Alle historischen Ziehungen für diesen Tag & Monat anzeigen",
        "found_res": "✅ Passende historische Ziehungen im Archiv:",
        "no_res": "⚠️ Keine passenden Ziehungen für diesen Tag und Monat gefunden.",
        "expander_title": "👁️ Vollständiges Archiv anzeigen",
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

def display_numbers(numbers, special_num, special_label="Superzahl"):
    nums_html = "".join([f"<span class='number-badge'>{num}</span>" for num in numbers])
    spec_html = f"<span class='special-badge'>{special_num}</span>"
    st.markdown(f"**أرقام السحب الأساسية:** {nums_html}", unsafe_allow_html=True)
    st.markdown(f"**{special_label}:** {spec_html}", unsafe_allow_html=True)

def run_archive_search_tab(df, game_name, matched_files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(matched_files) if matched_files else 'General Files'}`")
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    total_rows = len(df)
    st.markdown(f"""
        <div class="metric-card">
            <h2>📊 {game_name} Historical Archive</h2>
            <h3>Total Records: {total_rows}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"### {t['search_title']}")
        col_d, col_m = st.columns(2)
        with col_d:
            selected_day = st.selectbox(t["target_day"], list(range(1, 32)), index=0, key=f"s_day_{game_name}")
        with col_m:
            months_dict = {
                "يناير (01)": 1, "فبراير (02)": 2, "مارس (03)": 3, "أبريل (04)": 4,
                "مايو (05)": 5, "يونيو (06)": 6, "يوليو (07)": 7, "أغسطس (08)": 8,
                "سبتمبر (09)": 9, "أكتوبر (10)": 10, "نوفمبر (11)": 11, "ديسمبر (12)": 12
            }
            selected_month_name = st.selectbox(t["target_month"], list(months_dict.keys()), index=10, key=f"s_mon_{game_name}")
            selected_month_num = months_dict[selected_month_name]
            
        matched_rows = []
        if not df.empty:
            for idx, row in df.iterrows():
                is_matched = False
                for val in row.values:
                    if pd.notna(val):
                        v_str = str(val)
                        if (f".{selected_month_num:02d}.{selected_day:02d}" in v_str or 
                            f"-{selected_month_num:02d}-{selected_day:02d}" in v_str or 
                            f"{selected_day:02d}.{selected_month_num:02d}." in v_str):
                            is_matched = True
                            break
                        dt = pd.to_datetime(val, errors='coerce')
                        if pd.notna(dt) and dt.day == selected_day and dt.month == selected_month_num:
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
                    
                    # استخراج التاريخ إن وجد في الصف (لبحثه وعرضه بدقة)
                    full_date_str = "غير محدد"
                    for val in row_vals[:3]:
                        dt = pd.to_datetime(val, errors='coerce')
                        if pd.notna(dt):
                            full_date_str = dt.strftime('%d.%m.%Y')
                            break
                        elif pd.notna(val) and ("." in str(val) or "-" in str(val)):
                            full_date_str = str(val)
                            break

                    # استخراج الأرقام الأساسية بدقة من الأعمدة D إلى I (الإندكس 3 إلى 8 في بايثون)
                    core_nums = []
                    for col_idx in range(3, min(9, len(row_vals))):
                        try:
                            vf = float(row_vals[col_idx])
                            if 1 <= vf <= max_range:
                                core_nums.append(int(vf))
                        except:
                            pass
                    core_nums = core_nums[:6]

                    # استخراج الـ Superzahl بدقة من العمود K (الإندكس 10)
                    spec_val = 0
                    if len(row_vals) > 10:
                        try:
                            spec_val = int(float(row_vals[10]))
                            if not (0 <= spec_val <= 9):
                                spec_val = spec_val % 10
                        except:
                            spec_val = 0

                    st.markdown(f"""
                    <div class="draw-box">
                        <b>📌 سحب تاريخ: <span style="color:#d9534f;">{full_date_str}</span> (رقم الصف في الملف: {original_idx})</b><br><br>
                        <b>أرقام السحب الفعلية:</b> {" ".join([f"<span class='number-badge'>{n}</span>" for n in core_nums])}<br>
                        <b>{special_name}:</b> <span class='special-badge'>{spec_val}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(t["no_res"])

        with st.expander(t["expander_title"]):
            st.dataframe(df, use_container_width=True)

with tab1:
    run_archive_search_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_archive_search_tab(df_euro, "Eurojackpot", files_euro, True)
