from typing import Optional, Any, List, Iterator, Tuple, Type, Dict
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnablePassthrough
from langchain_core.runnables.utils import Input

from app import settings
from app.core.brainx.base import LLMModel
from app.core.brainx.chat.app import get_chat_prompt_template
from app.core.brainx.llm.langchain import get_openai_llm, get_kimi_llm, get_baidu_qianfan_llm, get_ollama_llm
from app.core.rag.ingestion.drivers.langchain.helper import convert_document_to_response
from app.core.rag.synthesis.drivers.langchain.helper import process_json
from app.core.rag.synthesis.interface import BaseAgentExecutor
from app.logger import logger
from app.models import App
from app.models.rag.invoke_response import InvokeResponse


class LangchainAgentExecutor(BaseAgentExecutor):
    def __init__(self,
                 llm: str,
                 temperature: float = 0.5,
                 streaming: bool = False,
                 **kwargs):
        super().__init__(llm=llm, temperature=temperature, streaming=streaming, **kwargs)

    def get_llm(self, temperature: float = 0.5, streaming: bool = False) -> Tuple[BaseChatModel, Exception | None]:
        match self.llm:
            case LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
                mdl_llm = get_openai_llm(self.llm, temperature=temperature, streaming=streaming)

            case LLMModel.KIMI_MOONSHOT_V1_8K.value:
                mdl_llm = get_kimi_llm(self.llm, temperature=temperature, streaming=streaming)

            case (
            LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value |
            LLMModel.BAIDU_ERNIE_3_D_5_8K.value |
            LLMModel.BAIDU_ERNIE_4_D_0_8K.value |
            LLMModel.BAIDU_ERNIE_Speed_128K.value |
            LLMModel.BAIDU_ERNIE_Lite_8K.value
            ):
                mdl_llm = get_baidu_qianfan_llm(self.llm, temperature=temperature, streaming=streaming)

            case (
            LLMModel.OLLAMA_13B_ALPACA_16K.value |
            LLMModel.OLLAMA_GEMMA_2B.value |
            LLMModel.OLLAMA_GEMMA_7B.value
            ):
                mdl_llm = get_ollama_llm(self.llm, temperature=temperature, streaming=streaming)
            case _:
                return None, Exception(f"Unsupported LLM model: {self.llm}")

        # print("query llm:", mdl_llm)

        return mdl_llm, None

    def stream(self, query: Dict,
               temperature: float = 0.5,
               input_variables=list[str], template: str = '',
               **kwargs: Any) -> Tuple[Iterator | None, Exception | None]:
        try:
            llm, exception = self.get_llm(temperature=temperature, streaming=True)
            if exception:
                raise exception

            prompt_template = PromptTemplate(
                input_variables=input_variables,
                template=template
            )
            # print(prompt_template.format(query=question))

            chain = prompt_template | llm

            response = chain.stream(
                input=Input(query),
            )

            return response, None

        except Exception as e:
            return None, e

    def invoke(self, query: Any,
               temperature: float = 0.5,
               input_variables=list[str],
               template: str = '',
               output_schemas: Any = None,
               **kwargs: Any) -> Tuple[Any | None, Exception | None]:
        try:

            llm, exception = self.get_llm(temperature=temperature, streaming=False)
            if exception:
                raise exception
            print("invoke llm:", llm)

            chain = llm

            parser = None
            partial_variables = {}
            if output_schemas:
                parser = JsonOutputParser(pydantic_object=output_schemas)

                partial_variables["format_instructions"] = parser.get_format_instructions()
                # print(partial_variables)

            # 是否要支持模版
            if template:
                prompt_template = PromptTemplate(
                    template=template,
                    input_variables=input_variables,
                    partial_variables=partial_variables,
                )

                chain = prompt_template | chain
            # print(prompt_template.format(query=question))

            # 直接使用LLM的模型，来设置结构化输出
            output = chain.invoke(
                input=query,
            )

            # 返回结构化输出结果
            if output_schemas:
                # 处理非正规格式的json
                if isinstance(output, str):
                    content = output
                else:
                    content = output.content

                print(111111, type(content), content)
                obj = parser.invoke(content)
                return obj, None

            response = convert_document_to_response(output)

            return response, None

        except Exception as e:
            logger.info(f"Error in langchain completion: {e}", exc_info=settings.log.exc_info)
            return None, e

    def chat_completion(self,
                        query: Dict,
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
                query,
                config={"configurable": {"session_id": "test_session_id"}},
            )

            return completion_response, None

        except Exception as e:
            return None, e

    def chat_stream(self,
                    query: Dict,
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
                query,
                config={"configurable": {"session_id": "test_session_id"}},
            )

            return stream_response, None

        except Exception as e:
            return None, e

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
