import http

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import settings
from app.api.middleware.auth import get_session_user
from app.database.deps import get_sync_db_session_dep
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
    question = data.question

    response, exception = await demo_struct_output_invoke(
        tenant_uuid=session_user.tenant_owner_uuid,
        question=question, llm=data.llm,
    )

    if exception:
        raise exception

    return ResponseDemoFormatQuery(data=response)


@router.post("/demo/invoke")
async def api_demo_invoke(
        data: RequestDemoQuery,
        session_user: User = Depends(get_session_user),
        sync_db: Session = Depends(get_sync_db_session_dep)
) -> ResponseDemoQuery | ResponseSchema:
    question = data.question
    tenant_uuid = str(session_user.tenant_owner_uuid)

    response, exception = await demo_str_output_invoke(
        sync_db=sync_db,
        tenant_uuid=tenant_uuid,
        question=question,
        provider_id=data.provider_id,
        model_id=data.model_id,
    )

    if exception:
        raise exception

    return ResponseDemoQuery(data=response)


@router.post("/demo/completion")
async def api_demo_completion(
        data: RequestDemoQuery,
) -> ResponseDemoQuery | ResponseSchema:
    question = data.question
    # print(data.question)

    response, exception = await demo_str_output_completion(
        question=question, llm=data.llm,
    )

    if exception:
        raise exception

    return ResponseDemoQuery(data=response)
