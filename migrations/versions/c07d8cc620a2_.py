"""empty message

Revision ID: c07d8cc620a2
Revises: 57f992f432cc
Create Date: 2022-06-03 21:14:46.492902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c07d8cc620a2'
down_revision = '57f992f432cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'seeking_description',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###
