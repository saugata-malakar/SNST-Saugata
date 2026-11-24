from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import asc
from sqlalchemy.orm import Session

from backend.api.dependencies import require_roles
from backend.api.submission_helpers import (
    ensure_payment,
    get_submission_or_404,
    serialize_submission,
)
from backend.database.models import ModeratorReview, Submission, User
from backend.database.session import get_db

router = APIRouter()


class ApproveRequest(BaseModel):
    note: Optional[str] = None


class RejectRequest(BaseModel):
    reason: str


@router.get("/queue")
def moderator_queue(
    current_user: User = Depends(require_roles("moderator", "admin")),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Submission)
        .filter(
            Submission.status == "ai_reviewed",
            Submission.submitter_role == "field_worker",
        )
        .order_by(asc(Submission.created_at))
        .all()
    )
    return {"queue": [serialize_submission(s, include_media=True) for s in rows]}


@router.post("/{submission_id}/approve")
def approve_submission(
    submission_id: str,
    payload: Optional[ApproveRequest] = Body(default=None),
    current_user: User = Depends(require_roles("moderator", "admin")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    if sub.status != "ai_reviewed":
        raise HTTPException(
            status_code=400,
            detail=f"Submission must be in 'ai_reviewed' status (currently '{sub.status}')",
        )

    review = ModeratorReview(
        submission_id=sub.submission_id,
        moderator_user_id=current_user.user_id,
        decision="approved",
        rejection_reason=payload.note if payload else None,
    )
    db.add(review)

    sub.status = "moderator_approved"
    sub.moderator_id = current_user.user_id
    sub.updated_at = datetime.utcnow()

    ensure_payment(
        db,
        submission_id=sub.submission_id,
        user_id=current_user.user_id,
        role="moderator",
        amount=20.0,
    )

    db.commit()
    db.refresh(sub)
    return serialize_submission(sub)


@router.post("/{submission_id}/reject")
def reject_submission(
    submission_id: str,
    payload: RejectRequest,
    current_user: User = Depends(require_roles("moderator", "admin")),
    db: Session = Depends(get_db),
):
    sub = get_submission_or_404(db, submission_id)
    if sub.status != "ai_reviewed":
        raise HTTPException(
            status_code=400,
            detail=f"Submission must be in 'ai_reviewed' status (currently '{sub.status}')",
        )

    review = ModeratorReview(
        submission_id=sub.submission_id,
        moderator_user_id=current_user.user_id,
        decision="rejected",
        rejection_reason=payload.reason,
    )
    db.add(review)

    sub.status = "moderator_rejected"
    sub.moderator_id = current_user.user_id
    sub.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(sub)
    return serialize_submission(sub)
