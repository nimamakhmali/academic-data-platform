from fastapi import FastAPI
from app.api.v1.students import router as students_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Academic Data Platform API", version="0.1.0")


@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
	return {"status": "ok"}


app.include_router(students_router)
