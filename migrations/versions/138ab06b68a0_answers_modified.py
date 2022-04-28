"""answers modified

Revision ID: 138ab06b68a0
Revises: c55913c40bfb
Create Date: 2022-04-28 23:56:49.824098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '138ab06b68a0'
down_revision = 'c55913c40bfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('options', sa.PickleType(), nullable=True))
    op.drop_column('questions', 'option_1')
    op.drop_column('questions', 'option_3')
    op.drop_column('questions', 'option_0')
    op.drop_column('questions', 'category')
    op.drop_column('questions', 'option_2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('option_2', sa.VARCHAR(length=128), nullable=True))
    op.add_column('questions', sa.Column('category', sa.INTEGER(), nullable=True))
    op.add_column('questions', sa.Column('option_0', sa.VARCHAR(length=128), nullable=True))
    op.add_column('questions', sa.Column('option_3', sa.VARCHAR(length=128), nullable=True))
    op.add_column('questions', sa.Column('option_1', sa.VARCHAR(length=128), nullable=True))
    op.drop_column('questions', 'options')
    # ### end Alembic commands ###
