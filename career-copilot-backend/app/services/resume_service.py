from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.resume import Resume
from app.schemas.resume import ResumeUpdateRequest
from app.services.storage_service import delete_resume_file, upload_resume_file
from app.utils.text_extract import extract_text


async def create_resume_from_upload(db: Session, user_id: int, title: str, file: UploadFile) -> Resume:
    filename = Path(file.filename or "resume").name
    file_bytes = await file.read(settings.max_upload_bytes + 1)
    if len(file_bytes) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Resume exceeds the 10 MB limit")
    try:
        raw_text = extract_text(file_bytes, filename)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    object_name = f"{user_id}/{uuid4().hex}-{filename}"
    content_type = file.content_type or "application/octet-stream"
    try:
        file_url = upload_resume_file(file_bytes, object_name, content_type)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Resume storage failed") from exc

    resume = Resume(user_id=user_id, title=title, raw_text=raw_text, file_name=filename,
                    file_path=object_name if file_url else None, file_url=file_url, mime_type=content_type)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def list_resumes(db: Session, user_id: int) -> list[Resume]:
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()


def get_resume(db: Session, user_id: int, resume_id: int) -> Resume:
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


def update_resume(db: Session, user_id: int, resume_id: int, req: ResumeUpdateRequest) -> Resume:
    resume = get_resume(db, user_id, resume_id)
    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(resume, field, value)
    db.commit()
    db.refresh(resume)
    return resume


def delete_resume(db: Session, user_id: int, resume_id: int) -> None:
    resume = get_resume(db, user_id, resume_id)
    delete_resume_file(resume.file_path)
    db.delete(resume)
    db.commit()
