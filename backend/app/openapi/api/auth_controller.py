import http

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.deps import get_async_db_session
from app.logger import logger
from app.openapi.middleware.auth import auth_openapi_access_key
from app.schemas.base import ResponseSchema
from app.openapi.schemas.auth import RequestAuthPlatform, ResponseAuthPlatform

router = APIRouter()


@router.post("/")
async def api_auth(
        data: RequestAuthPlatform,
        db: AsyncSession = Depends(get_async_db_session),

) -> ResponseAuthPlatform | ResponseSchema:
    try:
        # service_platform = PlatformService(db)
        # token, exception = await service_platform.auth_by_platform(db, data.account, data.password)
        token, exception = auth_openapi_access_key(data)
        if exception is not None:
            logger.error(exception, exc_info=settings.log.exc_info)
            if isinstance(exception, SQLAlchemyError):
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseAuthPlatform(
        platform=data.platform,
        token=token
    )

    return res
