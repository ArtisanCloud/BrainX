from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel, table_name_invoice
from typing import Dict, Union, Any


class InvoiceMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """

    SEC_DOCUMENT = "sec_invoice"


DocumentMetadataMap = Dict[Union[InvoiceMetadataKeysEnum, str], Any]




class Invoice(BaseModel):
    __tablename__ = table_name_invoice

    user_id = mapped_column('User_id', String(255))
    amount = mapped_column('Amount', String)
    status = mapped_column('Status', String)
    date = mapped_column('Date', String)
    name = mapped_column('Name', String)
    email = mapped_column('Email', String)
    image_url = mapped_column('Image_url', String)

    def __init__(self,
                 user_id: str,
                 amount: str,
                 status: str,
                 date: str,
                 name: str,
                 email: str,
                 image_url: str
                 ):
        super().__init__()
        self.user_id = user_id
        self.amount = amount
        self.status = status
        self.date = date
        self.name = name
        self.email = email
        self.image_url = image_url
