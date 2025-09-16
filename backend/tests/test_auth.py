import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login(monkeypatch, tmp_path):
	# set fresh sqlite DB
	monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'auth.db'}")
	async with AsyncClient(app=app, base_url="http://test") as ac:
		# register
		payload = {"email": "user@example.com", "username": "user", "role": "student", "password": "secret123"}
		resp = await ac.post("/api/v1/auth/register", json=payload)
		assert resp.status_code == 201
		# login (OAuth2PasswordRequestForm expects x-www-form-urlencoded)
		resp = await ac.post("/api/v1/auth/login", data={"username": "user@example.com", "password": "secret123"})
		assert resp.status_code == 200
		data = resp.json()
		assert "access_token" in data and data["token_type"] == "bearer"
