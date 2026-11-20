"""数据解析与校验：与 UI 解耦，方便单元测试"""


class DataParseError(Exception):
    """数据解析异常"""
    pass


def parse_labels(labels_str):
    """解析标签字符串 -> 列表"""
    if not labels_str or not labels_str.strip():
        raise DataParseError("标签不能为空")
    labels = [x.strip() for x in labels_str.split(",") if x.strip()]
    if not labels:
        raise DataParseError("至少需要一个标签")
    return labels


def parse_values(values_str):
    """解析数值字符串 -> 浮点列表"""
    if not values_str or not values_str.strip():
        raise DataParseError("数值不能为空")
    try:
        values = [float(x.strip()) for x in values_str.split(",") if x.strip()]
    except ValueError:
        raise DataParseError("数值格式错误，请使用数字（英文逗号分隔）")
    if not values:
        raise DataParseError("至少需要一个数值")
    return values


def parse_data(labels_str, values_str):
    """一次性解析标签和数值，返回 (labels, values)"""
    labels = parse_labels(labels_str)
    values = parse_values(values_str)
    if len(labels) != len(values):
        raise DataParseError(
            f"标签数量({len(labels)}) 与 数值数量({len(values)}) 不一致"
        )
    return labels, values