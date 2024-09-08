from abc import ABC, abstractmethod
from typing import Any, Optional, Callable


class CacheInterface(ABC):
    @abstractmethod
    async def connect(self):
        """连接到缓存服务器"""
        pass

    @abstractmethod
    async def disconnect(self):
        """断开与缓存服务器的连接"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置缓存值，支持设置过期时间（秒）"""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """删除缓存值"""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """检查缓存键是否存在"""
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        """自增缓存键的值"""
        pass

    @abstractmethod
    async def acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """获取分布式锁"""
        pass

    @abstractmethod
    async def release_lock(self, lock_key: str):
        """释放分布式锁"""
        pass

    @abstractmethod
    async def set_expire(self, key: str, timeout: int):
        """设置缓存键的过期时间"""
        pass

    @abstractmethod
    async def ttl(self, key: str) -> Optional[int]:
        """获取缓存键的剩余过期时间"""
        pass

    async def remember(self, key: str, ttl: int, func: Callable[[], str]) -> str:
        """
        Remember a value for a specified time to live (ttl) duration.
        If the key exists in cache, return it.
        Otherwise, call func to get the value, cache it, and return it.
        """
        value = await self.get(key)

        if value is None:
            # If value is not found in cache, call the provided function
            value = func()

            # Store the result in cache with the specified TTL
            await self.set(key, value, expire=ttl)
        return value
