"""feat(db): add department model with comprehensive fields

Revision ID: 0006_create_departments
Revises: 0005_create_grades
Create Date: 2024-10-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0006_create_departments"
down_revision = "0005_create_grades"
branch_labels = None
depends_on = None


def upgrade():
    """Create departments table with comprehensive academic department structure."""
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False, comment="Unique identifier for department"),
        sa.Column("name", sa.String(length=128), nullable=False, comment="Full name of the department"),
        sa.Column("code", sa.String(length=16), nullable=False, comment="Short code for department (e.g., CE, EE)"),
        sa.Column("description", sa.Text(), nullable=True, comment="Description of department activities and focus"),
        sa.Column("established_year", sa.Integer(), nullable=True, comment="Year when department was established"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record last update timestamp"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true"), comment="Whether department is currently active"),
        sa.PrimaryKeyConstraint("id")
    )
    
    # Create indexes for better performance
    op.create_index("ix_departments_id", "departments", ["id"], unique=False)
    op.create_index("ix_departments_name", "departments", ["name"], unique=False)
    op.create_index("ux_departments_code", "departments", ["code"], unique=True)


def downgrade():
    """Drop departments table and related indexes."""
    op.drop_index("ux_departments_code", table_name="departments")
    op.drop_index("ix_departments_name", table_name="departments") 
    op.drop_index("ix_departments_id", table_name="departments")
    op.drop_table("departments")
