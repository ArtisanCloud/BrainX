import http

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.database.deps import get_async_db_session_dep
from app.logger import logger
from app.schemas.auth import RequestRegisterUser, ResponseRegisterUser, RequestLoginUser, ResponseLoginUser
from app.schemas.base import ResponseSchema
from app.service.user.create_user import create_user_by_account
from app.service.user.login import login_by_account

router = APIRouter()


@router.post("/register")
async def api_register(
        data: RequestRegisterUser,
        async_db: AsyncSession = Depends(get_async_db_session_dep),

) -> ResponseRegisterUser | ResponseSchema:
    user, exception = await create_user_by_account(async_db, data.account, data.password)
    if exception is not None:
        raise exception

    res = ResponseRegisterUser(user=user)

    return res


@router.post("/login")
async def api_login(
        data: RequestLoginUser,
        async_db: AsyncSession = Depends(get_async_db_session_dep),

) -> ResponseLoginUser | ResponseSchema:
    token, exception = await login_by_account(async_db, data.account, data.password)
    if exception is not None:
        raise exception

    res = ResponseLoginUser(
        account=data.account,
        token=token
    )

    return res
