import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading
import re
from custom_ui import CustomFileList

def get_unique_filepath(directory, base_filename, ext):
    candidate = os.path.join(directory, f"{base_filename}{ext}")
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{base_filename}_{counter}{ext}")
        counter += 1
    return candidate

class IndividualApp:
    def __init__(self, root, debug=False, test_len=5):
        self.root = root
        self.debug = debug
        self.test_len = test_len
        self.root.title("Insta360 Individual Converter")
        
        self.files = []
        
        # 파일 선택 UI
        file_frame = tk.LabelFrame(root, text="입력 파일 (순차적으로 개별 변환됨)")
        file_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # self.listbox = tk.Listbox(file_frame, selectmode=tk.EXTENDED)
        self.listbox = CustomFileList(file_frame)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(side="right", fill="y", padx=5, pady=5)
        tk.Button(btn_frame, text="파일 추가", command=self.add_files, width=10).pack(pady=2)
        tk.Button(btn_frame, text="선택 삭제", command=self.remove_files, width=10).pack(pady=2)
        tk.Button(btn_frame, text="초기화", command=self.clear_files, width=10).pack(pady=2)
        
        # 출력 경로 UI
        out_frame = tk.LabelFrame(root, text="출력 경로")
        out_frame.pack(fill="x", padx=10, pady=5)
        
        self.same_path_var = tk.BooleanVar(value=True)
        tk.Checkbutton(out_frame, text="입력 경로와 같음", variable=self.same_path_var, command=self.toggle_out_path).pack(anchor="w")
        
        path_inner = tk.Frame(out_frame)
        path_inner.pack(fill="x", pady=2)
        self.out_path_var = tk.StringVar()
        self.entry_out = tk.Entry(path_inner, textvariable=self.out_path_var, state="disabled")
        self.entry_out.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_out = tk.Button(path_inner, text="경로 선택", command=self.browse_out, state="disabled")
        self.btn_out.pack(side="right")
        
        # 실행 버튼
        self.btn_run = tk.Button(root, text="Individual 실행", command=self.run, height=2, bg="lightgreen")
        self.btn_run.pack(fill="x", padx=10, pady=(10, 5))

        # 프로그래스 바 및 상태 표시창
        self.progress_frame = tk.Frame(root)
        self.progress_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", side="top", pady=2)
        
        self.status_label = tk.Label(self.progress_frame, text="대기 중...", anchor="w")
        self.status_label.pack(side="left", fill="x", expand=True)
        
        self.btn_log = tk.Button(self.progress_frame, text="로그 보기", command=self.show_log_window, state="disabled")
        self.btn_log.pack(side="right")
        
        self.log_window = None
        self.log_text = None
        self.full_log_history = ""

    def add_files(self):
        new_files = filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4 *.mov")])
        for f in new_files:
            if f not in self.files:
                self.files.append(f)
                self.listbox.insert(tk.END, f)

    def remove_files(self):
        for index in reversed(self.listbox.curselection()):
            self.listbox.delete(index)
            del self.files[index]

    def clear_files(self):
        self.listbox.delete(0, tk.END)
        self.files.clear()

    def show_log_window(self):
        if self.log_window and tk.Toplevel.winfo_exists(self.log_window):
            self.log_window.lift()
            return
        
        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("FFmpeg 진행 로그")
        self.log_window.geometry("800x400")
        
        self.log_text = tk.Text(self.log_window, bg="black", fg="white", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, side="left")
        
        scrollbar = tk.Scrollbar(self.log_window, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.insert(tk.END, self.full_log_history)
        self.log_text.see(tk.END)

    def toggle_out_path(self):
        state = "disabled" if self.same_path_var.get() else "normal"
        self.entry_out.config(state=state)
        self.btn_out.config(state=state)

    def browse_out(self):
        directory = filedialog.askdirectory()
        if directory:
            self.out_path_var.set(directory)

    def run(self):
        if not self.files:
            messagebox.showwarning("경고", "변환할 파일을 선택해 주세요.")
            return
        
        self.btn_run.config(state="disabled", text="실행 중...")
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        try:
            for f in self.files:
                target_dir = os.path.dirname(f) if self.same_path_var.get() else self.out_path_var.get()
                if not target_dir: target_dir = os.path.dirname(f)
                
                base_name = os.path.splitext(os.path.basename(f))[0] + "_rendered"
                out_file = get_unique_filepath(target_dir, base_name, ".mkv")
                
                cmd = [
                    "ffmpeg", "-hwaccel", "cuda", "-threads", "16", "-filter_threads", "8", 
                    "-i", f,
                    # balanced
                    # "-vf", "v360=input=fisheye:output=equirect:ih_fov=180:iv_fov=180:h_fov=180:v_fov=180:w=4096:h=4096:interp=nearest,pad=8192:4096:2048:0:black,format=yuv420p",
                    # "-c:v", "hevc_nvenc", "-preset", "p2", "-cq", "20", "-c:a", "aac"
                    # quality
                    "-vf", "v360=input=fisheye:output=equirect:ih_fov=180:iv_fov=180:h_fov=180:v_fov=180:w=4096:h=4096:interp=nearest,pad=8192:4096:2048:0:black,format=yuv420p",
                    "-c:v", "hevc_nvenc", "-preset", "p7", "-tune", "hq", "-cq", "12", "-c:a", "aac"
                ]
                if self.debug:
                    cmd.extend(["-t", str(self.test_len)])
                cmd.append(out_file)
                
                # subprocess.run(cmd)
                
                # meta_cmd = [
                #     "mkvpropedit", out_file,
                #     "--edit", "track:v1",
                #     "--set", "projection-type=1"
                # ]
                # subprocess.run(meta_cmd)

                self.root.after(0, lambda: self.btn_log.config(state="normal"))
                self.root.after(0, lambda: self.progress_var.set(0))
                self.root.after(0, lambda: self.status_label.config(text="초기화 중..."))
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                total_duration_sec = 0
                current_line = ""
                
                while True:
                    char = process.stdout.read(1)
                    if not char and process.poll() is not None:
                        break
                    
                    if char in ('\r', '\n'):
                        line = current_line.strip()
                        if line:
                            self.full_log_history += line + "\n"
                            
                            if self.log_window and tk.Toplevel.winfo_exists(self.log_window):
                                self.root.after(0, lambda l=line: (self.log_text.insert(tk.END, l + "\n"), self.log_text.see(tk.END)))
                            
                            match_dur = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", line)
                            if match_dur:
                                h, m, s = float(match_dur.group(1)), float(match_dur.group(2)), float(match_dur.group(3))
                                total_duration_sec += (h * 3600 + m * 60 + s)
                            
                            if line.startswith("frame="):
                                self.root.after(0, lambda l=line: self.status_label.config(text=l))
                                match_time = re.search(r"time=\s*(\d+):(\d+):(\d+\.\d+)", line)
                                if match_time and total_duration_sec > 0:
                                    h, m, s = float(match_time.group(1)), float(match_time.group(2)), float(match_time.group(3))
                                    current_sec = h * 3600 + m * 60 + s
                                    pct = min(100.0, (current_sec / total_duration_sec) * 100)
                                    self.root.after(0, lambda p=pct: self.progress_var.set(p))
                                    
                        current_line = ""
                    else:
                        current_line += char
                
                self.root.after(0, lambda: self.progress_var.set(100.0))
                self.root.after(0, lambda: self.status_label.config(text="메타데이터 주입 중..."))
                
                meta_cmd = [
                    "mkvpropedit", out_file,
                    "--edit", "track:v1",
                    "--set", "projection-type=1"
                ]
                subprocess.run(meta_cmd, creationflags=subprocess.CREATE_NO_WINDOW)
                
            messagebox.showinfo("완료", "모든 개별 변환 작업이 완료되었습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"작업 중 오류 발생:\n{e}")
        finally:
            self.btn_run.config(state="normal", text="Individual 실행")

if __name__ == "__main__":
    root = tk.Tk()
    app = IndividualApp(root)
    root.mainloop()