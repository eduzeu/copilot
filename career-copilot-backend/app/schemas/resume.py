from datetime import datetime
from pydantic import BaseModel, Field


class ResumeCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    raw_text: str = Field(..., min_length=50)


class ResumeUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    raw_text: str | None = Field(default=None, min_length=50)


class ResumeOut(BaseModel):
    id: int
    title: str
    raw_text: str
    file_name: str | None = None
    file_path: str | None = None
    file_url: str | None = None
    mime_type: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True