import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل وتوقع سحوبات اللوتو و Eurojackpot والأبراج", page_icon="🎰", layout="wide")

# دالة ذكية لتحميل ملفات اللوتو (تدعم CSV, JSON, Excel بكل نوافذه)
@st.cache_data
def load_lotto_data(uploaded_file):
    if uploaded_file is not None:
        try:
            filename = uploaded_file.name.lower()
            if filename.endswith('.json'):
                return pd.read_json(uploaded_file)
            elif filename.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif filename.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(uploaded_file)
                dfs = [pd.read_excel(xls, sheet_name=s) for s in xls.sheet_names]
                return pd.concat(dfs, ignore_index=True)
        except Exception:
            return pd.DataFrame()
    # بيانات تجريبية افتراضية
    return pd.DataFrame([
        {"full_date": "1955-09-09", "numbers": "5, 12, 23, 34, 42, 15"},
        {"full_date": "2010-09-09", "numbers": "3, 14, 25, 33, 40, 8"},
        {"full_date": "2015-09-09", "numbers": "5, 14, 23, 28, 40, 12"},
        {"full_date": "2023-05-12", "numbers": "7, 11, 19, 28, 39, 22"}
    ])

# دالة ذكية لتحميل ملفات يوروجاكبوت (تدعم جميع النوافذ في الاكسل)
@st.cache_data
def load_euro_data(uploaded_file):
    if uploaded_file is not None:
        try:
            filename = uploaded_file.name.lower()
            if filename.endswith('.json'):
                return pd.read_json(uploaded_file)
            elif filename.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif filename.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(uploaded_file)
                dfs = [pd.read_excel(xls, sheet_name=s) for s in xls.sheet_names]
                return pd.concat(dfs, ignore_index=True)
        except Exception:
            return pd.DataFrame()
    # بيانات تجريبية افتراضية
    return pd.DataFrame([
        {"full_date": "2020-09-09", "numbers": "10, 18, 27, 35, 44 + 3, 7"},
        {"full_date": "2022-10-15", "numbers": "2, 15, 22, 38, 49 + 1, 9"}
    ])

# دالة موحدة لاستخراج الشهر واليوم بدقة من أي نص تاريخ
def extract_month_day(date_val):
    if pd.isna(date_val):
        return ""
    s_val = str(date_val).strip()
    # محاولة تحويله لتاريخ لمعالجة الصيغ المختلفة
    dt = pd.to_datetime(s_val, errors='coerce')
    if pd.notna(dt):
        return dt.strftime('%m-%d')
    # إذا كان نصياً مثل 09.09 أو 09-09
    s_val = s_val.replace('.', '-')
    parts = s_val.split('-')
    if len(parts) >= 3: # صيغة YYYY-MM-DD
        return f"{parts[1]}-{parts[2]}"
    elif len(parts) == 2: # صيغة MM-DD أو DD-MM
        return f"{parts[0]}-{parts[1]}"
    return s_val

st.title("🎰 النظام الاحترافي الشامل للوتو و Eurojackpot والأبراج والفلك")
st.markdown("---")

st.sidebar.header("📂 إدارة ملفات السحوبات")
lotto_file = st.sidebar.file_uploader("رفع ملف سحوبات (Lotto - JSON/CSV/Excel):", type=["json", "csv", "xlsx", "xls"], key="lotto")
euro_file = st.sidebar.file_uploader("رفع ملف سحوبات (Eurojackpot - JSON/CSV/Excel):", type=["json", "csv", "xlsx", "xls"], key="euro")

df_lotto = load_lotto_data(lotto_file)
df_euro = load_euro_data(euro_file)

main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
    "🎯 سحوبات اللوتو", 
    "💶 سحوبات Eurojackpot", 
    "♈ قسم الأبراج الفلكية", 
    "📅 توقعات تاريخ الميلاد"
])

# ==================== التبويب الأول: اللوتو ====================
with main_tab1:
    st.subheader("🎯 البحث والتحليل في سحوبات اللوتو")
    if df_lotto.empty:
        st.warning("⚠️ لا توجد بيانات للوتو متاحة.")
    else:
        date_col = next((col for col in df_lotto.columns if 'date' in col.lower() or 'تاريخ' in col), df_lotto.columns[0])
        num_col = next((col for col in df_lotto.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_lotto.columns[1] if len(df_lotto.columns) > 1 else df_lotto.columns[0])

        df_lotto['clean_md'] = df_lotto[date_col].apply(extract_month_day)

        query_lotto = st.text_input("أدخل الشهر واليوم للبحث في اللوتو (مثال: 09.09 أو 09-09):", key="q_lotto").strip()

        if query_lotto:
            norm_q = query_lotto.replace('.', '-')
            results = df_lotto[df_lotto['clean_md'] == norm_q]
            if results.empty:
                parts = norm_q.split('-')
                if len(parts) == 2:
                    results = df_lotto[df_lotto['clean_md'] == f"{parts[1]}-{parts[0]}"]

            st.markdown(f"**عدد السحوبات المطابقة لهذا التاريخ عبر السنوات:** `{len(results)}` سحب")
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

# ==================== التبويب الثاني: يوروجاكبوت ====================
with main_tab2:
    st.subheader("💶 البحث والتحليل في سحوبات Eurojackpot (عبر كل النوافذ)")
    if df_euro.empty:
        st.warning("⚠️ لا توجد بيانات لـ Eurojackpot متاحة.")
    else:
        edate_col = next((col for col in df_euro.columns if 'date' in col.lower() or 'تاريخ' in col), df_euro.columns[0])
        enum_col = next((col for col in df_euro.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_euro.columns[1] if len(df_euro.columns) > 1 else df_euro.columns[0])

        df_euro['clean_md'] = df_euro[edate_col].apply(extract_month_day)

        query_euro = st.text_input("أدخل الشهر واليوم للبحث في Eurojackpot (مثال: 09.09 أو 10-15):", key="q_euro").strip()

        if query_euro:
            norm_eq = query_euro.replace('.', '-')
            eresults = df_euro[df_euro['clean_md'] == norm_eq]
            if eresults.empty:
                parts = norm_eq.split('-')
                if len(parts) == 2:
                    eresults = df_euro[df_euro['clean_md'] == f"{parts[1]}-{parts[0]}"]

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

# ==================== التبويب الثالث: الأبراج الفلكية ====================
with main_tab3:
    st.subheader("♈ الأبراج الفلكية وتوليد احتمالات متعددة لكل برج")
    st.markdown("اختر البرج أدناه، وسيولد لك النظام عدة احتمالات وأرقام مبنية على طاقة البرد:")

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

    selected_zodiac = st.selectbox("اختر البرج المراد توليد الأرقام له:", [f"{z['symbol']} {z['name']} ({z['element']})" for z in zodiacs])
    
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
