from typing import Optional

from .drivers.langchain.retriever import LangchainRetriever
from .drivers.llamaindex.retriever import LlamaIndexRetriever
from .interface import BaseRetriever
from .. import FrameworkDriverType
from ..vector_store.interface import  VectorStoreDriver
from ...ai_model.model_instance import ModelInstance


class RetrieverFactory:
    @staticmethod
    def get_retriever(framework_type: FrameworkDriverType,
                      vector_store_driver: VectorStoreDriver = None,
                      collection_name: str = "embeddings",
                      embedding_model_instance: Optional[ModelInstance] = None,
                      ) -> BaseRetriever:

        match framework_type.value:
            # LlamaIndex are supported
            case FrameworkDriverType.LLAMA_INDEX.value:
                return LlamaIndexRetriever()

            # Langchain are supported
            case FrameworkDriverType.LANGCHAIN.value:
                return LangchainRetriever(
                    vector_store_driver=vector_store_driver,
                    # vector_store为空，则需要传入初始化一个vector store的参数
                    collection_name=collection_name, embedding_model_instance=embedding_model_instance
                )

            # Other types are not supported
            case _:
                raise ValueError(f"Unknown retriever type: {framework_type.value}")
