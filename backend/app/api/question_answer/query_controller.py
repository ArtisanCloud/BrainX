import http

from fastapi import Depends, APIRouter


from app.api.context_manager import build_request_context
from app.schemas.base import ResponseSchema
from app.schemas.question_answer.query import RequestQuery, ResponseQuery

from app.service.question_answer.query import query_by_text

router = APIRouter()


@router.post("/query")
async def api_query(
        query: RequestQuery,
        _=Depends(build_request_context)
) -> ResponseQuery | ResponseSchema:
    """
    query question_answer by text
    """

    # print(db)
    question = query.question
    # print(question)
    llm = 'default'
    if query.llm is not None:
        llm = query.llm

    try:
        answer = await query_by_text(question, llm)

        return answer

    except Exception as e:
        # 在这里处理异常，您可以记录日志、返回特定的错误响应等
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)
