from typing import Tuple, Iterator, Any, List, Dict, Optional

from langchain_core.messages import HumanMessage

from app.core.agent_bot.agent import AgentBot
from app.core.rag.base import create_agent_executor, create_indexer, create_retriever, create_text_embedding_model
from app.core.workflow.state import GraphState
from app.models import AppModelConfig
from app.models.app.app import App
from app.models.rag.document_node import DocumentNode
from app.models.rag.invoke_response import InvokeResponse


class BrainXService:
    def __init__(
        self,
        llm: str,
        streaming: bool = False,
        collection_name: str = "rag_embeddings",
        app: App = None,
        app_model_config: AppModelConfig = None,
    ):
        # 进行其他初始化操作
        # create the embedding model
        embedding_model_instance = create_text_embedding_model()

        # define the ingestion
        self.indexer = create_indexer(embedding_model_instance)

        # define the retriever
        self.retriever = create_retriever(
            collection_name, embedding_model_instance
        )

        # get the vector store
        self.vector_store = self.retriever.get_vector_store()

        # define the agent executor
        self.agent_executor = create_agent_executor(llm=llm, streaming=streaming)

        # define the Agent Bot
        if app:
            self.agent_bot = AgentBot(
                default_llm=llm, app=app, retriever=self.retriever
            )


    def bind_llm(self, llm: str):
        self.llm = llm
        return self

    def set_streaming(self, streaming: bool):
        self.streaming = streaming
        return self

    async def retrieve(
        self, content: str, top_k: int, score_threshold: float, filters: dict = None
    ) -> Tuple[List[DocumentNode] | None, Exception | None]:
        return self.retriever.retrieve(content, top_k, score_threshold, filters)

    def stream(
        self,
        query: Dict,
        temperature: float = 0.5,
        input_variables=list[str],
        template: str = "",
    ) -> Tuple[Iterator | None, Exception | None]:
        return self.agent_executor.stream(
            query,
            temperature=temperature,
            input_variables=input_variables,
            template=template,
        )

    def invoke(
        self,
        query: Dict,
        temperature: float = 0.5,
        input_variables=list[str],
        template: str = "",
        output_schemas: Any = None,
    ) -> Tuple[InvokeResponse | None, Exception | None]:
        return self.agent_executor.invoke(
            query,
            temperature=temperature,
            input_variables=input_variables,
            template=template,
            output_schemas=output_schemas,
        )

    def completion(
        self,
        query: str,
        temperature: float = 0.5,
        config: Optional[Any] = None,
        output_schemas: Any = None,
        **kwargs: Any
    ) -> Tuple[Any, Exception | None]:
        return self.agent_executor.invoke(
            query=query,
            temperature=temperature,
            config=config,
            output_schemas=output_schemas,
            **kwargs
        )

    def chat_completion(
        self,
        question: Dict,
        temperature: float = 0.5,
        app: App = None,
        session_id: str = "",
    ) -> Tuple[str | None, Exception | None]:
        return self.agent_executor.chat_completion(
            question=question, app=app, session_id=session_id, temperature=temperature
        )

    def chat_stream(
        self,
        question: Dict,
        temperature: float = 0.5,
        app: App = None,
        session_id: str = "",
    ) -> Tuple[Iterator | None, Exception | None]:

        return self.agent_executor.chat_stream(
            question=question,
            app=app,
            session_id=session_id,
            temperature=temperature,
        )

    def agent_chat(
        self, question: str, session_id: str = ""
    ) -> Tuple[Iterator | None, Exception | None]:
        # print(self.agent_bot)

        state = GraphState(question=question, messages=[HumanMessage(content="")])
        # print(state)

        stream_response = self.agent_bot.run(state)

        return stream_response, None
