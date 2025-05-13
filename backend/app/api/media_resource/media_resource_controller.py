import http

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app import settings
from app.api.middleware.auth import get_session_user
from app.database.base import PER_PAGE, PAGE
from app.logger import logger
from app.database.deps import get_async_db_session_dep
from app.models import User
from app.schemas.base import ResponseSchema, Pagination
from app.schemas.media_resource.schema import ResponseGetMediaResourceList, ResponseCreateMediaResource, \
    RequestCreateMediaResourceByBase64, ResponseGetMediaResource
from app.service.media_resource.create import create_media_resource_by_file, create_media_resource_by_base64_string
from app.service.media_resource.get import get_media_resource_by_uuid
from app.service.media_resource.list import get_media_resource_list

router = APIRouter()


@router.get("/list")
async def api_get_media_resource_list(
        request: Request,
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseGetMediaResourceList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", PAGE))
    page_size = int(request.query_params.get("page_size", PER_PAGE))

    p = Pagination(page=page, page_size=page_size)

    try:
        media_resources, pagination, exception = await get_media_resource_list(async_db, p)
        if exception is not None:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetMediaResourceList(data=media_resources, pagination=pagination)

    return res


@router.post("/create")
async def create_media_resource(
        sort_index: int,
        async_db: AsyncSession = Depends(get_async_db_session_dep),
        resource: UploadFile = File(...)
) -> ResponseCreateMediaResource | ResponseSchema:
    try:

        media_resource, exception = await create_media_resource_by_file(async_db, resource)
        if exception is not None:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    media_resource.sort_index = sort_index
    res = ResponseCreateMediaResource(media_resource=media_resource, is_oss=(not media_resource.is_local_stored))

    return res


@router.post("/create/base64")
async def create_media_resource(
        data: RequestCreateMediaResourceByBase64,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseCreateMediaResource | ResponseSchema:
    try:
        # Parse multipart form
        # print(resource)
        #
        # print(session_user)
        media_resource, exception = await create_media_resource_by_base64_string(
            async_db, session_user,
            data.bucketName, data.base64Data,
            data.mediaName, data.sortIndex,
        )
        if exception is not None:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    # media_resource.sort_index = sort_index
    res = ResponseCreateMediaResource(media_resource=media_resource, is_oss=(not media_resource.is_local_stored))

    return res


@router.get("/{media_resource_uuid}")
async def api_get_media_resource_by_uuid(
        media_resource_uuid: str,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep)
):
    try:
        media_resource, exception = await get_media_resource_by_uuid(async_db, session_user, media_resource_uuid)
        if exception is not None:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetMediaResource(data=media_resource)

    return res
