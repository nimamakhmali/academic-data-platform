"""
Course model for Academic Data Platform.

This module defines the Course entity representing academic courses.
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .department import Department
    from .enrollment import Enrollment


class Course(Base):
	"""
	Course model representing academic courses.
	
	Attributes:
		id: Primary key
		code: Unique course code (e.g., "CS101", "MATH201")
		title: Course title/name
		credits: Number of credit units
		department_id: Foreign key to Department table
		level: Course level (undergraduate, graduate, etc.)
		description: Detailed course description
		prerequisites: Text description of prerequisites
		is_active: Whether course is currently offered
		created_at: Record creation timestamp
		updated_at: Record last update timestamp
	
	Relationships:
		department: Related Department record
		enrollments: List of student enrollments
	"""
	
	__tablename__ = "courses"

	# Primary Fields
	id: Mapped[int] = mapped_column(
		Integer, 
		primary_key=True, 
		index=True,
		comment="Unique identifier for course"
	)
	
	code: Mapped[str] = mapped_column(
		String(32), 
		unique=True, 
		index=True,
		comment="Unique course code (e.g., CS101, MATH201)"
	)
	
	title: Mapped[str] = mapped_column(
		String(255),
		nullable=False,
		index=True,
		comment="Course title/name"
	)
	
	credits: Mapped[int] = mapped_column(
		Integer, 
		default=3,
		comment="Number of credit units for this course"
	)
	
	department_id: Mapped[Optional[int]] = mapped_column(
		Integer,
		ForeignKey("departments.id", ondelete="SET NULL"),
		nullable=True,
		index=True,
		comment="Foreign key to departments table"
	)
	
	level: Mapped[Optional[str]] = mapped_column(
		String(32),
		nullable=True,
		comment="Course level (undergraduate, graduate, postgraduate)"
	)
	
	description: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True,
		comment="Detailed course description and objectives"
	)
	
	prerequisites: Mapped[Optional[str]] = mapped_column(
		Text,
		nullable=True,
		comment="Prerequisites and requirements for taking this course"
	)
	
	is_active: Mapped[bool] = mapped_column(
		Boolean,
		default=True,
		comment="Whether course is currently offered"
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

	# Relationships
	department: Mapped[Optional["Department"]] = relationship(
		back_populates="courses",
		lazy="joined"
	)
	
	enrollments: Mapped[List["Enrollment"]] = relationship(
		back_populates="course",
		cascade="all, delete-orphan",
		lazy="selectin",
	)

	def __repr__(self) -> str:
		return f"<Course(id={self.id}, code='{self.code}', title='{self.title}')>"
	
	def __str__(self) -> str:
		return f"{self.code} - {self.title}"
	
	@property
	def display_name(self) -> str:
		"""Returns formatted display name with code and title."""
		return f"{self.code}: {self.title}"
	
	@property
	def short_title(self) -> str:
		"""Returns truncated title for display purposes."""
		if len(self.title) <= 50:
			return self.title
		return f"{self.title[:47]}..."
