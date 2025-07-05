import customtkinter as ctk
import threading
import requests
import os
import time
import math
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

download_directory = os.path.abspath("downloads")
MAX_THREADS_PER_DOWNLOAD = 4

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Y{suffix}"

class DownloadWorker(threading.Thread):
    def __init__(self, url, start, end, filepath, parent_item, idx):
        super().__init__()
        self.url = url
        self.start = start
        self.end = end
        self.filepath = filepath
        self.parent_item = parent_item
        self.idx = idx
        self.daemon = True

    def run(self):
        headers = {"Range": f"bytes={self.start}-{self.end}"}
        try:
            with requests.get(self.url, headers=headers, stream=True, timeout=10) as r:
                if r.status_code not in (206, 200):
                    self.parent_item.update_status(f"\u274c HTTP {r.status_code} Error")
                    return
                with open(self.filepath, "r+b") as f:
                    f.seek(self.start)
                    for chunk in r.iter_content(chunk_size=8192):
                        while self.parent_item.is_paused or self.parent_item.is_cancelled:
                            if self.parent_item.is_cancelled:
                                return
                            time.sleep(0.1)
                        if chunk:
                            f.write(chunk)
                            self.parent_item.update_downloaded(len(chunk))
        except Exception as e:
            self.parent_item.update_status(f"\u274c Error: {str(e)}")
            self.parent_item.is_downloading = False

class DownloadItem(ctk.CTkFrame):
    def __init__(self, master, url, **kwargs):
        super().__init__(master, corner_radius=15, **kwargs)
        self.url = url
        self.local_filename = url.split("/")[-1].split("?")[0]
        self.filepath = os.path.join(download_directory, self.local_filename)
        self.filesize = 0
        self.downloaded_bytes = 0
        self.is_paused = False
        self.is_cancelled = False
        self.is_downloading = False
        self.workers = []
        self.start_time = None

        self.grid_columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text=self.local_filename[:40]+"...", width=250)
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.status = ctk.CTkLabel(self, text="در انتظار", width=150)
        self.speed_label = ctk.CTkLabel(self, text="سرعت: 0 KB/s", width=120)
        self.time_label = ctk.CTkLabel(self, text="زمان باقیمانده: --:--", width=160)
        self.pause_button = ctk.CTkButton(self, text="⏸ توقف", width=80, command=self.toggle_pause, corner_radius=10)
        self.cancel_button = ctk.CTkButton(self, text="❌ لغو", width=80, command=self.cancel, corner_radius=10)

        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.progress.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.status.grid(row=0, column=2, padx=10, pady=10)
        self.speed_label.grid(row=1, column=0, sticky="w", padx=10)
        self.time_label.grid(row=1, column=1, sticky="w", padx=10)
        self.pause_button.grid(row=1, column=2, padx=10)
        self.cancel_button.grid(row=1, column=3, padx=10)

    def toggle_pause(self):
        if not self.is_downloading:
            return
        self.is_paused = not self.is_paused
        self.pause_button.configure(text="▶️ ادامه" if self.is_paused else "⏸ توقف")
        self.update_status("⏸ متوقف شده" if self.is_paused else "⬇️ در حال دانلود")

    def cancel(self):
        if not self.is_downloading:
            return
        self.is_cancelled = True
        self.update_status("لغو شد")
        self.progress.set(0)
        self.speed_label.configure(text="سرعت: 0 KB/s")
        self.time_label.configure(text="زمان باقیمانده: --:--")
        self.pause_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")

    def update_progress(self, percent):
        self.progress.set(percent / 100)

    def update_status(self, text):
        self.status.configure(text=text)

    def update_downloaded(self, chunk_size):
        self.downloaded_bytes += chunk_size
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            speed = self.downloaded_bytes / elapsed
            speed_text = sizeof_fmt(speed) + "/s"
        else:
            speed = 0
            speed_text = "0 KB/s"

        self.speed_label.configure(text=f"سرعت: {speed_text}")

        if self.filesize > 0:
            percent = self.downloaded_bytes / self.filesize * 100
            self.update_progress(percent)

            remaining = self.filesize - self.downloaded_bytes
            if speed > 0:
                time_left = remaining / speed
                mins = int(time_left // 60)
                secs = int(time_left % 60)
                self.time_label.configure(text=f"زمان باقیمانده: {mins:02d}:{secs:02d}")
            else:
                self.time_label.configure(text="زمان باقیمانده: --:--")

        if self.downloaded_bytes >= self.filesize:
            self.update_status("✅ کامل شد")
            self.pause_button.configure(state="disabled")
            self.cancel_button.configure(state="disabled")
            self.is_downloading = False
            messagebox.showinfo("دانلود کامل شد", f"دانلود فایل '{self.local_filename}' به پایان رسید.")

    def start(self):
        threading.Thread(target=self.download, daemon=True).start()

    def download(self):
        os.makedirs(download_directory, exist_ok=True)
        self.is_paused = False
        self.is_cancelled = False
        self.is_downloading = True
        self.downloaded_bytes = 0
        self.start_time = time.time()

        try:
            r = requests.head(self.url, allow_redirects=True)
            self.filesize = int(r.headers.get("Content-Length", 0))
            accept_ranges = r.headers.get("Accept-Ranges", "none")
            if accept_ranges != "bytes" or self.filesize == 0:
                self.download_single_thread()
            else:
                self.download_multi_thread()
        except Exception as e:
            self.update_status(f"\u274c Error: {str(e)}")
            self.is_downloading = False

    def download_single_thread(self):
        try:
            with requests.get(self.url, stream=True) as r:
                if r.status_code != 200:
                    self.update_status(f"\u274c HTTP {r.status_code} Error")
                    return
                with open(self.filepath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        while self.is_paused or self.is_cancelled:
                            if self.is_cancelled:
                                return
                            time.sleep(0.1)
                        if chunk:
                            f.write(chunk)
                            self.update_downloaded(len(chunk))
            self.update_status("\u2705 کامل شد")
            self.is_downloading = False
        except Exception as e:
            self.update_status(f"\u274c Error: {str(e)}")
            self.is_downloading = False

    def download_multi_thread(self):
        with open(self.filepath, "wb") as f:
            f.truncate(self.filesize)

        part_size = math.ceil(self.filesize / MAX_THREADS_PER_DOWNLOAD)
        self.workers.clear()

        for i in range(MAX_THREADS_PER_DOWNLOAD):
            start = i * part_size
            end = min(start + part_size - 1, self.filesize - 1)
            worker = DownloadWorker(self.url, start, end, self.filepath, self, i)
            self.workers.append(worker)
            worker.start()

        for w in self.workers:
            w.join()

        if not self.is_cancelled:
            self.update_status("\u2705 کامل شد")
            self.is_downloading = False
            messagebox.showinfo("دانلود کامل شد", f"دانلود فایل '{self.local_filename}' به پایان رسید.")

class IDMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python IDM - دانلود منیجر")
        self.geometry("900x600")
        self.minsize(700, 400)

        self.download_items = []

        self.top_frame = ctk.CTkFrame(self, corner_radius=15)
        self.top_frame.pack(padx=20, pady=15, fill="x")

        self.url_entry = ctk.CTkEntry(self.top_frame, placeholder_text="لینک دانلود را وارد کنید...", corner_radius=10)
        self.url_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.add_button = ctk.CTkButton(self.top_frame, text="➕ افزودن به صف", command=self.add_to_queue, corner_radius=10)
        self.add_button.pack(side="left", padx=5)

        self.select_dir_button = ctk.CTkButton(self.top_frame, text="📁 انتخاب پوشه دانلود", command=self.select_folder, corner_radius=10)
        self.select_dir_button.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self, placeholder_text="جستجو در دانلودها...", corner_radius=10)
        self.search_entry.pack(padx=20, pady=10, fill="x")
        self.search_entry.bind("<KeyRelease>", self.filter_list)

        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.status_label = ctk.CTkLabel(self, text=f"پوشه دانلود: {download_directory}")
        self.status_label.pack(padx=20, pady=5)

    def select_folder(self):
        global download_directory
        folder = filedialog.askdirectory()
        if folder:
            download_directory = folder
            self.status_label.configure(text=f"پوشه دانلود: {download_directory}")

    def add_to_queue(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("هشدار", "لطفا لینک دانلود را وارد کنید.")
            return

        item = DownloadItem(self.list_frame, url)
        item.pack(fill="x", pady=5, padx=5)
        self.download_items.append(item)
        item.start()
        self.url_entry.delete(0, "end")

    def filter_list(self, event=None):
        term = self.search_entry.get().strip().lower()
        for item in self.download_items:
            name = item.local_filename.lower()
            if term in name:
                item.pack(fill="x", pady=5, padx=5)
            else:
                item.pack_forget()

if __name__ == "__main__":
    app = IDMApp()
    app.mainloop()
