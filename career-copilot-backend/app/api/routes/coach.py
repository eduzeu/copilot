from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.coach import GenerateCoachQuestionsRequest, CoachSessionOut
from app.services.coach_service import create_coach_session, get_coach_session, list_coach_sessions

router = APIRouter(prefix="/coach", tags=["coach"])


@router.post("/questions", response_model=CoachSessionOut)
def generate_coach_questions_endpoint(
    req: GenerateCoachQuestionsRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_coach_session(db=db, user_id=user.id, req=req)


@router.get("/sessions", response_model=list[CoachSessionOut])
def list_coach_sessions_endpoint(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return list_coach_sessions(db=db, user_id=user.id)


@router.get("/sessions/{session_id}", response_model=CoachSessionOut)
def get_coach_session_endpoint(
    session_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_coach_session(db=db, user_id=user.id, session_id=session_id)