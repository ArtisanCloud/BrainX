import http

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.api.middleware.auth import get_session_user
from app.database.deps import get_db_session
from app.models import Dataset, User
from app.schemas.auth import auth_user_uuid_key

from app.schemas.base import Pagination, ResponseSchema
from app.schemas.rag.dataset import ResponseGetDatasetList, RequestCreateDataset, make_dataset, RequestPatchDataset, \
    ResponseCreateDataset, ResponsePatchDataset, ResponseDeleteDataset
from app.service.rag.dataset.create import create_dataset
from app.service.rag.dataset.list import get_dataset_list
from app.service.rag.dataset.get import get_dataset_by_uuid
from app.service.rag.dataset.patch import patch_dataset
from app.service.rag.dataset.delete import soft_delete_dataset

router = APIRouter()


@router.get("/list")
async def api_get_dataset_list(
        request: Request,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetDatasetList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", 1))
    page_size = int(request.query_params.get("page_size", 10))

    p = Pagination(page=page, page_size=page_size)
    try:
        datasets, pagination, exception = await get_dataset_list(db, session_user.uuid, p)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetDatasetList(data=datasets, pagination=pagination)

    return res


@router.get("/{dataset_uuid}")
async def api_get_dataset_by_uuid(dataset_uuid: str, db: AsyncSession = Depends(get_db_session)):
    get_dataset_by_uuid(db, dataset_uuid)
    dataset = await db.get(Dataset, dataset_uuid)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.post("/create")
async def api_create_dataset(
        data: RequestCreateDataset,
        db: AsyncSession = Depends(get_db_session)):
    try:

        dataset = make_dataset(data)
        # print(dataset)
        dataset, exception = await create_dataset(db, dataset)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseCreateDataset(dataset=dataset)

    return res


@router.patch("/patch/{dataset_uuid}")
async def api_patch_dataset(
        dataset_uuid: str,  # 接收路径参数 dataset_uuid
        data: RequestPatchDataset,
        db: AsyncSession = Depends(get_db_session)):
    try:

        update_data = data.dict(exclude_unset=True)
        # print(dataset_uuid, update_data)

        dataset, exception = await patch_dataset(db, dataset_uuid, update_data)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponsePatchDataset(dataset=dataset)

    return res


@router.delete("/delete/{dataset_uuid}")
async def api_delete_dataset(
        dataset_uuid: str,  # 接收路径参数 dataset_uuid
        db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = 1
        result, exception = await soft_delete_dataset(db, user_id, dataset_uuid)
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseDeleteDataset(result=result)

    return res
