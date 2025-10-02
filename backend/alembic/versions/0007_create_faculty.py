"""feat(db): add faculty model with comprehensive academic staff structure

Revision ID: 0007_create_faculty
Revises: 0006_create_departments
Create Date: 2024-10-02 12:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0007_create_faculty"
down_revision = "0006_create_departments"
branch_labels = None
depends_on = None


def upgrade():
    """Create faculty table with comprehensive academic staff structure."""
    op.create_table(
        "faculty",
        sa.Column("id", sa.Integer(), nullable=False, comment="Unique identifier for faculty member"),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="Foreign key to users table"),
        sa.Column("full_name", sa.String(length=128), nullable=False, comment="Complete name of faculty member"),
        sa.Column("department_id", sa.Integer(), nullable=True, comment="Foreign key to departments table"),
        sa.Column("rank", sa.String(length=64), nullable=True, comment="Academic rank (Professor, Associate Professor, etc.)"),
        sa.Column("hire_date", sa.Date(), nullable=True, comment="Date when faculty member was hired"),
        sa.Column("office_location", sa.String(length=128), nullable=True, comment="Physical office location (building, room number)"),
        sa.Column("phone", sa.String(length=32), nullable=True, comment="Contact phone number"),
        sa.Column("bio", sa.Text(), nullable=True, comment="Biography, research interests, and background"),
        sa.Column("orcid_id", sa.String(length=32), nullable=True, comment="ORCID identifier for academic publications"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record last update timestamp"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true"), comment="Whether faculty member is currently active"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id")
    )
    
    # Create indexes for better performance
    op.create_index("ix_faculty_id", "faculty", ["id"], unique=False)
    op.create_index("ix_faculty_full_name", "faculty", ["full_name"], unique=False)
    op.create_index("ix_faculty_department_id", "faculty", ["department_id"], unique=False)
    op.create_index("ux_faculty_user_id", "faculty", ["user_id"], unique=True)
    op.create_index("ux_faculty_orcid_id", "faculty", ["orcid_id"], unique=True)


def downgrade():
    """Drop faculty table and related indexes."""
    op.drop_index("ux_faculty_orcid_id", table_name="faculty")
    op.drop_index("ux_faculty_user_id", table_name="faculty")
    op.drop_index("ix_faculty_department_id", table_name="faculty")
    op.drop_index("ix_faculty_full_name", table_name="faculty")
    op.drop_index("ix_faculty_id", table_name="faculty")
    op.drop_table("faculty")
