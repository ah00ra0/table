import customtkinter as ctk
import threading
import requests
import os

# تنظیم حالت تاریک و تم
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

download_directory = os.path.abspath("downloads")

class DownloadItem(ctk.CTkFrame):
    def __init__(self, master, url, **kwargs):
        super().__init__(master, corner_radius=15, **kwargs)
        self.url = url
        self.local_filename = url.split("/")[-1]
        self.filepath = os.path.join(download_directory, self.local_filename)
        self.is_paused = False
        self.is_downloading = False
        self.thread = None

        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text=self.local_filename[:40]+"...", width=200)
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.status = ctk.CTkLabel(self, text="در انتظار", width=100)
        self.button = ctk.CTkButton(self, text="⏸ Pause", width=80, command=self.toggle_pause, corner_radius=10)

        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.progress.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.status.grid(row=0, column=2, padx=10, pady=10)
        self.button.grid(row=0, column=3, padx=10, pady=10)

    def toggle_pause(self):
        if not self.is_downloading:
            return
        self.is_paused = not self.is_paused
        self.button.configure(text="▶️ Resume" if self.is_paused else "⏸ Pause")
        self.status.configure(text="⏸ متوقف شده" if self.is_paused else "⬇️ ادامه دانلود")

    def update_progress(self, percent):
        self.progress.set(percent / 100)

    def update_status(self, text):
        self.status.configure(text=text)

    def start(self):
        self.thread = threading.Thread(target=self.download)
        self.thread.start()

    def download(self):
        os.makedirs(download_directory, exist_ok=True)
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

class IDMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python IDM - دانلود منیجر")
        self.geometry("900x600")
        self.minsize(700, 400)

        self.download_items = []

        # ورودی لینک و دکمه ها
        self.top_frame = ctk.CTkFrame(self, corner_radius=15)
        self.top_frame.pack(padx=20, pady=15, fill="x")

        self.url_entry = ctk.CTkEntry(self.top_frame, placeholder_text="لینک دانلود را وارد کنید...", corner_radius=10)
        self.url_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.add_button = ctk.CTkButton(self.top_frame, text="➕ افزودن به صف", command=self.add_to_queue, corner_radius=10)
        self.add_button.pack(side="left", padx=10)

        self.start_button = ctk.CTkButton(self, text="▶️ شروع همه دانلودها", command=self.start_all_downloads, corner_radius=10)
        self.start_button.pack(pady=10, padx=20, fill="x")

        # انتخاب پوشه ذخیره سازی
        self.folder_frame = ctk.CTkFrame(self, corner_radius=15)
        self.folder_frame.pack(padx=20, pady=5, fill="x")

        self.folder_button = ctk.CTkButton(self.folder_frame, text="📂 انتخاب پوشه ذخیره", command=self.choose_download_folder, corner_radius=10)
        self.folder_button.pack(side="left", padx=10, pady=10)

        self.folder_label = ctk.CTkLabel(self.folder_frame, text=f"📁 ذخیره در: {download_directory}")
        self.folder_label.pack(side="left", padx=10)

        # فریم لیست دانلود
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.list_frame.pack(padx=20, pady=15, fill="both", expand=True)

    def choose_download_folder(self):
        from tkinter import filedialog
        global download_directory
        path = filedialog.askdirectory()
        if path:
            download_directory = path
            self.folder_label.configure(text=f"📁 ذخیره در: {download_directory}")

    def add_to_queue(self):
        url = self.url_entry.get()
        if not url:
            ctk.CTkMessageBox(title="خطا", message="لینک را وارد کنید.")
            return
        item = DownloadItem(self.list_frame, url)
        item.pack(pady=5, fill="x", padx=10)
        self.download_items.append(item)
        self.url_entry.delete(0, "end")

    def start_all_downloads(self):
        for item in self.download_items:
            if not item.is_downloading:
                item.start()

if __name__ == "__main__":
    app = IDMApp()
    app.mainloop()
