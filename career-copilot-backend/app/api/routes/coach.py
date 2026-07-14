from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.coach import CoachChatRequest, CoachChatResponse, CoachQuestionRequest
from app.services.coach_service import chat_with_career_coach, create_coach_session

router = APIRouter(prefix="/coach", tags=["coach"])

@router.post("/questions")
def generate_coach_questions_endpoint(
    req: CoachQuestionRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_coach_session(db=db, user_id=user.id, req=req)


@router.post("/chat", response_model=CoachChatResponse)
def career_coach_chat(
    req: CoachChatRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return chat_with_career_coach(db, user.id, req)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
