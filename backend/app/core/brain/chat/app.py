from typing import List

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from llama_index.core import Document
from pydantic import BaseModel, Field

from app.core.brain.index import LLMModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.chat_history import BaseChatMessageHistory

from app.core.brain.llm.langchain import get_openai_llm, get_baidu_qianfan_llm, get_ollama_llm, get_kimi_llm
from app.models.app.app import App

from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage) -> None:
        """Add a self-created message to the store"""
        self.messages.append(message)

    def clear(self) -> None:
        self.messages = []


store = {}


def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = InMemoryHistory()
    return store[(user_id, conversation_id)]


def fake_retriever(query):
    assert isinstance(query, str)
    return [
        Document(page_content="cats are the answer"),
        Document(page_content="CAT POWERS"),
    ]


fake_retriever = RunnableLambda(fake_retriever)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_chat_prompt_template(app: App) -> ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                # app.persona_prompt,
                "You are a helpful assistant. Answer all questions to the best of your ability."
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    return prompt


def chat_by_llm(question: str, llm: str, app: App = None, temperature: float = 0.5, stream_handler=None):
    # 初始化一个大模型
    # OpenAI的模型
    if llm == LLMModel.OPENAI_GPT_3_D_5_TURBO.value:
        chat_llm = get_openai_llm(llm, temperature, True)
    # Kimi的模型
    elif llm == LLMModel.KIMI_MOONSHOT_V1_8K.value:
        chat_llm = get_kimi_llm(llm, temperature, True)
    # 千帆的模型
    elif llm == (
            LLMModel.BAIDU_QIANFAN_QIANFAN_BLOOMZ_7B_COMPRESSED.value
            | LLMModel.BAIDU_ERNIE_3_D_5_8K.value
            | LLMModel.BAIDU_ERNIE_4_D_0_8K.value
            | LLMModel.BAIDU_ERNIE_Speed_128K.value
            | LLMModel.BAIDU_ERNIE_Lite_8K.value
    ):
        chat_llm = get_baidu_qianfan_llm(llm, temperature, True)
    # Ollama的模型
    else:
        chat_llm = get_ollama_llm(llm, temperature, True)

    # 设置一个提词模版
    prompt = get_chat_prompt_template(app)

    # 设置一个对话链
    # context = itemgetter("question") | fake_retriever | format_docs
    # first_step = RunnablePassthrough.assign(context=context)
    # chain = first_step | prompt | ChatLLM

    # Set up a chat history
    chat_history = RedisChatMessageHistory(session_id='test_session_id')

    # Define the chat chain
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
        if len(stored_messages) <= 2:
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
    stream_response = chain_with_trimming.stream(
        {"question": question},
        config={"configurable": {"session_id": "test_session_id"}},
    )

    # print(stream_response)
    return stream_response
