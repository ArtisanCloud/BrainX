from sentence_transformers import SentenceTransformer
from transformers import ViltProcessor, ViltForQuestionAnswering

from app.config.config import settings
from enum import Enum


class LLMModel(Enum):
    OPENAI_GPT_3_D_5_TURBO = 'gpt-3.5-turbo'
    BAIDU_ERNIE_BOT_TURBO = 'ERNIE-Bot-turbo'
    BAIDU_ERNIE_4_D_0_8K = 'ERNIE-4.0-8K'
    BAIDU_ERNIE_3_D_5_8K = 'ERNIE-3.5-8K'
    BAIDU_ERNIE_Speed_128K = 'ERNIE-Speed-128K'
    BAIDU_ERNIE_Lite_8K = 'ERNIE-Lite-8K'
    BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED = 'Qianfan-BLOOMZ-7B-compressed'
    KIMI_MOONSHOT_V1_8K = 'moonshot-v1-8k'
    KIMI_MOONSHOT_V1_32K = 'moonshot-v1-32k'
    KIMI_MOONSHOT_V1_128K = 'moonshot-v1-128k'
    OLLAMA_13B_ALPACA_16K = '13B-alpaca-16k:latest'
    OLLAMA_GEMMA_2B = 'gemma:2b'
    OLLAMA_GEMMA_7B = 'gemma:7b'
    OLLAMA_LLAMA3_2 = 'llama3.2'
    OLLAMA_LLAMA3_2_VISION = 'llama3.2-vision'
    OLLAMA_QWEN_2_5 = 'qwen2.5'
    OLLAMA_QWEN_CODER_2_5 = 'qwen2.5-coder'

    @classmethod
    def is_baidu_model(cls, llm: str) -> bool:
        """判断是否为百度模型"""
        return any(
            llm == model.value for model in cls 
            if model.name.startswith('BAIDU_')
        )

    @classmethod
    def is_openai_model(cls, llm: str) -> bool:
        """判断是否为OpenAI模型"""
        return any(
            llm == model.value for model in cls 
            if model.name.startswith('OPENAI_')
        )

    @classmethod
    def is_kimi_model(cls, llm: str) -> bool:
        """判断是否为Kimi模型"""
        return any(
            llm == model.value for model in cls 
            if model.name.startswith('KIMI_')
        )
    
    @classmethod
    def is_ollama_model(cls, llm: str) -> bool:
        """判断是否为Ollama模型"""
        return any(
            llm == model.value for model in cls 
            if model.name.startswith('OLLAMA_')
        )

    @classmethod
    def get_model_brand(cls, llm: str) -> str:
        """获取模型的品牌"""
        for model in cls:
            if model.value == llm:
                brand = model.name.split('_')[0]
                return brand
        return "UNKNOWN"

    @classmethod
    def is_same_brand(cls, llm1: str, llm2: str) -> bool:
        """判断两个模型是否属于同一品牌"""
        return cls.get_model_brand(llm1) == cls.get_model_brand(llm2)
    
class VisualQueryModelSingleton:
    _instance_processor = None
    _instance_model = None

    def __new__(cls):
        if cls._instance_processor is None:
            cls._instance_processor = ViltProcessor.from_pretrained(settings.models.visual_query_model_name)

        if cls._instance_model is None:
            cls._instance_model = ViltForQuestionAnswering.from_pretrained(settings.models.visual_query_model_name)

        return cls._instance_processor, cls._instance_model


class VisualSearchModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.models.visual_search_model_name)
        return cls._instance


def get_visual_search_embedding_model() -> SentenceTransformer:
    return VisualSearchModelSingleton()


def get_visual_query_embedding_model():
    return VisualQueryModelSingleton()
