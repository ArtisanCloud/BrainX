from enum import Enum
import uuid
from typing import List, Optional, Dict, Union, Any

from sqlalchemy import Column, String, UUID, BigInteger, Integer, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column

from app.models.base import BaseORM, table_name_customer


class ExternalId(BaseORM):
    __tablename__ = 'external_id'
    __table_args__ = {'schema': 'public'}  # 动态指定 schema

    open_id_in_mini_program = mapped_column(String)
    open_id_in_we_chat_official_account = mapped_column(String)
    open_id_in_we_com = mapped_column(String)


class CustomerMetadataKeysEnum(str, Enum):
    """
    Enum for the keys of the metadata map for a document
    """
    SEC_DOCUMENT = "sec_customer"


DocumentMetadataMap = Dict[Union[CustomerMetadataKeysEnum, str], Any]




class Customer(BaseORM):
    __tablename__ = table_name_customer
    __table_args__ = {'schema': 'public'}  # 动态指定 schema

    name = mapped_column(String)
    mobile = mapped_column(String, unique=True, nullable=False)
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    password = mapped_column(String)
    email = mapped_column(String)
    # inviter_id = mapped_column(BigInteger, ForeignKey('tenant.id'))
    mgm_id = mapped_column(Integer)
    invite_code = mapped_column(String)
    source = mapped_column(Integer)
    type = mapped_column(Integer)
    is_activated = mapped_column(Boolean, default=False)

    # inviter = relationship('Customer', remote_side=[id])

    def __repr__(self):
        return f"uuid: {self.uuid}, name: {self.name}, mobile: {self.mobile}"
