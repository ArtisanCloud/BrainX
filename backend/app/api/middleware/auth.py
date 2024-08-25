from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.deps import get_async_db_session
from app.schemas.auth import auth_user_uuid_key, ALGORITHM, SECRET_KEY
from app.service.user.service import UserService
from starlette.requests import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_session_user(
        request: Request,
        db: AsyncSession = Depends(get_async_db_session)
):
    session_exception = HTTPException(
        status_code=401,
        detail="Session have no user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_uuid = request.session[auth_user_uuid_key]
    # print("get session user:", user_uuid)
    if user_uuid is None:
        raise session_exception

    service_user = UserService(db)
    # print("get session user:", user_uuid)
    current_user, exception = await service_user.user_dao.async_get_by_uuid(user_uuid)
    # print(current_user)
    if exception is not None:
        session_exception.detail = exception
        raise session_exception
    if current_user is None:
        session_exception.detail = "cannot find the user from token"
        raise session_exception

    return current_user


# 验证JWT令牌
def auth_user_token(
        request: Request,
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 解析token里的user uuid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)
        user_uuid: str = payload.get(auth_user_uuid_key)
        if user_uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # print("auth token user_uuid:", user_uuid)
    request.session[auth_user_uuid_key] = user_uuid
    # print("set current context user uuid from token")
