import streamlit as st
import pandas as pd
import datetime as dt
import random
from collections import Counter

# =========================================================
# إعدادات الصفحة
# =========================================================

st.set_page_config(
    page_title="LOTTO MATRIX PRO",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #111827 0%, #030712 100%);
    color: #f9fafb;
}

.pro-card {
    background: linear-gradient(
        135deg,
        rgba(31, 41, 55, 0.75) 0%,
        rgba(17, 24, 39, 0.85) 100%
    );
    backdrop-filter: blur(10px);
    border: 1px solid rgba(75, 85, 99, 0.4);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    padding: 12px 20px;
    width: 100%;
}

.ball-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
    align-items: center;
}

.lotto-ball,
.super-ball,
.euro-ball {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

.lotto-ball {
    background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
    color: #0f172a;
}

.super-ball {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    color: white;
}

.euro-ball {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# القائمة الجانبية
# =========================================================

st.sidebar.markdown("### 🌟 LOTTO MATRIX PRO")
st.sidebar.markdown("---")

game_type = st.sidebar.radio(
    "🎯 اختر اللعبة:",
    ["Lotto 6aus49", "Eurojackpot"]
)

is_euro = game_type == "Eurojackpot"

st.sidebar.markdown("---")
st.sidebar.markdown("📂 **رفع ملفات الأرشيف**")

uploaded_files = st.sidebar.file_uploader(
    "CSV أو Excel",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "⚡ التنقل:",
    [
        "📌 آخر سحب والأرشيف",
        "📅 البحث بالتاريخ والتوليد الذكي",
        "🎲 توليد أرقام السحب القادم",
        "🎂 تاريخ الميلاد",
        "♈ الأبراج",
        "⚙️ الأنظمة الرياضية"
    ]
)

# =========================================================
# قراءة الملفات
# =========================================================

@st.cache_data(show_spinner=False)
def load_archive(files):
    rows = []

    if not files:
        return pd.DataFrame()

    for uploaded_file in files:
        try:
            filename = uploaded_file.name.lower()

            if filename.endswith(".csv"):
                uploaded_file.seek(0)

                try:
                    dataframe = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="utf-8",
                        on_bad_lines="skip"
                    )
                except UnicodeDecodeError:
                    uploaded_file.seek(0)

                    dataframe = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="latin-1",
                        on_bad_lines="skip"
                    )

                for _, row in dataframe.iterrows():
                    rows.append(row.tolist())

            else:
                excel = pd.ExcelFile(uploaded_file)

                for sheet in excel.sheet_names:
                    dataframe = pd.read_excel(
                        uploaded_file,
                        sheet_name=sheet,
                        header=None
                    )

                    for _, row in dataframe.iterrows():
                        rows.append(row.tolist())

        except Exception as error:
            st.sidebar.error(
                f"تعذر قراءة الملف {uploaded_file.name}: {error}"
            )

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


df = load_archive(uploaded_files)

# =========================================================
# استخراج التاريخ والأرقام
# =========================================================

def parse_date(value):
    if pd.isna(value):
        return None

    if isinstance(value, (dt.datetime, dt.date, pd.Timestamp)):
        return pd.Timestamp(value).date()

    text = str(value).strip()

    if not text or text.isdigit():
        return None

    parsed = pd.to_datetime(
        text,
        errors="coerce",
        dayfirst=True
    )

    if pd.notna(parsed):
        return parsed.date()

    return None


def parse_integer(value):
    if pd.isna(value):
        return None

    try:
        number = float(str(value).replace(",", ".").strip())

        if number.is_integer():
            return int(number)

    except Exception:
        pass

    return None


def extract_row(row_values, euro_game=False):
    date_value = None
    numeric_values = []

    for value in row_values:
        parsed_date = parse_date(value)

        if parsed_date is not None:
            date_value = parsed_date
            continue

        number = parse_integer(value)

        if number is not None:
            numeric_values.append(number)

    # إزالة التكرارات
    unique_numbers = []

    for number in numeric_values:
        if number not in unique_numbers:
            unique_numbers.append(number)

    if euro_game:
        # Eurojackpot: خمسة أرقام من 1 إلى 50
        main_numbers = [
            number for number in unique_numbers
            if 1 <= number <= 50
        ][:5]

        # رقما Euro من 1 إلى 12
        extra_numbers = [
            number for number in unique_numbers
            if number not in main_numbers and 1 <= number <= 12
        ][:2]

        if len(main_numbers) != 5 or len(extra_numbers) != 2:
            return None

        return {
            "date": date_value,
            "numbers": sorted(main_numbers),
            "extra": sorted(extra_numbers)
        }

    # Lotto 6aus49
    main_numbers = [
        number for number in unique_numbers
        if 1 <= number <= 49
    ][:6]

    super_number = next(
        (
            number for number in unique_numbers
            if number not in main_numbers and 0 <= number <= 9
        ),
        None
    )

    if len(main_numbers) != 6:
        return None

    return {
        "date": date_value,
        "numbers": sorted(main_numbers),
        "extra": super_number
    }


def extract_all_records(dataframe, euro_game=False):
    records = []

    if dataframe.empty:
        return records

    for _, row in dataframe.iterrows():
        record = extract_row(row.tolist(), euro_game)

        if record and record["date"]:
            records.append(record)

    # حذف السجلات المكررة
    unique_records = []
    seen = set()

    for record in records:
        extra = record["extra"]

        if isinstance(extra, list):
            extra_key = tuple(extra)
        else:
            extra_key = extra

        key = (
            record["date"],
            tuple(record["numbers"]),
            extra_key
        )

        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    return sorted(
        unique_records,
        key=lambda item: item["date"],
        reverse=True
    )


records = extract_all_records(df, is_euro)

# =========================================================
# عرض الأرقام
# =========================================================

def render_balls(numbers, extra, euro_game=False):
    html = "<div class='ball-container'>"

    for number in numbers:
        html += f"<div class='lotto-ball'>{number}</div>"

    if euro_game:
        for number in extra:
            html += f"<div class='euro-ball'>{number}</div>"
    else:
        html += f"<div class='super-ball'>{extra}</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


def render_record(record):
    st.markdown(
        f"""
        <div class="pro-card">
            <b>📅 تاريخ السحب: {record["date"].strftime("%Y-%m-%d")}</b>
        """,
        unsafe_allow_html=True
    )

    render_balls(
        record["numbers"],
        record["extra"],
        euro_game=is_euro
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# التوليد الإحصائي
# =========================================================

def generate_smart_prediction(history, euro_game=False):
    """
    اختيار مبني على أكثر الأرقام تكراراً في السحوبات السابقة.
    لا يمثل ضماناً لنتيجة السحب.
    """

    if not history:
        return None

    main_counter = Counter()

    for record in history:
        main_counter.update(record["numbers"])

    if euro_game:
        extra_counter = Counter()

        for record in history:
            extra_counter.update(record["extra"])

        ranked_main = sorted(
            range(1, 51),
            key=lambda number: (
                main_counter[number],
                random.random()
            ),
            reverse=True
        )

        ranked_extra = sorted(
            range(1, 13),
            key=lambda number: (
                extra_counter[number],
                random.random()
            ),
            reverse=True
        )

        return (
            sorted(ranked_main[:5]),
            sorted(ranked_extra[:2])
        )

    extra_counter = Counter()

    for record in history:
        if record["extra"] is not None:
            extra_counter.update([record["extra"]])

    ranked_main = sorted(
        range(1, 50),
        key=lambda number: (
            main_counter[number],
            random.random()
        ),
        reverse=True
    )

    ranked_extra = sorted(
        range(0, 10),
        key=lambda number: (
            extra_counter[number],
            random.random()
        ),
        reverse=True
    )

    return (
        sorted(ranked_main[:6]),
        ranked_extra[0]
    )

# =========================================================
# الصفحات
# =========================================================

if menu == "📌 آخر سحب والأرشيف":

    st.markdown(f"### 🏆 أحدث السحوبات - {game_type}")

    if not records:
        st.info("ارفع ملف CSV أو Excel يحتوي على أرشيف السحوبات.")
    else:
        st.markdown("#### أحدث سحب مسجل:")
        render_record(records[0])

        st.markdown("#### 📚 الأرشيف الكامل")

        archive_rows = []

        for record in records:
            row = {
                "التاريخ": record["date"].strftime("%Y-%m-%d"),
                "الأرقام": ", ".join(
                    map(str, record["numbers"])
                )
            }

            if is_euro:
                row["الأرقام الإضافية"] = ", ".join(
                    map(str, record["extra"])
                )
            else:
                row["Superzahl"] = record["extra"]

            archive_rows.append(row)

        st.dataframe(
            pd.DataFrame(archive_rows),
            use_container_width=True,
            hide_index=True
        )


elif menu == "📅 البحث بالتاريخ والتوليد الذكي":

    st.markdown(
        f"### 📅 البحث بنفس اليوم والشهر - {game_type}"
    )

    col1, col2 = st.columns(2)

    with col1:
        selected_day = st.number_input(
            "اليوم",
            min_value=1,
            max_value=31,
            value=5
        )

    with col2:
        selected_month = st.number_input(
            "الشهر",
            min_value=1,
            max_value=12,
            value=9
        )

    matching_records = [
        record for record in records
        if record["date"].day == selected_day
        and record["date"].month == selected_month
    ]

    if not matching_records:
        st.warning(
            f"لا توجد سحوبات بتاريخ "
            f"{selected_day:02d}-{selected_month:02d} "
            "ضمن الملفات المرفوعة."
        )
    else:
        st.success(
            f"تم العثور على {len(matching_records)} سحب مطابق."
        )

        for record in matching_records:
            render_record(record)

        st.markdown(
            "### 🌟 اقتراح مبني على نتائج نفس اليوم والشهر"
        )

        prediction = generate_smart_prediction(
            matching_records,
            euro_game=is_euro
        )

        if prediction:
            numbers, extra = prediction

            st.markdown(
                """
                <div class="pro-card"
                     style="border: 2px solid #a855f7;">
                    <b>✨ التشكيلة الإحصائية المقترحة:</b>
                """,
                unsafe_allow_html=True
            )

            render_balls(
                numbers,
                extra,
                euro_game=is_euro
            )

            st.caption(
                "التشكيلة مبنية على تكرار الأرقام تاريخياً، "
                "وليست ضماناً لنتيجة السحب."
            )

            st.markdown("</div>", unsafe_allow_html=True)


elif menu == "🎲 توليد أرقام السحب القادم":

    st.markdown(
        f"### 🎲 توليد اقتراحات - {game_type}"
    )

    if st.button("🚀 توليد 3 تشكيلات"):

        for index in range(1, 4):

            if records:
                numbers, extra = generate_smart_prediction(
                    records,
                    euro_game=is_euro
                )
            else:
                if is_euro:
                    numbers = sorted(
                        random.sample(range(1, 51), 5)
                    )
                    extra = sorted(
                        random.sample(range(1, 13), 2)
                    )
                else:
                    numbers = sorted(
                        random.sample(range(1, 50), 6)
                    )
                    extra = random.randint(0, 9)

            st.markdown(
                f"""
                <div class="pro-card">
                    <b>التشكيلة رقم {index}</b>
                """,
                unsafe_allow_html=True
            )

            render_balls(
                numbers,
                extra,
                euro_game=is_euro
            )

            st.caption(
                "اقتراح إحصائي/عشوائي وليس تنبؤاً مضموناً."
            )

            st.markdown("</div>", unsafe_allow_html=True)


elif menu == "🎂 تاريخ الميلاد":

    st.markdown("### 🎂 أرقام مبنية على تاريخ الميلاد")

    birth_date = st.date_input(
        "أدخل تاريخ ميلادك:",
        dt.date(1995, 6, 15)
    )

    if st.button("✨ توليد أرقام تاريخ الميلاد"):

        seed = (
            birth_date.day
            + birth_date.month * 100
            + birth_date.year * 10000
        )

        rng = random.Random(seed)

        if is_euro:
            numbers = sorted(
                rng.sample(range(1, 51), 5)
            )
            extra = sorted(
                rng.sample(range(1, 13), 2)
            )
        else:
            numbers = sorted(
                rng.sample(range(1, 50), 6)
            )
            extra = rng.randint(0, 9)

        st.markdown(
            "<div class='pro-card'><b>🔮 أرقامك:</b>",
            unsafe_allow_html=True
        )

        render_balls(
            numbers,
            extra,
            euro_game=is_euro
        )

        st.markdown("</div>", unsafe_allow_html=True)


elif menu == "♈ الأبراج":

    st.markdown("### ♈ الأبراج")

    signs = [
        "الحمل", "الثور", "الجوزاء", "السرطان",
        "الأسد", "العذراء", "الميزان", "العقرب",
        "القوس", "الجدي", "الدلو", "الحوت"
    ]

    sign = st.selectbox("اختر برجك:", signs)

    if st.button("🔮 توليد أرقام البرج"):

        rng = random.Random(sign)

        if is_euro:
            numbers = sorted(
                rng.sample(range(1, 51), 5)
            )
            extra = sorted(
                rng.sample(range(1, 13), 2)
            )
        else:
            numbers = sorted(
                rng.sample(range(1, 50), 6)
            )
            extra = rng.randint(0, 9)

        st.markdown(
            f"""
            <div class="pro-card">
                <b>✨ برج {sign}</b>
            """,
            unsafe_allow_html=True
        )

        render_balls(
            numbers,
            extra,
            euro_game=is_euro
        )

        st.markdown("</div>", unsafe_allow_html=True)


else:

    st.markdown(f"### ⚙️ الأنظمة الرياضية - {game_type}")

    system = st.selectbox(
        "اختر النظام:",
        [
            "System 008",
            "System 010",
            "Full Matrix System"
        ]
    )

    if st.button("تفعيل النظام"):

        if system == "System 008":
            count = 8
        elif system == "System 010":
            count = 10
        else:
            count = 12

        st.success(
            f"تم اختيار {system}. "
            f"سيتم استخدام {count} أرقام أساسية."
        )

        st.info(
            "يمكن لاحقاً إضافة توليد جميع التركيبات "
            "من الأرقام المختارة حسب نظام اللعبة."
        )
