import os
from typing import List, Dict, Any

import pytest

from app.core.libs.file import get_project_path
from app.core.libs.yaml import load_yaml_file
from app.models import ProviderModel

_global_provider_cache: Dict[str, Any] | None = None


class ProviderManager:
    def __init__(self):
        pass

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

    def load_provider_models(self) -> Dict[str, Any]:
        """Gather all configuration files under the given base path."""
        global _global_provider_cache

        # 如果全局缓存存在，直接返回它
        if _global_provider_cache is not None:
            return _global_provider_cache

        base_path = os.path.join(get_project_path(), 'core/ai_model/model_provider/providers')

        providers = {}
        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)
            if os.path.isdir(folder_path):  # 确保是一个目录
                provider_config = {}

                # 加载主配置文件（如 openai.yml）
                for file in os.listdir(folder_path):
                    if file.endswith('.yml') or file.endswith('.yaml'):
                        filepath = os.path.join(folder_path, file)
                        provider_config.update(load_yaml_file(filepath))
                        break  # 只加载一个主配置文件

                # 加载模型类型子文件夹中的所有 YAML 文件
                provider_config["models"] = {}
                for model_type in os.listdir(folder_path):
                    model_type_path = os.path.join(folder_path, model_type)
                    if os.path.isdir(model_type_path):  # 确保是一个目录
                        provider_config["models"][model_type] = {}

                        for model_file in os.listdir(model_type_path):
                            if model_file.endswith('.yml') or model_file.endswith('.yaml'):
                                model_filepath = os.path.join(model_type_path, model_file)
                                model_name = os.path.splitext(model_file)[0]  # 去掉文件扩展名，作为模型名

                                # 加载该模型的配置文件
                                model_config = load_yaml_file(model_filepath)
                                provider_config["models"][model_type][model_name] = model_config
                # print(provider_config)
                providers[folder_name] = provider_config

        # 保存到全局缓存中
        _global_provider_cache = providers
        # print(_global_provider_cache)

        return providers

    def load_providers(self) -> List[str]:
        # 列出所有注册的模型提供商
        return list(self.providers.keys())

    def list_providers(self) -> List[str]:
        # 列出所有注册的模型提供商
        return list(self.providers.keys())

    def remove_provider(self, provider_name: str):
        # 移除一个模型提供商
        if provider_name in self.providers:
            del self.providers[provider_name]
        else:
            raise ValueError(f"Provider {provider_name} not found.")
