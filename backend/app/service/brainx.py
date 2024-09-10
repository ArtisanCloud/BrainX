from typing import Tuple, Iterator, Any, List, Type
import uuid

from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import Output, Input
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.indices.vector_store import VectorIndexRetriever

from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.provider import ProviderID
from app.core.ai_model.drivers.langchain.factory import ModelProviderFactory
from app.core.ai_model.model_instance import ModelInstance
from app.core.brain.chat.app import get_chat_prompt_template
from app.core.brain.base import LLMModel
from app.core.brain.indexing.engine import generate_storage_context, get_service_context
from app.core.brain.llm.langchain import get_openai_llm, get_baidu_qianfan_llm, get_ollama_llm, get_kimi_llm
from app.config.config import settings
from app.core.rag import FrameworkDriverType
from app.core.rag.agent_executor.factory import AgentExecutorFactory
from app.core.rag.indexing.factory import IndexingFactory
from app.core.rag.retriever.factory import RetrieverFactory
from app.core.rag.retriever.interface import BaseRetriever
from app.models.app.app import App
from app.models.rag.document_node import DocumentNode


class BrainXService:
    def __init__(self,
                 llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 chat_history_cls: Type[ChatMessageHistory] = RedisChatMessageHistory,  # ChatMessageHistory 动态驱动
                 chat_history_kwargs: dict = {},  # 传递给 ChatMessageHistory 的其他参数
                 collection_name: str = "rag_embeddings",
                 table_name: str = "embeddings",
                 ):

        self.chat_history_cls = chat_history_cls
        self.chat_history_kwargs = chat_history_kwargs

        # 进行其他初始化操作
        # create the embedding model
        embedding_model_instance = self._create_embedding_model()

        # define the indexing
        self.indexer = self._create_indexer(embedding_model_instance)

        # define the retriever
        self.retriever = self._create_retriever(collection_name, embedding_model_instance)
        self.vector_store = self.retriever.get_vector_store()

        # define the Agent Bot
        self.AgentBot = None

        # define the agent executor
        self.agent_executor = self._create_agent_executor()

    def _create_embedding_model(self):
        model_provider = ModelProviderFactory.create_text_embedding_provider(ProviderID.HUGGINGFACE_HUB,
                                                                             HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value)
        model = model_provider.get_provider_model()
        embedding_model_instance = ModelInstance(
            model=model
        )
        return embedding_model_instance

    def _create_indexer(self, embedding_model_instance: ModelInstance = None):
        return IndexingFactory.get_indexer(
            FrameworkDriverType(settings.agent.framework_driver),
            None, embedding_model_instance,
            None, None,
        )

    def _create_retriever(self, collection_name: str, embedding_model_instance: ModelInstance = None) -> BaseRetriever:
        return RetrieverFactory.get_retriever(
            settings.agent.framework_driver,
            collection_name=collection_name,
            embedding_model_instance=embedding_model_instance
        )

    def _create_agent_executor(self,
                               llm: str,
                               temperature: float = 0.5,
                               streaming: bool = False,
                               ):

        return AgentExecutorFactory.get_agent_executor(
            FrameworkDriverType(settings.agent.framework_driver),
            llm, temperature, streaming
        )

    def bind_llm(self, llm: str):
        self.llm = llm
        return self

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        return self

    def set_streaming(self, streaming: bool):
        self.streaming = streaming
        return self

    async def retrieve(self, content: str, top_k: int, filters: dict = None) -> Tuple[
        List[DocumentNode] | None, Exception | None]:
        return self.retriever.retrieve(content, top_k, filters)


    def stream(
            self,
            inputs: str,
            input_variables=list[str],
            template: str = ''
    ) -> Tuple[Output | None, Exception | None]:
        return self.agent_executor.stream(inputs, input_variables, template)

    def complete(self,
                 inputs: Input,
                 input_variables=list[str],
                 template: str = ''
                 ) -> Tuple[Any | None, Exception | None]:
        return self.agent_executor.completion(inputs, input_variables, template)


    def generate_session_id(self) -> str:
        """生成会话ID"""
        return str(uuid.uuid4())

    def get_chat_history(self, session_id: str) -> ChatMessageHistory:
        return self.chat_history_cls(session_id=session_id, **self.chat_history_kwargs)

    def chat_completion(self,
                        question: str,
                        app: App = None,
                        session_id: str = "",
                        ) -> Tuple[Iterator | None, Exception | None]:
        return self.agent_executor.chat_completion(question, app, session_id)

    def chat_stream(self,
                    question: str,
                    app: App = None,
                    session_id: str = ""
                    ) -> Tuple[Iterator | None, Exception | None]:
        return self.agent_executor.chat_stream(question, app, session_id)