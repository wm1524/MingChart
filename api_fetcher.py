"""MingChart 接口数据获取模块 (支持深层嵌套 JSON 提取)"""
import urllib.request
import json
import ssl

def get_nested_value(data, path):
    """支持 'data.follower' 这种深层路径提取"""
    if not path:
        return None
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current

def fetch_multiple_apis(api_configs):
    """
    抓取多个接口的数据进行对比
    :param api_configs: 列表 [{"name": "名字", "url": "接口", "label_key": "标签路径", "value_key": "数值路径"}]
    """
    context = ssl._create_unverified_context()
    all_labels = []
    series_data = {}

    for i, config in enumerate(api_configs):
        url = config["url"]
        label_key = config["label_key"]
        value_key = config["value_key"]
        series_name = config["name"]

        try:
            # 伪装成浏览器，防止被 B 站拦截
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, context=context, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # 如果是老格式的列表，保持兼容
                if isinstance(data, list):
                    if i == 0: all_labels = [str(item.get(label_key, "未知")) for item in data]
                    vals = [float(item.get(value_key, 0)) for item in data]
                    series_data[series_name] = vals
                # 如果是字典（如 B 站），使用深层路径提取
                elif isinstance(data, dict):
                    # 找标签
                    label_val = get_nested_value(data, label_key)
                    if label_val is None:
                        label_val = series_name  # 找不到就用名字凑合
                    
                    # 找数值
                    val_raw = get_nested_value(data, value_key)
                    if val_raw is None:
                        raise ValueError(f"在返回的 JSON 中找不到路径 '{value_key}'")
                        
                    try:
                        val = float(val_raw)
                    except (ValueError, TypeError):
                        raise ValueError(f"提取到的值 '{val_raw}' 不是合法数字！")
                        
                    if i == 0:
                        all_labels = [str(label_val)]
                    
                    series_data[series_name] = [val]
                else:
                    raise ValueError("未知的 JSON 根结构")

        except Exception as e:
            raise Exception(f"接口 '{series_name}' 报错: {str(e)}")

    # 保证所有 series 的长度一致
    if len(series_data) > 0:
        first_len = len(list(series_data.values())[0])
        if first_len == 1:
            # 如果每个接口只抓到一个单值（比如粉丝数对比），我们就不需要 X 轴有多项
            all_labels = ["数据对比"]
        else:
            # 如果是列表数据，补全以防长短不一
            for k in series_data:
                while len(series_data[k]) < first_len:
                    series_data[k].append(0)
                all_labels = all_labels[:first_len]

    return all_labels, series_data