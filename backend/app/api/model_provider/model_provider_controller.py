import http
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse

from app.api.middleware.auth import get_session_user
from app.database.deps import get_async_db_session_dep
from app.logger import logger

from app.config.config import settings
from app.core.ai_model.model_manager import ModelManager
from app.models.originaztion.user import User
from app.core.rag import FrameworkDriverType
from app.schemas.base import ResponseSchema
from app.schemas.model_provider.provider import (
    RequestCreateModelProvider,
    ResponseCreateModelProvider,
    ResponseGetModelProviderList,
)
from app.service.model_provider.save import save_model_provider

router = APIRouter()


@router.get("/provider-schema/list")
async def api_get_model_provider_list(
        request: Request,
) -> ResponseGetModelProviderList | ResponseSchema:
    try:
        model_manager = ModelManager(
            FrameworkDriverType(settings.agent.framework_driver)
        )
        providers, exception = model_manager.provider_manager.load_provider_schemas()
        if exception is not None:
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

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
    try:
        model_manager = ModelManager(
            FrameworkDriverType(settings.agent.framework_driver)
        )
        icon_path, mimetype, exception = (
            model_manager.provider_manager.get_model_provider_icon(
                provider=provider,
                icon_type=icon,
                lang=lang,
            )
        )
        if exception:
            raise exception

        print(icon_path, mimetype)
        return FileResponse(media_type=mimetype, path=icon_path)
    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)


@router.post("/save")
async def api_save_model_provider(
        request: RequestCreateModelProvider,
        session_user: User = Depends(get_session_user),
        async_db: AsyncSession = Depends(get_async_db_session_dep),
) -> ResponseCreateModelProvider | ResponseSchema:
    try:
        model_provider, exception = await save_model_provider(
            async_db,
            tenant_uuid=session_user.tenant_owner_uuid,
            provider_name=request.provider,
            credentials=request.credentials,
        )
        if exception is not None:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=settings.log.exc_info)
        if isinstance(e, SQLAlchemyError):
            e = Exception("database query: pls check log")
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseCreateModelProvider(result=True)

    return res
