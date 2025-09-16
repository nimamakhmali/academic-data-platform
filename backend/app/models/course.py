from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Course(Base):
	__tablename__ = "courses"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
	title: Mapped[str] = mapped_column(String(255))
	credits: Mapped[int] = mapped_column(Integer, default=3)
	department: Mapped[str | None] = mapped_column(String(64), nullable=True)
