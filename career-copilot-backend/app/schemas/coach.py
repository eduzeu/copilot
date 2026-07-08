
from datetime import datetime
from typing import Literal, Optional 
from pydantic import BaseModel, Field


QuestionType = Literal["technical", "behavioral", "system_design", "mixed"]


class CoachQuestionRequest(BaseModel):
    role: str
    company: Optional[str] = None
    job_description: Optional[str] = None
    question_type: str = "technical"
    count: int = 10

class CoachQuestionOut(BaseModel):
    id: int
    question_type: str
    question_text: str
    reason: str | None = None

    class Config:
        from_attributes = True


class CoachSessionOut(BaseModel):
    id: int
    resume_id: int
    application_id: int
    question_type: str
    created_at: datetime
    questions: list[CoachQuestionOut]

    class Config:
        from_attributes = True