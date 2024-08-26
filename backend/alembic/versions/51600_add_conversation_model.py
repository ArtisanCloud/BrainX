"""add conversation models

Revision ID: 51600
Revises: 51500
Create Date: 2024-07-06 22:53:03.223522

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models.base import table_name_user, table_name_app, table_name_app_model_config
from app.models.robot_chat.conversation import table_name_conversation
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision: str = '51600'
down_revision: Union[str, None] = '51500'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_conversation,
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('user_uuid', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('app_uuid', UUID(as_uuid=True), nullable=True),
        sa.Column('app_model_config_uuid', UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=True),
        sa.Column('context', sa.Text(), nullable=True),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),

        # 添加索引
        sa.Index('idx_conversation_app_uuid', 'app_uuid'),
        sa.Index('idx_conversation_model_provider_uuid', 'app_model_config_uuid'),

        sa.ForeignKeyConstraint(['user_uuid'], [table_name_user + '.uuid']),
        sa.ForeignKeyConstraint(['app_uuid'], [table_name_app + '.uuid']),
        sa.ForeignKeyConstraint(['app_model_config_uuid'], [table_name_app_model_config + '.uuid']),
    )


def downgrade() -> None:
    op.drop_table(table_name_conversation)
