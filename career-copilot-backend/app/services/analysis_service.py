from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from app.models.analysis import Analysis, AnalysisBullet
from app.services.llm_analysis import analyze_bullet_with_stub
from app.utils.bullets import extract_bullets
from app.models.application import Application
from app.models.resume import Resume

def analyze_resume(
    db: Session,
    user_id: int,
    resume_text: str,
    job_description: str,
    job_title: str | None,
    application_id: int | None = None,
    resume_id: int | None = None,
):
    bullets = extract_bullets(resume_text)

    run = Analysis(
        user_id=user_id,
        resume_id=resume_id,           
        application_id=application_id,
        job_title=job_title,
        job_description=job_description,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    rows: list[AnalysisBullet] = []
    for i, bullet in enumerate(bullets):
        result = analyze_bullet_with_stub(bullet, job_description)

        rows.append(
            AnalysisBullet(
                run_id=run.id,
                bullet_index=i,
                original_text=bullet,
                relevance_score=result["relevance_score"],
                feedback=result["feedback"],
                rewrite_ats=result["rewrite_ats"],
                rewrite_strong=result["rewrite_strong"],
                missing_keywords_csv=",".join(result["missing_keywords"]) if result["missing_keywords"] else None,
            )
        )

    db.add_all(rows)
    db.commit()

    run = (
        db.query(Analysis)
        .options(selectinload(Analysis.bullets))
        .filter(Analysis.id == run.id, Analysis.user_id == user_id)
        .first()
    )
    return run

from sqlalchemy.orm import Session, selectinload

from app.models.analysis import Analysis, AnalysisBullet
from app.services.llm_analysis import analyze_bullet_with_stub
from app.utils.bullets import extract_bullets

def analyze_resume(
    db: Session,
    user_id: int,
    resume_text: str,
    job_description: str,
    job_title: str | None,
    application_id: int | None = None,
    resume_id: int | None = None,
):
    bullets = extract_bullets(resume_text)

    run = Analysis(
        user_id=user_id,
        resume_id=resume_id,           # store linkage if your model has it
        application_id=application_id, # store linkage if your model has it
        job_title=job_title,
        job_description=job_description,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    rows: list[AnalysisBullet] = []
    for i, bullet in enumerate(bullets):
        result = analyze_bullet_with_stub(bullet, job_description)

        rows.append(
            AnalysisBullet(
                run_id=run.id,
                bullet_index=i,
                original_text=bullet,
                relevance_score=result["relevance_score"],
                feedback=result["feedback"],
                rewrite_ats=result["rewrite_ats"],
                rewrite_strong=result["rewrite_strong"],
                missing_keywords_csv=",".join(result["missing_keywords"]) if result["missing_keywords"] else None,
            )
        )

    db.add_all(rows)
    db.commit()

    run = (
        db.query(Analysis)
        .options(selectinload(Analysis.bullets))
        .filter(Analysis.id == run.id, Analysis.user_id == user_id)
        .first()
    )
    return run


def analyze_from_application_and_resume(
    db: Session,
    user_id: int,
    application_id: int,
    resume_id: int,
):
    app = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == user_id)
        .first()
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == user_id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # CHANGE THESE to your real field names:
    resume_text = resume.text  # or resume.content or resume.resume_text
    job_description = app.job_description
    job_title = getattr(app, "job_title", None)

    return analyze_resume(
        db=db,
        user_id=user_id,
        resume_text=resume_text,
        job_description=job_description,
        job_title=job_title,
        application_id=application_id,
        resume_id=resume_id,
    )