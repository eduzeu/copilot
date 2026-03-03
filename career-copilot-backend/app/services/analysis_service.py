from sqlalchemy.orm import Session

from app.models.analysis import AnalysisRun, AnalysisBullet
from app.services.llm_analysis import analyze_bullet_with_stub
from app.utils.bullets import extract_bullets

def analyze_resume(db: Session, user_id: int, resume_text: str, job_description: str, job_title: str | None):
    bullets = extract_bullets(resume_text)

    run = AnalysisRun(
        user_id=user_id,
        job_title=job_title,
        job_description=job_description,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    for i, bullet in enumerate(bullets):
        result = analyze_bullet_with_stub(bullet, job_description)

        row = AnalysisBullet(
            run_id=run.id,
            bullet_index=i,
            original_text=bullet,
            relevance_score=result["relevance_score"],
            feedback=result["feedback"],
            rewrite_ats=result["rewrite_ats"],
            rewrite_strong=result["rewrite_strong"],
            missing_keywords_csv=",".join(result["missing_keywords"]) if result["missing_keywords"] else None,
        )
        db.add(row)

    db.commit()
    db.refresh(run)
    return run