import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو", page_icon="🎯", layout="wide")

st.title("🎯 النظام المباشر لتحليل والبحث في سحوبات اللوتو و Eurojackpot")

@st.cache_data
def load_raw_excel(uploaded_files):
    if not uploaded_files:
        return pd.DataFrame()
    
    all_data = []
    for file in uploaded_files:
        filename = file.name.lower()
        try:
            if filename.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(file)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
                    if not df.empty:
                        # تنظيف الأعمدة وتحويلها لنصوص لتسهيل البحث
                        df = df.dropna(how='all')
                        df['المصدر'] = f"{file.name} [{sheet_name}]"
                        all_data.append(df)
            elif filename.endswith('.csv'):
                df = pd.read_csv(file, header=None, encoding='utf-8', errors='ignore')
                df = df.dropna(how='all')
                df['المصدر'] = file.name
                all_data.append(df)
        except Exception as e:
            st.error(f"❌ تعذر قراءة الملف {file.name}: {e}")
            
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

st.sidebar.header("📂 رفع ملفات الإكسل الرسمية")
st.sidebar.info("💡 ارفع ملف الإكسل الخاص بك وسيقوم النظام بقراءته وعرضه فوراً.")

l_files = st.sidebar.file_uploader("ملفات اللوتو (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="lf")
e_files = st.sidebar.file_uploader("ملفات Eurojackpot (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="ef")

df_lotto = load_raw_excel(l_files)
df_euro = load_raw_excel(e_files)

tab1, tab2 = st.tabs(["🍀 اللوتو (Lotto)", "💶 يوروجاكبوت (Eurojackpot)"])

def run_tab(df, name, is_euro=False):
    st.subheader(f"البحث المباشر في قاعدة بيانات {name}")
    
    if df.empty:
        st.info(f"💡 يرجى رفع ملف الإكسل الخاص بـ {name} من القائمة الجانبية في الأعلى.")
        return
        
    st.success(f"✅ تم رفع وقراءة ملف {name} بنجاح!")
    
    with st.expander("👁️ عرض محتوى الملف كاملاً"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    query = st.text_input(f"🔍 ابحث عن أي رقم، تاريخ، أو كلمة داخل ملفات {name}:", key=f"q_{name}").strip()
    
    if query:
        # البحث في جميع أعمدة الجدول دفعة واحدة
        mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
        res = df[mask]
        
        st.info(f"النتائج المطابقة لبحثك: **{len(res)}** صف")
        
        if not res.empty:
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لبحثك في هذا الملف.")
            
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
    run_tab(df_lotto, "اللوتو", False)

with tab2:
    run_tab(df_euro, "Eurojackpot", True)
