from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003_create_courses"
down_revision = "0002_create_users"
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		"courses",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("code", sa.String(length=32), nullable=False),
		sa.Column("title", sa.String(length=255), nullable=False),
		sa.Column("credits", sa.Integer(), nullable=False, server_default="3"),
		sa.Column("department", sa.String(length=64), nullable=True),
	)
	op.create_index("ix_courses_id", "courses", ["id"], unique=False)
	op.create_index("ux_courses_code", "courses", ["code"], unique=True)


def downgrade():
	op.drop_index("ux_courses_code", table_name="courses")
	op.drop_index("ix_courses_id", table_name="courses")
	op.drop_table("courses")
