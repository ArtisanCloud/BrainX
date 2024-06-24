from enum import IntEnum

from sqlalchemy import Column, String, SmallInteger, BigInteger, Text, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models.app_model_config import table_name_app_model_config, AppModelConfig
from app.models.base import BaseModel, table_name_app
from app.models.tenant import table_name_tenant, Tenant
from app.models.workflow import table_name_workflow, Workflow


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


class App(BaseModel):
    __tablename__ = table_name_app

    workflow_uuid = mapped_column('workflow_uuid', UUID, ForeignKey(table_name_workflow + '.uuid'))
    tenant_uuid = mapped_column('tenant_uuid', UUID, ForeignKey(table_name_tenant + '.uuid'))

    name = mapped_column('name', String)
    status = mapped_column('status', SmallInteger)
    type = mapped_column('type', SmallInteger)
    mode = mapped_column('mode', SmallInteger)
    description = mapped_column('description', String)
    avatar_url = mapped_column('avatar_url', String)
    is_public = mapped_column('is_public', Boolean)

    # 定义与 AppModelConfig 的关系
    # model_config:Mapped["AppModelConfig"] = relationship( back_populates="app")
    # tenant:Mapped[Tenant] = relationship(back_populates="app")
    # workflow:Mapped[Workflow] = relationship(back_populates="app")

    # conversations = relationship("Conversation", backref="app")
    # groups = relationship("Group", backref="app")

    def __repr__(self):
        # 使用三元运算符来处理可能的 None 值
        description = self.description[:10] + '...' if self.description is not None else 'No description'

        return (
            f"<App(id={self.id}, "
            f"name='{self.name}', "
            f"workflow_uuid='{self.workflow_uuid}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"status={self.status}, "
            f"type={self.type}, "
            f"mode={self.mode}, "
            f"description='{description}', "
            f"avatar_url='{self.avatar_url}', "
            f"is_public={self.is_public})>"
        )
