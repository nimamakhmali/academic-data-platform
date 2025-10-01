from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Student(Base):
	__tablename__ = "students"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	student_no: Mapped[str] = mapped_column(String(32), unique=True, index=True)
	entry_year: Mapped[int] = mapped_column(Integer, nullable=True)
	full_name: Mapped[str] = mapped_column(String(128), nullable=True)

	# Relationships
	enrollments: Mapped[list["Enrollment"]] = relationship(
		back_populates="student",
		cascade="all, delete-orphan",
		lazy="selectin",
	)
