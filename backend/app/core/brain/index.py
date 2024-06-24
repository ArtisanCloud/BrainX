from sentence_transformers import SentenceTransformer
from transformers import ViltProcessor, ViltForQuestionAnswering

from app.core.config import settings
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
    OLLAMA_13B_ALPACA_16K = '13B-alpaca-16k:latest'
    OLLAMA_GEMMA_2B = 'gemma:2b'


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


def get_visual_search_embedding_model():
    return VisualSearchModelSingleton()


def get_visual_query_embedding_model():
    return VisualQueryModelSingleton()
