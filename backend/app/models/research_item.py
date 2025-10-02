"""
ResearchItem model for Academic Data Platform.

This module defines the ResearchItem entity which represents research outputs
such as papers, theses, projects, and other academic work.
"""

from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, func, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .faculty import Faculty


class ResearchItem(Base):
    """
    ResearchItem model representing research outputs and academic work.
    
    Attributes:
        id: Primary key
        title: Title of the research item
        type: Type of research (article, thesis, project, book, etc.)
        year: Publication/completion year
        owner_faculty_id: Primary faculty member responsible
        description: Detailed description of the research
        keywords: Research keywords for classification
        status: Current status (draft, under_review, published, etc.)
        publication_date: Date of publication/completion
        journal_name: Name of journal/conference (if applicable)
        doi: Digital Object Identifier
        citation_count: Number of citations received
        metadata: Additional structured metadata (JSON)
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
        is_public: Whether research item is publicly visible
    
    Relationships:
        owner_faculty: Primary faculty member responsible
        collaborators: List of faculty collaborators
    """
    
    __tablename__ = "research_items"

    # Primary Fields
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Unique identifier for research item"
    )
    
    title: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        index=True,
        comment="Title of the research item"
    )
    
    type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
        comment="Type of research (article, thesis, project, book, conference, patent, etc.)"
    )
    
    year: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="Publication or completion year"
    )
    
    owner_faculty_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("faculty.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to faculty table (primary researcher)"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed description, abstract, or summary of the research"
    )
    
    keywords: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Comma-separated keywords for research classification and search"
    )
    
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
        index=True,
        comment="Current status (draft, under_review, accepted, published, completed, etc.)"
    )
    
    publication_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Date of publication or completion"
    )
    
    journal_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Name of journal, conference, or publication venue"
    )
    
    doi: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        unique=True,
        comment="Digital Object Identifier for published works"
    )
    
    citation_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of citations received (updated periodically)"
    )
    
    metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="Additional structured metadata (pages, volume, issue, etc.)"
    )
    
    # Metadata Fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Record last update timestamp"
    )
    
    is_public: Mapped[bool] = mapped_column(
        default=True,
        comment="Whether research item is publicly visible"
    )

    # Relationships
    owner_faculty: Mapped["Faculty"] = relationship(
        back_populates="research_items",
        lazy="joined"
    )
    
    # This will be added after creating collaboration table
    # collaborators: Mapped[List["ResearchCollaboration"]] = relationship(back_populates="research_item")

    def __repr__(self) -> str:
        return f"<ResearchItem(id={self.id}, title='{self.title[:50]}...', type='{self.type}')>"
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year or 'N/A'})"
    
    @property
    def short_title(self) -> str:
        """Returns truncated title for display purposes."""
        if len(self.title) <= 50:
            return self.title
        return f"{self.title[:47]}..."
    
    @property
    def is_published(self) -> bool:
        """Check if the research item is published."""
        return self.status in ["published", "accepted"]
    
    @property
    def age_years(self) -> Optional[int]:
        """Calculate how many years old this research is."""
        if self.year:
            current_year = datetime.now().year
            return current_year - self.year
        return None
    
    def get_keywords_list(self) -> List[str]:
        """Parse keywords string into a list."""
        if self.keywords:
            return [kw.strip() for kw in self.keywords.split(",") if kw.strip()]
        return []
