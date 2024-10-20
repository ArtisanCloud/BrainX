"""add pivot tenant to user models

Revision ID: 13000
Revises: 12000
Create Date: 2024-06-15 15:26:49.265388

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app import settings
from app.config.server import ProjectType
from app.models.base import table_name_pivot_tenant_to_user

# revision identifiers, used by Alembic.
revision: str = '13000'
down_revision: Union[str, None] = '12000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.create_table(
            table_name_pivot_tenant_to_user,  # 替换为你的实际表名
            sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

            sa.Column('tenant_uuid', sa.UUID(), nullable=False, index=True),
            sa.Column('user_uuid', sa.UUID(), nullable=False, index=True),
            # 可选: 添加主键约束，可以根据需要决定是否使用组合键作为主键
            sa.PrimaryKeyConstraint('tenant_uuid', 'user_uuid', name='pivot_tenant_to_user_pkey'),

            sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
            schema="public"
        )


def downgrade() -> None:
    if settings.server.project_type == ProjectType.Standalone.value:
        op.drop_table(table_name_pivot_tenant_to_user, schema="public")
