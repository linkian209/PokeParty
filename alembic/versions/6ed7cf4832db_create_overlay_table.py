"""Create Overlay Table

Revision ID: 6ed7cf4832db
Revises: 10d079bc3ace
Create Date: 2022-11-26 14:25:16.021045

"""
from alembic import op
from app.db import OverlayConfigs
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ed7cf4832db'
down_revision = '10d079bc3ace'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'overlay',
        sa.Column('id', sa.String(32), primary_key=True),
        sa.Column('width', sa.Integer),
        sa.Column('height', sa.Integer),
        sa.Column('arrangement', sa.Enum(OverlayConfigs)),
        sa.Column('outline_items', sa.Boolean),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
    )


def downgrade() -> None:
    op.drop_table('overlay')
