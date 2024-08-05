from langchain_community.chat_models import ChatOpenAI, QianfanChatEndpoint
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

from app.config.config import settings


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
    return QianfanChatEndpoint(
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )


def get_ollama_llm(llm: str, temperature: float, streaming: bool):
    # print(settings.ollama.url)
    return Ollama(
        model=llm,
        base_url=settings.ollama.url,
        keep_alive=-1,
        temperature=temperature,
    )
