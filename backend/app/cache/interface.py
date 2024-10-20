from abc import ABC, abstractmethod
from typing import Any, Optional, Callable
import asyncio


class CacheInterface(ABC):
    @abstractmethod
    def connect(self):
        """连接到缓存服务器"""
        pass

    @abstractmethod
    async def disconnect(self):
        """断开与缓存服务器的连接"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置缓存值，支持设置过期时间（秒）"""
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        pass

    @abstractmethod
    def delete(self, key: str):
        """删除缓存值"""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """检查缓存键是否存在"""
        pass

    @abstractmethod
    def increment(self, key: str, amount: int = 1) -> int:
        """自增缓存键的值"""
        pass

    @abstractmethod
    def acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """获取分布式锁"""
        pass

    @abstractmethod
    async def is_locked(self, lock_key: str) -> bool:
        pass

    @abstractmethod
    def release_lock(self, lock_key: str):
        """释放分布式锁"""
        pass

    @abstractmethod
    def set_expire(self, key: str, timeout: int):
        """设置缓存键的过期时间"""
        pass

    @abstractmethod
    def ttl(self, key: str) -> Optional[int]:
        """获取缓存键的剩余过期时间"""
        pass

    async def async_connect(self):
        pass

    async def async_disconnect(self):
        pass

    @abstractmethod
    async def a_set(self, key: str, value: Any, expire: Optional[int] = None):
        """异步设置缓存，支持设置过期时间（秒）"""

    @abstractmethod
    async def a_get(self, key: str) -> Optional[Any]:
        """异步获取缓存"""

    @abstractmethod
    async def a_delete(self, key: str):
        """异步删除缓存"""

    @abstractmethod
    async def a_exists(self, key: str) -> bool:
        """异步检查缓存是否存在"""

    @abstractmethod
    async def a_increment(self, key: str, amount: int = 1) -> int:
        """异步自增缓存的值"""

    @abstractmethod
    async def a_acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """异步尝试获取一个分布式锁"""

    @abstractmethod
    async def a_is_locked(self, lock_key: str) -> bool:
        pass

    @abstractmethod
    async def a_release_lock(self, lock_key: str):
        """异步释放分布式锁"""

    @abstractmethod
    async def a_set_expire(self, key: str, timeout: int):
        """异步设置过期时间"""

    @abstractmethod
    async def a_ttl(self, key: str) -> Optional[int]:
        """异步获取剩余过期时间"""

    def remember(self, key: str, ttl: int, func: Callable[[], str]) -> str:
        """
        Remember a value for a specified time to live (ttl) duration.
        If the key exists in cache, return it.
        Otherwise, call func to get the value, cache it, and return it.
        """
        value = self.get(key)

        if value is None:
            # If value is not found in cache, call the provided function
            value = func()

            # Store the result in cache with the specified TTL
            self.set(key, value, expire=ttl)
        return value

    async def a_remember(self, key: str, ttl: int, func: Callable[[], str]) -> str:
        """
        Remember a value for a specified time to live (ttl) duration.
        If the key exists in cache, return it.
        Otherwise, call func to get the value, cache it, and return it.
        """
        value = await self.a_get(key)

        if value is None:
            # If value is not found in cache, call the provided function
            value = func()

            # Store the result in cache with the specified TTL
            await self.a_set(key, value, expire=ttl)
        return value
