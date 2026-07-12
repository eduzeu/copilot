from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.dashboard import DashboardResponse


def get_dashboard(db: Session, user_id: int) -> DashboardResponse:
    rows = (
        db.query(Application.status, func.count(Application.id))
        .filter(Application.user_id == user_id)
        .group_by(Application.status)
        .all()
    )
    counts = {status: count for status, count in rows}
    total = sum(counts.values())
    interviews = counts.get("interview", 0)
    offers = counts.get("accepted", 0)
    return DashboardResponse(
        user_id=user_id,
        total_applications=total,
        pending_applications=counts.get("pending", 0),
        interviewing=interviews,
        offers=offers,
        interview_rate=(interviews / total * 100) if total else 0,
        offer_rate=(offers / total * 100) if total else 0,
    )
