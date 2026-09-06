import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل وتوقع سحوبات اللوتو و Eurojackpot", page_icon="🎰", layout="wide")

# دالة ذكية جداً لقراءة ملفات Excel / CSV / JSON مع معالجة مكتبة openpyxl
@st.cache_data
def load_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            filename = uploaded_file.name.lower()
            if filename.endswith('.json'):
                df = pd.read_json(uploaded_file)
            elif filename.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif filename.endswith(('.xlsx', '.xls')):
                try:
                    xls = pd.ExcelFile(uploaded_file)
                    dfs = []
                    for sheet in xls.sheet_names:
                        temp_df = pd.read_excel(xls, sheet_name=sheet)
                        if not temp_df.empty:
                            dfs.append(temp_df)
                    df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
                except Exception as ex:
                    if "openpyxl" in str(ex):
                        st.error("⚠️ مكتبة قراءة ملفات الإكسل (openpyxl) غير مثبتة. يرجى إضافتها إلى ملف requirements.txt.")
                    else:
                        st.error(f"خطأ في قراءة ملف الإكسل: {ex}")
                    return pd.DataFrame(), False
            else:
                return pd.DataFrame(), False
            return df, True
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            return pd.DataFrame(), False
    return pd.DataFrame(), False

# دالة لاستخراج الشهر واليوم بدقة من أي نوع بيانات
def smart_extract_month_day(val):
    if pd.isna(val):
        return ""
    if isinstance(val, (int, float)):
        try:
            dt = pd.to_datetime(val, unit='d', origin='1899-12-30', errors='coerce')
            if pd.notna(dt):
                return dt.strftime('%m-%d')
        except:
            pass
            
    s = str(val).strip().replace('.', '-').replace('/', '-')
    dt = pd.to_datetime(s, errors='coerce')
    if pd.notna(dt):
        return dt.strftime('%m-%d')
        
    parts = s.split('-')
    if len(parts) >= 2:
        return f"{parts[-2].zfill(2)}-{parts[-1].zfill(2)}"
    return s

st.title("🎰 النظام الاحترافي الشامل للوتو و Eurojackpot والأبراج")
st.markdown("---")

st.sidebar.header("📂 إدارة ملفات السحوبات")
lotto_file = st.sidebar.file_uploader("رفع ملف سحوبات (Lotto):", type=["json", "csv", "xlsx", "xls"], key="lotto")
euro_file = st.sidebar.file_uploader("رفع ملف سحوبات (Eurojackpot):", type=["json", "csv", "xlsx", "xls"], key="euro")

# تحميل اللوتو
raw_lotto, lotto_ok = load_uploaded_file(lotto_file)
if lotto_ok:
    df_lotto = raw_lotto
    st.sidebar.success(f"✅ تم رفع ملف اللوتو ({len(df_lotto)} سحب)")
else:
    df_lotto = pd.DataFrame([
        {"full_date": "1955-09-09", "numbers": "5, 12, 23, 34, 42, 15"},
        {"full_date": "2010-09-09", "numbers": "3, 14, 25, 33, 40, 8"},
        {"full_date": "2015-09-09", "numbers": "5, 14, 23, 28, 40, 12"},
        {"full_date": "2023-05-12", "numbers": "7, 11, 19, 28, 39, 22"}
    ])
    if lotto_file is not None:
        st.sidebar.warning("⚠️ تعذر قراءة ملف اللوتو، يتم استخدام البيانات الافتراضية.")

# تحميل اليوروجاكبوت
raw_euro, euro_ok = load_uploaded_file(euro_file)
if euro_ok:
    df_euro = raw_euro
    st.sidebar.success(f"✅ تم رفع ملف Eurojackpot ({len(df_euro)} سحب)")
else:
    df_euro = pd.DataFrame([
        {"full_date": "2020-09-09", "numbers": "10, 18, 27, 35, 44 + 3, 7"},
        {"full_date": "2022-10-15", "numbers": "2, 15, 22, 38, 49 + 1, 9"}
    ])
    if euro_file is not None:
        st.sidebar.warning("⚠️ تعذر قراءة ملف Eurojackpot، يتم استخدام البيانات الافتراضية.")

main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
    "🎯 سحوبات اللوتو", 
    "💶 سحوبات Eurojackpot", 
    "♈ قسم الأبراج الفلكية", 
    "📅 توقعات تاريخ الميلاد"
])

# ==================== التبويب الأول: اللوتو ====================
with main_tab1:
    st.subheader("🎯 البحث والتحليل في سحوبات اللوتو")
    
    date_col = next((col for col in df_lotto.columns if any(k in str(col).lower() for k in ['date', 'تاريخ', 'time', 'day'])), df_lotto.columns[0])
    num_col = next((col for col in df_lotto.columns if any(k in str(col).lower() for k in ['num', 'result', 'رقم', 'ارقام', 'draw', 'balls'])), df_lotto.columns[1] if len(df_lotto.columns) > 1 else df_lotto.columns[0])

    df_lotto['clean_md'] = df_lotto[date_col].apply(smart_extract_month_day)

    query_lotto = st.text_input("أدخل الشهر واليوم للبحث في اللوتو (مثال: 09.09 أو 09-09):", key="q_lotto").strip()

    if query_lotto:
        norm_q = query_lotto.replace('.', '-').replace('/', '-')
        results = df_lotto[df_lotto['clean_md'] == norm_q]
        
        if results.empty:
            parts = norm_q.split('-')
            if len(parts) == 2:
                results = df_lotto[df_lotto['clean_md'] == f"{parts[1]}-{parts[0]}"]

        st.markdown(f"**عدد السحوبات المطابقة لتاريخ ({query_lotto}):** `{len(results)}` سحب")
        
        if not results.empty:
            found_nums = []
            for _, row in results.iterrows():
                d_val = row.get(date_col, 'غير متوفر')
                n_val = row.get(num_col, 'غير متوفر')
                st.success(f"📅 **التاريخ:** {d_val} \n\n 🔢 **الأرقام:** `{n_val}`")
                if pd.notna(n_val):
                    clean_str = str(n_val).replace('،', ',').replace('.', ',')
                    found_nums.extend([int(p.strip()) for p in clean_str.split(',') if p.strip().isdigit()])

            st.markdown("---")
            if found_nums:
                st.markdown("### 🎲 توليد احتمالات متعددة بناءً على سحوبات هذا التاريخ:")
                if st.button("🔄 توليد 3 احتمالات جديدة للوتو", key="btn_lotto"):
                    counts = pd.Series(found_nums).value_counts()
                    top_freq = list(counts.index[:12])
                    for i in range(1, 4):
                        np.random.seed(len(found_nums) * i * 17)
                        chosen = np.random.choice(top_freq, min(3, len(top_freq)), replace=False).tolist() if top_freq else []
                        remaining = [num for num in range(1, 50) if num not in chosen]
                        needed = 6 - len(chosen)
                        final_res = sorted(chosen + np.random.choice(remaining, needed, replace=False).tolist())
                        st.info(f"📌 **الاحتمال رقم {i}:** `{' - '.join(map(str, final_res))}`")
        else:
            st.warning("⚠️ لم يتم العثور على سحوبات مطابقة لهذا التاريخ.")

# ==================== التبويب الثاني: يوروجاكبوت ====================
with main_tab2:
    st.subheader("💶 البحث والتحليل في سحوبات Eurojackpot")
    
    edate_col = next((col for col in df_euro.columns if any(k in str(col).lower() for k in ['date', 'تاريخ', 'time', 'day'])), df_euro.columns[0])
    enum_col = next((col for col in df_euro.columns if any(k in str(col).lower() for k in ['num', 'result', 'رقم', 'ارقام', 'draw', 'balls'])), df_euro.columns[1] if len(df_euro.columns) > 1 else df_euro.columns[0])

    df_euro['clean_md'] = df_euro[edate_col].apply(smart_extract_month_day)

    query_euro = st.text_input("أدخل الشهر واليوم للبحث في Eurojackpot (مثال: 09.09 أو 10-15):", key="q_euro").strip()

    if query_euro:
        norm_eq = query_euro.replace('.', '-').replace('/', '-')
        eresults = df_euro[df_euro['clean_md'] == norm_eq]
        
        if eresults.empty:
            parts = norm_eq.split('-')
            if len(parts) == 2:
                eresults = df_euro[df_euro['clean_md'] == f"{parts[1]}-{parts[0]}"]

        st.markdown(f"**عدد السحوبات المطابقة لتاريخ ({query_euro}):** `{len(eresults)}` سحب")
        
        if not eresults.empty:
            efound_nums = []
            for _, row in eresults.iterrows():
                d_val = row.get(edate_col, 'غير متوفر')
                n_val = row.get(enum_col, 'غير متوفر')
                st.success(f"📅 **التاريخ:** {d_val} \n\n 🔢 **الأرقام:** `{n_val}`")
                if pd.notna(n_val):
                    clean_str = str(n_val).replace('،', ',').replace('.', ',')
                    efound_nums.extend([int(p.strip()) for p in clean_str.split(',') if p.strip().isdigit()])

            st.markdown("---")
            if efound_nums:
                st.markdown("### 🎲 توليد احتمالات متعددة لـ Eurojackpot بناءً على هذا التاريخ:")
                if st.button("🔄 توليد 3 احتمالات جديدة لـ Eurojackpot", key="btn_euro"):
                    counts = pd.Series(efound_nums).value_counts()
                    top_freq = list(counts.index[:12])
                    for i in range(1, 4):
                        np.random.seed(len(efound_nums) * i * 23)
                        chosen = np.random.choice(top_freq, min(2, len(top_freq)), replace=False).tolist() if top_freq else []
                        remaining = [num for num in range(1, 51) if num not in chosen]
                        needed_main = 5 - len(chosen)
                        main_nums = sorted(chosen + np.random.choice(remaining, needed_main, replace=False).tolist())
                        euro_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
                        st.info(f"📌 **الاحتمال {i}:** الأرقام الرئيسية `{' - '.join(map(str, main_nums))}` + النجوم `{' & '.join(map(str, euro_stars))}`")
        else:
            st.warning("⚠️ لم يتم العثور على سحوبات مطابقة لهذا التاريخ في الملف.")

# ==================== التبويب الثالث: الأبراج الفلكية ====================
with main_tab3:
    st.subheader("♈ الأبراج الفلكية وتوليد احتمالات متعددة لكل برج")
    zodiacs = [
        {"name": "الحمل (Aries)", "symbol": "♈", "element": "النار"},
        {"name": "الثور (Taurus)", "symbol": "♉", "element": "الأرض"},
        {"name": "الجوزاء (Gemini)", "symbol": "♊", "element": "الهواء"},
        {"name": "السرطان (Cancer)", "symbol": "♋", "element": "الماء"},
        {"name": "الأسد (Leo)", "symbol": "♌", "element": "النار"},
        {"name": "العذراء (Virgo)", "symbol": "♍", "element": "الأرض"},
        {"name": "الميزان (Libra)", "symbol": "♎", "element": "الهواء"},
        {"name": "العقرب (Scorpio)", "symbol": "♏", "element": "الماء"},
        {"name": "القوس (Sagittarius)", "symbol": "♐", "element": "النار"},
        {"name": "الجدي (Capricorn)", "symbol": "♑", "element": "الأرض"},
        {"name": "الدلو (Aquarius)", "symbol": "♒", "element": "الهواء"},
        {"name": "الحوت (Pisces)", "symbol": "♓", "element": "الماء"}
    ]

    selected_zodiac = st.selectbox("اختر البرج:", [f"{z['symbol']} {z['name']} ({z['element']})" for z in zodiacs])
    
    if st.button("🔮 توليد 3 احتمالات لطاقة هذا البرج"):
        st.markdown("---")
        base_seed = sum([ord(c) for c in selected_zodiac])
        for i in range(1, 4):
            np.random.seed(base_seed + i * 37)
            z_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            st.success(f"✨ **الاحتمال رقم {i}:** `{' - '.join(map(str, z_nums))}`")

# ==================== التبويب الرابع: تاريخ الميلاد ====================
with main_tab4:
    st.subheader("📅 توقعات تاريخ الميلاد (احتمالات متعددة)")
    b_date = st.date_input("أدخل تاريخ ميلادك:", value=datetime(1995, 6, 15), key="birth_input")
    
    if st.button("🌟 توليد 3 احتمالات جديدة بناءً على تاريخ الميلاد"):
        st.markdown("---")
        for i in range(1, 4):
            np.random.seed(b_date.toordinal() + i * 43)
            b_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            st.success(f"📌 **التوقع رقم {i}:** `{' - '.join(map(str, b_nums))}`")
