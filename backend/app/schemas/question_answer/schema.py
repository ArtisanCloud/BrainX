from typing import Dict, Any
from pydantic import SkipValidation

from app.schemas.base import BaseSchema


class Document(BaseSchema):
    text: str
    node_id: str
    similarity: SkipValidation[float]
    metadata: Dict[str, Any]


class ImageDocument(BaseSchema):
    image: str
    relative_document: SkipValidation[Document]
