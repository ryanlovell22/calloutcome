"""Add stripe_customer_id to partners

Revision ID: o5p6q7r8s9t0
Revises: n4o5p6q7r8s9
Create Date: 2026-04-26

"""
from alembic import op
import sqlalchemy as sa

revision = 'o5p6q7r8s9t0'
down_revision = 'n4o5p6q7r8s9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('partners', sa.Column('stripe_customer_id', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('partners', 'stripe_customer_id')
