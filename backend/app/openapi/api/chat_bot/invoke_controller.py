import http
from fastapi import APIRouter
from app.config.config import settings
from app.logger import logger
from app.schemas.base import ResponseSchema

from app.schemas.robot_chat.chat import RequestCompletion, ResponseChatCompletion
from app.service.robot_chat.completion import completion

router = APIRouter()


@router.post("/completion")
async def api_completion(
        data: RequestCompletion,
) -> ResponseChatCompletion:
    msg, exception = await completion(system=data.system, user=data.user, llm=data.llm)
    if exception:
        raise exception

    return ResponseChatCompletion(data=msg)
