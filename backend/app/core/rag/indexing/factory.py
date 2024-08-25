from typing import Optional

from app.models import User, Document
from .base import IndexingDriverType
from .drivers.langchain.indexing import LangchainIndexer
from .drivers.llamaindex.indexing import LLamaIndexIndexer
from .base import BaseIndexing
from .splitter.base import BaseTextSplitter


class IndexingFactory:
    @staticmethod
    def get_indexer(
            indexer_type: IndexingDriverType, splitter: BaseTextSplitter,
            user: Optional[User] = None,
            document: Optional[Document] = None,
    ) -> BaseIndexing:
        match indexer_type.value:
            # LLamaIndex are supported
            case IndexingDriverType.LLAMA_INDEX.value:
                return LLamaIndexIndexer(user=user, document=document, splitter=splitter)

            # Langchain are supported
            case IndexingDriverType.LANGCHAIN.value:
                return LangchainIndexer(user=user, document=document, splitter=splitter)

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown indexer type: {indexer_type}")
