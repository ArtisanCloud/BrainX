"""add pivot tenant to tenant model

Revision ID: 000000000003
Revises: 000000000020
Create Date: 2024-06-15 15:26:49.265388

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.base import BaseModel, table_name_pivot_tenant_to_user

# revision identifiers, used by Alembic.
revision: str = '000000000003'
down_revision: Union[str, None] = '000000000002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_pivot_tenant_to_user,  # 替换为你的实际表名
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', sa.UUID(), nullable=False, index=True),
        sa.Column('user_uuid', sa.UUID(), nullable=False, index=True),
        # 可选: 添加主键约束，可以根据需要决定是否使用组合键作为主键
        sa.PrimaryKeyConstraint('tenant_uuid', 'user_uuid', name='pivot_tenant_to_user_pkey'),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
    )


def downgrade() -> None:
    op.drop_table(table_name_pivot_tenant_to_user)
