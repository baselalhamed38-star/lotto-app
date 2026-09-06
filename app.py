import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو والأبراج المتقدم", page_icon="🔮", layout="wide")

# دالة ذكية لتحميل وقراءة الملفات واستخراج أعمدة التاريخ والأرقام بمرونة
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
        # بيانات افتراضية للتجربة في حال لم يتم رفع ملف
        sample_data = [
            {"full_date": "1955-09-09", "date_md": "09-09", "year": 1955, "numbers": "5, 12, 23, 34, 42, 15"},
            {"full_date": "2010-09-09", "date_md": "09-09", "year": 2010, "numbers": "3, 14, 25, 33, 40, 8"},
            {"full_date": "2023-05-12", "date_md": "05-12", "year": 2023, "numbers": "7, 11, 19, 28, 39, 22"},
            {"full_date": "2022-05-12", "date_md": "05-12", "year": 2022, "numbers": "5, 11, 14, 28, 33, 41"}
        ]
        return pd.DataFrame(sample_data)

st.title("🔮 النظام الاحترافي لتحليل سحوبات اللوتو والأبراج والفلك")
st.markdown("---")

# الشريط الجانبي لرفع الملفات
st.sidebar.header("📂 ملف السحوبات الخاص بك")
uploaded_file = st.sidebar.file_uploader("قم بتحديث ملف الـ JSON أو CSV:", type=["json", "csv"])

df_lotto = load_data(uploaded_file)

if df_lotto.empty:
    st.warning("⚠️ الملف المرفوع فارغ أو لا يحتوي على بيانات صالحة.")
else:
    # توحيد أسماء الأعمدة لتجنب أخطاء عدم مطابقة الأسماء في ملفك
    # سنبحث عن أعمدة التاريخ والأرقام بغض النظر عن تسميتها
    date_col = next((col for col in df_lotto.columns if 'date' in col.lower() or 'تاريخ' in col), df_lotto.columns[0])
    num_col = next((col for col in df_lotto.columns if 'num' in col.lower() or 'result' in col.lower() or 'رقم' in col or 'ارقام' in col), df_lotto.columns[1] if len(df_lotto.columns) > 1 else df_lotto.columns[0])

    tab1, tab2, tab3 = st.tabs(["📅 البحث المتقدم بالتاريخ", "✨ الأبراج وتوليد الاحتمالات المتعددة", "📊 الإحصائيات والتحليل الحقيقي"])

    # التبويب الأول: البحث المتقدم بالتاريخ
    with tab1:
        st.subheader("🔍 البحث الدقيق في السحوبات السابقة")
        st.info("💡 يمكنك البحث بصيغة الشهر واليوم مباشرة (مثال: `09-09` أو `09.09`) وسيظهر لك كافة السحوبات المطابقة عبر السنين.")
        
        query = st.text_input("أدخل التاريخ للبحث (مثال: 09-09 أو 1955):", "").strip()
        
        if query:
            # تنظيف المدخلات لدعم الفاصلة أو النقطة
            normalized_query = query.replace('.', '-')
            
            # البحث في كافة الأعمدة وخاصة عمود التاريخ
            mask = df_lotto.astype(str).apply(lambda x: x.str.contains(normalized_query, case=False, na=False) | x.str.contains(query, case=False, na=False)).any(axis=1)
            results = df_lotto[mask]
            
            st.markdown(f"**عدد السحوبات المطابقة لـ ({query}):** `{len(results)}` سحب")
            
            if not results.empty:
                for _, row in results.iterrows():
                    d_val = row.get(date_col, 'غير متوفر')
                    n_val = row.get(num_col, 'غير متوفر')
                    st.success(f"📅 **التاريخ:** {d_val}\n\n🔢 **الأرقام المسحوبة:** `{n_val}`")
            else:
                st.warning("⚠️ لم يتم العثور على سحوبات مطابقة لهذا التاريخ. تأكد من صيغة البحث.")

    # التبويب الثاني: الأبراج وتوليد احتمالات متعددة بناءً على تاريخ الميلاد
    with tab2:
        st.subheader("🌟 توليد توقعات متعددة للأرقام بناءً على تاريخ الميلاد والأبراج")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            birth_date = st.date_input("اختر تاريخ ميلادك:", value=datetime(1990, 5, 15))
            
        with col_b2:
            # تحديد البرج مع الأيقونة والاسم المعبر
            def get_zodiac_details(date):
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
            
            zodiac_name, element = get_zodiac_details(birth_date)
            st.info(f"✨ برجك الفلكي: **{zodiac_name}** | العنصر: **{element}**")
            
        if st.button("🔮 توليد 3 توقعات واحتمالات مختلفة"):
            st.markdown("---")
            st.markdown("### 🎲 التوقعات المقترحة لبرجك:")
            
            # توليد خوارزميات متعددة (3 خيارات مختلفة)
            for i in range(1, 4):
                # نغير البذور الحسابية لكل خيار ليعطيك تشكيلات مختلفة ومتنوعة
                np.random.seed(birth_date.toordinal() + i * 17)
                generated_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
                st.success(f"📌 **التوقع رقم {i}:** `{', '.join(map(str, generated_nums))}`")

    # التبويب الثالث: الإحصائيات وتحليل الأرقام من الملف الحقيقي
    with tab3:
        st.subheader("📊 الإحصائيات والتحليل الشامل من ملف السحوبات الفعلي")
        
        all_numbers = []
        for nums_str in df_lotto[num_col]:
            if pd.notna(nums_str):
                # تنظيف النصوص واستخراج الأرقام وحدها
                clean_str = str(nums_str).replace('،', ',').replace('.', ',')
                parts = [p.strip() for p in clean_str.split(',') if p.strip().isdigit()]
                all_numbers.extend([int(p) for p in parts])
                
        if all_numbers:
            s = pd.Series(all_numbers)
            counts = s.value_counts().reset_index()
            counts.columns = ['الرقم', 'التكرار']
            counts = counts.sort_values(by='التكرار', ascending=False)
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("**🔥 أكثر الأرقام تكراراً في السحوبات:**")
                st.dataframe(counts.head(5), hide_index=True)
                
            with col_s2:
                st.markdown("**❄️ أقل الأرقام تكراراً (الأرقام الباردة):**")
                st.dataframe(counts.tail(5), hide_index=True)
                
            st.markdown("---")
            st.markdown("**📈 رسم بياني لتوزيع تكرار الأرقام:**")
            st.bar_chart(counts.set_index('الرقم'))
        else:
            st.warning("⚠️ تعذر استخراج الأرقام بشكل صحيح من عمود الأرقام في الملف. تأكد أن عمود الأرقام يحتوي على أرقام مفصولة بفواصل.")
