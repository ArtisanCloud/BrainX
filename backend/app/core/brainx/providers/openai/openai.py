from typing import Optional

from app.core.brainx.base import LLMModel
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.interface.provider import ProviderInterface


class OpenAIProvider(ProviderInterface):

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
            model_id = LLMModel.OPENAI_GPT_3_D_5_TURBO.value

        model_instance = self.get_model_type_instance(ModelType(model_type), model_id)

        # 验证凭据
        try:
            model_instance.validate_credentials(credentials)

        except Exception as e:
            return e
