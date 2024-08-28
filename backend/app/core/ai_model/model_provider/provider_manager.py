import os
from typing import Dict, Optional

from app.core.ai_model.model_provider.schema.provider import ProviderSchema
from app.core.ai_model.model_provider.schema.provider_model import ProviderModelSchema
from app.core.libs.file import get_project_path
from app.core.libs.yaml import load_yaml_file

_global_provider_cache: Dict[str, ProviderSchema] | None = None


class ProviderManager:
    def __init__(self):
        pass

    def load_provider_models(self) -> Dict[str, ProviderSchema]:
        """Gather all configuration files under the given base path."""
        global _global_provider_cache

        # 如果全局缓存存在，直接返回它
        if _global_provider_cache is not None:
            return _global_provider_cache

        base_path = os.path.join(get_project_path(), 'core/ai_model/model_provider')

        provider_schemas: Dict[str, ProviderSchema] = {}
        # print(base_path,provider_schemas)
        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)
            if os.path.isdir(folder_path):  # 确保是一个目录
                provider_config_schema: Optional[ProviderSchema] = None

                # 加载主配置文件（如 openai.yml）
                for file in os.listdir(folder_path):
                    if file.endswith('.yml') or file.endswith('.yaml'):
                        filepath = os.path.join(folder_path, file)
                        yaml_data = load_yaml_file(filepath)

                        provider_config_schema = ProviderSchema.construct(**yaml_data)
                        # print(provider_config_schema)
                        break  # 只加载一个主配置文件

                if provider_config_schema is None:
                    continue

                # 加载模型类型子文件夹中的所有 YAML 文件
                for model_type in os.listdir(folder_path):
                    model_type_path = os.path.join(folder_path, model_type)
                    if os.path.isdir(model_type_path):  # 确保是一个目录

                        for model_file in os.listdir(model_type_path):
                            if model_file.endswith('.yml') or model_file.endswith('.yaml'):

                                model_filepath = os.path.join(model_type_path, model_file)
                                # print("~~~~", model_file, model_filepath)

                                # 加载该模型的配置文件
                                yaml_data = load_yaml_file(model_filepath)
                                model_schema = ProviderModelSchema.construct(**yaml_data)
                                # print("!!!!!!!",model_schema)
                                provider_config_schema.models.append(model_schema)

                # print(provider_config)
                provider_schemas[folder_name] = provider_config_schema

        # 保存到全局缓存中
        _global_provider_cache = provider_schemas
        # print(_global_provider_cache)

        return provider_schemas
