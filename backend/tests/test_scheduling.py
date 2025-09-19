import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_scheduling_greedy():
	payload = {
		"term": "1402-1",
		"slots": ["Sat-08", "Sat-10"],
		"sections": [
			{"section_id": "SEC1", "course_code": "CS101", "instructor_id": "I1", "enrolled": 30},
			{"section_id": "SEC2", "course_code": "CS102", "instructor_id": "I1", "enrolled": 40},
		],
		"rooms": [
			{"room_id": "R1", "capacity": 35},
			{"room_id": "R2", "capacity": 50}
		],
		"instructors": [
			{"instructor_id": "I1", "available_slots": ["Sat-08", "Sat-10"]}
		]
	}
	async with AsyncClient(app=app, base_url="http://test") as ac:
		resp = await ac.post("/api/v1/scheduling/generate", json=payload)
		assert resp.status_code == 200
		data = resp.json()
		assert data["term"] == "1402-1"
		# two sections should be scheduled
		assert len(data["items"]) == 2
		# ensure no room-slot reused
		used = set((i["room_id"], i["slot"]) for i in data["items"])
		assert len(used) == len(data["items"])  # unique pairs


@pytest.mark.asyncio
async def test_scheduling_unscheduled_when_capacity_low():
	payload = {
		"term": "1402-1",
		"slots": ["Sat-08"],
		"sections": [
			{"section_id": "SEC1", "course_code": "CS101", "instructor_id": "I1", "enrolled": 60},
		],
		"rooms": [
			{"room_id": "R1", "capacity": 50}
		]
	}
	async with AsyncClient(app=app, base_url="http://test") as ac:
		resp = await ac.post("/api/v1/scheduling/generate", json=payload)
		assert resp.status_code == 200
		data = resp.json()
		assert data["unscheduled"] == ["SEC1"]
