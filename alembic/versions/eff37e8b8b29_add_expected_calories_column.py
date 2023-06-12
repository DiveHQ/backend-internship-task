"""Add expected_calories column

Revision ID: eff37e8b8b29
Revises: 
Create Date: 2023-06-12 13:13:57.662491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eff37e8b8b29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('expected_calories', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'expected_calories')
    # ### end Alembic commands ###
