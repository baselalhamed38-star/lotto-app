import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="سحوبات اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

@st.cache_data
def load_data():
    raw_json = r'''%JSON_DATA%'''
    return pd.read_json(io.StringIO(raw_json))

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
        
        st.markdown---()
        st.subheader(f"نتائج البحث ({len(results)} سحب مطابق):")
        
        if not results.empty:
            for _, row in results.iterrows():
                st.success(f"📅 **التاريخ:** {row['full_date']} (السنة: {row['year']})\n\n"
                           f"🔢 **الأرقام:** {row['numbers']}")
        else:
            st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ. تأكد من كتابة التاريخ بصيغة الشهر واليوم (مثال: `10-09`).")
    else:
        st.info("💡 اكتب التاريخ في خانة البحث بالأعلى لعرض السحوبات المطابقة فوراً.")
