from fastapi import HTTPException, Query
from starlette.requests import Request

from app import settings


# 验证access_key令牌
def auth_openapi_access_key(access_key: str = Query(...)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
    )

    if access_key != settings.openapi.access_key:
        raise credentials_exception


