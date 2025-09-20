import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_students_pagination(monkeypatch, tmp_path):
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'pg.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# seed 3 students
		for i in range(3):
			resp = await ac.post("/api/v1/students/", json={"student_no": f"S{i}", "entry_year": 1400 + i})
			assert resp.status_code == 201
		# get first page limit=2
		resp = await ac.get("/api/v1/students/?limit=2&offset=0")
		assert resp.status_code == 200
		assert len(resp.json()) == 2
		# second page
		resp = await ac.get("/api/v1/students/?limit=2&offset=2")
		assert resp.status_code == 200
		assert len(resp.json()) == 1

