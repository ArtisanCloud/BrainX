from abc import ABC, abstractmethod
from typing import Any, Optional, List, Iterator, Tuple

from app.core.brain.base import LLMModel
from app.core.brain.llm.langchain import get_openai_llm, get_kimi_llm, get_baidu_qianfan_llm
from app.core.brain.llm.llamaindex import get_ollama_llm
from app.models import App


class BaseAgentExecutor(ABC):

    def __init__(self, llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 **kwargs):

        self.llm = llm
        self.temperature = temperature
        self.streaming = streaming

    """
    Define the interface for an AgentExecutor responsible for handling LLM tasks such as
    completion, streaming, chat-based interactions, and other agent-related operations.
    """

    def get_llm(self, temperature: float = 0.5, streaming: bool = False) -> Tuple[Any, Exception | None]:
        match self.llm:
            case LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
                mdl_llm = get_openai_llm(self.llm, temperature=temperature, streaming=streaming)

            case LLMModel.KIMI_MOONSHOT_V1_8K.value:
                mdl_llm = get_kimi_llm(self.llm, temperature=temperature, streaming=streaming)

            case (
            LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value |
            LLMModel.BAIDU_ERNIE_3_D_5_8K.value |
            LLMModel.BAIDU_ERNIE_4_D_0_8K.value |
            LLMModel.BAIDU_ERNIE_Speed_128K.value |
            LLMModel.BAIDU_ERNIE_Lite_8K.value
            ):
                mdl_llm = get_baidu_qianfan_llm(self.llm, temperature=temperature, streaming=streaming)

            case (LLMModel.OLLAMA_13B_ALPACA_16K.value | LLMModel.OLLAMA_GEMMA_2B.value):
                mdl_llm = get_ollama_llm(self.llm, temperature=temperature, streaming=streaming)
            case _:
                return None, Exception(f"Unsupported LLM model: {self.llm}")

        # print("query llm:", mdl_llm)

        return mdl_llm, None

    @abstractmethod
    def invoke(self, query: str, temperature: float = 0.5, config: Optional[Any] = None, **kwargs: Any) -> str:

        raise NotImplementedError

    @abstractmethod
    def stream(self, query: str,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def completion(self, query: str,
                   temperature: float = 0.5,
                   input_variables=list[str], template: str = '',
                   **kwargs: Any) -> Tuple[Any | None, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def chat_completion(self,
                        question: str,
                        temperature: float = 0.5,
                        app: App = None,
                        session_id: str = "",
                        **kwargs: Any) -> Tuple[str, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def chat_stream(self,
                    question: str,
                    temperature: float = 0.5,
                    app: App = None,
                    session_id: str = "",
                    **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        raise NotImplementedError
