"""feat(db): add research_items model for academic research tracking

Revision ID: 0008_create_research_items
Revises: 0007_create_faculty
Create Date: 2024-10-02 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0008_create_research_items"
down_revision = "0007_create_faculty"
branch_labels = None
depends_on = None


def upgrade():
    """Create research_items table for tracking academic research outputs."""
    op.create_table(
        "research_items",
        sa.Column("id", sa.Integer(), nullable=False, comment="Unique identifier for research item"),
        sa.Column("title", sa.String(length=255), nullable=False, comment="Title of the research item"),
        sa.Column("type", sa.String(length=32), nullable=False, comment="Type of research (article, thesis, project, etc.)"),
        sa.Column("year", sa.Integer(), nullable=True, comment="Publication or completion year"),
        sa.Column("owner_faculty_id", sa.Integer(), nullable=False, comment="Foreign key to faculty table (primary researcher)"),
        sa.Column("description", sa.Text(), nullable=True, comment="Detailed description, abstract, or summary"),
        sa.Column("keywords", sa.Text(), nullable=True, comment="Comma-separated keywords for classification"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft", comment="Current status (draft, published, etc.)"),
        sa.Column("publication_date", sa.Date(), nullable=True, comment="Date of publication or completion"),
        sa.Column("journal_name", sa.String(length=255), nullable=True, comment="Name of journal, conference, or venue"),
        sa.Column("doi", sa.String(length=128), nullable=True, comment="Digital Object Identifier"),
        sa.Column("citation_count", sa.Integer(), nullable=False, server_default="0", comment="Number of citations received"),
        sa.Column("metadata", sa.JSON(), nullable=True, comment="Additional structured metadata"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record creation timestamp"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False, comment="Record last update timestamp"),
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.text("true"), comment="Whether research item is publicly visible"),
        sa.ForeignKeyConstraint(["owner_faculty_id"], ["faculty.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id")
    )
    
    # Create indexes for better performance
    op.create_index("ix_research_items_id", "research_items", ["id"], unique=False)
    op.create_index("ix_research_items_title", "research_items", ["title"], unique=False)
    op.create_index("ix_research_items_type", "research_items", ["type"], unique=False)
    op.create_index("ix_research_items_year", "research_items", ["year"], unique=False)
    op.create_index("ix_research_items_owner_faculty_id", "research_items", ["owner_faculty_id"], unique=False)
    op.create_index("ix_research_items_status", "research_items", ["status"], unique=False)
    op.create_index("ux_research_items_doi", "research_items", ["doi"], unique=True)


def downgrade():
    """Drop research_items table and related indexes."""
    op.drop_index("ux_research_items_doi", table_name="research_items")
    op.drop_index("ix_research_items_status", table_name="research_items")
    op.drop_index("ix_research_items_owner_faculty_id", table_name="research_items")
    op.drop_index("ix_research_items_year", table_name="research_items")
    op.drop_index("ix_research_items_type", table_name="research_items")
    op.drop_index("ix_research_items_title", table_name="research_items")
    op.drop_index("ix_research_items_id", table_name="research_items")
    op.drop_table("research_items")
