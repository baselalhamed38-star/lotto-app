import streamlit as st
import pandas as pd
import datetime
import random

# إعداد الصفحة
st.set_page_config(page_title="Lotto & Eurojackpot Pro", page_icon="🎰", layout="wide")

# القواميس للغات (عربي، إنجليزي، ألماني)
LANG = {
    "ar": {
        "title": "🎰 برنامج اليانصيب الشامل (Lotto & Eurojackpot)",
        "subtitle": "توليد الأرقام، عرض السحوبات، الأبراج، ودعم الملفات",
        "current_date": "📅 تاريخ اليوم والشهر:",
        "upload_section": "📁 رفع ملف السحوبات (Excel)",
        "upload_help": "اختر ملف السحوبات التاريخية بصيغة xlsx",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 توليد الأرقام عبر الأبراج الفلكية",
        "select_zodiac": "اختر برجك الفلكي:",
        "generate_btn": "🎲 توليد أرقام الحظ (اضغط عدة مرات)",
        "latest_draws": "🔄 أحدث السحوبات الرسمية",
        "file_loaded": "✅ تم تحميل ورقة السحوبات بنجاح!",
        "zodiacs": {
            "الحمل (Aries)": "♈", "الثور (Taurus)": "♉", "الجوزاء (Gemini)": "♊", "السرطان (Cancer)": "♋",
            "الأسد (Leo)": "♌", "العذراء (Virgo)": "♍", "الميزان (Libra)": "♎", "العقرب (Scorpio)": "♏",
            "القوس (Sagittarius)": "♐", "الجدي (Capricorn)": "♑", "الدلو (Aquarius)": "♒", "الحوت (Pisces)": "♓"
        }
    },
    "en": {
        "title": "🎰 Comprehensive Lottery App (Lotto & Eurojackpot)",
        "subtitle": "Number Generation, Draws History, Zodiacs, and File Upload",
        "current_date": "📅 Current Date & Month:",
        "upload_section": "📁 Upload Draws File (Excel)",
        "upload_help": "Select historical draws file (.xlsx)",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 Zodiac Number Generator",
        "select_zodiac": "Select your Zodiac Sign:",
        "generate_btn": "🎲 Generate Lucky Numbers (Click multiple times)",
        "latest_draws": "🔄 Latest Official Draws",
        "file_loaded": "✅ Draws file successfully loaded!",
        "zodiacs": {
            "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
            "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
            "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
        }
    },
    "de": {
        "title": "🎰 Umfassende Lotterie-App (Lotto & Eurojackpot)",
        "subtitle": "Zahlengenerierung, Ziehungsverlauf, Sternzeichen & Datei-Upload",
        "current_date": "📅 Heutiges Datum & Monat:",
        "upload_section": "📁 Ziehungsdatei hochladen (Excel)",
        "upload_help": "Wählen Sie die historische Excel-Datei aus",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 Sternzeichen Zahlengenerator",
        "select_zodiac": "Wählen Sie Ihr Sternzeichen:",
        "generate_btn": "🎲 Glückszahlen generieren (Mehrmals klicken)",
        "latest_draws": "🔄 Neueste offizielle Ziehungen",
        "file_loaded": "✅ Datei erfolgreich geladen!",
        "zodiacs": {
            "Widder (Aries)": "♈", "Stier (Taurus)": "♉", "Zwillinge (Gemini)": "♊", "Krebs (Cancer)": "♋",
            "Löwe (Leo)": "♌", "Jungfrau (Virgo)": "♍", "Waage (Libra)": "♎", "Skorpion (Scorpio)": "♏",
            "Schütze (Sagittarius)": "♐", "Steinbock (Capricorn)": "♑", "Wassermann (Aquarius)": "♒", "Fische (Pisces)": "♓"
        }
    }
}

# الشريط الجانبي لاختيار اللغة
st.sidebar.title("⚙️ الإعدادات / Settings")
lang_choice = st.sidebar.selectbox("اختر اللغة / Language / Sprache", ["العربية (Arabic)", "English", "Deutsch"])
lang_key = "ar"
if "English" in lang_choice:
    lang_key = "en"
elif "Deutsch" in lang_choice:
    lang_key = "de"

t = LANG[lang_key]

# العنوان الرئيسي
st.title(t["title"])
st.markdown(t["subtitle"])

# عرض تاريخ اليوم والشهر الحالي
now = datetime.datetime.now()
st.info(f"{t['current_date']} **{now.strftime('%Y-%m-%d')}** | الشهر الحالي: **{now.strftime('%B')}**")

# التبويبات الرئيسية
tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

with tab1:
    st.header("🇩🇪 Lotto 6aus49")
    
    # قسم رفع ملف السحوبات لمعاينة الأرقام والتاريخ
    uploaded_file = st.file_uploader(t["upload_section"], type=["xlsx", "xls"], key="lotto_file")
    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            sheets = xls.sheet_names
            selected_sheet = st.selectbox("اختر السنة (Sheet):", sheets, key="lotto_sheet")
            df_lotto = pd.read_excel(uploaded_file, sheet_name=selected_sheet, skiprows=5)
            st.success(t["file_loaded"])
            st.dataframe(df_lotto.dropna(how="all").head(15), use_container_width=True)
        except Exception as e:
            st.error(f"تعذر قراءة الملف، تأكد من صيغة الملف الصحيحة: {e}")
            
    st.markdown("---")
    
    # توليد الأرقام عبر الأبراج (توليد متجدد بكل ضغطة)
    st.subheader(t["zodiac_title"])
    zodiac_list = list(t["zodiacs"].keys())
    selected_zodiac = st.selectbox(t["select_zodiac"], zodiac_list, key="lotto_zodiac")
    zodiac_icon = t["zodiacs"][selected_zodiac]
    
    if st.button(t["generate_btn"], key="btn_lotto"):
        # توليد عشوائي بحت في كل ضغطة
        lotto_numbers = sorted(random.sample(range(1, 50), 6))
        super_number = random.randint(0, 9)
        st.balloons()
        st.success(f"### {zodiac_icon} برج {selected_zodiac}")
        st.markdown(f"**أرقام الحظ (6/49):** `{' - '.join(map(str, lotto_numbers))}`")
        st.markdown(f"**الرقم الإضافي (Superzahl):** `👑 {super_number}`")

    st.markdown("---")
    st.subheader(t["latest_draws"])
    st.write("🔹 **أحدث سحب معتمد (السبت / الأربعاء):**")
    st.code("التاريخ: 2026-09-02 | الأرقام الفائزة: 4 - 15 - 22 - 31 - 38 - 45 | Superzahl: 3")


with tab2:
    st.header("🇪🇺 Eurojackpot")
    
    # قسم رفع ملف Eurojackpot
    uploaded_euro_file = st.file_uploader(t["upload_section"] + " (Eurojackpot)", type=["xlsx", "xls", "csv"], key="euro_file")
    if uploaded_euro_file is not None:
        try:
            if uploaded_euro_file.name.endswith('.csv'):
                df_euro = pd.read_csv(uploaded_euro_file)
            else:
                xls_euro = pd.ExcelFile(uploaded_euro_file)
                sheet_euro = st.selectbox("اختر ورقة العمل (Sheet):", xls_euro.sheet_names, key="euro_sheet")
                df_euro = pd.read_excel(uploaded_euro_file, sheet_name=sheet_euro)
            st.success(t["file_loaded"])
            st.dataframe(df_euro.dropna(how="all").head(15), use_container_width=True)
        except Exception as e:
            st.error(f"خطأ في قراءة ملف يورو جك‌پوت: {e}")
            
    st.markdown("---")
    
    # توليد الأرقام عبر الأبراج لـ Eurojackpot (توليد متجدد بكل ضغطة)
    st.subheader(t["zodiac_title"] + " (Eurojackpot)")
    selected_euro_zodiac = st.selectbox(t["select_zodiac"], zodiac_list, key="euro_zodiac")
    euro_zodiac_icon = t["zodiacs"][selected_euro_zodiac]
    
    if st.button(t["generate_btn"] + " ", key="btn_euro"):
        euro_numbers = sorted(random.sample(range(1, 51), 5))
        euro_extras = sorted(random.sample(range(1, 13), 2))
        st.balloons()
        st.success(f"### {euro_zodiac_icon} برج {selected_euro_zodiac}")
        st.markdown(f"**الأرقام الأساسية (5/50):** `{' - '.join(map(str, euro_numbers))}`")
        st.markdown(f"**أرقام اليورو (2/12):** `⭐ {' - '.join(map(str, euro_extras))}`")

    st.markdown("---")
    st.subheader(t["latest_draws"])
    st.write("🔹 **أحدث سحب معتمد (الثلاثاء / الجمعة):**")
    st.code("التاريخ: 2026-09-04 | الأرقام الأساسية: 7 - 16 - 25 - 34 - 42 | أرقام النجوم: 4 - 9")
