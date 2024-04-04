from enum import Enum
from .base import Base
from typing import List, Optional, Dict, Union, Any


class InvoiceMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_invoice"


DocumentMetadataMap = Dict[Union[InvoiceMetadataKeysEnum, str], Any]

class Invoice(Base):
    customer_id: int
    amount: int
    status: str
    date: str
    name: str
    email: str
    image_url: str
