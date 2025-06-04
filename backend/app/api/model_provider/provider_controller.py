import http

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.middleware.auth import get_session_user
from app.core.brainx.providers.registry import ModelProviderRegistry
from app.database.deps import get_sync_db_session_dep
from app.logger import logger

from app.config.config import settings
from app.models.originaztion.user import User
from app.schemas.base import ResponseSchema
from app.schemas.model_provider.provider import (
    RequestCreateModelProvider,
    ResponseCreateModelProvider,
    ResponseGetModelProviderList, RequestDeleteModelProvider, ResponseDeleteModelProvider, ResponseGetProviderCredentials, RequestGetProviderCredentials,
)
from app.service.model_provider.provider_service import ProviderService

router = APIRouter()


@router.get("/list")
async def api_get_model_provider_list(
        request: Request,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetModelProviderList | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    dataset_uuid = request.query_params.get("model_type", None)

    provider_service = ProviderService(sync_db=sync_db)

    providers, exception = provider_service.get_provider_list(tenant_uuid=tenant_uuid, model_type=dataset_uuid)
    if exception is not None:
        raise exception

    # print(providers)
    res = ResponseGetModelProviderList(data=providers)

    return res


@router.get("/icon/{provider}/{icon}/{lang}")
async def api_get_model_provider_icon(
        request: Request,
        provider: str,  # 路径参数：provider
        icon: str,  # 路径参数：icon
        lang: str,  # 路径参数：lang
) -> ResponseGetModelProviderList | ResponseSchema:
    icon_path, mimetype, exception = (
        ModelProviderRegistry().get_model_provider_icon(
            provider=provider,
            icon_type=icon,
            lang=lang,
        )
    )
    if exception:
        raise exception

    # print(icon_path, mimetype)
    return FileResponse(media_type=mimetype, path=icon_path)


@router.post("/save")
async def api_save_model_provider(
        request: RequestCreateModelProvider,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseCreateModelProvider | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_service = ProviderService(sync_db=sync_db)
    model_provider, exception = provider_service.save_model_provider_credentials(
        tenant_uuid=tenant_uuid,
        provider=request.provider,
        credentials=request.credentials,
    )
    if exception:
        raise exception

    res = ResponseCreateModelProvider(result=True)

    return res


@router.post("/get_provider_credentials")
async def api_get_model_provider_credentials(
        request: RequestGetProviderCredentials,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetProviderCredentials | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_service = ProviderService(sync_db=sync_db)

    credentials, exception = provider_service.get_provider_credentials(tenant_uuid=tenant_uuid, provider_id=request.provider)
    if exception:
        raise exception

    res = ResponseGetProviderCredentials(data=credentials)
    return res


@router.delete("/delete")
async def api_delete_model_provider(
        request: RequestDeleteModelProvider,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseDeleteModelProvider | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_service = ProviderService(sync_db=sync_db)

    provider_service.delete_provider(tenant_uuid=tenant_uuid, provider_id=request.provider)

    res = ResponseDeleteModelProvider(result=True)

    return res
