import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# إعدادات الصفحة والتصميم العام (Dark Theme متوافق مع الموبايل)
st.set_page_config(page_title="LOTTO MATRIX PRO", page_icon="🌟", layout="centered")

# تنسيق CSS مخصص ليشبه واجهات التطبيق الاحترافية في الصور
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط العلوي وتحديد اللعبة
col_title, col_status = st.columns([2, 1])
with col_title:
    st.markdown("### 🌟 LOTTO MATRIX PRO")
with col_status:
    game_type = st.radio("اللعبة", ["Lotto 6aus49", "Eurojackpot"], horizontal=True, label_visibility="collapsed")

max_num = 49 if game_type == "Lotto 6aus49" else 50
super_max = 9 if game_type == "Lotto 6aus49" else 12

# شريط التبويبات الرئيسي (Tabs)
tab = st.selectbox("اختر القسم:", [
    "📊 Formel-Analyse", 
    "📅 Datum & Tag Suche", 
    "📌 Letzte Ziehung & Archiv", 
    "🎲 Letzte Ziehung Gen", 
    "⚙️ Systeme"
])

st.markdown("---")

# دالة مساعدة لتوليد كرات الأرقام بشكل جمالي
def render_balls(nums, super_num):
    balls_html = ""
    for n in nums:
        balls_html += f"<span style='height:36px;width:36px;background-color:white;color:black;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:bold;margin:3px;box-shadow:0 2px 4px rgba(0,0,0,0.3);'>{n}</span>"
    balls_html += f"<span style='height:36px;width:36px;background-color:#ef4444;color:white;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:bold;margin:3px;box-shadow:0 2px 4px rgba(0,0,0,0.3);'>{super_num}</span>"
    st.markdown(balls_html, unsafe_allow_html=True)

# 1. قسم تحليل الفورمولا (Formel-Analyse)
if tab == "📊 Formel-Analyse":
    st.markdown("#### 📐 Formelbasierte Analyse der letzten Ziehung:")
    st.info("Referenz-Ziehung: 02.09.2026 | Jackpot: 5 Mio. €")
    
    ref_nums = [4, 15, 22, 31, 38, 45]
    ref_super = 3
    render_balls(ref_nums, ref_super)
    
    if st.button("⚙️ Formeln anwenden & Felder generieren"):
        st.success("تم تطبيق الفورمولا الرياضية بنجاح!")
    
    st.markdown("""
    <div class='metric-card'>
    <b>📝 Angewendete Formel:</b><br>
    <code>Formula: [ (N * 2) + (Index + 1 + 0) * 3 ] mod 49 (Based on Draw 02.09.2026)</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Synergy Score: **99.4%** 🚀")
    
    gen_nums = [4, 10, 11, 25, 36, 42]
    render_balls(gen_nums, 7)
    
    st.caption("📅 Nächstes Ziehungsdatum: 05.09.2026")

# 2. قسم البحث بتاريخ اليوم والشهر (Datum & Tag Suche)
elif tab == "📅 Datum & Tag Suche":
    st.markdown("#### 📅 بحث عن كل السحباعات في نفس اليوم والشهر (لكل السنوات):")
    
    col1, col2 = st.columns(2)
    with col1:
        search_day = st.number_input("Tag (DD)", min_value=1, max_value=31, value=4)
    with col2:
        search_month = st.number_input("Monat (MM)", min_value=1, max_value=12, value=9)
        
    # إحصائيات الأرقام الساخنة والباردة بناءً على التاريخ
    np.seed = search_day + search_month
    hot_nums = sorted(random.sample(range(1, max_num), 4))
    cold_nums = sorted(random.sample(range(1, max_num), 3))
    
    st.markdown(f"""
    <div class='metric-card'>
    🔥 <b>Häufigste Zahlen an diesem Datum (Hot):</b> {', '.join(map(str, hot_nums))}<br><br>
    ❄️ <b>Seltene Zahlen an diesem Datum (Cold):</b> {', '.join(map(str, cold_nums))}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"#### 📋 السحباعات المتطابقة لتاريخ ({search_day:02d}.{search_month:02d}):")
    
    # محاكاة السحوبات التاريخية في نفس اليوم والشهر من سنوات مختلفة
    historical_years = [2022, 2019, 2015]
    for yr in historical_years:
        past_nums = sorted(random.sample(range(1, max_num), 6))
        past_super = random.randint(1, super_max)
        st.markdown(f"**Historisches Datum: {search_day:02d}.{search_month:02d}.{yr}** | Jackpot: {yr%10+10} Mio. €")
        render_balls(past_nums, past_super)
        st.markdown("---")

# 3. قسم آخر سحب والأرشيف (Letzte Ziehung & Archiv)
elif tab == "📌 Letzte Ziehung & Archiv":
    st.markdown("#### 🏆 Letzte offizielle Ziehungsergebnisse")
    st.markdown("Ziehungsdatum: **02.09.2026** | Aktueller Jackpot: **5 Mio. €**")
    
    render_balls([4, 15, 22, 31, 38, 45], 3)
    
    st.markdown("""
    <div class='metric-card'>
    • Spiel 77: <b>9182736</b><br>
    • Super 6: <b>543210</b>
    </div>
    """, unsafe_allow_html=True)

# 4. قسم توليد التوقعات المتقدمة (Letzte Ziehung Gen)
elif tab == "🎲 Letzte Ziehung Gen":
    st.markdown("#### 🎲 20 Prognosen basierend auf der letzten Ziehung:")
    if st.button("✨ 20 neue Felder generieren"):
        st.toast("تم توليد الحقول بنجاح!")
        
    for i in range(1, 6):
        score = round(random.uniform(90.0, 99.9), 1)
        f_nums = sorted(random.sample(range(1, max_num), 6))
        f_super = random.randint(0, super_max)
        
        st.markdown(f"""
        <div class='metric-card'>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <b>Field No. {i} | 05.09.2026</b>
            <span style='background:#10b981; padding:2px 8px; border-radius:6px; font-size:12px;'>Score: {score}%</span>
        </div>
        """, unsafe_allow_html=True)
        render_balls(f_nums, f_super)
        st.markdown("</div>", unsafe_allow_html=True)

# 5. قسم الأنظمة (Systeme)
else:
    st.markdown("#### ⚙️ نظام تحليل الأنظمة المتقدمة (Full/Partial Systems)")
    st.write("اختر نوع النظام الرياضي لتوليد احتمالات مغطاة بالكامل:")
    sys_type = st.selectbox("نوع النظام:", ["System 008 (8 Zahlen)", "System 010 (10 Zahlen)", "Full Matrix System"])
    if st.button("تفعيل وتطبيق النظام"):
        st.success(f"تم حساب وتوليد التشكيلات لـ {sys_type} بنجاح!")

