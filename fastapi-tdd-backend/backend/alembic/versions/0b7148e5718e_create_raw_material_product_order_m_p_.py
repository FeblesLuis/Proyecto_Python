"""create raw_material, product, order, m_p and p_p tables

Revision ID: 0b7148e5718e
Revises: c205ef6e535c
Create Date: 2024-01-14 18:09:20.473519

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '0b7148e5718e'
down_revision = 'c205ef6e535c'
branch_labels = None
depends_on = None


def create_raw_material_table():
    op.create_table(
        'raw_material',
        sa.Column('id', UUID, primary_key=True, default=uuid4()),
        sa.Column('raw_material_name', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('type', sa.String(255), nullable=True),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('adquisition_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def create_product_table():
    op.create_table(
        'product',
        sa.Column('id', UUID, primary_key=True, default=uuid4()),
        sa.Column('product_name', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('type', sa.String(255), nullable=True),
        sa.Column('description', sa.String(255), nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def create_order_table():
    op.create_table(
        'orders',
        sa.Column('id', UUID, primary_key=True, default=uuid4()),
        sa.Column('orders_name', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('state', sa.String(255), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )


def create_m_p_table():
    op.create_table(
        'm_p',
        sa.Column('id', UUID, primary_key=True, default=uuid4()),
        sa.Column('required_quantity', sa.Integer, nullable=False),
        sa.Column('raw_material_id', UUID, sa.ForeignKey("raw_material.id"), nullable=True),
        sa.Column('product_id', UUID, sa.ForeignKey("product.id"), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )


def create_p_p_table():
    op.create_table(
        'p_p',
        sa.Column('id', UUID, primary_key=True, default=uuid4()),
        sa.Column('required_quantity', sa.Integer, nullable=False),
        sa.Column('order_id', UUID, sa.ForeignKey("orders.id"), nullable=True),
        sa.Column('product_id', UUID, sa.ForeignKey("product.id"), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_by', UUID, nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )



def upgrade() -> None:
    create_raw_material_table()
    create_product_table()
    create_order_table()
    create_m_p_table()
    create_p_p_table()


def downgrade() -> None:
    op.drop_table('p_p')
    op.drop_table('m_p')
    op.drop_table('raw_material')
    op.drop_table('product')
    op.drop_table('order')


