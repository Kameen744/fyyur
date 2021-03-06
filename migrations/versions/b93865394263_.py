"""empty message

Revision ID: b93865394263
Revises: 54b729fc691b
Create Date: 2022-06-04 18:41:26.647353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b93865394263'
down_revision = '54b729fc691b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artist_city_id_fkey', 'artist', type_='foreignkey')
    op.drop_column('artist', 'city_id')
    op.drop_column('artist', 'image_link')
    op.drop_column('artist', 'website_link')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'genres')
    op.drop_column('artist', 'facebook_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False))
    op.add_column('artist', sa.Column('city_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('artist_city_id_fkey', 'artist', 'city', ['city_id'], ['id'])
    # ### end Alembic commands ###
