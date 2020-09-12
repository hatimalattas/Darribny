"""empty message

Revision ID: d7326edc67c6
Revises: 7b480c6f338c
Create Date: 2020-09-10 17:03:30.493289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7326edc67c6'
down_revision = '7b480c6f338c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trainees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('gender', sa.String(length=64), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('mobile', sa.String(length=10), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile')
    )
    op.create_index(op.f('ix_trainees_email'), 'trainees', ['email'], unique=True)
    op.create_index(op.f('ix_trainees_username'), 'trainees', ['username'], unique=True)
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trainee_id', sa.Integer(), nullable=False),
    sa.Column('trainer_id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=64), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['trainee_id'], ['trainees.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('start_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_index(op.f('ix_trainees_username'), table_name='trainees')
    op.drop_index(op.f('ix_trainees_email'), table_name='trainees')
    op.drop_table('trainees')
    # ### end Alembic commands ###
