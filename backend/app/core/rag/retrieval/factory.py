from typing import Type

from .base import RetrieverDriverType
from .drivers.langchain.retriever import LangchainRetriever
from .drivers.llamaindex.retriever import LLamaIndexRetriever
from .interface import BaseRetriever


class RetrieverFactory:
    @staticmethod
    def get_retriever(retriever_type: str) -> BaseRetriever:
        match retriever_type:
            # LLamaIndex are supported
            case RetrieverDriverType.LLAMA_INDEX:
                return LLamaIndexRetriever()

            # Langchain are supported
            case RetrieverDriverType.LANGCHAIN:
                return LangchainRetriever()

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown retriever type: {retriever_type}")
