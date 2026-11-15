"""MingChart 主窗口"""
import tkinter as tk
from tkinter import filedialog, messagebox

from config import (
    APP_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE,
    SAVE_FILETYPES, HTML_FILETYPE
)
from data_parser import parse_data, DataParseError
from chart_drawer import ChartDrawer
from html_exporter import HtmlExporter
from ui.control_panel import ControlPanel
from ui.preview_panel import PreviewPanel
from ui.theme import apply_theme
from utils.file_helper import save_figure, move_temp_to, cleanup


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)

        apply_theme(self.root)

        self.drawer = ChartDrawer()
        self.html_exporter = HtmlExporter()
        self.current_values = []
        self._build()

    def _build(self):
        self.control = ControlPanel(
            self.root,
            on_preview=self._on_preview,
            on_save=self._on_save,
            on_export_html=self._on_export_html,
            on_mode_change=self._on_mode_change
        )
        self.control.pack(side=tk.LEFT, fill=tk.Y)

        self.preview = PreviewPanel(self.root, padding=0)
        self.preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True,
                          padx=8, pady=8)

    def _on_mode_change(self, mode):
        pass

    def _parse_input(self):
        try:
            return parse_data(
                self.control.get_labels_str(),
                self.control.get_values_str()
            )
        except DataParseError as e:
            messagebox.showerror("数据错误", str(e))
            return None, None

    def _build_figure(self, labels, values):
        return self.drawer.draw(
            self.control.get_chart_type(),
            labels, values,
            self.control.get_options()
        )

    def _on_data_changed_from_preview(self, new_values):
        self.current_values = new_values
        self.control.set_values_text(new_values)

    def _on_preview(self):
        labels, values = self._parse_input()
        if labels is None:
            return
            
        self.current_values = values
        
        try:
            result = self._build_figure(labels, values)
        except Exception as e:
            messagebox.showerror("绘图错误", str(e))
            return
            
        self.preview.set_context(
            mode=self.control.get_mode(),
            chart_type=self.control.get_chart_type(),
            values=values,
            on_data_changed=self._on_data_changed_from_preview
        )
        self.preview.show_result(result)

    def _on_save(self):
        current_fig = self.preview.get_current_figure()
        temp_file = None

        if current_fig is None:
            labels, values = self._parse_input()
            if labels is None:
                return
            try:
                result = self._build_figure(labels, values)
            except Exception as e:
                messagebox.showerror("绘图错误", str(e))
                return
            temp_file = "_mingchart_temp.png"
            result.fig.savefig(temp_file, dpi=self.control.get_dpi(),
                               bbox_inches="tight",
                               facecolor=result.fig.get_facecolor())
            import matplotlib.pyplot as plt
            plt.close(result.fig)

        path = filedialog.asksaveasfilename(
            title="保存图表",
            defaultextension=".png",
            filetypes=SAVE_FILETYPES,
            initialfile="mingchart.png"
        )
        if not path:
            cleanup(temp_file)
            return

        try:
            if temp_file:
                saved = move_temp_to(temp_file, path)
            else:
                saved = save_figure(current_fig, path,
                                    dpi=self.control.get_dpi())
            messagebox.showinfo("保存成功", f"图片已保存到：\n{saved}")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))
            cleanup(temp_file)

    def _on_export_html(self):
        labels, values = self._parse_input()
        if labels is None:
            return

        path = filedialog.asksaveasfilename(
            title="导出交互式 HTML",
            defaultextension=".html",
            filetypes=HTML_FILETYPE,
            initialfile="mingchart.html"
        )
        if not path:
            return

        try:
            saved = self.html_exporter.export(
                self.control.get_chart_type(),
                labels, values,
                self.control.get_options(),
                path
            )
            messagebox.showinfo(
                "导出成功",
                f"交互式 HTML 已生成：\n{saved}\n\n用浏览器打开即可悬停查看数据。"
            )
        except ImportError:
            messagebox.showerror(
                "缺少依赖",
                "导出 HTML 需要 plotly 库。\n\n"
                "请在 CMD 中执行：\n"
                "python -m pip install plotly -i https://pypi.tuna.tsinghua.edu.cn/simple"
            )
        except Exception as e:
            messagebox.showerror("导出失败", str(e))