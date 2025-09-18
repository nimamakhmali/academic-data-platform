from pydantic import BaseModel, Field


class EnrollmentBase(BaseModel):
	student_id: int
	course_id: int
	term: str = Field(..., max_length=10)
	grade: float | None = None


class EnrollmentCreate(EnrollmentBase):
	pass


class EnrollmentUpdate(BaseModel):
	grade: float | None = None


class EnrollmentOut(EnrollmentBase):
	id: int

	class Config:
		from_attributes = True

