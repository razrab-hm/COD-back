"""create cod tables

Revision ID: d14b420ebf59
Revises: 
Create Date: 2023-01-17 18:31:02.278015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd14b420ebf59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade() -> None:
    op.drop_table('account')
