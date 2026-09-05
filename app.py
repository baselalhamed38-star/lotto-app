import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو والأبراج", page_icon="🔮", layout="wide")

# دالة لتحميل البيانات (سواء من ملف مرفوع أو بيانات افتراضية)
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                st.error("⚠️ صيغة الملف غير مدعومة. يرجى رفع ملف JSON أو CSV.")
                return pd.DataFrame()
            return df
        except Exception as e:
            st.error(f"⚠️ خطأ في قراءة الملف: {e}")
            return pd.DataFrame()
    else:
        # بيانات تجريبية افتراضية في حال لم يتم رفع ملف بعد
        sample_data = [
            {"full_date": "1955-09-05", "date_md": "09-05", "year": 1955, "numbers": "5, 12, 23, 34, 42, 15"},
            {"full_date": "2020-10-09", "date_md": "10-09", "year": 2020, "numbers": "3, 14, 25, 33, 40, 8"},
            {"full_date": "2023-05-12", "date_md": "05-12", "year": 2023, "numbers": "7, 11, 19, 28, 39, 22"},
            {"full_date": "2022-05-12", "date_md": "05-12", "year": 2022, "numbers": "5, 11, 14, 28, 33, 41"}
        ]
        return pd.DataFrame(sample_data)

st.title("🔮 النظام الشامل لتحليل سحوبات اللوتو والأبراج والاحتمالات")
st.markdown("---")

# شريط جانبي لرفع الملفات
st.sidebar.header("📂 إدارة البيانات")
uploaded_file = st.sidebar.file_uploader("قم بتحديث أو رفع ملف السحوبات (JSON أو CSV):", type=["json", "csv"])

df_lotto = load_data(uploaded_file)

if df_lotto.empty:
    st.warning("⚠️ الملف المرفوع فارغ أو لم يتم تحميل البيانات بشكل صحيح.")
else:
    # تقسيم الواجهة إلى تبويبات منظمة
    tab1, tab2, tab3 = st.tabs(["📅 البحث بالتاريخ", "✨ توقعات الأبراج وتاريخ الميلاد", "📊 إحصائيات وتحليل الأرقام"])

    # التبويب الأول: البحث بالتاريخ
    with tab1:
        st.subheader("🔍 البحث المتقدم في السحوبات السابقة")
        query = st.text_input("أدخل التاريخ (مثال: 05-12 أو 2023-05-12):", "").strip()
        
        if query:
            mask = df_lotto.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
            results = df_lotto[mask]
            
            st.markdown(f"**نتائج البحث المطابقة ({len(results)} سحب):**")
            if not results.empty:
                for _, row in results.iterrows():
                    full_date = row.get('full_date', row.get('date', 'غير متوفر'))
                    year = row.get('year', '')
                    numbers = row.get('numbers', row.get('result', 'غير متوفر'))
                    st.success(f"📅 **التاريخ:** {full_date} " + (f"(السنة: {year})" if year else "") + f"\n\n🔢 **الأرقام المسحوبة:** {numbers}")
            else:
                st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ.")

    # التبويب الثاني: توقعات الأبراج وتاريخ الميلاد
    with tab2:
        st.subheader("🌟 توليد احتمالات الأرقام بناءً على تاريخ الميلاد والأبراج")
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            birth_date = st.date_input("أدخل تاريخ ميلادك:", value=datetime(1990, 1, 1))
            
        with col_b2:
            def get_zodiac_sign(date):
                m, d = date.month, date.day
                if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "الحمل (Aries)"
                elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "الثور (Taurus)"
                elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "الجوزاء (Gemini)"
                elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "السرطان (Cancer)"
                elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "الأسد (Leo)"
                elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "العذراء (Virgo)"
                elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "الميزان (Libra)"
                elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "العقرب (Scorpio)"
                elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "القوس (Sagittarius)"
                elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "الجدي (Capricorn)"
                elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "الدلو (Aquarius)"
                else: return "الحوت (Pisces)"
            
            zodiac = get_zodiac_sign(birth_date)
            st.info(f"✨ برجك الفلكي: **{zodiac}**")
            
        if st.button("🔮 توليد الأرقام المقترحة"):
            np.random.seed(birth_date.toordinal())
            lucky_numbers = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            st.success(f"🔢 **الأرقام المقترحة لبرجك وتاريخ ميلادك:** `{', '.join(map(str, lucky_numbers))}`")

    # التبويب الثالث: الإحصائيات وتحليل الأرقام
    with tab3:
        st.subheader("📊 إحصائيات سحوبات اللوتو والتحليل الشامل")
        
        all_nums = []
        for nums_str in df_lotto.get('numbers', []):
            if pd.notna(nums_str):
                clean_str = str(nums_str).replace('،', ',')
                parts = [p.strip() for p in clean_str.split(',') if p.strip().isdigit()]
                all_nums.extend([int(p) for p in parts])
                
        if all_nums:
            s = pd.Series(all_nums)
            counts = s.value_counts().reset_index()
            counts.columns = ['الرقم', 'التكرار']
            counts = counts.sort_values(by='التكرار', ascending=False)
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("**🔥 أكثر الأرقام تكراراً:**")
                st.dataframe(counts.head(5), hide_index=True)
                
            with col_s2:
                st.markdown("**❄️ أقل الأرقام تكراراً:**")
                st.dataframe(counts.tail(5), hide_index=True)
                
            st.markdown("---")
            st.bar_chart(counts.set_index('الرقم'))
        else:
            st.info("💡 لا توجد بيانات كافية ضمن عمود الأرقام لعرض الإحصائيات.")
