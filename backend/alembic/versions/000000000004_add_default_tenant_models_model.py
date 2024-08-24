"""add default tenant models  models

Revision ID: 000000000004
Revises: 000000000020
Create Date: 2024-06-15 15:29:48.824905

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

from app.models.tenant.tenant import table_name_tenant_default_model

# revision identifiers, used by Alembic.
revision: str = '000000000004'
down_revision: Union[str, None] = '000000000003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        table_name_tenant_default_model,  # 替换为你的实际表名
        # sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('uuid', UUID(as_uuid=True), nullable=False, index=True, unique=True),

        sa.Column('tenant_uuid', sa.String(), nullable=False),
        sa.Column('provider_name', sa.String(40), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(40), nullable=False),

        sa.Column('created_at', sa.TIMESTAMP(timezone=True), default=datetime.UTC, nullable=False),
        sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table(table_name_tenant_default_model)
