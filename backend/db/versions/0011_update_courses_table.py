"""feat(db): enhance courses table with department relationship and additional fields

Revision ID: 0011_update_courses_table
Revises: 0010_update_students_table
Create Date: 2024-10-02 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0011_update_courses_table"
down_revision = "0010_update_students_table"
branch_labels = None
depends_on = None


def upgrade():
    """Add department relationship and additional academic fields to courses table."""
    # First, drop the old department column (it was a string)
    op.drop_column("courses", "department")
    
    # Add new columns to courses table
    op.add_column("courses", sa.Column("department_id", sa.Integer(), nullable=True, comment="Foreign key to departments table"))
    op.add_column("courses", sa.Column("level", sa.String(length=32), nullable=True, comment="Course level (undergraduate, graduate, postgraduate)"))
    op.add_column("courses", sa.Column("description", sa.Text(), nullable=True, comment="Detailed course description and objectives"))
    op.add_column("courses", sa.Column("prerequisites", sa.Text(), nullable=True, comment="Prerequisites and requirements for taking this course"))
    op.add_column("courses", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true"), comment="Whether course is currently offered"))
    op.add_column("courses", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record creation timestamp"))
    op.add_column("courses", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record last update timestamp"))
    
    # Add foreign key constraint
    op.create_foreign_key("fk_courses_department_id", "courses", "departments", ["department_id"], ["id"], ondelete="SET NULL")
    
    # Add indexes for better performance
    op.create_index("ix_courses_department_id", "courses", ["department_id"], unique=False)
    op.create_index("ix_courses_title", "courses", ["title"], unique=False)


def downgrade():
    """Remove additional fields and relationships from courses table."""
    op.drop_index("ix_courses_title", table_name="courses")
    op.drop_index("ix_courses_department_id", table_name="courses")
    op.drop_constraint("fk_courses_department_id", "courses", type_="foreignkey")
    op.drop_column("courses", "updated_at")
    op.drop_column("courses", "created_at")
    op.drop_column("courses", "is_active")
    op.drop_column("courses", "prerequisites")
    op.drop_column("courses", "description")
    op.drop_column("courses", "level")
    op.drop_column("courses", "department_id")
    
    # Restore the old department column
    op.add_column("courses", sa.Column("department", sa.String(length=64), nullable=True))

