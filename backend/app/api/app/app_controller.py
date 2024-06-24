import http

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.api.context_manager import build_request_context
from app.database.deps import get_db_session
from app.models.app import App

from app.schemas.app import ResponseGetAppList, RequestCreateApp, make_app, ResponseCreateApp, \
    RequestPatchApp, ResponsePatchApp, ResponseDeleteApp
from app.schemas.base import Pagination, ResponseSchema
from app.service.app.create import create_app
from app.service.app.delete import soft_delete_app
from app.service.app.list import get_app_list
from app.service.app.patch import patch_app

router = APIRouter()


@router.get("/list")
async def api_get_app_list(
        request: Request,
        _=Depends(build_request_context),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetAppList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))

    p = Pagination(page=page, page_size=page_size)

    try:
        apps, pagination, exception = await get_app_list(db, p)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetAppList(data=apps, pagination=pagination)

    return res


@router.get("/{app_id}")
async def api_get_app_by_id(app_id: int, db: AsyncSession = Depends(get_db_session)):
    app = await db.get(App, app_id)
    if app is None:
        raise HTTPException(status_code=404, detail="App not found")
    return app


@router.post("/create")
async def api_create_app(
        data: RequestCreateApp,
        db: AsyncSession = Depends(get_db_session)):
    try:

        app = make_app(data)
        # print(app)
        app, exception = await create_app(db, app)
        if exception is not None:
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
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseDeleteApp(result=result)

    return res
