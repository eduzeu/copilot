from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.models.dashboard import Dashboard


def add_data_to_dashboard(db: Session, user_id: int, data: dict):
    dashboard = db.query(Dashboard).filter(Dashboard.user_id == user_id).first()
    if not dashboard:
        dashboard = Dashboard(user_id=user_id, **data)
        db.add(dashboard)
    else:
        for key, value in data.items():
            setattr(dashboard, key, value)
    db.commit()
    db.refresh(dashboard)
    return dashboard


def get_dashboard(db: Session, user_id: int) -> DashboardResponse:
    dashboard = db.query(Dashboard).filter(Dashboard.user_id == user_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return DashboardResponse(
        total_applications=dashboard.total_applications,
        pending_applications=dashboard.pending_applications,
        interviewing=dashboard.interviewing,
        offers=dashboard.offers,
        interview_rate=dashboard.interview_rate,
        offer_rate=dashboard.offer_rate
    )


