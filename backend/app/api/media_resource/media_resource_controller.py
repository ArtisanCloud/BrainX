import http

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


from app.database.deps import get_db_session
from app.schemas.base import ResponseSchema, Pagination
from app.schemas.media_resource.schema import ResponseGetMediaResourceList, ResponseCreateMediaResource, \
    RequestCreateMediaResourceByBase64
from app.service.media_resource.create import create_media_resource_by_file, create_media_resource_by_base64_string
from app.service.media_resource.list import get_media_resource_list
from app.utils.image import remove_base64_prefix

router = APIRouter()


@router.get("/list")
async def api_get_media_resource_list(
        request: Request,
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetMediaResourceList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))

    p = Pagination(page=page, page_size=page_size)

    try:
        media_resources, pagination, exception = await get_media_resource_list(db, p)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetMediaResourceList(data=media_resources, pagination=pagination)

    return res


@router.post("/create")
async def create_media_resource(request: Request,
                                sort_index: int,
                                db: AsyncSession = Depends(get_db_session),
                                resource: UploadFile = File(...)
                                ) -> ResponseCreateMediaResource | ResponseSchema:
    try:
        # Parse multipart form
        # print(resource)
        #

        media_resource, exception = await create_media_resource_by_file(db, resource)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    media_resource.sort_index = sort_index
    res = ResponseCreateMediaResource(media_resource=media_resource, is_oss=(not media_resource.is_local_stored))

    return res


@router.post("/create/base64")
async def create_media_resource(
        # sort_index: int,
        data: RequestCreateMediaResourceByBase64,
        db: AsyncSession = Depends(get_db_session),
) -> ResponseCreateMediaResource | ResponseSchema:
    try:
        # Parse multipart form
        # print(resource)
        #

        data.base64Data = remove_base64_prefix(data.base64Data)

        media_resource, exception = await create_media_resource_by_base64_string(db, data.bucketName, data.base64Data)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    # media_resource.sort_index = sort_index
    res = ResponseCreateMediaResource(media_resource=media_resource, is_oss=(not media_resource.is_local_stored))

    return res
