from typing import Optional

from app.cache.interface import CacheInterface
from app.cache.redis.redis_cache import RedisCache


class CacheFactory:
    _instance: Optional[CacheInterface] = None

    @staticmethod
    def create_cache(cache_type: str, **kwargs) -> CacheInterface:
        if cache_type == "redis":
            return RedisCache(**kwargs)
        # 可以扩展其他缓存实现
        # elif cache_type == "memcached":
        #     return MemcachedCache(**kwargs)
        else:
            raise ValueError(f"Unsupported cache type: {cache_type}")

    @classmethod
    def get_cache(cls) -> CacheInterface:
        if cls._instance is None:
            raise RuntimeError("Cache instance not initialized. Call 'initialize_cache' first.")
        return cls._instance

    @classmethod
    def initialize_cache(cls, cache_type: str, **kwargs):
        if cls._instance is None:
            cls._instance = cls.create_cache(cache_type, **kwargs)
