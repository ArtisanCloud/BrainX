from typing import List, Dict, Any
from app.schemas.base import BaseSchema
from pydantic import SkipValidation

from app.schemas.question_answer.schema import ImageDocument


# Visual Question Answer

class RequestVisualQuery(BaseSchema):
    question: str
    question_image: str
    llm: str


class ResponseVisualQuery(BaseSchema):
    answer: str

