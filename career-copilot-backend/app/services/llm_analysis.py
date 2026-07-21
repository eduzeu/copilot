import json 
from typing import Literal

from pydantic import BaseModel, Field, model_validator
from app.services.llm_service import call_llm_json

SYSTEM_PROMPT = '''
You are a master resume coach and ATS (Applicant Tracking System) optimization expert. 
Provide constructive, actionable feedback and always respond with valid JSON only.
'''


class ResumeFeedbackPayload(BaseModel):
    is_resume: bool
    quality_score: int | None = Field(default=None, ge=0, le=100)
    feedback: str
    rewrite_ats: str | None = None
    rewrite_strong: str | None = None
    suggestions: list[str] = Field(default_factory=list)
    quantification_suggestions: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def non_resume_has_no_score(self):
        if not self.is_resume:
            self.quality_score = None
            self.rewrite_ats = None
            self.rewrite_strong = None
            self.suggestions = []
            self.quantification_suggestions = []
        return self


class BulletPayload(BaseModel):
    quality_score: int = Field(ge=0, le=100)
    feedback: str
    rewrite_ats: str
    rewrite_strong: str
    suggestions: list[str] = Field(default_factory=list)
    quantification_suggestions: list[str] = Field(default_factory=list)


class BulletMatchPayload(BaseModel):
    relevance_score: int = Field(ge=0, le=100)
    feedback: str
    rewrite_ats: str
    rewrite_strong: str
    missing_keywords: list[str] = Field(default_factory=list)


class JobMatchPayload(BaseModel):
    is_resume: bool
    overall_score: int | None = Field(default=None, ge=0, le=100)
    summary: str
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    recommendation: Literal["Strong Match", "Good Match", "Partial Match", "Weak Match"] | None = None

    @model_validator(mode="after")
    def non_resume_has_no_score(self):
        if not self.is_resume:
            self.overall_score = None
            self.strengths = []
            self.gaps = []
            self.missing_keywords = []
            self.recommendation = None
        return self

def analyze_resume_general(resume_text: str) -> dict:
    """
    Analyze a full resume for general quality, ATS readiness, and impact.
    """
    prompt = f"""Analyze this full resume for general quality.
Evaluate clarity, structure, measurable impact, action verbs, ATS readability, and missing detail.

RESUME:
{resume_text}

Return a JSON object with exactly these fields:
{{
    "is_resume": <true only when the document is actually a resume or CV>,
    "quality_score": <integer 0-100 reflecting overall resume quality>,
    "feedback": <2-4 sentence overall summary>,
    "rewrite_ats": <short paragraph describing the highest-priority ATS rewrite strategy>,
    "rewrite_strong": <short paragraph describing how to make the resume stronger for a human reviewer>,
    "suggestions": <list of 4-6 short, specific improvements>,
    "quantification_suggestions": <list of 3-6 metrics or achievements the candidate could quantify>
}}

If the document is not a resume or CV, set is_resume to false, explain what the
document appears to be in feedback, set quality_score to null, set both rewrite
fields to null, and return empty lists. Do not score a non-resume document."""

    raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=2048, schema=ResumeFeedbackPayload)
    return {
        "is_resume": bool(raw.get("is_resume", True)),
        "quality_score": raw.get("quality_score"),
        "feedback": raw.get("feedback"),
        "rewrite_ats": raw.get("rewrite_ats"),
        "rewrite_strong": raw.get("rewrite_strong"),
        "suggestions": raw.get("suggestions", []),
        "quantification_suggestions": raw.get("quantification_suggestions", []),
    }

def analyze_bullet_general(bullet: str) -> dict:

    '''
    Option 1: analyze a resume bullet point with no job description context,
        providing general feedback on clarity, impact, and grammar.

        Args: 
            bullet: the resume bullet point to analyze
        Returns:
            a dictionary with the analysis results, including relevance_score, feedback, rewrite_ats, rewrite_strong, and missing_keywords
    '''

    prompt = f"""Analyze this resume bullet point for general quality. 
            Evaluate it on clarity, use of strong action verbs, quantification of impact, and ATS formatting best practices.

            RESUME BULLET:
            {bullet}

            Return a JSON object with exactly these fields:
            {{
                "quality_score": <integer 0-100 reflecting overall bullet quality>,
                "feedback": <specific, actionable feedback — 2-3 sentences on what works and what doesn't>,
                "rewrite_ats": <rewritten bullet optimized for ATS keyword formatting>,
                "rewrite_strong": <rewritten bullet optimized for impact with strong verbs and quantification>,
                "suggestions": <list of 3-5 short, specific tips to improve this bullet>,
                "quantification_suggestions": <list of specific metrics or achievements that could be quantified, if applicable>
            }}"""

    try: 
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT, schema=BulletPayload)
        result = raw

        return {
            "quality_score": result.get("quality_score"),
            "feedback": result.get("feedback"),
            "rewrite_ats": result.get("rewrite_ats"),
            "rewrite_strong": result.get("rewrite_strong"),
            "suggestions": result.get("suggestions", []),
            "quantification_suggestions": result.get("quantification_suggestions", []),
            }
    except RuntimeError:
        raise
    except Exception as e:
        print(f"Error analyzing bullet: {e}")
        return {
            "quality_score": None,
            "feedback": "Error analyzing bullet.",
            "rewrite_ats": None,
            "rewrite_strong": None,
            "suggestions": [],
            "quantification_suggestions": [],
            }

def analyze_bullet_with_llm(bullet: str, job_description: str) -> dict: 
    '''
    Option 2: analyze a resume bullet point in the context of a specific job description,
        providing feedback on relevance and suggestions for improvement based on the job requirements.

        Args: 
            bullet: the resume bullet point to analyze
            job_description: the full text of the job description to use as context for analysis
        Returns:
            a dictionary with the analysis results, including relevance_score, feedback, rewrite_ats, rewrite_strong, and missing_keywords'''
    

    prompt = f'''
    Analyze this resume bullet point in the context of the following job description.
    Evaluate how well the bullet point matches the job requirements and provide specific feedback on relevance,
    missing keywords
   
    RESUME_BULLET:
    {bullet}
    JOB_DESCRIPTION:
    {job_description}
    
    Return a JSON object with exactly these fields:
{{
        "relevance_score": <integer 0-100 reflecting how well the bullet matches the job requirements>,
        "feedback": <specific, actionable feedback — 2-3 sentences on what works and what doesn't>,
        "rewrite_ats": <rewritten bullet optimized for ATS keyword formatting>,
        "rewrite_strong": <rewritten bullet optimized for impact with strong verbs and quantification>,
        "missing_keywords": <list of keywords from the job description that are not present in the bullet>
    }}
'''
    
    try: 
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT, schema=BulletMatchPayload)
        result = raw
        return {
            "relevance_score": result.get("relevance_score"),
            "feedback": result.get("feedback"),
            "rewrite_ats": result.get("rewrite_ats"),
            "rewrite_strong": result.get("rewrite_strong"),
            "missing_keywords": result.get("missing_keywords", []),
            }
    except RuntimeError:
        raise
    except Exception as e:
        print(f"Error analyzing bullet: {e}")
        return {
            "relevance_score": None,
            "feedback": "Error analyzing bullet.",
            "rewrite_ats": None,
            "rewrite_strong": None,
            "missing_keywords": [],
            }

def score_resume_against_jd(resume_text: str, job_description: str) -> dict:
    """
    Option 2 (full resume): Score a full resume against a job description.

    Args:
        resume_text: Full resume as plain text
        job_description: The full job description text

    Returns:
        dict with overall_score, summary, strengths, gaps, missing_keywords, and recommendation
    """
    prompt = f"""You are evaluating a full resume against a job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return a JSON object with exactly these fields:
{{
    "is_resume": <true only when the first document is actually a resume or CV>,
    "overall_score": <integer 0-100 reflecting overall resume fit for the role>,
    "summary": <2-3 sentence overall assessment>,
    "strengths": <list of 3-5 specific strengths relevant to this JD>,
    "gaps": <list of 3-5 specific gaps or missing qualifications>,
    "missing_keywords": <list of up to 10 important keywords from the JD missing in the resume>,
    "recommendation": <one of: "Strong Match", "Good Match", "Partial Match", "Weak Match">
}}

If the first document is not a resume or CV, set is_resume to false, explain what
the document appears to be in summary, set overall_score to null, return empty
lists, and set recommendation to null. Do not calculate a match score."""

    try:
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1024, schema=JobMatchPayload)
        result = raw

        return {
            "is_resume": bool(result.get("is_resume", True)),
            "overall_score": result.get("overall_score"),
            "summary": result.get("summary", ""),
            "strengths": result.get("strengths", []),
            "gaps": result.get("gaps", []),
            "missing_keywords": result.get("missing_keywords", []),
            "recommendation": result.get("recommendation", "Partial Match"),
        }

    except RuntimeError:
        raise
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return {
            "overall_score": 0,
            "summary": "Scoring failed. Please try again.",
            "strengths": [],
            "gaps": [],
            "missing_keywords": [],
            "recommendation": "Unknown",
            "error": str(e),
        }







