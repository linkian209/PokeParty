"""Create Team Table

Revision ID: 10d079bc3ace
Revises: 943335c25fb5
Create Date: 2022-11-25 14:37:36.236152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10d079bc3ace'
down_revision = '943335c25fb5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'team',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
        sa.Column('pokemon1', sa.String(64), nullable=True),
        sa.Column('pokemon2', sa.String(64), nullable=True),
        sa.Column('pokemon3', sa.String(64), nullable=True),
        sa.Column('pokemon4', sa.String(64), nullable=True),
        sa.Column('pokemon5', sa.String(64), nullable=True),
        sa.Column('pokemon6', sa.String(64), nullable=True),
        sa.Column('item1', sa.String(64), nullable=True),
        sa.Column('item2', sa.String(64), nullable=True),
        sa.Column('item3', sa.String(64), nullable=True),
        sa.Column('item4', sa.String(64), nullable=True),
        sa.Column('item5', sa.String(64), nullable=True),
        sa.Column('item6', sa.String(64), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('team')
