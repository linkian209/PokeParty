"""Create User Table

Revision ID: 943335c25fb5
Revises: 
Create Date: 2022-11-23 17:21:45.720342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '943335c25fb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(64), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("user")