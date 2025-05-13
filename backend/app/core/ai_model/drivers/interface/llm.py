from abc import abstractmethod
from collections.abc import Mapping

from .ai_model import AIModel


class LLM(AIModel):

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self) -> any:
        raise NotImplementedError
