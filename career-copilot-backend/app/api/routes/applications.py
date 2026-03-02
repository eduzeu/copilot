from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.application_service import create_application, get_application, update_application, delete_application
from app.services import application_service
from app.schemas.application import ApplicationCreateRequest, ApplicationUpdateRequest, ApplicationResponse
router = APIRouter(prefix="/applications", tags=["applications"])

@router.post('/', response_model=ApplicationResponse)
def create(req: ApplicationCreateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return application_service.create_application(db, current_user.id, req)

@router.get("/{application_id}", response_model=ApplicationResponse)
def read(application_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return application_service.get_application(db, current_user.id, application_id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update(application_id: int, req: ApplicationUpdateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return application_service.update_application(db, current_user.id, application_id, req) 

@router.delete("/{application_id}")
def delete(application_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return application_service.delete_application(db, current_user.id, application_id)