from fastapi import APIRouter, Depends

from app.openapi.demo import demo_controller
from app.openapi.middleware.auth import auth_openapi_access_key

openapi_router = APIRouter(
    dependencies=[Depends(auth_openapi_access_key)],
)

openapi_router.include_router(demo_controller.router, prefix="/demo", tags=["demo"])
