from pydantic import BaseModel, Field


class StudentBase(BaseModel):
	student_no: str = Field(..., max_length=32)
	entry_year: int | None = None
	full_name: str | None = Field(default=None, max_length=128)


class StudentCreate(StudentBase):
	pass


class StudentUpdate(BaseModel):
	entry_year: int | None = None
	full_name: str | None = Field(default=None, max_length=128)


class StudentOut(StudentBase):
	id: int

	class Config:
		from_attributes = True
