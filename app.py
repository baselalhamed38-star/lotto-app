import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل وتوقع سحوبات اللوتو واليوروجاكبوت", page_icon="🎰", layout="wide")

# دالة لتحميل ملفات اللوتو
@st.cache_data
def load_lotto_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.json'):
                return pd.read_json(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
        except Exception:
            return pd.DataFrame()
    # بيانات تجريبية افتراضية للوتو
    return pd.DataFrame([
        {"full_date": "1955-09-09", "numbers": "5, 12, 23, 34, 42, 15"},
        {"full_date": "2010-09-09", "numbers": "3, 14, 25, 33, 40, 8"},
        {"full_date": "2015-09-09", "numbers": "5, 14, 23, 28, 40, 12"},
        {"full_date": "2023-05-12", "numbers": "7, 11, 19, 28, 39, 22"}
    ])

# دالة لتحميل ملفات يوروجاكبوت
@st.cache_data
def load_euro_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.json'):
                return pd.read_json(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
        except Exception:
            return pd.DataFrame()
    # بيانات تجريبية افتراضية ليوروجاكبوت
    return pd.DataFrame([
        {"full_date": "2020-09-09", "numbers": "10, 18, 27, 35, 44 + 3, 7"},
        {"full_date": "2022-10-15", "numbers": "2, 15, 22, 38, 49 + 1, 9"}
    ])

st.title("🎰 النظام الشامل لتحليل سحوبات اللوتو و Eurojackpot والأبراج")
st.markdown("---")

# القائمة الجانبية لرفع الملفات
st.sidebar.header("📂 إدارة ملفات السحوبات")
lotto_file = st.sidebar.file_uploader("رفع ملف سحوبات (Lotto):", type=["json", "csv"], key="lotto")
euro_file = st.sidebar.file_uploader("رفع ملف سحوبات (Eurojackpot):", type=["json", "csv"], key="euro")

df_lotto = load_lotto_data(lotto_file)
df_euro = load_euro_data(euro_file)

# تقسيم رئيسي بين النظامين والأبراج
main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
    "🎯 نظام سحوبات اللوتو", 
    "💶 نظام سحوبات Eurojackpot", 
    "♈ قسم الأبراج الفلكية", 
    "📅 توقعات تاريخ الميلاد"
])

# ==================== التبويب الأول: اللوتو ====================
with main_tab1:
    st.subheader("🎯 تحليل والبحث في سحوبات اللوتو")
    if df_lotto.empty:
        st.warning("⚠️ لا توجد بيانات للوتو متاحة.")
    else:
        date_col = next((col for col in df_lotto.columns if 'date' in col.lower() or 'تاريخ' in col), df_lotto.columns[0])
        num_col = next((col for col in df_lotto.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_lotto.columns[1] if len(df_lotto.columns) > 1 else df_lotto.columns[0])

        df_lotto['parsed_date'] = pd.to_datetime(df_lotto[date_col], errors='coerce')
        df_lotto['month_day'] = df_lotto['parsed_date'].dt.strftime('%m-%d')

        query_lotto = st.text_input("أدخل الشهر واليوم للبحث في اللوتو (مثال: 09-09 أو 09.09):", key="q_lotto").strip()

        if query_lotto:
            norm_q = query_lotto.replace('.', '-')
            results = df_lotto[df_lotto['month_day'] == norm_q]
            if results.empty:
                parts = norm_q.split('-')
                if len(parts) == 2:
                    results = df_lotto[df_lotto['month_day'] == f"{parts[1]}-{parts[0]}"]

            st.markdown(f"**عدد السحوبات المطابقة لهذا التاريخ:** `{len(results)}` سحب")
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
                if found_nums and st.button("🎲 توليد 6 مقترحات للوتو بناءً على نتائج هذا التاريخ"):
                    counts = pd.Series(found_nums).value_counts()
                    top_freq = list(counts.index[:10])
                    np.random.seed(len(found_nums) * 11)
                    chosen = np.random.choice(top_freq, min(3, len(top_freq)), replace=False).tolist() if top_freq else []
                    remaining = [i for i in range(1, 50) if i not in chosen]
                    needed = 6 - len(chosen)
                    final_res = sorted(chosen + np.random.choice(remaining, needed, replace=False).tolist())
                    st.success(f"🎯 **الـ 6 أرقام المقترحة للوتو:** `{' - '.join(map(str, final_res))}`")

# ==================== التبويب الثاني: يوروجاكبوت ====================
with main_tab2:
    st.subheader("💶 تحليل والبحث في سحوبات Eurojackpot")
    if df_euro.empty:
        st.warning("⚠️ لا توجد بيانات لـ Eurojackpot متاحة.")
    else:
        edate_col = next((col for col in df_euro.columns if 'date' in col.lower() or 'تاريخ' in col), df_euro.columns[0])
        enum_col = next((col for col in df_euro.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_euro.columns[1] if len(df_euro.columns) > 1 else df_euro.columns[0])

        df_euro['parsed_date'] = pd.to_datetime(df_euro[edate_col], errors='coerce')
        df_euro['month_day'] = df_euro['parsed_date'].dt.strftime('%m-%d')

        query_euro = st.text_input("أدخل الشهر واليوم للبحث في Eurojackpot (مثال: 09-09 أو 10-15):", key="q_euro").strip()

        if query_euro:
            norm_eq = query_euro.replace('.', '-')
            eresults = df_euro[df_euro['month_day'] == norm_eq]
            if eresults.empty:
                parts = norm_eq.split('-')
                if len(parts) == 2:
                    eresults = df_euro[df_euro['month_day'] == f"{parts[1]}-{parts[0]}"]

            st.markdown(f"**عدد السحوبات المطابقة لهذا التاريخ:** `{len(eresults)}` سحب")
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
                if efound_nums and st.button("🎲 توليد أرقام Eurojackpot المقترحة بناءً على هذا التاريخ"):
                    counts = pd.Series(efound_nums).value_counts()
                    top_freq = list(counts.index[:10])
                    np.random.seed(len(efound_nums) * 19)
                    chosen = np.random.choice(top_freq, min(3, len(top_freq)), replace=False).tolist() if top_freq else []
                    remaining = [i for i in range(1, 51) if i not in chosen]
                    needed_main = 5 - len(chosen)
                    main_nums = sorted(chosen + np.random.choice(remaining, needed_main, replace=False).tolist())
                    euro_stars = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
                    st.success(f"🎯 **الأرقام المقترحة لـ Eurojackpot:** `{' - '.join(map(str, main_nums))}` + النجمتان: `{' & '.join(map(str, euro_stars))}`")

# ==================== التبويب الثالث: الأبراج الفلكية ====================
with main_tab3:
    st.subheader("♈ اختيار البرج الفلكي وتوليد الأرقام حسب طاقته")
    st.markdown("اختر برجك أدناه للحصول على توقعات أرقام مخصصة لطاقته الفلكية:")

    zodiacs = [
        {"name": "الحمل (Aries)", "symbol": "♈", "element": "النار", "range": "21 مارس - 19 أبريل"},
        {"name": "الثور (Taurus)", "symbol": "♉", "element": "الأرض", "range": "20 أبريل - 20 مايو"},
        {"name": "الجوزاء (Gemini)", "symbol": "♊", "element": "الهواء", "range": "21 مايو - 20 يونيو"},
        {"name": "السرطان (Cancer)", "symbol": "♋", "element": "الماء", "range": "21 يونيو - 22 يوليو"},
        {"name": "الأسد (Leo)", "symbol": "♌", "element": "النار", "range": "23 يوليو - 22 أغسطس"},
        {"name": "العذراء (Virgo)", "symbol": "♍", "element": "الأرض", "range": "23 أغسطس - 22 سبتمبر"},
        {"name": "الميزان (Libra)", "symbol": "♎", "element": "الهواء", "range": "23 سبتمبر - 22 أكتوبر"},
        {"name": "العقرب (Scorpio)", "symbol": "♏", "element": "الماء", "range": "23 أكتوبر - 21 نوفمبر"},
        {"name": "القوس (Sagittarius)", "symbol": "♐", "element": "النار", "range": "22 نوفمبر - 21 ديسمبر"},
        {"name": "الجدي (Capricorn)", "symbol": "♑", "element": "الأرض", "range": "22 ديسمبر - 19 يناير"},
        {"name": "الدلو (Aquarius)", "symbol": "♒", "element": "الهواء", "range": "20 يناير - 18 فبراير"},
        {"name": "الحوت (Pisces)", "symbol": "♓", "element": "الماء", "range": "19 فبراير - 20 مارس"}
    ]

    selected_zodiac = st.selectbox("اختر البرج:", [z['name'] + " " + z['symbol'] for z in zodiacs])
    
    if st.button("🔮 توليد أرقام طاقة البرج"):
        # استخراج اسم البرج واستخدام بصمة نصية لتوليد أرقام فريدة لكل برج
        seed_val = sum([ord(c) for c in selected_zodiac])
        np.random.seed(seed_val)
        z_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
        st.success(f"✨ **الأرقام المقترحة لبرج {selected_zodiac}:**")
        st.markdown(f"### `{' - '.join(map(str, z_nums))}`")

# ==================== التبويب الرابع: تاريخ الميلاد ====================
with main_tab4:
    st.subheader("📅 توليد توقعات متعددة بناءً على تاريخ الميلاد الشخصي")
    
    b_date = st.date_input("أدخل تاريخ ميلادك الكامل:", value=datetime(1995, 6, 15), key="birth_input")
    
    if st.button("🌟 توليد 3 توقعات مختلفة لتاريخ الميلاد"):
        st.markdown("---")
        for i in range(1, 4):
            np.random.seed(b_date.toordinal() + i * 43)
            b_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            st.success(f"📌 **التوقع رقم {i}:** `{' - '.join(map(str, b_nums))}`")
