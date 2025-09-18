from fastapi import Depends, HTTPException
from app.services.tokens import get_current_user


def require_roles(*allowed_roles: str):
	def dependency(user=Depends(get_current_user)):
		if user.role not in allowed_roles:
			raise HTTPException(status_code=403, detail="forbidden")
		return user
	return dependency
