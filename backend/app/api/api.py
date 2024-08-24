import os

from fastapi import APIRouter, Depends
from starlette.staticfiles import StaticFiles

from app.api.auth import auth_controller
from app.api.conversation import conversation_controller, message_controller
from app.api.middleware.auth import auth_user_token, get_session_user
from app.api.rag import dataset_controller, document_controller, document_segment_controller
from app.api.system import status_controller, test_controller
from app.api.task import task_controller
from app.api.tenant import user_controller, tenant_controller
from app.api.media_resource import media_resource_controller

from app.api.app import app_controller
from app.api.chat_bot import chat_controller
from app.api.question_answer import query_controller, visual_search_controller, visual_query_controller

err_code_400 = 400

api_router = APIRouter()

# system
api_router.include_router(status_controller.router, prefix="/system", tags=["system"])
api_router.include_router(test_controller.router, prefix="/system", tags=["tests"])

# auth
api_router.include_router(auth_controller.router,
                          prefix="/auth", tags=["auth"])
# tenant
api_router.include_router(tenant_controller.router,
                          dependencies=[Depends(auth_user_token)],
                          prefix="/tenant", tags=["tenant"])
api_router.include_router(user_controller.router,
                          dependencies=[Depends(auth_user_token)],
                          prefix="/tenant/user", tags=["tenant", "user"])

# media resource
api_router.include_router(media_resource_controller.router, prefix="/media/resource",
                          dependencies=[Depends(auth_user_token)],
                          tags=["media_resource", "list", "create", "update", "delete"])

# robot_chat bot
api_router.include_router(chat_controller.router, prefix="/chat_bot",
                          dependencies=[Depends(auth_user_token)],
                          tags=["chatbot"])

# app
api_router.include_router(app_controller.router, prefix="/app",
                          dependencies=[Depends(auth_user_token)],
                          tags=["chatbot"])
# conversation
api_router.include_router(conversation_controller.router, prefix="/chat_bot/conversation",
                          dependencies=[Depends(auth_user_token)],
                          tags=["chatbot"])
api_router.include_router(message_controller.router, prefix="/chat_bot/conversation/message",
                          dependencies=[Depends(auth_user_token)],
                          tags=["chatbot"])

# question answer
api_router.include_router(query_controller.router, prefix="/question_answer",
                          dependencies=[Depends(auth_user_token)],
                          tags=["query"])
api_router.include_router(visual_query_controller.router, prefix="/question_answer",
                          dependencies=[Depends(auth_user_token)],
                          tags=["visual_query"])
api_router.include_router(visual_search_controller.router, prefix="/question_answer",
                          dependencies=[Depends(auth_user_token)],
                          tags=["visual_search"])

# rag
api_router.include_router(dataset_controller.router, prefix="/rag",
                          dependencies=[Depends(auth_user_token)],
                          tags=["chatbot"])

api_router.include_router(dataset_controller.router, prefix="/rag/dataset",
                          dependencies=[Depends(auth_user_token)],
                          tags=["rag", "dataset"])
api_router.include_router(document_controller.router, prefix="/rag/dataset/document",
                          dependencies=[Depends(auth_user_token)],
                          tags=["rag", "document"])
api_router.include_router(document_segment_controller.router, prefix="/rag/dataset/document/segment",
                          dependencies=[Depends(auth_user_token)],
                          tags=["rag", "document_segment"])

# task
api_router.include_router(task_controller.router, prefix="/task",
                          dependencies=[Depends(auth_user_token)],
                          tags=["task"])
