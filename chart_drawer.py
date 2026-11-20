"""MingChart 图表绘制核心"""
import matplotlib.pyplot as plt
import numpy as np
from config import CHART_PIE, CHART_BAR, CHART_LINE, FIGURE_SIZE, CHART_PALETTE

class ChartResult:
    def __init__(self, fig, interactive_data, artists=None):
        self.fig = fig
        self.interactive_data = interactive_data
        self.artists = artists or {}

class ChartDrawer:
    def draw(self, chart_type, labels, series_data, options=None):
        options = options or {}
        if chart_type == CHART_PIE:
            values = list(series_data.values())[0] if series_data else []
            return self._draw_pie(labels, values, options)
        elif chart_type == CHART_BAR:
            return self._draw_bar(labels, series_data, options)
        elif chart_type == CHART_LINE:
            return self._draw_line(labels, series_data, options)
        raise ValueError(f"未知图表类型: {chart_type}")

    def _add_watermark(self, fig):
        fig.text(0.98, 0.02, "MingChart 生成", fontsize=12, color="#999999", ha="right", va="bottom", alpha=0.8, fontweight="bold")
        fig.tight_layout()

    def _draw_pie(self, labels, values, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")
        show_percent = opt.get("show_percent", True)
        explode_flag = opt.get("explode", False)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        explode = [0.05] * len(values) if explode_flag else None
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%' if show_percent else None,
            explode=explode, startangle=90, shadow=True, colors=CHART_PALETTE[:len(values)],
            textprops={'fontsize': 11}
        )
        if autotexts:
            for a in autotexts:
                a.set_color('white')
                a.set_fontweight('bold')

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.axis('equal')
        self._add_watermark(fig)

        interactive = [{"artist": w, "label": l, "value": v} for w, l, v in zip(wedges, labels, values)]
        return ChartResult(fig, interactive, artists={})

    def _draw_bar(self, labels, series_data, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        x = np.arange(len(labels))
        width = 0.8 / len(series_data) if len(series_data) > 0 else 0.8

        first_bars = []
        texts = []
        for i, (name, values) in enumerate(series_data.items()):
            offset = (i - len(series_data)/2 + 0.5) * width
            # 这里只把第一组柱子暴露给拖拽/悬停检测
            bars = ax.bar(x + offset, values, width, label=name, color=CHART_PALETTE[i % len(CHART_PALETTE)], edgecolor="white", linewidth=1.2)
            
            if i == 0: first_bars = bars
            for bar, v in zip(bars, values):
                t = ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{v:g}', ha='center', va='bottom', fontsize=9)
                if i == 0: texts.append(t)

        if len(series_data) > 1:
            ax.legend()

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        self._add_watermark(fig)

        interactive = [{"artist": b, "label": l, "value": v} for b, l, v in zip(first_bars, labels, list(series_data.values())[0])]
        return ChartResult(fig, interactive, artists={"bars": first_bars, "texts": texts, "ax": ax})

    def _draw_line(self, labels, series_data, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")
        marker = opt.get("marker", "o")

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        first_line = None
        texts = []
        for i, (name, values) in enumerate(series_data.items()):
            line, = ax.plot(labels, values, marker=marker, color=CHART_PALETTE[i % len(CHART_PALETTE)], 
                    linewidth=2.2, markersize=9, markerfacecolor='white', markeredgewidth=2, label=name)
            if i == 0: first_line = line
            
            for x, y in zip(labels, values):
                t = ax.annotate(f'{y:g}', (x, y), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9)
                if i == 0: texts.append(t)

        if len(series_data) > 1:
            ax.legend()

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        self._add_watermark(fig)

        interactive = []
        first_vals = list(series_data.values())[0]
        for x, y, l in zip(labels, first_vals, labels):
            sc = ax.scatter([x], [y], s=200, color=CHART_PALETTE[0], alpha=0)
            interactive.append({"artist": sc, "label": l, "value": y})

        return ChartResult(fig, interactive, artists={"line": first_line, "texts": texts, "ax": ax})