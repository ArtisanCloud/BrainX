from collections.abc import Mapping

from .ai_model import AIModel


class Speech2TextModel(AIModel):

    def verify_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
