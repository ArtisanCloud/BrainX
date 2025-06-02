from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.middleware.auth import get_session_user
from app.database.deps import get_sync_db_session_dep
from app.models import User
from app.schemas.base import ResponseSchema
from app.schemas.model_provider.provider_model import ResponseGetProviderModelList, RequestGetProviderModelList
from app.service.model_provider.provider_model_service import ProviderModelService

router = APIRouter()


@router.get("/list")
async def get_provider_model_list(
        request: RequestGetProviderModelList,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),

) -> ResponseGetProviderModelList | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    model_provider_service = ProviderModelService(sync_db=sync_db)
    models, exception = model_provider_service.get_models_by_provider(tenant_uuid=tenant_uuid, provider_id=request.provider_id)
    if exception:
        raise exception

    return ResponseGetProviderModelList(data=models)
