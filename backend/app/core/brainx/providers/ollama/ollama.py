import logging
from decimal import Decimal
from typing import Optional

from app.core.brainx.base import LLMModel
from app.core.brainx.entity.base import I18nObject
from app.core.brainx.entity.provider_model import ModelPropertyKey, FetchFrom
from app.core.brainx.entity.runtime.provider_model import ModelType, PriceConfig, AIModelEntity
from app.core.brainx.interface.provider import ProviderInterface

logger = logging.getLogger(__name__)


class OllamaProvider(ProviderInterface):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(
            self,
            tenant_uuid: str,
            user_uuid: str,
            provider_id: str,
            credentials: dict,
            model_type: str = None,
            model_id: str = None,
    ) -> Optional[Exception]:
        # 获取LLM模型实例
        if model_type is None:
            model_type = ModelType.LLM.value
            model_id = LLMModel.OLLAMA_GEMMA_2B.value

        model_instance = self.get_model_type_instance(ModelType(model_type), model_id)

        # 验证凭据
        try:

            model_instance.validate_credentials(credentials)

        except Exception as e:
            return e

    def get_customizable_model_schema(self, model: str, credentials: dict) -> AIModelEntity:
        """
        generate custom model entities from credentials
        """
        entity = AIModelEntity(
            model=model,
            label=I18nObject(en_US=model),
            model_type=ModelType.TEXT_EMBEDDING,
            fetch_from=FetchFrom.CUSTOMIZABLE_MODEL,
            model_properties={
                ModelPropertyKey.CONTEXT_SIZE: int(credentials.get("context_size", 512)),
                ModelPropertyKey.MAX_CHUNKS: 1,
            },
            parameter_rules=[],
            pricing=PriceConfig(
                input=Decimal(credentials.get("input_price", 0)),
                unit=Decimal(credentials.get("unit", 0)),
                currency=credentials.get("currency", "USD"),
            ),
        )

        return entity
