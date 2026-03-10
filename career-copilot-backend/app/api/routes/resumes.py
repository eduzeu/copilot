from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.resume import ResumeCreateRequest, ResumeOut, ResumeUpdateRequest
from app.services.resume_service import create_resume, list_resumes, get_resume, delete_resume, update_resume, create_resume_from_upload

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post('/upload', response_model=ResumeOut)
async def upload_resume_endpoint(
    title: str,
    file: bytes,
    filename: str,
    content_type: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return create_resume_from_upload(
        db=db,
        user_id=current_user.id,
        title=title,
        filename=filename,
        content_type=content_type,
        file_bytes=file
    )

@router.get("/", response_model=list[ResumeOut])
def get_resumes_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_resumes(db, current_user.id)

@router.put("/{resume_id}", response_model=ResumeOut)
def update_resume_endpoint(
    resume_id: int,
    req: ResumeUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return update_resume(db, user.id, resume_id, req)

@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume_endpoint(resume_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_resume(db, current_user.id, resume_id)

@router.delete("/{resume_id}")
def delete_resume_endpoint(resume_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    delete_resume(db, current_user.id, resume_id)   