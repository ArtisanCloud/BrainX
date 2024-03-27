from fastapi import APIRouter

from app.api.endpoints import customer
# from app.api.endpoints import conversation, health, documents

api_router = APIRouter()
api_router.include_router(customer.router, prefix="/customer", tags=["customer"])
# api_router.include_router(
#     conversation.router, prefix="/conversation", tags=["conversation"]
# )
# api_router.include_router(documents.router, prefix="/document", tags=["document"])
# api_router.include_router(health.router, prefix="/health", tags=["health"])
