import urllib
from urllib.parse import urlparse, unquote, urljoin
from pathlib import Path
from typing import Tuple
import platform
import os
from app.config.config import settings


def get_project_root() -> str:
    """获取项目根目录的绝对路径"""
    current_file = Path(__file__).resolve()  # 获取当前文件的绝对路径
    # 假设 utils 目录在项目根目录的 app/utils 下
    project_root = current_file.parent.parent.parent
    return str(project_root)


def get_storage_path(uri: str) -> str:
    # 处理 file:// URL
    if uri.startswith("file://"):
        # 解析 file:// URL
        parsed_url = urllib.parse.urlparse(uri)
        file_path = parsed_url.path  # 获取文件的路径部分

        # 如果文件路径包含 URL 编码字符，进行解码
        file_path = urllib.parse.unquote(file_path)

        # 确保文件路径是绝对路径，通常不需要再用 get_project_root 拼接
        return os.path.normpath(file_path)

    project_root = get_project_root()
    abs_path = os.path.normpath(os.path.join(project_root, uri))
    return abs_path


def get_oss_url(uri: str) -> str:
    print(settings.storage.minio)
    endpoint = settings.storage.minio.endpoint
    use_ssl = settings.storage.minio.use_ssl

    # 根据 use_ssl 补齐协议
    protocol = "https://" if use_ssl else "http://"
    full_endpoint = f"{protocol}{endpoint}"

    # 拼接完整 URL
    return urljoin(full_endpoint, uri)


def get_storage_complete_url(resource_url: str) -> Tuple[str, bool]:
    """
    获取完整的存储URL或文件路径

    Args:
        resource_url: 资源URL或路径

    Returns:
        Tuple[str, str]: (完整URL或文件路径, 类型['url'|'file'])
    """
    # 解析 URL 并处理编码
    resource_url = unquote(resource_url)
    parsed_url = urlparse(resource_url)

    # 检查是否已经是完整的网络URL
    if parsed_url.scheme in ("http", "https"):
        return resource_url, True

    # 如果是 file:// 协议，直接获取路径部分
    if parsed_url.scheme == "file":
        path = parsed_url.path
        # Windows 路径需要去掉开头的额外斜杠
        if platform.system() == "Windows" and path.startswith("/"):
            path = path[1:]
        return path, False

    # 检查是否是绝对路径
    if os.path.isabs(resource_url):
        return resource_url, False

    # 处理相对路径
    if not parsed_url.scheme:
        # 将相对路径转换为绝对路径（相对于项目根目录）
        project_root = get_project_root()
        abs_path = os.path.normpath(os.path.join(project_root, resource_url))
        return abs_path, False

    # 默认返回原始路径
    return resource_url, False


def is_file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    try:
        return os.path.exists(file_path) and os.path.isfile(file_path)
    except Exception:
        return False


# 使用示例：
"""
url, is_url = get_storage_complete_url("http://example.com/file.pdf")
# 返回: ("http://example.com/file.pdf", True)

url, is_url = get_storage_complete_url("/absolute/path/file.pdf")
# Unix返回: ("file:///absolute/path/file.pdf", False)
# Windows返回: ("file:///C:/absolute/path/file.pdf", False)

url, is_url = get_storage_complete_url("relative/path/file.pdf")
# 返回相对于项目根目录的完整file://路径

url, is_url = get_storage_complete_url("storage/uploads/file.pdf")
# 返回: ("http://storage-host/storage/uploads/file.pdf", True)
"""
