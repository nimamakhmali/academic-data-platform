"""
Faculty model for Academic Data Platform.

This module defines the Faculty entity which represents academic staff members
including professors, lecturers, and other teaching personnel.
"""

from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .user import User
    from .department import Department
    from .research_item import ResearchItem


class Faculty(Base):
    """
    Faculty model representing academic staff members.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User table for authentication
        full_name: Complete name of faculty member
        department_id: Foreign key to Department table
        rank: Academic rank (Professor, Associate Professor, etc.)
        hire_date: Date when faculty member was hired
        office_location: Physical office location
        phone: Contact phone number
        bio: Biography/research interests
        orcid_id: ORCID identifier for research
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
        is_active: Whether faculty member is currently active
    
    Relationships:
        user: Related User record for authentication
        department: Related Department record
        research_items: List of research items owned by this faculty
        course_offerings: List of courses taught by this faculty
    """
    
    __tablename__ = "faculty"

    # Primary Fields
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Unique identifier for faculty member"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        comment="Foreign key to users table"
    )
    
    full_name: Mapped[str] = mapped_column(
        String(128), 
        nullable=False,
        index=True,
        comment="Complete name of faculty member"
    )
    
    department_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Foreign key to departments table"
    )
    
    rank: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        comment="Academic rank (Professor, Associate Professor, Assistant Professor, Lecturer, etc.)"
    )
    
    hire_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        comment="Date when faculty member was hired"
    )
    
    office_location: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        comment="Physical office location (building, room number)"
    )
    
    phone: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        comment="Contact phone number"
    )
    
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Biography, research interests, and background"
    )
    
    orcid_id: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        unique=True,
        comment="ORCID identifier for academic publications"
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
    
    is_active: Mapped[bool] = mapped_column(
        default=True,
        comment="Whether faculty member is currently active"
    )

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="faculty",
        lazy="joined",
        cascade="all, delete"
    )
    
    department: Mapped[Optional["Department"]] = relationship(
        back_populates="faculty_members",
        lazy="joined"
    )
    
    research_items: Mapped[List["ResearchItem"]] = relationship(
        back_populates="owner_faculty",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Course offerings will be added in future when we create CourseOffering model
    # course_offerings: Mapped[List["CourseOffering"]] = relationship(back_populates="faculty")

    def __repr__(self) -> str:
        return f"<Faculty(id={self.id}, name='{self.full_name}', rank='{self.rank}')>"
    
    def __str__(self) -> str:
        rank_prefix = f"{self.rank} " if self.rank else ""
        return f"{rank_prefix}{self.full_name}"
    
    @property
    def display_name(self) -> str:
        """Returns formatted display name with rank."""
        if self.rank:
            return f"{self.rank} {self.full_name}"
        return self.full_name
    
    @property
    def years_of_service(self) -> Optional[int]:
        """Calculate years of service if hire_date is available."""
        if self.hire_date:
            today = date.today()
            return today.year - self.hire_date.year
        return None
