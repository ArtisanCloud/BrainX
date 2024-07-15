from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.models.base import BaseModel, table_name_dataset, table_name_tenant, table_name_user
from app.models.app.app import table_name_app
from enum import IntEnum

__tablename__ = table_name_app


class IndexingDriverType(IntEnum):
    LANGCHAIN = 1
    LLAMAINDEX = 2


class Dataset(BaseModel):
    __tablename__ = table_name_dataset  # 替换为实际的表名

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)

    name = mapped_column(String)
    description = mapped_column(String)
    is_published = mapped_column(Boolean)

    driver_type = mapped_column(SmallInteger, nullable=False, enum=IndexingDriverType)  # 使用枚举类型定义

    embedding_model = mapped_column(String(255))
    embedding_model_provider = mapped_column(String(255))

    tenant: Mapped["Tenant"] = relationship(back_populates="datasets", foreign_keys=[tenant_uuid])
    documents: Mapped["Document"] = relationship(back_populates="dataset", foreign_keys="[Document.dataset_uuid]")

    def __repr__(self):
        description = self.description[:10] + '...' if self.description is not None else 'No description'
        return (
            f"<Dataset(id={self.id}, "
            f"uuid={self.uuid}, "
            f"name='{self.name}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"description='{description}', "
            f"is_published='{self.is_published}', "
            f"indexing_driver_type='{self.indexing_driver_type}', "
            f"embedding_model='{self.embedding_model}', "
            f"embedding_model_provider='{self.embedding_model_provider}', "
            f"is_public={self.is_public})>"
        )
