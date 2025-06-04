from typing import Dict, Type

from app.constant.ai_model.provider import ProviderID, ModelID
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.core.brainx.interface.ai_model import AIModel
from app.core.brainx.interface.image_embedding import ImageEmbeddingModel
from app.core.brainx.interface.img2img import Img2ImgModel
from app.core.brainx.interface.llm import LLM
from app.core.brainx.interface.rerank import RerankModel
from app.core.brainx.interface.speech2text import Speech2TextModel
from app.core.brainx.interface.text2img import Text2ImgModel
from app.core.brainx.interface.text2video import Text2VideoModel
from app.core.brainx.interface.text_embedding import TextEmbeddingModel
from app.core.brainx.interface.tts import TTSModel
from app.core.brainx.providers.huggingface_hub.llm.llm import HuggingFaceHubLMM
from app.core.brainx.providers.huggingface_hub.text_embedding.text_embedding import HuggingFaceHubTextEmbeddingModel
from app.core.brainx.providers.openai.llm.llm import OpenAILMM
from app.core.brainx.providers.openai.text_embedding.text_embedding import OpenAITextEmbeddingModel
from app.core.brainx.providers.wenxin.llm.llm import WenXinLLM
from app.core.brainx.providers.ollama.llm.llm import OllamaLLM
from app.core.brainx.providers.ollama.text_embedding.text_embedding import OllamaTextEmbeddingModel


class ProviderModelFactory:
    tenant_uuid: str

    _provider_model_map: Dict[str, Type[LLM]] = {
        ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubLMM,
        ProviderID.OPENAI.value: OpenAILMM,
        ProviderID.WENXIN.value: WenXinLLM,
        ProviderID.OLLAMA.value: OllamaLLM,
        # 可以在这里继续添加其他 LLM 提供者
    }

    text_embedding_provider_map: Dict[str, Type[TextEmbeddingModel]] = {
        ProviderID.HUGGINGFACE_HUB.value: HuggingFaceHubTextEmbeddingModel,
        ProviderID.OPENAI.value: OpenAITextEmbeddingModel,
        ProviderID.OLLAMA.value: OllamaTextEmbeddingModel,
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

    def __init__(self, tenant_uuid: str):
        self.tenant_uuid = tenant_uuid

    def get_model_type_instance(self, model_type: ModelType, provider_id: str, model_id: str) -> AIModel:

        provider_id = ProviderID(provider_id)

        init_params = {
            "tenant_uuid": self.tenant_uuid,
            "provider_id": provider_id,
            "provider_name": provider_id,
            "model_type": model_type,
            "model_id": model_id,
            # "plugin_model_provider": self.get_plugin_model_provider(provider),
        }

        if model_type == ModelType.LLM:
            return self.create_llm_provider(**init_params)
        elif model_type == ModelType.TEXT_EMBEDDING:
            return self.create_text_embedding_provider(**init_params)
        elif model_type == ModelType.RERANK:
            return self.create_rerank_provider(**init_params)
        elif model_type == ModelType.SPEECH2TEXT:
            return self.create_speech2text_provider(**init_params)
        elif model_type == ModelType.TEXT2VIDEO:
            return self.create_text2video_provider(**init_params)
        elif model_type == ModelType.TTS:
            return self.create_tts_provider(**init_params)
        else:
            raise ValueError(f'Unsupported model type: {model_type}')

    @staticmethod
    def create_llm_provider(**kwargs) -> LLM:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory._provider_model_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported LLM provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_text_embedding_provider(**kwargs) -> TextEmbeddingModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.text_embedding_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Text Embedding provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_image_embedding_provider(**kwargs) -> ImageEmbeddingModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.image_embedding_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Image Embedding provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_img2img_provider(**kwargs) -> Img2ImgModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.img2img_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Img2Img provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_rerank_provider(**kwargs) -> RerankModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.rerank_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Rerank provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_speech2text_provider(**kwargs) -> Speech2TextModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.speech2text_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Speech2Text provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_text2img_provider(**kwargs) -> Text2ImgModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.text2img_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Text2Img provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_text2video_provider(**kwargs) -> Text2VideoModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.text2video_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported Text2Video provider id: {provider_id}")
        return provider_model_class(**kwargs)

    @staticmethod
    def create_tts_provider(**kwargs) -> TTSModel:
        provider_id = kwargs.get("provider_id")
        provider_model_class = ProviderModelFactory.tts_provider_map.get(provider_id.value)
        if provider_model_class is None:
            raise ValueError(f"Unsupported TTS provider id: {provider_id}")
        return provider_model_class(**kwargs)
