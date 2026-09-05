import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="سحوبات اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

@st.cache_data
def load_data():
    # استبدل هذا الرابط أو البيانات بملف الـ JSON الفعلي الخاص بك
    raw_data = [
        {"full_date": "1955-09-05", "date_md": "09-05", "year": 1955, "numbers": "5, 12, 23, 34, 42"},
        {"full_date": "2020-10-09", "date_md": "10-09", "year": 2020, "numbers": "3, 14, 25, 33, 40"},
        {"full_date": "2023-05-12", "date_md": "05-12", "year": 2023, "numbers": "7, 11, 19, 28, 39"}
    ]
    return pd.DataFrame(raw_data)

st.title("🔢 نظام البحث في سحوبات اللوتو")
st.write("ابحث بالتاريخ (مثال: **09-05** أو **1955-09-05**):")

df_lotto = load_data()

if df_lotto.empty:
    st.error("⚠️ لا توجد بيانات متاحة.")
else:
    query = st.text_input("أدخل الشهر واليوم أو التاريخ الكامل:", "").strip()
    
    if query:
        # تحويل الأعمدة إلى نص للبحث المرن
        mask = df_lotto.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        results = df_lotto[mask]
        
        st.markdown("---")
        st.subheader(f"نتائج البحث ({len(results)} سحب مطابق):")
        
        if not results.empty:
            for _, row in results.iterrows():
                # التحقق من أسماء الأعمدة المتوفرة في بياناتك
                full_date = row.get('full_date', row.get('date', 'غير متوفر'))
                year = row.get('year', '')
                numbers = row.get('numbers', row.get('result', 'غير متوفر'))
                
                st.success(f"📅 **التاريخ:** {full_date} " + (f"(السنة: {year})" if year else "") + f"\n\n🔢 **الأرقام:** {numbers}")
        else:
            st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ. تأكد من صحة التاريخ المدخل.")
    else:
        st.info("💡 اكتب التاريخ في خانة البحث بالأعلى لعرض السحوبات المطابقة فوراً.")
