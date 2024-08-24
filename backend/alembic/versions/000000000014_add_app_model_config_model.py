"""add app models config  models

Revision ID: 000000000014
Revises: 000000000015
Create Date: 2024-06-15 15:33:28.987223

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.app.app_model_config import table_name_app_model_config

# revision identifiers, used by Alembic.
revision: str = '000000000014'
down_revision: Union[str, None] = '000000000013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_app_model_config,  # 使用表名
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('app_uuid', sa.UUID(), nullable=False, index=True),
        sa.Column('model_provider_uuid', sa.UUID(), nullable=True, index=True),
        sa.Column('configs', sa.Text(), nullable=True),
        sa.Column('persona_prompt', sa.Text(), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),

        # 添加索引
        sa.Index('idx_app_model_config_app_uuid', 'app_uuid'),
        sa.Index('idx_app_model_config_model_provider_uuid', 'model_provider_uuid')
    )


def downgrade() -> None:
    op.drop_table(table_name_app_model_config)
