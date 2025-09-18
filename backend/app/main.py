from fastapi import FastAPI
from app.api.v1.students import router as students_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.courses import router as courses_router
from app.api.v1.enrollments import router as enrollments_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Academic Data Platform API", version="0.1.0")


@app.on_event("startup")
def on_startup():
	Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
	return {"status": "ok"}


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)
