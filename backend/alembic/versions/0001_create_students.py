from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_create_students"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		"students",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("student_no", sa.String(length=32), nullable=False),
		sa.Column("entry_year", sa.Integer(), nullable=True),
		sa.Column("full_name", sa.String(length=128), nullable=True),
	)
	op.create_index("ix_students_id", "students", ["id"], unique=False)
	op.create_index("ux_students_student_no", "students", ["student_no"], unique=True)


def downgrade():
	op.drop_index("ux_students_student_no", table_name="students")
	op.drop_index("ix_students_id", table_name="students")
	op.drop_table("students")
