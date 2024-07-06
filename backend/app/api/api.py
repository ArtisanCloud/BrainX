from fastapi import APIRouter

from app.api.conversation import conversation_controller
from app.api.system import status_controller, test_controller
from app.api.customer import customer_controller
from app.api.media_resource import media_resource_controller

from app.api.app import app_controller
from app.api.chat_bot import chat_controller
from app.api.question_answer import query_controller, visual_search_controller, visual_query_controller

err_code_400 = 400

api_router = APIRouter()

# system
api_router.include_router(status_controller.router, prefix="/system", tags=["system"])
api_router.include_router(test_controller.router, prefix="/system", tags=["test"])

# media resource
api_router.include_router(media_resource_controller.router, prefix="/media/resource",
                          tags=["media_resource", "list", "create", "update", "delete"])

# customer
api_router.include_router(customer_controller.router, prefix="/customer", tags=["customer"])

# robot_chat bot
api_router.include_router(chat_controller.router, prefix="/chat_bot", tags=["chatbot"])

# app
api_router.include_router(app_controller.router, prefix="/chat_bot/app", tags=["chatbot"])
# conversation
api_router.include_router(conversation_controller.router, prefix="/chat_bot/conversation", tags=["chatbot"])

# question answer
api_router.include_router(query_controller.router, prefix="/question_answer", tags=["query"])
api_router.include_router(visual_query_controller.router, prefix="/question_answer", tags=["visual_query"])
api_router.include_router(visual_search_controller.router, prefix="/question_answer", tags=["visual_search"])


import os
from fastapi import APIRouter

# def include_router_from_folder(router: APIRouter, folder_path: str):
#     for root, _, files in os.walk(folder_path):
#         for file_name in files:
#             if file_name.endswith('.py'):
#                 file_path = os.path.join(root, file_name)
#                 module_path = '.'.join(os.path.relpath(file_path, folder_path).split(os.sep))[:-3]
#                 module = __import__(module_path, globals(), locals(), ['router'], 0)
#                 if hasattr(module, 'router'):
#                     router.include_router(module.router)
