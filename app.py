import pandas as pd
import glob
import os

def search_lotto_by_date(target_month_day):
    """
    بحث عن سحوبات اللوتو في ملفات Excel حسب الشهر واليوم (MM-DD)
    """
    # البحث عن ملفات اللوتو واستبعاد ملفات 2021 بناءً على طلبك السابق
    files = [f for f in glob.glob("LOTTO*.xlsx") if "2021" not in f]
    
    results = []
    
    for file in files:
        try:
            xls = pd.ExcelFile(file)
            for sheet in xls.sheet_names:
                # التحقق أن اسم ورقة العمل عبارة عن سنة ضمن النطاق المطلوب
                if sheet.isdigit() and 1955 <= int(sheet) <= 1964:
                    df = pd.read_excel(file, sheet_name=sheet)
                    for _, row in df.iterrows():
                        val = row.get('Unnamed: 1') # العمود الذي يحتوي على التاريخ
                        if pd.notna(val) and hasattr(val, 'year'):
                            date_obj = pd.to_datetime(val)
                            date_str = date_obj.strftime('%m-%d') # استخلاص الشهر واليوم فقط
                            full_date_str = date_obj.strftime('%Y-%m-%d')
                            
                            # مقارنة التاريخ المدخل مع تاريخ السحب
                            if target_month_day in date_str:
                                # جمع أرقام السحب الأساسية من الأعمدة المخصصة
                                nums = [str(int(row.get(f'Unnamed: i'))) for i in range(2, 8) if pd.notna(row.get(f'Unnamed: i'))]
                                zusatz = row.get('Unnamed: 8') # الرقم الإضافي
                                zusatz_str = f" | الرقم الإضافي: {int(zusatz)}" if pd.notna(zusatz) else ""
                                
                                results.append({
                                    "File": file,
                                    "Year": sheet,
                                    "Date": full_date_str,
                                    "Numbers": " - ".join(nums) + zusatz_str
                                })
        except Exception as e:
            print(f"خطأ في قراءة الملف {file}: {e}")
            
    return results

if __name__ == "__main__":
    print("--- نظام استعلام سحوبات اللوتو حسب التاريخ ---")
    # مثال للصيغة المطلوبة: الشهر-اليوم (مثل 05-12 أو 01-01)
    user_input = input("أدخل التاريخ بصيغة الشهر-اليوم (MM-DD): ").strip()
    
    found_draws = search_lotto_by_date(user_input)
    
    if found_draws:
        print(f"\nتم العثور على {len(found_draws)} سحب مطابق:")
        for idx, draw in enumerate(found_draws, 1):
            print(f"{idx}. التاريخ: {draw['Date']} | الأرقام: {draw['Numbers']} [ملف: {draw['File']} - ورقة: {draw['Year']}]")
    else:
        print("\n⚠️ لم يتم العثور على أي سحب بهذا التاريخ في الملفات المتاحة.")
