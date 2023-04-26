"""empty message

Revision ID: 6972fea25d11
Revises: 9a36d2b15142
Create Date: 2021-05-25 22:32:35.658240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6972fea25d11'
down_revision = '9a36d2b15142'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username')
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('type', sa.TEXT(), nullable=True))
    op.add_column('product', sa.Column('manu_name', sa.TEXT(), nullable=True))
    op.create_table('infrequent_customers',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('username', sa.TEXT(), nullable=True),
    sa.Column('card_info', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stores',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('store_region', sa.TEXT(), nullable=True),
    sa.Column('pName', sa.TEXT(), nullable=True),
    sa.Column('stock', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('warehouses',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('pName', sa.TEXT(), nullable=True),
    sa.Column('stock', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('pName', sa.TEXT(), nullable=True),
    sa.Column('unit_sales', sa.INTEGER(), nullable=True),
    sa.Column('unit_price', sa.INTEGER(), nullable=True),
    sa.Column('total_price', sa.INTEGER(), nullable=True),
    sa.Column('store_region', sa.TEXT(), nullable=True),
    sa.Column('date', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contract_customers',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('username', sa.TEXT(), nullable=True),
    sa.Column('account_number', sa.TEXT(), nullable=True),
    sa.Column('billing_date', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.create_table('manufacturers',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('manu_name', sa.TEXT(), nullable=True),
    sa.Column('pName', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('customers')
    # ### end Alembic commands ###