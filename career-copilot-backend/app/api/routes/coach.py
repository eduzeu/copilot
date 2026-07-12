from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.coach import CoachQuestionRequest
from app.services.coach_service import create_coach_session

router = APIRouter(prefix="/coach", tags=["coach"])

@router.post("/questions")
def generate_coach_questions_endpoint(
    req: CoachQuestionRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return create_coach_session(db=db, user_id=user.id, req=req)
