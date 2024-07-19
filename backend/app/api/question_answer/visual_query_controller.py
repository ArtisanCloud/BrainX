import http

from fastapi import Depends, APIRouter



from app.schemas.base import ResponseSchema
from app.schemas.question_answer.visual_query import RequestVisualQuery, ResponseVisualQuery
from app.service.question_answer.visual_query import visual_query

router = APIRouter()


@router.post("/visual_query")
async def api_visual_query(
        query: RequestVisualQuery,
) -> ResponseVisualQuery | ResponseSchema:
    """
    query question_answer by text
    """

    try:
        base64Image = query.question_image
        if base64Image.startswith('data:') and 'base64,' in base64Image:
            # Remove the prefix
            base64Image = base64Image.split('base64,')[1]

        res, exception = await visual_query(base64Image, query.question)
        # print(res, exception)
        if exception:
            raise exception
        return res

    except Exception as e:
        # 在这里处理异常，您可以记录日志、返回特定的错误响应等
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)
