from sqlalchemy import TIMESTAMP, BigInteger, select, PrimaryKeyConstraint, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from enum import IntEnum, Enum

from pytz import timezone
from datetime import datetime
import uuid as uuid

from sqlalchemy.orm import declarative_base, mapped_column

from app.database.deps import get_async_db_session

UTC = timezone('UTC')


def time_now():
    return datetime.now(UTC)


class BaseStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3


class PlatformSourceType(Enum):
    WEB = 'web'
    MOBILE = 'mobile'


Base = declarative_base()


class BaseORM(Base):
    __abstract__ = True

    """Base class for all db orm models"""
    # id = mapped_column(BigInteger, autoincrement=True)
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    created_at = mapped_column(TIMESTAMP(timezone=True), default=time_now, nullable=False)
    updated_at = mapped_column(TIMESTAMP(timezone=True), default=time_now, onupdate=time_now, nullable=False)
    deleted_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    def __repr__(self):
        return (f"id: "
                # f"{self.id},"
                f" uuid:{self.uuid}, created_at: {self.created_at}, updated_at:{self.updated_at}, deleted_at:{self.deleted_at}")

    @classmethod
    def get_by_uuid(cls, uuid):
        stmt = select(cls).filter(cls.uuid == uuid, cls.deleted_at.is_(None)).first()
        db: AsyncSession = get_async_db_session()
        return db.execute(stmt)

    @classmethod
    def get_by_id(cls, id):
        stmt = select(cls).filter(cls.id == id, cls.deleted_at.is_(None)).first()
        db: AsyncSession = get_async_db_session()
        return db.execute(stmt)


class BasePivotModel(Base):
    __abstract__ = True

    """Base class for all db orm models"""
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)

    created_at = mapped_column(TIMESTAMP(timezone=True), default=time_now, nullable=False)

    # updated_at = mapped_column(TIMESTAMP(timezone=True), default=time_now, onupdate=time_now, nullable=False)
    # deleted_at = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    def __repr__(self):
        return (f"created_at: {self.created_at}, "
                # f"updated_at:{self.updated_at}, "
                # f"deleted_at:{self.deleted_at}"
                )

    def generate_uuid(self):
        self.uuid = uuid.uuid4()


table_name_tenant = "tenants"
table_name_user = "users"
table_name_media_resource = 'media_resources'
table_name_pivot_tenant_to_user = "pivot_tenant_to_user"
table_name_revenue = 'revenue'
table_name_invoice = 'invoice'
table_name_app = "apps"
table_name_conversation = 'conversations'
table_name_message = 'messages'
table_name_workflow = "workflows"
table_name_dataset = "datasets"
table_name_dataset_segment_rule = "dataset_segment_rules"
table_name_document = "documents"
table_name_document_segment = "document_segments"
table_name_embedding = "embeddings"
table_name_customer = "tenant"
table_name_app_model_config = 'app_model_configs'
table_name_model_provider = "model_providers"
table_name_image_embedding = 'data_image_embedding'
table_name_tenant_default_model = "tenant_default_models"
