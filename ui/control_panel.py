"""MingChart 左侧控制面板"""
import tkinter as tk
from tkinter import ttk, colorchooser

from config import (
    CHART_PIE, CHART_BAR, CHART_LINE, CHART_TYPES,
    DEFAULT_LABELS, DEFAULT_VALUES, DEFAULT_TITLE,
    DEFAULT_BG_COLOR, DEFAULT_FG_COLOR, DEFAULT_DPI,
    MARKER_OPTIONS, MODE_INPUT, MODE_DRAW
)


class ControlPanel(ttk.Frame):
    def __init__(self, master, on_preview=None, on_save=None,
                 on_export_html=None, on_mode_change=None, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.configure(style="TFrame")

        self.on_preview = on_preview
        self.on_save = on_save
        self.on_export_html = on_export_html
        self.on_mode_change = on_mode_change
        self.bg_color = DEFAULT_BG_COLOR
        self.fg_color = DEFAULT_FG_COLOR

        self._build()
        self._on_type_change()

    def _build(self):
        # ---------- 1. 图表类型 ----------
        type_frame = ttk.LabelFrame(self, text=" 1. 图表类型 ", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 8))

        self.chart_type = tk.StringVar(value=CHART_PIE)
        row = ttk.Frame(type_frame, style="Card.TFrame")
        row.pack(fill=tk.X)
        for text, val in CHART_TYPES:
            ttk.Radiobutton(
                row, text=text, value=val,
                variable=self.chart_type,
                command=self._on_type_change
            ).pack(side=tk.LEFT, padx=(0, 12))

        # ---------- 2. 数据输入 ----------
        data_frame = ttk.LabelFrame(self, text=" 2. 数据输入 ", padding=10)
        data_frame.pack(fill=tk.X, pady=(0, 8))
        self.data_frame = data_frame

        ttk.Label(data_frame, text="标签（英文逗号分隔）",
                  style="Hint.TLabel").pack(anchor=tk.W)
        self.labels_entry = ttk.Entry(data_frame, width=40,
                                      font=("Microsoft YaHei", 10))
        self.labels_entry.insert(0, DEFAULT_LABELS)
        self.labels_entry.pack(fill=tk.X, pady=(2, 8))

        ttk.Label(data_frame, text="数值（英文逗号分隔）",
                  style="Hint.TLabel").pack(anchor=tk.W)
        self.values_entry = ttk.Entry(data_frame, width=40,
                                      font=("Microsoft YaHei", 10))
        self.values_entry.insert(0, DEFAULT_VALUES)
        self.values_entry.pack(fill=tk.X, pady=(2, 0))

        # ---------- 3. 图表专属选项 ----------
        self.specific_frame = ttk.LabelFrame(self, text=" 3. 图表选项 ", padding=10)
        self.specific_frame.pack(fill=tk.X, pady=(0, 8))

        # 饼图
        self.pie_frame = ttk.Frame(self.specific_frame, style="Card.TFrame")
        self.show_percent_var = tk.BooleanVar(value=True)
        self.explode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.pie_frame, text="显示百分比",
                        variable=self.show_percent_var).pack(anchor=tk.W, pady=1)
        ttk.Checkbutton(self.pie_frame, text="扇区分离",
                        variable=self.explode_var).pack(anchor=tk.W, pady=1)

        # 柱/折
        self.axis_color_frame = ttk.Frame(self.specific_frame, style="Card.TFrame")
        
        mode_sub_frame = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        mode_sub_frame.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(mode_sub_frame, text="操作模式", style="Hint.TLabel").pack(anchor=tk.W)
        self.mode_var = tk.StringVar(value=MODE_INPUT)
        mode_row = ttk.Frame(mode_sub_frame, style="Card.TFrame")
        mode_row.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(mode_row, text="📝 数值模式", value=MODE_INPUT,
                        variable=self.mode_var,
                        command=self._on_mode_switch).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_row, text="🎨 绘制拖拽", value=MODE_DRAW,
                        variable=self.mode_var,
                        command=self._on_mode_switch).pack(side=tk.LEFT)

        ttk.Separator(self.axis_color_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="X 轴", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.xlabel_entry = ttk.Entry(row, font=("Microsoft YaHei", 10))
        self.xlabel_entry.insert(0, "类别")
        self.xlabel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Y 轴", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.ylabel_entry = ttk.Entry(row, font=("Microsoft YaHei", 10))
        self.ylabel_entry.insert(0, "数值")
        self.ylabel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="颜色", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.fg_label = tk.Label(row, text="  ", bg=self.fg_color,
                                 relief=tk.FLAT, width=4, cursor="hand2")
        self.fg_label.pack(side=tk.LEFT, padx=(0, 4))
        self.fg_label.bind("<Button-1>", lambda e: self._pick_fg_color())
        ttk.Button(row, text="更改", style="Small.TButton",
                   command=self._pick_fg_color).pack(side=tk.LEFT)

        self.marker_row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        self.marker_row.pack(fill=tk.X, pady=2)
        ttk.Label(self.marker_row, text="标记", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.marker_var = tk.StringVar(value=MARKER_OPTIONS[0])
        ttk.Combobox(self.marker_row, textvariable=self.marker_var, width=5,
                     state="readonly", values=MARKER_OPTIONS,
                     font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)

        # ---------- 4. 通用设置 ----------
        common_frame = ttk.LabelFrame(self, text=" 4. 通用设置 ", padding=10)
        common_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(common_frame, text="标题", style="Hint.TLabel").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(common_frame, font=("Microsoft YaHei", 10))
        self.title_entry.insert(0, DEFAULT_TITLE)
        self.title_entry.pack(fill=tk.X, pady=(2, 8))

        row = ttk.Frame(common_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=(0, 6))

        col1 = ttk.Frame(row, style="Card.TFrame")
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(col1, text="背景色", style="Hint.TLabel").pack(anchor=tk.W)
        sub = ttk.Frame(col1, style="Card.TFrame")
        sub.pack(fill=tk.X, pady=(2, 0))
        self.bg_label = tk.Label(sub, text="  ", bg=self.bg_color,
                                 relief=tk.FLAT, width=4, height=1,
                                 cursor="hand2")
        self.bg_label.pack(side=tk.LEFT)
        self.bg_label.bind("<Button-1>", lambda e: self._pick_bg_color())
        ttk.Button(sub, text="更改", style="Small.TButton",
                   command=self._pick_bg_color).pack(side=tk.LEFT, padx=4)

        # ★ 恢复 DPI 设置 ★
        col2 = ttk.Frame(row, style="Card.TFrame")
        col2.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(col2, text="DPI", style="Hint.TLabel").pack(anchor=tk.W)
        self.dpi_var = tk.IntVar(value=DEFAULT_DPI)
        ttk.Spinbox(col2, from_=50, to=600, increment=50,
                    textvariable=self.dpi_var, width=6,
                    font=("Microsoft YaHei", 10)).pack(pady=(2, 0))

        # ---------- 5. 操作按钮 ----------
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(6, 0))

        ttk.Button(btn_frame, text="🎨  生成/刷新预览",
                   style="Primary.TButton",
                   command=self._do_preview).pack(fill=tk.X, pady=2)

        row2 = ttk.Frame(btn_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Button(row2, text="💾  保存图片",
                   style="Success.TButton",
                   command=self._do_save).pack(side=tk.LEFT,
                                               fill=tk.X, expand=True,
                                               padx=(0, 2))
        ttk.Button(row2, text="🌐  导出 HTML",
                   command=self._do_export_html).pack(side=tk.LEFT,
                                                      fill=tk.X, expand=True,
                                                      padx=(2, 0))

    def _on_mode_switch(self):
        mode = self.mode_var.get()
        if mode == MODE_DRAW:
            self.labels_entry.config(state="disabled")
            self.values_entry.config(state="disabled")
        else:
            self.labels_entry.config(state="normal")
            self.values_entry.config(state="normal")
            
        if self.on_mode_change:
            self.on_mode_change(mode)
            
        self._do_preview()

    def _on_type_change(self):
        for f in [self.pie_frame, self.axis_color_frame]:
            f.pack_forget()

        t = self.chart_type.get()
        if t == CHART_PIE:
            self.pie_frame.pack(fill=tk.X)
            self.mode_var.set(MODE_INPUT)
            self.labels_entry.config(state="normal")
            self.values_entry.config(state="normal")
        elif t == CHART_BAR:
            self.axis_color_frame.pack(fill=tk.X)
            self.marker_row.pack_forget()
        elif t == CHART_LINE:
            self.axis_color_frame.pack(fill=tk.X)
            self.marker_row.pack(fill=tk.X, pady=2)

    def _pick_bg_color(self):
        c = colorchooser.askcolor(color=self.bg_color, title="选择背景色")[1]
        if c:
            self.bg_color = c
            self.bg_label.config(bg=c)

    def _pick_fg_color(self):
        c = colorchooser.askcolor(color=self.fg_color, title="选择图形颜色")[1]
        if c:
            self.fg_color = c
            self.fg_label.config(bg=c)

    def _do_preview(self):
        if self.on_preview:
            self.on_preview()

    def _do_save(self):
        if self.on_save:
            self.on_save()

    def _do_export_html(self):
        if self.on_export_html:
            self.on_export_html()

    def set_values_text(self, values):
        val_str = ",".join([f"{v:g}" for v in values])
        state = self.values_entry.cget("state")
        self.values_entry.config(state="normal")
        self.values_entry.delete(0, tk.END)
        self.values_entry.insert(0, val_str)
        self.values_entry.config(state=state)

    def get_mode(self):
        return self.mode_var.get()

    def get_chart_type(self):
        return self.chart_type.get()

    def get_labels_str(self):
        return self.labels_entry.get()

    def get_values_str(self):
        return self.values_entry.get()

    def get_title(self):
        return self.title_entry.get().strip() or DEFAULT_TITLE

    def get_dpi(self):
        try:
            return self.dpi_var.get()
        except tk.TclError:
            return DEFAULT_DPI

    def get_options(self):
        return {
            "title": self.get_title(),
            "bg_color": self.bg_color,
            "fg_color": self.fg_color,
            "show_percent": self.show_percent_var.get(),
            "explode": self.explode_var.get(),
            "xlabel": self.xlabel_entry.get() or "类别",
            "ylabel": self.ylabel_entry.get() or "数值",
            "marker": self.marker_var.get(),
        }