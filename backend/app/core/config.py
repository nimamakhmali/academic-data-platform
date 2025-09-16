import os
from pydantic import BaseModel


class Settings(BaseModel):
	app_name: str = "Academic Data Platform API"
	version: str = "0.1.0"
	database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
	jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
	access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
