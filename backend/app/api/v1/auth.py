from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.security import verify_password, hash_password
from app.services.tokens import create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
	if db.query(User).filter(User.email == payload.email).first():
		raise HTTPException(status_code=409, detail="email already exists")
	user = User(email=payload.email, username=payload.username, role=payload.role, password_hash=hash_password(payload.password))
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == form.username).first()
	if not user or not verify_password(form.password, user.password_hash):
		raise HTTPException(status_code=401, detail="invalid credentials")
	token = create_access_token(user.email)
	return {"access_token": token, "token_type": "bearer"}
