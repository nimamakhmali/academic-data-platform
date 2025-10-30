from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_create_users"
down_revision = "0001_create_students"
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		"users",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("email", sa.String(length=255), nullable=False),
		sa.Column("username", sa.String(length=64), nullable=True),
		sa.Column("role", sa.String(length=32), nullable=False, server_default="student"),
		sa.Column("password_hash", sa.String(length=255), nullable=False),
	)
	op.create_index("ix_users_id", "users", ["id"], unique=False)
	op.create_index("ux_users_email", "users", ["email"], unique=True)
	op.create_index("ix_users_username", "users", ["username"], unique=False)


def downgrade():
	op.drop_index("ix_users_username", table_name="users")
	op.drop_index("ux_users_email", table_name="users")
	op.drop_index("ix_users_id", table_name="users")
	op.drop_table("users")
