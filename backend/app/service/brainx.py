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

from app.core.brain.chat.app import get_chat_prompt_template
from app.core.brain.index import LLMModel
from app.core.brain.indexing.engine import generate_storage_context, get_service_context
from app.core.brain.indexing.pg_vector import get_vector_store_singleton
from app.core.brain.llm.langchain import get_openai_llm, get_baidu_qianfan_llm, get_ollama_llm, get_kimi_llm
from app.core.config import settings
from app.models.app import App


class BrainXService:
    def __init__(self,
                 llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 chat_history_cls: Type[ChatMessageHistory] = RedisChatMessageHistory,  # ChatMessageHistory 动态驱动
                 chat_history_kwargs: dict = {},  # 传递给 ChatMessageHistory 的其他参数
                 ):
        self.llm = llm
        self.temperature = temperature
        self.streaming = streaming

        self.chat_history_cls = chat_history_cls
        self.chat_history_kwargs = chat_history_kwargs

        query_embedding_table = settings.database.table_name_vector_store
        self.vector_store, e = get_vector_store_singleton(query_embedding_table)
        if e:
            raise e

    def bind_llm(self, llm: str):
        self.llm = llm

    def get_llm(self, streaming: bool = False) -> Tuple[Any, Exception | None]:
        match self.llm:
            case LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
                mdl_llm = get_openai_llm(self.llm, self.temperature, streaming=streaming)

            case LLMModel.KIMI_MOONSHOT_V1_8K.value:
                mdl_llm = get_kimi_llm(self.llm, self.temperature, streaming=streaming)

            case (
            LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value |
            LLMModel.BAIDU_ERNIE_3_D_5_8K.value |
            LLMModel.BAIDU_ERNIE_4_D_0_8K.value |
            LLMModel.BAIDU_ERNIE_Speed_128K.value |
            LLMModel.BAIDU_ERNIE_Lite_8K.value
            ):
                mdl_llm = get_baidu_qianfan_llm(self.llm, self.temperature, streaming=streaming)

            case (LLMModel.OLLAMA_13B_ALPACA_16K.value | LLMModel.OLLAMA_GEMMA_2B.value):
                mdl_llm = get_ollama_llm(self.llm, self.temperature, streaming=streaming)
            case _:
                return None, Exception(f"Unsupported LLM model: {self.llm}")

        # print("query llm:", mdl_llm)

        return mdl_llm, None

    async def retrieve(self, content: str, top_k: int) -> Tuple[
        List[Document] | None, Exception | None]:
        try:

            # 存储上下文
            storage_context = generate_storage_context(self.vector_store)

            # 服务上下文
            service_context = get_service_context(self.llm)

            index = VectorStoreIndex.from_vector_store(
                self.vector_store,
                storage_context=storage_context,
                service_context=service_context
            )

            # configure retriever
            retriever = VectorIndexRetriever(
                index=index,
                similarity_top_k=top_k,
            )

            # configure response synthesizer
            response_synthesizer = get_response_synthesizer()

            match_docs = retriever.retrieve(content)
            # print(match_docs)

            return (
                list(Document(
                    page_content=doc.node.text,
                    metadata={
                        'score': doc.score,
                        'node_id': doc.node_id,
                        'metadata': doc.node.metadata
                    },
                ) for doc in match_docs),
                None
            )

        except Exception as e:
            return None, e

    def complete(self, inputs: Input, input_variables=list[str], template: str = '') -> Tuple[
        Output | None, Exception | None]:
        try:
            completion_llm, exception = self.get_llm(streaming=False)
            print("complete llm:", completion_llm)
            if exception:
                raise exception

            prompt_template = PromptTemplate(
                input_variables=input_variables,
                template=template
            )
            # print(prompt_template.format(query=question))

            chain = prompt_template | completion_llm

            response = chain.invoke(
                input=inputs,
            )

            return response, None

        except Exception as e:
            return None, e

    def stream(self, inputs: Input, input_variables=list[str], template: str = ''
               ) -> Tuple[
        Output | None, Exception | None]:
        try:
            completion_llm, exception = self.get_llm(streaming=True)
            if exception:
                raise exception

            prompt_template = PromptTemplate(
                input_variables=input_variables,
                template=template
            )
            # print(prompt_template.format(query=question))

            chain = prompt_template | completion_llm

            response = chain.stream(
                input=inputs,
            )

            return response, None

        except Exception as e:
            return None, e

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
        try:
            chat_llm, exception = self.get_llm(streaming=False)
            if exception:
                raise exception

            prompt = get_chat_prompt_template(app)

            # chat_history = RedisChatMessageHistory(session_id=session_id)
            chat_history = self.get_chat_history(session_id)

            chain = prompt | chat_llm

            # Add message history to the chain
            chain_with_message_history = RunnableWithMessageHistory(
                chain,
                lambda session_id: chat_history,
                input_messages_key="question",
                history_messages_key="history",
            )

            # Define a function to trim messages
            def trim_messages(chain_input):
                stored_messages = chat_history.messages
                if len(stored_messages) <= 6:
                    return False

                chat_history.clear()

                for message in stored_messages[-2:]:
                    chat_history.add_message(message)

                return True

            # Add message trimming to the chain
            chain_with_trimming = (
                    RunnablePassthrough.assign(messages_trimmed=trim_messages)
                    | chain_with_message_history)

            # Stream the response
            completion_response = chain_with_trimming.invoke(
                {"question": question},
                config={"configurable": {"session_id": "test_session_id"}},
            )

            return completion_response, None

        except Exception as e:
            return None, e

    def chat_stream(self,
                    question: str,
                    app: App = None,
                    session_id: str = ""
                    ) -> Tuple[Iterator | None, Exception | None]:

        try:
            chat_llm, exception = self.get_llm(streaming=True)
            if exception is not None:
                raise exception

            prompt = get_chat_prompt_template(app)

            chat_history = self.get_chat_history(session_id)

            chain = prompt | chat_llm

            # Add message history to the chain
            chain_with_message_history = RunnableWithMessageHistory(
                chain,
                lambda session_id: chat_history,
                input_messages_key="question",
                history_messages_key="history",
            )

            # Define a function to trim messages
            num_to_keep = 6
            def trim_messages(chain_input):
                stored_messages = chat_history.messages
                if len(stored_messages) <= num_to_keep:
                    return False

                # chat_history.clear()
                # for message in stored_messages[-2:]:
                #     chat_history.add_message(message)
                # return True
                # 这是裁剪给context的数据，暂时历史数据都会保存下来，后续可以调整。
                trimmed_messages = stored_messages[-num_to_keep:]
                return trimmed_messages

            # Add message trimming to the chain
            chain_with_trimming = (
                    RunnablePassthrough.assign(messages_trimmed=trim_messages)
                    | chain_with_message_history)

            # Stream the response
            stream_response = chain_with_trimming.stream(
                {"question": question},
                config={"configurable": {"session_id": "test_session_id"}},
            )

            return stream_response, None

        except Exception as e:
            return None, e
