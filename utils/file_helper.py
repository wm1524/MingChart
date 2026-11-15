"""MingChart 文件保存与路径处理工具"""
import os
import shutil

IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.svg', '.pdf')


def ensure_extension(path, default_ext=".png"):
    if not path.lower().endswith(IMAGE_EXTS):
        return path + default_ext
    return path


def save_figure(fig, path, dpi=150):
    path = ensure_extension(path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    return os.path.abspath(path)


def move_temp_to(temp_file, target_path):
    target_path = ensure_extension(target_path)
    shutil.move(temp_file, target_path)
    return os.path.abspath(target_path)


def cleanup(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError:
        pass