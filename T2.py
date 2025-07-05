import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import requests

def download_file(url, progress_callback, status_callback):
    dest_folder = "downloads"
    os.makedirs(dest_folder, exist_ok=True)
    local_filename = url.split("/")[-1]
    filepath = os.path.join(dest_folder, local_filename)

    resume_header = {}
    mode = "wb"

    if os.path.exists(filepath):
        downloaded_bytes = os.path.getsize(filepath)
        resume_header = {"Range": f"bytes={downloaded_bytes}-"}
        mode = "ab"
    else:
        downloaded_bytes = 0

    try:
        with requests.get(url, stream=True, headers=resume_header) as r:
            if r.status_code in (200, 206):
                total_size = int(r.headers.get("Content-Length", 0)) + downloaded_bytes
                downloaded = downloaded_bytes

                with open(filepath, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = downloaded / total_size * 100
                            progress_callback(percent)
                status_callback("✅ دانلود کامل شد.")
            else:
                status_callback(f"❌ خطا: HTTP {r.status_code}")
    except Exception as e:
        status_callback(f"❌ خطا: {str(e)}")

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("خطا", "لینک را وارد کنید.")
        return

    download_button.config(state="disabled")
    status_label.config(text="⏳ در حال دانلود...")

    def run():
        download_file(url, update_progress, update_status)
        download_button.config(state="normal")

    threading.Thread(target=run).start()

def update_progress(percent):
    progress_bar["value"] = percent

def update_status(message):
    status_label.config(text=message)

# رابط گرافیکی
root = tk.Tk()
root.title("Simple IDM by Python")
root.geometry("400x200")

tk.Label(root, text="لینک دانلود:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="شروع دانلود", command=start_download)
download_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
