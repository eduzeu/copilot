from sqlalchemy.orm import Session

from app.schemas.coach import CoachQuestionRequest
from app.services.coach_generator import generate_questions_for_interviews


def create_coach_session(
    db: Session,
    user_id: int,
    req: CoachQuestionRequest,
):
    generated_questions = generate_questions_for_interviews(
        role=req.role,
        company=req.company,
        job_description=req.job_description,
        question_type=req.question_type,
        count=req.count,
    )

    return {
        "questions": generated_questions
    }


def get_coach_session(db: Session, user_id: int, session_id: int):
    return {
        "message": "Coach session history is disabled for now."
    }


def list_coach_sessions(db: Session, user_id: int):
    return []