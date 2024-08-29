from enum import Enum

from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.langchain.factory import ModelProviderFactory
from app.core.ai_model.drivers.interface.model_provider import ModelProviderInterface


class LangchainModelProviderDriver:

    def __init__(self):
        self.model_provider = None

    def get_model_provider(self, provider_id: ProviderID, model_id: Enum) -> ModelProviderInterface:
        self.model_provider = ModelProviderFactory.create_text_embedding_provider(provider_id, model_id)

        return self.model_provider
