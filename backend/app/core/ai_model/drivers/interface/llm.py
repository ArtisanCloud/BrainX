from abc import abstractmethod
from collections.abc import Mapping

from .ai_model import AIModel


class LLM(AIModel):

    @abstractmethod
    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
