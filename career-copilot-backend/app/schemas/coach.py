
from datetime import datetime
from typing import Literal, Optional 
from pydantic import BaseModel, Field


QuestionType = Literal["technical", "behavioral", "system_design", "mixed"]


class CoachQuestionRequest(BaseModel):
    role: str
    company: Optional[str] = None
    job_description: Optional[str] = None
    question_type: QuestionType = "technical"
    count: int = Field(default=10, ge=1, le=20)

class CoachQuestionOut(BaseModel):
    id: int
    question_type: str
    question_text: str
    reason: str | None = None

    model_config = {"from_attributes": True}


class CoachSessionOut(BaseModel):
    id: int
    resume_id: int
    application_id: int
    question_type: str
    created_at: datetime
    questions: list[CoachQuestionOut]

    model_config = {"from_attributes": True}
