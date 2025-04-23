import os
import yt_dlp
import ffmpeg
from tkinter import Tk, Label, Text, Scrollbar, messagebox
from tkinter import Button as TkButton
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import threading

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
BTN_BG = "#333333"
BTN_FG = "#ffffff"
ENTRY_BG = "#2d2d2d"
BTN_HOVER_BG = "#555555"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

def select_videos():
    return askopenfilenames(title="Select videos", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])

def create_file_list(files, urls, list_file="file_list.txt", save_dir=None):
    save_dir = save_dir or os.getcwd()
    with open(list_file, "w") as f:
        for path in files:
            f.write(f"file '{path}'\n")
        for url in urls:
            downloaded = download_video(url, save_dir)
            if downloaded:
                f.write(f"file '{downloaded}'\n")

def download_video(url, save_dir):
    try:
        video_dir = os.path.join(save_dir, 'videos')
        os.makedirs(video_dir, exist_ok=True)

        opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(video_dir, '%(id)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception:
        return None

def concat_videos(file_list="file_list.txt", output_dir="output"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        out_file = get_unique_filename(output_dir)
        ffmpeg.input(file_list, format='concat', safe=0).output(out_file, c='copy').run()
    except ffmpeg.Error as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e.stderr.decode()}")

def get_unique_filename(output_dir):
    i = 1
    while True:
        path = os.path.join(output_dir, f"output{i}.mp4")
        if not os.path.exists(path):
            return path
        i += 1

def make_button(master, text, command):
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Dark.TButton",
                    background=BTN_BG,
                    foreground=BTN_FG,
                    borderwidth=0,
                    font=('Segoe UI', 14),  
                    padding=15) 
    style.map("Dark.TButton",
              background=[('active', BTN_HOVER_BG)],
              foreground=[('active', FG_COLOR)])
    return ttk.Button(master, text=text, command=command, style="Dark.TButton")

def enter_urls():
    win = Tk()
    win.title("Enter Video URLs")
    win.configure(bg=BG_COLOR)
    win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    Label(win, text="Enter URLs (one per line):", bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 14)).pack(pady=(20, 0))

    url_box = Text(win, height=10, width=50, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, bd=0, font=('Segoe UI', 12))
    url_box.pack(pady=20)

    scroll = Scrollbar(win, command=url_box.yview)
    scroll.pack(side='right', fill='y')
    url_box.config(yscrollcommand=scroll.set)

    def submit():
        urls = url_box.get("1.0", "end-1c").splitlines()
        win.destroy()
        if urls:
            threading.Thread(target=process_urls, args=(urls,)).start()
        else:
            messagebox.showwarning("No URLs", "You didn't enter any URLs.")

    make_button(win, "Download & Merge", submit).pack(pady=(0, 20))

    win.mainloop()

def process_urls(urls):
    create_file_list([], urls)
    concat_videos()

def select_videos_action():
    vids = select_videos()
    create_file_list(vids, []) 
    concat_videos()

def main_menu():
    win = Tk()
    win.title("Video Joiner")
    win.configure(bg=BG_COLOR)
    
    win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    Label(win, text="Choose an option:", bg=BG_COLOR, fg=FG_COLOR, font=('Segoe UI', 16)).pack(pady=30)

    make_button(win, "Pick videos from PC", select_videos_action).pack(pady=15)
    make_button(win, "Download videos from URLs", enter_urls).pack(pady=15)

    win.mainloop()

if __name__ == "__main__":
    main_menu()
