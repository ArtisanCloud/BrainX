from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.middleware.auth import get_session_user
from app.core.brainx.entity.runtime.provider_model import ModelType
from app.database.deps import get_sync_db_session_dep
from app.models import User
from app.schemas.base import ResponseSchema
from app.schemas.model_provider.provider_model import ResponseGetProviderModelList, RequestGetProviderModelList, RequestSaveModel, ResponseSaveModel, RequestChangeModelStatus, \
    ResponseChangeModelStatus, RequestDeleteModel, ResponseDeleteModel, RequestGetModelCredentials, ResponseGetModelCredentials, ResponseGetModelsByModelType, ResponseGetDefaultModelByModelType, \
    RequestUpdateDefaultModels, ResponseUpdateDefaultModels, ResponseGetModelParameterRule, RequestGetModelParameterRule
from app.service.model_provider.provider_model_service import ProviderModelService

router = APIRouter()


@router.post("/list")
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

    return ResponseSaveModel(result=True)


@router.patch("/status")
async def api_change_model_status(
        request: RequestChangeModelStatus,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseChangeModelStatus | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)

    provider_model_service = ProviderModelService(sync_db=sync_db)
    provider_model_service.change_status(
        tenant_uuid=tenant_uuid,
        provider=request.provider,
        model_type=request.model_type,
        model_id=request.model,
        status=request.status,
    )

    return ResponseChangeModelStatus(result=True)


@router.post("/get_model_credentials")
async def api_get_model_credentials(
        request: RequestGetModelCredentials,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetModelCredentials | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)

    credentials, exception = provider_model_service.get_model_credentials(
        tenant_uuid=tenant_uuid,
        provider=request.provider,
        model_type=request.model_type,
        model=request.model,
    )
    if exception:
        raise exception

    res = ResponseGetModelCredentials(data=credentials)
    return res


@router.delete("/delete")
async def api_delete_model(
        request: RequestDeleteModel,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseDeleteModel | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)

    provider_model_service.delete_model(
        tenant_uuid=tenant_uuid, provider_id=request.provider,
        model_type=request.model_type, model_id=request.model,
    )

    res = ResponseDeleteModel(result=True)

    return res


@router.get("/model-types/{model_type}")
async def api_get_models_by_type(
        model_type: str,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetModelsByModelType | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)

    models = provider_model_service.get_models_by_model_type(tenant_uuid=tenant_uuid, model_type=model_type)
    return ResponseGetModelsByModelType(data=models)


@router.get("/default-model/{model_type}")
async def api_get_default_model(
        model_type: str,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetDefaultModelByModelType | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)
    models = provider_model_service.get_default_model_of_model_type(tenant_uuid=tenant_uuid, model_type=model_type)
    return ResponseGetDefaultModelByModelType(data=models)


@router.post("/default-model")
async def api_update_default_model(
        request: RequestUpdateDefaultModels,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseUpdateDefaultModels | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)
    # print(request.model_settings)
    for model_setting in request.model_settings:
        if model_setting.provider is None:
            continue
        if model_setting.model is None:
            raise ValueError("invalid model")
        # print(model_setting.model_type, model_setting.provider, model_setting.model)
        models, exception = provider_model_service.update_default_model_of_model_type(
            tenant_uuid=tenant_uuid,
            model_type=model_setting.model_type,
            provider=model_setting.provider,
            model=model_setting.model,
        )
        if exception:
            raise exception

    return ResponseUpdateDefaultModels(result=True)


@router.post("/model-parameter-rule")
async def api_model_parameter_rule(
        request: RequestGetModelParameterRule,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> ResponseGetModelParameterRule | ResponseSchema:
    tenant_uuid = str(session_user.tenant_owner_uuid)
    provider_model_service = ProviderModelService(sync_db=sync_db)
    parameter_rules = provider_model_service.get_model_parameter_rules(
        tenant_uuid=tenant_uuid,
        provider=request.provider,
        model=request.model,
    )
    return ResponseGetModelParameterRule(data=parameter_rules)
