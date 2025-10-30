"""feat(db): enhance students table with user relationship and additional fields

Revision ID: 0010_update_students_table
Revises: 0009_update_users_table
Create Date: 2024-10-02 13:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0010_update_students_table"
down_revision = "0009_update_users_table"
branch_labels = None
depends_on = None


def upgrade():
    """Add user relationship and additional academic fields to students table."""
    # Add new columns to students table
    op.add_column("students", sa.Column("user_id", sa.Integer(), nullable=False, comment="Foreign key to users table"))
    op.add_column("students", sa.Column("department_id", sa.Integer(), nullable=True, comment="Foreign key to departments table"))
    op.add_column("students", sa.Column("level", sa.String(length=32), nullable=True, comment="Academic level (bachelor, master, phd, diploma)"))
    op.add_column("students", sa.Column("gpa", sa.Numeric(precision=3, scale=2), nullable=True, comment="Current Grade Point Average (0.00-20.00)"))
    op.add_column("students", sa.Column("status", sa.String(length=32), nullable=False, server_default="active", comment="Current status (active, graduated, dropped, suspended, transferred)"))
    op.add_column("students", sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record creation timestamp"))
    op.add_column("students", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record last update timestamp"))
    
    # Add foreign key constraints
    op.create_foreign_key("fk_students_user_id", "students", "users", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_students_department_id", "students", "departments", ["department_id"], ["id"], ondelete="SET NULL")
    
    # Add indexes for better performance
    op.create_index("ux_students_user_id", "students", ["user_id"], unique=True)
    op.create_index("ix_students_department_id", "students", ["department_id"], unique=False)
    op.create_index("ix_students_status", "students", ["status"], unique=False)
    op.create_index("ix_students_entry_year", "students", ["entry_year"], unique=False)
    op.create_index("ix_students_full_name", "students", ["full_name"], unique=False)


def downgrade():
    """Remove additional fields and relationships from students table."""
    op.drop_index("ix_students_full_name", table_name="students")
    op.drop_index("ix_students_entry_year", table_name="students")
    op.drop_index("ix_students_status", table_name="students")
    op.drop_index("ix_students_department_id", table_name="students")
    op.drop_index("ux_students_user_id", table_name="students")
    op.drop_constraint("fk_students_department_id", "students", type_="foreignkey")
    op.drop_constraint("fk_students_user_id", "students", type_="foreignkey")
    op.drop_column("students", "updated_at")
    op.drop_column("students", "created_at")
    op.drop_column("students", "status")
    op.drop_column("students", "gpa")
    op.drop_column("students", "level")
    op.drop_column("students", "department_id")
    op.drop_column("students", "user_id")

