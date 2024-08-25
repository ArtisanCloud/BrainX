from enum import IntEnum
from typing import List

from sqlalchemy import Text, String, SmallInteger, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.app.app_model_config import table_name_app_model_config
from app.models.base import BaseORM, table_name_app, table_name_user
from app.models.tenant.tenant import table_name_tenant
from app.models.workflow.workflow import table_name_workflow


class AppStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3


class AppType(IntEnum):
    BOT = 1
    AGENT = 2


class AppMode(IntEnum):
    SINGLE_AGENT = 1
    MULTI_AGENT = 2


class App(BaseORM):
    __tablename__ = table_name_app

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_user + '.uuid'), nullable=True)
    app_model_config_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_app_model_config + '.uuid'))
    workflow_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(table_name_workflow + '.uuid'))
    name = mapped_column(String)
    status = mapped_column(SmallInteger)
    type = mapped_column(SmallInteger)
    mode = mapped_column(SmallInteger)
    description = mapped_column(String)
    persona = mapped_column(Text)
    avatar_url = mapped_column(String)
    is_public = mapped_column(Boolean)

    # 定义与 AppModelConfig 的关系
    app_model_configs: Mapped[List["AppModelConfig"]] = relationship(back_populates="app",
                                                                     foreign_keys="[AppModelConfig.app_uuid]")
    current_app_model_config: Mapped["AppModelConfig"] = relationship(back_populates="current_selected_app",
                                                                      foreign_keys=[app_model_config_uuid],
                                                                      uselist=False)

    tenant: Mapped["Tenant"] = relationship(back_populates="apps")
    workflow: Mapped["Workflow"] = relationship(back_populates="app", foreign_keys=[workflow_uuid])

    # conversations = relationship("Conversation", backref="app")
    # groups = relationship("Group", backref="app")

    def __repr__(self):
        # 使用三元运算符来处理可能的 None 值
        description = self.description[:10] + '...' if self.description is not None else 'No description'

        return (
            f"<App("
            # f"id={self.id}, "
            f"uuid={self.uuid}, "
            f"name='{self.name}', "
            f"workflow_uuid='{self.workflow_uuid}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"status={self.status}, "
            f"type={self.type}, "
            f"mode={self.mode}, "
            f"description='{description}', "
            f"persona='{self.persona}', "
            f"avatar_url='{self.avatar_url}', "
            f"is_public={self.is_public})>"
        )
