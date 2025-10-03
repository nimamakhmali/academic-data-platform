"""feat(db): enhance users table with additional security and metadata fields

Revision ID: 0009_update_users_table
Revises: 0008_create_research_items
Create Date: 2024-10-02 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0009_update_users_table"
down_revision = "0008_create_research_items"
branch_labels = None
depends_on = None


def upgrade():
    """Add additional security and metadata fields to users table."""
    # Add new columns to users table
    op.add_column("users", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Account creation timestamp"))
    op.add_column("users", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Last account update timestamp"))
    op.add_column("users", sa.Column("last_login", sa.DateTime(timezone=True), nullable=True, comment="Last login timestamp"))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true"), comment="Whether account is active"))
    op.add_column("users", sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false"), comment="Whether email address is verified"))
    
    # Add index for role column for better performance
    op.create_index("ix_users_role", "users", ["role"], unique=False)


def downgrade():
    """Remove additional fields from users table."""
    op.drop_index("ix_users_role", table_name="users")
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_active")
    op.drop_column("users", "last_login")
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")

