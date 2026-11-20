"""MingChart 现代化表格输入组件"""
import tkinter as tk
from tkinter import ttk

class DataTableEditor(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, style="Card.TFrame", **kwargs)
        self.rows = []

        # 表头
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(header, text="标签", width=10, style="Hint.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(header, text="数值", width=10, style="Hint.TLabel").pack(side=tk.LEFT)
        
        # 滚动区域
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0, height=150)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=280)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 添加按钮
        self.add_btn = ttk.Button(self, text="➕ 添加数据", style="Small.TButton", command=lambda: self.add_row())
        self.add_btn.pack(fill=tk.X, pady=(5, 0))

    def add_row(self, label="", value=""):
        row_frame = ttk.Frame(self.scrollable_frame, style="Card.TFrame")
        row_frame.pack(fill=tk.X, pady=3)
        
        vcmd = (self.register(self._validate_number), '%P')
        lbl_var = tk.StringVar(value=label)
        val_var = tk.StringVar(value=str(value) if value != "" else "")
        
        ttk.Entry(row_frame, textvariable=lbl_var, width=10).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row_frame, textvariable=val_var, width=10, validate="key", validatecommand=vcmd).pack(side=tk.LEFT)
        
        del_btn = tk.Label(row_frame, text="❌", fg="#ff4d4f", cursor="hand2", bg="#ffffff")
        del_btn.pack(side=tk.LEFT, padx=5)
        
        row_data = (lbl_var, val_var, row_frame)
        self.rows.append(row_data)
        del_btn.bind("<Button-1>", lambda e, r=row_data: self.remove_row(r))

    def remove_row(self, row_data):
        if row_data in self.rows:
            self.rows.remove(row_data)
            row_data[2].destroy()

    def _validate_number(self, new_text):
        """严格拦截：只允许数字、负号和小数点"""
        if new_text in ("", "-"): return True
        try:
            float(new_text)
            return True
        except ValueError:
            return False

    def set_data(self, labels, values):
        for row in self.rows:
            row[2].destroy()
        self.rows.clear()
        for l, v in zip(labels, values):
            self.add_row(l, v)

    def get_data(self):
        labels, values = [], []
        for lbl_var, val_var, _ in self.rows:
            lbl, val = lbl_var.get().strip(), val_var.get().strip()
            if lbl and val:
                labels.append(lbl)
                values.append(float(val))
        return labels, values