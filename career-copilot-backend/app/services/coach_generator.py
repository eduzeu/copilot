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
- write an introduction.
- Do not write full LeetCode problem statements.
- Do not include code examples.
- Each question must be one sentence.
- Return numbered interview questions after introduction.
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

    except Exception:
        fallback = {
            "behavioral": [
                "Tell me about a difficult problem you solved and how you measured success.",
                "Describe a disagreement with a teammate and how you resolved it.",
                "Tell me about a project that did not go as planned and what you changed.",
                "Describe a time you learned a technical skill under a deadline.",
                "What accomplishment best demonstrates your readiness for this role?",
            ],
            "system_design": [
                "How would you clarify requirements before designing a scalable notification service?",
                "How would you design an API rate limiter and explain its tradeoffs?",
                "How would you store and retrieve large volumes of application events?",
                "How would you identify and remove a performance bottleneck in a web service?",
                "How would you make a service resilient to a downstream dependency failure?",
            ],
            "technical": [
                "How would you find duplicate values in a large dataset and discuss the complexity?",
                "When would you choose breadth-first search over depth-first search?",
                "How would you test an API endpoint that depends on a database?",
                "How would you diagnose a request that succeeds locally but times out in production?",
                "Explain a project decision where you traded simplicity for scalability.",
            ],
        }
        pool = fallback.get(question_type, fallback["technical"] + fallback["behavioral"])
        return [
            {"question_type": question_type, "question_text": question, "reason": "Offline fallback"}
            for question in (pool * ((count // len(pool)) + 1))[:count]
        ]
