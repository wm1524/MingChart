"""MingChart 左侧控制面板 (完美修复饼图选项显示)"""
import tkinter as tk
from tkinter import ttk, colorchooser
from config import (
    CHART_PIE, CHART_BAR, CHART_LINE, CHART_TYPES, DEFAULT_TITLE, 
    MODE_INPUT, MODE_DRAW, DEFAULT_DPI, DEFAULT_BG_COLOR, DEFAULT_FG_COLOR
)
from ui.table_editor import DataTableEditor

class ControlPanel(ttk.Frame):
    def __init__(self, master, on_preview=None, on_save=None, on_export_html=None, on_mode_change=None, **kwargs):
        super().__init__(master, padding=15, **kwargs)
        self.configure(style="TFrame")
        self.on_preview = on_preview
        self.on_save = on_save
        self.on_export_html = on_export_html
        self.on_mode_change = on_mode_change
        self.bg_color = DEFAULT_BG_COLOR
        self.fg_color = DEFAULT_FG_COLOR
        self.api_rows = []
        self.chart_radios = {}

        self._build()

    def _build(self):
        # ============ 1. 数据输入 ============
        data_frame = ttk.LabelFrame(self, text=" 1. 数据输入 ", padding=10)
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.data_source_var = tk.StringVar(value="manual")
        src_row = ttk.Frame(data_frame, style="Card.TFrame")
        src_row.pack(fill=tk.X, pady=(0, 10))
        ttk.Radiobutton(src_row, text="手动表格", value="manual", variable=self.data_source_var, command=self._on_data_source_change).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(src_row, text="多 API 接口", value="api", variable=self.data_source_var, command=self._on_data_source_change).pack(side=tk.LEFT)
        
        # 手动表格区
        self.manual_frame = ttk.Frame(data_frame, style="Card.TFrame")
        self.manual_frame.pack(fill=tk.BOTH, expand=True)
        self.table_editor = DataTableEditor(self.manual_frame)
        self.table_editor.pack(fill=tk.BOTH, expand=True)
        self.table_editor.set_data(["苹果", "香蕉", "橘子", "葡萄"], [35, 25, 20, 20])
        
        # API 动态区
        self.api_frame = ttk.Frame(data_frame, style="Card.TFrame")
        self.api_container = ttk.Frame(self.api_frame, style="Card.TFrame")
        self.api_container.pack(fill=tk.X)
        self.add_api_row("接口 1", "https://jsonplaceholder.typicode.com/users", "name", "id")
        ttk.Button(self.api_frame, text="➕ 添加新接口", style="Small.TButton", command=lambda: self.add_api_row(f"接口 {len(self.api_rows)+1}", "", "name", "id")).pack(fill=tk.X, pady=5)

        # ============ 2. 图表类型 ============
        type_frame = ttk.LabelFrame(self, text=" 2. 图表类型 ", padding=10)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        self.chart_type = tk.StringVar(value=CHART_PIE)
        row = ttk.Frame(type_frame, style="Card.TFrame")
        row.pack(fill=tk.X)
        for text, val in CHART_TYPES:
            rb = ttk.Radiobutton(row, text=text, value=val, variable=self.chart_type, command=self._on_type_change)
            rb.pack(side=tk.LEFT, padx=(0, 15))
            self.chart_radios[val] = rb

        # ============ 3. 交互与图表选项 ============
        self.specific_frame = ttk.LabelFrame(self, text=" 3. 图表选项 ", padding=10)
        self.specific_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 饼图选项
        self.pie_frame = ttk.Frame(self.specific_frame, style="Card.TFrame")
        self.show_percent_var = tk.BooleanVar(value=True)
        self.explode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.pie_frame, text="显示百分比", variable=self.show_percent_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(self.pie_frame, text="扇区分离", variable=self.explode_var).pack(anchor=tk.W, pady=2)

        # 柱状/折线选项（包含坐标轴、颜色等）
        self.axis_color_frame = ttk.Frame(self.specific_frame, style="Card.TFrame")
        
        # 操作模式（数值/拖拽）
        self.mode_sub_frame = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        ttk.Label(self.mode_sub_frame, text="操作模式", style="Hint.TLabel").pack(anchor=tk.W)
        self.mode_var = tk.StringVar(value=MODE_INPUT)
        mode_row = ttk.Frame(self.mode_sub_frame, style="Card.TFrame")
        mode_row.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(mode_row, text="📝 数值模式", value=MODE_INPUT, variable=self.mode_var, command=self._on_mode_switch).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(mode_row, text="🎨 绘制拖拽", value=MODE_DRAW, variable=self.mode_var, command=self._on_mode_switch).pack(side=tk.LEFT)

        # 坐标轴输入
        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="X 轴", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.xlabel_entry = ttk.Entry(row)
        self.xlabel_entry.insert(0, "类别")
        self.xlabel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Y 轴", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.ylabel_entry = ttk.Entry(row)
        self.ylabel_entry.insert(0, "数值")
        self.ylabel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 颜色选择
        row = ttk.Frame(self.axis_color_frame, style="Card.TFrame")
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="颜色", width=6, style="Hint.TLabel").pack(side=tk.LEFT)
        self.fg_label = tk.Label(row, text="  ", bg=self.fg_color, relief=tk.FLAT, width=4, cursor="hand2")
        self.fg_label.pack(side=tk.LEFT, padx=(0, 4))
        self.fg_label.bind("<Button-1>", lambda e: self._pick_fg_color())
        ttk.Button(row, text="更改", style="Small.TButton", command=self._pick_fg_color).pack(side=tk.LEFT)

        # ============ 4. 通用设置 ============
        common_frame = ttk.LabelFrame(self, text=" 4. 通用设置 ", padding=10)
        common_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(common_frame, text="标题", style="Hint.TLabel").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(common_frame)
        self.title_entry.insert(0, DEFAULT_TITLE)
        self.title_entry.pack(fill=tk.X, pady=(2, 8))

        # ============ 按钮 ============
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="🎨  生成/刷新预览", style="Primary.TButton", command=self._do_preview).pack(fill=tk.X, pady=4)
        row2 = ttk.Frame(btn_frame)
        row2.pack(fill=tk.X, pady=4)
        ttk.Button(row2, text="💾  保存图片", style="Success.TButton", command=self._do_save).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(row2, text="🌐  导出 HTML", command=self._do_export_html).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        # 初始化界面状态
        self._on_data_source_change()
        self._on_type_change()

    def _on_data_source_change(self):
        if self.data_source_var.get() == "manual":
            self.api_frame.pack_forget()
            self.manual_frame.pack(fill=tk.BOTH, expand=True)
            self.chart_radios[CHART_PIE].state(["!disabled"])
        else:
            self.manual_frame.pack_forget()
            self.api_frame.pack(fill=tk.X)
            self.chart_radios[CHART_PIE].state(["disabled"])
            if self.chart_type.get() == CHART_PIE:
                self.chart_type.set(CHART_BAR)
        
        # 强制刷新一次类型逻辑，确保界面正确
        self._on_type_change()

    def _on_type_change(self):
        # 1. 先隐藏所有选项
        self.pie_frame.pack_forget()
        self.axis_color_frame.pack_forget()

        # 2. 根据当前类型显示对应选项
        t = self.chart_type.get()
        if t == CHART_PIE:
            self.pie_frame.pack(fill=tk.X)
        else:
            self.axis_color_frame.pack(fill=tk.X)
            # 只有手动模式才显示“操作模式”
            if self.data_source_var.get() == "manual":
                self.mode_sub_frame.pack(fill=tk.X, pady=(0, 8), before=self.axis_color_frame.winfo_children()[1])
            else:
                self.mode_sub_frame.pack_forget()

    def _on_mode_switch(self):
        if self.on_mode_change:
            self.on_mode_change(self.mode_var.get())
        self._do_preview()

    def add_api_row(self, name_val, url_val, lk_val, vk_val):
        row_frame = ttk.Frame(self.api_container, style="Card.TFrame")
        row_frame.pack(fill=tk.X, pady=3)
        name_var = tk.StringVar(value=name_val)
        ttk.Entry(row_frame, textvariable=name_var, width=8).pack(side=tk.LEFT, padx=(0, 2))
        url_var = tk.StringVar(value=url_val)
        ttk.Entry(row_frame, textvariable=url_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        lk_var = tk.StringVar(value=lk_val)
        ttk.Entry(row_frame, textvariable=lk_var, width=6).pack(side=tk.LEFT, padx=2)
        vk_var = tk.StringVar(value=vk_val)
        ttk.Entry(row_frame, textvariable=vk_var, width=6).pack(side=tk.LEFT, padx=2)
        del_btn = tk.Label(row_frame, text="❌", fg="#ff4d4f", cursor="hand2", bg="#ffffff")
        del_btn.pack(side=tk.LEFT, padx=2)
        row_data = {"frame": row_frame, "name": name_var, "url": url_var, "lk": lk_var, "vk": vk_var}
        self.api_rows.append(row_data)
        del_btn.bind("<Button-1>", lambda e, r=row_data: self.remove_api_row(r))

    def remove_api_row(self, row_data):
        if row_data in self.api_rows:
            self.api_rows.remove(row_data)
            row_data["frame"].destroy()

    def _do_preview(self):
        if self.on_preview: self.on_preview()
    def _do_save(self):
        if self.on_save: self.on_save()
    def _do_export_html(self):
        if self.on_export_html: self.on_export_html()

    def _pick_bg_color(self):
        c = colorchooser.askcolor(color=self.bg_color, title="选择背景色")[1]
        if c: self.bg_color = c

    def _pick_fg_color(self):
        c = colorchooser.askcolor(color=self.fg_color, title="选择图形颜色")[1]
        if c:
            self.fg_color = c
            self.fg_label.config(bg=c)

    def get_data_source(self): return self.data_source_var.get()
    def get_manual_data(self): return self.table_editor.get_data()
    def set_manual_data(self, labels, values): self.table_editor.set_data(labels, values)
    def get_chart_type(self): return self.chart_type.get()
    def get_mode(self): return self.mode_var.get()
    def get_title(self): return self.title_entry.get().strip() or DEFAULT_TITLE
    
    def get_api_configs(self):
        configs = []
        for r in self.api_rows:
            if r["url"].get().strip():
                configs.append({
                    "name": r["name"].get().strip(), "url": r["url"].get().strip(),
                    "label_key": r["lk"].get().strip(), "value_key": r["vk"].get().strip()
                })
        return configs

    def get_options(self):
        return {
            "title": self.get_title(), "bg_color": self.bg_color, "fg_color": self.fg_color, 
            "show_percent": self.show_percent_var.get(), "explode": self.explode_var.get(), 
            "xlabel": self.xlabel_entry.get() or "类别", "ylabel": self.ylabel_entry.get() or "数值", "marker": "o"
        }