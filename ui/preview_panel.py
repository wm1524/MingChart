"""MingChart 预览面板：支持全图表悬停特效（饼图弹出、柱图高亮）、拖拽阻尼"""
import tkinter as tk
from tkinter import ttk
import numpy as np
import copy

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)

from config import COLORS, MODE_DRAW, CHART_BAR, CHART_LINE, CHART_PIE


class PreviewPanel(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style="Card.TFrame")
        self.fig = None
        self.canvas = None
        self.toolbar = None
        self.interactive_data = []
        self.annotation = None
        
        # 状态控制
        self.mode = "input"
        self.chart_type = ""
        self.values = []
        self.artists = {}
        self.dragging_index = None
        self.hovered_index = -1
        self.on_data_changed = None
        
        # 交互数据
        self.target_values = []
        self.base_colors = []
        self.original_wedges = [] # 用于恢复饼图状态

        self.hint = tk.Label(
            self, text="🖱 鼠标悬停在图形元素上可查看详细数值",
            bg=COLORS["primary_light"], fg=COLORS["primary"],
            font=("Microsoft YaHei", 10), pady=8, anchor="w", padx=12
        )
        self.hint.pack(fill=tk.X, padx=6, pady=(6, 0))

    def set_context(self, mode, chart_type, values, on_data_changed):
        self.mode = mode
        self.chart_type = chart_type
        self.values = list(values)
        self.target_values = list(values)
        self.on_data_changed = on_data_changed

        if self.mode == MODE_DRAW and self.chart_type in (CHART_BAR, CHART_LINE):
            self.hint.config(
                text="🎨 绘制模式：用鼠标按住柱子/折线点上下拖拽！",
                bg="#fff7e6", fg="#fa8c16"
            )
        else:
            self.hint.config(
                text="🖱 鼠标悬停可查看数值（饼图扇区会弹出），拖拽可修改",
                bg=COLORS["primary_light"], fg=COLORS["primary"]
            )

    def show_result(self, chart_result):
        self._clear()

        self.fig = chart_result.fig
        self.interactive_data = chart_result.interactive_data
        self.artists = chart_result.artists

        # 记录柱状图原始颜色
        if self.chart_type == CHART_BAR and "bars" in self.artists:
            self.base_colors = [bar.get_facecolor() for bar in self.artists["bars"]]

        # 记录饼图原始属性（用于弹出动画）
        if self.chart_type == CHART_PIE:
            for item in self.interactive_data:
                wedge = item["artist"]
                self.original_wedges.append({
                    "center": wedge.center,
                    "width": wedge.width,
                    "radius": wedge.r
                })

        self.annotation = self.fig.axes[0].annotate(
            "", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.6",
                      fc="#2c3e50", ec="none", alpha=0.92),
            arrowprops=dict(arrowstyle="->", color="#2c3e50", lw=1.5),
            color="white", fontsize=10, fontweight='bold',
            zorder=999
        )
        self.annotation.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # 绑定事件
        self.canvas.mpl_connect("motion_notify_event", self._on_hover)
        if self.chart_type in (CHART_BAR, CHART_LINE):
            self.canvas.mpl_connect("button_press_event", self._on_press)
            self.canvas.mpl_connect("button_release_event", self._on_release)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

    # ==================== 悬停特效 ====================
    def _on_hover(self, event):
        if event.inaxes is None:
            self._hide_annotation()
            self._reset_hover_effect()
            return

        found_idx = -1
        for i, item in enumerate(self.interactive_data):
            artist = item["artist"]
            # 兼容饼图和柱状图的命中检测
            contains = False
            if self.chart_type == CHART_PIE:
                contains = artist.contains(event)[0]
            else:
                contains = artist.contains(event)[0]
                
            if contains:
                found_idx = i
                if self.mode != MODE_DRAW:
                    self._show_annotation(artist, item, event)
                break

        if found_idx == -1:
            self._hide_annotation()

        self._apply_hover_effect(found_idx)

        if self.mode == MODE_DRAW and self.dragging_index is not None:
            self._execute_drag(event)

    def _apply_hover_effect(self, idx):
        if self.hovered_index == idx: return
        self.hovered_index = idx
        
        # 1. 柱状图：变色
        if self.chart_type == CHART_BAR and "bars" in self.artists:
            bars = self.artists["bars"]
            for i, bar in enumerate(bars):
                if i == idx:
                    r, g, b, a = self.base_colors[i]
                    bar.set_facecolor((min(r+0.2, 1), min(g+0.2, 1), min(b+0.2, 1), a))
                else:
                    bar.set_facecolor(self.base_colors[i])
                    
        # 2. 饼图：向外弹出（模拟网页端的 Explode 效果）
        elif self.chart_type == CHART_PIE:
            for i, item in enumerate(self.interactive_data):
                wedge = item["artist"]
                orig = self.original_wedges[i]
                if i == idx:
                    # 核心：计算扇区中心的坐标，让其沿角度方向向外平移
                    theta = (wedge.theta1 + wedge.theta2) / 2.0
                    angle_rad = np.deg2rad(theta)
                    # 弹出距离
                    offset = 0.15 
                    dx = offset * np.cos(angle_rad)
                    dy = offset * np.sin(angle_rad)
                    wedge.set_center((orig["center"][0] + dx, orig["center"][1] + dy))
                else:
                    # 恢复原状
                    wedge.set_center(orig["center"])
                    
        self.canvas.draw_idle()

    def _reset_hover_effect(self):
        if self.hovered_index == -1: return
        self.hovered_index = -1
        
        if self.chart_type == CHART_BAR and "bars" in self.artists:
            for i, bar in enumerate(self.artists["bars"]):
                bar.set_facecolor(self.base_colors[i])
                
        elif self.chart_type == CHART_PIE:
            for i, item in enumerate(self.interactive_data):
                item["artist"].set_center(self.original_wedges[i]["center"])
                
        self.canvas.draw_idle()

    def _show_annotation(self, artist, item, event):
        try:
            if hasattr(artist, "get_x") and hasattr(artist, "get_width"):
                px = artist.get_x() + artist.get_width() / 2
                py = artist.get_height()
            elif hasattr(artist, "get_center"):
                px, py = event.xdata, event.ydata
            else:
                px, py = artist.get_offsets()[0]

            self.annotation.xy = (px, py)
            self.annotation.set_text(f"  {item['label']}\n  数值: {item['value']:g}")
            self.annotation.set_visible(True)
            self.canvas.draw_idle()
        except Exception:
            self._hide_annotation()

    def _hide_annotation(self):
        if self.annotation and self.annotation.get_visible():
            self.annotation.set_visible(False)
            self.canvas.draw_idle()

    # ==================== 拖拽逻辑（仅柱/线） ====================
    def _on_press(self, event):
        if event.inaxes is None or event.button != 1: return
        
        if self.chart_type == CHART_BAR:
            for i, bar in enumerate(self.artists.get("bars", [])):
                if bar.contains(event)[0]:
                    self.dragging_index = i
                    break
        elif self.chart_type == CHART_LINE:
            ax = self.artists.get("ax")
            x_idx = list(ax.get_xticks())
            if event.xdata is not None:
                distances = [abs(x - event.xdata) for x in x_idx]
                min_idx = int(np.argmin(distances))
                if distances[min_idx] < 0.5:
                    self.dragging_index = min_idx

    def _execute_drag(self, event):
        if self.dragging_index is None or event.ydata is None: return
        
        new_y = max(0, event.ydata)
        self.target_values[self.dragging_index] = round(new_y, 1)

        ax = self.artists.get("ax")
        texts = self.artists.get("texts", [])
        
        diff = self.target_values[self.dragging_index] - self.values[self.dragging_index]
        self.values[self.dragging_index] += diff * 0.4

        if self.chart_type == CHART_BAR:
            bars = self.artists.get("bars", [])
            bar = bars[self.dragging_index]
            bar.set_height(self.values[self.dragging_index])
            r, g, b, a = self.base_colors[self.dragging_index]
            bar.set_facecolor((min(r+0.2, 1), min(g+0.2, 1), min(b+0.2, 1), a))
            
            if self.dragging_index < len(texts):
                texts[self.dragging_index].set_y(self.values[self.dragging_index])
                texts[self.dragging_index].set_text(f'{self.values[self.dragging_index]:.1f}')
                
        elif self.chart_type == CHART_LINE:
            line = self.artists.get("line")
            line.set_ydata(self.values)
            if self.dragging_index < len(texts):
                texts[self.dragging_index].set_position((self.dragging_index, self.values[self.dragging_index]))
                texts[self.dragging_index].set_text(f'{self.values[self.dragging_index]:.1f}')

        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)
        self.canvas.draw_idle()

    def _on_release(self, event):
        if self.dragging_index is not None:
            self.dragging_index = None
            for i in range(len(self.values)):
                self.values[i] = self.target_values[i]
            if self.on_data_changed:
                self.on_data_changed(self.values)

    # ==================== 清理 ====================
    def _clear(self):
        if self.toolbar:
            self.toolbar.destroy()
            self.toolbar = None
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None
        self.annotation = None
        self.interactive_data = []
        self.artists = {}
        self.dragging_index = None
        self.hovered_index = -1
        self.original_wedges = []

    def get_current_figure(self):
        return self.fig