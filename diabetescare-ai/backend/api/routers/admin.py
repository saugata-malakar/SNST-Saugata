from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, func, or_
from sqlalchemy.orm import Session

from backend.api.dependencies import parse_uuid, require_roles
from backend.api.submission_helpers import serialize_submission
from backend.database.models import Payment, Submission, User
from backend.database.session import get_db

router = APIRouter()


@router.get("/users")
def list_users(
    role: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role.strip().lower())
    if search:
        pat = f"%{search.strip()}%"
        q = q.filter(
            or_(
                User.email.ilike(pat),
                User.phone.ilike(pat),
                User.username.ilike(pat),
                User.worker_id.ilike(pat),
                User.full_name.ilike(pat),
                User.district.ilike(pat),
            )
        )
    users = q.order_by(desc(User.created_at)).all()
    return {
        "users": [
            {
                "user_id": str(u.user_id),
                "email": u.email,
                "phone": u.phone,
                "username": u.username,
                "worker_id": u.worker_id,
                "full_name": u.full_name,
                "role": u.role,
                "worker_type": u.worker_type,
                "district": u.district,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]
    }


@router.get("/submissions")
def list_submissions(
    status: Optional[str] = Query(default=None),
    submitter_role: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    q = db.query(Submission)
    if status:
        q = q.filter(Submission.status == status.strip().lower())
    if submitter_role:
        q = q.filter(Submission.submitter_role == submitter_role.strip().lower())
    if search:
        pat = f"%{search.strip()}%"
        q = q.filter(
            or_(
                Submission.patient_id.ilike(pat),
                Submission.patient_name.ilike(pat),
            )
        )
    rows = q.order_by(desc(Submission.created_at)).all()
    return {"submissions": [serialize_submission(s) for s in rows]}


@router.get("/payments")
def list_payments(
    role: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    user_id: Optional[str] = Query(default=None),
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    q = db.query(Payment)
    if role:
        q = q.filter(Payment.role == role.strip().lower())
    if status:
        q = q.filter(Payment.status == status.strip().lower())
    if user_id:
        q = q.filter(Payment.user_id == parse_uuid(user_id, "user_id"))

    rows = q.order_by(desc(Payment.created_at)).all()
    return {
        "payments": [
            {
                "payment_id": str(p.payment_id),
                "submission_id": str(p.submission_id),
                "user_id": str(p.user_id),
                "role": p.role,
                "amount": p.amount,
                "status": p.status,
                "paid_at": p.paid_at.isoformat() if p.paid_at else None,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in rows
        ]
    }


@router.get("/stats")
def dashboard_stats(
    current_user: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    users_by_role = dict(
        db.query(User.role, func.count(User.user_id)).group_by(User.role).all()
    )
    submissions_by_status = dict(
        db.query(Submission.status, func.count(Submission.submission_id))
        .group_by(Submission.status)
        .all()
    )
    total_payout = db.query(func.coalesce(func.sum(Payment.amount), 0.0)).scalar() or 0.0
    paid_payout = (
        db.query(func.coalesce(func.sum(Payment.amount), 0.0))
        .filter(Payment.status == "paid")
        .scalar()
        or 0.0
    )

    return {
        "total_users": sum(users_by_role.values()),
        "users_by_role": users_by_role,
        "total_submissions": sum(submissions_by_status.values()),
        "submissions_by_status": submissions_by_status,
        "total_payments_amount": float(total_payout),
        "paid_payments_amount": float(paid_payout),
    }
