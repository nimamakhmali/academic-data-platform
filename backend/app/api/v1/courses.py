from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate

router = APIRouter(prefix="/api/v1/courses", tags=["courses"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
	return db.query(Course).all()


@router.post("/", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
	exists = db.query(Course).filter(Course.code == payload.code).first()
	if exists:
		raise HTTPException(status_code=409, detail="code already exists")
	obj = Course(code=payload.code, title=payload.title, credits=payload.credits, department=payload.department)
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
	obj = db.get(Course, course_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	return obj


@router.patch("/{course_id}", response_model=CourseOut)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
	obj = db.get(Course, course_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	if payload.title is not None:
		obj.title = payload.title
	if payload.credits is not None:
		obj.credits = payload.credits
	if payload.department is not None:
		obj.department = payload.department
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
	obj = db.get(Course, course_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	db.delete(obj)
	db.commit()
	return None
