from sqlalchemy.orm import Session

from app.schemas.coach import CoachQuestionRequest
from app.services.coach_generator import generate_questions_for_interviews
from app.models.application import Application
from app.models.resume import Resume
from app.schemas.coach import CoachChatRequest
from app.services.career_profile_service import calculate_completeness, get_or_create_profile
from app.services.llm_service import call_llm
from app.services.coach_learning import STRATEGY_INSTRUCTIONS, choose_strategy, record_interaction


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
    pipeline_counts = {
        status: sum(1 for item in applications if item.status == status)
        for status in ("applied", "interview", "accepted", "rejected")
    }
    history = "\n".join(f"{item.role}: {item.content}" for item in req.history[-10:])
    strategy = choose_strategy(db, user_id, req.mode)
    strategy_instruction = STRATEGY_INSTRUCTIONS[strategy]
    mode_instruction = {
        "general": "Answer the question with practical, personalized career advice.",
        "weekly_plan": "Create at most five prioritized actions for the next seven days. Give each action a measurable finish line and explain why it matters now.",
        "application_strategy": "Diagnose the pipeline without claiming causation from small samples. Recommend specific targeting, resume, networking, and follow-up experiments.",
        "interview_prep": "If an interview-stage application exists, tailor preparation to that role using only known facts. Otherwise build a target-role preparation plan and clearly say it is not company-specific.",
        "profile_gaps": "Rank the three most consequential gaps between the current profile and target roles. Separate confirmed gaps from reasonable hypotheses.",
    }[req.mode]
    prompt = f"""
You are Career Copilot, a sharp, candid, and encouraging career strategist. Your job is
to help the user make better decisions, not to restate their profile.

COACHING RULES:
- Match the user's intent before using career context.
- For greetings, small talk, or messages such as "hey", "how are you", or
  "can we talk", respond warmly in no more than two sentences. Do not analyze
  the profile, provide a plan, or use headings unless the user asks a career question.
- For a specific question, answer that question first. Do not force every response
  into a complete career assessment.
- Use prior conversation turns naturally and do not reintroduce yourself repeatedly.
- Use only supplied facts. Label a useful inference as "Likely" or "Hypothesis".
- Never invent company interview processes, hiring preferences, feedback, deadlines,
  market conditions, or reasons for a rejection.
- A rejection is not evidence that the user performed poorly in an interview.
- Do not recommend researching a company's process as if you already know that process.
- Prioritize the 2-5 actions with the highest expected impact for this user right now.
- Make actions measurable: include scope, frequency, or a clear definition of done.
- Explain why each recommendation follows from the supplied context.
- If a crucial fact is missing, ask one focused follow-up question instead of guessing.
- Avoid generic advice such as "practice more" or "keep applying" without a concrete method.
- Do not repeat a long "current snapshot" unless the user asks for one.
- Keep substantive responses concise enough to act on, usually 250-500 words.
- Finish every sentence and section. If space is limited, provide fewer complete
  recommendations rather than more incomplete ones.

FORMAT:
- For casual conversation, use plain conversational text with no headings.
- For substantive advice, start by directly answering the question, use short
  Markdown headings and clean non-nested bullets, and end with "Best next move"
  containing exactly one immediate action.

Mode: {req.mode}
Instruction: {mode_instruction}
Learned coaching strategy: {strategy}
Strategy instruction: {strategy_instruction}
Career profile: {profile_fields}
Recent applications: {application_context}
Pipeline counts: {pipeline_counts}
Latest resume text (may be empty): {(resume_text[:8000] if resume_text else '')}
Recent conversation:
{history}

User: {req.message}
""".strip()
    answer = call_llm(prompt, max_tokens=3000, thinking_budget=256)
    interaction = record_interaction(
        db, user_id, req.mode, strategy, req.message, answer
    )
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
        "interaction_id": interaction.id,
        "strategy": strategy,
    }
