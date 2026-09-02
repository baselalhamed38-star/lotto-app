import streamlit as st
import datetime
import random

st.set_page_config(page_title="نظام اللوتو الذكي", layout="centered")

st.title("🎰 نظام توقعات اللوتو الذكي")
st.markdown("أدخل تاريخ ميلادك لمعرفة أرقام الحظ الخاصة بك:")

birth_date = st.date_input("تاريخ الميلاد", datetime.date(1990, 5, 15))

if st.button("توليد أرقام الحظ"):
    d = birth_date.day
    m = birth_date.month
    y = birth_date.year
    
    base_val = (d * 3 + m * 7 + y) % 49 + 1
    random.seed(d + m + y)
    formula_nums = sorted(list(set([(base_val + i * 7) % 49 + 1 for i in range(6)])))
    while len(formula_nums) < 6:
        r = random.randint(1, 49)
        if r not in formula_nums:
            formula_nums.append(r)
    formula_nums = sorted(formula_nums[:6])
    super_z = (d + m) % 10
    
    st.success("تم توليد التشكيلة بنجاح!")
    st.markdown(f"### الأرقام المقترحة: {', '.join(map(str, formula_nums))}")
    st.markdown(f"### الرقم الخارق (Superzahl): {super_z}")
