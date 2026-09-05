import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نتائج سحب اللوتو حسب التاريخ", page_icon="🔢", layout="centered")

# بيانات السحوبات مع الأرقام التي ظهرت في كل تاريخ (الشهر-اليوم)
lotto_data = [
    {"date": "05-12", "draw_numbers": "03 - 14 - 22 - 35 - 41  [النجمة: 5]", "title": "سحب فيلا (Villa)", "author": "Maya Alhamwi"},
    {"date": "03-10", "draw_numbers": "07 - 12 - 19 - 28 - 44  [النجمة: 2]", "title": "Steuererklärung", "author": "basel alhamed"},
    {"date": "01-15", "draw_numbers": "01 - 09 - 15 - 24 - 36  [النجمة: 8]", "title": "فانتوم", "author": "basel alhamed"},
    {"date": "11-20", "draw_numbers": "11 - 18 - 25 - 32 - 49  [النجمة: 3]", "title": "TrustWalletBackup", "author": "basel alhamed"},
    {"date": "04-02", "draw_numbers": "04 - 10 - 21 - 33 - 40  [النجمة: 7]", "title": "Finanzamt Dokumente", "author": "basel alhamed"}
]

st.title("🔢 أرقام السحب حسب التاريخ")
st.write("ابحث برقم اليوم أو الشهر (مثل: `05` أو `03-10`) لمعرفة الأرقام التي طلعت بالسحب في ذلك التاريخ:")

# حقل البحث
query = st.text_input("أدخل التاريخ (الشهر-اليوم أو جزء منه):", "").strip().lower()

# تصفية السحوبات بناءً على التاريخ المدخل
filtered_draws = []
for item in lotto_data:
    date_val = str(item.get('date', '')).lower()
    title_val = str(item.get('title', '')).lower()
    numbers_val = str(item.get('draw_numbers', '')).lower()
    
    if not query or query in date_val or query in title_val or query in numbers_val:
        filtered_draws.append(item)

st.markdown("---")
st.subheader("نتائج أرقام السحب:")

if filtered_draws:
    for item in filtered_draws:
        st.success(f"📅 **التاريخ:** {item.get('date')}  \n"
                   f"🔢 **الأرقام الخارجة بالسحب:** {item.get('draw_numbers')}  \n"
                   f"📄 **الملف المرتبط:** {item.get('title')} ({item.get('author')})")
else:
    st.warning("⚠️ لم يتم العثور على سحب مطابق لهذا التاريخ.")
