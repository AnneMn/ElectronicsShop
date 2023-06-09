"""empty message

Revision ID: 72687b0fc991
Revises: 9491068b810a
Create Date: 2021-05-21 21:23:19.502083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72687b0fc991'
down_revision = '9491068b810a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order') as batch_op:
        batch_op.drop_column( 'payment_method')
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', 'payment_method')
   
    # ### end Alembic commands ###
