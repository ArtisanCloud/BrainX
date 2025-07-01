"""add tenant preferred model provider  models

Revision ID: 14100
Revises: 14000
Create Date: 2024-06-15 15:29:48.824905

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app import settings
from app.models.base import time_now
from app.models.tenant.tenant import table_name_tenant_preferred_model_provider

# revision identifiers, used by Alembic.
revision: str = '14100'
down_revision: Union[str, None] = '14000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_tenant_preferred_model_provider,  # 替换为你的实际表名
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('provider_name', sa.String, nullable=False),
        sa.Column('preferred_provider_type', sa.String(40), nullable=False),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=time_now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), default=time_now(), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), default=None, nullable=True),
        sa.PrimaryKeyConstraint('uuid'),
        schema=settings.database.db_schema
    )


def downgrade() -> None:
    op.drop_table(table_name_tenant_preferred_model_provider, schema=settings.database.db_schema, if_exists=True)
