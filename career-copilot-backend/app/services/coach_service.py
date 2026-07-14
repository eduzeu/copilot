from sqlalchemy.orm import Session

from app.schemas.coach import CoachQuestionRequest
from app.services.coach_generator import generate_questions_for_interviews
from app.models.application import Application
from app.models.resume import Resume
from app.schemas.coach import CoachChatRequest
from app.services.career_profile_service import calculate_completeness, get_or_create_profile
from app.services.llm_service import call_llm


def create_coach_session(
    db: Session,
    user_id: int,
    req: CoachQuestionRequest,
):
    generated_questions = generate_questions_for_interviews(
        role=req.role,
        company=req.company,
        job_description=req.job_description,
        question_type=req.question_type,
        count=req.count,
    )

    return {
        "questions": generated_questions
    }


def get_coach_session(db: Session, user_id: int, session_id: int):
    return {
        "message": "Coach session history is disabled for now."
    }


def list_coach_sessions(db: Session, user_id: int):
    return []


def chat_with_career_coach(db: Session, user_id: int, req: CoachChatRequest) -> dict:
    profile = get_or_create_profile(db, user_id)
    applications = (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
        .limit(20)
        .all()
    )
    resume_text = (
        db.query(Resume.raw_text)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .scalar()
    )

    profile_fields = {
        key: getattr(profile, key)
        for key in (
            "status", "school", "degree", "major", "current_year", "graduation_year",
            "current_role", "years_experience", "current_industry", "experiences",
            "technical_skills", "dsa_level", "system_design_level", "behavioral_confidence",
            "preferred_language", "improvement_areas", "certifications", "target_roles",
            "target_companies", "target_industries", "target_locations", "position_types",
            "workplace_preferences", "application_timeline", "primary_goal",
        )
    }
    application_context = [
        {
            "company": item.company,
            "role": item.role_title,
            "status": item.status,
            "date_applied": str(item.date_applied),
        }
        for item in applications
    ]
    history = "\n".join(f"{item.role}: {item.content}" for item in req.history[-10:])
    mode_instruction = {
        "general": "Answer the question with practical, personalized career advice.",
        "weekly_plan": "Create a prioritized seven-day plan with realistic, measurable actions.",
        "application_strategy": "Analyze targeting and pipeline outcomes, then recommend concrete strategy changes.",
        "interview_prep": "Create preparation advice tailored to the user's level, targets, and active interviews.",
        "profile_gaps": "Identify the most important gaps between the user today and their target roles.",
    }[req.mode]
    prompt = f"""
You are Career Copilot, a candid and encouraging career strategist. Use only the supplied
facts when describing the user. Clearly label any inference. Do not invent experience,
application outcomes, or company-specific facts. Prioritize specific next actions over
generic encouragement. Use concise Markdown with short headings and bullets.

Mode: {req.mode}
Instruction: {mode_instruction}
Career profile: {profile_fields}
Recent applications: {application_context}
Latest resume text (may be empty): {(resume_text[:8000] if resume_text else '')}
Recent conversation:
{history}

User: {req.message}
""".strip()
    answer = call_llm(prompt, max_tokens=1800)
    context_used = ["career profile"]
    if applications:
        context_used.append("application pipeline")
    if resume_text:
        context_used.append("latest resume")
    return {
        "answer": answer,
        "mode": req.mode,
        "profile_completeness": calculate_completeness(profile),
        "context_used": context_used,
    }
