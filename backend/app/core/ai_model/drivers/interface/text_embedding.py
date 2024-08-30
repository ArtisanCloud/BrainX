from abc import abstractmethod
from collections.abc import Mapping

from .ai_model import AIModel


class TextEmbeddingModel(AIModel):
    @abstractmethod
    def verify_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_provider_model(self) -> any:
        raise NotImplementedError
