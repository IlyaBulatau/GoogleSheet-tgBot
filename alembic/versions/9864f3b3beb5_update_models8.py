"""update models8

Revision ID: 9864f3b3beb5
Revises: d65b3c34890e
Create Date: 2023-06-12 18:54:53.403226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9864f3b3beb5'
down_revision = 'd65b3c34890e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tablse', sa.Column('name', sa.String(), server_default='New Table', nullable=False))
    op.add_column('users', sa.Column('coints', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'coints')
    op.drop_column('tablse', 'name')
    # ### end Alembic commands ###