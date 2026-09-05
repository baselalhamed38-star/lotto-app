import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="سحوبات اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

@st.cache_data
def load_lotto_data():
    # اختيار ملف واحد كافٍ لقراءة كافة السنوات لتفادي التكرار والبطء
    files = glob.glob("LOTTO*.xlsx")
    if not files:
        return pd.DataFrame()
    
    # نأخذ أول ملف متوفر (لأنه يحوي كافة الشيتات من 1955 إلى 1964)
    file = files[0]
    all_draws = []
    
    try:
        xls = pd.ExcelFile(file)
        for sheet in xls.sheet_names:
            if sheet.isdigit() and 1955 <= int(sheet) <= 1964:
                df = pd.read_excel(file, sheet_name=sheet)
                for _, row in df.iterrows():
                    val = row.get('Unnamed: 1')
                    if pd.notna(val) and hasattr(val, 'year'):
                        date_obj = pd.to_datetime(val)
                        date_str = date_obj.strftime('%m-%d') # الشهر واليوم (مثل 05-12)
                        full_date_str = date_obj.strftime('%Y-%m-%d') # التاريخ الكامل
                        
                        # استخراج أرقام السحب الأساسية (من العمود 2 إلى 7)
                        nums = [str(int(row.get(f'Unnamed: i'))) for i in range(2, 8) if pd.notna(row.get(f'Unnamed: i'))]
                        zusatz = row.get('Unnamed: 8')
                        zusatz_str = f" | الرقم الإضافي: {int(zusatz)}" if pd.notna(zusatz) else ""
                        
                        if nums:
                            all_draws.append({
                                "date_md": date_str,
                                "full_date": full_date_str,
                                "year": sheet,
                                "numbers": " - ".join(nums) + zusatz_str
                            })
    except Exception as e:
        st.error(f"خطأ أثناء قراءة الملفات: {e}")
        
    return pd.DataFrame(all_draws)

st.title("🔢 نظام البحث في سحوبات اللوتو")
st.write("ابحث بالتاريخ (مثال: **10-09** أو **05-12**):")

# تحميل البيانات مع مؤشر تحميل
with st.spinner("جاري تحميل قاعدة بيانات السحوبات..."):
    df_lotto = load_lotto_data()

if df_lotto.empty:
    st.error("⚠️ لم يتم العثور على ملفات إكسيل LOTTO*.xlsx في المجلد. تأكد من رفع الملفات إلى المستودع.")
else:
    # حقل البحث
    query = st.text_input("أدخل الشهر واليوم (مثال: 09-10 أو 05-12):", "").strip()
    
    if query:
        # تصفية البيانات بشكل فوري ودقيق
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
            st.warning("⚠️ لم يتم العثور على أي سحب مطابق لهذا التاريخ. تأكد من كتابة التاريخ بصيغة الشهر-اليوم (مثال: `10-09`).")
    else:
        st.info("💡 اكتب التاريخ في خانة البحث بالأعلى لعرض السحوبات المطابقة فوراً.")
