from datetime import date
from pydantic import BaseModel, HttpUrl
from app.utils.enums import ApplicationStatus

class ApplicationCreateRequest(BaseModel):
    company: str
    role_title: str
    date_applied: date
    status: ApplicationStatus
  
class ApplicationUpdateRequest(BaseModel):
    company: str | None = None
    role_title: str | None = None
    date_applied: date | None = None
    status: ApplicationStatus | None = None 
  
class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company: str
    role_title: str
    date_applied: date
    status: ApplicationStatus
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True