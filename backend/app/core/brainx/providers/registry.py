import mimetypes
from typing import Optional, Dict, Tuple

from app.core.brainx.entity.provider_model import ModelWithProviderEntity
from app.core.brainx.entity.runtime.provider import ProviderEntity
from app.core.brainx.entity.runtime.provider_model import ModelType, AIModelEntity
from app.core.libs.file import get_project_path
import os

from app.core.brainx.entity.provider import ProviderConfig
from app.core.libs.yaml import load_yaml_file

_global_provider_cache: Dict[str, ProviderEntity] | None = None


class ModelProviderRegistry:

    def get_models(
            self, provider: str = None,
            model_type: ModelType = None,
            provider_configs: Optional[list[ProviderConfig]] = None,
    ) -> Tuple[list[ModelWithProviderEntity], Optional[Exception]]:
        # return _global_provider_cache[provider], None
        return None, None

    @staticmethod
    def load_provider_entities() -> Tuple[Dict[str, ProviderEntity] | None, Exception | None]:
        """Gather all configuration files under the given base path."""
        global _global_provider_cache

        # 如果全局缓存存在，直接返回它
        if _global_provider_cache is not None:
            print("load_provider_entities with global cached")
            return _global_provider_cache, None

        try:

            base_path = os.path.join(get_project_path(), "core/brainx/providers")

            provider_schemas: Dict[str, ProviderEntity] = {}
            # print(base_path, provider_schemas)
            for folder_name in os.listdir(base_path):
                folder_path = os.path.join(base_path, folder_name)
                if os.path.isdir(folder_path):  # 确保是一个目录
                    provider_config_schema: Optional[ProviderEntity] = None

                    # 加载主配置文件（如 openai.yml）
                    for file in os.listdir(folder_path):
                        if file.endswith(".yml") or file.endswith(".yaml"):
                            filepath = os.path.join(folder_path, file)
                            yaml_data = load_yaml_file(filepath)

                            provider_config_schema = ProviderEntity(**yaml_data)
                            # print(provider_config_schema)
                            break  # 只加载一个主配置文件

                    if provider_config_schema is None:
                        continue

                    # 加载模型类型子文件夹中的所有 YAML 文件
                    for model_type in os.listdir(folder_path):
                        model_type_path = os.path.join(folder_path, model_type)
                        if os.path.isdir(model_type_path):  # 确保是一个目录

                            for model_file in os.listdir(model_type_path):
                                if model_file.endswith(".yml") or model_file.endswith(
                                        ".yaml"
                                ):
                                    model_filepath = os.path.join(
                                        model_type_path, model_file
                                    )
                                    # print("~~~~", model_file, model_filepath)

                                    # 加载该模型的配置文件
                                    yaml_data = load_yaml_file(model_filepath)
                                    model_schema = AIModelEntity(**yaml_data)
                                    provider_config_schema.models.append(model_schema)

                    # print(provider_config)
                    provider_schemas[folder_name] = provider_config_schema
        except Exception as e:
            return None, e

        # 保存到全局缓存中
        _global_provider_cache = provider_schemas
        # print(_global_provider_cache)

        return provider_schemas, None

    def get_provider_entity(self, provider: str) -> ProviderEntity:
        """
        Get provider instance by provider name
        :param provider: provider name
        :return: provider instance
        """
        # scan all providers
        model_provider_models, exception = self.load_provider_entities()
        if exception:
            raise exception
        # print(111, model_provider_models)

        # get the provider
        model_provider = model_provider_models[provider]
        # print(type(model_provider))
        if not model_provider:
            raise Exception(f"Invalid provider: {provider}")

        return model_provider

    def get_model_provider_icon(
            self, provider: str, icon_type: str, lang: str
    ) -> tuple[Optional[str], Optional[str], Optional[Exception]]:
        """
        get model provider icon.

        :param provider: provider name
        :param icon_type: icon type (icon_small or icon_large)
        :param lang: language (zh_Hans or en_US)
        :return:
        """
        provider_descriptor = self.get_provider_entity(provider)
        file_name: str | None = None

        if icon_type.lower() == "icon_small":
            if not provider_descriptor.icon_small:
                raise ValueError(f"Provider {provider} does not have small icon.")

            if lang.lower() == "zh_cn":
                file_name = (
                        provider_descriptor.icon_small.zh_Hans
                        or provider_descriptor.icon_small.en_US
                )
            else:
                file_name = provider_descriptor.icon_small.en_US
        else:
            if not provider_descriptor.icon_large:
                raise ValueError(f"Provider {provider} does not have large icon.")

            if lang.lower() == "zh_cn":
                # print(provider_descriptor.icon_large)
                file_name = provider_descriptor.icon_large.zh_Hans
            else:
                file_name = provider_descriptor.icon_large.en_US
        if not file_name:
            return None, None, Exception("Icon file not found.")

        root_path = get_project_path()
        provider_instance_path = os.path.join(
            root_path, "core", "brainx", "providers", provider
        )

        file_path = os.path.join(provider_instance_path, "assets")
        file_path = os.path.join(file_path, file_name)
        if not os.path.exists(file_path):
            return None, None, Exception("File not found: {}".format(file_path))

        mimetype, _ = mimetypes.guess_type(file_path)
        mimetype = mimetype or "application/octet-stream"

        # read binary from file
        # byte_data = Path(file_path).read_bytes()
        # return byte_data, mimetype, None
        return file_path, mimetype, None
