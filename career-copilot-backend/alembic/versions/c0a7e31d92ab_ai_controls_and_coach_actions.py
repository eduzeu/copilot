"""AI controls and coach actions.

Revision ID: c0a7e31d92ab
Revises: 80039962503f
"""

from alembic import op
import sqlalchemy as sa

revision = "c0a7e31d92ab"
down_revision = "80039962503f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_response_cache",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cache_key", sa.String(length=64), nullable=False),
        sa.Column("feature", sa.String(length=80), nullable=False),
        sa.Column("response", sa.JSON(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_response_cache_cache_key", "ai_response_cache", ["cache_key"], unique=True)
    op.create_index("ix_ai_response_cache_expires_at", "ai_response_cache", ["expires_at"])
    op.create_table(
        "ai_request_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("feature", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_request_logs_created_at", "ai_request_logs", ["created_at"])
    op.create_index("ix_ai_request_logs_feature", "ai_request_logs", ["feature"])
    op.create_index("ix_ai_request_logs_user_id", "ai_request_logs", ["user_id"])
    op.create_table(
        "coach_actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("interaction_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["interaction_id"], ["coach_interactions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_coach_actions_status", "coach_actions", ["status"])
    op.create_index("ix_coach_actions_user_id", "coach_actions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_coach_actions_user_id", table_name="coach_actions")
    op.drop_index("ix_coach_actions_status", table_name="coach_actions")
    op.drop_table("coach_actions")
    op.drop_index("ix_ai_request_logs_user_id", table_name="ai_request_logs")
    op.drop_index("ix_ai_request_logs_feature", table_name="ai_request_logs")
    op.drop_index("ix_ai_request_logs_created_at", table_name="ai_request_logs")
    op.drop_table("ai_request_logs")
    op.drop_index("ix_ai_response_cache_expires_at", table_name="ai_response_cache")
    op.drop_index("ix_ai_response_cache_cache_key", table_name="ai_response_cache")
    op.drop_table("ai_response_cache")
