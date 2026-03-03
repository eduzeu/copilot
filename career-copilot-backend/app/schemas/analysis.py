from pydantic import BaseModel, Field 
from typing import List, Optional

class AnalyzedResumeRequest(BaseModel): 
  resume_text: str = Field(..., min_length=50) 
  job_description: str = Field(..., min_length=50)
  job_title: Optional[str] = None


class AnalysisBulletOut(BaseModel):
    bullet_index: int
    original_text: str
    relevance_score: int
    feedback: Optional[str] = None
    rewrite_ats: Optional[str] = None
    rewrite_strong: Optional[str] = None
    missing_keywords: List[str] = []

    class Config:
        from_attributes = True

class AnalysisRunOut(BaseModel):
    id: int
    job_title: Optional[str] = None
    bullets: List[AnalysisBulletOut]

    class Config:
        from_attributes = True
        