from langchain_community.chat_models import QianfanChatEndpoint

from app.core.brainx.base import LLMModel
from app.core.brainx.interface.llm import LLM
from typing import Mapping
from pydantic import Field


class WenXinLMM(LLM):
    model_id: str = Field(default=LLMModel.BAIDU_ERNIE_Lite_8K, description="模型 ID")

    def validate_credentials(self, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self, params: dict = None) -> any:
        # 从 params 中获取并进行处理
        temperature = float(params.get("temperature", 0))  # 默认值 0
        if temperature <= 0:
            temperature = 0.01
        if temperature > 1:
            temperature = 1

        top_p = float(params.get("top_p", 0.8))  # 默认值 0.8
        streaming = bool(params.get("streaming", False))  # 默认值 False
        request_timeout = int(params.get("request_timeout", 300))  # 默认值 300

        # 返回 QianfanChatEndpoint 实例
        return QianfanChatEndpoint(
            model=self.model_id,
            temperature=temperature,
            top_p=top_p,
            streaming=streaming,
            request_timeout=request_timeout,
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
