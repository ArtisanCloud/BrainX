def process_json(content) -> str:
    # 处理非正规格式的json
    if content.startswith("```json"):
        # 移除markdown代码块标记
        content = content.replace("```json", "").replace("```", "").strip()
        return content
    else:
        return content
