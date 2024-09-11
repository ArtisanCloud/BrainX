from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Any, Optional

from app.schemas.base import BaseSchema


class BlockType(Enum):
    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"


class Block(BaseSchema):
    block_id: Optional[str] = None
    # start: int
    # end: int
    type: str
    text: str = ""  # 默认值为空字符串
    image: Optional[Any] = None
    table: Optional[Any] = None
    rect: list = ()
    page_number: int = 0


class BaseDataExtractor(ABC):
    """
    Define the parser interface.
    """
    doc: Any = None

    @abstractmethod
    def extract(self) -> List[Block]:
        raise NotImplementedError
