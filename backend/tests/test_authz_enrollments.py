import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_enrollments_rbac(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'rbac_enr.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# faculty token
		await ac.post("/api/v1/auth/register", json={"email": "f@u.com", "username": "f", "role": "faculty", "password": "secretx"})
		login = await ac.post("/api/v1/auth/login", data={"username": "f@u.com", "password": "secretx"})
		token = login.json()["access_token"]
		headers = {"Authorization": f"Bearer {token}"}

		# seed student & course
		student = await ac.post("/api/v1/students/", json={"student_no": "S4001"})
		course = await ac.post("/api/v1/courses/", json={"code": "ENR1", "title": "Enroll"})

		# unauthorized create
		resp = await ac.post("/api/v1/enrollments/", json={"student_id": student.json()["id"], "course_id": course.json()["id"], "term": "1402-1"})
		assert resp.status_code in (401, 403)

		# authorized create
		resp = await ac.post("/api/v1/enrollments/", headers=headers, json={"student_id": student.json()["id"], "course_id": course.json()["id"], "term": "1402-1"})
		assert resp.status_code == 201

