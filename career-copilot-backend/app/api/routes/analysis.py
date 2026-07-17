from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.analysis import AnalyzedResumeRequest, AnalysisRunOut
# from app.services.analysis_service import analyze_resume, analyze_from_application_and_resume
from app.services.llm_analysis import analyze_bullet_general, analyze_bullet_with_llm, analyze_resume_general, score_resume_against_jd  
from app.core.config import settings
from app.utils.text_extract import extract_text
from app.services.llm_service import LLMRateLimitError
router = APIRouter(prefix="/analysis", tags=["analysis"])


def _run_ai(operation, *args):
    try:
        return operation(*args)
    except LLMRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail=str(exc),
            headers={"Retry-After": "3600"},
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


async def _read_resume(file: UploadFile) -> str:
    data = await file.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Resume exceeds the 10 MB limit")
    try:
        return extract_text(data, file.filename or "resume")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/resume-feedback")
async def resume_feedback(file: UploadFile = File(...), user=Depends(get_current_user)):
    resume_text = await _read_resume(file)
    return {"analysis": _run_ai(analyze_resume_general, resume_text)}


@router.post("/job-match")
async def job_match(file: UploadFile = File(...), job_description: str = Form(...), user=Depends(get_current_user)):
    resume_text = await _read_resume(file)
    return {"analysis": _run_ai(score_resume_against_jd, resume_text, job_description)}


@router.post("/bullet/general")
def analyze_bullet_general_endpoint(
    bullet: str,
    user=Depends(get_current_user),
):
    result = _run_ai(analyze_bullet_general, bullet)
    return result

@router.post("/bullet/llm")
def analyze_bullet_with_llm_endpoint(
    bullet: str,
    job_description: str,
    user=Depends(get_current_user),
):
    result = _run_ai(analyze_bullet_with_llm, bullet, job_description)
    return result

@router.post("/score")
def score_resume_against_jd_endpoint(
    resume_text: str,
    job_description: str,
    user=Depends(get_current_user),
):
    result = _run_ai(score_resume_against_jd, resume_text, job_description)
    return result
