"""create inventory table

Revision ID: c205ef6e535c
Revises: 492eec39b72d
Create Date: 2024-01-11 12:38:21.483909

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'c205ef6e535c'
down_revision = '492eec39b72d'
branch_labels = None
depends_on = None

def create_inventory_table():
    op.create_table(
        "inventory",
        sa.Column("id", UUID, primary_key=True, default=uuid4),
        sa.Column("inventory_name", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("location_stock", sa.String(255), index=True, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )



def upgrade() -> None:
    create_inventory_table()


def downgrade() -> None:
    op.drop_table("inventory")
