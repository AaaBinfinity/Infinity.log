def get_color(frequency, max_frequency):
    """
    根据频率生成深色系的暖色调颜色，频率越高，颜色越暖。
    这里使用 HSL 色调来生成颜色，频率值越大，色相偏向红色、橙色、黄色，且色调为深色。
    """
    normalized = frequency / max_frequency
    hue = int(normalized * 60)  # 色相（0 红色，60 黄色）
    saturation = 80  # 饱和度固定为 80%
    lightness = int(normalized * 20) + 20  # 亮度范围 20-40%

    return f"hsl({hue}, {saturation}%, {lightness}%)"