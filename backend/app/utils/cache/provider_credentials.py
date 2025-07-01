import json
from enum import Enum
from json import JSONDecodeError
from typing import Optional

from app.cache.factory import CacheFactory
from app.cache.interface import CacheInterface


class ProviderCredentialsCacheType(Enum):
    PROVIDER = "provider"
    MODEL = "provider_model"
    LOAD_BALANCING_MODEL = "load_balancing_provider_model"


class ProviderCredentialsCache:
    cache: CacheInterface

    def __init__(self, tenant_uuid: str, identity_id: str, cache_type: ProviderCredentialsCacheType):
        self.cache_key = f"{cache_type.value}_credentials:tenant_uuid:{tenant_uuid}:uuid:{identity_id}"
        self.cache = CacheFactory.get_cache()

    def get(self) -> Optional[dict]:
        """
        Get cached model provider credentials.

        :return:
        """
        cached_provider_credentials = self.cache.get(self.cache_key)
        return cached_provider_credentials

    def set(self, credentials: dict) -> None:
        """
        Cache model provider credentials.

        :param credentials: provider credentials
        :return:
        """
        self.cache.set(self.cache_key, json.dumps(credentials), 86400)

    def delete(self) -> None:
        """
        Delete cached model provider credentials.

        :return:
        """
        self.cache.delete(self.cache_key)
