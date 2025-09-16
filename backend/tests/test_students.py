import os
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture(autouse=True)
def _sqlite_tmp(monkeypatch, tmp_path):
	db_path = tmp_path / "test.db"
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
	yield


@pytest.mark.asyncio
async def test_students_crud():
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# list empty
		resp = await ac.get("/api/v1/students/")
		assert resp.status_code == 200
		assert resp.json() == []
		# create
		payload = {"student_no": "S1001", "entry_year": 1402, "full_name": "Test Student"}
		resp = await ac.post("/api/v1/students/", json=payload)
		assert resp.status_code == 201
		data = resp.json()
		student_id = data["id"]
		# get
		resp = await ac.get(f"/api/v1/students/{student_id}")
		assert resp.status_code == 200
		# update
		resp = await ac.patch(f"/api/v1/students/{student_id}", json={"full_name": "Updated"})
		assert resp.status_code == 200
		assert resp.json()["full_name"] == "Updated"
		# list one
		resp = await ac.get("/api/v1/students/")
		assert resp.status_code == 200
		assert len(resp.json()) == 1
		# delete
		resp = await ac.delete(f"/api/v1/students/{student_id}")
		assert resp.status_code == 204
		# list empty again
		resp = await ac.get("/api/v1/students/")
		assert resp.status_code == 200
		assert resp.json() == []
