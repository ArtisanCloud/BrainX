from collections.abc import Mapping

from .ai_model import AIModel


class Text2VideoModel(AIModel):

    def validate_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
