import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_enrollments_crud(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'enrollments.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# Create student and course first
		student_payload = {"student_no": "S1001", "entry_year": 1402, "full_name": "Test Student"}
		student_resp = await ac.post("/api/v1/students/", json=student_payload)
		assert student_resp.status_code == 201
		student_id = student_resp.json()["id"]
		
		course_payload = {"code": "CS101", "title": "Intro CS", "credits": 3, "department": "CS"}
		course_resp = await ac.post("/api/v1/courses/", json=course_payload)
		assert course_resp.status_code == 201
		course_id = course_resp.json()["id"]
		
		# Create enrollment
		enrollment_payload = {"student_id": student_id, "course_id": course_id, "term": "1402-1", "grade": 18.5}
		enrollment_resp = await ac.post("/api/v1/enrollments/", json=enrollment_payload)
		assert enrollment_resp.status_code == 201
		enrollment_id = enrollment_resp.json()["id"]
		
		# Get enrollment
		get_resp = await ac.get(f"/api/v1/enrollments/{enrollment_id}")
		assert get_resp.status_code == 200
		
		# Update grade
		update_resp = await ac.patch(f"/api/v1/enrollments/{enrollment_id}", json={"grade": 19.0})
		assert update_resp.status_code == 200
		assert update_resp.json()["grade"] == 19.0
		
		# Delete enrollment
		delete_resp = await ac.delete(f"/api/v1/enrollments/{enrollment_id}")
		assert delete_resp.status_code == 204
