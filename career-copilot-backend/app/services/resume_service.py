from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.resume import Resume
from app.schemas.resume import ResumeCreateRequest


def create_resume(db: Session, user_id: int, req: ResumeCreateRequest) -> Resume:
    resume = Resume(user_id=user_id, title=req.title, raw_text=req.raw_text)
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


def delete_resume(db: Session, user_id: int, resume_id: int) -> None:
    resume = get_resume(db, user_id, resume_id)
    db.delete(resume)
    db.commit()