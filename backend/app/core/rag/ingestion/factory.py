from typing import Optional

from app.models import User, Document
from .drivers.langchain.indexing import LangchainIndexer
from .interface import BaseIndexing
from .splitter.base import BaseTextSplitter
from ...brainx.model_instance import ModelInstance


class IndexingFactory:
    @staticmethod
    def get_indexer(
            splitter: BaseTextSplitter = None,
            embedding_model_instance: ModelInstance = None,
            user: Optional[User] = None,
            document: Optional[Document] = None,
    ) -> BaseIndexing:
        return LangchainIndexer(
            user=user, document=document,
            splitter=splitter,
            embedding_model_instance=embedding_model_instance
        )
