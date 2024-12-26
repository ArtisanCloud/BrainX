"""add pivot app to dataset models

Revision ID: 71100
Revises: 71000
Create Date: 2024-06-15 15:26:49.265388

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app import settings
from app.config.server import ProjectType
from app.models.base import table_name_pivot_app_to_dataset, time_now

# revision identifiers, used by Alembic.
revision: str = '71100'
down_revision: Union[str, None] = '71000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_pivot_app_to_dataset,  # 替换为你的实际表名
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('app_uuid', sa.UUID(), nullable=False, index=True),
        sa.Column('dataset_uuid', sa.UUID(), nullable=False, index=True),
        # 可选: 添加主键约束，可以根据需要决定是否使用组合键作为主键
        sa.PrimaryKeyConstraint('app_uuid', 'dataset_uuid', name='pivot_app_to_dataset_pkey'),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=time_now(), nullable=False),
        schema=settings.database.db_schema
    )


def downgrade() -> None:
    op.drop_table(table_name_pivot_app_to_dataset, schema=settings.database.db_schema, if_exists=True)
