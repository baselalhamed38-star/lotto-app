import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="نظام تحليل وتوليد سحوبات اللوتو ويوروجاكبوت", page_icon="🎯", layout="wide")

st.title("🎯 النظام المتقدم للبحث في السحوبات وتوليد أرقام 2026")

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

def run_complete_tab(df, game_name, matched_files, is_euro=False):
    st.subheader(f"📊 قاعدة بيانات ومعادلات {game_name}")
    st.info(f"📁 الملفات المرتبطة: `{matched_files if matched_files else 'ملفات عامة'}`")
    
    if df.empty:
        st.error(f"⚠️ تنبيه: لم يتم العثور على ملفات تخص {game_name} في المستودع.")
        return
        
    total_rows = len(df)
    numeric_sum = int(df.select_dtypes(include=[np.number]).sum().sum()) % 1000 if not df.select_dtypes(include=[np.number]).empty else 400
    
    # ----------------- 1. قسم البحث عبر تحديد التاريخ -----------------
    st.markdown("### 📅 البحث عن السحوبات القديمة عبر تحديد التاريخ")
    st.markdown("اختر أي تاريخ للبحث عنه في أرشيف السحوبات وإظهار النتائج المطابقة:")
    
    selected_search_date = st.date_input(f"حدد التاريخ المطلوب لـ {game_name}:", value=datetime(2022, 1, 1), key=f"search_date_{game_name}")
    date_str_dot = selected_search_date.strftime("%d.%m.%Y")
    date_str_slash = selected_search_date.strftime("%Y/%m/%d")
    date_str_hyphen = selected_search_date.strftime("%Y-%m-%d")
    
    # البحث بالصيغ المختلفة للتاريخ داخل الأرشيف
    mask = df.astype(str).apply(lambda x: x.str.contains(f"{selected_search_date.day}|{selected_search_date.month}|{selected_search_date.year}", case=False, na=False)).any(axis=1)
    # تصفية أدق بالتاريخ إذا وجد تطابق مباشر
    date_mask = df.astype(str).apply(lambda x: x.str.contains(date_str_dot, case=False, na=False) | 
                                               x.str.contains(date_str_slash, case=False, na=False) | 
                                               x.str.contains(date_str_hyphen, case=False, na=False)).any(axis=1)
    
    res_date = df[date_mask]
    
    if not res_date.empty:
        st.success(f"✅ تم العثور على **{len(res_date)}** سحب يطابق التاريخ المحدد ({date_str_dot}):")
        st.dataframe(res_date, use_container_width=True)
    else:
        st.warning(f"⚠️ لم يتم العثور على سحب مسجل بالتاريخ الدقيق ({date_str_dot}). يمكنك استعراض كامل الأرشيف أدناه:")
        
    with st.expander(f"👁️ استعراض كامل أرشيف سحوبات {game_name} ({total_rows} سحب)"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    
    # ----------------- 2. نافذة تاريخ الميلاد (مستقلة لتوليد الأرقام) -----------------
    st.markdown("### 🎫 نافذة توليد أرقام 2026 عبر (تاريخ الميلاد)")
    birth_date = st.date_input(f"حدد تاريخ ميلادك لـ {game_name}:", value=datetime(1990, 1, 1), key=f"b_date_{game_name}")
    
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state:
        st.session_state[birth_counter_key] = 0
        
    if st.button(f"🎲 توليد أرقام 2026 عبر (تاريخ الميلاد) لـ {game_name}", key=f"btn_birth_{game_name}"):
        st.session_state[birth_counter_key] += 1
        
    if st.session_state[birth_counter_key] > 0:
        seed_birth = total_rows + numeric_sum + birth_date.toordinal() + (st.session_state[birth_counter_key] * 99)
        np.random.seed(seed_birth)
        
        st.success(f"✨ نتائج توليد تاريخ الميلاد (التوقع رقم {st.session_state[birth_counter_key]}):")
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو المقترحة (تاريخ الميلاد)", str(p_nums))
            st.metric("رقم Superzahl", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية المقترحة (تاريخ الميلاد)", str(p_nums))
            st.metric("أرقام النجوم (Sternzahl)", str(p_stars))
            
    st.markdown("---")
    
    # ----------------- 3. نافذة الأبراج الفلكية (مستقلة لتوليد الأرقام) -----------------
    st.markdown("### 🌟 نافذة توليد أرقام 2026 عبر (البرج الفلكي)")
    zodiac = st.selectbox(f"اختر برجك الفلكي لـ {game_name}:", 
                          ["الحمل (Aries)", "الثور (Taurus)", "الجوزاء (Gemini)", "السرطان (Cancer)", 
                           "الأسد (Leo)", "العذراء (Virgo)", "الميزان (Libra)", "العقرب (Scorpio)", 
                           "القوس (Sagittarius)", "الجدي (Capricorn)", "الدلو (Aquarius)", "الحوت (Pisces)"], key=f"z_select_{game_name}")
    
    zodiac_counter_key = f"counter_zodiac_{game_name}"
    if zodiac_counter_key not in st.session_state:
        st.session_state[zodiac_counter_key] = 0
        
    if st.button(f"🎲 توليد أرقام 2026 عبر (البرج الفلكي) لـ {game_name}", key=f"btn_zodiac_{game_name}"):
        st.session_state[zodiac_counter_key] += 1
        
    if st.session_state[zodiac_counter_key] > 0:
        seed_zodiac = total_rows + numeric_sum + hash(zodiac) + (st.session_state[zodiac_counter_key] * 111)
        np.random.seed(seed_zodiac)
        
        st.success(f"✨ نتائج توليد الأبراج لبرج {zodiac.split()[0]} (التوقع رقم {st.session_state[zodiac_counter_key]}):")
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو المقترحة (البرج الفلكي)", str(p_nums))
            st.metric("رقم Superzahl", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية المقترحة (البرج الفلكي)", str(p_nums))
            st.metric("أرقام النجوم (Sternzahl)", str(p_stars))

with tab1:
    run_complete_tab(df_lotto, "اللوتو (Lotto)", files_lotto, False)

with tab2:
    run_complete_tab(df_euro, "يوروجاكبوت (Eurojackpot)", files_euro, True)
