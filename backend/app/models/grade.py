from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Grade(Base):
	__tablename__ = "grades"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	enrollment_id: Mapped[int] = mapped_column(Integer, ForeignKey("enrollments.id"), nullable=False)
	value: Mapped[float] = mapped_column(Float)

	# Relationships
	enrollment: Mapped["Enrollment"] = relationship(lazy="joined")
