import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل وتوقع سحوبات اللوتو", page_icon="🎯", layout="wide")

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return pd.DataFrame()
            return df
        except Exception:
            return pd.DataFrame()
    else:
        # بيانات افتراضية للتجربة
        sample_data = [
            {"full_date": "1955-09-09", "numbers": "5, 12, 23, 34, 42, 15"},
            {"full_date": "2010-09-09", "numbers": "3, 14, 25, 33, 40, 8"},
            {"full_date": "2015-09-09", "numbers": "5, 14, 23, 28, 40, 12"},
            {"full_date": "2023-05-12", "numbers": "7, 11, 19, 28, 39, 22"}
        ]
        return pd.DataFrame(sample_data)

st.title("🎯 النظام المتقدم لتحليل وتوقع سحوبات اللوتو حسب التاريخ")
st.markdown("---")

st.sidebar.header("📂 ملف البيانات")
uploaded_file = st.sidebar.file_uploader("رفع ملف الـ JSON أو CSV:", type=["json", "csv"])

df_lotto = load_data(uploaded_file)

if df_lotto.empty:
    st.warning("⚠️ لا توجد بيانات متاحة.")
else:
    # التعرف على عمود التاريخ والأرقام بذكاء
    date_col = next((col for col in df_lotto.columns if 'date' in col.lower() or 'تاريخ' in col), df_lotto.columns[0])
    num_col = next((col for col in df_lotto.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_lotto.columns[1] if len(df_lotto.columns) > 1 else df_lotto.columns[0])

    # معالجة تواريخ الملف لاستخراج الشهر واليوم بدقة (لضمان مطابقة اليوم والشهر فقط دون السنة)
    df_lotto['parsed_date'] = pd.to_datetime(df_lotto[date_col], errors='coerce')
    df_lotto['month_day'] = df_lotto['parsed_date'].dt.strftime('%m-%d') # صيغة ثابتة MM-DD

    tab1, tab2 = st.tabs(["📅 البحث الدقيق بالتاريخ (يوم وشهر)", "✨ توقعات الأبراج والفلك"])

    with tab1:
        st.subheader("🔍 البحث الدقيق بيوم وشهر السحب")
        st.info("💡 أدخل الشهر واليوم (مثال: `09-09` أو `09.09`) ليبحث النظام حصرياً عن السحوبات التي حدثت في هذا اليوم من كل السنوات دون التأثر بالسنة.")
        
        query = st.text_input("أدخل الشهر واليوم (مثال: 09-09 أو 05-12):", "").strip()
        
        if query:
            # توحيد إدخال المستخدم إلى صيغة MM-DD
            norm_query = query.replace('.', '-')
            
            # محاولة فهم المدخلات (سواء كتب المستخدم يوم-شهر أو شهر-يوم)
            # سنقوم بمطابقة النطاق الذي ينتهي أو يطابق الشهر واليوم المدخل
            results = df_lotto[
                df_lotto['month_day'] == norm_query
            ]
            
            # إذا لم يجد تطابقاً مباشراً، نبحث بطريقة تدعم عكس اليوم والشهر احتياطياً
            if results.empty:
                parts = norm_query.split('-')
                if len(parts) == 2:
                    reversed_query = f"{parts[1]}-{parts[0]}"
                    results = df_lotto[df_lotto['month_day'] == reversed_query]

            st.markdown(f"**عدد السحوبات المسجلة في هذا اليوم والشهر عبر السنين:** `{len(results)}` سحب")
            
            if not results.empty:
                found_numbers = []
                for _, row in results.iterrows():
                    d_val = row.get(date_col, 'غير متوفر')
                    n_val = row.get(num_col, 'غير متوفر')
                    st.success(f"📅 **التاريخ:** {d_val} \n\n 🔢 **الأرقام:** `{n_val}`")
                    
                    if pd.notna(n_val):
                        clean_str = str(n_val).replace('،', ',').replace('.', ',')
                        parts_nums = [p.strip() for p in clean_str.split(',') if p.strip().isdigit()]
                        found_numbers.extend([int(p) for p in parts_nums])
                
                st.markdown("---")
                st.subheader("📊 تحليل أرقام السحوبات المطابقة وتوليد الـ 6 مقترحات:")
                
                if found_numbers:
                    s = pd.Series(found_numbers)
                    counts = s.value_counts()
                    
                    st.write(f"الأرقام الأكثر تكراراً في هذا التاريخ تاريخياً: `{list(counts.head(6).index)}`")
                    
                    if st.button("🎲 توليد 6 أرقام مقترحة بناءً على سحوبات هذا التاريخ"):
                        top_frequent = list(counts.index[:10])
                        np.random.seed(len(found_numbers) * 13)
                        
                        sample_size = min(3, len(top_frequent))
                        chosen_frequent = np.random.choice(top_frequent, sample_size, replace=False).tolist() if top_frequent else []
                        
                        remaining_pool = [i for i in range(1, 50) if i not in chosen_frequent]
                        needed = 6 - len(chosen_frequent)
                        chosen_random = np.random.choice(remaining_pool, needed, replace=False).tolist()
                        
                        final_suggestion = sorted(chosen_frequent + chosen_random)
                        
                        st.balloons()
                        st.success(f"🎯 **الـ 6 أرقام المقترحة بناءً على تحليل تاريخ ({query}):**")
                        st.markdown(f"### `{' - '.join(map(str, final_suggestion))}`")
                else:
                    st.warning("⚠️ لا توجد أرقام كافية ضمن السحوبات المطابقة لتحليلها.")
            else:
                st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا اليوم والشهر. تأكد من صيغة الإدخال (مثال: 09-09).")

    with tab2:
        st.subheader("🌟 توليد توقعات الأبراج وتاريخ الميلاد")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            birth_date = st.date_input("تاريخ ميلادك:", value=datetime(1990, 5, 15))
        with col_b2:
            def get_zodiac(date):
                m, d = date.month, date.day
                if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "♈ الحمل (Aries)", "النار"
                elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "♉ الثور (Taurus)", "الأرض"
                elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "♊ الجوزاء (Gemini)", "الهواء"
                elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "♋ السرطان (Cancer)", "الماء"
                elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "♌ الأسد (Leo)", "النار"
                elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "♍ العذراء (Virgo)", "الأرض"
                elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "♎ الميزان (Libra)", "الهواء"
                elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "♏ العقرب (Scorpio)", "الماء"
                elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "♐ القوس (Sagittarius)", "النار"
                elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "♑ الجدي (Capricorn)", "الأرض"
                elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "♒ الدلو (Aquarius)", "الهواء"
                else: return "♓ الحوت (Pisces)", "الماء"
            
            z_name, elem = get_zodiac(birth_date)
            st.info(f"✨ البرج: **{z_name}** | العنصر: **{elem}**")
            
        if st.button("🔮 توليد توقعات الأبراج المتعددة"):
            for i in range(1, 4):
                np.random.seed(birth_date.toordinal() + i * 31)
                nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
                st.success(f"📌 **التوقع {i}:** `{' - '.join(map(str, nums))}`")
