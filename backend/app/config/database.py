from typing import ClassVar
from pydantic import BaseModel
from sqlalchemy.pool import NullPool  # 导入 NullPool 连接池类


class Database(BaseModel):
    # common config参数
    dsn: str  # 数据库连接字符串
    db_schema: str = "public"  # 默认的数据库 schema
    pool_size: int = 4  # 最大连接数
    max_overflow: int = 4  # 超过池大小的最大连接数
    pool_timeout: int = 120  # 连接池获取连接的超时时间（秒）
    pool_recycle: int = 3600  # 连接最大生命周期（秒）
    pool_pre_ping: bool = True  # 连接池健康检查
    echo: bool = True  # 输出 SQL 日志

    # sync config参数
    poolclass:ClassVar = NullPool  # 默认使用 NullPool 连接池

    # async config参数
