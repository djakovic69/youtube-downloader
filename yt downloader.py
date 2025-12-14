import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Missing dependency: yt-dlp. Install with: pip install yt-dlp", file=sys.stderr)
    sys.exit(1)


def download_video(url: str, output_dir: Path, audio_only: bool = False):
    outtmpl = str(output_dir / '%(title)s [%(id)s].%(ext)s')

    if audio_only:
        format_selector = 'bestaudio[ext=m4a]/bestaudio/best'
        postprocessors = [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '0',
            }
        ]
    else:
        format_selector = (
            'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/'
            'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best'
        )
        postprocessors = [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }
        ]

    ydl_opts = {
        'outtmpl': outtmpl,
        'format': format_selector,
        'restrictfilenames': True,
        'merge_output_format': 'mp4' if not audio_only else None,
        'postprocessors': postprocessors,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {e}")


def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_path.set(folder)


def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input needed", "Please enter a YouTube URL.")
        return

    folder = Path(output_path.get()).expanduser().resolve()
    
    try:
        folder.mkdir(parents=True, exist_ok=True)  # sigurnije kreiranje foldera
    except PermissionError:
        messagebox.showerror(
            "Permission Error",
            f"Cannot create folder:\n{folder}\nPlease choose another location."
        )
        return

    audio_only = audio_var.get() == 1
    download_video(url, folder, audio_only)


# GUI setup
root = tk.Tk()
root.title("YT Downloader (legal-only)")
root.geometry("500x250")

url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

folder_frame = tk.Frame(root)
folder_frame.pack(pady=5)

# Default folder u korisnikovom Downloads/YT_videos
default_download_folder = Path.home() / "Downloads" / "YT_videos"
default_download_folder.mkdir(parents=True, exist_ok=True)
output_path = tk.StringVar(value=str(default_download_folder))

folder_entry = tk.Entry(folder_frame, textvariable=output_path, width=40)
folder_entry.pack(side=tk.LEFT, padx=5)

folder_button = tk.Button(folder_frame, text="Choose Folder", command=choose_folder)
folder_button.pack(side=tk.LEFT)

audio_var = tk.IntVar()
audio_checkbox = tk.Checkbutton(root, text="Audio only (M4A)", variable=audio_var)
audio_checkbox.pack(pady=5)

download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=10)

# Developer label
developer_label = tk.Label(root, text="developed by djakovicc", fg="gray")
developer_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
