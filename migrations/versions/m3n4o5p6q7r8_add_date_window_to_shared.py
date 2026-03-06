"""Add date_window_days to shared_dashboards

Revision ID: m3n4o5p6q7r8
Revises: 8318a93e3a4e
Create Date: 2026-03-06 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'm3n4o5p6q7r8'
down_revision = '8318a93e3a4e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('shared_dashboards', sa.Column('date_window_days', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('shared_dashboards', 'date_window_days')
