from enum import Enum

from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.interface.ai_model import AIModel
from app.core.ai_model.drivers.langchain.factory import ModelProviderFactory
from app.models.model_provider.provider_model import ModelType


class LangchainModelProviderDriver:

    def __init__(self):
        self.model: AIModel

    def generate_provider_model(
            self,
            model_type: ModelType,
            provider_id: ProviderID,
            model_id: str
    ) -> any:
        match model_type.value:
            case ModelType.LLM.value:
                self.model_provider = ModelProviderFactory.create_llm_provider(provider_id, model_id)
            # case ModelType.EMBEDDING.value:
            #     self.model_provider = ModelProviderFactory.create_embedding_provider(provider_id, model_id)
            case ModelType.TEXT_EMBEDDING.value:
                self.model_provider = ModelProviderFactory.create_text_embedding_provider(provider_id, model_id)
            case ModelType.IMAGE_EMBEDDING.value:
                self.model_provider = ModelProviderFactory.create_image_embedding_provider(provider_id, model_id)
            case ModelType.RERANK.value:
                self.model_provider = ModelProviderFactory.create_rerank_provider(provider_id, model_id)
            case ModelType.SPEECH2TEXT.value:
                self.model_provider = ModelProviderFactory.create_speech2text_provider(provider_id, model_id)
            # case ModelType.MODERATION.value:
            #     self.model_provider = ModelProviderFactory.create_text_embedding_provider(provider_id, model_id)
            case ModelType.TTS.value:
                self.model_provider = ModelProviderFactory.create_tts_provider(provider_id, model_id)
            case ModelType.TEXT2IMG.value:
                self.model_provider = ModelProviderFactory.create_text2img_provider(provider_id, model_id)
            case ModelType.IMG2IMG.value:
                self.model_provider = ModelProviderFactory.create_img2img_provider(provider_id, model_id)
            case ModelType.TEXT2VIDEO.value:
                self.model_provider = ModelProviderFactory.create_text2video_provider(provider_id, model_id)
            case _:
                return None

        return self.model_provider
