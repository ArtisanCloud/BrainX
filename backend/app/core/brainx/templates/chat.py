from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.models import App


def get_chat_prompt_template(app: App) -> ChatPromptTemplate:
    persona = app.persona if app.persona else "You are a helpful assistant. Answer all questions to the best of your ability."

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                persona
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    return prompt
