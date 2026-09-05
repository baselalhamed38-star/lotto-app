import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="سحوبات اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

@st.cache_data
def load_data():
    # ضع بيانات الـ JSON الخاصة بك هنا، أو استبدل هذه القائمة بملف الـ JSON الفعلي
    raw_data = [
        {"full_date": "1955-10-09", "date_md": "10-09", "year": 1955, "numbers": "5, 12, 23, 34, 42"},
        {"full_date": "2020-10-09", "date_md": "10-09", "year": 2020, "numbers": "3, 14, 25, 33, 40"},
        {"full_date": "2023-05-12", "date_md": "05-12", "year": 2023, "numbers": "7, 11, 19, 28, 39"}
    ]
    return pd.DataFrame(raw_data)

st.title("🔢 نظام البحث في سحوبات اللوتو")
st.write("ابحث بالتاريخ (مثال: **10-09** أو **1955-10-09**):")

df_lotto = load_data()

if df_lotto.empty:
    st.error("⚠️ لا توجد بيانات متاحة.")
else:
    query = st.text_input("أدخل الشهر واليوم أو التاريخ الكامل:", "").strip()
    
    if query:
        mask = df_lotto['date_md'].astype(str).str.contains(query, case=False, na=False) | \
               df_lotto['full_date'].astype(str).str.contains(query, case=False, na=False)
        results = df_lotto[mask]
        
        st.markdown("---")
        st.subheader(f"نتائج البحث ({len(results)} سحب مطابق):")
        
        if not results.empty:
            for _, row in results.iterrows():
                st.success(f"📅 **التاريخ:** {row['full_date']} (السنة: {row['year']})\n\n"
                           f"🔢 **الأرقام:** {row['numbers']}")
        else:
            st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ. تأكد من كتابة التاريخ بصيغة الشهر واليوم (مثال: `10-09`).")
    else:
        st.info("💡 اكتب التاريخ في خانة البحث بالأعلى لعرض السحوبات المطابقة فوراً.")
