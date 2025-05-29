import uuid


def generate_session_id() -> str:
    """生成会话ID"""
    return str(uuid.uuid4())
