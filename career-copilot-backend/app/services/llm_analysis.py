import json 
from services.llm_service import call_llm_json

SYSTEM_PROMPT = '''
You are a master resume coach and ATS (Applicant Tracking System) optimization expert. 
Your task is to analyze individual bullet points from a resume in the context of a specific job description and provide feedback 
on how well each bullet point matches the job requirements.
ALWAYS respond with a JSON object that includes the following fields:
- relevance_score: a number between 0 and 100 indicating how relevant the bullet point is
- feedback: a brief explanation of why the bullet point received its relevance score
- rewrite_ats: a rewritten version of the bullet point optimized for ATS, incorporating relevant keywords from the job description
- rewrite_strong: a rewritten version of the bullet point optimized for human readers, emphasizing impact and achievements
- missing_keywords: a list of important keywords from the job description that are not present in the original bullet point
Make sure to provide constructive feedback and actionable suggestions for improvement. 
'''

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
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT)
        result = json.loads(raw)

        return {
            "quality_score": result.get("quality_score"),
            "feedback": result.get("feedback"),
            "rewrite_ats": result.get("rewrite_ats"),
            "rewrite_strong": result.get("rewrite_strong"),
            "suggestions": result.get("suggestions", []),
            "quantification_suggestions": result.get("quantification_suggestions", []),
            }
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
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT)
        result = json.loads(raw)
        return {
            "relevance_score": result.get("relevance_score"),
            "feedback": result.get("feedback"),
            "rewrite_ats": result.get("rewrite_ats"),
            "rewrite_strong": result.get("rewrite_strong"),
            "missing_keywords": result.get("missing_keywords", []),
            }
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
    "overall_score": <integer 0-100 reflecting overall resume fit for the role>,
    "summary": <2-3 sentence overall assessment>,
    "strengths": <list of 3-5 specific strengths relevant to this JD>,
    "gaps": <list of 3-5 specific gaps or missing qualifications>,
    "missing_keywords": <list of up to 10 important keywords from the JD missing in the resume>,
    "recommendation": <one of: "Strong Match", "Good Match", "Partial Match", "Weak Match">
}}"""

    try:
        raw = call_llm_json(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=1024)
        result = json.loads(raw)

        return {
            "overall_score": int(result.get("overall_score", 0)),
            "summary": result.get("summary", ""),
            "strengths": result.get("strengths", []),
            "gaps": result.get("gaps", []),
            "missing_keywords": result.get("missing_keywords", []),
            "recommendation": result.get("recommendation", "Partial Match"),
        }

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







