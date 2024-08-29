from enum import Enum
from typing import Dict, Type

from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.interface.image_embedding import ImageEmbeddingModel
from app.core.ai_model.drivers.interface.img2img import Img2ImgModel
from app.core.ai_model.drivers.interface.llm import LLM
from app.core.ai_model.drivers.interface.rerank import RerankModel
from app.core.ai_model.drivers.interface.speech2text import Speech2TextModel
from app.core.ai_model.drivers.interface.text2img import Text2ImgModel
from app.core.ai_model.drivers.interface.text2video import Text2VideoModel
from app.core.ai_model.drivers.interface.text_embedding import TextEmbeddingModel
from app.core.ai_model.drivers.interface.tts import TTSModel
from app.core.ai_model.drivers.langchain.model_provider.huggingface_hub.llm import HuggingFaceHubLMM
from app.core.ai_model.drivers.langchain.model_provider.huggingface_hub.text_embedding import \
    HuggingFaceHubTextEmbeddingModel
from app.core.ai_model.drivers.langchain.model_provider.openai.llm import OpenAILMM
from app.core.ai_model.drivers.langchain.model_provider.openai.text_embedding import OpenAITextEmbeddingModel
from app.core.ai_model.drivers.langchain.model_provider.wenxin.llm import WenXinLMM


class ModelProviderFactory:
    llm_provider_map: Dict[str, Type[LLM]] = {
        ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubLMM,
        ProviderID.OPENAI.value: OpenAILMM,
        ProviderID.WENXIN.value: WenXinLMM,
        # 可以在这里继续添加其他 LLM 提供者
    }

    text_embedding_provider_map: Dict[str, Type[TextEmbeddingModel]] = {
        ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubTextEmbeddingModel,
        ProviderID.OPENAI.value: OpenAITextEmbeddingModel,
        # 可以在这里继续添加其他 Text Embedding 提供者
    }

    image_embedding_provider_map: Dict[str, Type[ImageEmbeddingModel]] = {
        # ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubImageEmbeddingModel,
        # 其他 Image Embedding 提供者
    }

    img2img_provider_map: Dict[str, Type[Img2ImgModel]] = {
        # Img2Img 提供者映射
    }

    rerank_provider_map: Dict[str, Type[RerankModel]] = {
        # Rerank 提供者映射
    }

    speech2text_provider_map: Dict[str, Type[Speech2TextModel]] = {
        # Speech2Text 提供者映射
    }

    text2img_provider_map: Dict[str, Type[Text2ImgModel]] = {
        # Text2Img 提供者映射
    }

    text2video_provider_map: Dict[str, Type[Text2VideoModel]] = {
        # Text2Video 提供者映射
    }

    tts_provider_map: Dict[str, Type[TTSModel]] = {
        # ProviderID.WENXIN.value: WenXinTTSModel,
        # 其他 TTS 提供者
    }

    @staticmethod
    def create_llm_provider(
            provider_id: ProviderID, model_id: str
    ) -> LLM:
        model_provider_class = ModelProviderFactory.llm_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported LLM provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_text_embedding_provider(provider_id: ProviderID, model_id: Enum) -> TextEmbeddingModel:
        model_provider_class = ModelProviderFactory.text_embedding_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Text Embedding provider id: {provider_id}")
        return model_provider_class(model_id)

    @staticmethod
    def create_image_embedding_provider(provider_id: ProviderID, model_id: str) -> ImageEmbeddingModel:
        model_provider_class = ModelProviderFactory.image_embedding_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Image Embedding provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_img2img_provider(provider_id: ProviderID, model_id: str) -> Img2ImgModel:
        model_provider_class = ModelProviderFactory.img2img_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Img2Img provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_rerank_provider(provider_id: ProviderID, model_id: str) -> RerankModel:
        model_provider_class = ModelProviderFactory.rerank_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Rerank provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_speech2text_provider(provider_id: ProviderID, model_id: str) -> Speech2TextModel:
        model_provider_class = ModelProviderFactory.speech2text_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Speech2Text provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_text2img_provider(provider_id: ProviderID, model_id: str) -> Text2ImgModel:
        model_provider_class = ModelProviderFactory.text2img_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Text2Img provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_text2video_provider(provider_id: ProviderID, model_id: str) -> Text2VideoModel:
        model_provider_class = ModelProviderFactory.text2video_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported Text2Video provider id: {provider_id}")
        return model_provider_class()

    @staticmethod
    def create_tts_provider(provider_id: ProviderID, model_id: str) -> TTSModel:
        model_provider_class = ModelProviderFactory.tts_provider_map.get(provider_id.value)
        if model_provider_class is None:
            raise ValueError(f"Unsupported TTS provider id: {provider_id}")
        return model_provider_class()