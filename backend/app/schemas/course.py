from pydantic import BaseModel, Field


class CourseBase(BaseModel):
	code: str = Field(..., max_length=32)
	title: str = Field(..., max_length=255)
	credits: int = 3
	department: str | None = Field(default=None, max_length=64)


class CourseCreate(CourseBase):
	pass


class CourseUpdate(BaseModel):
	title: str | None = Field(default=None, max_length=255)
	credits: int | None = None
	department: str | None = Field(default=None, max_length=64)


class CourseOut(CourseBase):
	id: int

	class Config:
		from_attributes = True
