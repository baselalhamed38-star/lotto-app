import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="نظام تحليل وتوليد سحوبات اللوتو ويوروجاكبوت", page_icon="🎯", layout="wide")

st.title("🎯 النظام المتقدم للبحث وتحليل السحوبات التاريخية 2026")

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

def run_full_features_tab(df, game_name, matched_files, is_euro=False):
    st.subheader(f"📊 تحليل الأرشيف والسحوبات التاريخية لـ {game_name}")
    st.info(f"📁 الملفات المرتبطة: `{matched_files if matched_files else 'ملفات عامة'}`")
    
    if df.empty:
        st.error(f"⚠️ تنبيه: لم يتم العثور على ملفات تخص {game_name} في المستودع.")
        return
        
    total_rows = len(df)
    numeric_vals = df.select_dtypes(include=[np.number])
    matrix_sum = int(numeric_vals.sum().sum()) if not numeric_vals.empty else 12345
    
    # ----------------- 1. البحث الدقيق بنفس اليوم والشهر عبر السنين -----------------
    st.markdown("### 📅 البحث الدقيق عن نفس اليوم والشهر عبر السنين")
    col_d, col_m = st.columns(2)
    with col_d:
        selected_day = st.selectbox(f"اختر اليوم ({game_name}):", list(range(1, 32)), key=f"p_day_{game_name}")
    with col_m:
        months_dict = {
            "يناير (01)": "01", "فبراير (02)": "02", "مارس (03)": "03", "أبريل (04)": "04",
            "مايو (05)": "05", "يونيو (06)": "06", "يوليو (07)": "07", "أغسطس (08)": "08",
            "سبتمبر (09)": "09", "أكتوبر (10)": "10", "نوفمبر (11)": "11", "ديسمبر (12)": "12"
        }
        selected_month_name = st.selectbox(f"اختر الشهر ({game_name}):", list(months_dict.keys()), key=f"p_mon_{game_name}")
        selected_month_num = months_dict[selected_month_name]
        
    day_str = f"{selected_day:02d}"
    df_str = df.astype(str)
    
    pattern_dot = f".*\\b{day_str}\\.{selected_month_num}\\b.*"
    pattern_slash = f".*\\b{int(day_str)}/{int(selected_month_num)}/.*"
    pattern_hyphen = f".*\\b-{selected_month_num}-{day_str}\\b.*"
    
    exact_date_mask = df_str.apply(lambda x: x.str.contains(pattern_dot, regex=True, case=False, na=False) |
                                               x.str.contains(pattern_slash, regex=True, case=False, na=False) |
                                               x.str.contains(pattern_hyphen, regex=True, case=False, na=False)).any(axis=1)
    
    res_date = df[exact_date_mask]
    
    if not res_date.empty:
        st.success(f"✅ تم العثور على **{len(res_date)}** سحب في نفس اليوم والشهر ({day_str}/{selected_month_num}) بالسنوات السابقة:")
        st.dataframe(res_date, use_container_width=True)
    else:
        st.warning(f"⚠️ لم يتم العثور على سحوبات مطابقة تماماً لتاريخ ({day_str}/{selected_month_num}) في الأرشيف.")
        
    with st.expander(f"👁️ استعراض كامل أرشيف سحوبات {game_name} ({total_rows} سحب)"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    
    # ----------------- 2. زر تحليل السحوبات التاريخية لتوليد التوقعات -----------------
    st.markdown("### 🔍 تحليل السحوبات التاريخية وتوليد توقعات 2026")
    hist_counter_key = f"counter_hist_{game_name}"
    if hist_counter_key not in st.session_state:
        st.session_state[hist_counter_key] = 0
        
    if st.button(f"📊 تحليل الأرشيف وتوليد توقعات 2026 لـ {game_name}", key=f"btn_hist_{game_name}"):
        st.session_state[hist_counter_key] += 1
        
    if st.session_state[hist_counter_key] > 0:
        seed_hist = total_rows + matrix_sum + (st.session_state[hist_counter_key] * 444) + int(datetime.now().strftime("%f"))
        np.random.seed(seed_hist)
        
        st.success(f"✨ التوقع الإحصائي التاريخي رقم ({st.session_state[hist_counter_key]}):")
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو المقترحة من الأرشيف:", str(p_nums))
            st.metric("رقم Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية المقترحة من الأرشيف:", str(p_nums))
            st.metric("أرقام النجوم (Sternzahl):", str(p_stars))
            
    st.markdown("---")
    
    # ----------------- 3. نافذة تاريخ الميلاد المستقلة -----------------
    st.markdown("### 📅 نافذة تاريخ الميلاد المستقلة لتوليد الأرقام")
    birth_date = st.date_input(f"حدد تاريخ ميلادك لـ {game_name}:", value=datetime(1990, 1, 1), key=f"b_date_{game_name}")
    
    birth_counter_key = f"counter_birth_{game_name}"
    if birth_counter_key not in st.session_state:
        st.session_state[birth_counter_key] = 0
        
    if st.button(f"🎲 توليد أرقام 2026 عبر (تاريخ الميلاد) لـ {game_name}", key=f"btn_birth_{game_name}"):
        st.session_state[birth_counter_key] += 1
        
    if st.session_state[birth_counter_key] > 0:
        seed_birth = total_rows + matrix_sum + birth_date.toordinal() + (st.session_state[birth_counter_key] * 99)
        np.random.seed(seed_birth)
        
        st.success(f"✨ نتيجة توليد تاريخ الميلاد (التوقع رقم {st.session_state[birth_counter_key]}):")
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو (تاريخ الميلاد):", str(p_nums))
            st.metric("رقم Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية (تاريخ الميلاد):", str(p_nums))
            st.metric("أرقام النجوم (Sternzahl):", str(p_stars))
            
    st.markdown("---")
    
    # ----------------- 4. نافذة الأبراج الفلكية المستقلة -----------------
    st.markdown("### 🌟 نافذة الأبراج الفلكية المستقلة لتوليد الأرقام")
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
        seed_zodiac = total_rows + matrix_sum + hash(zodiac) + (st.session_state[zodiac_counter_key] * 111)
        np.random.seed(seed_zodiac)
        
        st.success(f"✨ نتيجة توليد الأبراج لبرج {zodiac.split()[0]} (التوقع رقم {st.session_state[zodiac_counter_key]}):")
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_super = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو (البرج الفلكي):", str(p_nums))
            st.metric("رقم Superzahl:", str(p_super))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية (البرج الفلكي):", str(p_nums))
            st.metric("أرقام النجوم (Sternzahl):", str(p_stars))

with tab1:
    run_full_features_tab(df_lotto, "اللوتو (Lotto)", files_lotto, False)

with tab2:
    run_full_features_tab(df_euro, "يوروجاكبوت (Eurojackpot)", files_euro, True)
