from typing import Optional

from app.models import User, Document
from .drivers.langchain.indexing import LangchainIndexer
from .drivers.llamaindex.indexing import LLamaIndexIndexer
from .base import BaseIndexing
from .splitter.base import BaseTextSplitter
from .. import FrameworkDriverType
from ...ai_model.model_instance import ModelInstance


class IndexingFactory:
    @staticmethod
    def get_indexer(
            framework_type: FrameworkDriverType,
            splitter: BaseTextSplitter = None,
            embedding_model_instance: ModelInstance = None,
            user: Optional[User] = None,
            document: Optional[Document] = None,
    ) -> BaseIndexing:
        match framework_type.value:
            # LLamaIndex are supported
            case FrameworkDriverType.LLAMA_INDEX.value:
                return LLamaIndexIndexer(
                    user=user, document=document,
                    splitter=splitter,
                    embedding_model_instance=embedding_model_instance
                )

            # Langchain are supported
            case FrameworkDriverType.LANGCHAIN.value:
                return LangchainIndexer(
                    user=user, document=document,
                    splitter=splitter,
                    embedding_model_instance=embedding_model_instance
                )

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown indexer type: {framework_type}")
