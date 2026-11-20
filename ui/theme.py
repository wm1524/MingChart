"""MingChart 界面主题：动态大屏适配"""
import tkinter as tk
from tkinter import ttk
from config import COLORS

def apply_theme(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # ================= 动态分辨率适配 =================
    screen_width = root.winfo_screenwidth()
    # 如果屏幕很宽（比如大屏触控白板），把 UI 放大 1.5 倍
    if screen_width >= 1920:
        scale = 1.5
    elif screen_width >= 1500:
        scale = 1.2
    else:
        scale = 1.0
        
    base_font_size = int(10 * scale)
    title_font_size = int(12 * scale)
    pad_x = int(10 * scale)
    pad_y = int(6 * scale)
    btn_pad_y = int(10 * scale)

    root.configure(bg=COLORS["bg"])
    style.configure(".", font=("Microsoft YaHei", base_font_size), background=COLORS["bg"])

    # Label 与 字体
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
    style.configure("Hint.TLabel", font=("Microsoft YaHei", int(9 * scale)), foreground=COLORS["text_secondary"])
    style.configure("TLabelframe", background=COLORS["card"], bordercolor=COLORS["border"], relief="solid", borderwidth=1)
    style.configure("TLabelframe.Label", background=COLORS["card"], foreground=COLORS["primary"], font=("Microsoft YaHei", title_font_size, "bold"))
    style.configure("Card.TFrame", background=COLORS["card"])
    style.configure("TFrame", background=COLORS["bg"])

    # 输入框与控件（增大内边距）
    style.configure("TEntry", padding=int(4 * scale), fieldbackground=COLORS["card"])
    style.configure("TSpinbox", padding=int(2 * scale))
    style.configure("TCombobox", padding=int(2 * scale))

    # 按钮（增大高度）
    style.configure("TButton", font=("Microsoft YaHei", base_font_size), padding=(pad_x, pad_y), borderwidth=0, background=COLORS["label_bg"])
    style.map("TButton", background=[("active", COLORS["primary_light"])])
    
    style.configure("Small.TButton", font=("Microsoft YaHei", int(9 * scale)), padding=(int(6*scale), int(4*scale)))

    # 亮色主按钮
    style.configure("Primary.TButton", font=("Microsoft YaHei", title_font_size, "bold"), padding=(pad_x, btn_pad_y), background=COLORS["primary"], foreground="white")
    style.map("Primary.TButton", background=[("active", COLORS["primary_hover"])])
    
    # 绿色成功按钮
    style.configure("Success.TButton", font=("Microsoft YaHei", title_font_size, "bold"), padding=(pad_x, btn_pad_y), background=COLORS["success"], foreground="white")
    style.map("Success.TButton", background=[("active", COLORS["success_hover"])])

    return style