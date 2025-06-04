from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.middleware.auth import get_session_user
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.database.deps import get_sync_db_session_dep
from app.models import User
from app.schemas.base import ResponseSchema
from app.schemas.model_provider.provider_model import ResponseGetProviderModelList, RequestGetProviderModelList, RequestSaveModel, ResponseSaveModel
from app.service.model_provider.provider_model_service import ProviderModelService

router = APIRouter()


@router.get("/list")
async def api_get_provider_model_list(
        request: RequestGetProviderModelList,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),

) -> ResponseGetProviderModelList | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    model_provider_service = ProviderModelService(sync_db=sync_db)
    models = model_provider_service.get_models_by_provider(tenant_uuid=tenant_uuid, provider_id=request.provider_id)

    return ResponseGetProviderModelList(data=models)


@router.post("/save")
async def api_save_model(
        request: RequestSaveModel,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseSaveModel | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)

    if request.load_balancing and request.load_balancing.enable:
        pass

    else:
        provider_model_service = ProviderModelService(sync_db=sync_db)
        model_type = ModelType(request.model_type)
        model_provider, exception = provider_model_service.save_model_credentials(
            tenant_uuid=tenant_uuid,
            provider=request.provider,
            model=request.model,
            model_type=model_type,
            credentials=request.credentials,
        )
        if exception:
            raise exception

    return ResponseSaveModel(success=True)
