from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
	email: EmailStr
	username: str | None = Field(default=None, max_length=64)
	role: str = Field(default="student", max_length=32)


class UserCreate(UserBase):
	password: str = Field(min_length=6)


class UserUpdate(BaseModel):
	username: str | None = Field(default=None, max_length=64)
	role: str | None = Field(default=None, max_length=32)
	password: str | None = Field(default=None, min_length=6)


class UserOut(UserBase):
	id: int

	class Config:
		from_attributes = True
