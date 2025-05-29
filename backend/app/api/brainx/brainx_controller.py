import http

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import settings
from app.api.middleware.auth import get_session_user
from app.database.deps import get_async_db_session_dep, get_sync_db_session_dep
from app.logger import logger
from app.models import User
from app.schemas.base import ResponseSchema
from app.schemas.brainx.demo.format import ResponseDemoFormatQuery
from app.schemas.brainx.demo.string import RequestDemoQuery, ResponseDemoQuery
from app.service.brainx.demo import demo_str_output_completion, demo_struct_output_invoke, \
    demo_str_output_invoke

router = APIRouter()


@router.post("/demo/format-output-invoke")
async def api_demo_format_output_invoke(
        data: RequestDemoQuery,
        session_user: User = Depends(get_session_user),
) -> ResponseDemoFormatQuery | ResponseSchema:
    try:
        question = data.question

        response, exception = await demo_struct_output_invoke(
            tenant_uuid=session_user.tenant_owner_uuid,
            question=question, llm=data.llm,
        )

        return ResponseDemoFormatQuery(data=response)

    except Exception as e:
        logger.error(f"Failed to brainx format output: {e}", exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)


@router.post("/demo/invoke")
async def api_demo_invoke(
        data: RequestDemoQuery,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep)
) -> ResponseDemoQuery | ResponseSchema:
    try:
        # print(session_user.tenant_owner_uuid)
        question = data.question
        tenant_uuid = str(session_user.tenant_owner_uuid)
        
        response, exception = await demo_str_output_invoke(
            sync_db=sync_db,
            tenant_uuid=tenant_uuid,
            question=question,
            llm=data.llm,
        )

        return ResponseDemoQuery(data=response)

    except Exception as e:
        logger.error(f"Failed to brainx format output: {e}", exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)


@router.post("/demo/completion")
async def api_demo_completion(
        data: RequestDemoQuery,
) -> ResponseDemoQuery | ResponseSchema:
    try:
        question = data.question
        # print(data.question)

        response, exception = await demo_str_output_completion(
            question=question, llm=data.llm,
        )

        return ResponseDemoQuery(data=response)

    except Exception as e:
        logger.error(f"Failed to brainx format output: {e}", exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)
