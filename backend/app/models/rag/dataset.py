from sqlalchemy import Column, String, SmallInteger, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship, mapped_column
from app.models.base import BaseModel, table_name_dataset, table_name_tenant, table_name_user
from app.models.app import table_name_app

__tablename__ = table_name_app


class Dataset(BaseModel):
    __tablename__ = table_name_dataset  # 替换为实际的表名

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)

    name = mapped_column(String)
    description = mapped_column(String)
    is_published = mapped_column(Boolean)

    embedding_model = mapped_column(String(255))
    embedding_model_provider = mapped_column(String(255))

    app = relationship("App", back_populates="datasets")

    def __repr__(self):
        description = self.description[:10] + '...' if self.description is not None else 'No description'
        return (
            f"<Dataset(id={self.id}, "
            f"uuid={self.uuid}, "
            f"name='{self.name}', "
            f"app_uuid='{self.app_uuid}', "
            f"description='{description}', "
            f"is_public={self.is_public})>"
        )
