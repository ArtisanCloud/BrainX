from typing import List

from app.models import ProviderModel


class ProviderManager:
    def __init__(self):
        # 初始化提供商管理器
        self.providers = {}

    def register_provider(self, provider_name: str, provider: ProviderModel):
        # 注册一个新的模型提供商
        if provider_name in self.providers:
            raise ValueError(f"Provider {provider_name} is already registered.")
        self.providers[provider_name] = provider

    def get_provider(self, provider_name: str) -> ProviderModel:
        # 根据名字获取模型提供商
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"Provider {provider_name} not found.")
        return provider

    def list_providers(self) -> List[str]:
        # 列出所有注册的模型提供商
        return list(self.providers.keys())

    def remove_provider(self, provider_name: str):
        # 移除一个模型提供商
        if provider_name in self.providers:
            del self.providers[provider_name]
        else:
            raise ValueError(f"Provider {provider_name} not found.")
