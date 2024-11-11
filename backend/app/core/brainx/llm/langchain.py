from typing import Tuple

from langchain_community.chat_models import ChatOpenAI, QianfanChatEndpoint
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from app.config.config import settings
from app.core.brainx.base import LLMModel


def get_openai_llm(llm: str, temperature: float, streaming: bool):
    return ChatOpenAI(
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )


def get_kimi_llm(llm: str, temperature: float, streaming: bool):
    return ChatOpenAI(
        model=llm,
        temperature=temperature,
        streaming=streaming,
        base_url=settings.kimi.api_base,
        api_key=settings.kimi.api_key,
    )


def get_baidu_qianfan_llm(llm: str, temperature: float, streaming: bool):
    if temperature <= 0:
        temperature = 0.1
    if temperature > 1:
        temperature = 1

    return QianfanChatEndpoint(
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )


def get_ollama_llm(llm: str, temperature: float, streaming: bool):
    # print(settings.ollama.url)

    return ChatOllama(
        model=llm,
        base_url=settings.ollama.url,
        keep_alive=-1,
        temperature=temperature,
        streaming=streaming,
    )


def get_llm(
    llm: str, temperature: float = 0.5, streaming: bool = False
) -> Tuple[BaseChatModel, Exception | None]:
    match llm:
        case LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
            mdl_llm = get_openai_llm(llm, temperature=temperature, streaming=streaming)

        case LLMModel.KIMI_MOONSHOT_V1_8K.value:
            mdl_llm = get_kimi_llm(llm, temperature=temperature, streaming=streaming)

        case (
            LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value
            | LLMModel.BAIDU_ERNIE_3_D_5_8K.value
            | LLMModel.BAIDU_ERNIE_4_D_0_8K.value
            | LLMModel.BAIDU_ERNIE_Speed_128K.value
            | LLMModel.BAIDU_ERNIE_Lite_8K.value
        ):
            mdl_llm = get_baidu_qianfan_llm(
                llm, temperature=temperature, streaming=streaming
            )

        case (
            LLMModel.OLLAMA_13B_ALPACA_16K.value
            | LLMModel.OLLAMA_GEMMA_2B.value
            | LLMModel.OLLAMA_GEMMA_7B.value
            | LLMModel.OLLAMA_LLAMA3_2.value
        ):
            mdl_llm = get_ollama_llm(llm, temperature=temperature, streaming=streaming)
        case _:
            return None, Exception(f"Unsupported LLM model: {llm}")

    return mdl_llm, None
