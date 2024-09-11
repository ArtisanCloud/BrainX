from typing import Dict, Any, Optional
from pydantic import SkipValidation

from app.schemas.base import BaseSchema


class Document(BaseSchema):
    text: Optional[str]
    node_id: Optional[str]
    similarity: Optional[float] = 0.1
    metadata: Optional[Dict[str, Any]] = None


class ImageDocument(BaseSchema):
    image: Optional[str] = None
    relative_document: Optional[Document] = None
