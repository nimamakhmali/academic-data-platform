from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	username: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
	role: Mapped[str] = mapped_column(String(32), default="student")
	password_hash: Mapped[str] = mapped_column(String(255))
