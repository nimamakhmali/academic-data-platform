from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0005_create_grades"
down_revision = "0004_create_enrollments"
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		"grades",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("enrollment_id", sa.Integer(), nullable=False),
		sa.Column("value", sa.Float(), nullable=False),
		sa.ForeignKeyConstraint(["enrollment_id"], ["enrollments.id"]),
	)
	op.create_index("ix_grades_id", "grades", ["id"], unique=False)


def downgrade():
	op.drop_index("ix_grades_id", table_name="grades")
	op.drop_table("grades")
