import tkinter as tk
from tkinter import messagebox

# قائمة الملفات مع تحديد اليوم والشهر فقط (MM-DD)
files_data = [
    {"title": "Villa", "author": "Maya Alhamwi", "date": "05-12", "category": "عقارات"},
    {"title": "Steuererklärung", "author": "basel alhamed", "date": "03-10", "category": "ضرائب"},
    {"title": "فانتوم", "author": "basel alhamed", "date": "01-15", "category": "مستندات عامة"},
    {"title": "TrustWalletBackup", "author": "basel alhamed", "date": "11-20", "category": "أمان وتشفير"},
    {"title": "Finanzamt Dokumente", "author": "basel alhamed", "date": "04-02", "category": "الضرائب المالية"}
]

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج البحث حسب اليوم والشهر")
        self.root.geometry("550x450")
        self.root.config(bg="#f0f0f0")

        # عنوان البرنامج
        title_label = tk.Label(root, text="📅 البحث في الملفات حسب (اليوم والشهر)", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)

        # حقل البحث
        search_frame = tk.Frame(root, bg="#f0f0f0")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="أدخل الشهر أو اليوم (مثال: 03-10 أو 05):", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14), width=15)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_files)

        search_btn = tk.Button(search_frame, text="بحث", font=("Arial", 11), bg="#007ACC", fg="white", command=self.perform_search)
        search_btn.pack(side=tk.LEFT, padx=5)

        # قائمة النتائج
        self.listbox = tk.Listbox(root, font=("Arial", 12), width=60, height=12)
        self.listbox.pack(pady=15)
        self.listbox.bind("<Double-Button-1>", self.show_details)

        # عرض كافة الملفات عند البداية
        self.update_list(files_data)

    def update_list(self, data):
        self.listbox.delete(0, tk.END)
        for item in data:
            self.listbox.insert(tk.END, f"📅 (الشهر-اليوم) {item['date']}  |  📄 {item['title']}  |  {item['author']}")

    def filter_files(self, event):
        query = self.search_entry.get().strip().lower()
        filtered = [f for f in files_data if query in f['date'].lower() or query in f['title'].lower()]
        self.update_list(filtered)

    def perform_search(self):
        self.filter_files(None)

    def show_details(self, event):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            text = self.listbox.get(index)
            messagebox.showinfo("تفاصيل الملف", f"معلومات الملف المحدد:\n{text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
