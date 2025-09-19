from pydantic import BaseModel, Field
from typing import List, Optional


class InstructorAvailability(BaseModel):
	instructor_id: str
	available_slots: List[str] = Field(default_factory=list)


class Section(BaseModel):
	section_id: str
	course_code: str
	instructor_id: str
	enrolled: int


class Room(BaseModel):
	room_id: str
	capacity: int


class ScheduleRequest(BaseModel):
	term: str
	slots: List[str]
	sections: List[Section]
	rooms: List[Room]
	instructors: Optional[List[InstructorAvailability]] = None


class ScheduledItem(BaseModel):
	section_id: str
	room_id: str
	slot: str


class ScheduleResponse(BaseModel):
	term: str
	items: List[ScheduledItem]
	unscheduled: List[str] = Field(default_factory=list)
