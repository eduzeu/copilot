
from datetime import date, datetime
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


CoachMode = Literal["general", "weekly_plan", "application_strategy", "interview_prep", "profile_gaps"]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10000)


class CoachChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    mode: CoachMode = "general"
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class CoachChatResponse(BaseModel):
    answer: str
    mode: CoachMode
    profile_completeness: int
    context_used: list[str]
    interaction_id: int
    strategy: str
    fallback: bool = False


class CoachFeedbackRequest(BaseModel):
    helpful: bool


class CoachFeedbackResponse(BaseModel):
    interaction_id: int
    helpful: bool
    policy_updated: bool = True


CoachActionStatus = Literal["pending", "completed", "skipped"]


class CoachActionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=240)
    due_date: date | None = None


class CoachActionUpdate(BaseModel):
    status: CoachActionStatus | None = None
    outcome: str | None = Field(default=None, max_length=2000)


class CoachActionOut(BaseModel):
    id: int
    title: str
    status: CoachActionStatus
    outcome: str | None = None
    due_date: date | None = None
    completed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
