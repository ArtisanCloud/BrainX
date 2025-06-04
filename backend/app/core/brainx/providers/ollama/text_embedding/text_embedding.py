from typing import Mapping

from pydantic import Field

from app.core.brainx.interface.text_embedding import TextEmbeddingModel


class OllamaTextEmbeddingModel(TextEmbeddingModel):
    model_id: str = Field(default="", description="模型 ID")
    """
    Model class for Ollama large language model.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_credentials(self, credentials: Mapping) -> None:
        llm = self.get_provider_model({
            "credentials": credentials,
            "streaming": False,
        })

        llm.invoke("ping")
