from typing import Tuple, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import logger
from app.database.deps import get_async_db_session_dep, get_sync_db_session_dep
from app.schemas.brainx.demo.format import DemoStructuredUserInfo, ResponseDemoFormatQuery
from app.service.brainx.service import BrainXService


async def demo_struct_output_invoke(
        question: str, llm: str,
        tenant_uuid: str,
        sync_db: Session = Depends(get_sync_db_session_dep),
):
    service_brain_x = BrainXService(
        tenant_uuid=tenant_uuid,
        llm=llm,
        sync_db=sync_db,
        streaming=False,
    )

    template = """
        Answer the user query in the following format:
       
       {format_instructions}
       
       {query}
       
       基于以上的描述，请直接返回我要的json结果，不要其他的额外文字信息，我只要json格式!!!
       
       """

    return service_brain_x.llm_model_instance.llm_invoke(
        query={
            "query": question,
        },
        temperature=0.1,
        template=template,
        output_schemas=DemoStructuredUserInfo
    )


async def demo_str_output_invoke(
        sync_db: Session,
        tenant_uuid: str,
        question: str,
        provider_id: str = None, model_id: str = None,
) -> Tuple[Any, Exception | None]:
    try:
        service_brain_x = BrainXService(
            tenant_uuid=tenant_uuid,
            provider_id=provider_id,
            model_id=model_id,
            sync_db=sync_db,
            streaming=False,
        )

        background = "你是一位HR分析师"

        template = """
        {background}
        {query}
        {output}
        """

        output = "请给我一份简单的简历格式"

        res, exception = service_brain_x.llm_model_instance.llm_invoke(
            query={
                "background": background,
                "query": question,
                "output": output,
            },
            template=template,
        )

        if exception:
            raise exception

    except Exception as e:
        logger.error(e, exc_info=True)
        return None, e

    return res, None


async def demo_str_output_completion(
        question: str, llm: str,
        sync_db: Session = Depends(get_sync_db_session_dep),
) -> Tuple[Any, Exception | None]:
    service_brain_x = BrainXService(
        llm=llm,
        sync_db=sync_db,
        streaming=False,
    )

    return service_brain_x.completion(
        query=question
    )
