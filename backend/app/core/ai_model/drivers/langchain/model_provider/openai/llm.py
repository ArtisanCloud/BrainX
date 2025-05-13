from typing import Mapping

from app.core.ai_model.drivers.interface.llm import LLM


class OpenAILMM(LLM):
    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
