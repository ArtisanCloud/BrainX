import http

from sqlalchemy.exc import SQLAlchemyError

from app import settings
from app.database.base import PER_PAGE, PAGE
from app.logger import logger

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.api.middleware.auth import get_session_user
from app.database.deps import get_async_db_session_dep
from app.models import User

from app.schemas.base import Pagination, ResponseSchema
from app.schemas.rag.dataset import ResponseGetDatasetList, RequestCreateDataset, make_dataset, RequestPatchDataset, \
    ResponseCreateDataset, ResponsePatchDataset, ResponseDeleteDataset, ResponseGetDataset, \
    RequestGetDatasetListWithApp, ResponseGetDatasetListWithApp, RequestDatasetConnectApps, ResponseDatasetConnectApps, \
    RequestDatasetDisconnectApps, ResponseDatasetDisconnectApps, RequestDatasetSyncApps, ResponseDatasetSyncApps
from app.service.app.service import AppService
from app.service.rag.dataset.create import create_dataset
from app.service.rag.dataset.list import get_dataset_list
from app.service.rag.dataset.get import get_dataset_by_uuid
from app.service.rag.dataset.list_with_app import get_dataset_list_with_connected_app
from app.service.rag.dataset.patch import patch_dataset
from app.service.rag.dataset.delete import soft_delete_dataset
from app.service.rag.dataset.service import DatasetService

router = APIRouter()


@router.get("/list")
async def api_get_dataset_list(
        request: Request,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseGetDatasetList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", PAGE))
    page_size = int(request.query_params.get("page_size", PER_PAGE))

    p = Pagination(page=page, page_size=page_size)

    datasets, pagination, exception = await get_dataset_list(async_db, session_user.tenant_owner_uuid, p)
    if exception is not None:
        raise exception

    res = ResponseGetDatasetList(data=datasets, pagination=pagination)

    return res


@router.get("/{dataset_uuid}")
async def api_get_dataset_by_uuid(
        dataset_uuid: str,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep)
):
    dataset, exception = await get_dataset_by_uuid(async_db, session_user, dataset_uuid)
    if exception is not None:
        raise exception

    res = ResponseGetDataset(data=dataset)

    return res


@router.post("/create")
async def api_create_dataset(
        data: RequestCreateDataset,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep)):
    dataset = make_dataset(data)
    dataset.tenant_uuid = str(session_user.tenant_owner_uuid)
    dataset.created_user_by = str(session_user.uuid)
    # print(dataset)
    dataset, exception = await create_dataset(async_db, dataset)
    if exception is not None:
        raise exception

    res = ResponseCreateDataset(dataset=dataset)

    return res


@router.patch("/patch/{dataset_uuid}")
async def api_patch_dataset(
        dataset_uuid: str,  # 接收路径参数 dataset_uuid
        data: RequestPatchDataset,
        async_db: AsyncSession = Depends(get_async_db_session_dep)):
    update_data = data.dict(exclude_unset=True)
    # print(dataset_uuid, update_data)

    dataset, exception = await patch_dataset(async_db, dataset_uuid, update_data)
    if exception is not None:
        raise exception

    res = ResponsePatchDataset(dataset=dataset)

    return res


@router.delete("/delete/{dataset_uuid}")
async def api_delete_dataset(
        dataset_uuid: str,  # 接收路径参数 dataset_uuid
        async_db: AsyncSession = Depends(get_async_db_session_dep)):
    user_id = 1
    result, exception = await soft_delete_dataset(async_db, user_id, dataset_uuid)
    if exception is not None:
        raise exception

    res = ResponseDeleteDataset(result=result)

    return res


@router.post("/list/connected-app")
async def api_get_dataset_list_with_connected_app(
        request: RequestGetDatasetListWithApp,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseGetDatasetListWithApp | ResponseSchema:
    if request.app_uuid == "":
        raise Exception("app_uuid is empty")

    datasets, exception = await get_dataset_list_with_connected_app(
        async_db, session_user.tenant_owner_uuid,
        request.app_uuid, request.only_connected
    )
    if exception is not None:
        raise exception

    res = ResponseGetDatasetListWithApp(data=datasets)

    return res


async def validate_app_uuid(async_db: AsyncSession, app_uuid: str, session_user: User):
    if app_uuid == "":
        raise Exception("app_uuid is empty")

    # validate the app
    app_service = AppService(async_db)
    app, exception = await app_service.app_dao.async_get_by_uuid(app_uuid)
    if exception:
        raise exception

    # print(app.tenant_uuid, session_user.tenant_owner_uuid)
    if str(app.tenant_uuid) != str(session_user.tenant_owner_uuid):
        raise Exception("app not belong to this tenant")


@router.post("/sync/apps")
async def api_dataset_sync_apps(
        request: RequestDatasetSyncApps,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseDatasetSyncApps | ResponseSchema:
    # validate the app
    await validate_app_uuid(async_db, request.app_uuid, session_user)

    # sync app with databases
    dataset_service = DatasetService(async_db)
    datasets, exception = await dataset_service.sync_dataset_with_apps(
        request.app_uuid,
        request.connect_dataset_uuids, request.disconnect_dataset_uuids
    )
    if exception is not None:
        raise exception

    res = ResponseDatasetSyncApps(data=datasets)

    return res


@router.post("/connect/apps")
async def api_dataset_connect_apps(
        request: RequestDatasetConnectApps,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseDatasetConnectApps | ResponseSchema:
    # validate the app
    await validate_app_uuid(async_db, request.app_uuid, session_user)

    # sync app with databases
    dataset_service = DatasetService(async_db)
    exception = await dataset_service.connect_dataset_with_apps(
        request.app_uuid,
        request.dataset_uuids
    )
    if exception:
        raise exception

    res = ResponseDatasetConnectApps(result=True)

    return res


@router.post("/disconnect/apps")
async def api_dataset_disconnect_apps(
        request: RequestDatasetDisconnectApps,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseDatasetDisconnectApps | ResponseSchema:
    await validate_app_uuid(async_db, request.app_uuid, session_user)

    # sync app with databases
    dataset_service = DatasetService(async_db)
    exception = await dataset_service.disconnect_dataset_with_apps(
        request.app_uuid,
        request.dataset_uuids
    )
    if exception is not None:
        raise exception

    res = ResponseDatasetDisconnectApps(result=True)

    return res
