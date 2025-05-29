from typing import Mapping

from langchain_openai import ChatOpenAI

from app.core.brainx.interface.llm import LLM


class OpenAILMM(LLM):
    model: str

    def __init__(self, model: str = 'gpt-3.5-turbo'):
        self.model = model

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self, params: dict = None) -> any:
        # 从 params 提取参数
        temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
        streaming = bool(params.get("streaming", False))  # 默认值 False

        # 初始化并返回模型
        return ChatOpenAI(
            model=self.model,
            temperature=temperature,
            streaming=streaming,
        )
