
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


QuestionType = Literal["technical", "behavioral", "system_design", "mixed"]


class GenerateCoachQuestionsRequest(BaseModel):
    resume_id: int
    application_id: int
    question_type: QuestionType
    count: int = Field(default=5, ge=1, le=10)


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