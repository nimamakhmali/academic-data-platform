from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut, EnrollmentUpdate

router = APIRouter(prefix="/api/v1/enrollments", tags=["enrollments"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/", response_model=list[EnrollmentOut])
def list_enrollments(db: Session = Depends(get_db)):
	return db.query(Enrollment).all()


@router.post("/", response_model=EnrollmentOut, status_code=201)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
	# Check if student exists
	from app.models.student import Student
	student = db.get(Student, payload.student_id)
	if not student:
		raise HTTPException(status_code=404, detail="student not found")
	
	# Check if course exists
	from app.models.course import Course
	course = db.get(Course, payload.course_id)
	if not course:
		raise HTTPException(status_code=404, detail="course not found")
	
	# Check for duplicate enrollment
	exists = db.query(Enrollment).filter(
		Enrollment.student_id == payload.student_id,
		Enrollment.course_id == payload.course_id,
		Enrollment.term == payload.term
	).first()
	if exists:
		raise HTTPException(status_code=409, detail="enrollment already exists")
	
	obj = Enrollment(
		student_id=payload.student_id,
		course_id=payload.course_id,
		term=payload.term,
		grade=payload.grade
	)
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.get("/{enrollment_id}", response_model=EnrollmentOut)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
	obj = db.get(Enrollment, enrollment_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	return obj


@router.patch("/{enrollment_id}", response_model=EnrollmentOut)
def update_enrollment(enrollment_id: int, payload: EnrollmentUpdate, db: Session = Depends(get_db)):
	obj = db.get(Enrollment, enrollment_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	if payload.grade is not None:
		obj.grade = payload.grade
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
	obj = db.get(Enrollment, enrollment_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	db.delete(obj)
	db.commit()
	return None
