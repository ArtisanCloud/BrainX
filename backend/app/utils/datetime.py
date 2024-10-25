from datetime import datetime

datetime_format = "%Y-%m-%d %H:%M:%S"


def format_datetime(dt: datetime) -> str | None:
    if isinstance(dt, datetime):
        return dt.strftime(datetime_format)
    return None  # 返回 None，如果 dt 不是有效的 datetime 对象
