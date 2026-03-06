"""Add onboarding_completed column to accounts

Revision ID: l2m3n4o5p6q7
Revises: k1l2m3n4o5p6
Create Date: 2026-03-06
"""
from alembic import op
import sqlalchemy as sa

revision = "l2m3n4o5p6q7"
down_revision = "k1l2m3n4o5p6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "accounts",
        sa.Column("onboarding_completed", sa.Boolean(), server_default="false", nullable=False),
    )

    # Existing users who already connected a call source skip the wizard
    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE accounts
        SET onboarding_completed = true
        WHERE twilio_service_sid IS NOT NULL
           OR (callrail_api_key_encrypted IS NOT NULL AND callrail_account_id IS NOT NULL)
    """))


def downgrade():
    op.drop_column("accounts", "onboarding_completed")
