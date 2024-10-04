import json
import re


def sanitize_json(content, encode='utf-8'):
    """
    处理非正规格式的JSON，使其变为合法可解析的JSON格式
    """
    # 处理空字符串的情况
    if not content:
        return '{}'  # 或者抛出一个 ValueError

    # 如果输入不是字符串，检查是否是字典
    if not isinstance(content, str):
        if isinstance(content, dict):
            json_bytes = json.dumps(content, separators=(',', ':')).encode(encode)
            return json_bytes.decode('utf-8')
        else:
            raise ValueError("无法处理的输入格式")

    # 去除前导和尾随空白字符
    content = content.strip()

    # 移除以 ```json 开头和 ``` 结尾的代码块标记
    code_block_pattern = re.compile(r'^```json\s*([\s\S]*?)\s*```$', re.MULTILINE)
    match = code_block_pattern.match(content)
    if match:
        content = match.group(1).strip()

    # 尝试直接解析合法的JSON
    try:
        json_obj = json.loads(content)
        json_bytes = json.dumps(json_obj, separators=(',', ':')).encode(encode)
        return json_bytes.decode('utf-8')

    except json.JSONDecodeError as e:
        # 输出解析错误信息
        print(f"直接解析失败: {e}. 尝试修复.")

        # 移除单行注释 (//...)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # 移除多行注释 (/*...*/)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.S)

        # 移除尾部多余的逗号，允许逗号后有空格或换行符
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r',\s*]', ']', content)

        try:
            # 尝试解析修复后的内容
            json_obj = json.loads(content)
            json_bytes = json.dumps(json_obj, separators=(',', ':')).encode(encode)
            return json_bytes.decode('utf-8')

        except json.JSONDecodeError as e:
            raise ValueError(f"无法修复并解析此JSON: {e}")