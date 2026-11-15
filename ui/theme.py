"""MingChart 界面主题"""
import tkinter as tk
from tkinter import ttk
from config import COLORS


FONT_FAMILY = "Microsoft YaHei"
FONT_TITLE = (FONT_FAMILY, 12, "bold")
FONT_NORMAL = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)


def apply_theme(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    root.configure(bg=COLORS["bg"])
    style.configure(".", font=FONT_NORMAL, background=COLORS["bg"])

    style.configure("TLabel", background=COLORS["bg"],
                    foreground=COLORS["text"], font=FONT_NORMAL)
    style.configure("Title.TLabel", font=FONT_TITLE,
                    foreground=COLORS["text"])
    style.configure("Hint.TLabel", font=FONT_SMALL,
                    foreground=COLORS["text_secondary"])

    style.configure("TLabelframe",
                    background=COLORS["card"],
                    bordercolor=COLORS["border"],
                    relief="solid", borderwidth=1)
    style.configure("TLabelframe.Label",
                    background=COLORS["card"],
                    foreground=COLORS["primary"],
                    font=(FONT_FAMILY, 10, "bold"))

    style.configure("Card.TFrame", background=COLORS["card"])
    style.configure("TFrame", background=COLORS["bg"])

    style.configure("TEntry",
                    fieldbackground=COLORS["card"],
                    bordercolor=COLORS["border"],
                    lightcolor=COLORS["border"],
                    darkcolor=COLORS["border"])

    style.configure("TRadiobutton", background=COLORS["card"],
                    font=FONT_NORMAL)
    style.map("TRadiobutton",
              background=[("active", COLORS["card"])])
    style.configure("TCheckbutton", background=COLORS["card"],
                    font=FONT_NORMAL)
    style.map("TCheckbutton",
              background=[("active", COLORS["card"])])

    style.configure("TSpinbox",
                    fieldbackground=COLORS["card"],
                    bordercolor=COLORS["border"])

    style.configure("TCombobox",
                    fieldbackground=COLORS["card"],
                    bordercolor=COLORS["border"],
                    background=COLORS["card"])

    style.configure("TButton",
                    font=FONT_NORMAL,
                    borderwidth=0,
                    relief="flat",
                    padding=(10, 6),
                    background=COLORS["label_bg"],
                    foreground=COLORS["text"])
    style.map("TButton",
              background=[("active", COLORS["primary_light"])])

    style.configure("Primary.TButton",
                    font=(FONT_FAMILY, 10, "bold"),
                    borderwidth=0,
                    relief="flat",
                    padding=(10, 9),
                    background=COLORS["primary"],
                    foreground="white")
    style.map("Primary.TButton",
              background=[("active", COLORS["primary_hover"]),
                          ("pressed", COLORS["primary_hover"])])

    style.configure("Success.TButton",
                    font=(FONT_FAMILY, 10, "bold"),
                    borderwidth=0,
                    relief="flat",
                    padding=(10, 9),
                    background=COLORS["success"],
                    foreground="white")
    style.map("Success.TButton",
              background=[("active", COLORS["success_hover"]),
                          ("pressed", COLORS["success_hover"])])

    style.configure("Small.TButton",
                    font=FONT_SMALL,
                    borderwidth=1,
                    relief="solid",
                    padding=(6, 3),
                    background=COLORS["card"])

    return style