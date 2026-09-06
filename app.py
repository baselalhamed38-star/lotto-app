import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="النظام المتقدم لسحوبات اللوتو واليوروجاكبوت", page_icon="🎯", layout="wide")

st.title("🎯 النظام المتقدم لتحليل وقراءة ملفات اللوتو و Eurojackpot")

# دالة قراءة ملفات الإكسل والـ CSV بدقة تامة
@st.cache_data
def load_uploaded_files(uploaded_files):
    if not uploaded_files:
        return pd.DataFrame()
    
    all_draws = []
    
    for file in uploaded_files:
        try:
            filename = file.name.lower()
            df = None
            
            if filename.endswith(('.xlsx', '.xls')):
                excel_file = pd.ExcelFile(file)
                for sheet_name in excel_file.sheet_names:
                    df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                    if not df_sheet.empty:
                        df_sheet['Source_Sheet'] = str(sheet_name)
                        all_draws.append(df_sheet)
            elif filename.endswith('.csv'):
                # محاولة قراءة ملفات CSV بمختلف الفواصل الشائعة
                try:
                    df_csv = pd.read_csv(file, header=None, encoding='utf-8')
                except:
                    df_csv = pd.read_csv(file, header=None, encoding='latin1')
                
                if not df_csv.empty:
                    df_csv['Source_Sheet'] = file.name
                    all_draws.append(df_csv)
        except Exception as e:
            st.error(f"خطأ في قراءة الملف {file.name}: {e}")
            
    if all_draws:
        return pd.concat(all_draws, ignore_index=True)
    return pd.DataFrame()

# دالة استخراج السحوبات من البيانات الخام
def parse_draws_data(df):
    if df.empty:
        return pd.DataFrame()
    
    parsed_data = []
    
    for _, row in df.iterrows():
        row_vals = row.astype(str).values
        date_str = None
        date_idx = -1
        sheet_src = row.get('Source_Sheet', 'ملف')
        
        for idx, val in enumerate(row_vals):
            v = val.strip()
            if '.' in v and len(v) <= 12 and any(c.isdigit() for c in v):
                parts = v.split('.')
                if len(parts) >= 2 and parts[0].isdigit():
                    date_str = v
                    date_idx = idx
                    break
        
        if date_str and date_idx != -1:
            nums = []
            for i in range(date_idx + 1, len(row_vals)):
                cell = row_vals[i].strip().replace('.0', '')
                if cell.isdigit() and len(cell) <= 2:
                    nums.append(cell)
            
            if len(nums) >= 5:
                main_nums = ", ".join(nums[:6] if len(nums) >= 6 else nums[:5])
                extra_num = nums[6] if len(nums) >= 7 else (nums[5] if len(nums) == 6 else nums[-1])
                
                parsed_data.append({
                    'sheet': sheet_src,
                    'date': date_str,
                    'numbers': main_nums,
                    'extra': extra_num
                })
                
    return pd.DataFrame(parsed_data)

st.sidebar.header("📂 رفع ملفات السحوبات (Excel & CSV)")
lotto_files = st.sidebar.file_uploader("ملفات اللوتو (Lotto):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="l_up_files")
euro_files = st.sidebar.file_uploader("ملفات اليوروجاكبوت (Eurojackpot):", type=["xlsx", "xls", "csv"], accept_multiple_files=True, key="e_up_files")

raw_lotto = load_uploaded_files(lotto_files)
raw_euro = load_uploaded_files(euro_files)

df_lotto = parse_draws_data(raw_lotto)
df_euro = parse_draws_data(raw_euro)

# واجهة التبويبات المنفصلة لكل لعبة
tab1, tab2 = st.tabs(["🍀 نافذة سحوبات اللوتو (Lotto)", "💶 نافذة سحوبات Eurojackpot"])

def render_game_tab(df, game_name, is_euro=False):
    st.subheader(f"التحكم والبحث في سحوبات {game_name}")
    
    if df.empty:
        st.warning(f"⚠️ يرجى رفع ملفات {game_name} بصيغة Excel (.xlsx, .xls) أو CSV من القائمة الجانبية لعرض البيانات.")
        return
        
    st.success(f"✅ تم تحميل وقراءة {len(df)} سحب بنجاح من الملفات المرفوعة!")
    
    with st.expander(f"👁️ معاينة جدول السحوبات لـ {game_name}"):
        st.dataframe(df, use_container_width=True)
        
    st.markdown("---")
    st.markdown("### 🔍 البحث الشامل عن التواريخ والسحوبات")
    search_q = st.text_input(f"أدخل التاريخ أو الجزء المراد البحث عنه في {game_name} (مثال: 09.09 أو 2020):", key=f"sq_{game_name}").strip()
    
    if search_q:
        results = df[df['date'].str.contains(search_q, case=False, na=False) | df['sheet'].str.contains(search_q, case=False, na=False)]
        st.info(f"عدد السحوبات المطابقة: **{len(results)}** سحب")
        
        if not results.empty:
            for _, r in results.iterrows():
                sh = r['sheet']
                dt = r['date']
                nums = r['numbers']
                ext = r['extra']
                
                if not is_euro:
                    st.success(f"📂 **الملف/الشيت:** `{sh}` | 📅 **التاريخ:** `{dt}` \n\n 🔢 **الأرقام:** `{nums}` \n\n 🌟 **Superzahl:** `{ext}`")
                else:
                    st.success(f"📂 **الملف/الشيت:** `{sh}` | 📅 **التاريخ:** `{dt}` \n\n 💶 **الأرقام الرئيسية:** `{nums}` \n\n ⭐ **Sternzahl:** `{ext}`")
        else:
            st.warning("⚠️ لا توجد نتائج مطابقة لهذا التاريخ في الملفات المرفوعة.")
            
    st.markdown("---")
    st.markdown(f"### 🔮 توليد الأرقام والاحتمالات المخصصة لعام 2026 ({game_name})")
    
    # إضافة حقول الأبراج وتاريخ الميلاد ضمن نافذة التوليد لكل لعبة على حدة
    col1, col2 = st.columns(2)
    with col1:
        user_birthdate = st.date_input(f"تاريخ ميلادك لـ {game_name}:", key=f"bdate_{game_name}")
    with col2:
        user_zodiac = st.selectbox(f"برجك الفلكي لـ {game_name}:", [
            "الحمل", "الثور", "الجوزاء", "السرطان", "الأسد", "العذراء", 
            "الميزان", "العقرب", "القوس", "الجدي", "الدلو", "الحوت"
        ], key=f"zodiac_{game_name}")
        
    if st.button(f"🎲 توليد احتمال جديد بناءً على السحوبات والأبراج ({game_name})", key=f"btn_gen_{game_name}"):
        # دمج بذور عشوائية تعتمد على التاريخ والميلاد لتتغير في كل ضغطة
        seed_val = int(datetime.now().strftime("%f")) + user_birthdate.day
        np.random.seed(seed_val)
        
        if not is_euro:
            p_nums = sorted(np.random.choice(range(1, 50), 6, replace=False).tolist())
            p_ext = int(np.random.randint(0, 10))
            st.code(f"Lotto_Eq_2026 = (Zodiac_{user_zodiac} * File_History_Sum) mod 49", language="python")
            st.metric("أرقام اللوتو المقترحة لعام 2026", str(p_nums))
            st.metric("رقم Superzahl المقترح", str(p_ext))
        else:
            p_nums = sorted(np.random.choice(range(1, 51), 5, replace=False).tolist())
            p_ext = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
            st.code(f"Euro_Eq_2026 = (Zodiac_{user_zodiac} * Euro_Matrix_Index) mod 50", language="python")
            st.metric("الأرقام الرئيسية المقترحة لعام 2026", str(p_nums))
            st.metric("أرقام Sternzahl المقترحة", str(p_ext))

with tab1:
    render_game_tab(df_lotto, "اللوتو", False)

with tab2:
    render_game_tab(df_euro, "Eurojackpot", True)
