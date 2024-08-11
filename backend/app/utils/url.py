from urllib.parse import urlparse
from app.config.config import settings


def get_complete_url(resource_url: str) -> str:
    # 解析 URL
    parsed_url = urlparse(resource_url)

    # 检查 URL 是否包含网络协议 (例如 'http', 'https')
    if not parsed_url.scheme:
        # 如果没有协议，说明可能是相对路径，需要补充完整的 endpoint
        complete_url = f"{settings.storage.host}/{resource_url.lstrip('/')}"
    else:
        # 如果已经是完整的 URL，直接返回
        complete_url = resource_url

    return complete_url
