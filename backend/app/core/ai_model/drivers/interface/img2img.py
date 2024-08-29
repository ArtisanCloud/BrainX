from collections.abc import Mapping

from .ai_model import AIModel


class Img2ImgModel(AIModel):

    def verify_credentials(self, model: str, credentials: Mapping) -> None:
        raise NotImplementedError
