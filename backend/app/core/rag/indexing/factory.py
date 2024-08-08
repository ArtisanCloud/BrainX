from typing import Type

from app.models.rag.dataset import IndexingDriverType
from .drivers.langchain.indexing import LangchainIndexer
from .drivers.llamaindex.indexing import LLamaIndexIndexer
from .interface import IndexingInterface


class IndexingFactory:
    @staticmethod
    def get_indexer(indexer_type: str) -> IndexingInterface:
        match indexer_type:
            # LLamaIndex are supported
            case IndexingDriverType.LLAMA_INDEX:
                return LLamaIndexIndexer()

            # Langchain are supported
            case IndexingDriverType.LANGCHAIN:
                return LangchainIndexer()

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown indexer type: {indexer_type}")
