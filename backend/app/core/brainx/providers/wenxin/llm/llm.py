from typing import Mapping, Any

from langchain_community.chat_models import QianfanChatEndpoint
from pydantic import Field

from app.core.brainx.base import LLMModel
from app.core.brainx.interface.llm import LLM
from app.core.exception.exceptions import ProviderModelCredentialNotProvidedException


class WenXinLLM(LLM):
    model_id: str = Field(default=LLMModel.BAIDU_ERNIE_Lite_8K, description="模型 ID")

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
        if not credentials:
            raise ProviderModelCredentialNotProvidedException()

        temperature = float(params.get("temperature", 0))  # 默认值 0
        if temperature <= 0:
            temperature = 0.01
        if temperature > 1:
            temperature = 1

        top_p = float(params.get("top_p", 0.8))  # 默认值 0.8
        streaming = bool(params.get("streaming", False))  # 默认值 False
        request_timeout = int(params.get("request_timeout", 300))  # 默认值 300

        secret_key = credentials.get('secret_key')
        api_key = credentials.get('openai_api_key')
        if api_key is None:  # 只检查api_key是否为空
            raise ProviderModelCredentialNotProvidedException("OpenAI API key is required")

        # 返回 QianfanChatEndpoint 实例
        return QianfanChatEndpoint(
            model=self.model_id,
            api_key=api_key,
            secret_key=secret_key,
            temperature=temperature,
            top_p=top_p,
            streaming=streaming,
            request_timeout=request_timeout,
        )
