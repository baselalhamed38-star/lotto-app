import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو", page_icon="🎯", layout="wide")

st.title("🎯 النظام المباشر لتحليل والبحث في سحوبات اللوتو و Eurojackpot")

@st.cache_data
def load_embedded_excel():
    # البحث عن أي ملف إكسل في المجلد الحالي
    excel_files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
    if not excel_files:
        return pd.DataFrame(), "لا يوجد ملف إكسل"
    
    file_name = excel_files[0]
    all_draws = []
    try:
        xls = pd.ExcelFile(file_name)
        for sheet_name in xls.sheet_names:
            df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            if not df_sheet.empty:
                df_sheet['Source_Info'] = f"ملف: {file_name} ➔ [شيت: {sheet_name}]"
                all_draws.append(df_sheet)
    except Exception as e:
        return pd.DataFrame(), str(e)
        
    if all_draws:
        return pd.concat(all_draws, ignore_index=True), file_name
    return pd.DataFrame(), "الملف فارغ"

df_data, loaded_filename = load_embedded_excel()

tab1, tab2 = st.tabs(["🍀 اللوتو (Lotto)", "💶 يوروجاكبوت (Eurojackpot)"])

def run_game_tab(df, name, is_euro=False):
    st.subheader(f"البحث الشامل في جميع شيتات وقواعد بيانات {name}")
    
    if df.empty:
        st.error(f"⚠️ تنبيه: تأكد من وجود ملف الإكسل في مستودع GitHub (الملف الظاهر في صورتك هو LOTTO6aus49_2021.xlsx ولكنه قد يحتاج لثوانٍ حتى يتم تحديث السيرفر).")
        return
        
    st.success(f"✅ تم تحميل وقراءة جميع الشيتات بنجاح من الملف: `{loaded_filename}`")
    
    with st.expander("👁️ عرض محتوى جميع الشيتات مجتمعة"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    query = st.text_input(f"🔍 بحث في كل الشيتات (أدخل تاريخ مثل 01.01 أو رقم معين):", key=f"q_{name}").strip()
    
    if query:
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        res = df[mask]
        
        st.info(f"عدد النتائج المطابقة في كل الشيتات: **{len(res)}** صف")
        
        if not res.empty:
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لبحثك في أي من شيتات هذا الملف.")
            
    st.markdown("---")
    st.markdown(f"### 🔮 توليد احتمالات عام 2026 لـ {name}")
    if st.button(f"🎲 توليد احتمالات جديدة لـ {name}", key=f"btn_{name}"):
        np.random.seed(int(datetime.now().strftime("%f")))
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_ext = int(np.random.randint(0, 10))
            st.metric("أرقام اللوتو المقترحة", str(p_nums))
            st.metric("رقم Superzahl المقترح", str(p_ext))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_ext = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.metric("الأرقام الرئيسية المقترحة", str(p_nums))
            st.metric("أرقام Sternzahl المقترحة", str(p_ext))

with tab1:
    run_game_tab(df_data, "اللوتو", False)

with tab2:
    run_game_tab(df_data, "Eurojackpot", True)
