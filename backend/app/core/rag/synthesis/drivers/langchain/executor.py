from typing import Optional, Any, List, Iterator, Tuple, Type
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from langchain_core.runnables.utils import Input

from app import settings
from app.core.brainx.chat.app import get_chat_prompt_template
from app.core.rag.ingestion.drivers.langchain.helper import convert_document_to_response
from app.core.rag.synthesis.interface import BaseAgentExecutor
from app.logger import logger
from app.models import App


class LangchainAgentExecutor(BaseAgentExecutor):
    def __init__(self,
                 llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 **kwargs):
        super().__init__(llm=llm, temperature=temperature, streaming=streaming, **kwargs)

    def stream(self, query: str,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:
        try:
            completion_llm, exception = self.get_llm(temperature=temperature, streaming=True)
            if exception:
                raise exception

            prompt_template = PromptTemplate(
                input_variables=input_variables,
                template=template
            )
            # print(prompt_template.format(query=question))

            chain = prompt_template | completion_llm

            response = chain.stream(
                input=Input(query),
            )

            return response, None

        except Exception as e:
            return None, e

    def completion(self, query: str,
                   temperature: float = 0.5,
                   input_variables=list[str], template: str = '',
                   **kwargs: Any) -> Tuple[Any | None, Exception | None]:
        try:
            completion_llm, exception = self.get_llm(temperature=temperature, streaming=False)
            print("complete llm:", completion_llm)
            if exception:
                raise exception

            prompt_template = PromptTemplate(
                input_variables=input_variables,
                template=template
            )
            # print(prompt_template.format(query=question))

            chain = prompt_template | completion_llm

            output = chain.invoke(
                input={"query": query},
            )

            response = convert_document_to_response(output)

            return response, None

        except Exception as e:
            logger.info(f"Error in langchain completion: {e}", exc_info=settings.log.exc_info)
            return None, e

    def chat_completion(self,
                        question: str,
                        temperature: float = 0.5,
                        app: App = None,
                        session_id: str = "",
                        **kwargs: Any) -> Tuple[str | None, Exception | None]:
        try:
            chat_llm, exception = self.get_llm(temperature=temperature, streaming=False)
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
                    temperature: float = 0.5,
                    session_id: str = "",
                    **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:

        try:
            chat_llm, exception = self.get_llm(temperature=temperature, streaming=True)
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

    def invoke(self, query: str, temperature: float = 0.5, config: Optional[Any] = None, **kwargs: Any) -> str:
        return ""

    def get_chat_history(self, session_id: str) -> ChatMessageHistory:
        chat_history_cls: Type[ChatMessageHistory] = RedisChatMessageHistory  # ChatMessageHistory 动态驱动
        chat_history_kwargs: dict = {
            "url": settings.cache.redis.url,
        }  # 传递给 ChatMessageHistory 的其他参数
        try:
            return chat_history_cls(session_id=session_id, **chat_history_kwargs)
        except Exception as e:
            # 处理错误，可能记录日志或抛出自定义异常
            raise Exception(f"Failed to create chat history: {e}")

