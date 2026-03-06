from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.analysis import AnalyzedResumeRequest, AnalysisRunOut
from app.services.analysis_service import analyze_resume, analyze_from_application_and_resume
from app.services.llm_analysis import analyze_bullet_general, analyze_bullet_with_llm, score_resume_against_jd  
router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/resume", response_model=AnalysisRunOut)
def analyze_resume_endpoint(
    req: AnalyzedResumeRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    run = analyze_resume(
        db=db,
        user_id=user.id,
        resume_text=req.resume_text,
        job_description=req.job_description,
        job_title=req.job_title,
    )
    # Convert missing_keywords_csv -> list in response (quick patch in schema layer)
    # easiest: just load run.bullets here and patch attr
    for b in run.bullets:
        mk = (b.missing_keywords_csv or "").strip()
        setattr(b, "missing_keywords", [x for x in mk.split(",") if x] if mk else [])
    return run

@router.post("/application/{application_id}/resume/{resume_id}", response_model=AnalysisRunOut)
def analyze_from_application_and_resume_endpoint(
    application_id: int,
    resume_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    run = analyze_from_application_and_resume(db, user.id, application_id, resume_id)
    for b in run.bullets:
        mk = (b.missing_keywords_csv or "").strip()
        setattr(b, "missing_keywords", [x for x in mk.split(",") if x] if mk else [])
    return run  

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
