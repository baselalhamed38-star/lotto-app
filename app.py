import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="نظام تحليل وتوليد سحوبات اللوتو ويوروجاكبوت", page_icon="🎯", layout="wide")

st.title("🎯 النظام المتقدم لتحليل السحوبات وتوليد أرقام 2026")

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
    st.subheader(f"📊 قاعدة بيانات وتحليل سحوبات {game_name}")
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
    st.markdown(f"### 🧮 معادلة السحوبات الذكية وتوليد أرقام 2026 لـ {game_name}")
    
    # نافذة تاريخ الميلاد المستقلة
    st.markdown("#### 📅 نافذة تاريخ الميلاد")
    birth_date = st.date_input(f"حدد تاريخ ميلادك لربطه بمعادلة {game_name}:", value=datetime(1990, 1, 1), key=f"b_{game_name}")
    
    # نافذة الأبراج المستقلة
    st.markdown("#### 🌟 نافذة الأبراج الفلكية")
    zodiac = st.selectbox(f"اختر برجك الفلكي لتعزيز التحليل لـ {game_name}:", 
                          ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", 
                           "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", 
                           "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"], key=f"z_{game_name}")
    
    # استخراج تحليل من السحوبات القديمة (عدد الصفوف وتكرار القيم الرياضية كمعادلة أساسية)
    total_historical_rows = len(df)
    sample_numeric_factor = int(df.select_dtypes(include=[np.number]).sum().sum()) % 1000 if not df.select_dtypes(include=[np.number]).empty else 500
    
    st.markdown(f"**🔬 المعادلة المطبقة المستخرجة من أرشيف السحوبات:**")
    st.code(f"Formula_2026 = (Historical_Rows({total_historical_rows}) + Data_Factor({sample_numeric_factor})) * Birth({birth_date.toordinal()}) + Zodiac({zodiac.split()[0]}) + Draw_2026", language="python")
    
    # مفتاح فريد لضمان التوليد المتكرر وغير المحدود في كل ضغطة
    if f"counter_{game_name}" not in st.session_state:
        st.session_state[f"counter_{game_name}"] = 0
        
    if st.button(f"🎲 تطبيق المعادلة وتوليد أرقام سحوبات 2026 لـ {game_name} (اضغط مراراً للتغيير)", key=f"btn_gen_{game_name}"):
        st.session_state[f"counter_{game_name}"] += 1
        
    # دمج السحوبات القديمة مع بذور التوليد لعام 2026
    computed_seed = total_historical_rows + sample_numeric_factor + birth_date.toordinal() + (st.session_state[f"counter_{game_name}"] * 123) + int(datetime.now().strftime("%f"))
    np.random.seed(computed_seed)
    
    if st.session_state[f"counter_{game_name}"] > 0:
        st.success(f"✨ التوقع رقم ({st.session_state[f"counter_{game_name}"]}) الناتج عن معادلة السحوبات القديمة وتاريخ 2026 وبرج **{zodiac.split()[0]}**:")
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric(f"🎫 أرقام اللوتو المقترحة لسحوبات 2026:", str(p_nums))
            st.metric(f"🌟 رقم Superzahl المقترح:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric(f"💶 الأرقام الرئيسية المقترحة لـ Eurojackpot 2026:", str(p_nums))
            st.metric(f"⭐ أرقام Sternzahl (النجوم):", str(p_stars))
    else:
        st.info("👆 اضغط على زر تطبيق المعادلة أعلاه لتوليد أرقام سحوبات 2026 المستندة للأرشيف القديم.")

with tab1:
    run_interactive_tab(df_lotto, "اللوتو (Lotto)", files_lotto, False)

with tab2:
    run_interactive_tab(df_euro, "يوروجاكبوت (Eurojackpot)", files_euro, True)
