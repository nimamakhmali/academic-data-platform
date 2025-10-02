from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Department(Base):
    """
    Department model representing academic departments/faculties.
    
    Attributes:
        id: Primary key
        name: Department name (e.g., "Computer Engineering")
        code: Department code (e.g., "CE", "EE") 
        description: Optional description of the department
        established_year: Year when department was established
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
        is_active: Whether department is currently active
    
    Relationships:
        faculty: List of faculty members in this department
        courses: List of courses offered by this department
        students: List of students enrolled in this department
    """
    
    __tablename__ = "departments"

    # Primary Fields
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Unique identifier for department"
    )
    
    name: Mapped[str] = mapped_column(
        String(128), 
        nullable=False,
        index=True,
        comment="Full name of the department"
    )
    
    code: Mapped[str] = mapped_column(
        String(16), 
        unique=True, 
        nullable=False,
        index=True,
        comment="Short code for department (e.g., CE, EE)"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Description of department activities and focus"
    )
    
    established_year: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Year when department was established"
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
        comment="Whether department is currently active"
    )

    # Relationships (will be defined after creating Faculty and Course models)
    # faculty: Mapped[List["Faculty"]] = relationship(back_populates="department")
    # courses: Mapped[List["Course"]] = relationship(back_populates="department") 
    # students: Mapped[List["Student"]] = relationship(back_populates="department")

    def __repr__(self) -> str:
        return f"<Department(id={self.id}, code='{self.code}', name='{self.name}')>"
    
    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
