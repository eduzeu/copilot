import json
from typing import Any

from app.services.llm_service import call_llm_json


def generate_questions_for_interviews(application: Any) -> dict:
    """
    Generate interview questions for a given application using the LLM.

    Args:
        application: SQLAlchemy application object containing job details

    Returns:
        dict with:
        - questions: list[str]
        - error: str | None
        - details: str | None
    """

    # Use getattr so the function doesn't crash if field names differ slightly
    company = getattr(application, "company_name", None) or getattr(application, "company", "Unknown Company")
    role = getattr(application, "role", None) or getattr(application, "role_title", "Unknown Role")
    job_description = getattr(application, "job_description", None) or ""

    if not job_description.strip():
        return {
            "questions": [],
            "error": "Application does not contain a job description.",
            "details": None,
        }

    prompt = f"""
You are a career coach helping a software engineering candidate prepare for interviews.

Based on the application details below, generate 4 interview questions the candidate should prepare for.

Requirements:
- Return ONLY valid JSON
- The JSON must be an array of strings
- Include a mix of likely technical and behavioral questions when appropriate
- Questions should be tailored to the role and job description

APPLICATION DETAILS:
Company: {company}
Role: {role}
Job Description: {job_description}
""".strip()

    try:
        raw = call_llm_json(prompt, max_tokens=512)

        if isinstance(raw, list):
            questions = raw
        elif isinstance(raw, str):
            questions = json.loads(raw)
        else:
            raise ValueError("LLM response was neither a JSON string nor a Python list.")

        if not isinstance(questions, list) or not all(isinstance(q, str) for q in questions):
            raise ValueError("LLM response was not a valid list of question strings.")

        return {
            "questions": questions,
            "error": None,
            "details": None,
        }

    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        return {
            "questions": [],
            "error": "Failed to generate interview questions. Please try again.",
            "details": str(e),
        }