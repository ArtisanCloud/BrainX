import http

from fastapi import APIRouter

from app import settings
from app.logger import logger
from app.schemas.base import ResponseSchema
from app.schemas.brainx.demo.format import ResponseDemoFormatQuery
from app.schemas.brainx.demo.string import RequestDemoQuery, ResponseDemoQuery
from app.service.brainx.demo import demo_str_output_completion, demo_struct_output_invoke, \
    demo_str_output_invoke

router = APIRouter()


@router.post("/demo/format-output-invoke")
async def api_demo_format_output_invoke(
        data: RequestDemoQuery,
) -> ResponseDemoFormatQuery | ResponseSchema:
    try:
        question = data.question

        response, exception = await demo_struct_output_invoke(
            question=question, llm=data.llm,
        )

        return ResponseDemoFormatQuery(data=response)

    except Exception as e:
        logger.error(f"Failed to brainx format output: {e}", exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)


@router.post("/demo/invoke")
async def api_demo_invoke(
        data: RequestDemoQuery,
) -> ResponseDemoQuery | ResponseSchema:
    try:
        question = data.question

        response, exception = await demo_str_output_invoke(
            question=question, llm=data.llm,
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
