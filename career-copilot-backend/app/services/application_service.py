from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.dashboard_service import add_data_to_dashboard
from app.models.application import Application
from app.schemas.application import ApplicationCreateRequest, ApplicationUpdateRequest


def create_application(db: Session, user_id: int, req: ApplicationCreateRequest) -> Application:
    application = Application(user_id=user_id, **req.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)

    # Update dashboard data
    dashboard_data = {
        "total_applications": application.user.dashboard.total_applications + 1,
        "pending_applications": application.user.dashboard.pending_applications + 1
    }
    add_data_to_dashboard(db, user_id, dashboard_data)

    return application

def get_application(db: Session, user_id: int, application_id: int) -> Application:
    application = db.query(Application).filter(Application.id == application_id, Application.user_id == user_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

def update_application(db: Session, user_id: int, application_id: int, req: ApplicationUpdateRequest) -> Application:
    application = get_application(db, user_id, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)

    if req.status and req.status != application.status:
        # Update dashboard data based on status change
        dashboard_data = {}
        if application.status == "pending":
            dashboard_data["pending_applications"] = application.user.dashboard.pending_applications - 1
        elif application.status == "interviewing":
            dashboard_data["interviewing"] = application.user.dashboard.interviewing - 1
        elif application.status == "offer":
            dashboard_data["offers"] = application.user.dashboard.offers - 1

        if req.status == "pending":
            dashboard_data["pending_applications"] = application.user.dashboard.pending_applications + 1
        elif req.status == "interviewing":
            dashboard_data["interviewing"] = application.user.dashboard.interviewing + 1
        elif req.status == "offer":
            dashboard_data["offers"] = application.user.dashboard.offers + 1

        add_data_to_dashboard(db, user_id, dashboard_data)
    return application

def delete_application(db: Session, user_id: int, application_id: int) -> None:
    application = get_application(db, user_id, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()


