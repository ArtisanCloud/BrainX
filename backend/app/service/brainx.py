from typing import Tuple, Iterator, Any, List, Type, Dict

from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.langchain.factory import ModelProviderFactory
from app.core.ai_model.model_instance import ModelInstance
from app.config.config import settings
from app.core.rag import FrameworkDriverType
from app.core.rag.synthesis.factory import AgentExecutorFactory
from app.core.rag.ingestion.factory import IndexingFactory
from app.core.rag.retrieval.factory import RetrieverFactory
from app.core.rag.retrieval.interface import BaseRetriever
from app.models.app.app import App
from app.models.rag.document_node import DocumentNode
from app.models.rag.retrievial_response import RetrievalResponse


class BrainXService:
    def __init__(self,
                 llm: str,
                 streaming: bool = False,
                 collection_name: str = "rag_embeddings",
                 table_name: str = "embeddings",
                 ):

        # 进行其他初始化操作
        # create the embedding model
        embedding_model_instance = self._create_embedding_model()

        # define the ingestion
        self.indexer = self._create_indexer(embedding_model_instance)

        # define the retriever
        self.retriever = self._create_retriever(collection_name, embedding_model_instance)

        # get the vector store
        self.vector_store = self.retriever.get_vector_store()

        # define the Agent Bot
        self.AgentBot = None

        # define the agent executor
        self.agent_executor = self._create_agent_executor(llm=llm, streaming=streaming)

    @staticmethod
    def _create_embedding_model():
        text_embedding_model = ModelProviderFactory.create_text_embedding_provider(ProviderID.HUGGINGFACE_HUB,
                                                                                   HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value)
        embedding_model_instance = ModelInstance(
            model=text_embedding_model
        )
        return embedding_model_instance

    @staticmethod
    def _create_indexer(embedding_model_instance: ModelInstance = None):
        return IndexingFactory.get_indexer(
            FrameworkDriverType(settings.agent.framework_driver),
            None, embedding_model_instance,
            None, None,
        )

    @staticmethod
    def _create_retriever(collection_name: str, embedding_model_instance: ModelInstance = None) -> BaseRetriever:
        return RetrieverFactory.get_retriever(
            FrameworkDriverType(settings.agent.framework_driver),
            collection_name=collection_name,
            embedding_model_instance=embedding_model_instance
        )

    @staticmethod
    def _create_agent_executor(
            llm: str,
            temperature: float = 0.5,
            streaming: bool = False,
    ):
        return AgentExecutorFactory.get_agent_executor(
            FrameworkDriverType(settings.agent.framework_driver),
            llm, temperature=temperature, streaming=streaming
        )

    def bind_llm(self, llm: str):
        self.llm = llm
        return self

    def set_streaming(self, streaming: bool):
        self.streaming = streaming
        return self

    async def retrieve(self, content: str, top_k: int, score_threshold: float, filters: dict = None) -> Tuple[
        List[DocumentNode] | None, Exception | None]:
        return self.retriever.retrieve(content, top_k, score_threshold, filters)

    def stream(
            self,
            query: Dict,
            temperature: float = 0.5,
            input_variables=list[str],
            template: str = ''
    ) -> Tuple[Iterator | None, Exception | None]:
        return self.agent_executor.stream(query, temperature=temperature, input_variables=input_variables,
                                          template=template)

    def complete(self,
                 query: Dict,
                 temperature: float = 0.5,
                 input_variables=list[str],
                 template: str = '',
                 ) -> Tuple[RetrievalResponse | None, Exception | None]:
        return self.agent_executor.completion(query, temperature=temperature, input_variables=input_variables,
                                              template=template)


    def chat_completion(self,
                        query: Dict,
                        temperature: float = 0.5,
                        app: App = None,
                        session_id: str = "",
                        ) -> Tuple[str | None, Exception | None]:
        return self.agent_executor.chat_completion(query, app=app, session_id=session_id, temperature=temperature)

    def chat_stream(self,
                    query: Dict,
                    temperature: float = 0.5,
                    app: App = None,
                    session_id: str = ""
                    ) -> Tuple[Iterator | None, Exception | None]:
        return self.agent_executor.chat_stream(query, app=app, session_id=session_id, temperature=temperature)
