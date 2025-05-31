from typing import Mapping, Any

from langchain_openai import ChatOpenAI
from pydantic import Field

from app.core.brainx.base import LLMModel
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
        temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
        streaming = bool(params.get("streaming", False))  # 默认值 False

        if not credentials:
            raise ProviderModelCredentialNotProvidedException()

        api_base = credentials.get('openai_api_base')
        api_key = credentials.get('openai_api_key')
        if api_key is None:  # 只检查api_key是否为空
            raise ProviderModelCredentialNotProvidedException("OpenAI API key is required")

        # 初始化并返回模型
        return ChatOpenAI(
            model=self.model_id,
            temperature=temperature,
            streaming=streaming,
            base_url=api_base if api_base else None,  # 如果是空字符串则传None
            api_key=api_key
        )
