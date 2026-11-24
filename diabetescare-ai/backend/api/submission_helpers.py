from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import parse_uuid
from backend.database.models import Payment, Submission


def get_submission_or_404(db: Session, submission_id_str: str) -> Submission:
    """Fetch a Submission by UUID string or raise 400/404."""
    sid = parse_uuid(submission_id_str, "submission_id")
    sub = db.query(Submission).filter(Submission.submission_id == sid).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return sub


def ensure_payment(
    db: Session,
    submission_id,
    user_id,
    role: str,
    amount: float,
    mark_paid: bool = True,
) -> Payment:
    """Create a Payment record if one does not already exist for (submission, user, role)."""
    existing = (
        db.query(Payment)
        .filter(
            Payment.submission_id == submission_id,
            Payment.user_id == user_id,
            Payment.role == role,
        )
        .first()
    )
    if existing:
        return existing

    now = datetime.utcnow()
    payment = Payment(
        submission_id=submission_id,
        user_id=user_id,
        role=role,
        amount=amount,
        status="paid" if mark_paid else "pending",
        paid_at=now if mark_paid else None,
        created_at=now,
    )
    db.add(payment)
    return payment


def serialize_submission(sub: Submission, include_media: bool = False) -> dict:
    """Serialize a Submission with optional photo/report base64 payloads."""
    photos_sorted = sorted(sub.photos or [], key=lambda p: p.photo_number)
    return {
        "submission_id": str(sub.submission_id),
        "patient_id": sub.patient_id,
        "submitted_by_user_id": str(sub.submitted_by_user_id),
        "submitter_role": sub.submitter_role,
        "status": sub.status,
        "ai_quality_passed": sub.ai_quality_passed,
        "ai_rejection_reason": sub.ai_rejection_reason,
        "moderator_id": str(sub.moderator_id) if sub.moderator_id else None,
        "doctor_id": str(sub.doctor_id) if sub.doctor_id else None,
        "patient_name": sub.patient_name,
        "patient_age": sub.patient_age,
        "patient_weight_kg": sub.patient_weight_kg,
        "patient_bp_systolic": sub.patient_bp_systolic,
        "patient_bp_diastolic": sub.patient_bp_diastolic,
        "patient_blood_sugar": sub.patient_blood_sugar,
        "patient_comorbidities": sub.patient_comorbidities,
        "is_followup": sub.is_followup,
        "original_submission_id": str(sub.original_submission_id) if sub.original_submission_id else None,
        "created_at": sub.created_at.isoformat() if sub.created_at else None,
        "updated_at": sub.updated_at.isoformat() if sub.updated_at else None,
        "photo_count": len(photos_sorted),
        "photos": [
            {
                "photo_id": str(p.photo_id),
                "photo_number": p.photo_number,
                "photo_type": p.photo_type,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                **({"photo_data": p.photo_data} if include_media else {}),
            }
            for p in photos_sorted
        ],
        "reports": [
            {
                "report_id": str(r.report_id),
                "file_name": r.file_name,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                **({"file_data": r.file_data} if include_media else {}),
            }
            for r in (sub.reports or [])
        ],
        "clinical_notes": [
            {
                "note_id": str(n.note_id),
                "doctor_user_id": str(n.doctor_user_id),
                "diagnosis": n.diagnosis,
                "severity": n.severity,
                "treatment_needed": n.treatment_needed,
                "medication": n.medication,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in (sub.clinical_notes or [])
        ],
        "moderator_reviews": [
            {
                "review_id": str(m.review_id),
                "moderator_user_id": str(m.moderator_user_id),
                "decision": m.decision,
                "rejection_reason": m.rejection_reason,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in (sub.moderator_reviews or [])
        ],
        "payments": [
            {
                "payment_id": str(pay.payment_id),
                "user_id": str(pay.user_id),
                "role": pay.role,
                "amount": pay.amount,
                "status": pay.status,
                "paid_at": pay.paid_at.isoformat() if pay.paid_at else None,
            }
            for pay in (sub.payments or [])
        ],
    }
