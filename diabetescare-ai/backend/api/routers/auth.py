import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.api.dependencies import create_access_token, get_current_user
from backend.database.models import User
from backend.database.session import get_db

router = APIRouter()
pwd_ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

ALLOWED_ROLES = {"doctor", "field_worker", "moderator", "admin"}
ALLOWED_WORKER_TYPES = {"ASHA", "ICDS", "CHO"}


def _clean(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None


def _serialize_user(user: User) -> dict:
    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
        "worker_id": user.worker_id,
        "full_name": user.full_name,
        "role": user.role,
        "worker_type": user.worker_type,
        "district": user.district,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


class RegisterRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    worker_id: Optional[str] = None
    password: str
    role: str = "field_worker"   # doctor | field_worker | moderator | admin
    full_name: Optional[str] = None
    worker_type: Optional[str] = None  # ASHA | ICDS | CHO
    district: Optional[str] = None


class LoginRequest(BaseModel):
    identifier: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    worker_id: Optional[str] = None
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user: dict


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = _clean(payload.email)
    phone = _clean(payload.phone)
    username = _clean(payload.username)
    worker_id = _clean(payload.worker_id)
    role = (payload.role or "field_worker").strip().lower()
    if role == "asha":
        role = "field_worker"
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role '{payload.role}'. Must be one of: {', '.join(sorted(ALLOWED_ROLES))}",
        )

    if not any([email, phone, username, worker_id]):
        raise HTTPException(
            status_code=400,
            detail="At least one of email, phone, username, or worker_id is required",
        )

    worker_type = _clean(payload.worker_type)
    if worker_type:
        worker_type = worker_type.upper()
        if worker_type not in ALLOWED_WORKER_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid worker_type '{payload.worker_type}'. Must be ASHA, ICDS, or CHO",
            )

    unique_checks = [
        ("email", User.email, email, "Email already registered"),
        ("phone", User.phone, phone, "Phone already registered"),
        ("username", User.username, username, "Username already registered"),
        ("worker_id", User.worker_id, worker_id, "Worker ID already registered"),
    ]
    for _, column, val, err_msg in unique_checks:
        if val and db.query(User).filter(column == val).first():
            raise HTTPException(status_code=400, detail=err_msg)

    if not worker_id:
        prefix = "DOC" if role == "doctor" else "MOD" if role == "moderator" else "ADM" if role == "admin" else (worker_type or "FW")
        worker_id = f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    user = User(
        email=email,
        phone=phone,
        username=username,
        worker_id=worker_id,
        full_name=_clean(payload.full_name),
        hashed_password=pwd_ctx.hash(payload.password),
        role=role,
        worker_type=worker_type,
        district=_clean(payload.district),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _serialize_user(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ident = (
        _clean(payload.identifier)
        or _clean(payload.email)
        or _clean(payload.phone)
        or _clean(payload.username)
        or _clean(payload.worker_id)
    )
    if not ident:
        raise HTTPException(
            status_code=400,
            detail="Provide identifier, email, phone, username, or worker_id",
        )

    user = (
        db.query(User)
        .filter(
            or_(
                User.email == ident,
                User.phone == ident,
                User.username == ident,
                User.worker_id == ident,
            )
        )
        .first()
    )
    if not user or not user.is_active or not pwd_ctx.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        subject=str(user.user_id),
        user_id=str(user.user_id),
        role=user.role,
        email=user.email,
        phone=user.phone,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user": _serialize_user(user),
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return _serialize_user(current_user)
