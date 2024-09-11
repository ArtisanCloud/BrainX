import http

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.database.deps import get_async_db_session
from app.logger import logger
from app.schemas.auth import RequestRegisterUser, ResponseRegisterUser, RequestLoginUser, ResponseLoginUser
from app.schemas.base import ResponseSchema
from app.service.user.create_user import create_user_by_account
from app.service.user.login import login_by_account

router = APIRouter()


@router.post("/register")
async def api_register(
        data: RequestRegisterUser,
        db: AsyncSession = Depends(get_async_db_session),

) -> ResponseRegisterUser | ResponseSchema:
    try:

        user, exception = await create_user_by_account(db, data.account, data.password)
        if exception is not None:
            logger.error(exception)
            if isinstance(exception, SQLAlchemyError):
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseRegisterUser(user=user)

    return res


@router.post("/login")
async def api_login(
        data: RequestLoginUser,
        db: AsyncSession = Depends(get_async_db_session),

) -> ResponseLoginUser | ResponseSchema:
    try:

        token, exception = await login_by_account(db, data.account, data.password)
        if exception is not None:
            logger.error(exception, exc_info=settings.log.exc_info)
            if isinstance(exception, SQLAlchemyError):
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseLoginUser(
        account=data.account,
        token=token
    )

    return res
