from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.application import Application
from app.schemas.application import ApplicationCreateRequest, ApplicationUpdateRequest
from app.core.metrics import increment


def _status_tag(status) -> str:
    return getattr(status, "value", str(status))


def create_application(db: Session, user_id: int, req: ApplicationCreateRequest) -> Application:
    application = Application(user_id=user_id, **req.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    increment("applications.events", tags=["action:created", f"status:{_status_tag(application.status)}"])
    return application


def list_applications(db: Session, user_id: int) -> list[Application]:
    return (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .order_by(Application.id.desc())
        .all()
    )


def get_application(db: Session, user_id: int, application_id: int) -> Application:
    application = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user_id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


def update_application(db: Session, user_id: int, application_id: int, req: ApplicationUpdateRequest) -> Application:
    application = get_application(db, user_id, application_id)
    previous_status = application.status

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    increment("applications.events", tags=["action:updated", f"status:{_status_tag(application.status)}"])
    if req.status is not None and application.status != previous_status:
        increment(
            "applications.status_changes",
            tags=[f"from:{_status_tag(previous_status)}", f"to:{_status_tag(application.status)}"],
        )
    return application


def delete_application(db: Session, user_id: int, application_id: int) -> None:
    application = get_application(db, user_id, application_id)
    status = application.status
    db.delete(application)
    db.commit()
    increment("applications.events", tags=["action:deleted", f"status:{_status_tag(status)}"])
