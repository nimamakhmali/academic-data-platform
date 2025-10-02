"""
Student model for Academic Data Platform.

This module defines the Student entity representing enrolled students.
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .user import User
    from .department import Department
    from .enrollment import Enrollment


class Student(Base):
	"""
	Student model representing enrolled students.
	
	Attributes:
		id: Primary key
		user_id: Foreign key to User table for authentication
		student_no: Unique student identification number
		full_name: Complete name of student
		entry_year: Year when student was enrolled
		department_id: Foreign key to Department table
		level: Academic level (bachelor, master, phd)
		gpa: Current Grade Point Average
		status: Current status (active, graduated, dropped, suspended)
		created_at: Record creation timestamp
		updated_at: Record last update timestamp
	
	Relationships:
		user: Related User record for authentication
		department: Related Department record
		enrollments: List of course enrollments
	"""
	
	__tablename__ = "students"

	# Primary Fields
	id: Mapped[int] = mapped_column(
		Integer, 
		primary_key=True, 
		index=True,
		comment="Unique identifier for student"
	)
	
	user_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("users.id", ondelete="CASCADE"),
		unique=True,
		nullable=False,
		comment="Foreign key to users table"
	)
	
	student_no: Mapped[str] = mapped_column(
		String(32), 
		unique=True, 
		index=True,
		comment="Unique student identification number"
	)
	
	full_name: Mapped[Optional[str]] = mapped_column(
		String(128), 
		nullable=True,
		index=True,
		comment="Complete name of student"
	)
	
	entry_year: Mapped[Optional[int]] = mapped_column(
		Integer, 
		nullable=True,
		index=True,
		comment="Year when student was enrolled"
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
		comment="Academic level (bachelor, master, phd, diploma)"
	)
	
	gpa: Mapped[Optional[float]] = mapped_column(
		Numeric(3, 2),
		nullable=True,
		comment="Current Grade Point Average (0.00-20.00)"
	)
	
	status: Mapped[str] = mapped_column(
		String(32),
		default="active",
		index=True,
		comment="Current status (active, graduated, dropped, suspended, transferred)"
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
	user: Mapped["User"] = relationship(
		back_populates="student",
		lazy="joined"
	)
	
	department: Mapped[Optional["Department"]] = relationship(
		back_populates="students",
		lazy="joined"
	)
	
	enrollments: Mapped[List["Enrollment"]] = relationship(
		back_populates="student",
		cascade="all, delete-orphan",
		lazy="selectin",
	)

	def __repr__(self) -> str:
		return f"<Student(id={self.id}, student_no='{self.student_no}', name='{self.full_name}')>"
	
	def __str__(self) -> str:
		return f"{self.student_no} - {self.full_name or 'Unknown'}"
	
	@property
	def display_name(self) -> str:
		"""Returns formatted display name."""
		if self.full_name:
			return f"{self.full_name} ({self.student_no})"
		return self.student_no
	
	@property
	def years_enrolled(self) -> Optional[int]:
		"""Calculate years since enrollment."""
		if self.entry_year:
			current_year = datetime.now().year
			return current_year - self.entry_year
		return None
	
	@property
	def is_active(self) -> bool:
		"""Check if student is currently active."""
		return self.status == "active"
