from .base import IndexingDriverType
from .drivers.langchain.indexing import LangchainIndexer
from .drivers.llamaindex.indexing import LLamaIndexIndexer
from .interface import BaseIndexing
from ..splitter.base import BaseTextSplitter


class IndexingFactory:
    @staticmethod
    def get_indexer(indexer_type: IndexingDriverType, splitter: BaseTextSplitter) -> BaseIndexing:
        match indexer_type.value:
            # LLamaIndex are supported
            case IndexingDriverType.LLAMA_INDEX.value:
                return LLamaIndexIndexer(splitter)

            # Langchain are supported
            case IndexingDriverType.LANGCHAIN.value:
                return LangchainIndexer(splitter)

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown indexer type: {indexer_type}")
