import streamlit as st
import pandas as pd
import datetime as dt
import random
from collections import Counter

# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="LOTTO HISTORY ANALYZER",
    page_icon="🎱",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #111827 0%, #030712 100%);
    color: #f9fafb;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.card {
    background: rgba(31, 41, 55, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
}

.ball-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 12px;
    margin-bottom: 8px;
}

.ball {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    box-shadow: 0 3px 10px rgba(0,0,0,.35);
}

.main-ball {
    background: linear-gradient(135deg, #ffffff, #cbd5e1);
    color: #111827;
}

.super-ball {
    background: linear-gradient(135deg, #ef4444, #991b1b);
    color: white;
}

.euro-ball {
    background: linear-gradient(135deg, #f59e0b, #b45309);
    color: white;
}

.warning-box {
    background: rgba(127, 29, 29, .35);
    border: 1px solid #ef4444;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# إعدادات اللعبة
# =========================================================

st.sidebar.title("🎱 LOTTO HISTORY ANALYZER")

game_type = st.sidebar.radio(
    "اختر اللعبة:",
    ["Lotto 6aus49", "Eurojackpot"]
)

is_euro = game_type == "Eurojackpot"

st.sidebar.markdown("---")

uploaded_files = st.sidebar.file_uploader(
    "ارفع ملفات CSV أو Excel",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "القسم:",
    [
        "البحث حسب اليوم والشهر",
        "كل السحوبات",
        "توليد اقتراحات",
        "فحص الملف"
    ]
)

# =========================================================
# قراءة الملفات
# =========================================================

def read_uploaded_files(files):
    """
    يقرأ كل ملفات CSV وExcel وكل أوراق Excel.
    لا يوجد حد لعدد الصفوف أو السحوبات.
    """

    all_rows = []
    file_information = []

    if not files:
        return pd.DataFrame(), file_information

    for uploaded_file in files:
        filename = uploaded_file.name.lower()

        try:
            if filename.endswith(".csv"):
                uploaded_file.seek(0)

                try:
                    dataframe = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="utf-8",
                        sep=None,
                        engine="python",
                        on_bad_lines="skip"
                    )
                except UnicodeDecodeError:
                    uploaded_file.seek(0)

                    dataframe = pd.read_csv(
                        uploaded_file,
                        header=None,
                        encoding="latin-1",
                        sep=None,
                        engine="python",
                        on_bad_lines="skip"
                    )

                before = len(all_rows)

                for _, row in dataframe.iterrows():
                    all_rows.append({
                        "source_file": uploaded_file.name,
                        "source_sheet": "",
                        "values": row.tolist()
                    })

                file_information.append({
                    "الملف": uploaded_file.name,
                    "النوع": "CSV",
                    "الأوراق": 1,
                    "عدد الصفوف": len(all_rows) - before
                })

            elif filename.endswith(".xlsx") or filename.endswith(".xls"):
                excel_file = pd.ExcelFile(uploaded_file)
                before = len(all_rows)

                for sheet_name in excel_file.sheet_names:
                    dataframe = pd.read_excel(
                        uploaded_file,
                        sheet_name=sheet_name,
                        header=None
                    )

                    for _, row in dataframe.iterrows():
                        all_rows.append({
                            "source_file": uploaded_file.name,
                            "source_sheet": sheet_name,
                            "values": row.tolist()
                        })

                file_information.append({
                    "الملف": uploaded_file.name,
                    "النوع": "Excel",
                    "الأوراق": len(excel_file.sheet_names),
                    "عدد الصفوف": len(all_rows) - before
                })

        except Exception as error:
            st.error(
                f"تعذر قراءة الملف {uploaded_file.name}: {error}"
            )

    if not all_rows:
        return pd.DataFrame(), file_information

    return pd.DataFrame(all_rows), file_information


raw_df, file_information = read_uploaded_files(uploaded_files)

# =========================================================
# تحويل القيم إلى تاريخ
# =========================================================

def parse_date(value):
    if pd.isna(value):
        return None

    if isinstance(value, (dt.date, dt.datetime, pd.Timestamp)):
        return pd.Timestamp(value).date()

    text = str(value).strip()

    if not text:
        return None

    # تاريخ Excel، مثل 45200
    try:
        numeric = float(text)

        if 30000 <= numeric <= 60000:
            excel_date = (
                pd.Timestamp("1899-12-30")
                + pd.to_timedelta(numeric, unit="D")
            )

            return excel_date.date()

    except Exception:
        pass

    # الأرقام العادية ليست تواريخ
    if text.isdigit():
        return None

    # يدعم 05.09.2020 و05/09/2020 و2020-09-05
    parsed = pd.to_datetime(
        text,
        errors="coerce",
        dayfirst=True
    )

    if pd.notna(parsed):
        return parsed.date()

    return None


# =========================================================
# تحويل القيم إلى أرقام
# =========================================================

def parse_number(value):
    if pd.isna(value):
        return None

    try:
        text = str(value).strip()
        text = text.replace(",", ".")

        number = float(text)

        if number.is_integer():
            return int(number)

    except Exception:
        return None

    return None


# =========================================================
# استخراج السحب من صف
# =========================================================

def extract_draw(row_values, euro_game):
    found_date = None
    numbers = []

    for value in row_values:
        date_value = parse_date(value)

        if date_value is not None:
            found_date = date_value
            continue

        number = parse_number(value)

        if number is not None:
            numbers.append(number)

    if found_date is None:
        return None

    # حذف التكرارات، مع المحافظة على الترتيب
    unique_numbers = []

    for number in numbers:
        if number not in unique_numbers:
            unique_numbers.append(number)

    if euro_game:
        """
        Eurojackpot:
        5 أرقام رئيسية من 1 إلى 50
        رقمان إضافيان من 1 إلى 12
        نأخذ آخر 7 أرقام من الصف
        """

        possible_numbers = [
            number for number in unique_numbers
            if 1 <= number <= 50
        ]

        if len(possible_numbers) < 7:
            return None

        last_seven = possible_numbers[-7:]

        main_numbers = last_seven[:5]
        euro_numbers = last_seven[5:]

        if len(euro_numbers) != 2:
            return None

        if not all(1 <= number <= 12 for number in euro_numbers):
            return None

        return {
            "date": found_date,
            "main": sorted(main_numbers),
            "extra": sorted(euro_numbers)
        }

    else:
        """
        Lotto 6aus49:
        6 أرقام رئيسية من 1 إلى 49
        رقم Superzahl من 0 إلى 9
        """

        possible_numbers = [
            number for number in unique_numbers
            if 1 <= number <= 49
        ]

        if len(possible_numbers) < 6:
            return None

        main_numbers = possible_numbers[-6:]

        # نبحث عن Superzahl في آخر أرقام الصف
        super_candidates = [
            number for number in unique_numbers
            if 0 <= number <= 9
        ]

        super_number = (
            super_candidates[-1]
            if super_candidates
            else 0
        )

        return {
            "date": found_date,
            "main": sorted(main_numbers),
            "extra": super_number
        }


# =========================================================
# تحويل كل الصفوف إلى سحوبات
# =========================================================

def extract_all_draws(dataframe, euro_game):
    draws = []
    invalid_rows = []

    if dataframe.empty:
        return draws, invalid_rows

    for index, row in dataframe.iterrows():
        values = row["values"]

        draw = extract_draw(
            values,
            euro_game=euro_game
        )

        if draw is None:
            invalid_rows.append({
                "رقم الصف": index + 1,
                "الملف": row["source_file"],
                "الورقة": row["source_sheet"],
                "محتوى الصف": " | ".join(
                    str(value)
                    for value in values
                    if not pd.isna(value)
                )
            })
        else:
            draw["file"] = row["source_file"]
            draw["sheet"] = row["source_sheet"]
            draws.append(draw)

    # إزالة السحوبات المكررة
    clean_draws = []
    seen = set()

    for draw in draws:
        if isinstance(draw["extra"], list):
            extra_key = tuple(draw["extra"])
        else:
            extra_key = draw["extra"]

        key = (
            draw["date"],
            tuple(draw["main"]),
            extra_key
        )

        if key not in seen:
            seen.add(key)
            clean_draws.append(draw)

    clean_draws.sort(
        key=lambda draw: draw["date"],
        reverse=True
    )

    return clean_draws, invalid_rows


draws, invalid_rows = extract_all_draws(
    raw_df,
    euro_game=is_euro
)

# =========================================================
# عرض الكرات
# =========================================================

def render_balls(main_numbers, extra, euro_game):
    html = "<div class='ball-row'>"

    for number in main_numbers:
        html += (
            f"<div class='ball main-ball'>{number}</div>"
        )

    if euro_game:
        for number in extra:
            html += (
                f"<div class='ball euro-ball'>{number}</div>"
            )
    else:
        html += (
            f"<div class='ball super-ball'>{extra}</div>"
        )

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def render_draw(draw):
    st.markdown(
        f"""
        <div class="card">
            <b>📅 {draw["date"].strftime("%d.%m.%Y")}</b>
            <br>
            <small>
                الملف: {draw["file"]}
                {(" | الورقة: " + draw["sheet"])
                if draw["sheet"] else ""}
            </small>
        """,
        unsafe_allow_html=True
    )

    render_balls(
        draw["main"],
        draw["extra"],
        euro_game=is_euro
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# تحليل السحوبات
# =========================================================

def get_matching_draws(day, month):
    return [
        draw for draw in draws
        if draw["date"].day == day
        and draw["date"].month == month
    ]


def create_prediction(matching_draws, euro_game):
    if not matching_draws:
        return None

    main_frequency = Counter()

    for draw in matching_draws:
        main_frequency.update(draw["main"])

    if euro_game:
        extra_frequency = Counter()

        for draw in matching_draws:
            extra_frequency.update(draw["extra"])

        ranked_main = sorted(
            range(1, 51),
            key=lambda number: (
                main_frequency[number],
                random.random()
            ),
            reverse=True
        )

        ranked_extra = sorted(
            range(1, 13),
            key=lambda number: (
                extra_frequency[number],
                random.random()
            ),
            reverse=True
        )

        return {
            "main": sorted(ranked_main[:5]),
            "extra": sorted(ranked_extra[:2]),
            "main_frequency": main_frequency,
            "extra_frequency": extra_frequency
        }

    extra_frequency = Counter()

    for draw in matching_draws:
        extra_frequency.update([draw["extra"]])

    ranked_main = sorted(
        range(1, 50),
        key=lambda number: (
            main_frequency[number],
            random.random()
        ),
        reverse=True
    )

    ranked_extra = sorted(
        range(0, 10),
        key=lambda number: (
            extra_frequency[number],
            random.random()
        ),
        reverse=True
    )

    return {
        "main": sorted(ranked_main[:6]),
        "extra": ranked_extra[0],
        "main_frequency": main_frequency,
        "extra_frequency": extra_frequency
    }


# =========================================================
# واجهة التطبيق
# =========================================================

st.title("🎱 LOTTO HISTORY ANALYZER")
st.write(
    "ارفع جميع ملفات السحوبات، ثم اختر اليوم والشهر "
    "لتحليل كل السنوات المطابقة."
)

if not uploaded_files:
    st.info(
        "ابدأ برفع ملفات CSV أو Excel من القائمة الجانبية."
    )
else:
    st.success(
        f"تم تحميل {len(uploaded_files)} ملف، "
        f"وتم التعرف على {len(draws)} سحب."
    )

# =========================================================
# قسم البحث حسب اليوم والشهر
# =========================================================

if page == "البحث حسب اليوم والشهر":

    st.header("🔎 البحث في جميع السنوات")

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

    matching_draws = get_matching_draws(
        selected_day,
        selected_month
    )

    st.subheader(
        f"السحوبات بتاريخ "
        f"{selected_day:02d}.{selected_month:02d}"
    )

    if not matching_draws:
        st.warning(
            "لم يتم العثور على سحوبات بهذا اليوم والشهر."
        )

        st.write("عدد الصفوف المقروءة:", len(raw_df))
        st.write("عدد السحوبات المفهومة:", len(draws))

    else:
        st.success(
            f"تم العثور على {len(matching_draws)} سحب "
            "من جميع السنوات."
        )

        # عرض كل السحوبات بدون head أو حد أقصى
        for draw in matching_draws:
            render_draw(draw)

        st.header("📊 تحليل كل السحوبات المطابقة")

        prediction = create_prediction(
            matching_draws,
            euro_game=is_euro
        )

        if prediction:
            st.markdown(
                "<div class='card'>"
                "<h3>🌟 التوقع الإحصائي</h3>",
                unsafe_allow_html=True
            )

            render_balls(
                prediction["main"],
                prediction["extra"],
                euro_game=is_euro
            )

            st.info(
                "هذا اقتراح إحصائي مبني على تكرار الأرقام "
                "في السحوبات المطابقة، وليس نتيجة مضمونة."
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.subheader("🔢 تكرار الأرقام الرئيسية")

            frequency_data = []

            for number, count in prediction[
                "main_frequency"
            ].most_common():

                frequency_data.append({
                    "الرقم": number,
                    "مرات الظهور": count
                })

            st.dataframe(
                pd.DataFrame(frequency_data),
                use_container_width=True,
                hide_index=True
            )

            st.subheader("🎯 تكرار الأرقام الإضافية")

            extra_data = []

            for number, count in prediction[
                "extra_frequency"
            ].most_common():

                extra_data.append({
                    "الرقم الإضافي": number,
                    "مرات الظهور": count
                })

            st.dataframe(
                pd.DataFrame(extra_data),
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# قسم كل السحوبات
# =========================================================

elif page == "كل السحوبات":

    st.header("📚 كل السحوبات الموجودة في الملفات")

    if not draws:
        st.warning("لم يتم التعرف على أي سحب.")
    else:
        # بدون تحديد عدد، يعرض كل السجلات
        for draw in draws:
            render_draw(draw)


# =========================================================
# قسم توليد الاقتراحات
# =========================================================

elif page == "توليد اقتراحات":

    st.header("🎲 توليد اقتراحات")

    col1, col2 = st.columns(2)

    with col1:
        selected_day = st.number_input(
            "اليوم",
            min_value=1,
            max_value=31,
            value=5,
            key="prediction_day"
        )

    with col2:
        selected_month = st.number_input(
            "الشهر",
            min_value=1,
            max_value=12,
            value=9,
            key="prediction_month"
        )

    matching_draws = get_matching_draws(
        selected_day,
        selected_month
    )

    if not matching_draws:
        st.warning(
            "لا توجد سحوبات بنفس اليوم والشهر."
        )
    else:
        st.write(
            f"سيتم التحليل اعتماداً على "
            f"{len(matching_draws)} سحب."
        )

        if st.button("🚀 توليد الاقتراح"):

            prediction = create_prediction(
                matching_draws,
                euro_game=is_euro
            )

            st.markdown(
                "<div class='card'>"
                "<h3>التشكيلة المقترحة</h3>",
                unsafe_allow_html=True
            )

            render_balls(
                prediction["main"],
                prediction["extra"],
                euro_game=is_euro
            )

            st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# قسم فحص الملف
# =========================================================

elif page == "فحص الملف":

    st.header("🧪 فحص الملفات")

    if not uploaded_files:
        st.info("ارفع الملفات أولاً.")
    else:
        st.subheader("معلومات الملفات")

        if file_information:
            st.dataframe(
                pd.DataFrame(file_information),
                use_container_width=True,
                hide_index=True
            )

        st.subheader("إحصائيات القراءة")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "الملفات",
                len(uploaded_files)
            )

        with col2:
            st.metric(
                "الصفوف المقروءة",
                len(raw_df)
            )

        with col3:
            st.metric(
                "السحوبات المفهومة",
                len(draws)
            )

        st.subheader("السحوبات المفهومة")

        if draws:
            preview_rows = []

            for draw in draws:
                preview_rows.append({
                    "التاريخ": draw["date"].strftime("%d.%m.%Y"),
                    "الأرقام": ", ".join(
                        map(str, draw["main"])
                    ),
                    "الإضافي": (
                        ", ".join(map(str, draw["extra"]))
                        if isinstance(draw["extra"], list)
                        else draw["extra"]
                    ),
                    "الملف": draw["file"],
                    "الورقة": draw["sheet"]
                })

            st.dataframe(
                pd.DataFrame(preview_rows),
                use_container_width=True,
                hide_index=True
            )

        st.subheader("الصفوف التي لم يتم فهمها")

        if invalid_rows:
            st.warning(
                f"يوجد {len(invalid_rows)} صف لم يتم تحويله إلى سحب."
            )

            st.dataframe(
                pd.DataFrame(invalid_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success(
                "تم فهم جميع الصفوف الموجودة في الملفات."
            )
