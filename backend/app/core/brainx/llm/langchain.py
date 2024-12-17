from typing import Tuple

from langchain_community.chat_models import QianfanChatEndpoint, ChatCoze
from langchain_community.llms.moonshot import Moonshot
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
    return Moonshot(
        model=llm,
        temperature=temperature,
        streaming=streaming,
        base_url=settings.kimi.api_base,
        api_key=settings.kimi.api_key,
    )


def get_baidu_qianfan_llm(
    llm: str, temperature: float, streaming: bool, request_timeout: int = 300
):
    if temperature <= 0:
        temperature = 0.1
    if temperature > 1:
        temperature = 1

    return QianfanChatEndpoint(
        model=llm,
        temperature=temperature,
        streaming=streaming,
        request_timeout=request_timeout,
    )


def get_tencent_huyuan_llm(
    llm: str, temperature: float, streaming: bool, request_timeout: int = 300
):
    if temperature <= 0:
        temperature = 0.1
    if temperature > 1:
        temperature = 1

    return ChatOpenAI(
        openai_api_key=settings.tencent_hunyuan.api_key,
        openai_api_base=settings.tencent_hunyuan.api_base,
        model=llm,
        temperature=temperature,
        streaming=streaming,
        request_timeout=request_timeout,
    )


def get_ollama_llm(llm: str, temperature: float, streaming: bool, format: str = ""):
    # print(settings.ollama.url)

    return ChatOllama(
        model=llm,
        base_url=settings.ollama.url,
        keep_alive=-1,
        temperature=temperature,
        streaming=streaming,
        format=format,
    )


def get_chat_coze(
    bot_id: str,
    user_id: str,
    conversation_id: str,
    streaming: bool = False,
):
    # print(settings.ollama.url)

    return ChatCoze(
        coze_api_base=settings.coze.api_base,
        coze_api_key=settings.coze.api_key,
        bot_id=bot_id,
        user=user_id,
        conversation_id=conversation_id,
        streaming=streaming,
    )


def get_llm(
    llm: str,
    temperature: float = 0.5,
    streaming: bool = False,
    format: str = "",
    request_timeout: int = 300,
) -> Tuple[BaseChatModel, Exception | None]:
    match llm:
        case _ if LLMModel.is_openai_model(llm):
            mdl_llm = get_openai_llm(llm, temperature=temperature, streaming=streaming)

        case _ if LLMModel.is_kimi_model(llm):
            mdl_llm = get_kimi_llm(llm, temperature=temperature, streaming=streaming)

        case _ if LLMModel.is_baidu_model(llm):
            mdl_llm = get_baidu_qianfan_llm(
                llm,
                temperature=temperature,
                streaming=streaming,
                request_timeout=request_timeout,
            )
        case _ if LLMModel.is_tencent_hunyuan_model(llm):
            mdl_llm = get_tencent_huyuan_llm(
                llm,
                temperature=temperature,
                streaming=streaming,
                request_timeout=request_timeout,
            )

        case _ if LLMModel.is_ollama_model(llm):
            mdl_llm = get_ollama_llm(
                llm, temperature=temperature, streaming=streaming, format=format
            )

        case _:
            return None, Exception(f"Unsupported LLM model: {llm}")

    return mdl_llm, None


