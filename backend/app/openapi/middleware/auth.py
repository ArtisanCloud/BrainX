from typing import Tuple

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette.requests import Request

from app import settings
from app.api.middleware.auth import oauth2_scheme
from app.logger import logger
from app.openapi.api.token import sign_token
from app.openapi.models.platform import Platform
from app.openapi.schemas.auth import RequestAuthPlatform
from app.schemas.auth import  ALGORITHM, AccessTokenSchema

auth_platform_uuid_key = "auth_access_key"
# auth_platform_uuid_key = "platform_uuid"


# 验证access_key令牌
def auth_openapi_access_key(data: RequestAuthPlatform) -> Tuple[AccessTokenSchema | None, Exception | None]:
    platform_account_exception = HTTPException(
        status_code=401,
        detail="Invalid key access credentials",
    )

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid key secret credentials",
    )

    setting_access_key = ""
    setting_secret_key = ""
    # print(data)
    match data.platform:
        case "powerx":
            setting_access_key = settings.openapi.platforms.power_x.access_key
            setting_secret_key = settings.openapi.platforms.power_x.secret_key

        case "other_platform":
            pass

        case _:
            raise platform_account_exception
    # print(setting_access_key,setting_secret_key)
    if data.access_key != setting_access_key:
        raise platform_account_exception

    if data.secret_key != setting_secret_key:
        raise credentials_exception

    # create token
    platform = Platform(
        name=data.platform,
        access_key=data.access_key,
        secret_key=data.secret_key,
    )
    access_token = sign_token(platform, settings.openapi.platforms.token_secret_key, settings.jwt.expire_in)
    return access_token, None


# 验证access_key令牌
def auth_platform_token(
        request: Request,
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 解析token里的platform uuid
    try:

        payload = jwt.decode(token, settings.openapi.platforms.token_secret_key, algorithms=[ALGORITHM])
        # print(payload)
        platform_uuid: str = payload.get(auth_platform_uuid_key)
        if platform_uuid is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(e, exc_info=settings.log.exc_info)
        raise credentials_exception
    # print("api_auth token platform_uuid:", platform_uuid)
    request.session[auth_platform_uuid_key] = platform_uuid
    # print("set current context platform uuid from token")
