import os
from pydantic import BaseModel


class Settings(BaseModel):
	app_name: str = "Academic Data Platform API"
	version: str = "0.1.0"
	database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")


settings = Settings()
