import tkinter as tk
from individual_app_nvenc_nearest import IndividualApp
from merge_app_nvenc_nearest import MergeApp

def launch_app(root, mode, debug=False, test_len=5):
    root.destroy()
    new_root = tk.Tk()
    if mode == "individual":
        app = IndividualApp(new_root, debug=debug, test_len=test_len)
    else:
        app = MergeApp(new_root, debug=debug, test_len=test_len)
    new_root.mainloop()

def main():
    DEBUG_MODE = False
    DEBUG_MODE = True
    TEST_LEN = 5

    root = tk.Tk()
    root.title("Insta360 Converter")
    root.geometry("300x150")
    
    tk.Label(root, text="실행할 변환 모드를 선택해 주세요.", pady=15).pack()
    
    tk.Button(root, text="Individual 모드 (개별 변환)", command=lambda: launch_app(root, "individual", debug=DEBUG_MODE, test_len=TEST_LEN), height=2).pack(fill="x", padx=20, pady=5)
    tk.Button(root, text="Merge 모드 (병합 변환)", command=lambda: launch_app(root, "merge", debug=DEBUG_MODE, test_len=TEST_LEN), height=2).pack(fill="x", padx=20, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()