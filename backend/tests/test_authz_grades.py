import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_grades_rbac(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'rbac.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# seed a faculty and get token
		reg = await ac.post("/api/v1/auth/register", json={"email": "t@u.com", "username": "t", "role": "faculty", "password": "xsecret"})
		assert reg.status_code == 201
		login = await ac.post("/api/v1/auth/login", data={"username": "t@u.com", "password": "xsecret"})
		token = login.json()["access_token"]
		headers = {"Authorization": f"Bearer {token}"}

		# seed student/course/enrollment
		student = await ac.post("/api/v1/students/", json={"student_no": "S3001"})
		course = await ac.post("/api/v1/courses/", json={"code": "RBAC1", "title": "RBAC"})
		enr = await ac.post("/api/v1/enrollments/", json={"student_id": student.json()["id"], "course_id": course.json()["id"], "term": "1402-1"})
		enr_id = enr.json()["id"]

		# unauthorized create (no token)
		resp = await ac.post("/api/v1/grades/", json={"enrollment_id": enr_id, "value": 15.0})
		assert resp.status_code in (401, 403)

		# authorized create (faculty)
		resp = await ac.post("/api/v1/grades/", headers=headers, json={"enrollment_id": enr_id, "value": 15.0})
		assert resp.status_code == 201
