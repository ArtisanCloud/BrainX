from typing import Tuple, Iterator, Any, List, Dict, Optional

from langchain_core.messages import HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import logger
from app.constant.ai_model.provider import ProviderID
from app.core.agent_bot.agent import AgentBot
from app.core.brainx.base import LLMModel
from app.core.brainx.model_manager import ModelManager
from app.core.rag.base import create_indexer, create_retriever, create_text_embedding_model
from app.core.workflow.state import GraphState
from app.models.app.app import App
from app.models.model_provider.provider_model import ModelType


class BrainXService:
    tenant_uuid: str
    model_manager: ModelManager
    async_db: AsyncSession
    sync_db: Session

    def __init__(
            self,
            tenant_uuid: str = None,
            app: App = None,
            async_db: AsyncSession = None,
            sync_db: Session = None,
            provider_id: str = ProviderID.OPENAI,
            model_id: str = LLMModel.OPENAI_GPT_3_D_5_TURBO,
            streaming: bool = False,
            collection_name: str = "rag_embeddings",
    ):
        # 初始化属性
        self.tenant_uuid = tenant_uuid
        self.async_db = async_db
        self.sync_db = sync_db
        self.streaming = streaming

        # 初始化 ModelManager
        self.model_manager = ModelManager(
            provider_id=provider_id, model_id=model_id,
            async_db=async_db, sync_db=sync_db
        )

        # define the agent executor
        self.llm_model_instance, exception = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.LLM)
        if exception:
            return

        self.text_embedding_model_instance, exception = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.TEXT_EMBEDDING)
        if exception:
            raise exception

        # self.image_embedding_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.IMAGE_EMBEDDING)
        # self.rerank_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.RERANK)
        # self.speech2text_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.SPEECH2TEXT)
        # self.moderation_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.MODERATION)
        # self.tts_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.TTS)
        # self.text2img_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.TEXT2IMG)
        # self.img2img_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.IMG2IMG)
        # self.text2video_model_instance = self.model_manager.get_default_model_instance(tenant_uuid, ModelType.TEXT2VIDEO)

        # define the ingestion
        self.indexer = create_indexer(self.text_embedding_model_instance)

        # define the retriever
        self.retriever = create_retriever(
            collection_name, self.text_embedding_model_instance
        )

        # get the vector store
        self.vector_store = self.retriever.get_vector_store()

        # define the Agent Bot
        if app:
            self.agent_bot = AgentBot(
                app=app,
                llm_model_instance=self.llm_model_instance,
                retriever=self.retriever
            )

    # async def retrieve(
    #         self, content: str, top_k: int, score_threshold: float, filters: dict = None
    # ) -> Tuple[List[DocumentNode] | None, Exception | None]:
    #     return self.retriever.retrieve(content, top_k, score_threshold, filters)
    #
    # def stream(
    #         self,
    #         query: Dict,
    #         temperature: float = 0.5,
    #         input_variables=list[str],
    #         template: str = "",
    # ) -> Tuple[Iterator | None, Exception | None]:
    #     return self.llm_model_instance.stream(
    #         query,
    #         temperature=temperature,
    #         input_variables=input_variables,
    #         template=template,
    #     )
    #
    # def invoke(
    #         self,
    #         query: Dict,
    #         temperature: float = 0.5,
    #         input_variables=list[str],
    #         template: str = "",
    #         output_schemas: Any = None,
    # ) -> Tuple[InvokeResponse | None, Exception | None]:
    #     return self.agent_executor.invoke(
    #         query,
    #         temperature=temperature,
    #         input_variables=input_variables,
    #         template=template,
    #         output_schemas=output_schemas,
    #     )
    #
    # def completion(
    #         self,
    #         query: str,
    #         temperature: float = 0.5,
    #         config: Optional[Any] = None,
    #         output_schemas: Any = None,
    #         **kwargs: Any
    # ) -> Tuple[Any, Exception | None]:
    #     return self.agent_executor.invoke(
    #         query=query,
    #         temperature=temperature,
    #         config=config,
    #         output_schemas=output_schemas,
    #         **kwargs
    #     )
    #
    # def chat_completion(
    #         self,
    #         question: Dict,
    #         temperature: float = 0.5,
    #         app: App = None,
    #         session_id: str = "",
    # ) -> Tuple[str | None, Exception | None]:
    #     return self.agent_executor.chat_completion(
    #         question=question, app=app, session_id=session_id, temperature=temperature
    #     )
    #
    # def chat_stream(
    #         self,
    #         question: Dict,
    #         temperature: float = 0.5,
    #         app: App = None,
    #         session_id: str = "",
    # ) -> Tuple[Iterator | None, Exception | None]:
    #     return self.agent_executor.chat_stream(
    #         question=question,
    #         app=app,
    #         session_id=session_id,
    #         temperature=temperature,
    #     )

    def agent_chat(
            self, question: str, session_id: str = ""
    ) -> Tuple[Iterator | None, Exception | None]:
        # print(self.agent_bot)

        state = GraphState(question=question, messages=[HumanMessage(content="")])
        # print(state)

        stream_response = self.agent_bot.run(state)

        return stream_response, None
