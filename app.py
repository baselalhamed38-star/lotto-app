import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import re
from collections import Counter

# إعدادات الصفحة
st.set_page_config(
    page_title="Lottery & Eurojackpot Analytics 2026", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم الواجهة والتنسيقات
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .analysis-box {
        background-color: #ffffff;
        border-right: 5px solid #1f77b4;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .number-badge {
        display: inline-block;
        background-color: #1f77b4;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 6px 12px;
        margin: 3px;
        border-radius: 50px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .special-badge {
        display: inline-block;
        background-color: #ff4b4b;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 6px 14px;
        margin: 3px;
        border-radius: 50px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# القائمة الجانبية لاختيار اللغة
with st.sidebar:
    st.markdown("### 🌐 Language / اللغات")
    lang_choice = st.selectbox("اختر اللغة / Choose Language:", ["العربية", "English"])
    st.markdown("---")
    st.info("محرك التحليل الحقيقي لمعادلات الأرشيف وتاريخ السحوبات لعام 2026.")

texts = {
    "العربية": {
        "title": "🎯 النظام الذكي لتحليل الأرشيف ومعادلات السحب لعام 2026",
        "lotto_tab": "🍀 اللوتو (Lotto)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "file_info": "📁 الملفات المرتبطة بالقاعدة:",
        "search_title": "📅 البحث الدقيق في الأرشيف لنفس اليوم والشهر عبر السنين",
        "day_label": "اختر اليوم:",
        "month_label": "اختر الشهر:",
        "found_res": "✅ السحوبات التاريخية المسجلة في نفس اليوم والشهر:",
        "no_res": "⚠️ لا توجد سحوبات مطابقة لهذا التاريخ بالتحديد، سيعتمد المحرك على الأرشيف العام.",
        "analysis_engine_title": "🔬 محرك التحليل الرياضي والأوزان والترددات لأرشيف السحوبات",
        "analysis_btn": "🔍 تحليل الأرشيف وتطبيق معادلة الأوزان وتوليد 4 احتمالات 2026",
        "gen_title": "🎲 مركز توليد التوقعات الذكية",
        "gen_btn": "🚀 توليد الأرقام والتحليل الاعتيادي",
    },
    "English": {
        "title": "🎯 Archive Analytics & Draw Equation System 2026",
        "lotto_tab": "🍀 Lotto",
        "euro_tab": "💶 Eurojackpot",
        "file_info": "📁 Associated Files:",
        "search_title": "📅 Historical Date Search (Day & Month Across Years)",
        "day_label": "Select Day:",
        "month_label": "Select Month:",
        "found_res": "✅ Historical draws found for this day and month:",
        "no_res": "⚠️ No matching draws for this exact date; fallback to general archive active.",
        "analysis_engine_title": "🔬 Mathematical Frequency & Weighting Analysis Engine",
        "analysis_btn": "🔍 Analyze Archive, Apply Weight Equation & Generate 4 Probabilities",
        "gen_title": "🎲 Smart Prediction Center",
        "gen_btn": "🚀 Generate Numbers & Analysis",
    }
}
t = texts[lang_choice]

st.markdown(f"<h1 style='text-align: center; color: #1f77b4;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_game_files(game_type):
    all_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls', '.csv'))]
    matched_files = [f for f in all_files if game_type in f.lower()] or all_files
    
    all_draws = []
    for file_name in matched_files:
        try:
            if file_name.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(file_name)
                for sheet_name in xls.sheet_names:
                    df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                    if not df_sheet.empty:
                        all_draws.append(df_sheet)
            elif file_name.endswith('.csv'):
                df_csv = pd.read_csv(file_name, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty:
                    all_draws.append(df_csv)
        except Exception:
            pass
    return pd.concat(all_draws, ignore_index=True) if all_draws else pd.DataFrame(), matched_files

df_lotto, files_lotto = load_game_files("lotto")
df_euro, files_euro = load_game_files("euro" if "euro" in "".join(os.listdir('.')) else "ej")

tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

def display_numbers(numbers, special_num, special_label="Superzahl"):
    nums_html = "".join([f"<span class='number-badge'>{num}</span>" for num in numbers])
    spec_html = "".join([f"<span class='special-badge'>{s}</span>" for s in special_num]) if isinstance(special_num, list) else f"<span class='special-badge'>{special_num}</span>"
    st.markdown(f"**Numbers:** {nums_html}<br>**{special_label}:** {spec_html}", unsafe_allow_html=True)

def filter_by_date(df, target_day, target_month):
    matched = []
    for _, row in df.iterrows():
        for col_idx in [0, 1]:
            if len(row) > col_idx and pd.notna(row.iloc[col_idx]):
                val_str = str(row.iloc[col_idx]).strip()
                try:
                    dt = pd.to_datetime(val_str, errors='coerce')
                    if pd.notna(dt) and dt.day == target_day and dt.month == target_month:
                        matched.append(row)
                        break
                except:
                    pass
                if f"{target_day}.{target_month}" in val_str or f"{target_day}/{target_month}" in val_str:
                    matched.append(row)
                    break
    return pd.DataFrame(matched) if matched else pd.DataFrame(columns=df.columns)

def run_analytics_tab(df, game_name, files, is_euro=False):
    st.info(f"{t['file_info']} `{' , '.join(files) if files else 'General Files'}`")
    if df.empty:
        st.error(f"⚠️ No files found for {game_name}.")
        return
        
    st.markdown(f"<div class='metric-card'><h2>📊 {game_name} Archive</h2><h3>Total Draws: {len(df)}</h3></div>", unsafe_allow_html=True)
    
    col_d, col_m = st.columns(2)
    with col_d:
        selected_day = st.selectbox(t["day_label"], list(range(1, 32)), key=f"d_{game_name}")
    with col_m:
        months = {"يناير": 1, "فبراير": 2, "مارس": 3, "أبريل": 4, "مايو": 5, "يونيو": 6, "يوليو": 7, "أغسطس": 8, "سبتمبر": 9, "أكتوبر": 10, "نوفمبر": 11, "ديسمبر": 12}
        selected_month_name = st.selectbox(t["month_label"], list(months.keys()), key=f"m_{game_name}")
        selected_month_num = months[selected_month_name]
        
    res_date = filter_by_date(df, selected_day, selected_month_num)
    if not res_date.empty:
        st.success(f"{t['found_res']} ({len(res_date)} draws)")
    else:
        st.warning(t["no_res"])
        
    st.markdown("---")
    st.markdown(f"### {t['analysis_engine_title']}")
    
    if st.button(t["analysis_btn"], key=f"btn_ana_{game_name}"):
        # حساب الترددات والأوزان
        exact_numbers = []
        for _, r in res_date.iterrows():
            for val in r.values:
                if pd.notna(val):
                    for n in re.findall(r'\b\d{1,2}\b', str(val)):
                        num = int(n)
                        if 1 <= num <= (50 if is_euro else 49):
                            exact_numbers.append(num)
                            
        all_numbers = []
        for _, r in df.iterrows():
            for val in r.values:
                if pd.notna(val):
                    for n in re.findall(r'\b\d{1,2}\b', str(val)):
                        num = int(n)
                        if 1 <= num <= (50 if is_euro else 49):
                            all_numbers.append(num)
                            
        c_exact = Counter(exact_numbers)
        c_all = Counter(all_numbers)
        
        # تطبيق معادلة الأوزان W(N) لكل رقم متاح
        max_limit = 50 if is_euro else 49
        weights = {}
        for num in range(1, max_limit + 1):
            f_date = c_exact.get(num, 0)
            f_global = c_all.get(num, 0)
            # معادلة الأوزان المذكورة
            weights[num] = (f_date * 5) + (f_global * 1) + ((selected_day + selected_month_num) / (num + 1))
            
        sorted_weighted_nums = sorted(weights.keys(), key=lambda x: weights[x], reverse=True)
        
        st.markdown(f"""
        <div class="analysis-box">
            <h4>📋 نتائج تطبيق معادلة الأوزان والترددات:</h4>
            <ul>
                <li><b>الأرقام الأعلى وزناً بناءً على تاريخ ({selected_day:02d}/{selected_month_num:02d}):</b> <code>{sorted_weighted_nums[:6]}</code></li>
                <li><b>آلية الاختيار:</b> تم دمج التردد التاريخي الموسمي مع التردد العام في الأرشيف وتطبيق عامل التصحيح الزمني لتوليد خيارات 2026 بدقة.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 الاحتمالات الـ 4 المستخرجة بمعادلة الأوزان لعام 2026:")
        pick_count = 5 if is_euro else 6
        
        for i in range(1, 5):
            np.random.seed(2026 + selected_day + selected_month_num + (i * 77))
            # اختيار أرقام مأخوذة من أعلى الأرقام وزناً مع تنوع عشوائي مدروس
            top_pool = sorted_weighted_nums[:25]
            chosen = sorted(np.random.choice(top_pool, pick_count, replace=False).tolist())
            spec = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist()) if is_euro else int(np.random.randint(0, 10))
            
            st.markdown(f"**الاحتمال الرياضي رقم {i}:**")
            display_numbers(chosen, spec, "Stars / Superzahl")
            st.markdown("---")

with tab1:
    run_analytics_tab(df_lotto, "Lotto", files_lotto, False)

with tab2:
    run_analytics_tab(df_euro, "Eurojackpot", files_euro, True)
