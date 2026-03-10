from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.dashboard_service import get_dashboard, add_data_to_dashboard
from app.schemas.dashboard import DashboardResponse


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get('/', response_model=DashboardResponse)
def read_dashboard(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_dashboard(db, current_user.id)

@router.put('/', response_model=DashboardResponse)
def update_dashboard(db: Session = Depends(get_db), current_user = Depends(get_current_user), data: dict = None):
    return add_data_to_dashboard(db, current_user.id, data)

@router.post('/reset', response_model=DashboardResponse)
def reset_dashboard(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return add_data_to_dashboard(db, current_user.id, {
        "total_applications": 0,
        "pending_applications": 0,
        "interviewing": 0,
        "offers": 0
    })
