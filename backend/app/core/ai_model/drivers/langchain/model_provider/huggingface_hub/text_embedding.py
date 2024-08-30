from collections.abc import Mapping

from app import settings
from app.core.ai_model.drivers.interface.text_embedding import TextEmbeddingModel
from langchain_huggingface import HuggingFaceEmbeddings


class HuggingFaceHubTextEmbeddingModel(TextEmbeddingModel):

    def __init__(self, model_id: str):

        self.model_id = model_id

    def verify_credentials(self, model: str, credentials: Mapping) -> None:
        pass

    def get_provider_model(self) -> any:
        embeddings = HuggingFaceEmbeddings(model_name=settings.models.qa_embedding_model_name)
        # embeddings = HuggingFaceEmbeddings(model_name=self.model_id)

        return embeddings

    def run_text_embedding(self, input_text: str) -> any:
        embeddings = self.get_provider_model()