"""MingChart 图表绘制核心"""
import matplotlib.pyplot as plt

from config import (
    CHART_PIE, CHART_BAR, CHART_LINE,
    FIGURE_SIZE, CHART_PALETTE,
)


class ChartResult:
    """绘图结果：Figure + 可交互元数据 + 底层对象"""

    def __init__(self, fig, interactive_data, artists=None):
        self.fig = fig
        self.interactive_data = interactive_data
        self.artists = artists or {}


class ChartDrawer:
    def draw(self, chart_type, labels, values, options=None):
        options = options or {}
        if chart_type == CHART_PIE:
            return self._draw_pie(labels, values, options)
        elif chart_type == CHART_BAR:
            return self._draw_bar(labels, values, options)
        elif chart_type == CHART_LINE:
            return self._draw_line(labels, values, options)
        raise ValueError(f"未知图表类型: {chart_type}")

    def _add_watermark(self, fig):
        """统一的右下角水印方法"""
        fig.text(
            0.98, 0.02, "MingChart 生成", 
            fontsize=12, 
            color="#999999", 
            ha="right", 
            va="bottom", 
            alpha=0.8, 
            fontweight="bold"
        )
        fig.tight_layout()

    # ---------- 饼图 ----------
    def _draw_pie(self, labels, values, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")
        show_percent = opt.get("show_percent", True)
        explode_flag = opt.get("explode", False)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        explode = [0.05] * len(values) if explode_flag else None
        wedges, texts, autotexts = ax.pie(
            values, labels=labels,
            autopct='%1.1f%%' if show_percent else None,
            explode=explode, startangle=90, shadow=True,
            colors=CHART_PALETTE[:len(values)],
            textprops={'fontsize': 11}
        )
        if autotexts:
            for a in autotexts:
                a.set_color('white')
                a.set_fontweight('bold')

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.axis('equal')
        
        self._add_watermark(fig)

        interactive = [
            {"artist": w, "label": l, "value": v}
            for w, l, v in zip(wedges, labels, values)
        ]
        return ChartResult(fig, interactive, artists={})

    # ---------- 柱状图 ----------
    def _draw_bar(self, labels, values, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")
        fg = opt.get("fg_color", "#4a90e2")
        xlabel = opt.get("xlabel", "类别")
        ylabel = opt.get("ylabel", "数值")

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        bars = ax.bar(labels, values, color=fg,
                      edgecolor="white", linewidth=1.2)
        
        texts = []
        for bar, v in zip(bars, values):
            t = ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                        f'{v:g}', ha='center', va='bottom', fontsize=10)
            texts.append(t)

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        self._add_watermark(fig)

        interactive = [
            {"artist": b, "label": l, "value": v}
            for b, l, v in zip(bars, labels, values)
        ]
        return ChartResult(fig, interactive, artists={"bars": bars, "texts": texts, "ax": ax})

    # ---------- 折线图 ----------
    def _draw_line(self, labels, values, opt):
        bg = opt.get("bg_color", "white")
        title = opt.get("title", "数据图表")
        fg = opt.get("fg_color", "#4a90e2")
        xlabel = opt.get("xlabel", "类别")
        ylabel = opt.get("ylabel", "数值")
        marker = opt.get("marker", "o")

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, facecolor=bg)
        ax.set_facecolor(bg)

        line, = ax.plot(labels, values, marker=marker, color=fg,
                        linewidth=2.2, markersize=9,
                        markerfacecolor='white',
                        markeredgewidth=2)
        
        texts = []
        for x, y in zip(labels, values):
            t = ax.annotate(f'{y:g}', (x, y), textcoords="offset points",
                        xytext=(0, 12), ha='center', fontsize=9)
            texts.append(t)

        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        self._add_watermark(fig)

        interactive = []
        for x, y, l in zip(labels, values, labels):
            sc = ax.scatter([x], [y], s=200, color=fg, alpha=0)
            interactive.append({"artist": sc, "label": l, "value": y})
        
        return ChartResult(fig, interactive, artists={"line": line, "texts": texts, "ax": ax})