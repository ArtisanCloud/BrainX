from fastapi import APIRouter
from app.config.config import settings

from cozepy import ChatStatus, Coze, Message, TokenAuth, COZE_CN_BASE_URL

from app.openapi.schemas.coze import RequestChat, ResponseChat

router = APIRouter()


@router.post("/create")
async def api_create(data: RequestChat) -> ResponseChat:

    coze = Coze(auth=TokenAuth(settings.coze.api_key))

    chat_poll = coze.chat.create_and_poll(
        # id of bot
        bot_id=data.bot_id,
        # id of user, Note: The user_id here is specified by the developer, for example, it can be the
        # business id in the developer system, and does not include the internal attributes of coze.
        user_id=data.user_id,
        # user input
        additional_messages=[Message.build_user_question_text(data.input)],
    )
    for message in chat_poll.messages:
        print(message.content, end="")

    if chat_poll.chat.status == ChatStatus.COMPLETED:
        print()
        print("token usage:", chat_poll.chat.usage.token_count)

    return ResponseChat(chat_poll)
