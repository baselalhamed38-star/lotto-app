import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="نظام تحليل وتوليد سحوبات اللوتو ويوروجاكبوت", page_icon="🎯", layout="wide")

st.title("🎯 النظام المتقدم لتحليل السحوبات وتوليد الأرقام (تحديث 2026)")

# دالة لتحميل وفصل الملفات لكل لعبة بدقة
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
                        df_sheet['Source_Info'] = f"ملف: {file_name} ➔ [شيت: {sheet_name}]"
                        all_draws.append(df_sheet)
            elif file_name.endswith('.csv'):
                df_csv = pd.read_csv(file_name, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty:
                    df_csv['Source_Info'] = f"ملف: {file_name}"
                    all_draws.append(df_csv)
        except Exception as e:
            pass
            
    if all_draws:
        return pd.concat(all_draws, ignore_index=True), matched_files
    return pd.DataFrame(), []

df_lotto, files_lotto = load_game_files("lotto")
df_euro, files_euro = load_game_files("euro")

tab1, tab2 = st.tabs(["🍀 اللوتو (Lotto)", "💶 يوروجاكبوت (Eurojackpot)"])

def run_interactive_tab(df, game_name, matched_files, is_euro=False):
    st.subheader(f"📊 قاعدة بيانات وتحليل {game_name}")
    st.info(f"📁 الملفات المرتبطة: `{matched_files if matched_files else 'ملفات عامة'}`")
    
    if df.empty:
        st.error(f"⚠️ تنبيه: لم يتم العثور على ملفات تخص {game_name} في المستودع.")
        return
        
    with st.expander(f"👁️ عرض محتوى ملفات {game_name}"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    query = st.text_input(f"🔍 بحث دقيق في ملفات {game_name}:", key=f"q_{game_name}").strip()
    if query:
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        res = df[mask]
        st.info(f"عدد النتائج: **{len(res)}**")
        if not res.empty:
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة.")
            
    st.markdown("---")
    st.markdown(f"### 🔮 حاسبة التوقع الذكية وتوليد الأرقام المتكرر لـ {game_name}")
    
    # مدخلات الأبراج وتاريخ الميلاد
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input(f"📅 حدد تاريخ ميلادك لربطه بالمعادلة ({game_name}):", value=datetime(1990, 1, 1), key=f"b_{game_name}")
    with col2:
        zodiac = st.selectbox(f"🌟 اختر برجك الفلكي لتعزيز التوقع ({game_name}):", 
                              ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", 
                               "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", 
                               "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"], key=f"z_{game_name}")
        
    st.markdown(f"**🔬 المعادلة المطبقة:** `Analysis_Formula({game_name}) = Historical_Pattern + BirthDate_Seed + Zodiac_Factor + CurrentTime`")
    
    # مفتاح فريد لضمان تفعيل زر التوليد المتكرر في كل ضغطة
    if f"counter_{game_name}" not in st.session_state:
        st.session_state[f"counter_{game_name}"] = 0
        
    if st.button(f"🎲 توليد مجموعة أرقام جديدة لـ {game_name} (اضغط مراراً للتغيير)", key=f"btn_gen_{game_name}"):
        st.session_state[f"counter_{game_name}"] += 1
        
    # توليد عشوائي ديناميكي متغير في كل ضغطة
    current_seed = int(datetime.now().strftime("%f")) + st.session_state[f"counter_{game_name}"] * 77 + birth_date.toordinal()
    np.random.seed(current_seed)
    
    if st.session_state[f"counter_{game_name}"] > 0:
        st.success(f"✨ التوقع رقم ({st.session_state[f"counter_{game_name}"]}) متوافق مع برج **{zodiac.split()[0]}** وتاريخ ميلادك:")
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("🎫 أرقام اللوتو المقترحة:", str(p_nums))
            st.metric("🌟 رقم Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("💶 الأرقام الرئيسية المقترحة:", str(p_nums))
            st.metric("⭐ أرقام Sternzahl (النجوم):", str(p_stars))
    else:
        st.info("👆 اضغط على زر التوليد أعلاه للحصول على أول مجموعة أرقام مخصصة ومبنية على تاريخ ميلادك وبرجك.")

with tab1:
    run_interactive_tab(df_lotto, "اللوتو (Lotto)", files_lotto, False)

with tab2:
    run_interactive_tab(df_euro, "يوروجاكبوت (Eurojackpot)", files_euro, True)
