from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.analysis import AnalyzedResumeRequest, AnalysisRunOut
# from app.services.analysis_service import analyze_resume, analyze_from_application_and_resume
from app.services.llm_analysis import analyze_bullet_general, analyze_bullet_with_llm, score_resume_against_jd  
router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/bullet/general")
def analyze_bullet_general_endpoint(
    bullet: str,
    job_description: str,
):
    result = analyze_bullet_general(bullet, job_description)
    return result

@router.post("/bullet/llm")
def analyze_bullet_with_llm_endpoint(
    bullet: str,
    job_description: str,
):
    result = analyze_bullet_with_llm(bullet, job_description)
    return result

@router.post("/score")
def score_resume_against_jd_endpoint(
    resume_text: str,
    job_description: str,
):
    result = score_resume_against_jd(resume_text, job_description)
    return result
