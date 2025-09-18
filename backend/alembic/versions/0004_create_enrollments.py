from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004_create_enrollments"
down_revision = "0003_create_courses"
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		"enrollments",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("student_id", sa.Integer(), nullable=False),
		sa.Column("course_id", sa.Integer(), nullable=False),
		sa.Column("term", sa.String(length=10), nullable=False),
		sa.Column("grade", sa.Float(), nullable=True),
		sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
		sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
	)
	op.create_index("ix_enrollments_id", "enrollments", ["id"], unique=False)
	op.create_index("ix_enrollments_student_id", "enrollments", ["student_id"], unique=False)
	op.create_index("ix_enrollments_course_id", "enrollments", ["course_id"], unique=False)


def downgrade():
	op.drop_index("ix_enrollments_course_id", table_name="enrollments")
	op.drop_index("ix_enrollments_student_id", table_name="enrollments")
	op.drop_index("ix_enrollments_id", table_name="enrollments")
	op.drop_table("enrollments")
