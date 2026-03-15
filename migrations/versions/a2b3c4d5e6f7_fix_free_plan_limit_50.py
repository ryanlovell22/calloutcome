"""fix free plan server_default from 10 to 50 and update existing accounts

Revision ID: a2b3c4d5e6f7
Revises: f8c7c523af15
Create Date: 2026-03-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2b3c4d5e6f7'
down_revision = 'f8c7c523af15'
branch_labels = None
depends_on = None


def upgrade():
    # Fix the server_default from 10 to 50
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.alter_column('plan_calls_limit',
                              existing_type=sa.Integer(),
                              server_default='50')

    # Fix any existing free accounts stuck at 10
    op.execute(
        "UPDATE accounts SET plan_calls_limit = 50 "
        "WHERE (stripe_plan = 'free' OR stripe_plan IS NULL) "
        "AND plan_calls_limit = 10"
    )


def downgrade():
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.alter_column('plan_calls_limit',
                              existing_type=sa.Integer(),
                              server_default='10')
