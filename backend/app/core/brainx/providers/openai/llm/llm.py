from typing import Mapping

from langchain_openai import ChatOpenAI
from pydantic import Field

from app.core.brainx.base import LLMModel
from app.core.brainx.interface.llm import LLM


class OpenAILMM(LLM):
    model_id: str = Field(default=LLMModel.OPENAI_GPT_3_D_5_TURBO, description="模型 ID")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self, params: dict = None) -> any:
        # 从 params 提取参数
        temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
        streaming = bool(params.get("streaming", False))  # 默认值 False

        # 初始化并返回模型
        return ChatOpenAI(
            model=self.model_id,
            temperature=temperature,
            streaming=streaming,
        )
