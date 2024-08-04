import http

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.api.middleware.auth import get_session_user
from app.database.deps import get_db_session
from app.logger import logger
from app.models import User
from app.models.app.app import App

from app.schemas.app.app import ResponseGetAppList, RequestCreateApp, make_app, ResponseCreateApp, \
    RequestPatchApp, ResponsePatchApp, ResponseDeleteApp, ResponseGetApp
from app.schemas.base import Pagination, ResponseSchema
from app.service.app.create import create_app
from app.service.app.delete import soft_delete_app
from app.service.app.get import get_app_by_uuid
from app.service.app.list import get_app_list
from app.service.app.patch import patch_app

router = APIRouter()


@router.get("/list")
async def api_get_app_list(
        request: Request,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetAppList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))

    p = Pagination(page=page, page_size=page_size)

    try:
        apps, pagination, exception = await get_app_list(db, session_user.tenant_owner_uuid, p)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetAppList(data=apps, pagination=pagination)

    return res


@router.get("/{app_uuid}")
async def api_get_app_by_uuid(
        app_uuid: str,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)
):
    try:
        app, exception = await get_app_by_uuid(db, session_user, app_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetApp(data=app)

    return res

@router.post("/create")
async def api_create_app(
        data: RequestCreateApp,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)):
    try:

        app = make_app(data)
        app.tenant_uuid = str(session_user.tenant_owner_uuid)
        app.created_user_by = str(session_user.uuid)
        # print(app)
        app, exception = await create_app(db, app)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseCreateApp(app=app)

    return res


@router.patch("/patch/{app_uuid}")
async def api_patch_app(
        app_uuid: str,  # 接收路径参数 app_uuid
        data: RequestPatchApp,
        db: AsyncSession = Depends(get_db_session)):
    try:

        update_data = data.dict(exclude_unset=True)
        # print(app_uuid, update_data)

        app, exception = await patch_app(db, app_uuid, update_data)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponsePatchApp(app=app)

    return res


@router.delete("/delete/{app_uuid}")
async def api_delete_app(
        app_uuid: str,  # 接收路径参数 app_uuid
        db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = 1
        result, exception = await soft_delete_app(db, user_id, app_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseDeleteApp(result=result)

    return res
