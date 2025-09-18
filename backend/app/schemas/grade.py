from pydantic import BaseModel


class GradeBase(BaseModel):
	enrollment_id: int
	value: float


class GradeCreate(GradeBase):
	pass


class GradeUpdate(BaseModel):
	value: float | None = None


class GradeOut(GradeBase):
	id: int

	class Config:
		from_attributes = True
