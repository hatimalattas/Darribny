"""empty message

Revision ID: 7e2c6f10c3a0
Revises: a002fd276091
Create Date: 2020-09-16 00:53:21.048037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e2c6f10c3a0'
down_revision = 'a002fd276091'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('status', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservations', 'status')
    # ### end Alembic commands ###
