import re
from typing import Optional

from app.services.llm_service import call_llm


def generate_questions_for_interviews(
    role: str,
    company: Optional[str] = None,
    job_description: Optional[str] = None,
    question_type: str = "technical",
    count: int = 10,
) -> list[dict]:
    company = company or "Unknown Company"
    job_description = job_description or ""

    prompt = f"""
Generate exactly {count} concise interview questions for a software engineering interview.

Role: {role}
Company: {company}
Question type: {question_type}

Job description:
{job_description}

Rules:
- Do not write an introduction.
- Do not write full LeetCode problem statements.
- Do not include code examples.
- Each question must be one sentence.
- Return only numbered interview questions.
- Keep each question under 25 words.
""".strip()

    try:
        raw = call_llm(prompt, max_tokens=1600)

        lines = [line.strip() for line in raw.split("\n") if line.strip()]

        questions = []

        for line in lines:
            match = re.match(r"^\d+[\.\)]\s*(.+)", line)

            if match:
                cleaned = match.group(1).strip()
                questions.append({
                    "question_type": question_type,
                    "question_text": cleaned,
                    "reason": None,
                })

        return questions[:count]

    except Exception as e:
        return [
            {
                "question_type": question_type,
                "question_text": "Failed to generate interview questions. Please try again.",
                "reason": str(e),
            }
        ]