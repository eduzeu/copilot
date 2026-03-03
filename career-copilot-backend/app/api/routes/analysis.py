from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.analysis import AnalyzeResumeRequest, AnalysisRunOut
from app.services.analysis_service import analyze_resume

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/resume", response_model=AnalysisRunOut)
def analyze_resume_endpoint(
    req: AnalyzeResumeRequest,
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