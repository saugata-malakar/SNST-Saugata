from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.api.dependencies import get_current_user
from backend.database.models import Payment, User
from backend.database.session import get_db

router = APIRouter()


@router.get("/my")
def my_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Payment)
        .filter(Payment.user_id == current_user.user_id)
        .order_by(desc(Payment.created_at))
        .all()
    )
    items = [
        {
            "payment_id": str(p.payment_id),
            "submission_id": str(p.submission_id),
            "role": p.role,
            "amount": p.amount,
            "status": p.status,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
            "date": (p.paid_at or p.created_at).isoformat() if (p.paid_at or p.created_at) else None,
        }
        for p in rows
    ]
    total_paid = sum(p.amount for p in rows if p.status == "paid")
    total_pending = sum(p.amount for p in rows if p.status != "paid")
    return {
        "payments": items,
        "total_earned": total_paid,
        "total_pending": total_pending,
    }
