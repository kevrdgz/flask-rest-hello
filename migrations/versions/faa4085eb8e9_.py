"""empty message

Revision ID: faa4085eb8e9
Revises: 6a50da098dc6
Create Date: 2021-03-30 19:01:52.963957

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'faa4085eb8e9'
down_revision = '6a50da098dc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=50), nullable=False))
    op.drop_column('user', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_name', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
