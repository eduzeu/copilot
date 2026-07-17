from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.coach import CoachChatRequest, CoachChatResponse, CoachFeedbackRequest, CoachFeedbackResponse, CoachQuestionRequest
from app.services.coach_service import chat_with_career_coach, create_coach_session
from app.services.coach_learning import train_from_feedback
from app.services.llm_service import LLMRateLimitError

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
    except LLMRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail=str(exc),
            headers={"Retry-After": "3600"},
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.put("/interactions/{interaction_id}/feedback", response_model=CoachFeedbackResponse)
def coach_feedback(
    interaction_id: int,
    req: CoachFeedbackRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    interaction = train_from_feedback(db, user.id, interaction_id, req.helpful)
    return {
        "interaction_id": interaction.id,
        "helpful": bool(interaction.feedback),
        "policy_updated": True,
    }
