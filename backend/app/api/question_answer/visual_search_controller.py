import http

from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.context_manager import build_request_context
from app.database.deps import get_db_session
from app.schemas.base import ResponseSchema
from app.schemas.question_answer.visual_search import RequestVisualSearch, \
    ResponseVisualSearch
from app.service.question_answer.visual_search import visual_search
from app.utils.image import image_base64_to_embed
from app.core.brain.index import get_visual_search_embedding_model

router = APIRouter()


@router.post("/visual_search")
async def api_visual_search(
        query: RequestVisualSearch,
        _=Depends(build_request_context),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseVisualSearch | ResponseSchema:
    """
    query question_answer by text
    """

    try:

        embedding_model = get_visual_search_embedding_model()

        base64Image = query.question_image
        if base64Image.startswith('data:') and 'base64,' in base64Image:
            # Remove the prefix
            base64Image = base64Image.split('base64,')[1]

        query_embedding = image_base64_to_embed(base64Image, embedding_model)

        res = await visual_search(db, query_embedding)

        return res

    except Exception as e:
        # 在这里处理异常，您可以记录日志、返回特定的错误响应等
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)
