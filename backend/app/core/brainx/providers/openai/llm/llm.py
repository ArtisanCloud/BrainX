from typing import Mapping, Any

from langchain_openai import ChatOpenAI
from pydantic import Field

from app.core.brainx.base import LLMModel
from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider_model import FetchFrom
from app.core.brainx.entity.runtime.provider_model import AIModelEntity, ModelType
from app.core.brainx.interface.llm import LLM
from app.core.exception.exceptions import ProviderModelCredentialNotProvidedException


class OpenAILMM(LLM):
    model_id: str = Field(default=LLMModel.OPENAI_GPT_3_D_5_TURBO, description="模型 ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(self, credentials: Mapping) -> None:

        llm = self.get_provider_model({
            "credentials": credentials,
            "streaming": False,
        })

        llm.invoke("ping")

    def get_provider_model(self, params: dict = None) -> Any:
        # 从 params 提取参数
        credentials = dict(params.get("credentials", {})) if params else {}
        print("credentials:", credentials)
        if not credentials:
            raise ProviderModelCredentialNotProvidedException()
        temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
        streaming = bool(params.get("streaming", False))  # 默认值 False

        api_base = credentials.get('openai_api_base')
        api_key = credentials.get('openai_api_key')
        if api_key is None:  # 只检查api_key是否为空
            raise ProviderModelCredentialNotProvidedException("OpenAI API key is required")
        # print("api_base:", api_base, api_key)
        # 初始化并返回模型
        return ChatOpenAI(
            model=self.model_id,
            temperature=temperature,
            streaming=streaming,
            base_url=api_base if api_base else None,  # 如果是空字符串则传None
            api_key=api_key
        )

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity:
        if not model.startswith("ft:"):
            base_model = model
        else:
            # get base_model
            base_model = model.split(":")[1]

        # get model schema
        base_model_schema = None
        for predefined_model in self.predefined_models():
            if base_model == predefined_model.model:
                base_model_schema = predefined_model
                break

        if not base_model_schema:
            raise ValueError(f"Base model {base_model} not found")

        base_model_schema_features = base_model_schema.features or []
        base_model_schema_model_properties = base_model_schema.model_properties
        base_model_schema_parameters_rules = base_model_schema.parameter_rules

        entity = AIModelEntity(
            model=model,
            label=I18nObject(zh_Hans=model, en_US=model),
            model_type=ModelType.LLM,
            features=list(base_model_schema_features),
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties=dict(base_model_schema_model_properties.items()),
            parameter_rules=list(base_model_schema_parameters_rules),
            pricing=base_model_schema.pricing,
        )

        return entity
