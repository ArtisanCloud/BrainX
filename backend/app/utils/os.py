import os
import platform


def detect_os():
    if os.name == "posix":  # Linux 或 macOS
        if platform.system() == "Linux":
            return "Linux"
        elif platform.system() == "Darwin":  # macOS 的系统名称是 Darwin
            return "macOS"
    elif os.name == "nt":  # Windows
        return "Windows"
    return "Unknown"


def set_unix_permissions(path: str, permissions: int):
    """
    设置 Linux/macOS 的文件或目录权限
    :param path: 文件或目录路径
    :param permissions: 权限数值（例如 0o755 或 0o644）
    """
    os.chmod(path, permissions)


def set_windows_permissions(path: str, permissions: int):
    """
    设置 Windows 的文件或目录权限
    :param path: 文件或目录路径
    :param permissions: 权限数值（例如 0o666 或 0o444）
    """
    os.chmod(path, permissions)


def set_permissions(path: str, permissions: int):
    """
    根据操作系统类型设置权限
    :param path: 文件或目录路径
    :param permissions: 权限数值
    """
    system_type = detect_os()
    try:
        if system_type in ["Linux", "macOS"]:
            set_unix_permissions(path, permissions)
            print(f"Permissions set for {system_type}: {oct(permissions)}")
        elif system_type == "Windows":
            set_windows_permissions(path, permissions)
            print(f"Permissions set for Windows: {oct(permissions)}")
        else:
            print("Unknown OS. No permissions set.")
    except Exception as e:
        print(f"Failed to set permissions: {e}")
