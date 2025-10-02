"""
Models package for Academic Data Platform.

This package contains all database models and their relationships.
Import all models here to ensure they are available for Alembic migrations.
"""

from .user import User
from .student import Student  
from .course import Course
from .enrollment import Enrollment
from .grade import Grade
from .department import Department
from .faculty import Faculty
from .research_item import ResearchItem

__all__ = [
    "User",
    "Student", 
    "Course",
    "Enrollment",
    "Grade",
    "Department",
    "Faculty",
    "ResearchItem",
]
