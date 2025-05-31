from collections.abc import Mapping

from .ai_model import AIModel


class Speech2TextModel(AIModel):

    def validate_credentials(self, credentials: Mapping) -> None:
        raise NotImplementedError

    def get_provider_model(self) -> any:
        raise NotImplementedError
