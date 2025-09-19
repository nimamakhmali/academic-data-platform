from typing import List, Set
from app.schemas.scheduling import ScheduleRequest, ScheduleResponse, ScheduledItem


def greedy_schedule(req: ScheduleRequest) -> ScheduleResponse:
	assigned: List[ScheduledItem] = []
	unscheduled: List[str] = []
	# availability map
	instr_avail: dict[str, Set[str]] = {}
	if req.instructors:
		for ia in req.instructors:
			instr_avail[ia.instructor_id] = set(ia.available_slots)
	# room capacities
	rooms = {r.room_id: r.capacity for r in req.rooms}
	# try to assign each section
	used = set()  # (room_id, slot)
	for sec in req.sections:
		placed = False
		for slot in req.slots:
			# respect instructor availability if provided
			if instr_avail and sec.instructor_id in instr_avail and slot not in instr_avail[sec.instructor_id]:
				continue
			for room_id, cap in rooms.items():
				if cap < sec.enrolled:
					continue
				key = (room_id, slot)
				if key in used:
					continue
				assigned.append(ScheduledItem(section_id=sec.section_id, room_id=room_id, slot=slot))
				used.add(key)
				placed = True
				break
			if placed:
				break
		if not placed:
			unscheduled.append(sec.section_id)
	return ScheduleResponse(term=req.term, items=assigned, unscheduled=unscheduled)
