from fastapi import APIRouter, Depends

from app.openapi.api import auth_controller
from app.openapi.api.chat_bot import chat_controller
from app.openapi.api.demo import demo_controller
from app.openapi.api.coze import coze_controller
from app.openapi.middleware.auth import auth_platform_token

openapi_router = APIRouter()

# auth
openapi_router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

# demo
openapi_router.include_router(
    demo_controller.router,
    dependencies=[Depends(auth_platform_token)],
    prefix="/demo",
    tags=["demo"],
)


openapi_router.include_router(
    chat_controller.router,
    dependencies=[Depends(auth_platform_token)],
    prefix="/chat-bot",
    tags=["chat"],
)

openapi_router.include_router(
    coze_controller.router,
    dependencies=[Depends(auth_platform_token)],
    prefix="/coze",
    tags=["coze"],
)
