import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="سحوبات اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

# تغيير اسم الدالة لتحديث الـ Cache تماماً وإجبار Streamlit على قراءة الكود الجديد
@st.cache_data
def load_lotto_data_fresh():
    files = [f for f in glob.glob("LOTTO*.xlsx") if "2021" not in f]
    all_draws = []
    
    for file in files:
        try:
            xls = pd.ExcelFile(file)
            for sheet in xls.sheet_names:
                if sheet.isdigit() and 1955 <= int(sheet) <= 1964:
                    df = pd.read_excel(file, sheet_name=sheet)
                    for _, row in df.iterrows():
                        val = row.get('Unnamed: 1')
                        if pd.notna(val) and hasattr(val, 'year'):
                            date_obj = pd.to_datetime(val)
                            date_str = date_obj.strftime('%m-%d')
                            full_date_str = date_obj.strftime('%Y-%m-%d')
                            
                            nums = [str(int(row.get(f'Unnamed: i'))) for i in range(2, 8) if pd.notna(row.get(f'Unnamed: i'))]
                            zusatz = row.get('Unnamed: 8')
                            zusatz_str = f" | الرقم الإضافي: {int(zusatz)}" if pd.notna(zusatz) else ""
                            
                            all_draws.append({
                                "date_md": date_str,
                                "full_date": full_date_str,
                                "year": sheet,
                                "numbers": " - ".join(nums) + zusatz_str,
                                "file": file
                            })
        except Exception as e:
            pass
            
    return pd.DataFrame(all_draws)

st.title("🔢 نظام البحث السريع في سحوبات اللوتو")
st.write("ابحث بالتاريخ (الشهر واليوم) لاستخراج أرقام السحب من الملفات المحددة:")

# تحميل البيانات الجديدة
with st.spinner("جاري تحميل بيانات السحوبات..."):
    df_lotto = load_lotto_data_fresh()

# حقل البحث
query = st.text_input("أدخل التاريخ (مثال: 05-12 أو 03):", "").strip().lower()

if query:
    # طريقة بحث آمنة جداً تتفادى أي KeyError مهما كانت الأعمدة
    if not df_lotto.empty and 'date_md' in df_lotto.columns and 'full_date' in df_lotto.columns:
        mask = df_lotto['date_md'].astype(str).str.lower().str.contains(query) | df_lotto['full_date'].astype(str).str.lower().str.contains(query)
        results = df_lotto[mask]
    else:
        results = pd.DataFrame()
    
    st.markdown("---")
    st.subheader(f"نتائج البحث ({len(results)} سحب مطابق):")
    
    if not results.empty:
        for _, row in results.iterrows():
            st.success(f"📅 **التاريخ:** {row['full_date']} (سنة: {row['year']})\n\n"
                       f"🔢 **الأرقام:** {row['numbers']}\n\n"
                       f"📂 **الملف:** {row['file']}")
    else:
        st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ أو البيانات فارغة.")
else:
    st.info("💡 اكتب التاريخ في خانة البحث بالأعلى لعرض السحوبات المطابقة فوراً.")
