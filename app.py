import pandas as pd
import datetime as dt
import random
from collections import Counter


# =========================================================
# تحويل أي قيمة إلى تاريخ
# =========================================================

def get_date_from_value(value):
    if pd.isna(value):
        return None

    # تاريخ جاهز من Excel أو pandas
    if isinstance(value, (dt.datetime, dt.date, pd.Timestamp)):
        return pd.Timestamp(value).date()

    text = str(value).strip()

    if not text:
        return None

    # معالجة تاريخ Excel الرقمي
    # أرقام Excel للتاريخ غالباً تكون بين 30000 و60000
    try:
        numeric_value = float(text)

        if 30000 <= numeric_value <= 60000:
            excel_date = pd.Timestamp(
                "1899-12-30"
            ) + pd.to_timedelta(
                numeric_value,
                unit="D"
            )

            return excel_date.date()
    except Exception:
        pass

    # منع اعتبار الرقم العادي تاريخاً
    if text.isdigit():
        return None

    # معالجة صيغ التاريخ المختلفة
    parsed = pd.to_datetime(
        text,
        errors="coerce",
        dayfirst=True
    )

    if pd.notna(parsed):
        return parsed.date()

    return None


# =========================================================
# تحويل القيمة إلى رقم
# =========================================================

def get_number_from_value(value):
    if pd.isna(value):
        return None

    try:
        text = str(value).strip()
        number = float(text.replace(",", "."))

        if number.is_integer():
            return int(number)

    except Exception:
        return None

    return None


# =========================================================
# استخراج السحب من صف واحد
# =========================================================

def extract_draw_from_row(row_values, euro_game=False):
    date_value = None
    numbers = []

    for value in row_values:
        found_date = get_date_from_value(value)

        if found_date is not None:
            date_value = found_date
            continue

        number = get_number_from_value(value)

        if number is not None:
            numbers.append(number)

    if date_value is None:
        return None

    # إزالة القيم غير المفيدة في بداية الصف
    # ثم نأخذ آخر أرقام الصف لأنها غالباً أرقام السحب
    if euro_game:
        # Eurojackpot يحتاج 5 أرقام رئيسية + 2 Euro
        valid_numbers = [
            n for n in numbers
            if 1 <= n <= 50
        ]

        if len(valid_numbers) < 7:
            return None

        last_seven = valid_numbers[-7:]

        main_numbers = last_seven[:5]
        euro_numbers = last_seven[5:]

        # التأكد أن أرقام Euro صحيحة
        if not all(1 <= n <= 12 for n in euro_numbers):
            # محاولة بديلة من كل الأرقام
            possible_euro = [
                n for n in numbers
                if 1 <= n <= 12
            ]

            if len(possible_euro) >= 2:
                euro_numbers = possible_euro[-2:]

        if len(main_numbers) != 5 or len(euro_numbers) != 2:
            return None

        return {
            "date": date_value,
            "main": sorted(main_numbers),
            "extra": sorted(euro_numbers)
        }

    else:
        # Lotto 6aus49 يحتاج 6 أرقام + Superzahl
        valid_main = [
            n for n in numbers
            if 1 <= n <= 49
        ]

        if len(valid_main) < 6:
            return None

        # آخر 6 أرقام تعتبر أرقام السحب الرئيسية
        main_numbers = valid_main[-6:]

        # نبحث عن Superzahl بعد أرقام السحب
        super_number = None

        if numbers:
            possible_super = [
                n for n in numbers
                if 0 <= n <= 9
            ]

            if possible_super:
                super_number = possible_super[-1]

        if super_number is None:
            super_number = 0

        return {
            "date": date_value,
            "main": sorted(main_numbers),
            "extra": super_number
        }


# =========================================================
# قراءة كل الملفات وكل أوراق Excel
# =========================================================

@st.cache_data(show_spinner=False)
def read_all_uploaded_files(uploaded_files):
    all_rows = []

    if not uploaded_files:
        return pd.DataFrame()

    for uploaded_file in uploaded_files:
        try:
            filename = uploaded_file.name.lower()

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

                for _, row in dataframe.iterrows():
                    all_rows.append(row.tolist())

            else:
                excel_file = pd.ExcelFile(uploaded_file)

                for sheet_name in excel_file.sheet_names:
                    dataframe = pd.read_excel(
                        uploaded_file,
                        sheet_name=sheet_name,
                        header=None
                    )

                    for _, row in dataframe.iterrows():
                        all_rows.append(row.tolist())

        except Exception as error:
            st.error(
                f"خطأ في قراءة الملف {uploaded_file.name}: {error}"
            )

    if not all_rows:
        return pd.DataFrame()

    return pd.DataFrame(all_rows)


# =========================================================
# تحويل البيانات إلى سحوبات مفهومة
# =========================================================

def build_draws(dataframe, euro_game=False):
    draws = []

    if dataframe.empty:
        return draws

    for _, row in dataframe.iterrows():
        draw = extract_draw_from_row(
            row.tolist(),
            euro_game=euro_game
        )

        if draw is not None:
            draws.append(draw)

    # إزالة التكرار
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

    return sorted(
        clean_draws,
        key=lambda item: item["date"],
        reverse=True
    )


# =========================================================
# السحوبات بنفس اليوم والشهر
# =========================================================

def find_same_day_month(draws, selected_day, selected_month):
    return [
        draw for draw in draws
        if draw["date"].day == selected_day
        and draw["date"].month == selected_month
    ]


# =========================================================
# تحليل السحوبات المطابقة
# =========================================================

def analyze_matching_draws(matching_draws, euro_game=False):
    if not matching_draws:
        return None

    main_counter = Counter()

    for draw in matching_draws:
        main_counter.update(draw["main"])

    if euro_game:
        extra_counter = Counter()

        for draw in matching_draws:
            extra_counter.update(draw["extra"])

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

        prediction = {
            "main": sorted(ranked_main[:5]),
            "extra": sorted(ranked_extra[:2]),
            "main_frequency": main_counter,
            "extra_frequency": extra_counter
        }

    else:
        extra_counter = Counter()

        for draw in matching_draws:
            extra_counter.update([draw["extra"]])

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

        prediction = {
            "main": sorted(ranked_main[:6]),
            "extra": ranked_extra[0],
            "main_frequency": main_counter,
            "extra_frequency": extra_counter
        }

    return prediction
