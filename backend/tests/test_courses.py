import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_courses_crud(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'courses.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# empty list
		resp = await ac.get("/api/v1/courses/")
		assert resp.status_code == 200
		assert resp.json() == []
		# create
		payload = {"code": "CS101", "title": "Intro CS", "credits": 3, "department": "CS"}
		resp = await ac.post("/api/v1/courses/", json=payload)
		assert resp.status_code == 201
		course_id = resp.json()["id"]
		# get
		resp = await ac.get(f"/api/v1/courses/{course_id}")
		assert resp.status_code == 200
		# update
		resp = await ac.patch(f"/api/v1/courses/{course_id}", json={"title": "Intro to CS"})
		assert resp.status_code == 200
		assert resp.json()["title"] == "Intro to CS"
		# delete
		resp = await ac.delete(f"/api/v1/courses/{course_id}")
		assert resp.status_code == 204
