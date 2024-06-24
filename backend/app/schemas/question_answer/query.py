from typing import List
from app.schemas.base import BaseSchema
from pydantic import SkipValidation

from app.schemas.question_answer.schema import Document


# Question Answer
class RequestQuery(BaseSchema):
    question: str
    llm: str


class ResponseQuery(BaseSchema):
    answer: str
    documents: SkipValidation[List[Document]]


# Visual Search
