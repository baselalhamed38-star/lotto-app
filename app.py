import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="برنامج البحث في الملفات", page_icon="📅", layout="centered")

# قائمة الملفات مع تحديد اليوم والشهر فقط (MM-DD)
files_data = [
    {"title": "Villa", "author": "Maya Alhamwi", "date": "05-12", "category": "عقارات"},
    {"title": "Steuererklärung", "author": "basel alhamed", "date": "03-10", "category": "ضرائب"},
    {"title": "فانتوم", "author": "basel alhamed", "date": "01-15", "category": "مستندات عامة"},
    {"title": "TrustWalletBackup", "author": "basel alhamed", "date": "11-20", "category": "أمان وتشفير"},
    {"Title": "Finanzamt Dokumente", "author": "basel alhamed", "date": "04-02", "category": "الضرائب المالية"}
]

st.title("📅 نظام البحث في الملفات حسب (اليوم والشهر)")
st.write("ابحث عن أي ملف بكتابة الشهر أو اليوم (مثل: `03-10` أو `05`):")

# حقل البحث
query = st.text_input("أدخل نص أو تاريخ للبحث:", "").strip().lower()

# تصفية الملفات بناءً على البحث
filtered_files = [
    f for f in files_data 
    if query in f['date'].lower() or query in f['title'].lower() or query in f['author'].lower()
]

st.markdown("---")
st.subheader("نتائج البحث:")

if filtered_files:
    for item in filtered_files:
        st.info(f"📅 **التاريخ (الشهر-اليوم):** {item['date']}  \n  📄 **الملف:** {item['title']}  \n  👤 **الكاتب:** {item['author']}  \n  📂 **التصنيف:** {item['category']}")
else:
    st.warning("⚠️ لم يتم العثور على أي ملف مطابق للبحث.")
