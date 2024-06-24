from enum import Enum
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel, table_name_revenue
from typing import Dict, Union, Any


class RevenueMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_revenue"


DocumentMetadataMap = Dict[Union[RevenueMetadataKeysEnum, str], Any]



class Revenue(BaseModel):

    __tablename__ = table_name_revenue

    month = mapped_column(String(255), nullable=True)
    revenue = mapped_column(Integer, nullable=True)
    # month: str
    # revenue: int

    def __init__(self, month: str, revenue: int):
        super().__init__()
        self.month = month
        self.revenue = revenue



