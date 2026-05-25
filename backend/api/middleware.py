"""
JWT authentication middleware for FastAPI.

Provides:
- verify_jwt() - Decode and validate JWT tokens
- get_current_user() - FastAPI dependency for protected endpoints
- get_current_patient() - Patient-specific dependency
- get_current_doctor() - Doctor-specific dependency
- get_current_asha() - ASHA worker-specific dependency

Migration from Flask: backend/legacy/middleware/auth_middleware.py

Owner: Sahil Kumar Gupta (adapted from Flask legacy)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import uuid

from backend.utils.config import settings
from backend.database.session import get_db
from backend.database.models import Patient, Doctor, AshaWorker

security = HTTPBearer()


class TokenPayload:
    """JWT token payload structure."""
    def __init__(self, user_id: str, user_type: str, role: Optional[str] = None):
        self.user_id = user_id
        self.user_type = user_type  # "patient", "doctor", "asha", "admin"
        self.role = role


def create_access_token(
    user_id: str,
    user_type: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.
    
    Args:
        user_id: Patient/Doctor/ASHA ID (UUID string)
        user_type: "patient" | "doctor" | "asha" | "admin"
        expires_delta: Custom expiration (defaults to JWT_EXPIRATION_HOURS)
    
    Returns:
        JWT token string
    
    Example:
        token = create_access_token("pat-123", "patient")
    """
    if expires_delta is None:
        expires_delta = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    encoded_jwt = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    
    return encoded_jwt


def verify_jwt(token: str) -> TokenPayload:
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        TokenPayload with user_id and user_type
    
    Raises:
        HTTPException: If token invalid or expired
    
    Example:
        payload = verify_jwt(token)
        print(payload.user_id)  # "pat-123"
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        
        user_id: str = payload.get("user_id")
        user_type: str = payload.get("user_type")
        
        if user_id is None or user_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenPayload(user_id=user_id, user_type=user_type)
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
) -> TokenPayload:
    """
    FastAPI dependency for any authenticated user.
    
    Usage:
        @router.get("/me")
        async def get_me(user: TokenPayload = Depends(get_current_user)):
            return {"user_id": user.user_id, "type": user.user_type}
    """
    token = credentials.credentials
    return verify_jwt(token)


async def get_current_patient(
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Patient:
    """
    FastAPI dependency for patient endpoints.
    Verifies user is a patient and loads patient record.
    
    Usage:
        @router.get("/me")
        async def get_patient_me(patient: Patient = Depends(get_current_patient)):
            return patient
    """
    if user.user_type != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can access this endpoint",
        )
    
    patient = db.query(Patient).filter(
        Patient.patient_id == uuid.UUID(user.user_id)
    ).first()
    
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )
    
    return patient


async def get_current_doctor(
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Doctor:
    """
    FastAPI dependency for doctor endpoints.
    Verifies user is a doctor and loads doctor record.
    
    Usage:
        @router.get("/me")
        async def get_doctor_me(doctor: Doctor = Depends(get_current_doctor)):
            return doctor
    """
    if user.user_type != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can access this endpoint",
        )
    
    doctor = db.query(Doctor).filter(
        Doctor.doctor_id == uuid.UUID(user.user_id)
    ).first()
    
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )
    
    return doctor


async def get_current_asha(
    user: TokenPayload = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AshaWorker:
    """
    FastAPI dependency for ASHA worker endpoints.
    Verifies user is an ASHA worker and loads record.
    
    Usage:
        @router.get("/me")
        async def get_asha_me(asha: AshaWorker = Depends(get_current_asha)):
            return asha
    """
    if user.user_type != "asha":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ASHA workers can access this endpoint",
        )
    
    asha = db.query(AshaWorker).filter(
        AshaWorker.asha_worker_id == uuid.UUID(user.user_id)
    ).first()
    
    if asha is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ASHA worker not found",
        )
    
    return asha
