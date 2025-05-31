from abc import abstractmethod
from collections.abc import Mapping

from app.models.model_provider.provider_model import ModelType
from .ai_model import AIModel


class TextEmbeddingModel(AIModel):
    _embeddings_cache = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_type = ModelType.TEXT_EMBEDDING
        self._embeddings_cache = {}

    def validate_credentials(self, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self) -> any:
        raise NotImplementedError
