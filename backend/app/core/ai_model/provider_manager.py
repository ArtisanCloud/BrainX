import os
from typing import Dict, Optional, Tuple

from sqlalchemy.orm import Session

from app.core.ai_model.drivers.langchain.driver import LangchainModelProviderDriver
from app.core.ai_model.drivers.interface.model_provider import ModelProviderInterface
from app.core.ai_model.schema.provider import ProviderSchema
from app.core.ai_model.schema.provider_model import ProviderModelSchema
from app.core.libs.file import get_project_path
from app.core.libs.yaml import load_yaml_file
from app.core.rag import FrameworkDriverType
from app.dao.tenant.tenant_default_model import TenantDefaultModelDAO
from app.models.model_provider.provider_model import ModelType

_global_provider_cache: Dict[str, ProviderSchema] | None = None


class ProviderManager:
    def __init__(self, framework_type: FrameworkDriverType):
        self._initialize(framework_type)
        self.model_provider_driver = None

    def _initialize(self, framework_type: FrameworkDriverType):
        match framework_type.value:
            case FrameworkDriverType.LANGCHAIN.value:
                self.model_provider_driver = LangchainModelProviderDriver()
            case _:
                raise Exception("Unsupported framework type for Provider Manager")

    def get_model_provider(self, db: Session, tenant_uuid: str, provider: str, model_type: ModelType) -> Tuple[
        Optional[ModelProviderInterface], Optional[Exception]]:

        # self.model_provider_driver
        _global_provider_cache[provider]

        return None, None

    def get_default_model_provider(
            self, db: Session,
            tenant_uuid: str, model_type: ModelType
    ) -> Tuple[Optional[ModelProviderInterface], Optional[Exception]]:
        try:
            # 获取默认模型
            service_tenant_default_model = TenantDefaultModelDAO(db)
            default_model, exception = service_tenant_default_model.get_default_model_by_uuid(
                tenant_uuid, model_type.value
            )

            if exception is not None:
                raise exception

            if default_model is None:
                raise Exception("Cannot query the default_model")

            model_provider, exception = self.model_provider_driver.convert_model_provider(
                db, tenant_uuid,
                default_model.provider_name, model_type)
            if exception is not None:
                return None, exception

        except Exception as e:
            # 记录异常或打印日志（可选）
            return None, e

        return model_provider, None

    def load_provider_models(self) -> Dict[str, ProviderSchema]:
        """Gather all configuration files under the given base path."""
        global _global_provider_cache

        # 如果全局缓存存在，直接返回它
        if _global_provider_cache is not None:
            return _global_provider_cache

        base_path = os.path.join(get_project_path(), 'core/ai_model/providers')

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
