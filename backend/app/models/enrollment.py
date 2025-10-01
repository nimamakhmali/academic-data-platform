from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Enrollment(Base):
	__tablename__ = "enrollments"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
	course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False)
	term: Mapped[str] = mapped_column(String(10), nullable=False)
	grade: Mapped[float | None] = mapped_column(nullable=True)

	# Relationships
	student: Mapped["Student"] = relationship(back_populates="enrollments", lazy="joined")
	course: Mapped["Course"] = relationship(back_populates="enrollments", lazy="joined")
