from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentOut, StudentUpdate

router = APIRouter(prefix="/api/v1/students", tags=["students"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
	return db.query(Student).all()


@router.post("/", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
	exists = db.query(Student).filter(Student.student_no == payload.student_no).first()
	if exists:
		raise HTTPException(status_code=409, detail="student_no already exists")
	obj = Student(student_no=payload.student_no, entry_year=payload.entry_year, full_name=payload.full_name)
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
	obj = db.get(Student, student_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	return obj


@router.patch("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
	obj = db.get(Student, student_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	if payload.entry_year is not None:
		obj.entry_year = payload.entry_year
	if payload.full_name is not None:
		obj.full_name = payload.full_name
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
	obj = db.get(Student, student_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	db.delete(obj)
	db.commit()
	return None
