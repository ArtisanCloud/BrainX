from fastapi import APIRouter, Depends

from app.openapi.api import auth_controller
from app.openapi.api.demo import demo_controller
from app.openapi.middleware.auth import auth_platform_token

openapi_router = APIRouter()

# auth
openapi_router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

# demo
openapi_router.include_router(demo_controller.router,
                              dependencies=[Depends(auth_platform_token)],
                              prefix="/demo", tags=["demo"])
