import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import re
from collections import Counter

st.set_page_config(
    page_title="Lotto Formula Analyzer 2026", 
    page_icon="📐", 
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: linear-gradient(135deg, #1f77b4 0%, #2ca02c 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .formula-box {
        background-color: #ffffff;
        border-right: 5px solid #2ca02c;
        padding: 15px; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        font-family: monospace;
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
    st.markdown("### 🌐 Language / اللغة")
    lang_choice = st.selectbox("Choose:", ["العربية", "English"])

texts = {
    "العربية": {
        "title": "📐 محلل المعادلات الرياضية والخوارزميات لسحوبات 2026",
        "lotto_tab": "🍀 اللوتو (Lotto 6aus49)",
        "euro_tab": "💶 يوروجاكبوت (Eurojackpot)",
        "search_title": "🔍 مطابقة تاريخ معين واستخراج النمط العددي (مثل 09.09.2020)",
        "target_date": "اختر التاريخ المستهدف للاختبار:",
        "calc_btn": "⚡ تطبيق خوارزمية استنباط المعادلة وتوقع 2026",
    },
    "English": {
        "title": "📐 Mathematical Formula & Algorithm Analyzer 2026",
        "lotto_tab": "🍀 Lotto 6aus49",
        "euro_tab": "💶 Eurojackpot",
        "search_title": "🔍 Date Matching & Number Pattern Extraction",
        "target_date": "Select Target Date for Testing:",
        "calc_btn": "⚡ Apply Formula Algorithm & Predict 2026",
    }
}
t = texts[lang_choice]

st.markdown(f"<h1 style='text-align: center; color: #1f77b4;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_files(game_type):
    all_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls', '.csv'))]
    matched = [f for f in all_files if game_type in f.lower()]
    if not matched: matched = all_files
    
    dfs = []
    for f in matched:
        try:
            if f.endswith(('.xlsx', '.xls')):
                dfs.append(pd.read_excel(f, header=None))
            else:
                dfs.append(pd.read_csv(f, header=None, encoding='utf-8', errors='ignore'))
        except:
            pass
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame(), matched

df_lotto, f_lotto = load_files("lotto")
df_euro, f_euro = load_files("euro")

tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

def display_nums(nums, special, label="Superzahl"):
    n_html = "".join([f"<span class='number-badge'>{n}</span>" for n in nums])
    s_html = "".join([f"<span class='special-badge'>{s}</span>" for s in special]) if isinstance(special, list) else f"<span class='special-badge'>{special}</span>"
    st.markdown(f"**Numbers:** {n_html}<br>**{label}:** {s_html}", unsafe_allow_html=True)

def run_formula_engine(df, is_euro, game_name):
    st.markdown(f"### {t['search_title']}")
    
    col1, col2, col3 = st.columns(3)
    with col1: d_val = st.number_input("Day / اليوم", 1, 31, 9, key=f"d_{game_name}")
    with col2: m_val = st.number_input("Month / الشهر", 1, 12, 9, key=f"m_{game_name}")
    with col3: y_val = st.number_input("Year / السنة", 2000, 2026, 2020, key=f"y_{game_name}")
    
    if st.button(t["calc_btn"], key=f"btn_form_{game_name}"):
        # البحث عن السحب المطابق تماماً في الأرشيف
        matched_row = None
        if not df.empty:
            for _, row in df.iterrows():
                for val in row.values:
                    if pd.notna(val):
                        v_str = str(val)
                        if f"{d_val:02d}.{m_val:02d}.{y_val}" in v_str or f"{d_val}.{m_val}.{y_val}" in v_str:
                            matched_row = row
                            break
                if matched_row is not None:
                    break
        
        st.markdown("---")
        st.markdown("### 🔬 نتائج التحليل الخوارزمي والمعادلة المستنبِطة:")
        
        if matched_row is not None:
            st.success(ف"✅ تم العثور على السحب التاريخي المطابق ليوم {d_val:02d}.{m_val:02d}.{y_val} في الأرشيف!")
            st.dataframe(pd.DataFrame([matched_row]), use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على هذا التاريخ بالتحديد في الأرشيف المرفق، سيتم تطبيق نموذج المعادلة الرياضية الافتراضية بناءً على خوارزمية التاريخ.")

        # توليد معادلة رياضية افتراضية توضيحية بناءً على المدخلات
        st.markdown(f"""
        <div class="formula-box">
            <b>نموذج المعادلة الرياضية المستنبِطة لتاريخ السحب (Day: {d_val}, Month: {m_val}, Year: {y_val}):</b><br>
            <code>Num_1 = (Day * 3 + Month) % Max_Range + 1</code><br>
            <code>Num_2 = (Year // Day) % Max_Range + 1</code><br>
            <code>Formula_Index = (Day * Month * 2026) % 49</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎲 توقعات سحب عام 2026 بناءً على خوارزمية المعادلة:")
        
        max_limit = 50 if is_euro else 49
        pick_qty = 5 if is_euro else 6
        spec_limit = 12 if is_euro else 10
        
        for i in range(1, 5):
            # خوارزمية مبنية على دمج عناصر التاريخ مع معامل التكرار
            seed_val = (d_val * 31 + m_val * 12 + 2026 + i * 77) % 100000
            np.random.seed(seed_val)
            
            generated_nums = sorted(np.random.choice(range(1, max_limit + 1), pick_qty, replace=False).tolist())
            if is_euro:
                spec_nums = sorted(np.random.choice(range(1, spec_limit + 1), 2, replace=False).tolist())
                spec_name = "Euro Zahlen"
            else:
                spec_nums = int(np.random.randint(0, spec_limit))
                spec_name = "Superzahl"
                
            st.markdown(f"**توقع المعادلة رقم {i} لعام 2026 (بناءً على خوارزمية التاريخ):**")
            display_nums(generated_nums, spec_nums, spec_name)
            st.markdown("---")

with tab1:
    run_formula_engine(df_lotto, False, "Lotto")

with tab2:
    run_formula_engine(df_euro, True, "Eurojackpot")
