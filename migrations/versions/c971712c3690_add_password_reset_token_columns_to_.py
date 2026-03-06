"""Add password reset token columns to accounts

Revision ID: c971712c3690
Revises: l2m3n4o5p6q7
Create Date: 2026-03-06 21:27:15.427808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c971712c3690'
down_revision = 'l2m3n4o5p6q7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_reset_token', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('password_reset_expires', sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.drop_column('password_reset_expires')
        batch_op.drop_column('password_reset_token')
