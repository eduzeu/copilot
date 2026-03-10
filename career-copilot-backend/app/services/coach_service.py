from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models.application import Application
from app.models.resume import Resume
from app.models.coach import CoachSession, CoachQuestion
from app.schemas.coach import GenerateCoachQuestionsRequest
from app.services.coach_generator import generate_questions_for_interviews

def create_coach_session(
    db: Session,
    user_id: int,
    req: GenerateCoachQuestionsRequest,
) -> CoachSession:
    application = (
        db.query(Application)
        .filter(Application.id == req.application_id, Application.user_id == user_id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    resume = (
        db.query(Resume)
        .filter(Resume.id == req.resume_id, Resume.user_id == user_id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume_text = getattr(resume, "raw_text", None)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume has no text content")

    job_description = getattr(application, "job_description", None)
    if not job_description:
        raise HTTPException(status_code=400, detail="Application has no job description")

    session = CoachSession(
        user_id=user_id,
        resume_id=req.resume_id,
        application_id=req.application_id,
        question_type=req.question_type,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    generated_questions = generate_questions_for_interviews(
        resume_text=resume_text,
        job_description=job_description,
        question_type=req.question_type,
        count=req.count,
    )

    rows = []
    for q in generated_questions:
        rows.append(
            CoachQuestion(
                session_id=session.id,
                question_type=q["question_type"],
                question_text=q["question_text"],
                reason=q.get("reason"),
            )
        )

    db.add_all(rows)
    db.commit()

    session = (
        db.query(CoachSession)
        .options(selectinload(CoachSession.questions))
        .filter(CoachSession.id == session.id, CoachSession.user_id == user_id)
        .first()
    )
    return session


def get_coach_session(db: Session, user_id: int, session_id: int) -> CoachSession:
    session = (
        db.query(CoachSession)
        .options(selectinload(CoachSession.questions))
        .filter(CoachSession.id == session_id, CoachSession.user_id == user_id)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Coach session not found")
    return session


def list_coach_sessions(db: Session, user_id: int) -> list[CoachSession]:
    return (
        db.query(CoachSession)
        .options(selectinload(CoachSession.questions))
        .filter(CoachSession.user_id == user_id)
        .order_by(CoachSession.created_at.desc())
        .all()
    )