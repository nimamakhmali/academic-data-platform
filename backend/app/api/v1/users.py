from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.security import hash_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
	return db.query(User).all()


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
	exists = db.query(User).filter(User.email == payload.email).first()
	if exists:
		raise HTTPException(status_code=409, detail="email already exists")
	obj = User(email=payload.email, username=payload.username, role=payload.role, password_hash=hash_password(payload.password))
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
	obj = db.get(User, user_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	return obj


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
	obj = db.get(User, user_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	if payload.username is not None:
		obj.username = payload.username
	if payload.role is not None:
		obj.role = payload.role
	if payload.password is not None:
		obj.password_hash = hash_password(payload.password)
	db.add(obj)
	db.commit()
	db.refresh(obj)
	return obj


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
	obj = db.get(User, user_id)
	if not obj:
		raise HTTPException(status_code=404, detail="not found")
	db.delete(obj)
	db.commit()
	return None
