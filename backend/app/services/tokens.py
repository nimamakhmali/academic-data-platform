from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
	expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
	to_encode = {"sub": subject, "exp": expire}
	return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
	credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
	try:
		payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		email: str | None = payload.get("sub")
		if email is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	user = db.query(User).filter(User.email == email).first()
	if user is None:
		raise credentials_exception
	return user
