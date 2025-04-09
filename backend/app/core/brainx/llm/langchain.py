from typing import Dict, Tuple, Union

from langchain_community.chat_models import QianfanChatEndpoint, ChatCoze
from langchain_community.llms.moonshot import Moonshot
from langchain_community.llms.vllm import VLLM
from langchain_core.language_models import BaseChatModel
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from app.config.config import settings
from app.core.brainx.base import LLMModel


def get_openai_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 提取参数
    temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
    streaming = bool(params.get("streaming", False))  # 默认值 False

    # 初始化并返回模型
    return ChatOpenAI(
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )


def get_kimi_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 提取参数
    temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
    streaming = bool(params.get("streaming", False))  # 默认值 False

    # 初始化并返回模型
    return Moonshot(
        model=llm,
        temperature=temperature,
        streaming=streaming,
        base_url=settings.kimi.api_base,
        api_key=settings.kimi.api_key,
    )


def get_baidu_qianfan_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 中获取并进行处理
    temperature = float(params.get("temperature", 0))  # 默认值 0
    if temperature <= 0:
        temperature = 0.01
    if temperature > 1:
        temperature = 1

    top_p = float(params.get("top_p", 0.8))  # 默认值 0.8
    streaming = bool(params.get("streaming", False))  # 默认值 False
    request_timeout = int(params.get("request_timeout", 300))  # 默认值 300

    # 返回 QianfanChatEndpoint 实例
    return QianfanChatEndpoint(
        model=llm,
        temperature=temperature,
        top_p=top_p,
        streaming=streaming,
        request_timeout=request_timeout,
    )


def get_tencent_huyuan_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 中获取并进行处理
    temperature = float(params.get("temperature", 0))  # 默认值 0
    if temperature <= 0:
        temperature = 0.01
    if temperature > 1:
        temperature = 1

    streaming = bool(params.get("streaming", False))  # 默认值 False
    request_timeout = int(params.get("request_timeout", 300))  # 默认值 300

    # 返回 ChatOpenAI 实例
    return ChatOpenAI(
        openai_api_key=settings.tencent_hunyuan.api_key,
        openai_api_base=settings.tencent_hunyuan.api_base,
        model=llm,
        temperature=temperature,
        streaming=streaming,
        request_timeout=request_timeout,
    )

def get_deepseek_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 中获取并进行处理
    temperature = float(params.get("temperature", 0))  # 默认值 0
    if temperature < 0:
        temperature = 0
    if temperature > 1:
        temperature = 1
    streaming = bool(params.get("streaming", False))  # 默认值 False
    request_timeout = settings.deepseek.request_timeout  # 默认值 300
    # 返回 ChatOpenAI 实例
    return ChatDeepSeek(
        api_key=settings.deepseek.api_key,
        api_base=settings.deepseek.api_base,
        model=llm,
        temperature=temperature,
        streaming=streaming,
        timeout=request_timeout,
    )


def get_ollama_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 中获取并进行处理
    temperature = float(params.get("temperature", 0))  # 默认值 0
    streaming = bool(params.get("streaming", False))  # 默认值 False
    # fmt = str(params.get("format", ""))  # 默认值 ""
    # timeout = int(params.get("timeout", 300))  # 默认值 300

    # 返回 ChatOllama 实例
    return ChatOllama(
        model=llm,
        base_url=settings.ollama.url,
        keep_alive=-1,
        temperature=temperature,
        streaming=streaming,
        # format=fmt,
        # timeout=timeout,
    )


def get_llama_cpp_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 提取参数
    temperature = float(params.get("temperature", 0.5))  # 默认值 0.5
    streaming = bool(params.get("streaming", False))  # 默认值 False

    # 初始化并返回模型
    return ChatOpenAI(
        base_url=settings.llama_cpp.url,
        model=llm,
        temperature=temperature,
        streaming=streaming,
    )


def get_vllm_llm(llm: str, params: Dict[str, Union[float, bool, int, str]]):
    trust_remote_code = bool(params.get("trust_remote_code", True))
    max_new_tokens = int(params.get("max_new_tokens", 128))
    top_k = int(params.get("top_k", 10))
    top_p = float(params.get("top_p", 0.95))  # 默认值 0
    temperature = float(params.get("temperature", 0))  # 默认值 0
    return VLLM(
        model=llm,
        trust_remote_code=trust_remote_code,  # mandatory for hf models
        max_new_tokens=max_new_tokens,
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
    )


def get_chat_coze(params: Dict[str, Union[float, bool, int, str]]):
    # 从 params 获取参数
    bot_id = params.get("bot_id", settings.coze.bot_id)
    user_id = params.get("user_id", settings.coze.user_id)
    conversation_id = params.get("conversation_id", settings.coze.conversation_id)
    streaming = bool(params.get("streaming", False))
    # print(f"Bot ID: {bot_id}, User ID: {user_id}, Conversation ID: {conversation_id}")
    # print(f"Streaming: {streaming}")

    # 返回 ChatCoze 实例
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
        params: Dict[str, Union[float, bool, int, str]],
) -> Tuple[BaseChatModel | None, Exception | None]:
    try:
        # 根据模型类型动态加载实例
        match llm:
            case _ if LLMModel.is_openai_model(llm):
                mdl_llm = get_openai_llm(llm, params)

            case _ if LLMModel.is_coze_model(llm):
                mdl_llm = get_chat_coze(params)

            case _ if LLMModel.is_kimi_model(llm):
                mdl_llm = get_kimi_llm(llm, params)

            case _ if LLMModel.is_baidu_model(llm):
                mdl_llm = get_baidu_qianfan_llm(llm, params)

            case _ if LLMModel.is_tencent_hunyuan_model(llm):
                mdl_llm = get_tencent_huyuan_llm(llm, params)

            case _ if LLMModel.is_deepseek_model(llm):
                mdl_llm = get_deepseek_llm(llm, params)

            case _ if LLMModel.is_ollama_model(llm):
                mdl_llm = get_ollama_llm(llm, params)

            case _ if LLMModel.is_llama_cpp_model(llm):
                mdl_llm = get_llama_cpp_llm(llm, params)

            case _ if LLMModel.is_vllm_model(llm):
                mdl_llm = get_vllm_llm(llm, params)

            case _:
                return None, Exception(f"Unsupported LLM model: {llm}")

        return mdl_llm, None

    except Exception as e:
        return None, e
