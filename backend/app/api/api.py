from fastapi import APIRouter

from app.api.customer import customer_controller
from app.api.revenue import revenue_controller
from app.api.revenue import invoice_controller

# from app.api.customer import conversation, health, documents

api_router = APIRouter()
api_router.include_router(customer_controller.router, prefix="/customer", tags=["customer"])
api_router.include_router(revenue_controller.router, prefix="/revenue", tags=["revenue"])
api_router.include_router(invoice_controller.router, prefix="/invoice", tags=["invoice"])
# api_router.include_router(
#     conversation.router, prefix="/conversation", tags=["conversation"]
# )
# api_router.include_router(documents.router, prefix="/document", tags=["document"])
# api_router.include_router(health.router, prefix="/health", tags=["health"])
