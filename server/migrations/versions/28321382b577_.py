"""empty message

Revision ID: 28321382b577
Revises: None
Create Date: 2014-02-21 14:20:43.671967

"""

# revision identifiers, used by Alembic.
revision = '28321382b577'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['email'])
    op.create_unique_constraint(None, 'user', ['fb_username'])
    op.create_unique_constraint(None, 'user', ['username'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user')
    op.drop_constraint(None, 'user')
    op.drop_constraint(None, 'user')
    ### end Alembic commands ###