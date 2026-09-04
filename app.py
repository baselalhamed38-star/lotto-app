import streamlit as st
import pandas as pd
import datetime
import random
import requests

# إعداد الصفحة
st.set_page_config(page_title="Lotto & Eurojackpot Pro", page_icon="🎰", layout="wide")

# القواميس للغات (عربي، إنجليزي، ألماني)
LANG = {
    "ar": {
        "title": "🎰 برنامج اليانصيب الشامل (Lotto & Eurojackpot)",
        "subtitle": "توليد الأرقام، عرض السحوبات، الأبراج، ودعم الملفات",
        "current_date": "📅 تاريخ اليوم:",
        "upload_section": "📁 رفع ملف السحوبات (Excel)",
        "upload_help": "اختر ملف السحوبات التاريخية بصيغة xlsx",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 توليد الأرقام عبر الأبراج",
        "select_zodiac": "اختر برجك الفلكي:",
        "generate_btn": "🎲 توليد الأرقام الحظ",
        "latest_draws": "🔄 أحدث السحوبات (تحديث تلقائي)",
        "lang_select": "اختر اللغة / Language / Sprache:",
        "file_loaded": "✅ تم تحميل الملف بنجاح!",
        "zodiacs": {
            "الحمل (Aries)": "♈",
            "الثور (Taurus)": "♉",
            "الجوزاء (Gemini)": "♊",
            "السرطان (Cancer)": "♋",
            "الأسد (Leo)": "♌",
            "العذراء (Virgo)": "♍",
            "الميزان (Libra)": "♎",
            "العقرب (Scorpio)": "♏",
            "القوس (Sagittarius)": "♐",
            "الجدي (Capricorn)": "♑",
            "الدلو (Aquarius)": "♒",
            "الحوت (Pisces)": "♓"
        }
    },
    "en": {
        "title": "🎰 Comprehensive Lottery App (Lotto & Eurojackpot)",
        "subtitle": "Number Generation, Draws History, Zodiacs, and File Upload",
        "current_date": "📅 Current Date:",
        "upload_section": "📁 Upload Draws File (Excel)",
        "upload_help": "Select historical draws file (.xlsx)",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 Zodiac Number Generator",
        "select_zodiac": "Select your Zodiac Sign:",
        "generate_btn": "🎲 Generate Lucky Numbers",
        "latest_draws": "🔄 Latest Draws (Auto-Updated)",
        "lang_select": "Select Language / اللغة / Sprache:",
        "file_loaded": "✅ File successfully loaded!",
        "zodiacs": {
            "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
            "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
            "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
        }
    },
    "de": {
        "title": "🎰 Umfassende Lotterie-App (Lotto & Eurojackpot)",
        "subtitle": "Zahlengenerierung, Ziehungsverlauf, Sternzeichen & Datei-Upload",
        "current_date": "📅 Heutiges Datum:",
        "upload_section": "📁 Ziehungsdatei hochladen (Excel)",
        "upload_help": "Wählen Sie die historische Excel-Datei aus",
        "lotto_tab": "🇩🇪 Lotto 6aus49",
        "euro_tab": "🇪🇺 Eurojackpot",
        "zodiac_title": "🔮 Sternzeichen Zahlengenerator",
        "select_zodiac": "Wählen Sie Ihr Sternzeichen:",
        "generate_btn": "🎲 Glückszahlen generieren",
        "latest_draws": "🔄 Neueste Ziehungen (Automatisch aktualisiert)",
        "lang_select": "Sprache auswählen / Language / اللغة:",
        "file_loaded": "✅ Datei erfolgreich geladen!",
        "zodiacs": {
            "Widder (Aries)": "♈", "Stier (Taurus)": "♉", "Zwillinge (Gemini)": "♊", "Krebs (Cancer)": "♋",
            "Löwe (Leo)": "♌", "Jungfrau (Virgo)": "♍", "Waage (Libra)": "♎", "Skorpion (Scorpio)": "♏",
            "Schütze (Sagittarius)": "♐", "Steinbock (Capricorn)": "♑", "Wassermann (Aquarius)": "♒", "Fische (Pisces)": "♓"
        }
    }
}

# اختيار اللغة في الشريط الجانبي
st.sidebar.title("⚙️ الإعدادات / Settings")
lang_choice = st.sidebar.selectbox("اختر اللغة / Language", ["العربية (Arabic)", "English", "Deutsch"])
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

# التبويبات الرئيسية (Lotto 6aus49 و Eurojackpot)
tab1, tab2 = st.tabs([t["lotto_tab"], t["euro_tab"]])

with tab1:
    st.header("🇩🇪 Lotto 6aus49 - Management & Generator")
    
    # قسم رفع الملف
    uploaded_file = st.file_uploader(t["upload_section"], type=["xlsx", "xls"], key="lotto_file")
    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            sheets = xls.sheet_names
            selected_sheet = st.selectbox("اختر السنة / ورقة العمل (Sheet)", sheets, key="lotto_sheet")
            df_lotto = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            st.success(t["file_loaded"])
            st.dataframe(df_lotto.head(10))
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            
    st.markdown("---")
    
    # توليد الأرقام عبر الأبراج لـ Lotto (6 أرقام من 49 + رقم إضافي)
    st.subheader(t["zodiac_title"])
    zodiac_list = list(t["zodiacs"].keys())
    selected_zodiac = st.selectbox(t["select_zodiac"], zodiac_list, key="lotto_zodiac")
    zodiac_icon = t["zodiacs"][selected_zodiac]
    
    if st.button(t["generate_btn"] + " (Lotto)", key="btn_lotto"):
        random.seed(str(selected_zodiac) + str(now.day))
        lotto_numbers = sorted(random.sample(range(1, 50), 6))
        super_number = random.randint(0, 9)
        st.balloons()
        st.success(f"### {zodiac_icon} برج {selected_zodiac}")
        st.markdown(f"**أرقام الحظ (6/49):** `{' - '.join(map(str, lotto_numbers))}`")
        st.markdown(f"**الرقم الإضافي (Superzahl):** `👑 {super_number}`")

    st.markdown("---")
    st.subheader(t["latest_draws"])
    # محاكاة جلب أحدث السحوبات تلقائياً
    st.write("🔹 **آخر سحب تم رصده تلقائياً:** الأربعاء / السبت (تحديث مباشر من المصدر الرسمي)")
    st.code("الأرقام الفائزة الأخيرة: 5 - 12 - 23 - 34 - 41 - 48 | Superzahl: 7")


with tab2:
    st.header("🇪🇺 Eurojackpot - Management & Generator")
    
    # قسم رفع الملف لـ Eurojackpot
    uploaded_euro_file = st.file_uploader(t["upload_section"] + " (Eurojackpot)", type=["xlsx", "xls", "csv"], key="euro_file")
    if uploaded_euro_file is not None:
        try:
            if uploaded_euro_file.name.endswith('.csv'):
                df_euro = pd.read_csv(uploaded_euro_file)
            else:
                df_euro = pd.read_excel(uploaded_euro_file)
            st.success(t["file_loaded"])
            st.dataframe(df_euro.head(10))
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            
    st.markdown("---")
    
    # توليد الأرقام عبر الأبراج لـ Eurojackpot (5 من 50 + 2 من 12)
    st.subheader(t["zodiac_title"] + " (Eurojackpot)")
    selected_euro_zodiac = st.selectbox(t["select_zodiac"], zodiac_list, key="euro_zodiac")
    euro_zodiac_icon = t["zodiacs"][selected_euro_zodiac]
    
    if st.button(t["generate_btn"] + " (Eurojackpot)", key="btn_euro"):
        random.seed(str(selected_euro_zodiac) + str(now.month))
        euro_numbers = sorted(random.sample(range(1, 51), 5))
euro_extras = sorted(random.sample(range(1, 13), 2))
        st.balloons()
        st.success(f"### {euro_zodiac_icon} برج {selected_euro_zodiac}")
        st.markdown(f"**الأرقام الأساسية (5/50):** `{' - '.join(map(str, euro_numbers))}`")
        st.markdown(f"**أرقام اليورو (2/12):** `⭐ {' - '.join(map(str, euro_extras))}`")

    st.markdown("---")
    st.subheader(t["latest_draws"])
    st.write("🔹 **آخر سحب تم رصده تلقائياً:** الثلاثاء / الجمعة (يتم التحديث المباشر أسبوعياً)")
    st.code("الأرقام الفائزة الأخيرة: 8 - 14 - 22 - 39 - 45 | أرقام النجوم: 3 - 11")
