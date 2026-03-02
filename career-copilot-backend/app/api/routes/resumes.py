from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.resume import ResumeCreateRequest, ResumeOut
from app.services.resume_service import create_resume, list_resumes, get_resume, delete_resume

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("/", response_model=ResumeOut)
def create_resume_endpoint(req: ResumeCreateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_resume(db, current_user.id, req)

@router.get("/", response_model=list[ResumeOut])
def get_resumes_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_resumes(db, current_user.id)

@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume_endpoint(resume_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_resume(db, current_user.id, resume_id)

@router.delete("/{resume_id}")
def delete_resume_endpoint(resume_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    delete_resume(db, current_user.id, resume_id)   