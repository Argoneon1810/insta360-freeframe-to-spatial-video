import tkinter as tk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class CustomFileList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.labels = []
        self.selected_indices = set()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.update_alignments(event.width)

    def insert(self, index, filepath):
        idx = len(self.labels)
        lbl = tk.Label(self.scrollable_frame, text=filepath, bg="white", anchor="w", padx=5, pady=2)
        lbl.pack(fill="x")
        lbl.bind("<Button-1>", lambda e, i=idx: self.toggle_selection(i))
        ToolTip(lbl, filepath)
        
        self.labels.append(lbl)
        self.update_alignments(self.canvas.winfo_width())

    def toggle_selection(self, idx):
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
            self.labels[idx].config(bg="white", fg="black")
        else:
            self.selected_indices.add(idx)
            self.labels[idx].config(bg="#0078D7", fg="white")

    def curselection(self):
        return sorted(list(self.selected_indices))

    def delete(self, first, last=None):
        if last == tk.END:
            for lbl in self.labels:
                lbl.destroy()
            self.labels.clear()
            self.selected_indices.clear()
        else:
            idx = first
            self.labels[idx].destroy()
            del self.labels[idx]
            if idx in self.selected_indices:
                self.selected_indices.remove(idx)
            
            new_selection = set()
            for sel in self.selected_indices:
                if sel > idx:
                    new_selection.add(sel - 1)
                else:
                    new_selection.add(sel)
            self.selected_indices = new_selection
            
            for i, lbl in enumerate(self.labels):
                lbl.bind("<Button-1>", lambda e, i=i: self.toggle_selection(i))

    def update_alignments(self, canvas_width):
        if canvas_width <= 1:
            return
        for lbl in self.labels:
            text_width = lbl.winfo_reqwidth()
            if text_width > canvas_width:
                lbl.config(anchor="e")
            else:
                lbl.config(anchor="w")