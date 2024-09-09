import json

from pydantic import BaseModel
from redis import asyncio as aioredis
from redis import StrictRedis
from typing import Any, Optional

from redis.asyncio import Redis

from app.cache.interface import CacheInterface


class RedisCache(CacheInterface):
    def __init__(self, redis_url: str, **kwargs):
        self.redis_url = redis_url
        self.a_redis: Optional[Redis] = None
        self.redis: Optional[StrictRedis] = None

    def connect(self):
        if self.redis is None:
            self.redis = StrictRedis.from_url(self.redis_url)

    def disconnect(self):
        if self.redis:
            self.redis.close()

    def set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置缓存，支持设置过期时间（秒）"""
        if self.redis:
            if isinstance(value, BaseModel):
                # 如果 value 是 Pydantic 模型，将其序列化为 JSON 字符串
                value = value.json()
            elif not isinstance(value, (str, bytes, int, float)):
                # 如果不是原生类型，也不是 Pydantic 模型，尝试将其转换为 JSON 字符串
                value = json.dumps(value)
            self.redis.set(key, value, ex=expire)

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if self.redis:
            value_str = self.redis.get(key)
            return value_str
        return None

    def delete(self, key: str):
        """删除缓存"""
        if self.redis:
            self.redis.delete(key)

    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if self.redis:
            return self.redis.exists(key) > 0
        return False

    def increment(self, key: str, amount: int = 1) -> int:
        """自增缓存的值"""
        if self.redis:
            return self.redis.incrby(key, amount)
        return 0

    def acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """尝试获取一个分布式锁"""
        if self.redis:
            return self.redis.setnx(lock_key, "True")

    def is_locked(self, lock_key: str) -> bool:
        if self.redis:
            return self.get(lock_key)
        return False

    def release_lock(self, lock_key: str):
        """释放分布式锁"""
        if self.redis:
            self.redis.delete(lock_key)

    def set_expire(self, key: str, timeout: int):
        """设置过期时间"""
        if self.redis:
            self.redis.expire(key, timeout)

    def ttl(self, key: str) -> Optional[int]:
        """获取剩余过期时间"""
        if self.redis:
            return self.redis.ttl(key)
        return None

    async def async_connect(self):
        if self.a_redis is None:
            self.a_redis = aioredis.from_url(self.redis_url)

    async def async_disconnect(self):
        if self.a_redis:
            await self.a_redis.close()

    async def a_set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置缓存，支持设置过期时间（秒）"""
        if self.a_redis:
            if isinstance(value, BaseModel):
                # 如果 value 是 Pydantic 模型，将其序列化为 JSON 字符串
                value = value.json()
            elif not isinstance(value, (str, bytes, int, float)):
                # 如果不是原生类型，也不是 Pydantic 模型，尝试将其转换为 JSON 字符串
                value = json.dumps(value)
            await self.a_redis.set(key, value, ex=expire)

    async def a_get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if self.a_redis:
            value_str = await self.a_redis.get(key)
            return value_str
        return None

    async def a_delete(self, key: str):
        """删除缓存"""
        if self.a_redis:
            await self.a_redis.delete(key)

    async def a_exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if self.a_redis:
            return await self.a_redis.exists(key) > 0
        return False

    async def a_increment(self, key: str, amount: int = 1) -> int:
        """自增缓存的值"""
        if self.a_redis:
            return await self.a_redis.incrby(key, amount)
        return 0

    async def a_acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """尝试获取一个分布式锁"""
        if self.a_redis:
            return await self.a_redis.setnx(lock_key, "True")
        return False

    async def a_is_locked(self, lock_key: str) -> bool:
        if self.a_redis:
            return await self.a_get(lock_key)
        return False

    async def a_release_lock(self, lock_key: str):
        """释放分布式锁"""
        if self.a_redis:
            await self.a_redis.delete(lock_key)

    async def a_set_expire(self, key: str, timeout: int):
        """设置过期时间"""
        if self.a_redis:
            await self.a_redis.expire(key, timeout)

    async def a_ttl(self, key: str) -> Optional[int]:
        """获取剩余过期时间"""
        if self.a_redis:
            return await self.a_redis.ttl(key)
        return None
