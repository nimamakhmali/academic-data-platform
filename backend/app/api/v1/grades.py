from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.grade import Grade
from app.models.enrollment import Enrollment
from app.schemas.grade import GradeCreate, GradeOut, GradeUpdate
from app.services.authz import require_roles
from app.services.pagination import pagination_params, apply_pagination

router = APIRouter(prefix="/api/v1/grades", tags=["grades"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/", response_model=list[GradeOut])
def list_grades(db: Session = Depends(get_db), pag=Depends(pagination_params)):
	limit, offset = pag
	q = db.query(Grade)
	return apply_pagination(q, limit, offset).all()


@router.post("/", response_model=GradeOut, status_code=201, dependencies=[Depends(require_roles("faculty", "admin"))])
def create_grade(payload: GradeCreate, db: Session = Depends(get_db)):
	# verify enrollment exists
	enr = db.get(Enrollment, payload.enrollment_id)
	if not enr:
		raise HTTPException(status_code=404, detail="enrollment not found")
	obj = Grade(enrollment_id=payload.enrollment_id, value=payload.value)
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.get("/{grade_id}", response_model=GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
	obj = db.get(Grade, grade_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	return obj


@router.patch("/{grade_id}", response_model=GradeOut, dependencies=[Depends(require_roles("faculty", "admin"))])
def update_grade(grade_id: int, payload: GradeUpdate, db: Session = Depends(get_db)):
	obj = db.get(Grade, grade_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	if payload.value is not None:
		obj.value = payload.value
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.delete("/{grade_id}", status_code=204, dependencies=[Depends(require_roles("faculty", "admin"))])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
	obj = db.get(Grade, grade_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	db.delete(obj)
	db.commit()
	return None
