import base64
import uuid
from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_user, parse_uuid, require_roles
from backend.api.submission_helpers import (
    ensure_payment,
    get_submission_or_404,
    serialize_submission,
)
from backend.database.models import (
    ClinicalNote,
    Submission,
    SubmissionPhoto,
    SubmissionReport,
    User,
)
from backend.database.session import get_db

router = APIRouter()

PHOTO_TYPE_BY_NUMBER = {
    1: "distant",
    2: "medium",
    3: "close",
}


class CreateSubmissionRequest(BaseModel):
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    patient_weight_kg: Optional[float] = None
    patient_bp_systolic: Optional[int] = None
    patient_bp_diastolic: Optional[int] = None
    patient_blood_sugar: Optional[float] = None
    patient_comorbidities: Optional[Any] = None
    is_followup: bool = False
    original_submission_id: Optional[str] = None


class ClinicalNoteRequest(BaseModel):
    diagnosis: str
    severity: Optional[str] = None
    treatment_needed: Optional[str] = None
    medication: Optional[str] = None


def _check_submission_owner(sub: Submission, user: User) -> None:
    if user.role != "admin" and sub.submitted_by_user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this submission",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_submission(
    payload: CreateSubmissionRequest,
    current_user: User = Depends(require_roles("doctor", "field_worker", "admin")),
    db: Session = Depends(get_db),
):
    orig_uuid = None
    patient_id = payload.patient_id.strip() if payload.patient_id else None

    if payload.original_submission_id:
        orig_uuid = parse_uuid(payload.original_submission_id, "original_submission_id")
        orig = db.query(Submission).filter(Submission.submission_id == orig_uuid).first()
        if not orig:
            raise HTTPException(status_code=404, detail="Original submission not found")
        if not patient_id:
            patient_id = orig.patient_id

    if not patient_id:
        patient_id = f"PT-{uuid.uuid4().hex[:8].upper()}"

    sub = Submission(
        patient_id=patient_id,
        submitted_by_user_id=current_user.user_id,
        submitter_role=current_user.role,
        status="draft",
        patient_name=payload.patient_name,
        patient_age=payload.patient_age,
        patient_weight_kg=payload.patient_weight_kg,
        patient_bp_systolic=payload.patient_bp_systolic,
        patient_bp_diastolic=payload.patient_bp_diastolic,
        patient_blood_sugar=payload.patient_blood_sugar,
        patient_comorbidities=payload.patient_comorbidities,
        is_followup=payload.is_followup or (orig_uuid is not None),
        original_submission_id=orig_uuid,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return serialize_submission(sub)


@router.post("/{submission_id}/photos", status_code=status.HTTP_201_CREATED)
async def upload_photo(
    submission_id: str,
    photo_number: int = Form(...),
    photo_type: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles("doctor", "field_worker", "admin")),
    db: Session = Depends(get_db),
):
    if photo_number not in PHOTO_TYPE_BY_NUMBER:
        raise HTTPException(status_code=400, detail="photo_number must be 1, 2, or 3")

    sub = get_submission_or_404(db, submission_id)
    _check_submission_owner(sub, current_user)

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded photo file is empty")

    encoded = base64.b64encode(raw_bytes).decode("utf-8")
    resolved_type = (photo_type or PHOTO_TYPE_BY_NUMBER[photo_number]).strip().lower()

    existing = (
        db.query(SubmissionPhoto)
        .filter(
            SubmissionPhoto.submission_id == sub.submission_id,
            SubmissionPhoto.photo_number == photo_number,
        )
        .first()
    )
    if existing:
        existing.photo_data = encoded
        existing.photo_type = resolved_type
        photo = existing
    else:
        photo = SubmissionPhoto(
            submission_id=sub.submission_id,
            photo_number=photo_number,
            photo_data=encoded,
            photo_type=resolved_type,
        )
        db.add(photo)

    sub.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(photo)
    return {
        "photo_id": str(photo.photo_id),
        "submission_id": str(photo.submission_id),
        "photo_number": photo.photo_number,
        "photo_type": photo.photo_type,
        "created_at": photo.created_at.isoformat() if photo.created_at else None,
    }


@router.post("/{submission_id}/reports", status_code=status.HTTP_201_CREATED)
async def upload_report(
    submission_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles("doctor", "field_worker", "admin")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    _check_submission_owner(sub, current_user)

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded report file is empty")

    report = SubmissionReport(
        submission_id=sub.submission_id,
        file_data=base64.b64encode(raw_bytes).decode("utf-8"),
        file_name=file.filename or "medical_report",
    )
    db.add(report)
    sub.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(report)
    return {
        "report_id": str(report.report_id),
        "submission_id": str(report.submission_id),
        "file_name": report.file_name,
        "created_at": report.created_at.isoformat() if report.created_at else None,
    }


@router.post("/{submission_id}/clinical-note", status_code=status.HTTP_201_CREATED)
def add_clinical_note(
    submission_id: str,
    payload: ClinicalNoteRequest,
    current_user: User = Depends(require_roles("doctor")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)

    note = ClinicalNote(
        submission_id=sub.submission_id,
        doctor_user_id=current_user.user_id,
        diagnosis=payload.diagnosis,
        severity=payload.severity,
        treatment_needed=payload.treatment_needed,
        medication=payload.medication,
    )
    db.add(note)
    sub.doctor_id = current_user.user_id
    sub.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return {
        "note_id": str(note.note_id),
        "submission_id": str(note.submission_id),
        "doctor_user_id": str(note.doctor_user_id),
        "diagnosis": note.diagnosis,
        "severity": note.severity,
        "treatment_needed": note.treatment_needed,
        "medication": note.medication,
        "created_at": note.created_at.isoformat() if note.created_at else None,
    }


@router.post("/{submission_id}/submit")
def submit_for_ai_check(
    submission_id: str,
    current_user: User = Depends(require_roles("doctor", "field_worker", "admin")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    _check_submission_owner(sub, current_user)

    if sub.status not in ("draft", "rejected"):
        raise HTTPException(
            status_code=400,
            detail=f"Submission in status '{sub.status}' cannot be re-submitted",
        )

    photo_count = (
        db.query(SubmissionPhoto)
        .filter(SubmissionPhoto.submission_id == sub.submission_id)
        .count()
    )

    if photo_count != 3:
        sub.ai_quality_passed = False
        sub.ai_rejection_reason = (
            f"Exactly 3 wound photos (distant, medium, close) are required; found {photo_count}"
        )
        sub.status = "rejected"
        sub.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return serialize_submission(sub)

    # All 3 photos present -> AI quality check passes
    sub.ai_quality_passed = True
    sub.ai_rejection_reason = None
    sub.updated_at = datetime.utcnow()

    if sub.submitter_role == "doctor":
        sub.status = "accepted"
        sub.doctor_id = sub.submitted_by_user_id
        ensure_payment(
            db,
            submission_id=sub.submission_id,
            user_id=sub.submitted_by_user_id,
            role="doctor",
            amount=80.0,
        )
    else:
        sub.status = "ai_reviewed"

    db.commit()
    db.refresh(sub)
    return serialize_submission(sub)


@router.get("/my")
def my_submissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Submission)
        .filter(Submission.submitted_by_user_id == current_user.user_id)
        .order_by(desc(Submission.created_at))
        .all()
    )
    return {"submissions": [serialize_submission(s) for s in rows]}


@router.get("/{submission_id}")
def get_submission_detail(
    submission_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    if (
        current_user.role not in ("admin", "moderator", "doctor")
        and sub.submitted_by_user_id != current_user.user_id
    ):
        raise HTTPException(status_code=403, detail="Not authorized to view this submission")
    return serialize_submission(sub, include_media=True)
