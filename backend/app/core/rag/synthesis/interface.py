from abc import ABC, abstractmethod
from typing import Any, Optional, List, Iterator, Tuple, Dict

from app.core.brainx.base import LLMModel
from app.core.brainx.llm.langchain import get_openai_llm, get_kimi_llm, get_baidu_qianfan_llm
from app.core.brainx.llm.llamaindex import get_ollama_llm
from app.models import App
from app.models.rag.invoke_response import InvokeResponse


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

    @abstractmethod
    def get_llm(self, temperature: float = 0.5, streaming: bool = False) -> Tuple[Any, Exception | None]:
        raise NotImplementedError


    @abstractmethod
    def stream(self, query: Any,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def invoke(self, query: Any,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               output_schemas: Any = None,
               **kwargs: Any) -> Tuple[Any | None, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def chat_completion(self,
                        question: Any,
                        temperature: float = 0.5,
                        app: App = None,
                        session_id: str = "",
                        **kwargs: Any) -> Tuple[str, Exception | None]:

        raise NotImplementedError

    @abstractmethod
    def chat_stream(self,
                    question: Any,
                    temperature: float = 0.5,
                    app: App = None,
                    session_id: str = "",
                    **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        raise NotImplementedError
