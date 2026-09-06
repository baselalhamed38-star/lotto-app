import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو", page_icon="🎯", layout="wide")

st.title("🎯 النظام المباشر لتحليل والبحث في سحوبات اللوتو و Eurojackpot")

@st.cache_data
def load_all_sheets_excel(uploaded_files):
    if not uploaded_files:
        return pd.DataFrame()
    
    all_draws = []
    for file in uploaded_files:
        filename = file.name.lower()
        try:
            if filename.endswith(('.xlsx', '.xls')):
                # قراءة كل النوافذ (Sheets) داخل ملف الإكسل
                xls = pd.ExcelFile(file)
                for sheet_name in xls.sheet_names:
                    df_sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                    if not df_sheet.empty:
                        # إضافة اسم الملف ورقم النافذة/الشيت لكل صف لتسهيل التمييز
                        df_sheet['Source_Info'] = f"{file.name} ➔ [نافذة: {sheet_name}]"
                        all_draws.append(df_sheet)
            elif filename.endswith('.csv'):
                df_csv = pd.read_csv(file, header=None, encoding='utf-8', errors='ignore')
                if not df_csv.empty:
                    df_csv['Source_Info'] = f"{file.name}"
                    all_draws.append(df_csv)
        except Exception as e:
            st.error(f"❌ خطأ في قراءة الملف {file.name}: {e}")
            
    if all_draws:
        return pd.concat(all_draws, ignore_index=True)
    return pd.DataFrame()

st.sidebar.header("📂 رفع ملفات الإكسل متعددة النوافذ")
st.sidebar.info("💡 ارفع ملف الإكسل الذي يحتوي على عدة نوافذ (مثل 2018، 2019، 2020).")

l_files = st.sidebar.file_uploader("ملفات اللوتو (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="lf")
e_files = st.sidebar.file_uploader("ملفات Eurojackpot (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="ef")

df_lotto_raw = load_all_sheets_excel(l_files)
df_euro_raw = load_all_sheets_excel(e_files)

tab1, tab2 = st.tabs(["🍀 اللوتو (Lotto)", "💶 يوروجاكبوت (Eurojackpot)"])

def run_game_tab(df, name, is_euro=False):
    st.subheader(f"البحث الشامل في جميع نوافذ وعامّات {name}")
    
    if df.empty:
        st.info(f"💡 يرجى رفع ملف الإكسل الخاص بـ {name} من القائمة الجانبية لعرض كافة النوافذ.")
        return
        
    st.success(f"✅ تم قراءة جميع النوافذ والبيانات بنجاح لـ {name}!")
    
    with st.expander("👁️ عرض محتوى جميع النوافذ مجتمعة"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    query = st.text_input(f"🔍 بحث في كل النوافذ (أدخل تاريخ مثل 01.01 أو رقم معين):", key=f"q_{name}").strip()
    
    if query:
        # البحث في جميع الخلايا والأعمدة عبر كل النوافذ
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        res = df[mask]
        
        st.info(f"عدد النتائج المطابقة في كل النوافذ: **{len(res)}** صف")
        
        if not res.empty:
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لبحثك في أي من نوافذ هذا الملف.")
            
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
    run_game_tab(df_lotto_raw, "اللوتو", False)

with tab2:
    run_game_tab(df_euro_raw, "Eurojackpot", True)
