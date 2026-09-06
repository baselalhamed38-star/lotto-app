import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="نظام تحليل سحوبات اللوتو", page_icon="🎯", layout="wide")

st.title("🎯 النظام المباشر لتحليل والبحث في سحوبات اللوتو و Eurojackpot")

@st.cache_data
def load_files(uploaded_files):
    if not uploaded_files:
        return pd.DataFrame()
    
    all_data = []
    for file in uploaded_files:
        filename = file.name.lower()
        try:
            if filename.endswith(('.xlsx', '.xls')):
                # قراءة ملفات الإكسل عبر openpyxl
                xls = pd.ExcelFile(file)
                for sheet in xls.sheet_names:
                    df_s = pd.read_excel(xls, sheet_name=sheet, header=None)
                    if not df_s.empty:
                        df_s['File_Sheet'] = f"{file.name} -> {sheet}"
                        all_data.append(df_s)
            elif filename.endswith('.csv'):
                df_c = pd.read_csv(file, header=None, encoding='utf-8', errors='ignore')
                if not df_c.empty:
                    df_c['File_Sheet'] = file.name
                    all_data.append(df_c)
        except Exception as e:
            st.error(f"خطأ في ملف {file.name}: {e}")
            
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

def parse_draws(df):
    if df.empty:
        return pd.DataFrame()
    
    extracted = []
    for _, row in df.iterrows():
        vals = row.astype(str).values
        src = row.get('File_Sheet', 'ملف')
        date_val = None
        date_pos = -1
        
        # البحث عن خلية تاريخ
        for idx, val in enumerate(vals):
            v = val.strip()
            if '.' in v and len(v) <= 12 and any(c.isdigit() for c in v):
                parts = v.split('.')
                if len(parts) >= 2 and parts[0].isdigit():
                    date_val = v
                    date_pos = idx
                    break
        
        if date_val and date_pos != -1:
            nums = []
            for i in range(date_pos + 1, len(vals)):
                cell = vals[i].strip().replace('.0', '')
                if cell.isdigit() and len(cell) <= 2:
                    nums.append(cell)
            
            if len(nums) >= 5:
                main_ns = ", ".join(nums[:6] if len(nums) >= 6 else nums[:5])
                extra_n = nums[6] if len(nums) >= 7 else (nums[5] if len(nums) == 6 else nums[-1])
                
                extracted.append({
                    'source': src,
                    'date': date_val,
                    'numbers': main_ns,
                    'extra': extra_n
                })
                
    return pd.DataFrame(extracted)

st.sidebar.header("📂 رفع الملفات الرسمية")
l_files = st.sidebar.file_uploader("ملفات اللوتو (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="lf")
e_files = st.sidebar.file_uploader("ملفات Eurojackpot (Excel / CSV):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="ef")

df_lotto = parse_draws(load_files(l_files))
df_euro = parse_draws(load_files(e_files))

tab1, tab2 = st.tabs(["🍀 اللوتو (Lotto)", "💶 يوروجاكبوت (Eurojackpot)"])

def run_tab(df, name, is_euro=False):
    st.subheader(f"البحث في سحوبات وقاعدة بيانات {name}")
    
    if df.empty:
        st.warning(f"⚠️ يرجى رفع ملفات {name} بصيغة Excel (.xlsx) أو CSV من القائمة الجانبية.")
        return
        
    st.success(f"✅ تم تحميل وقراءة {len(df)} سحب بنجاح!")
    
    with st.expander("👁️ عرض جدول السحوبات المستخرجة"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    query = st.text_input(f"بحث عن تاريخ أو رقم في سحوبات {name} (مثال: 09.09 أو 2020 أو رقم معين):", key=f"q_{name}").strip()
    
    if query:
        res = df[df['date'].str.contains(query, case=False, na=False) | 
                 df['numbers'].str.contains(query, case=False, na=False) | 
                 df['source'].str.contains(query, case=False, na=False)]
        st.info(f"النتائج المطابقة: **{len(res)}** نتيجة")
        
        if not res.empty:
            for _, r in res.iterrows():
                if not is_euro:
                    st.success(f"📂 **المصدر:** `{r['source']}` | 📅 **التاريخ:** `{r['date']}` \n\n 🔢 **الأرقام:** `{r['numbers']}` \n\n 🌟 **Superzahl:** `{r['extra']}`")
                else:
                    st.success(f"📂 **المصدر:** `{r['source']}` | 📅 **التاريخ:** `{r['date']}` \n\n 💶 **الأرقام:** `{r['numbers']}` \n\n ⭐ **Sternzahl:** `{r['extra']}`")
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لبحثك.")
            
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
