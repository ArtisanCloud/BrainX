from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, List, Any, Optional

from pydantic import BaseModel

from app.models.rag.document_segment import DocumentSegment


class BlockType(Enum):
    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"


class Block(BaseModel):
    block_id: Optional[str] = None
    # start: int
    # end: int
    type: str
    text: str = ""  # 默认值为空字符串
    image: Optional[Any] = None
    table: Optional[Any] = None
    rect: list
    page_number: int

    class Config:
        arbitrary_types_allowed = True


class BaseDataExtractor(ABC):
    """
    Define the parser interface.
    """
    doc: Any = None

    @abstractmethod
    def extract(self) -> List[Block]:
        raise NotImplementedError
