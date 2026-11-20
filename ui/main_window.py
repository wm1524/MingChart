"""MingChart 主窗口"""
import tkinter as tk
from tkinter import filedialog, messagebox
from config import APP_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE, SAVE_FILETYPES, HTML_FILETYPE
from chart_drawer import ChartDrawer
from html_exporter import HtmlExporter
from ui.control_panel import ControlPanel
from ui.preview_panel import PreviewPanel
from ui.theme import apply_theme
from utils.file_helper import save_figure
from api_fetcher import fetch_multiple_apis

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
        self.root.after(200, self._on_preview)

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
        self.preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _on_mode_change(self, mode):
        pass

    def _on_data_changed_from_preview(self, new_values):
        self.current_values = new_values
        # 拖拽结束，同步回表格
        labels = [row[0].get() for row in self.control.table_editor.rows if row[1].get()]
        self.control.set_manual_data(labels, new_values)

    def _on_preview(self):
        if self.control.get_data_source() == "api":
            configs = self.control.get_api_configs()
            if not configs:
                messagebox.showwarning("警告", "请至少配置一个有效的 API 接口！")
                return
            try:
                labels, series_data = fetch_multiple_apis(configs)
            except Exception as e:
                messagebox.showerror("接口数据错误", str(e))
                return
        else:
            labels, values = self.control.get_manual_data()
            if not labels or not values: return
            series_data = {"当前数据": values}
            self.current_values = values

        try:
            result = self.drawer.draw(
                self.control.get_chart_type(),
                labels, series_data,
                self.control.get_options()
            )
        except Exception as e:
            messagebox.showerror("绘图错误", str(e))
            return
            
        # 恢复完整的交互上下文
        self.preview.set_context(
            mode=self.control.get_mode(),
            chart_type=self.control.get_chart_type(),
            values=self.current_values,
            on_data_changed=self._on_data_changed_from_preview
        )
        self.preview.show_result(result)

    def _on_save(self):
        current_fig = self.preview.get_current_figure()
        if not current_fig:
            messagebox.showwarning("提示", "请先生成图表！")
            return
        path = filedialog.asksaveasfilename(title="保存图表", defaultextension=".png", filetypes=SAVE_FILETYPES, initialfile="mingchart.png")
        if not path: return
        try:
            saved = save_figure(current_fig, path, dpi=150)
            messagebox.showinfo("保存成功", f"图片已保存到：\n{saved}")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))

    def _on_export_html(self):
        labels, values = self.control.get_manual_data()
        if not labels or not values:
            messagebox.showwarning("提示", "请先在“手动表格”下生成数据，再导出 HTML。")
            return
        path = filedialog.asksaveasfilename(title="导出交互式 HTML", defaultextension=".html", filetypes=HTML_FILETYPE, initialfile="mingchart.html")
        if not path: return
        try:
            self.html_exporter.export(self.control.get_chart_type(), labels, values, self.control.get_options(), path)
            messagebox.showinfo("导出成功", f"交互式 HTML 已生成：\n{path}")
        except Exception as e:
            messagebox.showerror("导出失败", str(e))