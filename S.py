import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os

# مسیر پیش‌فرض برای ذخیره فایل‌ها
download_directory = os.path.abspath("downloads")

# کلاس مدیریت دانلود یک فایل
class DownloadItem:
    def __init__(self, url, frame, row):
        self.url = url
        self.local_filename = url.split("/")[-1]
        self.filepath = os.path.join(download_directory, self.local_filename)
        self.is_paused = False
        self.is_downloading = False
        self.thread = None

        # رابط گرافیکی
        self.label = tk.Label(frame, text=self.local_filename[:40] + "...")
        self.progress = ttk.Progressbar(frame, length=250, mode="determinate")
        self.status = tk.Label(frame, text="در انتظار")
        self.button = tk.Button(frame, text="⏸ Pause", command=self.toggle_pause)

        self.label.grid(row=row, column=0, sticky="w")
        self.progress.grid(row=row, column=1, padx=5)
        self.status.grid(row=row, column=2)
        self.button.grid(row=row, column=3)

    def toggle_pause(self):
        if not self.is_downloading:
            return
        self.is_paused = not self.is_paused
        self.button.config(text="▶️ Resume" if self.is_paused else "⏸ Pause")
        self.status.config(text="⏸ متوقف شده" if self.is_paused else "⬇️ ادامه دانلود")

    def update_progress(self, percent):
        self.progress["value"] = percent

    def update_status(self, text):
        self.status.config(text=text)

    def start(self):
        self.thread = threading.Thread(target=self.download)
        self.thread.start()

    def download(self):
        global download_directory
        os.makedirs(download_directory, exist_ok=True)
        self.filepath = os.path.join(download_directory, self.local_filename)

        resume_header = {}
        mode = "wb"

        if os.path.exists(self.filepath):
            downloaded_bytes = os.path.getsize(self.filepath)
            resume_header = {"Range": f"bytes={downloaded_bytes}-"}
            mode = "ab"
        else:
            downloaded_bytes = 0

        try:
            with requests.get(self.url, stream=True, headers=resume_header) as r:
                if r.status_code not in (200, 206):
                    self.update_status(f"❌ HTTP {r.status_code}")
                    return

                total_size = int(r.headers.get("Content-Length", 0)) + downloaded_bytes
                downloaded = downloaded_bytes
                self.is_downloading = True

                with open(self.filepath, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        while self.is_paused:
                            if not self.is_downloading:
                                return
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = downloaded / total_size * 100
                            self.update_progress(percent)
                self.update_status("✅ کامل شد")
            self.is_downloading = False
        except Exception as e:
            self.update_status(f"❌ خطا: {str(e)}")
            self.is_downloading = False

# رابط گرافیکی
root = tk.Tk()
root.title("Python IDM - دانلود منیجر ساده")
root.geometry("850x550")

# مسیر انتخاب پوشه ذخیره‌سازی
def choose_download_folder():
    global download_directory
    path = filedialog.askdirectory()
    if path:
        download_directory = path
        folder_label.config(text=f"📁 ذخیره در: {download_directory}")

# نوار بالا: ورود لینک و دکمه‌ها
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="لینک دانلود:").pack(side="left")
url_entry = tk.Entry(top_frame, width=60)
url_entry.pack(side="left", padx=5)

def add_to_queue():
    url = url_entry.get()
    if not url:
        messagebox.showerror("خطا", "لینک را وارد کنید.")
        return
    row = len(download_items)
    item = DownloadItem(url, list_frame, row)
    download_items.append(item)
    url_entry.delete(0, tk.END)

def start_all_downloads():
    for item in download_items:
        if not item.is_downloading:
            item.start()

tk.Button(top_frame, text="➕ افزودن به صف", command=add_to_queue).pack(side="left", padx=5)
tk.Button(root, text="▶️ شروع همه دانلودها", command=start_all_downloads).pack(pady=10)

# مسیر انتخاب پوشه
folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)

tk.Button(folder_frame, text="📂 انتخاب پوشه ذخیره‌سازی", command=choose_download_folder).pack(side="left")
folder_label = tk.Label(folder_frame, text=f"📁 ذخیره در: {download_directory}")
folder_label.pack(side="left", padx=10)

# فریم لیست دانلود
list_frame = tk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=10, pady=10)

# لیست دانلودها
download_items = []

# شروع رابط
root.mainloop()
