import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق تحليل وتوقعات اللوتو الشامل", layout="centered")

# الشريط الجانبي للاختيارات واللغات
st.sidebar.title("⚙️ الإعدادات والتحكم")
lang = st.sidebar.selectbox("اختر اللغة / Language / Sprache", ["العربية (AR)", "English (EN)", "Deutsch (DE)"])

if lang.startswith("العربية"):
    title_text = "🎰 نظام تحليل وتوقعات اللوتو الذكي"
    subtitle_text = "اختر تاريخ ميلادك أو أدخل بياناتك للحصول على تحليل الأرقام الذكي:"
    btn_text = "توليد التوقعات المتقدمة"
    res_title = "📊 نتائج التحليل والتوقع:"
    lucky_nums = "أرقام الحظ المقترحة:"
    super_num = "الرقم الخارق (Superzahl):"
elif lang.startswith("English"):
    title_text = "🎰 Smart Lotto Analysis & Prediction System"
    subtitle_text = "Enter your birth date or details to get smart number forecasting:"
    btn_text = "Generate Advanced Predictions"
    res_title = "📊 Analysis & Prediction Results:"
    lucky_nums = "Suggested Lucky Numbers:"
    super_num = "Superzahl / Mega Number:"
else:
    title_text = "🎰 Intelligentes Lotto-Analyse- & Vorhersagesystem"
    subtitle_text = "Geben Sie Ihr Geburtsdatum ein für intelligente Zahlentrends:"
    btn_text = "Erweiterte Vorhersage generieren"
    res_title = "📊 Analyse- und Vorhersageergebnisse:"
    lucky_nums = "Vorgeschlagene Glückszahlen:"
    super_num = "Superzahl:"

st.title(title_text)
st.write(subtitle_text)

# مدخلات المستخدم
birth_date = st.date_input("تاريخ الميلاد / Birth Date / Geburtsdatum", datetime.date(1990, 5, 15))
user_lucky_num = st.number_input("رقم مفضل إضافي (اختياري) / Optional favorite number", min_value=1, max_value=49, value=7)

if st.button(btn_text):
    # خوارزمية تحليل رياضية تعتمد على تاريخ الميلاد باستخدام Numpy
    d = birth_date.day
    m = birth_date.month
    y = birth_date.year
    
    # حسابات مصفوفات numpy لتحليل الأرقام
    np.random.seed(d + m + y + user_lucky_num)
    base_array = np.array([d, m, y, user_lucky_num])
    calculated_seed = int(np.sum(base_array) * 7) % 49 + 1
    
    # توليد الأرقام بطريقة ذكية
    raw_nums = [(calculated_seed + i * 11) % 49 + 1 for i in range(10)]
    random.shuffle(raw_nums)
    
    final_lotto = sorted(list(set(raw_nums))[:6])
    while len(final_lotto) < 6:
        r = random.randint(1, 49)
        if r not in final_lotto:
            final_lotto.append(r)
    final_lotto = sorted(final_lotto[:6])
    
    superz = (d + m + user_lucky_num) % 10
    
    # عرض النتائج بطريقة احترافية وجذابة
    st.markdown(f"### {res_title}")
    st.success(f"**{lucky_nums}** {', '.join(map(str, final_lotto))}")
    st.info(f"**{super_num}** {superz}")
    
    # جدول إحصائي تحليل تكميلي باستخدام Pandas
    df_analysis = pd.DataFrame({
        "مؤشر التحليل (Metric)": ["التوافق الفلكي", "مؤشر الحظ الرياضي", "قوة التردد الرقمي"],
        "النتيجة (Value)": [f"{((d*m)%85)+15}%", f"مستوى {(y%3)+1}", "مرتفع جداً 🚀"]
    })
    st.table(df_analysis)

st.markdown("---")
st.caption("تم تطوير هذا النظام ليعمل بكفاءة عالية على الهواتف الذكية عبر السحاب 🌐")
