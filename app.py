import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="برنامج البحث في الملفات", page_icon="📅", layout="centered")

# قائمة الملفات بأسماء مفاتيح موحدة وصحيحة تماماً
files_data = [
    {"title": "Villa", "author": "Maya Alhamwi", "date": "05-12", "category": "عقارات"},
    {"title": "Steuererklärung", "author": "basel alhamed", "date": "03-10", "category": "ضرائب"},
    {"title": "فانتوم", "author": "basel alhamed", "date": "01-15", "category": "مستندات عامة"},
    {"title": "TrustWalletBackup", "author": "basel alhamed", "date": "11-20", "category": "أمان وتشفير"},
    {"title": "Finanzamt Dokumente", "author": "basel alhamed", "date": "04-02", "category": "الضرائب المالية"}
]

st.title("📅 نظام البحث في الملفات حسب (اليوم والشهر)")
st.write("ابحث عن أي ملف بكتابة الشهر أو اليوم (مثل: `03-10` أو `05`):")

# حقل البحث
query = st.text_input("أدخل نص أو تاريخ للبحث:", "").strip().lower()

# تصفية الملفات مع حماية الكود من أي خطأ في المفاتيح
filtered_files = []
for f in files_data:
    date_val = str(f.get('date', '')).lower()
    title_val = str(f.get('title', '')).lower()
    author_val = str(f.get('author', '')).lower()
    cat_val = str(f.get('category', '')).lower()
    
    if not query or query in date_val or query in title_val or query in author_val or query in cat_val:
        filtered_files.append(f)

st.markdown("---")
st.subheader("نتائج البحث:")

if filtered_files:
    for item in filtered_files:
        st.info(f"📅 **التاريخ (الشهر-اليوم):** {item.get('date')}  \n  📄 **الملف:** {item.get('title')}  \n  👤 **الكاتب:** {item.get('author')}  \n  📂 **التصنيف:** {item.get('category')}")
else:
    st.warning("⚠️ لم يتم العثور على أي ملف مطابق للبحث.")
