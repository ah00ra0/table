import os
import requests

def download_file(url, dest_folder="downloads"):
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

    with requests.get(url, stream=True, headers=resume_header) as r:
        if r.status_code in (200, 206):
            total_size = int(r.headers.get("Content-Length", 0)) + downloaded_bytes
            print(f"Downloading: {local_filename} | Size: {total_size / 1024:.2f} KB")

            with open(filepath, mode) as f:
                downloaded = downloaded_bytes
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        done = int(50 * downloaded / total_size)
                        print(f"\r[{'█' * done}{'.' * (50 - done)}] {downloaded / 1024:.2f} KB", end="")
            print("\nDownload complete.")
        else:
            print("Failed to download. HTTP Status:", r.status_code)

# مثال:
download_file("https://speed.hetzner.de/100MB.bin")
