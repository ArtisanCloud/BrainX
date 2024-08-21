from hashlib import sha256


def generate_node_hash(text: str) -> str:
    """
    根据给定的文本生成一个 SHA-256 哈希值，并在文本末尾附加 'nil' 字符串。

    :param text: 用于生成哈希的文本内容
    :return: 生成的 SHA-256 哈希值（64 位十六进制字符串）
    """
    hash_text = text + "end"
    return sha256(hash_text.encode()).hexdigest()
