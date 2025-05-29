from typing import Optional

from .drivers.langchain.retriever import LangchainRetriever
from .interface import BaseRetriever
from ..vector_store.interface import VectorStoreDriver
from ...brainx.model_instance import ModelInstance
from app.config.config import settings


class RetrieverFactory:
    @staticmethod
    def get_retriever(vector_store_driver: VectorStoreDriver = None,
                      collection_name: str = settings.agent.vector_store_collection,
                      embedding_model_instance: Optional[ModelInstance] = None,
                      ) -> BaseRetriever:
        return LangchainRetriever(
            vector_store_driver=vector_store_driver,
            # vector_store为空，则需要传入初始化一个vector store的参数
            collection_name=collection_name, embedding_model_instance=embedding_model_instance
        )
