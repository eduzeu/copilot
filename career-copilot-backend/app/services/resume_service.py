from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.resume import Resume
from app.schemas.resume import ResumeCreateRequest
from app.services.storage_service import upload_resume_file, get_public_resume_url
from app.utils.text_extract import extract_text_from_resume
from app.services.storage_service import upload_resume_file, get_public_resume_url
from app.utils.text_extract import extract_text_from_resume
    
def create_resume_from_upload(
    db: Session,
    user_id: int,
    title: str,
    filename: str,
    content_type: str | None,
    file_bytes: bytes,
) -> Resume:
    extracted_text = extract_text_from_resume(
        file_bytes=file_bytes,
        filename=filename,
        content_type=content_type,
    )
   

def list_resumes(db: Session, user_id: int) -> list[Resume]:
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()


def get_resume(db: Session, user_id: int, resume_id: int) -> Resume:
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

from app.schemas.resume import ResumeCreateRequest, ResumeUpdateRequest


def update_resume(db: Session, user_id: int, resume_id: int, req: ResumeUpdateRequest) -> Resume:
    resume = get_resume(db, user_id, resume_id)

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(resume, field, value)

    db.commit()
    db.refresh(resume)
    return resume

def delete_resume(db: Session, user_id: int, resume_id: int) -> None:
    resume = get_resume(db, user_id, resume_id)
    db.delete(resume)
    db.commit()