from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import asc
from sqlalchemy.orm import Session

from backend.api.dependencies import require_roles
from backend.api.submission_helpers import (
    ensure_payment,
    get_submission_or_404,
    serialize_submission,
)
from backend.database.models import ClinicalNote, Submission, User
from backend.database.session import get_db

router = APIRouter()


class DoctorValidateRequest(BaseModel):
    diagnosis: str
    severity: Optional[str] = None
    treatment_needed: Optional[str] = None
    medication: Optional[str] = None


@router.get("/queue")
def doctor_queue(
    current_user: User = Depends(require_roles("doctor", "admin")),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Submission)
        .filter(
            Submission.status == "moderator_approved",
            Submission.submitter_role == "field_worker",
        )
        .order_by(asc(Submission.created_at))
        .all()
    )
    return {"queue": [serialize_submission(s, include_media=True) for s in rows]}


@router.post("/{submission_id}/validate")
def validate_asha_submission(
    submission_id: str,
    payload: DoctorValidateRequest,
    current_user: User = Depends(require_roles("doctor", "admin")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    if sub.status != "moderator_approved":
        raise HTTPException(
            status_code=400,
            detail=f"Submission must be 'moderator_approved' before doctor validation (currently '{sub.status}')",
        )

    note = ClinicalNote(
        submission_id=sub.submission_id,
        doctor_user_id=current_user.user_id,
        diagnosis=payload.diagnosis,
        severity=payload.severity,
        treatment_needed=payload.treatment_needed,
        medication=payload.medication,
    )
    db.add(note)

    sub.status = "doctor_completed"
    sub.doctor_id = current_user.user_id
    sub.updated_at = datetime.utcnow()

    ensure_payment(
        db,
        submission_id=sub.submission_id,
        user_id=sub.submitted_by_user_id,
        role="field_worker",
        amount=50.0,
    )
    ensure_payment(
        db,
        submission_id=sub.submission_id,
        user_id=current_user.user_id,
        role="doctor",
        amount=30.0,
    )

    db.commit()
    db.refresh(sub)
    return serialize_submission(sub)
