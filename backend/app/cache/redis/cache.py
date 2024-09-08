from redis import asyncio as aioredis
from typing import Any, Optional
import json

from app.cache.interface import CacheInterface


class RedisCache(CacheInterface):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """设置缓存，支持设置过期时间（秒）"""
        if self.redis:
            value_str = json.dumps(value)
            await self.redis.set(key, value_str, ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if self.redis:
            value_str = await self.redis.get(key)
            if value_str:
                return json.loads(value_str)
        return None

    async def delete(self, key: str):
        """删除缓存"""
        if self.redis:
            await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        if self.redis:
            return await self.redis.exists(key) > 0
        return False

    async def increment(self, key: str, amount: int = 1) -> int:
        """自增缓存的值"""
        if self.redis:
            return await self.redis.incrby(key, amount)
        return 0

    async def acquire_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """尝试获取一个分布式锁"""
        if self.redis:
            return await self.redis.setnx(lock_key, "1", ex=timeout)

    async def release_lock(self, lock_key: str):
        """释放分布式锁"""
        if self.redis:
            await self.redis.delete(lock_key)

    async def set_expire(self, key: str, timeout: int):
        """设置过期时间"""
        if self.redis:
            await self.redis.expire(key, timeout)

    async def ttl(self, key: str) -> Optional[int]:
        """获取剩余过期时间"""
        if self.redis:
            return await self.redis.ttl(key)
        return None
