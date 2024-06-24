from typing import List, Dict, Any
from app.schemas.base import BaseSchema
from pydantic import SkipValidation

from app.schemas.question_answer.schema import ImageDocument


# Visual Question Answer
class RequestVisualSearch(BaseSchema):
    question_image: str
    llm: str


class ResponseVisualSearch(BaseSchema):
    image_documents: SkipValidation[List[ImageDocument]]


