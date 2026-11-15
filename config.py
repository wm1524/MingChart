"""MingChart 全局配置"""
import matplotlib

matplotlib.rcParams['font.sans-serif'] = [
    'Microsoft YaHei', 'SimHei', 'PingFang SC',
    'WenQuanYi Zen Hei', 'DejaVu Sans'
]
matplotlib.rcParams['axes.unicode_minus'] = False

# ==================== 应用信息 ====================
APP_NAME = "MingChart"
APP_TITLE = "MingChart - 铭数据图表生成器"
APP_VERSION = "2.2.1"
WINDOW_SIZE = "1220x780"
MIN_WINDOW_SIZE = (1050, 680)

# ==================== 工作模式 ====================
MODE_INPUT = "input"
MODE_DRAW = "draw"

# ==================== 图表类型 ====================
CHART_PIE = "pie"
CHART_BAR = "bar"
CHART_LINE = "line"

CHART_TYPES = [
    ("饼图", CHART_PIE),
    ("柱状图", CHART_BAR),
    ("折线图", CHART_LINE),
]

# ==================== 默认数据 ====================
DEFAULT_LABELS = "苹果,香蕉,橘子,葡萄"
DEFAULT_VALUES = "35,25,20,20"
DEFAULT_TITLE = "数据图表"
DEFAULT_BG_COLOR = "#ffffff"
DEFAULT_FG_COLOR = "#4a90e2"
DEFAULT_DPI = 150

# ==================== 保存格式====================
SAVE_FILETYPES = [
    ("PNG 图片", "*.png"),
    ("JPEG 图片", "*.jpg"),
    ("PDF 文档", "*.pdf"),
]
HTML_FILETYPE = [("HTML 网页", "*.html")]

# ==================== 折线图标记 ====================
MARKER_OPTIONS = ["o", "s", "^", "D", "*", "x", "+"]

# ==================== 图片尺寸 ====================
FIGURE_SIZE = (8, 6)

# ==================== 主题配色 ====================
COLORS = {
    "primary":        "#4a90e2",
    "primary_hover":  "#357abd",
    "primary_light":  "#e8f1fc",
    "success":        "#52c41a",
    "success_hover":  "#45a816",
    "danger":         "#ff4d4f",
    "bg":             "#f5f7fa",
    "card":           "#ffffff",
    "border":         "#e1e4e8",
    "text":           "#262626",
    "text_secondary": "#8c8c8c",
    "label_bg":       "#fafbfc",
}

# 图表调色板
CHART_PALETTE = [
    "#4a90e2", "#50c5b7", "#f5a623", "#e94b6c",
    "#8b6fc9", "#ff8c5a", "#5bc0de", "#7ed321",
]