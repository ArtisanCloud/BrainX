from enum import Enum
from .base import Base
from typing import List, Optional, Dict, Union, Any


class CustomerMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_customer"


DocumentMetadataMap = Dict[Union[CustomerMetadataKeysEnum, str], Any]

class Customer(Base):
    Id: str
    Name: str
