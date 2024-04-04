from enum import Enum
from .base import Base
from typing import List, Optional, Dict, Union, Any


class RevenueMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_revenue"


DocumentMetadataMap = Dict[Union[RevenueMetadataKeysEnum, str], Any]

class Revenue(Base):
    month: str
    revenue: int
