"""empty message

Revision ID: 524e5316e944
Revises: 
Create Date: 2024-11-03 09:45:15.700833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524e5316e944'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('company', sa.String(length=120), nullable=True),
    sa.Column('address_1', sa.String(length=120), nullable=False),
    sa.Column('address_2', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('postcode', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=3), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shipping',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('company', sa.String(length=120), nullable=True),
    sa.Column('address_1', sa.String(length=120), nullable=False),
    sa.Column('address_2', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('postcode', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=False),
    sa.Column('last_name', sa.String(length=120), nullable=False),
    sa.Column('company', sa.String(length=120), nullable=True),
    sa.Column('role', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_paying_customer', sa.Boolean(), nullable=True),
    sa.Column('billing_id', sa.Integer(), nullable=True),
    sa.Column('shipping_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['billing_id'], ['billing.id'], ),
    sa.ForeignKeyConstraint(['shipping_id'], ['shipping.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=80), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('total', sa.String(length=80), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('billing_id', sa.Integer(), nullable=True),
    sa.Column('shipping_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['billing_id'], ['billing.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['shipping_id'], ['shipping.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coupon_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=80), nullable=False),
    sa.Column('discount', sa.String(length=80), nullable=False),
    sa.Column('discount_tax', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fee_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('tax_class', sa.String(length=80), nullable=True),
    sa.Column('tax_status', sa.String(length=80), nullable=False),
    sa.Column('total', sa.String(length=80), nullable=False),
    sa.Column('total_tax', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('line_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('variation_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('tax_class', sa.String(length=80), nullable=True),
    sa.Column('subtotal', sa.String(length=80), nullable=False),
    sa.Column('subtotal_tax', sa.String(length=80), nullable=False),
    sa.Column('total', sa.String(length=80), nullable=False),
    sa.Column('total_tax', sa.String(length=80), nullable=False),
    sa.Column('sku', sa.String(length=80), nullable=True),
    sa.Column('price', sa.String(length=80), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('meta_data', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refund',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(length=255), nullable=True),
    sa.Column('total', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shipping_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('method_title', sa.String(length=80), nullable=False),
    sa.Column('method_id', sa.String(length=80), nullable=False),
    sa.Column('total', sa.String(length=80), nullable=False),
    sa.Column('total_tax', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax_line',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('rate_code', sa.String(length=80), nullable=False),
    sa.Column('rate_id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=80), nullable=False),
    sa.Column('compound', sa.Boolean(), nullable=False),
    sa.Column('tax_total', sa.String(length=80), nullable=False),
    sa.Column('shipping_tax_total', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tax_line')
    op.drop_table('shipping_line')
    op.drop_table('refund')
    op.drop_table('line_item')
    op.drop_table('fee_line')
    op.drop_table('coupon_line')
    op.drop_table('order')
    op.drop_table('customer')
    op.drop_table('user')
    op.drop_table('shipping')
    op.drop_table('billing')
    # ### end Alembic commands ###
