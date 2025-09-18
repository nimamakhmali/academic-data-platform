import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_grades_crud(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'grades.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# seed student, course, enrollment
		student = await ac.post("/api/v1/students/", json={"student_no": "S2001", "entry_year": 1402})
		assert student.status_code == 201
		course = await ac.post("/api/v1/courses/", json={"code": "MATH101", "title": "Math", "credits": 3})
		assert course.status_code == 201
		enrollment = await ac.post("/api/v1/enrollments/", json={"student_id": student.json()["id"], "course_id": course.json()["id"], "term": "1402-1"})
		assert enrollment.status_code == 201
		enrollment_id = enrollment.json()["id"]
		# create grade
		resp = await ac.post("/api/v1/grades/", json={"enrollment_id": enrollment_id, "value": 17.25})
		assert resp.status_code == 201
		grade_id = resp.json()["id"]
		# get
		resp = await ac.get(f"/api/v1/grades/{grade_id}")
		assert resp.status_code == 200
		# update
		resp = await ac.patch(f"/api/v1/grades/{grade_id}", json={"value": 18.0})
		assert resp.status_code == 200
		assert resp.json()["value"] == 18.0
		# delete
		resp = await ac.delete(f"/api/v1/grades/{grade_id}")
		assert resp.status_code == 204
