"""
User model for Academic Data Platform authentication.

This module defines the User entity for authentication and authorization.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .student import Student
    from .faculty import Faculty


class User(Base):
	"""
	User model for authentication and authorization.
	
	Attributes:
		id: Primary key
		email: Unique email address for login
		username: Optional username for display
		role: User role (admin, faculty, student)
		password_hash: Hashed password for authentication
		created_at: Account creation timestamp
		updated_at: Last account update timestamp
		last_login: Last login timestamp
		is_active: Whether account is active
		is_verified: Whether email is verified
	
	Relationships:
		student: Related Student record (1:1)
		faculty: Related Faculty record (1:1)
	"""
	
	__tablename__ = "users"

	# Primary Fields
	id: Mapped[int] = mapped_column(
		Integer, 
		primary_key=True, 
		index=True,
		comment="Unique identifier for user"
	)
	
	email: Mapped[str] = mapped_column(
		String(255), 
		unique=True, 
		index=True,
		comment="Unique email address for authentication"
	)
	
	username: Mapped[Optional[str]] = mapped_column(
		String(64), 
		nullable=True, 
		index=True,
		comment="Optional username for display purposes"
	)
	
	role: Mapped[str] = mapped_column(
		String(32), 
		default="student",
		index=True,
		comment="User role (admin, faculty, student)"
	)
	
	password_hash: Mapped[str] = mapped_column(
		String(255),
		comment="Hashed password for authentication"
	)
	
	# Metadata Fields
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		comment="Account creation timestamp"
	)
	
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		server_default=func.now(),
		onupdate=func.now(),
		comment="Last account update timestamp"
	)
	
	last_login: Mapped[Optional[datetime]] = mapped_column(
		DateTime(timezone=True),
		nullable=True,
		comment="Last login timestamp"
	)
	
	is_active: Mapped[bool] = mapped_column(
		Boolean,
		default=True,
		comment="Whether account is active"
	)
	
	is_verified: Mapped[bool] = mapped_column(
		Boolean,
		default=False,
		comment="Whether email address is verified"
	)

	# Relationships
	student: Mapped[Optional["Student"]] = relationship(
		back_populates="user",
		uselist=False,
		cascade="all, delete-orphan"
	)
	
	faculty: Mapped[Optional["Faculty"]] = relationship(
		back_populates="user",
		uselist=False,
		cascade="all, delete-orphan"
	)

	def __repr__(self) -> str:
		return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
	
	def __str__(self) -> str:
		return self.email
	
	@property
	def display_name(self) -> str:
		"""Returns display name based on role and related records."""
		if self.role == "faculty" and self.faculty:
			return self.faculty.display_name
		elif self.role == "student" and self.student:
			return self.student.full_name or self.email
		elif self.username:
			return self.username
		return self.email
