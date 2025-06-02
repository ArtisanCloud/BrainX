from typing import Optional

from app.core.brainx.base import LLMModel
from app.core.brainx.interface.provider import ProviderInterface
from app.models.model_provider.provider_model import ModelType


class OpenAIProvider(ProviderInterface):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_provider_credentials(self, credentials: dict) -> Optional[Exception]:
        # 获取LLM模型实例
        model_instance = self.get_model_type_instance(ModelType.LLM, LLMModel.OPENAI_GPT_3_D_5_TURBO.value)

        # 验证凭据
        try:
            model_instance.validate_credentials(credentials)

        except Exception as e:
            return e
