import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.database.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "diabetescare-dev-secret-change-in-prod")
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    user_id: Optional[str] = None,
) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": subject,
        "user_id": user_id or subject,
        "role": role,
        "exp": expire,
    }
    if email:
        payload["email"] = email
    if phone:
        payload["phone"] = phone
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(credentials.credentials)
        user_id: str = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        uid = uuid.UUID(str(user_id))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token subject")

    user = db.query(User).filter(User.user_id == uid).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


def require_roles(*allowed_roles: str):
    """FastAPI dependency factory enforcing that current_user.role is in allowed_roles."""
    def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to roles: {', '.join(allowed_roles)}",
            )
        return current_user
    return _checker


def parse_uuid(value: str, label: str = "ID") -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid {label}")
