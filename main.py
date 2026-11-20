"""MingChart 程序入口"""
import os
import sys
import tkinter as tk

from config import APP_NAME
from ui.main_window import MainWindow


def resource_path(relative_path):
    """获取资源绝对路径（兼容 PyInstaller 打包后）"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def set_window_icon(root):
    """设置窗口左上角图标"""
    icon_path = resource_path("icon.ico")
    if not os.path.exists(icon_path):
        print(f"[警告] 图标文件不存在: {icon_path}")
        return

    # 方法1：iconbitmap（Windows 最稳）
    try:
        root.iconbitmap(icon_path)
        return
    except Exception as e:
        print(f"[警告] iconbitmap 失败: {e}")

    # 方法2：Pillow 转 PhotoImage（跨平台兜底）
    try:
        from PIL import Image, ImageTk
        img = Image.open(icon_path)
        photo = ImageTk.PhotoImage(img)
        root.iconphoto(True, photo)
        root._icon_photo = photo   # 防 GC
    except Exception as e:
        print(f"[警告] iconphoto 也失败: {e}")


def main():
    root = tk.Tk()

    # Windows 高 DPI 适配
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # 设置窗口图标
    set_window_icon(root)

    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()